from __future__ import annotations

import numpy as np

from .intermediary_market import IntermediaryConfig, ThreeLayerResult, evaluate_three_layer_policy
from .three_stage_game import (
    NASH_MAX_SWEEPS,
    NASH_REGRET_TOLERANCE,
    NASH_STRATEGY_TOLERANCE,
    _best_response,
    _candidate_wholesale,
    _flatten_strategy,
    _initial_middle_strategy,
    _intermediary_profit,
    _search_config,
    _GameState,
)


DIRECT_API_CAPACITY = 1500.0
DIRECT_API_BRAND = 1.08
DIRECT_API_RETAIL_PRICE = 0.82


def direct_api_config(
    config: IntermediaryConfig,
    *,
    direct_capacity: float = DIRECT_API_CAPACITY,
    direct_brand: float = DIRECT_API_BRAND,
) -> IntermediaryConfig:
    data = {**config.__dict__}
    data["intermediary_capacity"] = np.append(config.intermediary_capacity, direct_capacity)
    data["brand_quality"] = np.append(config.brand_quality, direct_brand)
    return IntermediaryConfig.default(**data)


def optimize_direct_access_stackelberg(
    config: IntermediaryConfig,
    *,
    direct_retail_price: float = DIRECT_API_RETAIL_PRICE,
    direct_capacity: float = DIRECT_API_CAPACITY,
    direct_brand: float = DIRECT_API_BRAND,
    qos_aware: bool = True,
    policy: str = "direct_api_user_choice",
) -> ThreeLayerResult:
    game_config = direct_api_config(config, direct_capacity=direct_capacity, direct_brand=direct_brand)
    rng = np.random.default_rng(config.random_seed)
    best: ThreeLayerResult | None = None
    evaluations = 0
    for trial in range(config.optimizer_trials):
        wholesale = _candidate_wholesale(config, rng, trial)
        candidate, evals = _solve_candidate(
            wholesale,
            game_config,
            broker_count=config.num_intermediaries,
            direct_retail_price=direct_retail_price,
            qos_aware=qos_aware,
            policy=policy,
        )
        evaluations += evals
        if best is None or candidate.platform_revenue > best.platform_revenue:
            best = candidate
    assert best is not None
    best.diagnostics.update({
        "objective_evaluations": evaluations,
        "platform_objective": "platform_revenue_with_direct_api",
        "platform_trials": config.optimizer_trials,
        "direct_api_price": direct_retail_price,
        "direct_api_capacity": direct_capacity,
        "direct_api_brand": direct_brand,
    })
    return best


def _solve_candidate(
    wholesale: np.ndarray,
    config: IntermediaryConfig,
    *,
    broker_count: int,
    direct_retail_price: float,
    qos_aware: bool,
    policy: str,
) -> tuple[ThreeLayerResult, int]:
    retail, capacity = _initial_middle_strategy(wholesale, config)
    direct_idx = config.num_intermediaries - 1
    retail[direct_idx] = direct_retail_price
    capacity[direct_idx] = _direct_capacity(config)
    evaluations = 0
    converged = False
    for iteration in range(1, NASH_MAX_SWEEPS + 1):
        previous = _flatten_strategy(retail[:broker_count], capacity[:broker_count])
        all_success = True
        for idx in range(broker_count):
            state = _GameState(wholesale, retail, capacity, config)
            response = _best_response(idx, state, qos_aware=qos_aware)
            retail[idx] = response.retail
            capacity[idx] = response.capacity
            evaluations += response.evaluations
            all_success = all_success and response.success
        current = _flatten_strategy(retail[:broker_count], capacity[:broker_count])
        if all_success and float(np.max(np.abs(current - previous))) <= NASH_STRATEGY_TOLERANCE:
            converged = True
            break
    base = evaluate_three_layer_policy(wholesale, retail, capacity, config, policy=policy)
    regret, regret_evals = _broker_regret(wholesale, retail, capacity, config, broker_count, qos_aware=qos_aware)
    result = _reaccount_direct_api(base, config, broker_count)
    result.diagnostics.update({
        "broker_count": broker_count,
        "direct_api_index": direct_idx,
        "middle_strategy_converged": converged,
        "nash_converged": regret <= NASH_REGRET_TOLERANCE,
        "max_nash_regret": regret,
        "nash_tolerance": NASH_REGRET_TOLERANCE,
        "middle_iterations": iteration,
    })
    return result, evaluations + regret_evals


def _broker_regret(
    wholesale: np.ndarray,
    retail: np.ndarray,
    capacity: np.ndarray,
    config: IntermediaryConfig,
    broker_count: int,
    *,
    qos_aware: bool,
) -> tuple[float, int]:
    state = _GameState(wholesale, retail.copy(), capacity.copy(), config)
    search_config = _search_config(config, qos_aware=qos_aware)
    current = evaluate_three_layer_policy(wholesale, retail, capacity, search_config)
    max_regret = 0.0
    evaluations = 0
    for idx in range(broker_count):
        response = _best_response(idx, state, qos_aware=qos_aware)
        current_profit = _intermediary_profit(current, search_config, idx)
        max_regret = max(max_regret, response.profit - current_profit)
        evaluations += response.evaluations
    return max(0.0, float(max_regret)), evaluations


def _direct_capacity(config: IntermediaryConfig) -> np.ndarray:
    preference = config.time_preference / np.sum(config.time_preference)
    return config.intermediary_capacity[-1] * preference


def _reaccount_direct_api(
    result: ThreeLayerResult,
    config: IntermediaryConfig,
    broker_count: int,
) -> ThreeLayerResult:
    hours = config.period_hours
    brokers = slice(0, broker_count)
    direct_idx = config.num_intermediaries - 1
    broker_effective = result.demand[brokers] * result.qos[brokers]
    wholesale_income = float(np.sum(result.wholesale_prices[None, :] * broker_effective * hours))
    direct_effective = result.demand[direct_idx] * result.qos[direct_idx]
    direct_income = float(np.sum(result.retail_prices[direct_idx] * direct_effective * hours))
    direct_capacity_cost = float(np.sum(config.capacity_cost * result.capacity[direct_idx] * hours))
    direct_qos_cost = float(np.sum(config.degrade_cost * (1.0 - result.qos[direct_idx]) * result.demand[direct_idx] * hours))
    platform_payoff = wholesale_income + direct_income - direct_capacity_cost - direct_qos_cost
    broker_profit = _broker_profit(result, config, broker_count)
    diagnostics = {**result.diagnostics}
    diagnostics["direct_api_share"] = float(np.sum(result.demand[direct_idx]) / max(np.sum(result.demand), 1e-12))
    return ThreeLayerResult(
        result.policy,
        result.wholesale_prices,
        result.retail_prices,
        result.capacity,
        result.shares,
        result.demand,
        result.utilization,
        result.qos,
        platform_payoff,
        broker_profit,
        platform_payoff + broker_profit,
        {"broker_profit": broker_profit, "direct_platform_payoff": platform_payoff},
        diagnostics,
    )


def _broker_profit(result: ThreeLayerResult, config: IntermediaryConfig, broker_count: int) -> float:
    hours = config.period_hours
    brokers = slice(0, broker_count)
    margin = result.retail_prices[brokers] - result.wholesale_prices[None, :]
    effective = result.demand[brokers] * result.qos[brokers]
    revenue = float(np.sum(margin * effective * hours))
    capacity_cost = float(np.sum(config.capacity_cost * result.capacity[brokers] * hours))
    qos_cost = float(np.sum(config.degrade_cost * (1.0 - result.qos[brokers]) * result.demand[brokers] * hours))
    return revenue - capacity_cost - qos_cost
