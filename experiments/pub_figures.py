"""Matplotlib publication-quality figures: policy detail + baseline comparison.

Usage:
    from experiments.pub_figures import plot_policy_detail, plot_baseline_comparison
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# ── publication styling ──────────────────────────────────────────
mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 7.5,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "figure.dpi": 150,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
})

# ── Color palette (colorblind-safe, muted academic tones) ──────
C = {
    "blue":    "#2B5F8A",
    "red":     "#C44E52",
    "green":   "#3D8C40",
    "orange":  "#E89242",
    "purple":  "#7B5EA7",
    "teal":    "#4E9CA0",
    "gray":    "#828282",
    "dark":    "#333333",
    "light1":  "#BFD7EA",
    "light2":  "#9BC4CB",
    "light3":  "#D7C9AA",
}

CAPACITY_COLORS = [C["light1"], C["light2"], C["light3"]]

PERIOD_LABELS = ["1", "2", "3", "4", "5", "6", "7", "8"]

STRATEGY_LABELS: dict[str, str] = {
    "uniform_retail":        "Uniform\nretail",
    "direct_platform":       "Direct\nplatform",
    "single_intermediary":   "Single\nintermediary",
    "no_qos_pricing":        "Dynamic\n(no QoS)",
    "three_layer_qos_aware": "QoS-aware\n(3-layer)",
}

STRATEGY_ORDER = [
    "uniform_retail",
    "direct_platform",
    "single_intermediary",
    "no_qos_pricing",
    "three_layer_qos_aware",
]

STRATEGY_COLORS = {
    "uniform_retail":        C["gray"],
    "direct_platform":       C["blue"],
    "single_intermediary":   C["teal"],
    "no_qos_pricing":        C["orange"],
    "three_layer_qos_aware": C["green"],
}


def plot_policy_detail(record: dict[str, Any], output_dir: Path) -> Path:
    """Figure 2 ― three-layer QoS-aware strategy: prices, capacity, QoS & utilization."""
    wholesale = np.asarray(record["wholesale_prices"])
    retail = np.asarray(record["retail_prices"])
    capacity = np.asarray(record["capacity"])
    qos_arr = np.asarray(record["qos"])
    util_arr = np.asarray(record["utilization"])
    qos_threshold = record.get("config", {}).get("qos_threshold", 0.82)
    periods = np.arange(1, wholesale.size + 1)

    fig, axes = plt.subplots(1, 3, figsize=(8.0, 2.8))
    fig.subplots_adjust(wspace=0.32, left=0.06, right=0.96, top=0.88, bottom=0.18)

    # ── (a) Wholesale & retail prices ────────────────────────────
    ax = axes[0]
    ax.plot(periods, wholesale, "s-", color=C["dark"], linewidth=2.0, markersize=5.5,
            markerfacecolor="white", markeredgewidth=1.2, label="Wholesale", zorder=5)
    retail_styles = [
        ("o--", C["red"],   "Retail 1"),
        ("^--", C["blue"],  "Retail 2"),
        ("d--", C["orange"],"Retail 3"),
    ]
    offsets = [-0.08, 0.0, 0.08]
    for idx, (style, color, label) in enumerate(retail_styles):
        ax.plot(periods, retail[idx] + offsets[idx], style, color=color,
                linewidth=1.3, markersize=4.5, markerfacecolor="white",
                markeredgewidth=0.9, label=label, alpha=0.9)
    ax.set_xticks(periods)
    ax.set_xticklabels(PERIOD_LABELS)
    ax.set_ylabel("Price (normalized units)")
    ax.set_title("(a) Wholesale & retail prices", loc="left", pad=4)
    ax.legend(frameon=True, edgecolor="#CCCCCC", fancybox=False,
              handlelength=1.8, borderpad=0.4, labelspacing=0.3,
              loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=4).set_zorder(10)
    ax.grid(axis="y", alpha=0.25, linewidth=0.4)

    # ── (b) Capacity allocation ──────────────────────────────────
    ax = axes[1]
    stack = ax.stackplot(periods, capacity, colors=CAPACITY_COLORS, alpha=0.85,
                         edgecolor="white", linewidth=0.5,
                         labels=["Intermediary 1", "Intermediary 2", "Intermediary 3"])
    ax.set_xticks(periods)
    ax.set_xticklabels(PERIOD_LABELS)
    ax.set_ylabel("Capacity")
    ax.set_title("(b) Capacity allocation", loc="left", pad=4)
    ax.legend(frameon=True, edgecolor="#CCCCCC", fancybox=False,
              fontsize=7, handlelength=1.4, borderpad=0.3, labelspacing=0.2)
    ax.set_ylim(0, ax.get_ylim()[1] * 1.08)

    # ── (c) QoS floor & peak utilization ─────────────────────────
    ax = axes[2]
    qos_min = np.min(qos_arr, axis=0)
    util_max = np.max(util_arr, axis=0)
    # QoS (left axis)
    ax.plot(periods, qos_min, "s-", color=C["green"], linewidth=2.2, markersize=5.5,
            markerfacecolor="white", markeredgewidth=1.2, label="QoS floor", zorder=5)
    ax.axhline(y=1.0, color="#AAAAAA", linestyle="--", linewidth=0.7, alpha=0.6)
    ax.set_ylabel("QoS", color=C["green"])
    ax.tick_params(axis="y", labelcolor=C["green"])
    ax.set_ylim(0.93, 1.05)
    # Utilization (right axis)
    ax2 = ax.twinx()
    ax2.plot(periods, util_max, "o--", color=C["red"], linewidth=1.5, markersize=5,
             markerfacecolor="white", markeredgewidth=1.0, label="Peak utilization")
    ax2.axhline(y=qos_threshold, color=C["red"], linestyle=":", linewidth=0.8, alpha=0.5)
    ax2.set_ylabel("Utilization", color=C["red"])
    ax2.tick_params(axis="y", labelcolor=C["red"])
    # combined legend
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, frameon=True,
              edgecolor="#CCCCCC", fancybox=False, fontsize=7,
              handlelength=1.8, borderpad=0.3, labelspacing=0.2,
              loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=3).set_zorder(10)
    ax.set_xticks(periods)
    ax.set_xticklabels(PERIOD_LABELS)
    ax.set_title("(c) QoS floor & utilization", loc="left", pad=4)
    ax.grid(axis="y", alpha=0.25, linewidth=0.4)

    plt.tight_layout()
    path = output_dir / "three_layer_policy_detail"
    fig.savefig(f"{path}.pdf")
    fig.savefig(f"{path}.svg")
    fig.savefig(f"{path}.png", dpi=300)
    plt.close(fig)
    return path.with_suffix(".pdf")


def plot_baseline_comparison(records: list[dict[str, Any]], output_dir: Path) -> Path:
    """Figure 3 ― five-strategy baseline comparison: profit, QoS, utilization."""
    # Collect data in strategy order
    data: dict[str, dict[str, float]] = {}
    for rec in records:
        policy = rec["policy"]
        if policy not in STRATEGY_ORDER:
            continue
        qos_arr = np.asarray(rec["qos"])
        util_arr = np.asarray(rec["utilization"])
        data[policy] = {
            "system_profit":    float(rec["system_profit"]),
            "platform_revenue": float(rec["platform_revenue"]),
            "intermed_profit":  float(rec["intermediary_profit"]),
            "min_qos":          float(np.min(qos_arr)),
            "max_utilization":  float(np.max(util_arr)),
        }

    labels = [STRATEGY_LABELS[p] for p in STRATEGY_ORDER]
    colors = [STRATEGY_COLORS[p] for p in STRATEGY_ORDER]
    profit = [data[p]["system_profit"] for p in STRATEGY_ORDER]
    qos = [data[p]["min_qos"] for p in STRATEGY_ORDER]
    util = [data[p]["max_utilization"] for p in STRATEGY_ORDER]
    x = np.arange(len(labels))

    fig, axes = plt.subplots(1, 3, figsize=(8.0, 2.8))
    fig.subplots_adjust(wspace=0.30, left=0.07, right=0.96, top=0.88, bottom=0.22)

    bar_kw = dict(edgecolor="white", linewidth=0.4, width=0.62)

    # ── (a) System profit ────────────────────────────────────────
    ax = axes[0]
    bars = ax.bar(x, profit, color=colors, **bar_kw)
    for bar, val in zip(bars, profit):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 150,
                f"{val:.0f}", ha="center", va="bottom", fontsize=6.5, color=C["dark"])
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=7)
    ax.set_title("(a) System profit", loc="left", pad=4)
    ax.set_ylabel("Profit")
    ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, _: f"{v:.0f}"))
    ax.grid(axis="y", alpha=0.25, linewidth=0.4)

    # ── (b) Minimum QoS ──────────────────────────────────────────
    ax = axes[1]
    bars = ax.bar(x, qos, color=colors, **bar_kw)
    for bar, val in zip(bars, qos):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                f"{val:.4f}", ha="center", va="bottom", fontsize=6.5, color=C["dark"])
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=7)
    ax.set_title("(b) Minimum QoS", loc="left", pad=4)
    ax.set_ylabel("QoS")
    ax.set_ylim(0.78, 1.08)
    ax.grid(axis="y", alpha=0.25, linewidth=0.4)

    # ── (c) Peak utilization ─────────────────────────────────────
    ax = axes[2]
    bars = ax.bar(x, util, color=colors, **bar_kw)
    for bar, val in zip(bars, util):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                f"{val:.4f}", ha="center", va="bottom", fontsize=6.5, color=C["dark"])
    ax.axhline(y=0.82, color=C["red"], linestyle=":", linewidth=0.8, alpha=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=7)
    ax.set_title("(c) Peak utilization", loc="left", pad=4)
    ax.set_ylabel("Utilization")
    ax.set_ylim(0.35, 1.05)
    ax.grid(axis="y", alpha=0.25, linewidth=0.4)

    plt.tight_layout()
    path = output_dir / "three_layer_baselines"
    fig.savefig(f"{path}.pdf")
    fig.savefig(f"{path}.svg")
    fig.savefig(f"{path}.png", dpi=300)
    plt.close(fig)
    return path.with_suffix(".pdf")
