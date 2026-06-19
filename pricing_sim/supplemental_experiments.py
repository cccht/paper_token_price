from __future__ import annotations

from dataclasses import replace
from itertools import product
from time import perf_counter

import numpy as np

from .config import SimulationConfig
from .economics import PolicyEvaluation, evaluate_policy
from .optimize import OptimizationResult, optimize_qos_aware, uniform_pricing
from .projection import project_bounded_mean


def _row(name: str, result: OptimizationResult) -> dict[str, float | str]:
    return {
        "policy": name,
        "profit": result.policy.profit,
        "welfare": result.policy.welfare,
        "posted_bill": result.policy.posted_bill,
        "effective_bill": result.policy.effective_bill,
        "min_qos": float(np.min(result.policy.qos)),
        "max_utilization": float(np.max(result.policy.utilization)),
        "cap_residual": result.diagnostics.cap_residual,
        "solver_success": result.diagnostics.solver_success,
    }


def _rule_result(raw: np.ndarray, config: SimulationConfig) -> PolicyEvaluation:
    prices = project_bounded_mean(
        raw,
        cap=config.posted_price_cap,
        lower=config.price_lower_bound,
        upper=config.price_upper_bound,
    )
    return evaluate_policy(prices, config)


def _rule_row(name: str, policy: PolicyEvaluation, config: SimulationConfig) -> dict[str, float | str]:
    return {
        "policy": name,
        "profit": policy.profit,
        "welfare": policy.welfare,
        "posted_bill": policy.posted_bill,
        "effective_bill": policy.effective_bill,
        "min_qos": float(np.min(policy.qos)),
        "max_utilization": float(np.max(policy.utilization)),
        "cap_residual": abs(float(np.mean(policy.prices)) - config.posted_price_cap),
    }


def rule_baseline_records(config: SimulationConfig) -> list[dict[str, float | str]]:
    centered_load = config.rigid_baseline - float(np.mean(config.rigid_baseline))
    scale = float(np.std(config.rigid_baseline))
    normalized = centered_load / scale if scale else centered_load
    time_of_use = _rule_result(config.posted_price_cap + 0.25 * normalized, config)
    queue_aware = _rule_result(config.posted_price_cap + 0.45 * normalized, config)
    best_observed = optimize_qos_aware(config, seed=42)
    return [
        _row("uniform", uniform_pricing(config)),
        _rule_row("time_of_use", time_of_use, config),
        _rule_row("queue_aware", queue_aware, config),
        _row("best_observed", best_observed),
    ]


def billing_ablation_records(config: SimulationConfig) -> list[dict[str, float | str]]:
    rows = []
    for mode in ("effective", "full", "sla_penalty"):
        varied = replace(config, billing_mode=mode)
        row = _row("qos_aware", optimize_qos_aware(varied, seed=42))
        row["billing_mode"] = mode
        rows.append(row)
    return rows


def constraint_ablation_records(config: SimulationConfig) -> list[dict[str, float | str]]:
    uniform_bill = uniform_pricing(config).policy.posted_bill
    variants = (
        ("fixed_mean", config),
        (
            "fixed_mean_with_bill_protection",
            replace(config, enforce_bill_protection=True),
        ),
    )
    rows = []
    for name, varied in variants:
        result = optimize_qos_aware(varied, seed=42)
        row = _row("qos_aware", result)
        row.update({
            "constraint_mode": name,
            "posted_bill": result.policy.posted_bill,
            "bill_ratio_vs_uniform": result.policy.posted_bill / uniform_bill,
        })
        rows.append(row)
    return rows


def empirical_profile_records(
    config: SimulationConfig,
    *,
    profiles: tuple[tuple[str, float, float], ...],
) -> list[dict[str, float | str]]:
    variants = (("synthetic_default", config.qos_threshold, config.qos_strength),) + profiles
    rows = []
    for name, threshold, strength in variants:
        varied = replace(config, qos_threshold=threshold, qos_strength=strength)
        row = _row("qos_aware", optimize_qos_aware(varied, seed=42))
        row.update({"profile": name, "qos_threshold": threshold, "qos_strength": strength})
        rows.append(row)
    return rows


def _resample(values: np.ndarray, periods: int) -> np.ndarray:
    source = np.linspace(0.0, 1.0, len(values))
    target = np.linspace(0.0, 1.0, periods)
    return np.interp(target, source, values)


def coarse_grid_reference_records(
    config: SimulationConfig,
    *,
    periods: int = 4,
    grid_step: float = 0.05,
) -> list[dict[str, float | int]]:
    varied = replace(
        config,
        rigid_baseline=_resample(config.rigid_baseline, periods),
        time_preference=_resample(config.time_preference, periods),
    )
    levels = np.arange(
        varied.price_lower_bound,
        varied.price_upper_bound + grid_step / 2.0,
        grid_step,
    )
    target_sum = periods * varied.posted_price_cap
    grid_profit = float("-inf")
    feasible_points = 0
    for prefix in product(levels, repeat=periods - 1):
        last_price = target_sum - sum(prefix)
        if not varied.price_lower_bound <= last_price <= varied.price_upper_bound:
            continue
        feasible_points += 1
        prices = np.array((*prefix, last_price), dtype=float)
        grid_profit = max(grid_profit, evaluate_policy(prices, varied).profit)
    slsqp = optimize_qos_aware(varied, seed=42).policy
    return [{
        "periods": periods,
        "grid_step": grid_step,
        "feasible_grid_points": feasible_points,
        "grid_profit": grid_profit,
        "slsqp_profit": slsqp.profit,
        "slsqp_advantage_vs_grid": slsqp.profit / grid_profit - 1.0,
    }]


def scalability_records(
    config: SimulationConfig,
    *,
    period_counts: tuple[int, ...] = (8, 16, 32, 64),
    trial_counts: tuple[int, ...] = (5, 20, 40),
) -> list[dict[str, float | int]]:
    rows = []
    for periods in period_counts:
        for trials in trial_counts:
            varied = replace(
                config,
                rigid_baseline=_resample(config.rigid_baseline, periods),
                time_preference=_resample(config.time_preference, periods),
                optimizer_trials=trials,
            )
            started = perf_counter()
            result = optimize_qos_aware(varied, seed=42)
            rows.append({
                "periods": periods,
                "optimizer_trials": trials,
                "runtime_seconds": perf_counter() - started,
                "profit": result.policy.profit,
                "objective_evaluations": result.diagnostics.objective_evaluations,
                "cap_residual": result.diagnostics.cap_residual,
            })
    return rows


def fairness_records(config: SimulationConfig) -> list[dict[str, float | str]]:
    policy = optimize_qos_aware(config, seed=42).policy
    segments = (("low_sensitivity", 1.0), ("medium_sensitivity", 3.5), ("high_sensitivity", 8.0))
    rows = []
    for name, sensitivity in segments:
        varied = replace(config, price_sensitivity=sensitivity)
        evaluation = evaluate_policy(policy.prices, varied)
        effective_prices = evaluation.prices * evaluation.qos
        rows.append({
            "segment": name,
            "price_sensitivity": sensitivity,
            "mean_effective_price": float(np.mean(effective_prices)),
            "mean_qos": float(np.mean(evaluation.qos)),
            "effective_spending": float(np.sum(
                evaluation.prices * evaluation.demand.total * evaluation.qos * config.period_hours
            )),
            "rigid_consumer_surplus": evaluation.welfare_components["rigid_consumer_surplus"],
            "flexible_consumer_surplus": evaluation.welfare_components["flexible_consumer_surplus"],
        })
    return rows
