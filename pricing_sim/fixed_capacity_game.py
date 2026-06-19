"""Fixed-capacity ablation solver for the three-stage pricing game."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize

from .intermediary_market import IntermediaryConfig, ThreeLayerResult, _default_capacity, evaluate_three_layer_policy
from .three_stage_game import (
    NASH_MAX_SWEEPS,
    NASH_REGRET_TOLERANCE,
    NASH_STRATEGY_TOLERANCE,
    _candidate_wholesale,
    _intermediary_profit,
)


@dataclass(frozen=True)
class FixedCapacityResult:
    policy: ThreeLayerResult
    max_regret: float
    iterations: int
    objective_evaluations: int


def optimize_fixed_capacity_stackelberg(config: IntermediaryConfig) -> ThreeLayerResult:
    rng = np.random.default_rng(config.random_seed)
    best: ThreeLayerResult | None = None
    evaluations = 0
    for trial in range(config.optimizer_trials):
        wholesale = _candidate_wholesale(config, rng, trial)
        middle = solve_fixed_capacity_middle(wholesale, config)
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
        "capacity_strategic": False,
    })
    return best


def solve_fixed_capacity_middle(wholesale: np.ndarray, config: IntermediaryConfig) -> FixedCapacityResult:
    retail = np.maximum(
        np.tile(wholesale[None, :] + 0.32, (config.num_intermediaries, 1)),
        config.retail_lower_bound,
    )
    capacity = _default_capacity(config)
    evaluations = 0
    for iteration in range(1, NASH_MAX_SWEEPS + 1):
        previous = retail.copy()
        all_success = True
        for idx in range(config.num_intermediaries):
            row, _, row_evals, success = _best_response(idx, wholesale, retail, capacity, config)
            retail[idx] = row
            evaluations += row_evals
            all_success = all_success and success
        change = float(np.max(np.abs(retail - previous)))
        if all_success and change <= NASH_STRATEGY_TOLERANCE:
            break
    final = evaluate_three_layer_policy(wholesale, retail, capacity, config, policy="fixed_capacity_qos_aware")
    regret, regret_evals = _max_regret(wholesale, retail, capacity, config)
    evaluations += regret_evals
    final.diagnostics.update({
        "middle_iterations": iteration,
        "max_nash_regret": regret,
        "nash_tolerance": NASH_REGRET_TOLERANCE,
        "nash_converged": regret <= NASH_REGRET_TOLERANCE,
        "capacity_strategic": False,
        "objective_evaluations": evaluations,
    })
    return FixedCapacityResult(final, regret, iteration, evaluations)


def _best_response(
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
        candidate = retail.copy()
        candidate[idx] = values
        result = evaluate_three_layer_policy(wholesale, candidate, capacity, config)
        return -_intermediary_profit(result, config, idx)

    result = minimize(
        objective,
        retail[idx],
        method="SLSQP",
        bounds=[(config.retail_lower_bound, config.retail_upper_bound)] * config.num_periods,
        options={"maxiter": config.optimizer_maxiter, "ftol": 1e-9, "disp": False},
    )
    return np.asarray(result.x, dtype=float), -float(result.fun), evaluations, bool(result.success)


def _max_regret(
    wholesale: np.ndarray,
    retail: np.ndarray,
    capacity: np.ndarray,
    config: IntermediaryConfig,
) -> tuple[float, int]:
    current = evaluate_three_layer_policy(wholesale, retail, capacity, config)
    max_regret = 0.0
    evaluations = 0
    for idx in range(config.num_intermediaries):
        _, profit, row_evals, _ = _best_response(idx, wholesale, retail, capacity, config)
        current_profit = _intermediary_profit(current, config, idx)
        max_regret = max(max_regret, profit - current_profit)
        evaluations += row_evals
    return max(0.0, float(max_regret)), evaluations
