"""Build the vLLM QoS measurement anchor for the peak-shaving paper."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
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

from pricing_sim.calibration import fit_qos_curve, load_controlled_aggregate
from pricing_sim.qos import qos_factor
from experiments.plot_style import configure_times_new_roman

DEFAULT_SOURCES = (
    (
        "vllm-0.5b",
        "Qwen2.5-0.5B-Instruct",
        Path("artifacts/vllm-study/20260531-190126/controlled_aggregate.csv"),
        Path("artifacts/vllm-study/20260531-190126/study_metadata.json"),
    ),
    (
        "vllm-3b",
        "Qwen2.5-3B-Instruct",
        Path("artifacts/vllm-study-qwen25-3b/20260531-214710/controlled_aggregate.csv"),
        Path("artifacts/vllm-study-qwen25-3b/20260531-214710/study_metadata.json"),
    ),
)
POINT_FIELDS = (
    "profile",
    "model",
    "source",
    "concurrency",
    "repeats",
    "normalized_utilization",
    "observed_qos",
    "observed_qos_ci95",
    "fitted_qos",
)


@dataclass(frozen=True)
class AnchorSource:
    profile: str
    model: str
    aggregate: Path
    metadata: Path


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _read_metadata(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _source_from_tuple(item: tuple[str, str, Path, Path]) -> AnchorSource:
    profile, model, aggregate, metadata = item
    return AnchorSource(profile, model, PROJECT_ROOT / aggregate, PROJECT_ROOT / metadata)


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)


def build_anchor(sources: list[AnchorSource]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    profiles: list[dict[str, Any]] = []
    points: list[dict[str, Any]] = []
    metadata: dict[str, Any] = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "qos_definition": "TTFT SLA rate with threshold 0.5 seconds",
        "fit_function": "q(u)=exp(-strength * max(u-threshold,0)^2)",
        "source_count": len(sources),
    }
    runtime: list[dict[str, Any]] = []
    for source in sources:
        if not source.aggregate.exists():
            raise FileNotFoundError(source.aggregate)
        raw_rows = _read_rows(source.aggregate)
        fit = fit_qos_curve(load_controlled_aggregate(source.aggregate))
        meta = _read_metadata(source.metadata)
        runtime.append({"profile": source.profile, "metadata": meta.get("runtime", {})})
        repeats = int(float(raw_rows[0].get("repeats", 1))) if raw_rows else 1
        observed = np.array([float(row["ttft_sla_0_5_rate_mean"]) for row in raw_rows], dtype=float)
        concurrency = np.array([float(row["concurrency"]) for row in raw_rows], dtype=float)
        drop_candidates = concurrency[observed < 0.99]
        first_drop = float(drop_candidates[0]) if len(drop_candidates) else None
        profiles.append({
            "profile": source.profile,
            "model": source.model,
            "source": _display_path(source.aggregate),
            "metadata": _display_path(source.metadata),
            "capacity_concurrency": fit.capacity_concurrency,
            "qos_threshold": fit.threshold,
            "qos_strength": fit.strength,
            "fit_rmse": fit.rmse,
            "repeats": repeats,
            "min_observed_qos": float(np.min(observed)),
            "first_sla_drop_concurrency": first_drop,
        })
        by_concurrency = {
            float(row["concurrency"]): row for row in raw_rows
        }
        for concurrency_value, utilization, observed_qos, fitted_qos in zip(
            fit.concurrency,
            fit.utilization,
            fit.observed_qos,
            fit.fitted_qos,
        ):
            raw = by_concurrency[float(concurrency_value)]
            points.append({
                "profile": source.profile,
                "model": source.model,
                "source": _display_path(source.aggregate),
                "concurrency": float(concurrency_value),
                "repeats": repeats,
                "normalized_utilization": float(utilization),
                "observed_qos": float(observed_qos),
                "observed_qos_ci95": float(raw.get("ttft_sla_0_5_rate_ci95") or 0.0),
                "fitted_qos": float(fitted_qos),
            })
    metadata["runtime"] = runtime
    return profiles, points, metadata


def write_csv(path: Path, rows: list[dict[str, Any]], fields: tuple[str, ...] | None = None) -> None:
    if not rows:
        raise ValueError("rows must not be empty")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields or rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def plot_anchor(profiles: list[dict[str, Any]], points: list[dict[str, Any]], output: Path) -> None:
    configure_times_new_roman()
    mpl.rcParams.update({"axes.grid": True, "grid.alpha": 0.18})
    colors = {"vllm-0.5b": "#1F4E79", "vllm-3b": "#E6A400"}
    fig, ax = plt.subplots(figsize=(6.8, 3.2))
    for profile in profiles:
        name = str(profile["profile"])
        rows = [row for row in points if row["profile"] == name]
        rows.sort(key=lambda row: row["normalized_utilization"])
        x = np.array([row["normalized_utilization"] for row in rows], dtype=float)
        y = np.array([row["observed_qos"] for row in rows], dtype=float)
        err = np.array([row["observed_qos_ci95"] for row in rows], dtype=float)
        color = colors.get(name, "#333333")
        ax.errorbar(x, y, yerr=err, fmt="o", color=color, capsize=2.5, label=f"{profile['model']} measured")
        grid = np.linspace(min(x), max(x), 160)
        fitted = qos_factor(grid, threshold=float(profile["qos_threshold"]), strength=float(profile["qos_strength"]))
        ax.plot(grid, fitted, color=color, linewidth=1.8, alpha=0.85, label=f"{profile['model']} fit")
    ax.axvline(1.0, color="#4D4D4D", linestyle="--", linewidth=1.0, alpha=0.7,
               label="healthy boundary")
    ax.set_xlabel("Normalized concurrency")
    ax.set_ylabel("TTFT SLA rate")
    ax.set_ylim(-0.02, 1.05)
    ax.legend(loc="lower left", ncol=1, fontsize=7.2, frameon=False,
              borderaxespad=0.25, handlelength=1.5, labelspacing=0.25)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output)
    fig.savefig(output.with_suffix(".png"), dpi=300)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=PROJECT_ROOT / "artifacts/peak_shaving/20260619_submission")
    parser.add_argument("--figure-dir", type=Path, default=PROJECT_ROOT / "figures/peak_shaving_submission")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    sources = [_source_from_tuple(item) for item in DEFAULT_SOURCES]
    profiles, points, metadata = build_anchor(sources)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.output_dir / "vllm_qos_anchor_points.csv", points, POINT_FIELDS)
    summary = {"metadata": metadata, "profiles": profiles}
    (args.output_dir / "vllm_qos_anchor_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    plot_anchor(profiles, points, args.figure_dir / "vllm_qos_anchor.pdf")
    print(args.output_dir / "vllm_qos_anchor_summary.json")
    print(args.output_dir / "vllm_qos_anchor_points.csv")
    print(args.figure_dir / "vllm_qos_anchor.pdf")


if __name__ == "__main__":
    main()
