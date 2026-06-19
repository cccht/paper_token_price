"""Run supplementary SCI-style robustness experiments for the pricing game."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
import sys
from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
for import_path in (PROJECT_ROOT, SCRIPT_DIR):
    path_text = str(import_path)
    if path_text not in sys.path:
        sys.path.insert(0, path_text)

from pricing_sim.fixed_capacity_game import optimize_fixed_capacity_stackelberg
from pricing_sim.intermediary_market import (
    IntermediaryConfig,
    ThreeLayerResult,
    _default_capacity,
    evaluate_three_layer_policy,
)
from pricing_sim.three_stage_game import optimize_three_stage_stackelberg


SCREENING_TRIALS = 3
SCREENING_MAXITER = 60
COLORS = ["#0072B2", "#D55E00", "#009E73", "#E69F00", "#CC79A7"]

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


def _screening_config(**overrides: object) -> IntermediaryConfig:
    data = {"optimizer_trials": SCREENING_TRIALS, "optimizer_maxiter": SCREENING_MAXITER}
    data.update(overrides)
    return IntermediaryConfig.default(**data)


def _metrics(name: str, result: ThreeLayerResult, extra: dict[str, Any] | None = None) -> dict[str, Any]:
    row = {
        "experiment": name,
        "policy": result.policy,
        "platform_revenue": result.platform_revenue,
        "intermediary_profit": result.intermediary_profit,
        "system_profit": result.system_profit,
        "min_qos": float(np.min(result.qos)),
        "max_utilization": float(np.max(result.utilization)),
        "objective_evaluations": result.diagnostics.get("objective_evaluations", 1),
        "max_nash_regret": result.diagnostics.get("max_nash_regret", ""),
        "middle_iterations": result.diagnostics.get("middle_iterations", ""),
    }
    if extra:
        row.update(extra)
    return row


def _uniform_result(config: IntermediaryConfig) -> ThreeLayerResult:
    wholesale = np.full(config.num_periods, config.base_wholesale_price)
    retail = np.full((config.num_intermediaries, config.num_periods), config.base_retail_price)
    return evaluate_three_layer_policy(wholesale, retail, _default_capacity(config), config, policy="uniform_retail")


def run_experiments() -> dict[str, list[dict[str, Any]]]:
    return {
        "platform_trials": _platform_trials_sweep(),
        "qos_threshold": _qos_threshold_sweep(),
        "demand_scale": _demand_scale_sweep(),
        "capacity_ablation": _capacity_ablation(),
    }


def _platform_trials_sweep() -> list[dict[str, Any]]:
    rows = []
    for trials in [1, 2, 4, 8]:
        config = _screening_config(optimizer_trials=trials)
        result = optimize_three_stage_stackelberg(config, policy="three_layer_qos_aware")
        rows.append(_metrics("platform_trials", result, {"platform_trials": trials}))
    return rows


def _qos_threshold_sweep() -> list[dict[str, Any]]:
    rows = []
    for threshold in [0.76, 0.80, 0.82, 0.86, 0.90]:
        config = _screening_config(qos_threshold=threshold)
        result = optimize_three_stage_stackelberg(config, policy="three_layer_qos_aware")
        rows.append(_metrics("qos_threshold", result, {"qos_threshold": threshold}))
    return rows


def _demand_scale_sweep() -> list[dict[str, Any]]:
    rows = []
    base = IntermediaryConfig.default()
    for scale in [0.85, 1.00, 1.15, 1.30]:
        config = _screening_config(
            rigid_baseline=base.rigid_baseline * scale,
            flexible_baseline=base.flexible_baseline * scale,
        )
        rows.append(_metrics("demand_scale", _uniform_result(config), {"demand_scale": scale}))
        aware = optimize_three_stage_stackelberg(config, policy="three_layer_qos_aware")
        rows.append(_metrics("demand_scale", aware, {"demand_scale": scale}))
    return rows


def _capacity_ablation() -> list[dict[str, Any]]:
    config = _screening_config(optimizer_trials=4)
    fixed = optimize_fixed_capacity_stackelberg(config)
    strategic = optimize_three_stage_stackelberg(config, policy="three_layer_qos_aware")
    return [
        _metrics("capacity_ablation", fixed, {"capacity_mode": "fixed"}),
        _metrics("capacity_ablation", strategic, {"capacity_mode": "strategic"}),
    ]


def _write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    keys = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def _plot_line(rows: list[dict[str, Any]], x_key: str, path: Path, title: str) -> None:
    x = [row[x_key] for row in rows]
    fig, axes = plt.subplots(1, 3, figsize=(10.8, 3.0))
    for axis, key, label, color in zip(
        axes,
        ["system_profit", "min_qos", "max_utilization"],
        ["System profit", "Minimum QoS", "Peak utilization"],
        COLORS,
    ):
        axis.plot(x, [row[key] for row in rows], "o-", color=color)
        axis.set_title(label)
        axis.set_xlabel(title)
        axis.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(path.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


def _plot_demand(rows: list[dict[str, Any]], path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0))
    for policy, color in [("uniform_retail", COLORS[1]), ("three_layer_qos_aware", COLORS[0])]:
        selected = [row for row in rows if row["policy"] == policy]
        x = [row["demand_scale"] for row in selected]
        axes[0].plot(x, [row["system_profit"] for row in selected], "o-", color=color, label=policy)
        axes[1].plot(x, [row["min_qos"] for row in selected], "o-", color=color, label=policy)
    axes[0].set_title("System profit")
    axes[1].set_title("Minimum QoS")
    for axis in axes:
        axis.set_xlabel("Demand scale")
        axis.grid(alpha=0.25)
        axis.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(path.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


def _plot_capacity(rows: list[dict[str, Any]], path: Path) -> None:
    labels = [row["capacity_mode"] for row in rows]
    fig, axes = plt.subplots(1, 3, figsize=(8.6, 3.0))
    for axis, key, title in zip(axes, ["system_profit", "min_qos", "max_utilization"], ["System profit", "Minimum QoS", "Peak utilization"]):
        axis.bar(labels, [row[key] for row in rows], color=COLORS[: len(rows)])
        axis.set_title(title)
        axis.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(path.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


def write_artifacts(results: dict[str, list[dict[str, Any]]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "sci_experiment_records.json").write_text(
        json.dumps(_jsonable(results), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    for name, rows in results.items():
        _write_csv(rows, output_dir / f"{name}.csv")
    _plot_line(results["platform_trials"], "platform_trials", output_dir / "platform_trials_sweep", "Platform trials")
    _plot_line(results["qos_threshold"], "qos_threshold", output_dir / "qos_threshold_sweep", "QoS threshold")
    _plot_demand(results["demand_scale"], output_dir / "demand_scale_sweep")
    _plot_capacity(results["capacity_ablation"], output_dir / "capacity_ablation")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, default=PROJECT_ROOT / "artifacts" / "intermediary_sci")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    output_dir = args.output_root / datetime.now().strftime("%Y%m%d-%H%M%S")
    results = run_experiments()
    write_artifacts(results, output_dir)
    print(f"output={output_dir}")


if __name__ == "__main__":
    main()
