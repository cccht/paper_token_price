from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize
from scipy.special import expit

from .intermediary_market import IntermediaryConfig, qos_factor

FIXED_POINT_MAX_ITERATIONS = 200
FIXED_POINT_TOLERANCE = 1e-9
QOS_DAMPING = 0.35
MIN_CAPACITY = 1e-6


@dataclass(frozen=True)
class TwoLayerResult:
    policy: str
    retail_prices: np.ndarray
    capacity: np.ndarray
    shares: np.ndarray
    demand: np.ndarray
    utilization: np.ndarray
    qos: np.ndarray
    gross_revenue: float
    capacity_cost: float
    qos_cost: float
    system_profit: float
    inclusive_value: float
    diagnostics: dict[str, float | int | bool | str]


def _two_layer_choice_shares(
    retail: np.ndarray,
    qos: np.ndarray,
    config: IntermediaryConfig,
) -> np.ndarray:
    time_term = np.log(config.time_preference + 1e-10)
    move_cost = config.inconvenience_cost * (1.0 - config.native_period_distribution)
    utility = (
        -config.price_sensitivity * (retail + move_cost - config.base_retail_price)
        + time_term
        - config.qos_feedback_weight * (1.0 - qos)
    )
    exp_utility = np.exp(utility - np.max(utility))
    return exp_utility / np.sum(exp_utility)


def _two_layer_demand(
    shares: np.ndarray,
    retail: np.ndarray,
    config: IntermediaryConfig,
) -> np.ndarray:
    avg_price = float(np.sum(shares * retail))
    growth = 1.0 + config.market_growth * max(config.base_retail_price - avg_price, 0.0)
    flexible = config.flexible_baseline * growth * shares
    rigid_response = expit(config.rigid_churn_rate * (config.rigid_wtp - retail))
    rigid = config.rigid_baseline * rigid_response * shares
    return rigid + flexible


def evaluate_two_layer_policy(
    retail: np.ndarray,
    capacity: np.ndarray,
    config: IntermediaryConfig,
    *,
    policy: str = "two_layer",
) -> TwoLayerResult:
    qos = np.ones_like(retail, dtype=float)
    converged = False
    for iterations in range(1, FIXED_POINT_MAX_ITERATIONS + 1):
        shares = _two_layer_choice_shares(retail, qos, config)
        demand = _two_layer_demand(shares, retail, config)
        utilization = demand / np.maximum(capacity, 1e-8)
        target_qos = qos_factor(utilization, config)
        residual = float(np.max(np.abs(target_qos - qos)))
        if residual <= FIXED_POINT_TOLERANCE:
            converged = True
            break
        qos = QOS_DAMPING * target_qos + (1.0 - QOS_DAMPING) * qos

    if not converged:
        shares = _two_layer_choice_shares(retail, qos, config)
        demand = _two_layer_demand(shares, retail, config)

    utilization = demand / np.maximum(capacity, 1e-8)
    hours = config.period_hours
    gross_revenue = float(np.sum(retail * demand * qos * hours))
    cap_cost = float(np.sum(config.capacity_cost * capacity * hours))
    qos_penalty = float(np.sum(config.degrade_cost * (1.0 - qos) * demand * hours))

    return TwoLayerResult(
        policy=policy,
        retail_prices=np.asarray(retail, dtype=float),
        capacity=np.asarray(capacity, dtype=float),
        shares=np.asarray(shares, dtype=float),
        demand=np.asarray(demand, dtype=float),
        utilization=np.asarray(utilization, dtype=float),
        qos=np.asarray(qos, dtype=float),
        gross_revenue=gross_revenue,
        capacity_cost=cap_cost,
        qos_cost=qos_penalty,
        system_profit=gross_revenue - cap_cost - qos_penalty,
        inclusive_value=_inclusive_value(retail, qos, config),
        diagnostics={
            "converged": converged,
            "iterations": iterations,
            "min_qos": float(np.min(qos)),
            "max_utilization": float(np.max(utilization)),
            "avg_retail_price": float(np.mean(retail)),
        },
    )


def _inclusive_value(
    retail: np.ndarray,
    qos: np.ndarray,
    config: IntermediaryConfig,
) -> float:
    time_term = np.log(config.time_preference + 1e-10)
    move_cost = config.inconvenience_cost * (1.0 - config.native_period_distribution)
    utility = (
        -config.price_sensitivity * (retail + move_cost - config.base_retail_price)
        + time_term
        - config.qos_feedback_weight * (1.0 - qos)
    )
    return float(np.log(np.sum(np.exp(utility))))


def solve_two_layer_stackelberg(
    config: IntermediaryConfig,
    *,
    internalize_costs: bool = True,
    policy: str = "two_layer_stackelberg",
) -> TwoLayerResult:
    G_total = float(np.sum(config.intermediary_capacity))
    periods = config.num_periods

    p0 = np.full(periods, config.base_retail_price)
    g0 = np.maximum(
        config.time_preference / np.sum(config.time_preference) * G_total,
        MIN_CAPACITY,
    )
    g0 = g0 / np.sum(g0) * G_total
    x0 = np.concatenate([p0, g0])

    evaluations = 0

    def objective(x: np.ndarray) -> float:
        nonlocal evaluations
        evaluations += 1
        retail = np.asarray(x[:periods], dtype=float)
        capacity = np.asarray(x[periods:], dtype=float)
        result = evaluate_two_layer_policy(retail, capacity, config)
        if internalize_costs:
            return -result.system_profit
        return -result.gross_revenue

    price_bounds = [
        (config.retail_lower_bound, config.retail_upper_bound)
    ] * periods
    cap_bounds = [(MIN_CAPACITY, G_total)] * periods
    constraints = {"type": "eq", "fun": lambda x: np.sum(x[periods:]) - G_total}

    result = minimize(
        objective,
        x0,
        method="SLSQP",
        bounds=price_bounds + cap_bounds,
        constraints=constraints,
        options={"maxiter": 800, "ftol": 1e-12},
    )

    retail_opt = np.asarray(result.x[:periods], dtype=float)
    capacity_opt = np.asarray(result.x[periods:], dtype=float)

    final = evaluate_two_layer_policy(retail_opt, capacity_opt, config, policy=policy)
    final.diagnostics.update({
        "success": bool(result.success),
        "objective_evaluations": evaluations,
        "solver_message": str(result.message),
        "internalize_costs": internalize_costs,
    })
    return final


def solve_two_layer_restricted(
    config: IntermediaryConfig,
    *,
    price_cap: float = 0.80,
    policy: str = "two_layer_protected",
) -> TwoLayerResult:
    G_total = float(np.sum(config.intermediary_capacity))
    periods = config.num_periods

    p0 = np.full(periods, min(config.base_retail_price, price_cap))
    g0 = np.maximum(
        config.time_preference / np.sum(config.time_preference) * G_total,
        MIN_CAPACITY,
    )
    g0 = g0 / np.sum(g0) * G_total
    x0 = np.concatenate([p0, g0])

    evaluations = 0

    def objective(x: np.ndarray) -> float:
        nonlocal evaluations
        evaluations += 1
        retail = np.asarray(x[:periods], dtype=float)
        capacity = np.asarray(x[periods:], dtype=float)
        result = evaluate_two_layer_policy(retail, capacity, config)
        return -result.system_profit

    price_bounds = [(config.retail_lower_bound, price_cap)] * periods
    cap_bounds = [(MIN_CAPACITY, G_total)] * periods
    constraints = {"type": "eq", "fun": lambda x: np.sum(x[periods:]) - G_total}

    result = minimize(
        objective,
        x0,
        method="SLSQP",
        bounds=price_bounds + cap_bounds,
        constraints=constraints,
        options={"maxiter": 800, "ftol": 1e-12},
    )

    retail_opt = np.asarray(result.x[:periods], dtype=float)
    capacity_opt = np.asarray(result.x[periods:], dtype=float)

    final = evaluate_two_layer_policy(retail_opt, capacity_opt, config, policy=policy)
    final.diagnostics.update({
        "success": bool(result.success),
        "objective_evaluations": evaluations,
        "price_cap": price_cap,
    })
    return final


def run_two_layer_baselines(
    config: IntermediaryConfig,
) -> dict[str, TwoLayerResult]:
    G_total = float(np.sum(config.intermediary_capacity))
    periods = config.num_periods

    uniform_retail = np.full(periods, config.base_retail_price)
    uniform_cap = np.maximum(
        config.time_preference / np.sum(config.time_preference) * G_total,
        MIN_CAPACITY,
    )
    uniform_cap = uniform_cap / np.sum(uniform_cap) * G_total

    results: dict[str, TwoLayerResult] = {}
    results["two_layer_uniform"] = evaluate_two_layer_policy(
        uniform_retail, uniform_cap, config, policy="two_layer_uniform"
    )
    results["two_layer_centralized"] = solve_two_layer_stackelberg(
        config, internalize_costs=True, policy="two_layer_centralized"
    )
    results["two_layer_revenue_only"] = solve_two_layer_stackelberg(
        config, internalize_costs=False, policy="two_layer_revenue_only"
    )
    results["two_layer_user_protected"] = solve_two_layer_restricted(
        config, price_cap=0.80, policy="two_layer_user_protected"
    )
    return results
