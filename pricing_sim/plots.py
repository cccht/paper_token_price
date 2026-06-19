from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 8,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "pdf.fonttype": 42,
    "svg.fonttype": "none",
    "axes.unicode_minus": False,
})


def _baseline(records: list[dict[str, Any]], policy: str) -> dict[str, Any]:
    return next(
        record["policy_evaluation"]
        for record in records
        if record["experiment"] == "baseline" and record["policy"] == policy
    )


def _write_baseline_plot(records: list[dict[str, Any]], output_dir: Path) -> Path:
    uniform = _baseline(records, "uniform")
    myopic = _baseline(records, "myopic")
    aware = _baseline(records, "qos_aware")
    periods = np.arange(len(uniform["prices"]))
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.2))
    for label, record, style in [
        ("Uniform", uniform, "--"),
        ("Myopic", myopic, "-."),
        ("QoS-aware", aware, "-"),
    ]:
        axes[0].plot(periods, record["prices"], style, marker="o", label=label)
        axes[1].plot(periods, record["utilization"], style, marker="o", label=label)
        axes[2].plot(periods, record["qos"], style, marker="o", label=label)
    axes[0].set_ylabel("Posted price")
    axes[1].set_ylabel("Utilization")
    axes[2].set_ylabel("QoS factor")
    for axis in axes:
        axis.set_xlabel("Period")
        axis.grid(alpha=0.25)
    axes[0].legend(fontsize=8)
    fig.tight_layout()
    path = output_dir / "baseline_comparison.pdf"
    fig.savefig(path)
    plt.close(fig)
    return path


def _write_metric_plot(records: list[dict[str, Any]], output_dir: Path) -> Path:
    policies = ["uniform", "myopic", "qos_aware"]
    labels = ["Uniform", "Myopic", "QoS-aware"]
    evaluations = [_baseline(records, policy) for policy in policies]
    fig, axes = plt.subplots(1, 3, figsize=(9, 3.2))
    metrics = [
        ("profit", "Profit"),
        ("welfare", "Welfare"),
        ("qos", "Minimum QoS"),
    ]
    for axis, (metric, label) in zip(axes, metrics):
        values = [min(item[metric]) if metric == "qos" else item[metric] for item in evaluations]
        axis.bar(labels, values, color=["#999999", "#E69F00", "#0072B2"])
        axis.set_ylabel(label)
        axis.tick_params(axis="x", rotation=20)
        axis.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    path = output_dir / "baseline_metrics.pdf"
    fig.savefig(path)
    plt.close(fig)
    return path


def _write_sensitivity_plot(records: list[dict[str, Any]], output_dir: Path) -> Path | None:
    selected = [
        record for record in records
        if record["experiment"] == "qos_strength" and record["policy"] == "qos_aware"
    ]
    if not selected:
        return None
    selected.sort(key=lambda record: record["parameter_value"])
    x = [record["parameter_value"] for record in selected]
    y = [record["policy_evaluation"]["profit"] for record in selected]
    fig, axis = plt.subplots(figsize=(4.8, 3.2))
    axis.plot(x, y, marker="o", color="#0072B2")
    axis.set_xlabel("QoS degradation strength")
    axis.set_ylabel("QoS-aware profit")
    axis.grid(alpha=0.25)
    fig.tight_layout()
    path = output_dir / "qos_strength_sensitivity.pdf"
    fig.savefig(path)
    plt.close(fig)
    return path


def write_plots(
    records: list[dict[str, Any]],
    *,
    output_root: Path,
    run_id: str,
) -> list[Path]:
    output_dir = output_root / "plots" / run_id
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = [
        _write_baseline_plot(records, output_dir),
        _write_metric_plot(records, output_dir),
    ]
    sensitivity = _write_sensitivity_plot(records, output_dir)
    return paths + ([sensitivity] if sensitivity else [])
