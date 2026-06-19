"""Run reality-oriented robustness experiments for the intermediary game."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
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

from pricing_sim.calibration import fit_qos_curve, load_controlled_aggregate
from pricing_sim.intermediary_market import IntermediaryConfig, ThreeLayerResult
from pricing_sim.three_stage_game import optimize_three_stage_stackelberg


DEFAULT_TRIALS = 4
DEFAULT_MAXITER = 70
DEFAULT_SEEDS = tuple(range(8))
REFERENCE_TRIALS = (4, 8, 16)
ACTIVE_DEMAND_FRACTION = 1e-3
CALIBRATION_SOURCES = (
    ("vllm-study", Path("artifacts/vllm-study/20260531-190126/controlled_aggregate.csv")),
    ("vllm-study-qwen25-3b", Path("artifacts/vllm-study-qwen25-3b/20260531-214710/controlled_aggregate.csv")),
)

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "font.size": 8,
})


@dataclass(frozen=True)
class QosProfile:
    name: str
    source: str
    capacity_concurrency: float
    threshold: float
    strength: float
    rmse: float


def calibrated_qos_profiles(project_root: Path) -> list[QosProfile]:
    profiles: list[QosProfile] = []
    for name, relative in CALIBRATION_SOURCES:
        source = project_root / relative
        if not source.exists():
            continue
        fit = fit_qos_curve(load_controlled_aggregate(source))
        profiles.append(QosProfile(
            name=name,
            source=str(relative),
            capacity_concurrency=fit.capacity_concurrency,
            threshold=fit.threshold,
            strength=fit.strength,
            rmse=fit.rmse,
        ))
    if not profiles:
        raise FileNotFoundError("No vLLM calibration aggregate files were found.")
    return profiles


def result_row(experiment: str, result: ThreeLayerResult, extra: dict[str, Any]) -> dict[str, Any]:
    active = result.demand >= max(float(np.max(result.demand)) * ACTIVE_DEMAND_FRACTION, 1e-8)
    weighted_qos = float(np.sum(result.demand * result.qos) / max(np.sum(result.demand), 1e-12))
    row = {
        "experiment": experiment,
        "policy": result.policy,
        "platform_revenue": result.platform_revenue,
        "intermediary_profit": result.intermediary_profit,
        "system_profit": result.system_profit,
        "min_qos": float(np.min(result.qos)),
        "active_min_qos": float(np.min(result.qos[active])),
        "demand_weighted_qos": weighted_qos,
        "max_utilization": float(np.max(result.utilization)),
        "active_max_utilization": float(np.max(result.utilization[active])),
        "objective_evaluations": result.diagnostics.get("objective_evaluations", 1),
        "max_nash_regret": result.diagnostics.get("max_nash_regret", ""),
        "middle_iterations": result.diagnostics.get("middle_iterations", ""),
        "platform_trials": result.diagnostics.get("platform_trials", ""),
        "random_seed": result.diagnostics.get("random_seed", ""),
    }
    row.update(extra)
    return row


def empirical_qos_rows(project_root: Path, *, trials: int, maxiter: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    synthetic = IntermediaryConfig.default(optimizer_trials=trials, optimizer_maxiter=maxiter)
    synthetic_result = optimize_three_stage_stackelberg(synthetic, policy="three_layer_qos_aware")
    rows.append(result_row("empirical_qos", synthetic_result, {
        "profile": "synthetic_default",
        "qos_threshold": synthetic.qos_threshold,
        "qos_strength": synthetic.qos_strength,
        "calibration_rmse": "",
    }))
    for profile in calibrated_qos_profiles(project_root):
        config = IntermediaryConfig.default(
            optimizer_trials=trials,
            optimizer_maxiter=maxiter,
            qos_threshold=profile.threshold,
            qos_strength=profile.strength,
        )
        result = optimize_three_stage_stackelberg(config, policy="three_layer_qos_aware")
        rows.append(result_row("empirical_qos", result, {
            "profile": profile.name,
            "qos_threshold": profile.threshold,
            "qos_strength": profile.strength,
            "calibration_rmse": profile.rmse,
        }))
    return rows


def seed_robustness_rows(seeds: Iterable[int], *, trials: int, maxiter: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for seed in seeds:
        config = IntermediaryConfig.default(
            optimizer_trials=trials,
            optimizer_maxiter=maxiter,
            random_seed=int(seed),
        )
        result = optimize_three_stage_stackelberg(config, policy="three_layer_qos_aware")
        rows.append(result_row("seed_robustness", result, {"seed": int(seed)}))
    return rows


def summarize_seed_rows(rows: list[dict[str, Any]]) -> dict[str, float | int]:
    profits = np.array([row["system_profit"] for row in rows], dtype=float)
    qos = np.array([row["min_qos"] for row in rows], dtype=float)
    active_qos = np.array([row.get("active_min_qos", row["min_qos"]) for row in rows], dtype=float)
    weighted_qos = np.array([row.get("demand_weighted_qos", row["min_qos"]) for row in rows], dtype=float)
    regret = np.array([row["max_nash_regret"] for row in rows], dtype=float)
    return {
        "runs": int(len(rows)),
        "system_profit_mean": float(np.mean(profits)),
        "system_profit_std": float(np.std(profits, ddof=1)) if len(rows) > 1 else 0.0,
        "system_profit_best": float(np.max(profits)),
        "system_profit_worst": float(np.min(profits)),
        "best_gap_vs_mean": float(np.max(profits) - np.mean(profits)),
        "min_qos_mean": float(np.mean(qos)),
        "min_qos_worst": float(np.min(qos)),
        "active_min_qos_worst": float(np.min(active_qos)),
        "demand_weighted_qos_mean": float(np.mean(weighted_qos)),
        "demand_weighted_qos_worst": float(np.min(weighted_qos)),
        "max_nash_regret_max": float(np.max(regret)),
    }


def platform_reference_rows(*, trial_counts: Iterable[int], maxiter: int, seed: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for trials in trial_counts:
        config = IntermediaryConfig.default(
            optimizer_trials=int(trials),
            optimizer_maxiter=maxiter,
            random_seed=seed,
        )
        result = optimize_three_stage_stackelberg(config, policy="three_layer_qos_aware")
        rows.append(result_row("platform_reference", result, {"candidate_count": int(trials), "seed": seed}))
    best_platform = max(float(row["platform_revenue"]) for row in rows)
    best_system = max(float(row["system_profit"]) for row in rows)
    for row in rows:
        row["platform_revenue_gap_to_reference"] = best_platform - float(row["platform_revenue"])
        row["system_profit_gap_to_best_observed"] = best_system - float(row["system_profit"])
    return rows


def run_experiments(project_root: Path, *, trials: int, maxiter: int, seed_count: int) -> dict[str, Any]:
    seeds = tuple(range(seed_count))
    seed_rows = seed_robustness_rows(seeds, trials=trials, maxiter=maxiter)
    return {
        "empirical_qos": empirical_qos_rows(project_root, trials=trials, maxiter=maxiter),
        "seed_robustness": seed_rows,
        "seed_summary": [summarize_seed_rows(seed_rows)],
        "platform_reference": platform_reference_rows(
            trial_counts=REFERENCE_TRIALS,
            maxiter=maxiter,
            seed=42,
        ),
        "calibration_profiles": [asdict(profile) for profile in calibrated_qos_profiles(project_root)],
    }


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


def _plot_empirical(rows: list[dict[str, Any]], path: Path) -> None:
    labels = [row["profile"] for row in rows]
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9))
    axes[0].bar(labels, [row["system_profit"] for row in rows], color="#2A9D8F")
    axes[1].bar(labels, [row["max_utilization"] for row in rows], color="#E9C46A")
    axes[0].set_title("System profit")
    axes[1].set_title("Peak utilization")
    for axis in axes:
        axis.tick_params(axis="x", rotation=20)
        axis.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(path.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


def _plot_line(rows: list[dict[str, Any]], x_key: str, path: Path, xlabel: str) -> None:
    x = [row[x_key] for row in rows]
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9))
    axes[0].plot(x, [row["system_profit"] for row in rows], "o-", color="#264653")
    axes[1].plot(x, [row["max_nash_regret"] for row in rows], "o-", color="#E76F51")
    axes[0].set_title("System profit")
    axes[1].set_title("Max Nash regret")
    axes[1].set_yscale("log")
    for axis in axes:
        axis.set_xlabel(xlabel)
        axis.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(path.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


def write_artifacts(results: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "reality_experiment_records.json").write_text(
        json.dumps(_jsonable(results), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    for name, rows in results.items():
        if isinstance(rows, list) and rows and isinstance(rows[0], dict):
            _write_csv(rows, output_dir / f"{name}.csv")
    _plot_empirical(results["empirical_qos"], output_dir / "empirical_qos_calibration")
    _plot_line(results["seed_robustness"], "seed", output_dir / "seed_robustness", "Random seed")
    _plot_line(results["platform_reference"], "candidate_count", output_dir / "platform_reference", "Candidate count")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, default=PROJECT_ROOT / "artifacts" / "intermediary_reality")
    parser.add_argument("--trials", type=int, default=DEFAULT_TRIALS)
    parser.add_argument("--maxiter", type=int, default=DEFAULT_MAXITER)
    parser.add_argument("--seed-count", type=int, default=len(DEFAULT_SEEDS))
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    output_dir = args.output_root / datetime.now().strftime("%Y%m%d-%H%M%S")
    results = run_experiments(PROJECT_ROOT, trials=args.trials, maxiter=args.maxiter, seed_count=args.seed_count)
    write_artifacts(results, output_dir)
    print(f"output={output_dir}")


if __name__ == "__main__":
    main()
