"""Build diagnostic figures from existing peak-shaving policy artifacts."""
import csv, json, sys
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

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

SRC = ROOT / "artifacts" / "peak_shaving" / "20260618"
OUT = ROOT / "artifacts" / "peak_shaving" / "20260619"
FIG = ROOT / "figures" / "peak_shaving_diagnostics"
CAP = np.array([300.0, 120.0])
QOS_SHAPE = "sigmoid"
CASE_LABELS = {"uniform": "Uniform", "dynamic_coarse": "Dynamic coarse", "dynamic_fine": "Dynamic fine"}
COLORS = {"uniform": "#4C78A8", "dynamic_coarse": "#F58518", "dynamic_fine": "#54A24B"}


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
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    ax.axis("off")
    boxes = [("Users\nrigid / elastic", 0.08, 0.55), ("Intermediary\nretail price + routing", 0.43, 0.55),
             ("Firm A\nlarge capacity", 0.78, 0.72), ("Firm B\nsmall capacity", 0.78, 0.36),
             ("Outside option", 0.08, 0.18)]
    for text, x, y in boxes:
        ax.text(x, y, text, ha="center", va="center", fontsize=10,
                bbox=dict(boxstyle="round,pad=0.35", facecolor="#F7F7F7", edgecolor="#444444"))
    arrows = [((0.21, 0.55), (0.32, 0.55)), ((0.54, 0.62), (0.68, 0.72)),
              ((0.54, 0.48), (0.68, 0.36)), ((0.21, 0.50), (0.69, 0.71)),
              ((0.21, 0.44), (0.69, 0.37)), ((0.08, 0.45), (0.08, 0.29))]
    for start, end in arrows:
        ax.annotate("", xy=end, xytext=start, arrowprops=dict(arrowstyle="->", lw=1.5, color="#555555"))
    ax.text(0.43, 0.87, "Fixed GPU capacity, time-varying demand, QoS feedback", ha="center", fontsize=11)
    fig.savefig(FIG / "market_schematic.pdf", bbox_inches="tight")
    plt.close(fig)


def plot_qos_utilization(bundle: dict[str, Any]) -> None:
    t = np.arange(1, 9)
    fig, axes = plt.subplots(2, 1, figsize=(7.2, 5.6), sharex=True)
    for name, rec in bundle["cases"].items():
        axes[0].plot(t, rec["utilization"].max(axis=0), marker="o", label=CASE_LABELS[name], color=COLORS[name])
        axes[1].plot(t, rec["qos_firm"].min(axis=0), marker="o", label=CASE_LABELS[name], color=COLORS[name])
    axes[0].axhline(0.82, color="#666666", lw=1, ls="--", label="QoS threshold")
    axes[0].set_ylabel("Peak firm utilization"); axes[1].set_ylabel("Minimum firm QoS")
    axes[1].set_xlabel("Period")
    for ax in axes:
        ax.grid(alpha=0.25)
        ax.legend(frameon=False, ncol=2, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "qos_utilization_profiles.pdf")
    plt.close(fig)


def plot_mechanism(bundle: dict[str, Any]) -> None:
    names = list(bundle["cases"])
    x = np.arange(len(names))
    fig, axes = plt.subplots(2, 2, figsize=(8.0, 6.0))
    for ax, metric, title in [
        (axes[0, 0], "average_paid_price", "Average paid price"),
        (axes[1, 0], "served_volume", "QoS-adjusted served volume"),
        (axes[1, 1], "weighted_inclusive_value", "Population-weighted inclusive value"),
    ]:
        ax.bar(x, [bundle["cases"][n]["summary"][metric] for n in names], color=[COLORS[n] for n in names])
        ax.set_title(title, fontsize=10)
    rigid = [bundle["cases"][n]["exit_probability"]["rigid"] for n in names]
    elastic = [bundle["cases"][n]["exit_probability"]["elastic"] for n in names]
    axes[0, 1].bar(x - 0.18, rigid, 0.36, label="Rigid", color="#72B7B2")
    axes[0, 1].bar(x + 0.18, elastic, 0.36, label="Elastic", color="#E45756")
    axes[0, 1].set_title("No-purchase probability", fontsize=10)
    axes[0, 1].legend(frameon=False, fontsize=8)
    for ax in axes.ravel():
        ax.set_xticks(x, [CASE_LABELS[n] for n in names], rotation=18, ha="right")
        ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIG / "mechanism_diagnostics.pdf")
    plt.close(fig)


def plot_profit_regret(bundle: dict[str, Any]) -> None:
    names = list(bundle["cases"])
    fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.6))
    bottom = np.zeros(len(names))
    parts = [("firm_A_profit", "#4C78A8"), ("firm_B_profit", "#72B7B2"), ("intermediary_profit", "#F58518")]
    for key, color in parts:
        vals = np.array([bundle["cases"][n]["summary"][key] for n in names])
        axes[0].bar(np.arange(len(names)), vals, bottom=bottom, label=key.replace("_", " "), color=color)
        bottom += vals
    axes[0].set_title("Profit by market participant", fontsize=10)
    axes[0].legend(frameon=False, fontsize=8)
    meta = bundle["metadata"]
    axes[1].bar([0, 1], [meta["dynamic_coarse_maxregret"], meta["dynamic_fine_maxregret"]],
                color=[COLORS["dynamic_coarse"], COLORS["dynamic_fine"]])
    axes[1].axhline(5.0, color="#666666", lw=1, ls="--", label="target < 5")
    axes[1].set_xticks([0, 1], ["Coarse\nround 22", "Fine\nround 40"])
    axes[1].set_title("Final stored max regret", fontsize=10)
    axes[1].legend(frameon=False, fontsize=8)
    axes[0].set_xticks(np.arange(len(names)), [CASE_LABELS[n] for n in names], rotation=18, ha="right")
    for ax in axes:
        ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
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
