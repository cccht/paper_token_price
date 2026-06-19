"""Build reference-aligned figures for the SCI main manuscript."""

from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path
from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "figures" / "reference_aligned"
MAIN_RUN = ROOT / "artifacts" / "intermediary" / "20260608-144953"
SCI_RUN = ROOT / "artifacts" / "intermediary_sci" / "20260608-150237"
REALISM_RUN = ROOT / "artifacts" / "intermediary_realism" / "20260608-145715"
REVIEWER_RUN = ROOT / "artifacts" / "reviewer_response" / "20260608-151841"
STRENGTHENING_RUN = ROOT / "artifacts" / "review_strengthening" / "20260608-145716"

COLORS = ["#0072B2", "#D55E00", "#009E73", "#E69F00", "#CC79A7", "#56B4E9"]
POLICY_LABEL = {
    "uniform_retail": "Uniform retail",
    "direct_platform": "Direct platform",
    "single_intermediary": "Single broker",
    "no_qos_pricing": "No-QoS dynamic",
    "three_layer_qos_aware": "Three-layer QoS",
}

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "font.size": 8,
    "axes.unicode_minus": False,
})


def _csv_rows(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return [{key: _coerce(value) for key, value in row.items()} for row in rows]


def _coerce(value: str) -> Any:
    if value in {"", "True", "False"}:
        return {"": "", "True": True, "False": False}[value]
    try:
        return float(value)
    except ValueError:
        return value


def _records() -> list[dict[str, Any]]:
    return json.loads((MAIN_RUN / "three_layer_records.json").read_text(encoding="utf-8"))


def _record(policy: str) -> dict[str, Any]:
    return next(item for item in _records() if item["policy"] == policy)


def _save(fig: plt.Figure, stem: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for suffix in (".pdf", ".svg"):
        fig.savefig(OUT_DIR / f"{stem}{suffix}", bbox_inches="tight")
    plt.close(fig)


def copy_static_figures() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    sources = [
        (MAIN_RUN, "three_layer_baselines"),
        (MAIN_RUN, "three_layer_policy_detail"),
        (REVIEWER_RUN, "attribution_ablation"),
        (REVIEWER_RUN, "profit_slices"),
        (REVIEWER_RUN, "finite_psne_logit"),
        (STRENGTHENING_RUN, "user_protection_frontier"),
        (STRENGTHENING_RUN, "direct_api_sensitivity"),
    ]
    for directory, stem in sources:
        for suffix in (".pdf", ".svg"):
            source = directory / f"{stem}{suffix}"
            if source.exists():
                shutil.copyfile(source, OUT_DIR / f"{stem}{suffix}")


def _box(ax: plt.Axes, xy: tuple[float, float], text: str, color: str, w: float = 0.23, h: float = 0.14) -> None:
    patch = FancyBboxPatch(
        xy,
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.02",
        linewidth=1.0,
        facecolor=color,
        edgecolor="#333333",
        alpha=0.92,
    )
    ax.add_patch(patch)
    ax.text(xy[0] + w / 2, xy[1] + h / 2, text, ha="center", va="center", fontsize=8)


def _arrow(ax: plt.Axes, start: tuple[float, float], end: tuple[float, float], label: str = "") -> None:
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=11, lw=1.0, color="#333333"))
    if label:
        mid = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
        ax.text(mid[0], mid[1] + 0.025, label, ha="center", va="bottom", fontsize=7)


def information_flow() -> None:
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ax.set_axis_off()
    _box(ax, (0.04, 0.66), "Model/API\nprovider", "#D7EAF7")
    _box(ax, (0.38, 0.66), "Wholesale\nplatform", "#FFF2CC")
    _box(ax, (0.72, 0.66), "API brokers\nand resellers", "#DDEFD5")
    _box(ax, (0.18, 0.30), "Applications\nand users", "#F8D7DA")
    _box(ax, (0.58, 0.30), "QoS monitor\nand billing", "#E8E1F5")
    _arrow(ax, (0.28, 0.71), (0.38, 0.71), "capacity")
    _arrow(ax, (0.62, 0.71), (0.72, 0.71), "wholesale price")
    _arrow(ax, (0.80, 0.66), (0.36, 0.42))
    _arrow(ax, (0.41, 0.37), (0.58, 0.37), "demand")
    _arrow(ax, (0.68, 0.44), (0.50, 0.66))
    ax.text(0.57, 0.55, "retail price", ha="center", fontsize=7)
    ax.text(0.64, 0.51, "QoS feedback", ha="center", fontsize=7)
    ax.text(0.03, 0.08, "Decision order: wholesale price -> broker price/capacity -> user migration -> QoS and revenue feedback", fontsize=8)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    _save(fig, "information_interaction")


def fixed_point_map() -> None:
    fig, ax = plt.subplots(figsize=(6.8, 3.2))
    ax.set_axis_off()
    _box(ax, (0.05, 0.50), "Upper map\nfP(w | x)", "#D7EAF7", 0.25, 0.18)
    _box(ax, (0.38, 0.50), "Middle map\nfI(p,g | w,s)", "#DDEFD5", 0.25, 0.18)
    _box(ax, (0.71, 0.50), "Lower map\nfU(s | p,g,q)", "#F8D7DA", 0.25, 0.18)
    _arrow(ax, (0.30, 0.59), (0.38, 0.59))
    _arrow(ax, (0.63, 0.59), (0.71, 0.59))
    ax.text(0.34, 0.65, "w", ha="center", fontsize=8)
    ax.text(0.67, 0.65, "p,g,q", ha="center", fontsize=8)
    ax.plot([0.83, 0.83, 0.18, 0.18], [0.50, 0.25, 0.25, 0.50], color="#555555", lw=1.0)
    ax.text(0.50, 0.29, "shares and effective demand", ha="center", va="bottom", fontsize=8)
    ax.text(0.50, 0.14, "A candidate response is accepted only with small unilateral-improvement regret.", ha="center", fontsize=8)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    _save(fig, "fixed_point_candidate_response")


def market_topology() -> None:
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ax.set_axis_off()
    xs = [0.14, 0.38, 0.62, 0.86]
    for x, text in zip(xs, ["DeepSeek\nAPI", "Claude\nAPI", "GPT/OpenAI\nAPI", "Other model\nAPIs"]):
        _box(ax, (x - 0.09, 0.72), text, "#D7EAF7", 0.18, 0.13)
        _arrow(ax, (x, 0.72), (0.50, 0.58))
    _box(ax, (0.37, 0.46), "Platform\nwholesale layer", "#FFF2CC", 0.26, 0.14)
    for x, text in zip([0.20, 0.50, 0.80], ["Broker 1", "Broker 2", "Broker 3"]):
        _box(ax, (x - 0.08, 0.22), text, "#DDEFD5", 0.16, 0.12)
        _arrow(ax, (0.50, 0.46), (x, 0.34), "w")
        _arrow(ax, (x, 0.22), (0.50, 0.12), "p,g")
    _box(ax, (0.40, 0.02), "User classes\nand time slots", "#F8D7DA", 0.20, 0.10)
    _box(ax, (0.70, 0.02), "Direct API\noutside option", "#E8E1F5", 0.20, 0.10)
    _arrow(ax, (0.50, 0.46), (0.80, 0.12), "pD,gD")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    _save(fig, "api_market_topology")


def time_profile_inputs() -> None:
    rec = _record("three_layer_qos_aware")
    cfg = rec["config"]
    periods = np.arange(1, 9)
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.0))
    axes[0].plot(periods, cfg["time_preference"], "o-", color=COLORS[0], label="preference")
    axes[0].plot(periods, cfg["native_period_distribution"], "s--", color=COLORS[2], label="native share")
    axes[1].bar(periods, cfg["rigid_baseline"], color=COLORS[3], label="rigid")
    axes[1].plot(periods, np.array(cfg["time_preference"]) * cfg["flexible_baseline"], "o-", color=COLORS[1], label="flexible index")
    axes[2].bar(np.arange(1, 4), cfg["intermediary_capacity"], color=COLORS[:3])
    for ax in axes:
        ax.grid(alpha=0.25)
    axes[0].set_title("User time profile")
    axes[1].set_title("Demand inputs")
    axes[2].set_title("Broker capacity budgets")
    axes[0].legend(fontsize=7)
    axes[1].legend(fontsize=7)
    axes[0].set_xlabel("Period")
    axes[1].set_xlabel("Period")
    axes[2].set_xlabel("Broker")
    _save(fig, "time_profile_inputs")


def convergence_diagnostics() -> None:
    rows = _csv_rows(SCI_RUN / "platform_trials.csv")
    x = [row["platform_trials"] for row in rows]
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.0))
    axes[0].plot(x, [row["platform_revenue"] for row in rows], "o-", color=COLORS[0], label="platform")
    axes[0].plot(x, [row["system_profit"] for row in rows], "s--", color=COLORS[2], label="system")
    axes[1].plot(x, [row["objective_evaluations"] for row in rows], "o-", color=COLORS[1])
    axes[2].semilogy(x, [max(float(row["max_nash_regret"]), 1e-12) for row in rows], "o-", color=COLORS[4])
    for ax, title in zip(axes, ["Best objective", "Function evaluations", "Regret diagnostic"]):
        ax.set_title(title)
        ax.set_xlabel("Platform candidates")
        ax.grid(alpha=0.25)
    axes[0].legend(fontsize=7)
    _save(fig, "convergence_diagnostics")


def stakeholder_objectives() -> None:
    rows = _csv_rows(MAIN_RUN / "three_layer_summary.csv")
    labels = [POLICY_LABEL[row["policy"]].replace(" ", "\n") for row in rows]
    x = np.arange(len(rows))
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 3.2))
    axes[0].bar(x - 0.18, [row["platform_revenue"] for row in rows], 0.36, label="Platform", color=COLORS[0])
    axes[0].bar(x + 0.18, [row["intermediary_profit"] for row in rows], 0.36, label="Brokers", color=COLORS[2])
    axes[1].bar(x, [row["system_profit"] for row in rows], color=COLORS[3])
    for ax in axes:
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=20, ha="right")
        ax.grid(axis="y", alpha=0.25)
    axes[0].set_title("Stakeholder payoff")
    axes[1].set_title("System profit")
    axes[0].legend(fontsize=7)
    _save(fig, "stakeholder_objectives")


def price_curves() -> None:
    rec = _record("three_layer_qos_aware")
    p = np.array(rec["retail_prices"])
    periods = np.arange(1, p.shape[1] + 1)
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    ax.plot(periods, rec["wholesale_prices"], "o-", color=COLORS[0], label="Wholesale")
    ax.plot(periods, p.mean(axis=0), "s-", color=COLORS[1], label="Mean retail")
    ax.fill_between(periods, p.min(axis=0), p.max(axis=0), color=COLORS[1], alpha=0.18, label="Retail range")
    ax.set_xlabel("Period")
    ax.set_ylabel("Normalized price")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=7)
    _save(fig, "equilibrium_price_curves")


def demand_service_balance() -> None:
    rec = _record("three_layer_qos_aware")
    demand = np.array(rec["demand"])
    served = demand * np.array(rec["qos"])
    periods = np.arange(1, demand.shape[1] + 1)
    fig, ax = plt.subplots(figsize=(7.0, 3.2))
    bottom = np.zeros(demand.shape[1])
    for idx, color in enumerate(COLORS[:3]):
        ax.bar(periods, demand[idx], bottom=bottom, color=color, alpha=0.72, label=f"Broker {idx + 1}")
        bottom += demand[idx]
    ax.plot(periods, served.sum(axis=0), "k.-", label="Effective served")
    ax.set_xlabel("Period")
    ax.set_ylabel("Token-demand units")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(fontsize=7, ncol=2)
    _save(fig, "demand_service_balance")


def qos_utilization_balance() -> None:
    rec = _record("three_layer_qos_aware")
    util = np.array(rec["utilization"])
    qos = np.array(rec["qos"])
    periods = np.arange(1, util.shape[1] + 1)
    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.2))
    axes[0].plot(periods, util.max(axis=0), "o-", color=COLORS[1], label="peak utilization")
    axes[0].axhline(rec["config"]["qos_threshold"], ls="--", color="#555555", label="QoS threshold")
    axes[1].plot(periods, qos.min(axis=0), "s-", color=COLORS[2], label="QoS floor")
    for ax in axes:
        ax.set_xlabel("Period")
        ax.grid(alpha=0.25)
        ax.legend(fontsize=7)
    axes[0].set_ylabel("Utilization")
    axes[1].set_ylabel("QoS")
    _save(fig, "qos_utilization_balance")


def capacity_allocation() -> None:
    rec = _record("three_layer_qos_aware")
    cap = np.array(rec["capacity"])
    fig, ax = plt.subplots(figsize=(7.0, 3.2))
    image = ax.imshow(cap, aspect="auto", cmap="YlGnBu")
    ax.set_xlabel("Period")
    ax.set_ylabel("Broker")
    ax.set_xticks(np.arange(cap.shape[1]), np.arange(1, cap.shape[1] + 1))
    ax.set_yticks(np.arange(cap.shape[0]), np.arange(1, cap.shape[0] + 1))
    for i in range(cap.shape[0]):
        for j in range(cap.shape[1]):
            ax.text(j, i, f"{cap[i, j]:.0f}", ha="center", va="center", fontsize=7)
    fig.colorbar(image, ax=ax, fraction=0.032, pad=0.02, label="capacity")
    _save(fig, "capacity_allocation_heatmap")


def load_shift() -> None:
    records = {item["policy"]: item for item in _records()}
    periods = np.arange(1, 9)
    fig, ax = plt.subplots(figsize=(7.0, 3.2))
    for policy, color in [("uniform_retail", COLORS[3]), ("no_qos_pricing", COLORS[1]), ("three_layer_qos_aware", COLORS[0])]:
        total = np.array(records[policy]["demand"]).sum(axis=0)
        ax.plot(periods, total, "o-", color=color, label=POLICY_LABEL[policy])
    ax.set_xlabel("Period")
    ax.set_ylabel("Total demand")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=7)
    _save(fig, "load_shift_comparison")


def arrival_vllm_boundary() -> None:
    arrival = _csv_rows(REALISM_RUN / "arrival_replay.csv")
    vllm = _csv_rows(REALISM_RUN / "vllm_pressure.csv")
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.2))
    labels = [POLICY_LABEL[row["policy"]].replace(" ", "\n") for row in arrival]
    x = np.arange(len(arrival))
    axes[0].bar(x, [row["system_profit"] for row in arrival], color=COLORS[: len(arrival)])
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels, rotation=20, ha="right")
    axes[0].set_title("Measured-arrival replay")
    for profile, color in [("vllm-0.5b", COLORS[0]), ("vllm-3b", COLORS[1])]:
        selected = [row for row in vllm if row["profile"] == profile]
        shortfall = [(1.0 - row["active_min_qos"]) * 1e9 for row in selected]
        axes[1].plot([row["demand_scale"] for row in selected], shortfall, "o-", color=color, label=profile)
    axes[1].set_title("vLLM QoS substitution")
    axes[1].set_xlabel("Demand scale")
    axes[1].set_ylabel("QoS shortfall (1e-9)")
    axes[1].legend(fontsize=7)
    for ax in axes:
        ax.grid(alpha=0.25)
    _save(fig, "arrival_vllm_boundary")


def main() -> None:
    copy_static_figures()
    fixed_point_map()
    time_profile_inputs()
    convergence_diagnostics()
    stakeholder_objectives()
    price_curves()
    demand_service_balance()
    qos_utilization_balance()
    capacity_allocation()
    load_shift()
    arrival_vllm_boundary()
    print(f"output={OUT_DIR}")


if __name__ == "__main__":
    main()
