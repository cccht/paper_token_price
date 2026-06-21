"""Run SMPT-oriented diagnostics for the peak-shaving manuscript."""
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
from experiments.peak_shaving_smpt_tools import (
    FIG,
    OUT,
    admission_control_record,
    build_phase_grid,
    congested_base,
    evaluate_equal_routing,
    evaluate_params,
    make_baseline_param_sets,
    record_from_state,
    summarize_records,
    trace_fixed_point_residuals,
)
from pricing_sim.peak_shaving_config import PeakShavingConfig
from pricing_sim.peak_shaving_equilibrium import FirmParams, intermediary_best_response
from pricing_sim.peak_shaving_market import firm_profit

configure_times_new_roman()

def serialise(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, dict):
        return {k: serialise(v) for k, v in value.items() if k not in {"prices", "routing", "utilization", "qos_firm"}}
    if isinstance(value, list):
        return [serialise(v) for v in value]
    if isinstance(value, (np.floating, np.integer)):
        return value.item()
    return value


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def run_baselines() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    cfg = congested_base()
    param_sets = make_baseline_param_sets()
    records = []
    for name, params in param_sets.items():
        records.append(evaluate_params(name, params, cfg, static_shape=name == "optimal_static_qos_routing"))
    records.append(evaluate_equal_routing("dynamic_coarse_equal_routing", param_sets["dynamic_coarse"], cfg))
    dynamic_peak = next(r["peak_utilization"] for r in records if r["case"] == "dynamic_coarse")
    records.append(admission_control_record(records[0], dynamic_peak))
    comparable = [r for r in records if "system_profit" in r]
    return records, summarize_records(comparable, "optimal_static_qos_routing")


def run_ablations() -> list[dict[str, Any]]:
    base = congested_base()
    policies = make_baseline_param_sets()
    variants = {
        "baseline": base,
        "no_outside_option": base.evolve(outside_utility=-20.0),
        "suppressed_direct_channel": base.evolve(firm_brand=np.array([1e-6, 1e-6])),
        "homogeneous_capacity": base.evolve(firm_capacity=np.array([210.0, 210.0])),
        "no_time_flexible_users": base.evolve(pop_rigid=1.0, pop_elastic=0.0),
    }
    rows = []
    for variant, cfg in variants.items():
        uniform = evaluate_params("uniform", policies["optimal_static_qos_routing"], cfg, static_shape=True)
        dynamic = evaluate_params("dynamic_coarse", policies["dynamic_coarse"], cfg)
        rows.append({
            "variant": variant,
            "uniform_min_qos": uniform["minimum_qos"],
            "dynamic_min_qos": dynamic["minimum_qos"],
            "qos_gain": dynamic["minimum_qos"] - uniform["minimum_qos"],
            "peak_reduction": uniform["peak_utilization"] - dynamic["peak_utilization"],
            "profit_gain_pct": 100.0 * (dynamic["system_profit"] - uniform["system_profit"]) / abs(uniform["system_profit"]),
        })
    equal = evaluate_equal_routing("dynamic_equal_routing", policies["dynamic_coarse"], base)
    uniform = evaluate_params("uniform", policies["optimal_static_qos_routing"], base, static_shape=True)
    rows.append({
        "variant": "fixed_equal_routing",
        "uniform_min_qos": uniform["minimum_qos"],
        "dynamic_min_qos": equal["minimum_qos"],
        "qos_gain": equal["minimum_qos"] - uniform["minimum_qos"],
        "peak_reduction": uniform["peak_utilization"] - equal["peak_utilization"],
        "profit_gain_pct": 100.0 * (equal["system_profit"] - uniform["system_profit"]) / abs(uniform["system_profit"]),
    })
    return rows


def run_phase_grid() -> list[dict[str, Any]]:
    rows = []
    policies = make_baseline_param_sets()
    for point in build_phase_grid([0.8, 0.9, 1.0, 1.1, 1.2], [0.7, 0.85, 1.0, 1.15, 1.3]):
        cfg = congested_base().evolve(
            firm_capacity=congested_base().firm_capacity * point["capacity_scale"],
            alpha_rigid=congested_base().alpha_rigid * point["alpha_scale"],
            alpha_elastic=congested_base().alpha_elastic * point["alpha_scale"],
        )
        uniform = evaluate_params("uniform", policies["optimal_static_qos_routing"], cfg, static_shape=True)
        dynamic = evaluate_params("dynamic_coarse", policies["dynamic_coarse"], cfg)
        rows.append({
            **point,
            "qos_gain": dynamic["minimum_qos"] - uniform["minimum_qos"],
            "peak_reduction": uniform["peak_utilization"] - dynamic["peak_utilization"],
            "profit_gain_pct": 100.0 * (dynamic["system_profit"] - uniform["system_profit"]) / abs(uniform["system_profit"]),
        })
    return rows


def local_candidate_sets() -> tuple[list[FirmParams], list[FirmParams]]:
    param_sets = make_baseline_param_sets()
    left, right = [], []
    for params in param_sets.values():
        left.append(params[0])
        right.append(params[1])
    def unique(values: list[FirmParams]) -> list[FirmParams]:
        seen = set()
        out = []
        for item in values:
            key = tuple(np.round(item.to_vector(), 6))
            if key not in seen:
                seen.add(key)
                out.append(item)
        return out
    return unique(left), unique(right)


def evaluate_pair(params: list[FirmParams], cfg: PeakShavingConfig):
    wholesale = np.vstack([params[0].wholesale(cfg), params[1].wholesale(cfg)])
    direct = np.vstack([params[0].direct(cfg), params[1].direct(cfg)])
    return intermediary_best_response(wholesale, direct, cfg, qos_shape="sigmoid")


def restricted_local_re_solve(cfg: PeakShavingConfig, rounds: int = 4) -> tuple[list[FirmParams], dict[str, Any]]:
    left_candidates, right_candidates = local_candidate_sets()
    current = [left_candidates[0], right_candidates[0]]
    trace = []
    for rnd in range(1, rounds + 1):
        best_left, best_left_profit = current[0], -np.inf
        for cand in left_candidates:
            state, res = evaluate_pair([cand, current[1]], cfg)
            value = firm_profit(0, state, res, cfg)
            if value > best_left_profit:
                best_left, best_left_profit = cand, value
        current[0] = best_left
        best_right, best_right_profit = current[1], -np.inf
        for cand in right_candidates:
            state, res = evaluate_pair([current[0], cand], cfg)
            value = firm_profit(1, state, res, cfg)
            if value > best_right_profit:
                best_right, best_right_profit = cand, value
        current[1] = best_right
        trace.append({
            "round": rnd,
            "left_profit": float(best_left_profit),
            "right_profit": float(best_right_profit),
            "left_params": current[0].to_vector().tolist(),
            "right_params": current[1].to_vector().tolist(),
        })
    state, res = evaluate_pair(current, cfg)
    return current, {"trace": trace, "state": state, "res": res}


def run_resolved_sensitivity() -> list[dict[str, Any]]:
    base = congested_base()
    cases = {
        "capacity_0.90": base.evolve(firm_capacity=base.firm_capacity * 0.9),
        "alpha_1.15": base.evolve(alpha_rigid=base.alpha_rigid * 1.15, alpha_elastic=base.alpha_elastic * 1.15),
        "flexible_share_0.70": base.evolve(pop_rigid=0.3, pop_elastic=0.7),
        "qos_threshold_0.78": base.evolve(qos_threshold=0.78),
        "outside_utility_0.50": base.evolve(outside_utility=0.5),
    }
    rows = []
    for name, cfg in cases.items():
        uniform = evaluate_params("uniform", make_baseline_param_sets()["optimal_static_qos_routing"], cfg, static_shape=True)
        params, solved = restricted_local_re_solve(cfg)
        dynamic = record_from_state("restricted_re_solved", solved["state"], solved["res"], cfg)
        rows.append({
            "scenario": name,
            "uniform_profit": uniform["system_profit"],
            "dynamic_profit": dynamic["system_profit"],
            "profit_gain_pct": 100.0 * (dynamic["system_profit"] - uniform["system_profit"]) / abs(uniform["system_profit"]),
            "uniform_min_qos": uniform["minimum_qos"],
            "dynamic_min_qos": dynamic["minimum_qos"],
            "qos_gain": dynamic["minimum_qos"] - uniform["minimum_qos"],
            "peak_reduction": uniform["peak_utilization"] - dynamic["peak_utilization"],
            "restricted_rounds": len(solved["trace"]),
            "restricted_candidates_per_firm": len(local_candidate_sets()[0]),
            "left_params": params[0].to_vector().tolist(),
            "right_params": params[1].to_vector().tolist(),
        })
    return rows


def run_residuals() -> list[dict[str, Any]]:
    cfg = congested_base()
    records = []
    for name, params in make_baseline_param_sets().items():
        rec = evaluate_params(name, params, cfg, static_shape=name == "optimal_static_qos_routing")
        trace = trace_fixed_point_residuals(rec["prices"], rec["routing"], cfg)
        records.append({"case": name, **{k: v for k, v in trace.items() if k != "residuals"}})
    return records


def plot_baselines(rows: list[dict[str, Any]]) -> None:
    comparable = [r for r in rows if "system_profit" in r]
    label_map = {
        "optimal_static_qos_routing": "Static\nQoS routing",
        "offpeak_discount_only": "Off-peak\ndiscount",
        "peak_surcharge_only": "Peak\nsurcharge",
        "dynamic_coarse": "Dynamic\ncoarse",
        "dynamic_fine": "Dynamic\nfine",
        "dynamic_coarse_equal_routing": "Equal-routing\ndynamic",
    }
    labels = [label_map.get(r["case"], r["case"].replace("_", "\n")) for r in comparable]
    x = np.arange(len(labels))
    fig, axes = plt.subplots(1, 3, figsize=(9.6, 3.4))
    metrics = [("minimum_qos", "Minimum QoS"), ("peak_utilization", "Peak utilization"), ("system_profit", "System profit")]
    colors = ["#3C5488", "#00A087", "#E64B35"]
    for ax, (key, title), color in zip(axes, metrics, colors):
        ax.bar(x, [r[key] for r in comparable], color=color)
        ax.set_title(title)
        ax.set_xticks(x, labels, rotation=0, ha="center", fontsize=7)
        ax.grid(axis="y", alpha=0.2)
    fig.tight_layout(pad=1.1)
    fig.savefig(FIG / "smpt_baseline_comparison.pdf")
    plt.close(fig)


def plot_phase(rows: list[dict[str, Any]]) -> None:
    caps = sorted({r["capacity_scale"] for r in rows})
    alphas = sorted({r["alpha_scale"] for r in rows})
    for key, title, filename in [
        ("qos_gain", "QoS gain", "smpt_phase_qos_gain.pdf"),
        ("profit_gain_pct", "Profit gain (%)", "smpt_phase_profit_gain.pdf"),
    ]:
        matrix = np.array([[next(r[key] for r in rows if r["capacity_scale"] == c and r["alpha_scale"] == a) for a in alphas] for c in caps])
        fig, ax = plt.subplots(figsize=(4.9, 3.8))
        im = ax.imshow(matrix, cmap="viridis", aspect="auto", origin="lower")
        ax.set_xticks(range(len(alphas)), [f"{a:.2g}" for a in alphas])
        ax.set_yticks(range(len(caps)), [f"{c:.2g}" for c in caps])
        ax.set_xlabel("Price-sensitivity scale")
        ax.set_ylabel("Capacity scale")
        ax.set_title(title)
        midpoint = (float(np.nanmin(matrix)) + float(np.nanmax(matrix))) / 2.0
        for i in range(len(caps)):
            for j in range(len(alphas)):
                color = "white" if matrix[i, j] < midpoint else "black"
                ax.text(j, i, f"{matrix[i, j]:.2f}", ha="center", va="center", fontsize=6.8, color=color)
        fig.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
        fig.tight_layout()
        fig.savefig(FIG / filename)
        plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    baselines, baseline_summary = run_baselines()
    ablations = run_ablations()
    phase = run_phase_grid()
    residuals = run_residuals()
    resolved = run_resolved_sensitivity()
    bundle = {
        "metadata": {"note": "SMPT-oriented diagnostics; budgeted re-solve rows are not equilibrium proofs."},
        "baselines": serialise(baselines),
        "baseline_summary": baseline_summary,
        "ablations": ablations,
        "phase_grid": phase,
        "fixed_point_residuals": residuals,
        "resolved_sensitivity": resolved,
        "resolved_sensitivity_boundary": "Restricted local candidate re-solve over static, dynamic, off-peak-only, and peak-only candidate families.",
    }
    (OUT / "peak_shaving_smpt_experiments.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(OUT / "smpt_baselines.csv", serialise(baselines))
    write_csv(OUT / "smpt_ablations.csv", ablations)
    write_csv(OUT / "smpt_phase_grid.csv", phase)
    write_csv(OUT / "smpt_fixed_point_residuals.csv", residuals)
    write_csv(OUT / "smpt_resolved_sensitivity.csv", resolved)
    plot_baselines(baselines)
    plot_phase(phase)
    print(json.dumps({
        "bundle": str((OUT / "peak_shaving_smpt_experiments.json").relative_to(ROOT)),
        "baseline_rows": len(baselines),
        "ablation_rows": len(ablations),
        "phase_rows": len(phase),
        "resolved_rows": len(resolved),
        "figures": [
            str((FIG / "smpt_baseline_comparison.pdf").relative_to(ROOT)),
            str((FIG / "smpt_phase_qos_gain.pdf").relative_to(ROOT)),
            str((FIG / "smpt_phase_profit_gain.pdf").relative_to(ROOT)),
        ],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
