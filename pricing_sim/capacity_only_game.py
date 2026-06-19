"""Capacity-only ablation solver for the three-stage pricing game."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize

from .intermediary_market import IntermediaryConfig, ThreeLayerResult, _default_capacity, evaluate_three_layer_policy
from .three_stage_game import NASH_MAX_SWEEPS, NASH_REGRET_TOLERANCE, NASH_STRATEGY_TOLERANCE, _intermediary_profit


@dataclass(frozen=True)
class CapacityOnlyResult:
    policy: ThreeLayerResult
    max_regret: float
    iterations: int
    objective_evaluations: int


def optimize_capacity_only(config: IntermediaryConfig) -> ThreeLayerResult:
    wholesale = np.full(config.num_periods, config.base_wholesale_price)
    retail = np.full((config.num_intermediaries, config.num_periods), config.base_retail_price)
    middle = solve_capacity_only_middle(wholesale, retail, config)
    result = middle.policy
    result.diagnostics.update({
        "objective_evaluations": middle.objective_evaluations,
        "platform_objective": "fixed_base_wholesale",
        "platform_trials": 1,
        "random_seed": config.random_seed,
        "capacity_strategic": True,
        "retail_strategic": False,
    })
    return result


def solve_capacity_only_middle(
    wholesale: np.ndarray,
    retail: np.ndarray,
    config: IntermediaryConfig,
) -> CapacityOnlyResult:
    capacity = _default_capacity(config)
    evaluations = 0
    for iteration in range(1, NASH_MAX_SWEEPS + 1):
        previous = capacity.copy()
        all_success = True
        for idx in range(config.num_intermediaries):
            row, profit, row_evals, success = _best_capacity_response(idx, wholesale, retail, capacity, config)
            capacity[idx] = row
            evaluations += row_evals
            all_success = all_success and success and np.isfinite(profit)
        change = float(np.max(np.abs(capacity - previous)))
        if all_success and change <= NASH_STRATEGY_TOLERANCE:
            break
    final = evaluate_three_layer_policy(wholesale, retail, capacity, config, policy="capacity_only_fixed_price")
    regret, regret_evals = _max_capacity_regret(wholesale, retail, capacity, config)
    evaluations += regret_evals
    final.diagnostics.update({
        "middle_iterations": iteration,
        "max_nash_regret": regret,
        "nash_tolerance": NASH_REGRET_TOLERANCE,
        "nash_converged": regret <= NASH_REGRET_TOLERANCE,
        "capacity_strategic": True,
        "retail_strategic": False,
        "objective_evaluations": evaluations,
    })
    return CapacityOnlyResult(final, regret, iteration, evaluations)


def _best_capacity_response(
    idx: int,
    wholesale: np.ndarray,
    retail: np.ndarray,
    capacity: np.ndarray,
    config: IntermediaryConfig,
) -> tuple[np.ndarray, float, int, bool]:
    evaluations = 0

    def objective(values: np.ndarray) -> float:
        nonlocal evaluations
        evaluations += 1
        candidate = capacity.copy()
        candidate[idx] = values
        result = evaluate_three_layer_policy(wholesale, retail, candidate, config)
        return -_intermediary_profit(result, config, idx)

    result = minimize(
        objective,
        capacity[idx],
        method="SLSQP",
        bounds=[(1e-6, float(config.intermediary_capacity[idx]))] * config.num_periods,
        constraints=({"type": "eq", "fun": lambda values: np.sum(values) - config.intermediary_capacity[idx]},),
        options={"maxiter": config.optimizer_maxiter, "ftol": 1e-9, "disp": False},
    )
    return np.asarray(result.x, dtype=float), -float(result.fun), evaluations, bool(result.success)


def _max_capacity_regret(
    wholesale: np.ndarray,
    retail: np.ndarray,
    capacity: np.ndarray,
    config: IntermediaryConfig,
) -> tuple[float, int]:
    current = evaluate_three_layer_policy(wholesale, retail, capacity, config)
    max_regret = 0.0
    evaluations = 0
    for idx in range(config.num_intermediaries):
        _, profit, row_evals, _ = _best_capacity_response(idx, wholesale, retail, capacity, config)
        current_profit = _intermediary_profit(current, config, idx)
        max_regret = max(max_regret, profit - current_profit)
        evaluations += row_evals
    return max(0.0, float(max_regret)), evaluations
