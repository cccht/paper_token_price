from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

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


def _read_rows(source: Path) -> list[dict[str, float]]:
    with source.open(newline="", encoding="utf-8-sig") as handle:
        return [
            {key: float(value) for key, value in row.items()}
            for row in csv.DictReader(handle)
        ]


def write_vllm_plot(source: Path) -> Path:
    rows = _read_rows(source)
    concurrency = [row["concurrency"] for row in rows]
    figure, axes = plt.subplots(1, 3, figsize=(11, 3.1))
    axes[0].plot(
        concurrency,
        [row["throughput_tokens_per_second"] for row in rows],
        marker="o",
    )
    axes[0].set_ylabel("Throughput (token/s)")
    axes[1].plot(
        concurrency,
        [row["mean_ttft_seconds"] for row in rows],
        marker="o",
        label="Mean",
    )
    axes[1].plot(
        concurrency,
        [row["p95_ttft_seconds"] for row in rows],
        marker="s",
        label="P95",
    )
    axes[1].set_ylabel("TTFT (s)")
    axes[1].legend()
    axes[2].plot(
        concurrency,
        [row["ttft_sla_0_5_rate"] for row in rows],
        marker="o",
    )
    axes[2].set_ylabel("TTFT SLA rate")
    for axis in axes:
        axis.set_xlabel("Concurrent requests")
        axis.grid(alpha=0.25)
    output = source.parent / "vllm_overload_curve.pdf"
    figure.tight_layout()
    figure.savefig(output, bbox_inches="tight")
    plt.close(figure)
    return output


def write_vllm_reliability_plot(source: Path) -> Path:
    rows = _read_rows(source)
    concurrency = [row["concurrency"] for row in rows]
    figure, axes = plt.subplots(1, 3, figsize=(11, 3.1))
    series = (
        ("throughput_tokens_per_second", "Throughput (token/s)"),
        ("mean_ttft_seconds", "Mean TTFT (s)"),
        ("ttft_sla_0_5_rate", "TTFT SLA rate"),
    )
    for axis, (field, ylabel) in zip(axes, series):
        axis.errorbar(
            concurrency,
            [row[f"{field}_mean"] for row in rows],
            yerr=[row[f"{field}_ci95"] for row in rows],
            marker="o",
            capsize=3,
        )
        axis.set_xlabel("Concurrent requests")
        axis.set_ylabel(ylabel)
        axis.grid(alpha=0.25)
    output = source.parent / "vllm_reliability_curve.pdf"
    figure.tight_layout()
    figure.savefig(output, bbox_inches="tight")
    plt.close(figure)
    return output
