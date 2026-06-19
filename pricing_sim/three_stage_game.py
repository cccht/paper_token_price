from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize

from .intermediary_market import (
    IntermediaryConfig,
    ThreeLayerResult,
    _default_capacity,
    evaluate_three_layer_policy,
)


NASH_MAX_SWEEPS = 24
NASH_STRATEGY_TOLERANCE = 1e-5
NASH_REGRET_TOLERANCE = 1e-3
MIN_CAPACITY = 1e-6


@dataclass(frozen=True)
class MiddleStageResult:
    policy: ThreeLayerResult
    max_regret: float
    iterations: int
    converged: bool
    objective_evaluations: int


@dataclass(frozen=True)
class _GameState:
    wholesale: np.ndarray
    retail: np.ndarray
    capacity: np.ndarray
    config: IntermediaryConfig


@dataclass(frozen=True)
class _BestResponse:
    retail: np.ndarray
    capacity: np.ndarray
    profit: float
    evaluations: int
    success: bool


def solve_middle_stage_nash(
    wholesale: np.ndarray,
    config: IntermediaryConfig,
    *,
    qos_aware: bool = True,
    congestion_proxy_weight: float = 0.0,
    policy: str = "middle_stage_nash",
) -> MiddleStageResult:
    retail, capacity = _initial_middle_strategy(wholesale, config)
    evaluations = 0
    converged = False
    for iteration in range(1, NASH_MAX_SWEEPS + 1):
        previous = _flatten_strategy(retail, capacity)
        all_success = True
        for idx in range(config.num_intermediaries):
            state = _GameState(wholesale, retail, capacity, config)
            response = _best_response(
                idx,
                state,
                qos_aware=qos_aware,
                congestion_proxy_weight=congestion_proxy_weight,
            )
            retail[idx] = response.retail
            capacity[idx] = response.capacity
            evaluations += response.evaluations
            all_success = all_success and response.success
        change = float(np.max(np.abs(_flatten_strategy(retail, capacity) - previous)))
        if all_success and change <= NASH_STRATEGY_TOLERANCE:
            converged = True
            break
    final = evaluate_three_layer_policy(wholesale, retail, capacity, config, policy=policy)
    regret, regret_evaluations = _max_regret(
        wholesale,
        retail,
        capacity,
        config,
        qos_aware=qos_aware,
        congestion_proxy_weight=congestion_proxy_weight,
    )
    evaluations += regret_evaluations
    nash_converged = regret <= NASH_REGRET_TOLERANCE
    final.diagnostics.update({
        "middle_converged": converged or nash_converged,
        "middle_strategy_converged": converged,
        "nash_converged": nash_converged,
        "middle_iterations": iteration,
        "max_nash_regret": regret,
        "nash_tolerance": NASH_REGRET_TOLERANCE,
        "capacity_strategic": True,
        "congestion_proxy_weight": congestion_proxy_weight,
        "objective_evaluations": evaluations,
    })
    return MiddleStageResult(final, regret, iteration, converged or nash_converged, evaluations)


def optimize_three_stage_stackelberg(
    config: IntermediaryConfig,
    *,
    qos_aware: bool = True,
    congestion_proxy_weight: float = 0.0,
    policy: str = "three_layer_qos_aware",
) -> ThreeLayerResult:
    rng = np.random.default_rng(config.random_seed)
    best: ThreeLayerResult | None = None
    evaluations = 0
    for trial in range(config.optimizer_trials):
        wholesale = _candidate_wholesale(config, rng, trial)
        middle = solve_middle_stage_nash(
            wholesale,
            config,
            qos_aware=qos_aware,
            congestion_proxy_weight=congestion_proxy_weight,
            policy=policy,
        )
        evaluations += middle.objective_evaluations
        candidate = middle.policy
        if best is None or candidate.platform_revenue > best.platform_revenue:
            best = candidate
    assert best is not None
    best.diagnostics.update({
        "objective_evaluations": evaluations,
        "platform_objective": "platform_revenue",
        "platform_trials": config.optimizer_trials,
        "random_seed": config.random_seed,
        "qos_aware_search": qos_aware,
        "congestion_proxy_weight": congestion_proxy_weight,
    })
    return best


def optimize_congestion_proxy_stackelberg(
    config: IntermediaryConfig,
    *,
    proxy_weight: float | None = None,
    policy: str = "congestion_proxy_pricing",
) -> ThreeLayerResult:
    weight = config.degrade_cost if proxy_weight is None else float(proxy_weight)
    return optimize_three_stage_stackelberg(
        config,
        qos_aware=False,
        congestion_proxy_weight=weight,
        policy=policy,
    )


def _initial_middle_strategy(
    wholesale: np.ndarray,
    config: IntermediaryConfig,
) -> tuple[np.ndarray, np.ndarray]:
    retail = np.maximum(
        np.tile(wholesale[None, :] + 0.32, (config.num_intermediaries, 1)),
        config.retail_lower_bound,
    )
    return retail, _default_capacity(config)


def _best_response(
    idx: int,
    state: _GameState,
    *,
    qos_aware: bool,
    congestion_proxy_weight: float = 0.0,
) -> _BestResponse:
    evaluations = 0
    search_config = _search_config(state.config, qos_aware=qos_aware)
    initial = np.concatenate([state.retail[idx], state.capacity[idx]])

    def objective(values: np.ndarray) -> float:
        nonlocal evaluations
        evaluations += 1
        retail, capacity = _replace_row(idx, values, state)
        result = evaluate_three_layer_policy(state.wholesale, retail, capacity, search_config)
        return -_intermediary_profit(
            result,
            search_config,
            idx,
            congestion_proxy_weight=congestion_proxy_weight,
        )

    result = minimize(
        objective,
        initial,
        method="SLSQP",
        bounds=_strategy_bounds(state.config, idx),
        constraints=({"type": "eq", "fun": lambda values: np.sum(values[state.config.num_periods:]) - state.config.intermediary_capacity[idx]},),
        options={"maxiter": state.config.optimizer_maxiter, "ftol": 1e-9, "disp": False},
    )
    retail, capacity = _split_strategy(result.x, state.config)
    return _BestResponse(retail, capacity, -float(result.fun), evaluations, bool(result.success))


def _max_regret(
    wholesale: np.ndarray,
    retail: np.ndarray,
    capacity: np.ndarray,
    config: IntermediaryConfig,
    *,
    qos_aware: bool,
    congestion_proxy_weight: float = 0.0,
) -> tuple[float, int]:
    state = _GameState(wholesale, retail.copy(), capacity.copy(), config)
    search_config = _search_config(config, qos_aware=qos_aware)
    current = evaluate_three_layer_policy(wholesale, retail, capacity, search_config)
    max_regret = 0.0
    evaluations = 0
    for idx in range(config.num_intermediaries):
        response = _best_response(
            idx,
            state,
            qos_aware=qos_aware,
            congestion_proxy_weight=congestion_proxy_weight,
        )
        current_profit = _intermediary_profit(
            current,
            search_config,
            idx,
            congestion_proxy_weight=congestion_proxy_weight,
        )
        max_regret = max(max_regret, response.profit - current_profit)
        evaluations += response.evaluations
    return max(0.0, float(max_regret)), evaluations


def _replace_row(
    idx: int,
    values: np.ndarray,
    state: _GameState,
) -> tuple[np.ndarray, np.ndarray]:
    retail = state.retail.copy()
    capacity = state.capacity.copy()
    retail[idx], capacity[idx] = _split_strategy(values, state.config)
    return retail, capacity


def _split_strategy(
    values: np.ndarray,
    config: IntermediaryConfig,
) -> tuple[np.ndarray, np.ndarray]:
    periods = config.num_periods
    retail = np.asarray(values[:periods], dtype=float)
    capacity = np.asarray(values[periods:], dtype=float)
    return retail, capacity


def _strategy_bounds(
    config: IntermediaryConfig,
    idx: int,
) -> list[tuple[float, float]]:
    price_bounds = [(config.retail_lower_bound, config.retail_upper_bound)] * config.num_periods
    capacity_bounds = [(MIN_CAPACITY, float(config.intermediary_capacity[idx]))] * config.num_periods
    return price_bounds + capacity_bounds


def _intermediary_profit(
    result: ThreeLayerResult,
    config: IntermediaryConfig,
    idx: int,
    *,
    congestion_proxy_weight: float = 0.0,
) -> float:
    hours = config.period_hours
    retail_margin = result.retail_prices[idx] - result.wholesale_prices
    effective = result.demand[idx] * result.qos[idx]
    revenue = float(np.sum(retail_margin * effective * hours))
    capacity_cost = float(np.sum(config.capacity_cost * result.capacity[idx] * hours))
    qos_cost = float(np.sum(config.degrade_cost * (1.0 - result.qos[idx]) * result.demand[idx] * hours))
    proxy_cost = _congestion_proxy_cost(result, config, idx, congestion_proxy_weight)
    return revenue - capacity_cost - qos_cost - proxy_cost


def _congestion_proxy_cost(
    result: ThreeLayerResult,
    config: IntermediaryConfig,
    idx: int,
    weight: float,
) -> float:
    if weight <= 0.0:
        return 0.0
    overload = np.maximum(result.utilization[idx] - config.qos_threshold, 0.0)
    return float(np.sum(weight * overload * overload * result.demand[idx] * config.period_hours))


def _search_config(
    config: IntermediaryConfig,
    *,
    qos_aware: bool,
) -> IntermediaryConfig:
    if qos_aware:
        return config
    return IntermediaryConfig.default(**{**config.__dict__, "qos_strength": 0.0})


def _flatten_strategy(retail: np.ndarray, capacity: np.ndarray) -> np.ndarray:
    return np.concatenate([retail.ravel(), capacity.ravel()])


def _candidate_wholesale(
    config: IntermediaryConfig,
    rng: np.random.Generator,
    trial: int,
) -> np.ndarray:
    if trial == 0:
        return np.full(config.num_periods, config.base_wholesale_price)
    return rng.uniform(config.wholesale_lower_bound, config.wholesale_upper_bound, config.num_periods)
