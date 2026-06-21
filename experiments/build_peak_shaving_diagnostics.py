"""Build diagnostic figures from existing peak-shaving policy artifacts."""
import csv, json, sys
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from experiments.plot_style import configure_times_new_roman
from pricing_sim.peak_shaving_config import PeakShavingConfig
from pricing_sim.peak_shaving_equilibrium import FirmParams, intermediary_best_response
from pricing_sim.peak_shaving_market import (
    choice_shares_with_exit,
    firm_profit,
    inclusive_value,
    intermediary_profit,
    system_profit,
    type_channel_demand,
)

configure_times_new_roman()

SRC = ROOT / "artifacts" / "peak_shaving" / "20260618"
OUT = ROOT / "artifacts" / "peak_shaving" / "20260619"
FIG = ROOT / "figures" / "peak_shaving_diagnostics"
CAP = np.array([300.0, 120.0])
QOS_SHAPE = "sigmoid"
CASE_LABELS = {"uniform": "Uniform", "dynamic_coarse": "Dynamic coarse", "dynamic_fine": "Dynamic fine"}
REFERENCE_POLICY_COLORS = {
    "uniform": "#7884B4",
    "dynamic_coarse": "#E4CCD8",
    "dynamic_fine": "#F0C0CC",
}
COLORS = REFERENCE_POLICY_COLORS
REFERENCE_PARTICIPANT_COLORS = {
    "firm_A_profit": "#B4C0E4",
    "firm_B_profit": "#7884B4",
    "intermediary_profit": "#E4CCD8",
}
REFERENCE_USER_COLORS = {"rigid": "#484878", "elastic": "#F0C0CC"}
REFERENCE_LINE_COLOR = "#606060"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def serialise(value: Any) -> Any:
    if isinstance(value, np.ndarray): return value.tolist()
    if isinstance(value, dict): return {k: serialise(v) for k, v in value.items()}
    if isinstance(value, list): return [serialise(v) for v in value]
    if isinstance(value, (np.floating, np.integer)): return value.item()
    return value


def base_config(uniform: bool = False) -> PeakShavingConfig:
    cfg = PeakShavingConfig.default().evolve(firm_capacity=CAP, pop_rigid=0.4, pop_elastic=0.6)
    if uniform:
        cfg = cfg.evolve(load_shape_hat=np.zeros(cfg.num_periods))
    return cfg


def firm_components(idx: int, state, res: dict, cfg: PeakShavingConfig) -> dict[str, float]:
    h = cfg.period_hours
    demand = res["demand"]
    qos_firm = res["qos_firm"]
    intermediary_demand = demand[0]
    direct_demand = demand[1:][idx]
    routed = state.routing[idx] * intermediary_demand
    qos_m = qos_firm[idx]
    wholesale_rev = float(np.sum(state.wholesale[idx] * routed * qos_m * h))
    direct_rev = float(np.sum(state.direct[idx] * direct_demand * qos_m * h))
    idle_cost = float(cfg.capacity_cost * cfg.firm_capacity[idx] * h * cfg.num_periods)
    served = routed + direct_demand
    degrade_cost = float(np.sum(cfg.degrade_cost * (1.0 - qos_m) * served * h))
    return {"wholesale_revenue": wholesale_rev, "direct_revenue": direct_rev, "idle_cost": idle_cost,
            "degrade_cost": degrade_cost, "profit": wholesale_rev + direct_rev - idle_cost - degrade_cost}


def intermediary_components(state, res: dict, cfg: PeakShavingConfig) -> dict[str, float]:
    h = cfg.period_hours
    demand = res["demand"]
    intermediary_demand = demand[0]
    qos_channel = res["qos_channel"][0]
    avg_wholesale = np.sum(state.routing * state.wholesale, axis=0)
    retail_rev = float(np.sum(state.retail * intermediary_demand * qos_channel * h))
    wholesale_cost = float(np.sum(avg_wholesale * intermediary_demand * qos_channel * h))
    degrade_cost = float(np.sum(cfg.degrade_cost * (1.0 - qos_channel) * intermediary_demand * h))
    return {"retail_revenue": retail_rev, "wholesale_cost": wholesale_cost,
            "degrade_cost": degrade_cost, "profit": retail_rev - wholesale_cost - degrade_cost}


def evaluate_case(name: str, vectors: list[list[float]], uniform: bool, source: dict) -> dict[str, Any]:
    cfg = base_config(uniform=uniform)
    params = [FirmParams.from_vector(np.array(v, dtype=float)) for v in vectors]
    wholesale = np.vstack([params[0].wholesale(cfg), params[1].wholesale(cfg)])
    direct = np.vstack([params[0].direct(cfg), params[1].direct(cfg)])
    state, res = intermediary_best_response(wholesale, direct, cfg, qos_shape=QOS_SHAPE)
    return build_case_record(name, cfg, params, state, res, source)


def build_case_record(name: str, cfg, params, state, res: dict, source: dict) -> dict[str, Any]:
    prices = res["prices"]
    qos = res["qos_channel"]
    demand = res["demand"]
    served = demand * qos
    type_demand = {ut: type_channel_demand(prices, qos, cfg, ut) for ut in ("rigid", "elastic")}
    exit_prob = {ut: choice_shares_with_exit(prices, qos, cfg, ut)[1] for ut in ("rigid", "elastic")}
    inc_value = {ut: inclusive_value(prices, qos, cfg, ut) for ut in ("rigid", "elastic")}
    comps = {"firm_A": firm_components(0, state, res, cfg), "firm_B": firm_components(1, state, res, cfg),
             "intermediary": intermediary_components(state, res, cfg)}
    weighted_iv = cfg.pop_rigid * inc_value["rigid"] + cfg.pop_elastic * inc_value["elastic"]
    avg_price = float(np.sum(prices * demand) / max(np.sum(demand), 1e-12))
    return {
        "name": name,
        "source": source,
        "firm_params": [p.to_vector() for p in params],
        "prices": prices,
        "routing": state.routing,
        "demand": demand,
        "served": served,
        "type_demand": type_demand,
        "utilization": res["utilization"],
        "qos_firm": res["qos_firm"],
        "qos_channel": qos,
        "exit_probability": exit_prob,
        "inclusive_value": inc_value,
        "profit_components": comps,
        "summary": {
            "system_profit": system_profit(state, res, cfg),
            "firm_A_profit": firm_profit(0, state, res, cfg),
            "firm_B_profit": firm_profit(1, state, res, cfg),
            "intermediary_profit": intermediary_profit(state, res, cfg),
            "peak_utilization": float(res["utilization"].max()),
            "minimum_qos": float(res["qos_firm"].min()),
            "total_demand_volume": float(np.sum(demand) * cfg.period_hours),
            "served_volume": float(np.sum(served) * cfg.period_hours),
            "average_paid_price": avg_price,
            "weighted_inclusive_value": weighted_iv,
        },
    }


def build_records() -> dict[str, Any]:
    congested = load_json(SRC / "peak_shaving_congested_fp.json")
    coarse = load_json(SRC / "peak_shaving_fp_dynamic_converged.json")
    fine = load_json(SRC / "peak_shaving_fp_dynamic_converged_fine.json")
    ckpt = load_json(SRC / "fp_dynamic_ckpt.json")
    ckpt_fine = load_json(SRC / "fp_dynamic_ckpt_fine.json")
    records = {
        "uniform": evaluate_case("uniform", congested["uniform"]["firm_params"], True, congested["uniform"]),
        "dynamic_coarse": evaluate_case("dynamic_coarse", coarse["firm_params"], False, coarse | {"checkpoint": ckpt}),
        "dynamic_fine": evaluate_case("dynamic_fine", fine["firm_params"], False, fine | {"checkpoint": ckpt_fine}),
    }
    meta = {
        "source_artifacts": str(SRC.relative_to(ROOT)),
        "qos_shape": QOS_SHAPE,
        "congested_capacity": CAP.tolist(),
        "uniform_converged": congested["uniform"].get("converged"),
        "dynamic_coarse_round": ckpt["round"],
        "dynamic_coarse_maxregret": ckpt["maxreg"],
        "dynamic_fine_round": ckpt_fine["round"],
        "dynamic_fine_maxregret": ckpt_fine["maxreg"],
        "note": "Diagnostics reconstruct reported policy snapshots; no new equilibrium search is run.",
    }
    return {"metadata": meta, "cases": records}


def write_tables(bundle: dict[str, Any]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "peak_shaving_diagnostics.json").write_text(
        json.dumps(serialise(bundle), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    rows = [{"case": name, "metric": m, "value": v}
            for name, rec in bundle["cases"].items()
            for m, v in {**rec["summary"], **{f"exit_probability_{u}": x for u, x in rec["exit_probability"].items()}}.items()]
    with (OUT / "peak_shaving_mechanism_summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["case", "metric", "value"])
        writer.writeheader()
        writer.writerows(rows)
    rows = [{"case": name, "period": t + 1, "total_demand": float(rec["demand"][:, t].sum()),
             "served_demand": float(rec["served"][:, t].sum()),
             "peak_utilization": float(rec["utilization"][:, t].max()),
             "minimum_firm_qos": float(rec["qos_firm"][:, t].min()),
             "intermediary_price": float(rec["prices"][0, t])}
            for name, rec in bundle["cases"].items() for t in range(rec["demand"].shape[1])]
    with (OUT / "peak_shaving_time_profiles.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def plot_market_schematic() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9.4, 5.1))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    def panel(x, y, w, h, fc, ec, lw=1.2):
        patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.018,rounding_size=0.025",
                               facecolor=fc, edgecolor=ec, linewidth=lw)
        ax.add_patch(patch)
        return patch

    def arrow(start, end, *, dashed=False, rad=0.0, color="#333333", lw=1.4):
        patch = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=12,
                                connectionstyle=f"arc3,rad={rad}", linewidth=lw,
                                linestyle="--" if dashed else "-", color=color)
        ax.add_patch(patch)
        return patch

    def user_icon(cx, cy, scale=1.0, color="#1F3A24"):
        ax.add_patch(Circle((cx, cy + 0.035 * scale), 0.022 * scale, fill=False, ec=color, lw=1.6))
        ax.add_patch(FancyBboxPatch((cx - 0.035 * scale, cy - 0.035 * scale), 0.07 * scale, 0.055 * scale,
                                    boxstyle="round,pad=0.004,rounding_size=0.012",
                                    facecolor="none", edgecolor=color, linewidth=1.6))
        for dx in (-0.065, 0.065):
            ax.add_patch(Circle((cx + dx * scale, cy + 0.02 * scale), 0.014 * scale, fill=False, ec=color, lw=1.2))
            ax.plot([cx + dx * scale - 0.025 * scale, cx + dx * scale + 0.025 * scale],
                    [cy - 0.018 * scale, cy - 0.018 * scale], color=color, lw=1.2)

    def server_icon(x, y, scale=1.0):
        for i in range(3):
            ax.add_patch(FancyBboxPatch((x, y + i * 0.038 * scale), 0.075 * scale, 0.03 * scale,
                                        boxstyle="round,pad=0.002,rounding_size=0.004",
                                        facecolor="#D9E7F7", edgecolor="#1F3B57", linewidth=1.1))
            ax.add_patch(Circle((x + 0.061 * scale, y + i * 0.038 * scale + 0.015 * scale),
                                0.0045 * scale, color="#1F3B57"))
        ax.add_patch(Rectangle((x + 0.088 * scale, y + 0.02 * scale), 0.065 * scale, 0.06 * scale,
                               facecolor="#E9F2FC", edgecolor="#1F3B57", linewidth=1.1))
        for j in range(3):
            ax.add_patch(Circle((x + 0.103 * scale + j * 0.018 * scale, y + 0.05 * scale),
                                0.011 * scale, fill=False, edgecolor="#1F3B57", linewidth=1.0))

    panel(0.03, 0.31, 0.19, 0.48, "#EAF6E1", "#4F7D3C")
    ax.text(0.125, 0.755, "Users", ha="center", va="center", fontsize=15, fontweight="bold")
    panel(0.055, 0.56, 0.14, 0.15, "#F5FAEE", "#6A9658")
    ax.text(0.125, 0.675, "Time-rigid users", ha="center", va="center", fontsize=10.5, fontweight="bold")
    user_icon(0.125, 0.605, 0.82)
    panel(0.055, 0.36, 0.14, 0.15, "#F5FAEE", "#6A9658")
    ax.text(0.125, 0.475, "Time-flexible users", ha="center", va="center", fontsize=10.5, fontweight="bold")
    user_icon(0.125, 0.405, 0.82)

    panel(0.04, 0.06, 0.17, 0.11, "#F5F5F5", "#666666")
    ax.text(0.125, 0.14, "Outside option", ha="center", va="center", fontsize=11.5, fontweight="bold")
    user_icon(0.125, 0.075, 0.55, color="#555555")

    panel(0.36, 0.35, 0.27, 0.30, "#FFF0DB", "#CC7A1C")
    ax.text(0.495, 0.605, "API Intermediary", ha="center", va="center", fontsize=14, fontweight="bold")
    panel(0.385, 0.495, 0.22, 0.08, "#FFF8EF", "#D98A31", lw=1.0)
    ax.text(0.495, 0.535, r"Retail price $p_t$", ha="center", va="center", fontsize=11.5)
    panel(0.385, 0.385, 0.22, 0.08, "#FFF8EF", "#D98A31", lw=1.0)
    ax.text(0.495, 0.425, r"QoS-aware routing $r_{m,t}$", ha="center", va="center", fontsize=11.5)

    panel(0.76, 0.58, 0.20, 0.22, "#EAF3FF", "#2E5D9F")
    ax.text(0.86, 0.755, "Provider A", ha="center", va="center", fontsize=13.5, fontweight="bold")
    ax.text(0.86, 0.705, r"Large GPU capacity $G_A$", ha="center", va="center", fontsize=10.0)
    server_icon(0.79, 0.59, 0.82)

    panel(0.76, 0.22, 0.20, 0.22, "#EAF3FF", "#2E5D9F")
    ax.text(0.86, 0.395, "Provider B", ha="center", va="center", fontsize=13.5, fontweight="bold")
    ax.text(0.86, 0.345, r"Small GPU capacity $G_B$", ha="center", va="center", fontsize=10.0)
    server_icon(0.79, 0.23, 0.82)

    arrow((0.22, 0.50), (0.36, 0.50), lw=1.7)
    ax.text(0.29, 0.535, "brokered API\npurchase", ha="center", va="bottom", fontsize=9.5)
    arrow((0.63, 0.555), (0.76, 0.70), lw=1.6)
    arrow((0.63, 0.445), (0.76, 0.315), lw=1.6)
    arrow((0.76, 0.61), (0.63, 0.525), dashed=True, lw=1.1, color="#666666")
    arrow((0.76, 0.265), (0.63, 0.405), dashed=True, lw=1.1, color="#666666")
    ax.text(0.68, 0.595, "routed traffic", ha="center", va="center", fontsize=8.8, color="#333333")
    ax.text(0.685, 0.385, r"QoS feedback $q_{m,t}$", ha="center", va="center", fontsize=8.8, color="#555555")
    arrow((0.22, 0.68), (0.76, 0.73), dashed=True, rad=-0.18, lw=1.4)
    arrow((0.22, 0.40), (0.76, 0.27), dashed=True, rad=0.18, lw=1.4)
    ax.text(0.50, 0.765, "direct API access", ha="center", va="center", fontsize=10.5)
    ax.text(0.50, 0.255, "direct API access", ha="center", va="center", fontsize=10.5)
    arrow((0.125, 0.31), (0.125, 0.17), lw=1.5)
    ax.text(0.17, 0.225, "exit /\nno purchase", ha="center", va="center", fontsize=9.5)

    ax.text(0.50, 0.92, "Inference-Service Market Structure",
            ha="center", va="center", fontsize=20, fontweight="bold")
    fig.savefig(FIG / "market_schematic.pdf", bbox_inches="tight")
    plt.close(fig)


def plot_qos_utilization(bundle: dict[str, Any]) -> None:
    t = np.arange(1, 9)
    fig, axes = plt.subplots(2, 1, figsize=(7.4, 5.55), sharex=True)
    for name, rec in bundle["cases"].items():
        axes[0].plot(t, rec["utilization"].max(axis=0), marker="o", label=CASE_LABELS[name], color=COLORS[name])
        axes[1].plot(t, rec["qos_firm"].min(axis=0), marker="o", label=CASE_LABELS[name], color=COLORS[name])
    axes[0].axhline(0.82, color=REFERENCE_LINE_COLOR, lw=1, ls="--", label="QoS threshold")
    axes[0].set_ylabel("Peak firm utilization"); axes[1].set_ylabel("Minimum firm QoS")
    axes[1].set_xlabel("Period")
    for ax in axes:
        ax.grid(alpha=0.25)
        ax.margins(y=0.14)
    handles, labels = axes[0].get_legend_handles_labels()
    axes[0].legend(handles, labels, frameon=False, ncol=4, loc="lower center",
                   bbox_to_anchor=(0.5, 1.0), fontsize=7.6,
                   borderaxespad=0.0, handlelength=1.5, columnspacing=0.9)
    fig.tight_layout(rect=[0, 0, 1, 0.985])
    fig.savefig(FIG / "qos_utilization_profiles.pdf")
    plt.close(fig)


def plot_mechanism(bundle: dict[str, Any]) -> None:
    names = list(bundle["cases"])
    x = np.arange(len(names))
    fig, axes = plt.subplots(2, 2, figsize=(8.2, 6.65))
    strategy_handles = [Patch(facecolor=REFERENCE_POLICY_COLORS[n], edgecolor="none", label=CASE_LABELS[n]) for n in names]
    for ax, metric, title, panel_label in [
        (axes[0, 0], "average_paid_price", "Average paid price", "(a)"),
        (axes[1, 0], "served_volume", "QoS-adjusted served volume", "(c)"),
        (axes[1, 1], "weighted_inclusive_value", "Population-weighted inclusive value", "(d)"),
    ]:
        ax.bar(x, [bundle["cases"][n]["summary"][metric] for n in names],
               color=[REFERENCE_POLICY_COLORS[n] for n in names])
        ax.set_title(title, fontsize=10, fontweight="bold", loc="left", pad=8)
        ax.text(0.5, -0.34, panel_label, transform=ax.transAxes, ha="center",
                va="top", fontsize=9, fontweight="bold", clip_on=False)
        loc = "upper right" if ax is axes[0, 0] else "upper left"
        ax.legend(handles=strategy_handles, frameon=False, fontsize=7, loc=loc,
                  borderaxespad=0.25, handlelength=1.2, labelspacing=0.25)
    rigid = [bundle["cases"][n]["exit_probability"]["rigid"] for n in names]
    elastic = [bundle["cases"][n]["exit_probability"]["elastic"] for n in names]
    axes[0, 1].bar(x - 0.18, rigid, 0.36, label="Rigid", color=REFERENCE_USER_COLORS["rigid"])
    axes[0, 1].bar(x + 0.18, elastic, 0.36, label="Elastic", color=REFERENCE_USER_COLORS["elastic"])
    axes[0, 1].set_title("No-purchase probability", fontsize=10, fontweight="bold", loc="left", pad=8)
    axes[0, 1].text(0.5, -0.34, "(b)", transform=axes[0, 1].transAxes, ha="center",
                    va="top", fontsize=9, fontweight="bold", clip_on=False)
    axes[0, 1].legend(frameon=False, fontsize=8, loc="upper right")
    for ax in axes.ravel():
        ax.set_xticks(x, [CASE_LABELS[n] for n in names], rotation=18, ha="right")
        ax.grid(axis="y", alpha=0.25)
        ax.margins(y=0.22)
    fig.tight_layout(pad=1.2, h_pad=3.2, w_pad=1.8)
    fig.subplots_adjust(bottom=0.12)
    fig.savefig(FIG / "mechanism_diagnostics.pdf")
    plt.close(fig)


def plot_profit_regret(bundle: dict[str, Any]) -> None:
    names = list(bundle["cases"])
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.9))
    bottom = np.zeros(len(names))
    parts = [("firm_A_profit", REFERENCE_PARTICIPANT_COLORS["firm_A_profit"], "Provider A"),
             ("firm_B_profit", REFERENCE_PARTICIPANT_COLORS["firm_B_profit"], "Provider B"),
             ("intermediary_profit", REFERENCE_PARTICIPANT_COLORS["intermediary_profit"], "Intermediary")]
    handles = []
    legend_labels = []
    for key, color, label in parts:
        vals = np.array([bundle["cases"][n]["summary"][key] for n in names])
        handle = axes[0].bar(np.arange(len(names)), vals, bottom=bottom, label=label, color=color)
        handles.append(handle[0])
        legend_labels.append(label)
        bottom += vals
    axes[0].set_title("Profit by market participant", fontsize=10)
    axes[0].set_xlim(-0.6, len(names) - 0.05)
    axes[0].legend(handles, legend_labels, frameon=False, fontsize=7.5,
                   loc="upper left", ncol=1, handlelength=1.3,
                   labelspacing=0.25, borderaxespad=0.25)
    meta = bundle["metadata"]
    axes[1].bar([0, 1], [meta["dynamic_coarse_maxregret"], meta["dynamic_fine_maxregret"]],
                color=[REFERENCE_POLICY_COLORS["dynamic_coarse"], REFERENCE_POLICY_COLORS["dynamic_fine"]])
    axes[1].axhline(5.0, color=REFERENCE_LINE_COLOR, lw=1, ls="--", label="target < 5")
    axes[1].set_xticks([0, 1], ["Coarse\nround 22", "Fine\nround 40"])
    axes[1].set_title("Final stored max regret", fontsize=10)
    axes[1].set_xlim(-0.55, 1.55)
    regret_handles = [
        Patch(facecolor=REFERENCE_POLICY_COLORS["dynamic_coarse"], edgecolor="none", label="Dynamic coarse"),
        Patch(facecolor=REFERENCE_POLICY_COLORS["dynamic_fine"], edgecolor="none", label="Dynamic fine"),
        Line2D([0], [0], color=REFERENCE_LINE_COLOR, lw=1, ls="--", label="target < 5"),
    ]
    axes[1].legend(handles=regret_handles, frameon=False, fontsize=7.5, loc="upper left",
                   borderaxespad=0.35, handlelength=1.4, labelspacing=0.3)
    axes[0].set_xticks(np.arange(len(names)), [CASE_LABELS[n] for n in names], rotation=18, ha="right")
    for ax in axes:
        ax.grid(axis="y", alpha=0.25)
        ax.margins(y=0.16)
    fig.tight_layout(pad=1.0)
    fig.savefig(FIG / "profit_components_and_regret.pdf")
    plt.close(fig)


def validate(bundle: dict[str, Any]) -> list[str]:
    warnings = []
    checks = {"uniform": ("system_profit", 1783.239231608924),
              "dynamic_coarse": ("system_profit", 1948.7877581277107),
              "dynamic_fine": ("system_profit", 1748.7937984034195)}
    for name, (metric, expected) in checks.items():
        actual = bundle["cases"][name]["summary"][metric]
        if abs(actual - expected) > 1.0:
            warnings.append(f"{name}.{metric}: expected {expected:.3f}, got {actual:.3f}")
    return warnings


if __name__ == "__main__":
    bundle = build_records()
    warnings = validate(bundle)
    bundle["metadata"]["validation_warnings"] = warnings
    write_tables(bundle)
    plot_market_schematic()
    plot_qos_utilization(bundle)
    plot_mechanism(bundle)
    plot_profit_regret(bundle)
    print(json.dumps({
        "output_dir": str(OUT.relative_to(ROOT)),
        "figure_dir": str(FIG.relative_to(ROOT)),
        "validation_warnings": warnings,
    }, ensure_ascii=False, indent=2))
