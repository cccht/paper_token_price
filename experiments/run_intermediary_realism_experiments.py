"""Run realism-oriented validation experiments for the intermediary game."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
import sys
from typing import Any

import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
for import_path in (PROJECT_ROOT, SCRIPT_DIR):
    path_text = str(import_path)
    if path_text not in sys.path:
        sys.path.insert(0, path_text)

from pricing_sim.calibration import fit_qos_curve, load_controlled_aggregate
from pricing_sim.intermediary_market import (
    IntermediaryConfig,
    ThreeLayerResult,
    _default_capacity,
    evaluate_three_layer_policy,
)
from pricing_sim.three_stage_game import optimize_three_stage_stackelberg


DEFAULT_TRIALS = 4
DEFAULT_MAXITER = 70
DEMAND_SCALES = (1.0, 1.15, 1.30)
USER_PROTECTED_RETAIL_CAP = 0.80
USER_PROTECTED_WHOLESALE_CAP = 0.80
ARRIVAL_SOURCE = Path("artifacts/vllm-study/20260531-190126/arrival_summary.csv")
CALIBRATION_SOURCES = (
    ("vllm-0.5b", Path("artifacts/vllm-study/20260531-190126/controlled_aggregate.csv")),
    ("vllm-3b", Path("artifacts/vllm-study-qwen25-3b/20260531-214710/controlled_aggregate.csv")),
)
ACTIVE_DEMAND_FRACTION = 1e-3


def _jsonable(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    return value


def _read_csv_rows(path: Path) -> list[dict[str, float]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return [{key: float(value) for key, value in row.items()} for row in csv.DictReader(handle)]


def _write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    keys = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def arrival_rate_pattern(rows: list[dict[str, float]], periods: int) -> np.ndarray:
    rates = np.array([row["arrival_rate_rps"] for row in rows], dtype=float)
    if rates.size == 0 or np.any(rates <= 0.0):
        raise ValueError("arrival rates must be positive")
    if rates.size == 1:
        pattern = np.repeat(rates[0], periods)
    else:
        source_x = np.linspace(0.0, 1.0, rates.size)
        target_x = np.linspace(0.0, 1.0, periods)
        pattern = np.interp(target_x, source_x, rates)
    return pattern / float(np.mean(pattern))


def scaled_market_config(
    config: IntermediaryConfig,
    *,
    demand_scale: float = 1.0,
    capacity_scale: float = 1.0,
    arrival_pattern: np.ndarray | None = None,
    qos_threshold: float | None = None,
    qos_strength: float | None = None,
) -> IntermediaryConfig:
    data = {**config.__dict__}
    pattern = np.ones(config.num_periods) if arrival_pattern is None else np.asarray(arrival_pattern, dtype=float)
    if pattern.shape != config.rigid_baseline.shape or np.any(pattern <= 0.0):
        raise ValueError("arrival_pattern must match periods and be positive")
    data["rigid_baseline"] = config.rigid_baseline * demand_scale * pattern
    data["flexible_baseline"] = config.flexible_baseline * demand_scale
    data["intermediary_capacity"] = config.intermediary_capacity * capacity_scale
    data["time_preference"] = config.time_preference * pattern / float(np.max(pattern))
    data["native_period_distribution"] = config.native_period_distribution * pattern
    if qos_threshold is not None:
        data["qos_threshold"] = qos_threshold
    if qos_strength is not None:
        data["qos_strength"] = qos_strength
    return IntermediaryConfig.default(**data)


def uniform_result(config: IntermediaryConfig) -> ThreeLayerResult:
    wholesale = np.full(config.num_periods, config.base_wholesale_price)
    retail = np.full((config.num_intermediaries, config.num_periods), config.base_retail_price)
    return evaluate_three_layer_policy(wholesale, retail, _default_capacity(config), config, policy="uniform_retail")


def user_protected_config(config: IntermediaryConfig) -> IntermediaryConfig:
    data = {**config.__dict__}
    data["retail_upper_bound"] = min(config.retail_upper_bound, USER_PROTECTED_RETAIL_CAP)
    data["wholesale_upper_bound"] = min(config.wholesale_upper_bound, USER_PROTECTED_WHOLESALE_CAP)
    return IntermediaryConfig.default(**data)


def _active_mask(result: ThreeLayerResult) -> np.ndarray:
    cutoff = max(float(np.max(result.demand)) * ACTIVE_DEMAND_FRACTION, 1e-8)
    return result.demand >= cutoff


def _inclusive_value(result: ThreeLayerResult, config: IntermediaryConfig) -> float:
    retail = result.retail_prices
    time_term = np.log(config.time_preference + 1e-10)[None, :]
    brand_term = np.log(config.brand_quality + 1e-10)[:, None]
    move_cost = config.inconvenience_cost * (1.0 - config.native_period_distribution)[None, :]
    utility = -config.price_sensitivity * (retail + move_cost - config.base_retail_price)
    utility += time_term + brand_term - config.qos_feedback_weight * (1.0 - result.qos)
    shifted = utility - float(np.max(utility))
    return float(np.max(utility) + np.log(np.sum(np.exp(shifted))))


def market_metric_row(
    label: str,
    result: ThreeLayerResult,
    config: IntermediaryConfig,
    *,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    demand_sum = max(float(np.sum(result.demand)), 1e-12)
    active = _active_mask(result)
    row = {
        "policy": label,
        "platform_revenue": result.platform_revenue,
        "intermediary_profit": result.intermediary_profit,
        "system_profit": result.system_profit,
        "total_demand": float(np.sum(result.demand)),
        "average_retail_price": float(np.sum(result.retail_prices * result.demand) / demand_sum),
        "inclusive_value": _inclusive_value(result, config),
        "min_qos": float(np.min(result.qos)),
        "active_min_qos": float(np.min(result.qos[active])),
        "demand_weighted_qos": float(np.sum(result.demand * result.qos) / demand_sum),
        "max_utilization": float(np.max(result.utilization)),
        "max_nash_regret": result.diagnostics.get("max_nash_regret", ""),
    }
    row.update(extra or {})
    return row


def _add_uniform_deltas(row: dict[str, Any], reference: dict[str, Any]) -> dict[str, Any]:
    row["platform_revenue_gain_vs_uniform"] = row["platform_revenue"] - reference["platform_revenue"]
    row["inclusive_value_gain_vs_uniform"] = row["inclusive_value"] - reference["inclusive_value"]
    row["demand_weighted_qos_gain_vs_uniform"] = row["demand_weighted_qos"] - reference["demand_weighted_qos"]
    row["active_min_qos_gain_vs_uniform"] = row["active_min_qos"] - reference["active_min_qos"]
    return row


def _calibrated_profiles(project_root: Path) -> list[dict[str, Any]]:
    profiles: list[dict[str, Any]] = []
    for name, relative in CALIBRATION_SOURCES:
        source = project_root / relative
        if not source.exists():
            continue
        fit = fit_qos_curve(load_controlled_aggregate(source))
        profiles.append({"profile": name, "threshold": fit.threshold, "strength": fit.strength, "rmse": fit.rmse})
    if not profiles:
        raise FileNotFoundError("No vLLM calibration aggregate files were found.")
    return profiles


def welfare_comparison_rows(*, trials: int, maxiter: int) -> list[dict[str, Any]]:
    config = IntermediaryConfig.default(optimizer_trials=trials, optimizer_maxiter=maxiter)
    rows = [market_metric_row("uniform_retail", uniform_result(config), config, extra={"experiment": "welfare"})]
    for label, aware in (("no_qos_pricing", False), ("three_layer_qos_aware", True)):
        result = optimize_three_stage_stackelberg(config, qos_aware=aware, policy=label)
        rows.append(market_metric_row(label, result, config, extra={"experiment": "welfare"}))
    return rows


def user_protected_revenue_rows(*, trials: int, maxiter: int) -> list[dict[str, Any]]:
    base = IntermediaryConfig.default(optimizer_trials=trials, optimizer_maxiter=maxiter)
    uniform = market_metric_row(
        "uniform_retail",
        uniform_result(base),
        base,
        extra={"experiment": "user_protected_revenue"},
    )
    unconstrained = optimize_three_stage_stackelberg(base, policy="three_layer_qos_aware")
    protected_config = user_protected_config(base)
    protected = optimize_three_stage_stackelberg(protected_config, policy="user_protected_revenue")
    rows = [
        uniform,
        market_metric_row("three_layer_qos_aware", unconstrained, base, extra={"experiment": "user_protected_revenue"}),
        market_metric_row("user_protected_revenue", protected, protected_config, extra={
            "experiment": "user_protected_revenue",
            "retail_price_cap": USER_PROTECTED_RETAIL_CAP,
            "wholesale_price_cap": USER_PROTECTED_WHOLESALE_CAP,
        }),
    ]
    return [_add_uniform_deltas(row, uniform) for row in rows]


def vllm_pressure_rows(project_root: Path, *, trials: int, maxiter: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    base = IntermediaryConfig.default(optimizer_trials=trials, optimizer_maxiter=maxiter)
    for profile in _calibrated_profiles(project_root):
        for scale in DEMAND_SCALES:
            config = scaled_market_config(
                base,
                demand_scale=scale,
                qos_threshold=profile["threshold"],
                qos_strength=profile["strength"],
            )
            result = optimize_three_stage_stackelberg(config, policy="three_layer_qos_aware")
            rows.append(market_metric_row("three_layer_qos_aware", result, config, extra={
                "experiment": "vllm_pressure",
                "profile": profile["profile"],
                "demand_scale": scale,
                "calibration_rmse": profile["rmse"],
            }))
    return rows


def arrival_replay_rows(project_root: Path, *, trials: int, maxiter: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    base = IntermediaryConfig.default(optimizer_trials=trials, optimizer_maxiter=maxiter)
    pattern = arrival_rate_pattern(_read_csv_rows(project_root / ARRIVAL_SOURCE), base.num_periods)
    config = scaled_market_config(base, arrival_pattern=pattern)
    rows.append(market_metric_row("uniform_retail", uniform_result(config), config, extra={"experiment": "arrival_replay"}))
    for label, aware in (("no_qos_pricing", False), ("three_layer_qos_aware", True)):
        result = optimize_three_stage_stackelberg(config, qos_aware=aware, policy=label)
        rows.append(market_metric_row(label, result, config, extra={"experiment": "arrival_replay"}))
    return rows


def run_experiments(project_root: Path, *, trials: int, maxiter: int) -> dict[str, list[dict[str, Any]]]:
    return {
        "welfare_comparison": welfare_comparison_rows(trials=trials, maxiter=maxiter),
        "user_protected_revenue": user_protected_revenue_rows(trials=trials, maxiter=maxiter),
        "vllm_pressure": vllm_pressure_rows(project_root, trials=trials, maxiter=maxiter),
        "arrival_replay": arrival_replay_rows(project_root, trials=trials, maxiter=maxiter),
    }


def write_artifacts(results: dict[str, list[dict[str, Any]]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "realism_experiment_records.json").write_text(
        json.dumps(_jsonable(results), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    for name, rows in results.items():
        _write_csv(rows, output_dir / f"{name}.csv")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, default=PROJECT_ROOT / "artifacts" / "intermediary_realism")
    parser.add_argument("--trials", type=int, default=DEFAULT_TRIALS)
    parser.add_argument("--maxiter", type=int, default=DEFAULT_MAXITER)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    output_dir = args.output_root / datetime.now().strftime("%Y%m%d-%H%M%S")
    write_artifacts(run_experiments(PROJECT_ROOT, trials=args.trials, maxiter=args.maxiter), output_dir)
    print(f"output={output_dir}")


if __name__ == "__main__":
    main()
