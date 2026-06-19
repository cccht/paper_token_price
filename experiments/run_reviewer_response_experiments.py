"""Run reviewer-response diagnostics for the intermediary pricing paper."""

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

from pricing_sim.intermediary_market import IntermediaryConfig
from pricing_sim.reviewer_diagnostics import attribution_rows, finite_bridge_rows, profit_slice_rows
from pricing_sim.three_stage_game import optimize_three_stage_stackelberg


mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "font.size": 8,
})


ATTRIBUTION_LABELS = {
    "none": "Base",
    "capacity_only": "Cap.",
    "price_only": "Price",
    "price_and_capacity_without_qos_internalization": "Price+Cap.",
    "price_capacity_with_congestion_proxy": "+Cong.",
    "price_capacity_and_qos_internalization": "+QoS",
}


def run_experiments(config: IntermediaryConfig) -> dict[str, list[dict[str, Any]]]:
    full = optimize_three_stage_stackelberg(config, policy="three_layer_qos_aware")
    slices, slice_summary = profit_slice_rows(full, config)
    finite_rows, finite_summary = finite_bridge_rows(full, config)
    return {
        "attribution_ablation": attribution_rows(config),
        "profit_slices": slices,
        "profit_slice_summary": slice_summary,
        "finite_psne_logit": finite_rows,
        "finite_psne_logit_summary": finite_summary,
    }


def write_artifacts(results: dict[str, list[dict[str, Any]]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "reviewer_response_records.json").write_text(
        json.dumps(_jsonable(results), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    for name, rows in results.items():
        _write_csv(rows, output_dir / f"{name}.csv")
    _plot_attribution(results["attribution_ablation"], output_dir / "attribution_ablation")
    _plot_profit_slices(results["profit_slices"], output_dir / "profit_slices")
    _plot_finite_bridge(results["finite_psne_logit_summary"], output_dir / "finite_psne_logit")


def _write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    keys = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def _plot_attribution(rows: list[dict[str, Any]], path: Path) -> None:
    labels = [ATTRIBUTION_LABELS.get(str(row["mechanism"]), str(row["mechanism"])) for row in rows]
    profit = [float(row["system_profit"]) for row in rows]
    qos = [float(row["min_qos"]) for row in rows]
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.0))
    axes[0].bar(range(len(rows)), profit, color="#2A9D8F")
    axes[1].bar(range(len(rows)), qos, color="#E76F51")
    for axis, title in zip(axes, ["System profit", "Minimum QoS"]):
        axis.set_title(title)
        axis.set_xticks(range(len(rows)))
        axis.set_xticklabels(labels, rotation=0, ha="center")
        axis.set_xlabel("Mechanism")
        axis.tick_params(axis="x", pad=4)
        axis.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(path.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


def _plot_profit_slices(rows: list[dict[str, Any]], path: Path) -> None:
    slices = sorted({str(row["slice"]) for row in rows})
    fig, axes = plt.subplots(1, len(slices), figsize=(8.8, 3.2))
    if len(slices) == 1:
        axes = [axes]
    for axis, slice_name in zip(axes, slices):
        selected = [row for row in rows if row["slice"] == slice_name]
        axis.plot([float(row["x"]) for row in selected], [float(row["profit"]) for row in selected], "o-", color="#264653")
        axis.set_title(slice_name.replace("_", " "))
        axis.set_xlabel("slice coordinate")
        axis.set_ylabel("broker profit")
        axis.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(path.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


def _plot_finite_bridge(rows: list[dict[str, Any]], path: Path) -> None:
    players = [int(row["players"]) for row in rows]
    l1 = [float(row["l1_share_gap_mean"]) for row in rows]
    cosine = [float(row["cosine_similarity_mean"]) for row in rows]
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0))
    axes[0].plot(players, l1, "o-", color="#D55E00")
    axes[1].plot(players, cosine, "o-", color="#0072B2")
    axes[0].set_title("Mean L1 share gap")
    axes[1].set_title("Mean cosine similarity")
    for axis in axes:
        axis.set_xlabel("finite players")
        axis.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(path.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


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


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, default=PROJECT_ROOT / "artifacts" / "reviewer_response")
    parser.add_argument("--trials", type=int, default=8)
    parser.add_argument("--maxiter", type=int, default=140)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    config = IntermediaryConfig.default(optimizer_trials=args.trials, optimizer_maxiter=args.maxiter)
    output_dir = args.output_root / datetime.now().strftime("%Y%m%d-%H%M%S")
    write_artifacts(run_experiments(config), output_dir)
    print(f"output={output_dir}")


if __name__ == "__main__":
    main()
