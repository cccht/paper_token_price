"""Run calibration-uncertainty experiments for the three-stage market."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
import sys
from typing import Any, Iterable

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
for import_path in (PROJECT_ROOT, SCRIPT_DIR):
    path_text = str(import_path)
    if path_text not in sys.path:
        sys.path.insert(0, path_text)

from experiments.run_intermediary_realism_experiments import (  # noqa: E402
    _calibrated_profiles,
    market_metric_row,
    scaled_market_config,
    uniform_result,
    user_protected_config,
)
from pricing_sim.direct_access_game import (  # noqa: E402
    direct_api_config,
    optimize_direct_access_stackelberg,
)
from pricing_sim.fixed_capacity_game import optimize_fixed_capacity_stackelberg  # noqa: E402
from pricing_sim.intermediary_market import IntermediaryConfig  # noqa: E402
from pricing_sim.three_stage_game import optimize_three_stage_stackelberg  # noqa: E402


DEFAULT_TRIALS = 3
DEFAULT_MAXITER = 60
UNCERTAINTY_VARIANTS = (
    "low_elasticity",
    "high_elasticity",
    "high_migration_cost",
    "high_capacity_cost",
    "high_qos_penalty",
    "low_qos_feedback",
    "high_demand",
    "low_direct_preference",
)
MEASURED_QOS_DEMAND_SCALES = (1.15, 1.30)
MEASURED_QOS_CAPACITY_SCALES = (0.85, 1.00)
DIRECT_API_BRAND_LOW = 1.01

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "font.size": 8,
})


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

def _write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    keys = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)

def parameter_audit_rows() -> list[dict[str, Any]]:
    config = IntermediaryConfig.default()
    rows = (
        ("qos_threshold", "\\bar u", config.qos_threshold, "synthetic", "base-case QoS threshold"),
        ("qos_strength", "\\kappa", config.qos_strength, "synthetic", "base-case QoS strength"),
        ("vllm_qos_profiles", "\\bar u,\\kappa", "1.00/0.52; 1.06/0.94", "measured", "vLLM QoS curve fit"),
        ("arrival_shape", "a_t", "8/16/32 rps replay", "measured", "vLLM arrival replay"),
        ("price_sensitivity", "\\alpha", config.price_sensitivity, "synthetic", "demand elasticity"),
        ("inconvenience_cost", "c_s", config.inconvenience_cost, "synthetic", "migration friction"),
        ("capacity_cost", "c_g", config.capacity_cost, "synthetic", "intermediary operating cost"),
        ("degrade_cost", "c_q", config.degrade_cost, "synthetic", "SLA or churn penalty"),
        ("qos_feedback_weight", "\\gamma", config.qos_feedback_weight, "synthetic", "QoS user response"),
        ("direct_api_preference", "b_0", 1.08, "assumed", "direct API brand preference"),
    )
    return [
        {"parameter": p, "symbol": s, "baseline_value": v, "source_type": t, "calibration_need": n}
        for p, s, v, t, n in rows
    ]

def uncertainty_sweep_rows(
    *,
    trials: int,
    maxiter: int,
    variants: Iterable[str] = UNCERTAINTY_VARIANTS,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    base = IntermediaryConfig.default(optimizer_trials=trials, optimizer_maxiter=maxiter)
    for variant in variants:
        config, direct_brand = _variant_config(base, variant)
        uniform = market_metric_row("uniform_retail", uniform_result(config), config)
        protected = user_protected_config(config)
        protected_result = optimize_three_stage_stackelberg(protected, policy="user_protected_revenue")
        rows.append(_policy_row("user_protected_revenue", protected_result, config=protected, uniform=uniform, variant=variant))
        direct_result = optimize_direct_access_stackelberg(
            protected,
            direct_brand=direct_brand,
            policy="direct_api_user_choice",
        )
        direct_config = direct_api_config(protected, direct_brand=direct_brand)
        rows.append(_policy_row("direct_api_user_choice", direct_result, config=direct_config, uniform=uniform, variant=variant))
    return rows


def _variant_config(
    base: IntermediaryConfig,
    variant: str,
) -> tuple[IntermediaryConfig, float]:
    data: dict[str, Any] = {**base.__dict__}
    direct_brand = 1.08
    overrides = {
        "low_elasticity": {"price_sensitivity": 2.0},
        "high_elasticity": {"price_sensitivity": 5.0},
        "high_migration_cost": {"inconvenience_cost": 0.45},
        "high_capacity_cost": {"capacity_cost": 0.030},
        "high_qos_penalty": {"degrade_cost": 0.70},
        "low_qos_feedback": {"qos_feedback_weight": 0.35},
    }
    if variant in overrides:
        data.update(overrides[variant])
    elif variant == "high_demand":
        data["rigid_baseline"] = base.rigid_baseline * 1.20
        data["flexible_baseline"] = base.flexible_baseline * 1.20
    elif variant == "low_direct_preference":
        direct_brand = DIRECT_API_BRAND_LOW
    else:
        raise ValueError(f"unknown uncertainty variant: {variant}")
    return IntermediaryConfig.default(**data), direct_brand


def _policy_row(
    label: str,
    result,
    *,
    config: IntermediaryConfig,
    uniform: dict[str, Any],
    variant: str,
) -> dict[str, Any]:
    row = market_metric_row(label, result, config, extra={"experiment": "calibration_uncertainty", "variant": variant})
    row["platform_revenue_gain_vs_uniform"] = row["platform_revenue"] - uniform["platform_revenue"]
    row["inclusive_value_gain_vs_uniform"] = row["inclusive_value"] - uniform["inclusive_value"]
    row["active_min_qos_gain_vs_uniform"] = row["active_min_qos"] - uniform["active_min_qos"]
    row["improves_revenue_and_user_experience"] = bool(
        row["platform_revenue_gain_vs_uniform"] > 0.0
        and row["inclusive_value_gain_vs_uniform"] > 0.0
        and row["active_min_qos_gain_vs_uniform"] >= 0.0
    )
    return row


def measured_qos_stress_rows(
    project_root: Path,
    *,
    trials: int,
    maxiter: int,
    demand_scales: Iterable[float] = MEASURED_QOS_DEMAND_SCALES,
    capacity_scales: Iterable[float] = MEASURED_QOS_CAPACITY_SCALES,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    base = IntermediaryConfig.default(optimizer_trials=trials, optimizer_maxiter=maxiter)
    for profile in _calibrated_profiles(project_root):
        for demand_scale in demand_scales:
            for capacity_scale in capacity_scales:
                config = scaled_market_config(
                    base,
                    demand_scale=float(demand_scale),
                    capacity_scale=float(capacity_scale),
                    qos_threshold=profile["threshold"],
                    qos_strength=profile["strength"],
                )
                fixed = optimize_fixed_capacity_stackelberg(config)
                adaptive = optimize_three_stage_stackelberg(config, policy="measured_qos_adaptive_capacity")
                rows.append(_stress_row("measured_qos_fixed_capacity", fixed, config=config, profile=profile, demand_scale=demand_scale, capacity_scale=capacity_scale))
                rows.append(_stress_row("measured_qos_adaptive_capacity", adaptive, config=config, profile=profile, demand_scale=demand_scale, capacity_scale=capacity_scale))
    return rows


def _stress_row(
    label: str,
    result,
    *,
    config: IntermediaryConfig,
    profile: dict[str, Any],
    demand_scale: float,
    capacity_scale: float,
) -> dict[str, Any]:
    return market_metric_row(label, result, config, extra={
        "experiment": "measured_qos_stress",
        "profile": profile["profile"],
        "demand_scale": float(demand_scale),
        "capacity_scale": float(capacity_scale),
        "qos_threshold": profile["threshold"],
        "qos_strength": profile["strength"],
        "calibration_rmse": profile["rmse"],
    })


def run_experiments(project_root: Path, *, trials: int, maxiter: int) -> dict[str, list[dict[str, Any]]]:
    return {
        "parameter_source_audit": parameter_audit_rows(),
        "calibration_uncertainty": uncertainty_sweep_rows(trials=trials, maxiter=maxiter),
        "measured_qos_stress": measured_qos_stress_rows(project_root, trials=trials, maxiter=maxiter),
    }


def write_artifacts(results: dict[str, list[dict[str, Any]]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "calibration_uncertainty_records.json").write_text(
        json.dumps(_jsonable(results), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    for name, rows in results.items():
        _write_csv(rows, output_dir / f"{name}.csv")
    _plot_uncertainty(results["calibration_uncertainty"], output_dir / "calibration_uncertainty")
    _plot_measured_qos(results["measured_qos_stress"], output_dir / "measured_qos_stress")


def _plot_uncertainty(rows: list[dict[str, Any]], path: Path) -> None:
    variants = sorted({row["variant"] for row in rows})
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.2), sharex=True)
    for idx, policy in enumerate(["user_protected_revenue", "direct_api_user_choice"]):
        selected = [row for row in rows if row["policy"] == policy]
        x = np.arange(len(variants)) + (idx - 0.5) * 0.34
        values = [next(row for row in selected if row["variant"] == variant) for variant in variants]
        axes[0].bar(x, [row["inclusive_value_gain_vs_uniform"] for row in values], width=0.32, label=policy)
        axes[1].bar(x, [row["platform_revenue_gain_vs_uniform"] for row in values], width=0.32, label=policy)
    for axis, title in zip(axes, ["Inclusive value gain", "Platform revenue gain"]):
        axis.axhline(0.0, color="#555555", linewidth=0.8)
        axis.set_title(title)
        axis.set_xticks(np.arange(len(variants)))
        axis.set_xticklabels(variants, rotation=35, ha="right")
        axis.grid(axis="y", alpha=0.25)
    axes[1].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(path.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


def _plot_measured_qos(rows: list[dict[str, Any]], path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0))
    labels = [f"{row['profile']}\\n{row['demand_scale']:.2f}/{row['capacity_scale']:.2f}" for row in rows[::2]]
    fixed = [row for row in rows if row["policy"] == "measured_qos_fixed_capacity"]
    adaptive = [row for row in rows if row["policy"] == "measured_qos_adaptive_capacity"]
    x = np.arange(len(fixed))
    for axis, key, title in zip(axes, ["active_min_qos", "system_profit"], ["Active minimum QoS", "System profit"]):
        axis.bar(x - 0.18, [row[key] for row in fixed], width=0.35, label="fixed")
        axis.bar(x + 0.18, [row[key] for row in adaptive], width=0.35, label="adaptive")
        axis.set_title(title)
        axis.set_xticks(x)
        axis.set_xticklabels(labels, rotation=35, ha="right")
        axis.grid(axis="y", alpha=0.25)
        axis.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(path.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, default=PROJECT_ROOT / "artifacts" / "calibration_uncertainty")
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
