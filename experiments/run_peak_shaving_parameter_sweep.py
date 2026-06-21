"""Parameter stress test for reported congested peak-shaving policies."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from experiments.plot_style import configure_times_new_roman
from experiments.peak_shaving_submission_tools import build_parameter_scenarios
from pricing_sim.peak_shaving_config import PeakShavingConfig
from pricing_sim.peak_shaving_equilibrium import FirmParams, intermediary_best_response
from pricing_sim.peak_shaving_market import choice_shares_with_exit, inclusive_value, system_profit

SRC = ROOT / "artifacts" / "peak_shaving" / "20260618"
OUT = ROOT / "artifacts" / "peak_shaving" / "20260619_submission"
FIG = ROOT / "figures" / "peak_shaving_submission"
CAP = np.array([300.0, 120.0])
QOS_SHAPE = "sigmoid"
CASE_LABELS = {"uniform": "Uniform", "dynamic_coarse": "Dynamic coarse", "dynamic_fine": "Dynamic fine"}
configure_times_new_roman()


def scenario_label(name: str) -> str:
    return (name.replace("capacity_scale_", "capacity\n")
                .replace("alpha_scale_", "alpha\n")
                .replace("switch_cost_scale_", "switch cost\n")
                .replace("qos_threshold_", "QoS threshold\n"))


def load_json(name: str) -> dict[str, Any]:
    return json.loads((SRC / name).read_text(encoding="utf-8"))


def congested_base() -> PeakShavingConfig:
    return PeakShavingConfig.default().evolve(firm_capacity=CAP, pop_rigid=0.4, pop_elastic=0.6)


def load_policy_vectors() -> dict[str, list[list[float]]]:
    congested = load_json("peak_shaving_congested_fp.json")
    coarse = load_json("peak_shaving_fp_dynamic_converged.json")
    fine = load_json("peak_shaving_fp_dynamic_converged_fine.json")
    return {"uniform": congested["uniform"]["firm_params"],
            "dynamic_coarse": coarse["firm_params"],
            "dynamic_fine": fine["firm_params"]}


def evaluate_policy(case: str, vectors: list[list[float]], cfg: PeakShavingConfig) -> dict[str, float]:
    if case == "uniform":
        cfg = cfg.evolve(load_shape_hat=np.zeros(cfg.num_periods))
    params = [FirmParams.from_vector(np.array(v, dtype=float)) for v in vectors]
    wholesale = np.vstack([params[0].wholesale(cfg), params[1].wholesale(cfg)])
    direct = np.vstack([params[0].direct(cfg), params[1].direct(cfg)])
    state, res = intermediary_best_response(wholesale, direct, cfg, qos_shape=QOS_SHAPE)
    prices = res["prices"]
    demand = res["demand"]
    qos = res["qos_channel"]
    served = demand * qos
    exit_rigid = choice_shares_with_exit(prices, qos, cfg, "rigid")[1]
    exit_elastic = choice_shares_with_exit(prices, qos, cfg, "elastic")[1]
    avg_price = float(np.sum(prices * demand) / max(np.sum(demand), 1e-12))
    weighted_iv = (cfg.pop_rigid * inclusive_value(prices, qos, cfg, "rigid")
                   + cfg.pop_elastic * inclusive_value(prices, qos, cfg, "elastic"))
    return {"system_profit": system_profit(state, res, cfg),
            "peak_utilization": float(res["utilization"].max()),
            "minimum_qos": float(res["qos_firm"].min()),
            "served_volume": float(np.sum(served) * cfg.period_hours),
            "average_paid_price": avg_price,
            "exit_probability_rigid": exit_rigid,
            "exit_probability_elastic": exit_elastic,
            "weighted_inclusive_value": weighted_iv}


def run_sweep() -> list[dict[str, Any]]:
    policies = load_policy_vectors()
    rows = []
    for scenario in build_parameter_scenarios(congested_base()):
        values = {case: evaluate_policy(case, vecs, scenario.config) for case, vecs in policies.items()}
        base = values["uniform"]
        for case, metrics in values.items():
            row = {"scenario": scenario.name, "group": scenario.group, "value": scenario.value, "case": case}
            row.update(metrics)
            row["qos_gain_vs_uniform"] = metrics["minimum_qos"] - base["minimum_qos"]
            row["peak_util_reduction_vs_uniform"] = base["peak_utilization"] - metrics["peak_utilization"]
            row["served_gain_vs_uniform"] = metrics["served_volume"] - base["served_volume"]
            row["profit_gain_pct_vs_uniform"] = 100.0 * (metrics["system_profit"] - base["system_profit"]) / abs(base["system_profit"])
            rows.append(row)
    return rows


def write_outputs(rows: list[dict[str, Any]]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "peak_shaving_parameter_sweep.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    with (OUT / "peak_shaving_parameter_sweep.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def plot_sweep(rows: list[dict[str, Any]]) -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    scenarios = [r["scenario"] for r in rows if r["case"] == "uniform"]
    fig, axes = plt.subplots(2, 1, figsize=(9.2, 6.4), sharex=True)
    x = np.arange(len(scenarios))
    width = 0.36
    for offset, case, color in [(-width / 2, "dynamic_coarse", "#E6A400"), (width / 2, "dynamic_fine", "#5B9BD5")]:
        subset = [r for r in rows if r["case"] == case]
        axes[0].bar(x + offset, [r["qos_gain_vs_uniform"] for r in subset], width, label=CASE_LABELS[case], color=color)
        axes[1].bar(x + offset, [r["peak_util_reduction_vs_uniform"] for r in subset], width, label=CASE_LABELS[case], color=color)
    axes[0].axhline(0.0, color="#666666", lw=1)
    axes[1].axhline(0.0, color="#666666", lw=1)
    axes[0].set_ylabel("Minimum QoS gain")
    axes[1].set_ylabel("Peak-utilization reduction")
    axes[1].set_xticks(x, [scenario_label(s) for s in scenarios], rotation=0, ha="center", fontsize=8)
    for ax in axes:
        ax.grid(axis="y", alpha=0.25)
    handles, labels = axes[0].get_legend_handles_labels()
    axes[0].legend(handles, labels, frameon=False, ncol=2, loc="upper right",
                   fontsize=8, borderaxespad=0.25, handlelength=1.4,
                   columnspacing=0.9)
    fig.tight_layout()
    fig.savefig(FIG / "parameter_sweep_qos.pdf")
    plt.close(fig)


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    out = {}
    for case in ("dynamic_coarse", "dynamic_fine"):
        subset = [r for r in rows if r["case"] == case]
        out[case] = {"scenarios": len(subset),
                     "qos_gain_positive": sum(r["qos_gain_vs_uniform"] > 0 for r in subset),
                     "peak_reduction_positive": sum(r["peak_util_reduction_vs_uniform"] > 0 for r in subset),
                     "profit_gain_positive": sum(r["profit_gain_pct_vs_uniform"] > 0 for r in subset),
                     "min_qos_gain": min(r["qos_gain_vs_uniform"] for r in subset),
                     "min_peak_reduction": min(r["peak_util_reduction_vs_uniform"] for r in subset)}
    return out


if __name__ == "__main__":
    rows = run_sweep()
    write_outputs(rows)
    plot_sweep(rows)
    summary = summarize(rows)
    (OUT / "peak_shaving_parameter_sweep_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"rows": len(rows), "summary": summary,
                      "csv": str((OUT / "peak_shaving_parameter_sweep.csv").relative_to(ROOT)),
                      "figure": str((FIG / "parameter_sweep_qos.pdf").relative_to(ROOT))}, ensure_ascii=False, indent=2))
