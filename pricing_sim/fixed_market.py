"""Reviewer-driven corrected three-layer market.

This module is a self-contained, switchable re-implementation of the three-layer
candidate-response simulation used in the SCI main paper. It exists so that the
reviewer fixes (M1 rigid-demand J-scaling, M3 missing no-purchase outside option,
M4 smooth QoS shapes) can be turned on independently while leaving the original
``intermediary_market`` / ``three_stage_game`` modules untouched.

Design contract (do NOT break):
  * With ``MarketFix()`` defaults (all fixes OFF) the numbers MUST match the
    original artifacts bit-for-bit. ``run_fidelity_check`` enforces this.
  * Each fix is an independent boolean so we can attribute the change in results
    to a specific reviewer concern.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Literal

import numpy as np
from scipy.optimize import minimize
from scipy.special import expit, logsumexp

from .intermediary_market import IntermediaryConfig


FIXED_POINT_MAX_ITERATIONS = 200
FIXED_POINT_TOLERANCE = 1e-9
QOS_DAMPING = 0.35
MIN_CAPACITY = 1e-6
NASH_MAX_SWEEPS = 24
NASH_STRATEGY_TOLERANCE = 1e-5
NASH_REGRET_TOLERANCE = 1e-3

QoSShape = Literal["threshold", "linear", "sigmoid", "sqrt"]


@dataclass(frozen=True)
class MarketFix:
    """Switches for the reviewer-driven corrections.

    fix_rigid_scaling : M1. When True the rigid/replay arrival is normalised
        *within* a period by the channel's relative share, so total rigid arrival
        is invariant to the number of intermediaries J. When False the original
        (buggy) ``rigid_baseline[t] * sigmoid * sum_k s[k,t]`` is reproduced.
    outside_option : M3. When True an explicit no-purchase alternative with
        deterministic utility ``outside_utility`` enters the logit denominator,
        so negative utilities actually shed demand instead of being renormalised
        away. The same option is used to compute the inclusive value, so profit
        and exit probability live in ONE consistent model.
    qos_shape : M4. Degradation functional form. "threshold" is the original
        flat-then-Gaussian form; the rest are genuinely smooth alternatives.
    """

    fix_rigid_scaling: bool = False
    outside_option: bool = False
    outside_utility: float = 0.0
    qos_shape: QoSShape = "threshold"

    @property
    def tag(self) -> str:
        bits = []
        bits.append("rigidfix" if self.fix_rigid_scaling else "rigidraw")
        bits.append("outside" if self.outside_option else "nooutside")
        bits.append(self.qos_shape)
        return "+".join(bits)


@dataclass(frozen=True)
class FixedResult:
    policy: str
    fix_tag: str
    wholesale_prices: np.ndarray
    retail_prices: np.ndarray
    capacity: np.ndarray
    shares: np.ndarray
    demand: np.ndarray
    utilization: np.ndarray
    qos: np.ndarray
    platform_revenue: float
    intermediary_profit: float
    system_profit: float
    inclusive_value: float
    exit_probability: float
    active_min_qos: float
    demand_weighted_qos: float
    avg_retail_price: float
    diagnostics: dict


# --------------------------------------------------------------------------- #
# QoS shapes (M4)
# --------------------------------------------------------------------------- #
def qos_factor(util: np.ndarray, config: IntermediaryConfig, shape: QoSShape) -> np.ndarray:
    u = np.asarray(util, dtype=float)
    ubar = config.qos_threshold
    if shape == "threshold":
        excess = np.maximum(u - ubar, 0.0)
        return np.exp(-config.qos_strength * excess * excess)
    if shape == "linear":
        # Continuous degradation starting well below the peak; q(1.0)~0.
        ubar_low = 0.5
        c_lin = 1.0 / (1.0 - ubar_low)
        return np.clip(1.0 - c_lin * np.maximum(u - ubar_low, 0.0), 0.0, 1.0)
    if shape == "sigmoid":
        kappa_s = 30.0
        return 1.0 / (1.0 + np.exp(kappa_s * (u - ubar)))
    if shape == "sqrt":
        kappa_r = 2.5
        return np.clip(1.0 - kappa_r * np.sqrt(np.maximum(u - ubar, 0.0)), 0.0, 1.0)
    raise ValueError(f"unknown qos_shape {shape}")


# --------------------------------------------------------------------------- #
# User layer: logit shares (+ optional outside option) and demand
# --------------------------------------------------------------------------- #
def _utilities(retail: np.ndarray, qos: np.ndarray, config: IntermediaryConfig) -> np.ndarray:
    time_term = np.log(config.time_preference + 1e-10)[None, :]
    brand_term = np.log(config.brand_quality + 1e-10)[:, None]
    move_cost = config.inconvenience_cost * (1.0 - config.native_period_distribution)[None, :]
    utility = -config.price_sensitivity * (retail + move_cost - config.base_retail_price)
    utility = utility + time_term + brand_term - config.qos_feedback_weight * (1.0 - qos)
    return utility


def _choice_shares(
    retail: np.ndarray,
    qos: np.ndarray,
    config: IntermediaryConfig,
    fix: MarketFix,
) -> np.ndarray:
    """Return logit shares over (j,t). With outside option the shares sum to
    < 1; the residual mass is the no-purchase probability and is intentionally
    NOT reallocated to the inside options."""
    utility = _utilities(retail, qos, config)
    if fix.outside_option:
        # Stable softmax including a no-purchase alternative with fixed utility.
        flat = utility.ravel()
        all_u = np.concatenate([flat, [fix.outside_utility]])
        m = np.max(all_u)
        exp_all = np.exp(all_u - m)
        denom = float(np.sum(exp_all))
        inside = exp_all[:-1] / denom
        return inside.reshape(utility.shape)
    exp_utility = np.exp(utility - np.max(utility))
    return exp_utility / np.sum(exp_utility)


def _demand_from_shares(
    shares: np.ndarray,
    retail: np.ndarray,
    config: IntermediaryConfig,
    fix: MarketFix,
) -> np.ndarray:
    period_share = np.sum(shares, axis=0)  # sum over intermediaries -> (T,)
    avg_price = float(np.sum(shares * retail))
    growth = 1.0 + config.market_growth * max(config.base_retail_price - avg_price, 0.0)
    flexible = config.flexible_baseline * growth * shares
    rigid_response = expit(config.rigid_churn_rate * (config.rigid_wtp - retail))

    if fix.fix_rigid_scaling:
        # M1 fix (minimal, level-preserving): give channel j its OWN share s[j,t]
        # instead of the whole-period aggregate sum_k s[k,t]. Then
        #   sum_j rigid[j,t] = rigid_baseline[t]*response*period_share[t],
        # which is invariant to the number of intermediaries J (period_share[t] is
        # the period's total inside mass, ~J-invariant). With J=1 this is identical
        # to the original, so the single-intermediary baseline is unchanged.
        rigid = config.rigid_baseline[None, :] * rigid_response * shares
    else:
        # Original (buggy) behaviour: every channel multiplied by whole-period share,
        # so total rigid demand scales ~linearly with J.
        rigid = config.rigid_baseline[None, :] * rigid_response * period_share[None, :]
    return rigid + flexible


def _inclusive_value(retail: np.ndarray, qos: np.ndarray, config: IntermediaryConfig, fix: MarketFix) -> float:
    utility = _utilities(retail, qos, config)
    flat = utility.ravel()
    if fix.outside_option:
        all_u = np.concatenate([flat, [fix.outside_utility]])
        return float(logsumexp(all_u))
    return float(logsumexp(flat))


def _exit_probability(retail: np.ndarray, qos: np.ndarray, config: IntermediaryConfig, fix: MarketFix) -> float:
    """Probability mass on the no-purchase option. With the outside option this is
    a *real* model quantity; without it we report the same diagnostic the original
    paper used (1/(1+exp(IV))) so the two models are comparable."""
    utility = _utilities(retail, qos, config)
    flat = utility.ravel()
    if fix.outside_option:
        all_u = np.concatenate([flat, [fix.outside_utility]])
        m = np.max(all_u)
        denom = float(np.sum(np.exp(all_u - m)))
        return float(np.exp(fix.outside_utility - m) / denom)
    iv = float(logsumexp(flat))
    return float(1.0 / (1.0 + np.exp(iv)))


def evaluate_policy(
    wholesale: np.ndarray,
    retail: np.ndarray,
    capacity: np.ndarray,
    config: IntermediaryConfig,
    fix: MarketFix,
    *,
    policy: str = "candidate",
    qos_aware: bool = True,
) -> FixedResult:
    shape = fix.qos_shape
    eff_strength = config.qos_strength if qos_aware else 0.0
    eval_config = config if qos_aware else replace(config, qos_strength=0.0)

    qos = np.ones_like(retail, dtype=float)
    converged = False
    iterations = 0
    for iterations in range(1, FIXED_POINT_MAX_ITERATIONS + 1):
        shares = _choice_shares(retail, qos, config, fix)
        demand = _demand_from_shares(shares, retail, config, fix)
        utilization = demand / np.maximum(capacity, 1e-8)
        target_qos = qos_factor(utilization, eval_config, shape)
        residual = float(np.max(np.abs(target_qos - qos)))
        if residual <= FIXED_POINT_TOLERANCE:
            converged = True
            break
        qos = QOS_DAMPING * target_qos + (1.0 - QOS_DAMPING) * qos
    if not converged:
        shares = _choice_shares(retail, qos, config, fix)
        demand = _demand_from_shares(shares, retail, config, fix)

    # Profit is computed under the QoS the search actually sees: during the no-QoS
    # search (qos_aware=False) the iterated qos stays at 1 (eval_config strength=0),
    # reproducing the original "search assumes q=1" convention. The final policy is
    # re-evaluated with qos_aware=True, where the iterated qos IS the true degradation.
    utilization = demand / np.maximum(capacity, 1e-8)
    true_qos = qos

    hours = config.period_hours
    platform_revenue = float(np.sum(wholesale[None, :] * demand * true_qos * hours))
    retail_revenue = float(np.sum(retail * demand * true_qos * hours))
    capacity_cost = float(np.sum(config.capacity_cost * capacity * hours))
    qos_cost = float(np.sum(config.degrade_cost * (1.0 - true_qos) * demand * hours))
    intermediary_profit = retail_revenue - platform_revenue - capacity_cost - qos_cost
    system_profit = platform_revenue + intermediary_profit

    active = demand > 1e-6
    active_min_qos = float(np.min(true_qos[active])) if np.any(active) else 1.0
    dw = float(np.sum(true_qos * demand) / np.sum(demand)) if np.sum(demand) > 0 else 1.0

    return FixedResult(
        policy=policy,
        fix_tag=fix.tag,
        wholesale_prices=np.asarray(wholesale, float),
        retail_prices=np.asarray(retail, float),
        capacity=np.asarray(capacity, float),
        shares=np.asarray(shares, float),
        demand=np.asarray(demand, float),
        utilization=np.asarray(utilization, float),
        qos=np.asarray(true_qos, float),
        platform_revenue=platform_revenue,
        intermediary_profit=intermediary_profit,
        system_profit=system_profit,
        inclusive_value=_inclusive_value(retail, true_qos, config, fix),
        exit_probability=_exit_probability(retail, true_qos, config, fix),
        active_min_qos=active_min_qos,
        demand_weighted_qos=dw,
        avg_retail_price=float(np.mean(retail)),
        diagnostics={
            "converged": converged,
            "iterations": iterations,
            "min_qos": float(np.min(true_qos)),
            "max_utilization": float(np.max(utilization)),
        },
    )


# --------------------------------------------------------------------------- #
# Middle + platform layers (same SLSQP / candidate-ranking logic as original)
# --------------------------------------------------------------------------- #
def _default_capacity(config: IntermediaryConfig) -> np.ndarray:
    pref = config.time_preference / np.sum(config.time_preference)
    return config.intermediary_capacity[:, None] * pref[None, :]


def _intermediary_profit_idx(result: FixedResult, config: IntermediaryConfig, idx: int) -> float:
    hours = config.period_hours
    margin = result.retail_prices[idx] - result.wholesale_prices
    effective = result.demand[idx] * result.qos[idx]
    revenue = float(np.sum(margin * effective * hours))
    capacity_cost = float(np.sum(config.capacity_cost * result.capacity[idx] * hours))
    qos_cost = float(np.sum(config.degrade_cost * (1.0 - result.qos[idx]) * result.demand[idx] * hours))
    return revenue - capacity_cost - qos_cost


def _best_response(
    idx: int,
    wholesale: np.ndarray,
    retail: np.ndarray,
    capacity: np.ndarray,
    config: IntermediaryConfig,
    fix: MarketFix,
    *,
    qos_aware: bool,
):
    periods = config.num_periods
    evals = 0

    def objective(values: np.ndarray) -> float:
        nonlocal evals
        evals += 1
        r = retail.copy()
        c = capacity.copy()
        r[idx] = values[:periods]
        c[idx] = values[periods:]
        res = evaluate_policy(wholesale, r, c, config, fix, qos_aware=qos_aware)
        return -_intermediary_profit_idx(res, config, idx)

    x0 = np.concatenate([retail[idx], capacity[idx]])
    price_bounds = [(config.retail_lower_bound, config.retail_upper_bound)] * periods
    cap_bounds = [(MIN_CAPACITY, float(config.intermediary_capacity[idx]))] * periods
    cons = ({"type": "eq", "fun": lambda v: np.sum(v[periods:]) - config.intermediary_capacity[idx]},)
    res = minimize(
        objective, x0, method="SLSQP",
        bounds=price_bounds + cap_bounds, constraints=cons,
        options={"maxiter": config.optimizer_maxiter, "ftol": 1e-9, "disp": False},
    )
    return res.x[:periods], res.x[periods:], -float(res.fun), evals, bool(res.success)


def solve_middle_stage(
    wholesale: np.ndarray,
    config: IntermediaryConfig,
    fix: MarketFix,
    *,
    qos_aware: bool,
    policy: str,
):
    retail = np.maximum(
        np.tile(wholesale[None, :] + 0.32, (config.num_intermediaries, 1)),
        config.retail_lower_bound,
    )
    capacity = _default_capacity(config)
    evals = 0
    iteration = 0
    for iteration in range(1, NASH_MAX_SWEEPS + 1):
        prev = np.concatenate([retail.ravel(), capacity.ravel()])
        for idx in range(config.num_intermediaries):
            r, c, _, e, _ = _best_response(idx, wholesale, retail, capacity, config, fix, qos_aware=qos_aware)
            retail[idx] = r
            capacity[idx] = c
            evals += e
        change = float(np.max(np.abs(np.concatenate([retail.ravel(), capacity.ravel()]) - prev)))
        if change <= NASH_STRATEGY_TOLERANCE:
            break
    # The SEARCH may run under reduced QoS (qos_aware=False for the no-QoS baseline),
    # but the FINAL policy is always evaluated under the true full-strength QoS, matching
    # the original "search with kappa=0, evaluate with full kappa" convention.
    final = evaluate_policy(wholesale, retail, capacity, config, fix, policy=policy, qos_aware=True)

    # max regret
    max_regret = 0.0
    for idx in range(config.num_intermediaries):
        _, _, br_profit, e, _ = _best_response(idx, wholesale, retail, capacity, config, fix, qos_aware=qos_aware)
        cur = _intermediary_profit_idx(final, config, idx)
        max_regret = max(max_regret, br_profit - cur)
        evals += e
    final.diagnostics.update({"max_regret": max(0.0, max_regret), "objective_evaluations": evals, "middle_iterations": iteration})
    return final, max(0.0, max_regret)


def optimize_three_layer(
    config: IntermediaryConfig,
    fix: MarketFix,
    *,
    qos_aware: bool = True,
    policy: str = "three_layer_qos_aware",
) -> FixedResult:
    rng = np.random.default_rng(config.random_seed)
    best: FixedResult | None = None
    for trial in range(config.optimizer_trials):
        if trial == 0:
            wholesale = np.full(config.num_periods, config.base_wholesale_price)
        else:
            wholesale = rng.uniform(config.wholesale_lower_bound, config.wholesale_upper_bound, config.num_periods)
        cand, _ = solve_middle_stage(wholesale, config, fix, qos_aware=qos_aware, policy=policy)
        if best is None or cand.platform_revenue > best.platform_revenue:
            best = cand
    assert best is not None
    return best


def _single_config(config: IntermediaryConfig) -> IntermediaryConfig:
    data = {**config.__dict__}
    data["intermediary_capacity"] = np.array([float(np.sum(config.intermediary_capacity))])
    data["brand_quality"] = np.array([1.0])
    return IntermediaryConfig.default(**data)


def run_baselines(config: IntermediaryConfig, fix: MarketFix) -> dict[str, FixedResult]:
    full_cap = _default_capacity(config)
    wholesale = np.full(config.num_periods, config.base_wholesale_price)
    retail = np.full((config.num_intermediaries, config.num_periods), config.base_retail_price)

    single_cfg = _single_config(config)
    single_cap = _default_capacity(single_cfg)
    single_retail = np.full((1, config.num_periods), config.base_retail_price)

    uniform = evaluate_policy(wholesale, retail, full_cap, config, fix, policy="uniform_retail")
    single = evaluate_policy(
        np.full(single_cfg.num_periods, single_cfg.base_wholesale_price),
        single_retail, single_cap, single_cfg, fix, policy="single_intermediary",
    )
    no_qos = optimize_three_layer(config, fix, qos_aware=False, policy="no_qos_pricing")
    three = optimize_three_layer(config, fix, qos_aware=True, policy="three_layer_qos_aware")
    return {
        "uniform_retail": uniform,
        "single_intermediary": single,
        "no_qos_pricing": no_qos,
        "three_layer_qos_aware": three,
    }
