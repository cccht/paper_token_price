from __future__ import annotations

from dataclasses import asdict, replace
from typing import Any, Iterable

import numpy as np

from .config import SimulationConfig
from .optimize import OptimizationResult, optimize_myopic, optimize_qos_aware, uniform_pricing


def _jsonable(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def _record(
    experiment: str,
    policy_name: str,
    result: OptimizationResult,
    config: SimulationConfig,
    *,
    seed: int | None,
    parameter: str | None = None,
    parameter_value: float | None = None,
) -> dict[str, Any]:
    return _jsonable({
        "experiment": experiment,
        "policy": policy_name,
        "seed": seed,
        "parameter": parameter,
        "parameter_value": parameter_value,
        "config": asdict(config),
        "diagnostics": asdict(result.diagnostics),
        "search_qos_strength": result.search_qos_strength,
        "evaluation_qos_strength": result.evaluation_qos_strength,
        "policy_evaluation": asdict(result.policy),
    })


def _baseline_records(config: SimulationConfig, seed: int) -> list[dict[str, Any]]:
    return [
        _record("baseline", "uniform", uniform_pricing(config), config, seed=None),
        _record("baseline", "myopic", optimize_myopic(config, seed=seed), config, seed=seed),
        _record("baseline", "qos_aware", optimize_qos_aware(config, seed=seed), config, seed=seed),
    ]


def run_smoke_matrix(config: SimulationConfig) -> list[dict[str, Any]]:
    return _baseline_records(config, seed=42)


def _sweep(
    config: SimulationConfig,
    *,
    experiment: str,
    parameter: str,
    values: Iterable[float],
    seed: int,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for value in values:
        varied = replace(config, **{parameter: value})
        for policy_name, result in [
            ("uniform", uniform_pricing(varied)),
            ("myopic", optimize_myopic(varied, seed=seed)),
            ("qos_aware", optimize_qos_aware(varied, seed=seed)),
        ]:
            records.append(_record(
                experiment,
                policy_name,
                result,
                varied,
                seed=None if policy_name == "uniform" else seed,
                parameter=parameter,
                parameter_value=float(value),
            ))
    return records


def run_full_matrix(config: SimulationConfig) -> list[dict[str, Any]]:
    records = _baseline_records(config, seed=42)
    for seed in range(10):
        records.append(_record(
            "seed_stability",
            "qos_aware",
            optimize_qos_aware(config, seed=seed),
            config,
            seed=seed,
        ))
    sweeps = [
        ("price_cap", "posted_price_cap", [0.60, 0.80, 1.00, 1.20]),
        ("qos_strength", "qos_strength", [0.0, 5.0, 15.0, 30.0]),
        ("qos_threshold", "qos_threshold", [0.75, 0.82, 0.90]),
        ("capacity", "capacity", [750.0, 950.0, 1200.0]),
        ("elasticity", "price_sensitivity", [1.0, 3.5, 8.0]),
        ("shift_cost", "inconvenience_cost", [0.05, 0.20, 0.80]),
        ("market_growth", "market_growth", [0.0, 2.5, 6.0]),
        ("churn_cost", "churn_future_cost", [0.0, 0.60, 1.20]),
        ("qos_feedback", "qos_feedback_weight", [0.0, 1.0, 2.0]),
    ]
    for experiment, parameter, values in sweeps:
        records.extend(_sweep(
            config,
            experiment=experiment,
            parameter=parameter,
            values=values,
            seed=42,
        ))
    return records
