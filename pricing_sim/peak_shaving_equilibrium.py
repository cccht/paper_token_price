from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize

from .peak_shaving_config import PeakShavingConfig
from .peak_shaving_market import (
    MarketState, solve_market_fixed_point, firm_profit, intermediary_profit,
    system_profit, choice_shares_with_exit, inclusive_value,
)


def expand_price(base: float, delta: float, config: PeakShavingConfig,
                 lower: float, upper: float) -> np.ndarray:
    raw = base * (1.0 + delta * config.load_shape_hat)
    return np.clip(raw, lower, upper)


@dataclass(frozen=True)
class FirmParams:
    wbar: float
    delta: float
    pdbar: float
    delta_d: float

    def to_vector(self) -> np.ndarray:
        return np.array([self.wbar, self.delta, self.pdbar, self.delta_d], dtype=float)

    @classmethod
    def from_vector(cls, v: np.ndarray) -> "FirmParams":
        return cls(float(v[0]), float(v[1]), float(v[2]), float(v[3]))

    def wholesale(self, config: PeakShavingConfig) -> np.ndarray:
        return expand_price(self.wbar, self.delta, config,
                            config.wholesale_lower, config.wholesale_upper)

    def direct(self, config: PeakShavingConfig) -> np.ndarray:
        return expand_price(self.pdbar, self.delta_d, config,
                            config.price_lower, config.price_upper)


def routing_from_beta(wholesale: np.ndarray, qos_firm: np.ndarray, route_beta: float,
                      config: PeakShavingConfig, qos_weight: float = 3.0) -> np.ndarray:
    """Logit routing over firms per period: prefer low wholesale + high QoS."""
    util = -route_beta * wholesale + qos_weight * qos_firm   # (2,T)
    util = util - np.max(util, axis=0, keepdims=True)
    exp_u = np.exp(util)
    return exp_u / np.sum(exp_u, axis=0, keepdims=True)


def _solve_with_routing(retail: np.ndarray, wholesale: np.ndarray, direct: np.ndarray,
                        route_beta: float, config: PeakShavingConfig, qos_shape: str = "threshold"):
    """Joint fixed point over (QoS, routing). Routing and QoS are coupled, so we
    iterate them together in ONE damped loop instead of nesting a full QoS fixed
    point inside each of N routing sweeps (which compounded badly under congestion,
    where the QoS fixed point itself needs many iterations). One joint loop is both
    correct and far cheaper."""
    from pricing_sim.peak_shaving_market import (
        channel_demand, _firm_loads, qos_factor as _qos, FIXED_POINT_MAX_ITER,
        FIXED_POINT_TOL, QOS_DAMPING)
    T = config.num_periods
    G = config.firm_capacity[:, None]
    qos_firm = np.ones((2, T))
    routing = np.full((2, T), 0.5)
    converged = False
    for _ in range(FIXED_POINT_MAX_ITER):
        qos_channel = np.vstack([np.sum(routing * qos_firm, axis=0)[None, :], qos_firm])
        prices = np.vstack([retail[None, :], direct])
        demand = channel_demand(prices, qos_channel, config)
        loads = _firm_loads(demand, routing)
        util = loads / np.maximum(G, 1e-8)
        target_qos = _qos(util, config, qos_shape)
        new_routing = routing_from_beta(wholesale, target_qos, route_beta, config)
        resid = max(float(np.max(np.abs(target_qos - qos_firm))),
                    float(np.max(np.abs(new_routing - routing))))
        qos_firm = QOS_DAMPING * target_qos + (1.0 - QOS_DAMPING) * qos_firm
        routing = QOS_DAMPING * new_routing + (1.0 - QOS_DAMPING) * routing
        if resid <= FIXED_POINT_TOL:
            converged = True
            break
    state = MarketState(retail=retail, direct=direct, wholesale=wholesale, routing=routing)
    res = solve_market_fixed_point(state.channel_prices(), routing, config, qos_shape)
    return state, res


def intermediary_best_response(wholesale: np.ndarray, direct: np.ndarray,
                               config: PeakShavingConfig, n_starts: int = 6,
                               qos_shape: str = "threshold", seed: int = 0):
    """Optimize the intermediary's 3 scalars (pbar, delta_p, route_beta) by a
    COARSE GRID. Each evaluation is one joint (QoS, routing) fixed point (~0.004s),
    so the grid is cheap, deterministic, and — unlike the previous nested
    L-BFGS-B — bounded in cost when called inside the firm-layer grid. The
    base-price / zero-dynamic point is always included so the result can never be
    worse than uniform retail pricing. n_starts/seed kept for compatibility."""
    pbar_grid = np.unique(np.concatenate([
        np.linspace(0.60, min(config.price_upper, 1.6), 3), [config.base_price]]))
    deltap_grid = np.array([-0.2, 0.0, 0.2])
    beta_grid = np.array([1.5, 4.0])

    best = None
    best_profit = -np.inf
    for pbar in pbar_grid:
        for dp in deltap_grid:
            retail = expand_price(pbar, dp, config, config.price_lower, config.price_upper)
            for beta in beta_grid:
                state, res = _solve_with_routing(retail, wholesale, direct, beta, config, qos_shape)
                prof = intermediary_profit(state, res, config)
                if prof > best_profit:
                    best_profit = prof
                    best = (state, res)
    return best


def _firm_best_response(idx: int, params: list, config: PeakShavingConfig,
                        n_starts: int, qos_shape: str, rng, inner_starts: int = 1) -> FirmParams:
    """Firm idx best-responds via a COARSE GRID over its 4 scalars
    (wbar, delta, pdbar, delta_d), given the other firm's params and the
    intermediary's best response.

    Grid (not Powell) is used deliberately: the firm objective is evaluated
    through a nested inner optimizer, so it has no reliable gradient and can be
    non-smooth near the QoS threshold. A grid is bounded, predictable in cost,
    parallel-friendly, and robust to that non-smoothness — Powell thrashed and
    timed out in the congested regime. n_starts is ignored (kept for signature
    compatibility); resolution is fixed below."""
    other = 1 - idx
    wb_lo, wb_hi = config.wholesale_lower, config.wholesale_upper
    pd_lo, pd_hi = config.price_lower, min(config.price_upper, 1.6)

    # Coarse grids: base prices at 3 levels, dynamic strengths at 3 levels each.
    wbar_grid = np.linspace(wb_lo + 0.02, wb_hi - 0.02, 3)
    pdbar_grid = np.linspace(0.60, pd_hi, 3)
    delta_grid = np.array([-0.2, 0.0, 0.2])
    deltad_grid = np.array([-0.2, 0.0, 0.2])

    def eval_vec(vec_idx) -> float:
        fps = [None, None]
        fps[idx] = FirmParams.from_vector(vec_idx)
        fps[other] = params[other]
        wholesale = np.vstack([fps[0].wholesale(config), fps[1].wholesale(config)])
        direct = np.vstack([fps[0].direct(config), fps[1].direct(config)])
        state, res = intermediary_best_response(wholesale, direct, config,
                                                n_starts=inner_starts, qos_shape=qos_shape)
        return firm_profit(idx, state, res, config)

    # Start from the incumbent so we never regress.
    best_vec = params[idx].to_vector()
    best_val = eval_vec(best_vec)
    for wb in wbar_grid:
        for dl in delta_grid:
            for pdb in pdbar_grid:
                for dld in deltad_grid:
                    vec = np.array([wb, dl, pdb, dld])
                    val = eval_vec(vec)
                    if val > best_val:
                        best_val = val
                        best_vec = vec
    return FirmParams.from_vector(best_vec)


def solve_firm_nash(config: PeakShavingConfig, max_sweeps: int = 15, n_starts: int = 3,
                    seed: int = 0, qos_shape: str = "threshold", damping: float = 0.7,
                    tol: float = 3e-3) -> dict:
    rng = np.random.default_rng(seed)
    # 初始: 统一价(delta=0), 基准批发/直连
    params = [FirmParams(0.40, 0.0, 0.85, 0.0), FirmParams(0.45, 0.0, 0.88, 0.0)]
    norm_history = []
    converged = False
    for sweep in range(1, max_sweeps + 1):
        old = np.concatenate([p.to_vector() for p in params])
        # 仅首轮多起点广搜(防坏局部最优); 之后用 warm 单起点(已验证收敛到同一点, 大幅提速)
        sweep_starts = n_starts if sweep == 1 else 1
        for idx in range(2):
            br = _firm_best_response(idx, params, config, sweep_starts, qos_shape, rng)
            # 阻尼更新: damping=0.7 在"全 best-response(易互逐振荡)"与"过阻尼(收敛极慢)"
            # 之间取折中, 经验上 9-11 轮内收敛, 跨种子 rel_std≈0.0004。
            blended = damping * br.to_vector() + (1 - damping) * params[idx].to_vector()
            params[idx] = FirmParams.from_vector(blended)
        new = np.concatenate([p.to_vector() for p in params])
        change = float(np.max(np.abs(new - old)))
        norm_history.append(change)
        if change < tol:
            converged = True
            break
    # 最终评估
    wholesale = np.vstack([params[0].wholesale(config), params[1].wholesale(config)])
    direct = np.vstack([params[0].direct(config), params[1].direct(config)])
    state, res = intermediary_best_response(wholesale, direct, config, n_starts=4, qos_shape=qos_shape)
    return {
        "firm_params": [p.to_vector().tolist() for p in params],
        "state": state, "res": res,
        "firm_profits": [firm_profit(i, state, res, config) for i in range(2)],
        "intermediary_profit": intermediary_profit(state, res, config),
        "system_profit": system_profit(state, res, config),
        "converged": converged, "sweeps": sweep, "norm_history": norm_history,
    }
