from __future__ import annotations

from dataclasses import dataclass, replace
import warnings

import numpy as np
from scipy.optimize import minimize

from .config import SimulationConfig
from .economics import PolicyEvaluation, evaluate_policy
from .projection import project_bounded_mean


@dataclass(frozen=True)
class OptimizerDiagnostics:
    success: bool
    solver_success: bool
    message: str
    objective_evaluations: int
    cap_residual: float
    lower_bound_residual: float
    upper_bound_residual: float
    bill_cap_residual: float


@dataclass(frozen=True)
class OptimizationResult:
    policy: PolicyEvaluation
    diagnostics: OptimizerDiagnostics
    search_qos_strength: float
    evaluation_qos_strength: float


def _project(raw: np.ndarray, config: SimulationConfig) -> np.ndarray:
    return project_bounded_mean(
        raw,
        cap=config.posted_price_cap,
        lower=config.price_lower_bound,
        upper=config.price_upper_bound,
    )


def _diagnostics(
    policy: PolicyEvaluation,
    *,
    success: bool,
    solver_success: bool,
    message: str,
    objective_evaluations: int,
    config: SimulationConfig,
) -> OptimizerDiagnostics:
    prices = policy.prices
    bill_cap = _uniform_posted_bill(config) * config.bill_cap_ratio
    return OptimizerDiagnostics(
        success=success,
        solver_success=solver_success,
        message=message,
        objective_evaluations=objective_evaluations,
        cap_residual=abs(float(np.mean(prices)) - config.posted_price_cap),
        lower_bound_residual=max(config.price_lower_bound - float(np.min(prices)), 0.0),
        upper_bound_residual=max(float(np.max(prices)) - config.price_upper_bound, 0.0),
        bill_cap_residual=(
            max(policy.posted_bill - bill_cap, 0.0)
            if config.enforce_bill_protection else 0.0
        ),
    )


def _initial_prices(config: SimulationConfig, rng: np.random.Generator, trial: int) -> np.ndarray:
    if trial == 0:
        raw = np.full(config.num_periods, config.posted_price_cap)
    else:
        raw = rng.uniform(config.price_lower_bound, config.price_upper_bound, config.num_periods)
    return _project(raw, config)


def _uniform_posted_bill(config: SimulationConfig) -> float:
    prices = np.full(config.num_periods, config.posted_price_cap)
    return evaluate_policy(prices, config).posted_bill


def _constraints(config: SimulationConfig) -> list[dict]:
    constraints = [{
        "type": "eq",
        "fun": lambda prices: np.mean(prices) - config.posted_price_cap,
    }]
    if config.enforce_bill_protection:
        bill_cap = _uniform_posted_bill(config) * config.bill_cap_ratio
        constraints.append({
            "type": "ineq",
            "fun": lambda prices: bill_cap - evaluate_policy(prices, config).posted_bill,
        })
    return constraints


def _is_feasible(prices: np.ndarray, config: SimulationConfig, *, tolerance: float = 1e-6) -> bool:
    if abs(float(np.mean(prices)) - config.posted_price_cap) > tolerance:
        return False
    if float(np.min(prices)) < config.price_lower_bound - tolerance:
        return False
    if float(np.max(prices)) > config.price_upper_bound + tolerance:
        return False
    if config.enforce_bill_protection:
        bill_cap = _uniform_posted_bill(config) * config.bill_cap_ratio
        if evaluate_policy(prices, config).posted_bill > bill_cap + tolerance:
            return False
    return True


def _search(config: SimulationConfig, seed: int) -> tuple[np.ndarray, bool, bool, str, int]:
    rng = np.random.default_rng(seed)
    best_prices = _initial_prices(config, rng, 0)
    best_profit = evaluate_policy(best_prices, config).profit
    evaluations = 1
    best_success = False
    best_solver_success = False
    best_message = "no successful optimizer candidate"
    constraints = _constraints(config)

    for trial in range(config.optimizer_trials):
        initial = _initial_prices(config, rng, trial)

        def objective(prices: np.ndarray) -> float:
            return -evaluate_policy(prices, config).profit

        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                message="Values in x were outside bounds during a minimize step",
                category=RuntimeWarning,
            )
            result = minimize(
                objective,
                initial,
                method="SLSQP",
                bounds=[(config.price_lower_bound, config.price_upper_bound)] * config.num_periods,
                constraints=constraints,
                options={"maxiter": config.optimizer_maxiter, "ftol": 1e-10},
            )
        evaluations += int(result.nfev)
        prices = _project(result.x, config)
        profit = evaluate_policy(prices, config).profit
        candidate_feasible = _is_feasible(prices, config)
        candidate_solver_success = bool(result.success)
        prefer_candidate = (
            not best_success
            or (candidate_solver_success and not best_solver_success)
            or (candidate_solver_success == best_solver_success and profit > best_profit)
        )
        if candidate_feasible and prefer_candidate:
            best_prices, best_profit = prices, profit
            best_success = True
            best_solver_success = candidate_solver_success
            best_message = str(result.message)
    return best_prices, best_success, best_solver_success, best_message, evaluations


def optimize_qos_aware(config: SimulationConfig, *, seed: int = 42) -> OptimizationResult:
    prices, success, solver_success, message, evaluations = _search(config, seed)
    policy = evaluate_policy(prices, config)
    diagnostics = _diagnostics(
        policy,
        success=success,
        solver_success=solver_success,
        message=message,
        objective_evaluations=evaluations,
        config=config,
    )
    return OptimizationResult(policy, diagnostics, config.qos_strength, config.qos_strength)


def optimize_myopic(config: SimulationConfig, *, seed: int = 42) -> OptimizationResult:
    search_config = replace(config, qos_strength=0.0)
    prices, success, solver_success, message, evaluations = _search(search_config, seed)
    policy = evaluate_policy(prices, config)
    diagnostics = _diagnostics(
        policy,
        success=success,
        solver_success=solver_success,
        message=message,
        objective_evaluations=evaluations,
        config=config,
    )
    return OptimizationResult(policy, diagnostics, 0.0, config.qos_strength)


def uniform_pricing(config: SimulationConfig) -> OptimizationResult:
    prices = np.full(config.num_periods, config.posted_price_cap)
    policy = evaluate_policy(prices, config)
    diagnostics = _diagnostics(
        policy,
        success=True,
        solver_success=True,
        message="uniform baseline",
        objective_evaluations=1,
        config=config,
    )
    return OptimizationResult(policy, diagnostics, config.qos_strength, config.qos_strength)
