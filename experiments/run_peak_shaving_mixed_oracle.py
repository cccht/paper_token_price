"""Mixed-strategy diagnostic for the congested peak-shaving fine grid."""
from __future__ import annotations

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
from experiments.peak_shaving_submission_tools import (
    best_response_regret,
    empirical_fictitious_play,
    fine_candidate_grid,
    nearest_candidate,
)
from pricing_sim.peak_shaving_config import PeakShavingConfig
from pricing_sim.peak_shaving_equilibrium import FirmParams, intermediary_best_response
from pricing_sim.peak_shaving_market import firm_profit, system_profit

SRC = ROOT / "artifacts" / "peak_shaving" / "20260618"
OUT = ROOT / "artifacts" / "peak_shaving" / "20260619_submission"
FIG = ROOT / "figures" / "peak_shaving_submission"
CAP = np.array([300.0, 120.0])
QOS_SHAPE = "sigmoid"
configure_times_new_roman()


def load_json(name: str) -> dict[str, Any]:
    return json.loads((SRC / name).read_text(encoding="utf-8"))


def cfg() -> PeakShavingConfig:
    return PeakShavingConfig.default().evolve(firm_capacity=CAP, pop_rigid=0.4, pop_elastic=0.6)


def idx_of(vec: np.ndarray, grid: np.ndarray) -> int:
    nearest = nearest_candidate(vec, grid)
    return int(np.argmin(np.linalg.norm(grid - nearest[None, :], axis=1)))


def initial_supports(grid: np.ndarray) -> tuple[list[int], list[int]]:
    fine = load_json("peak_shaving_fp_dynamic_converged_fine.json")
    coarse = load_json("peak_shaving_fp_dynamic_converged.json")
    base = [np.array([0.40, 0.0, 0.85, 0.0]), np.array([0.45, 0.0, 0.88, 0.0])]
    left = [idx_of(np.array(fine["firm_params"][0]), grid), idx_of(np.array(coarse["firm_params"][0]), grid), idx_of(base[0], grid)]
    right = [idx_of(np.array(fine["firm_params"][1]), grid), idx_of(np.array(coarse["firm_params"][1]), grid), idx_of(base[1], grid)]
    return sorted(set(left)), sorted(set(right))


def evaluate_pair(row_idx: int, col_idx: int, grid: np.ndarray, config: PeakShavingConfig, cache: dict) -> dict:
    key = (row_idx, col_idx)
    if key in cache:
        return cache[key]
    params = [FirmParams.from_vector(grid[row_idx]), FirmParams.from_vector(grid[col_idx])]
    wholesale = np.vstack([params[0].wholesale(config), params[1].wholesale(config)])
    direct = np.vstack([params[0].direct(config), params[1].direct(config)])
    state, res = intermediary_best_response(wholesale, direct, config, qos_shape=QOS_SHAPE)
    rec = {
        "firm_A_profit": firm_profit(0, state, res, config),
        "firm_B_profit": firm_profit(1, state, res, config),
        "system_profit": system_profit(state, res, config),
        "peak_utilization": float(res["utilization"].max()),
        "minimum_qos": float(res["qos_firm"].min()),
    }
    cache[key] = rec
    return rec


def payoff_matrix(rows: list[int], cols: list[int], grid: np.ndarray, config: PeakShavingConfig, cache: dict):
    a = np.zeros((len(rows), len(cols)))
    b = np.zeros_like(a)
    for i, row in enumerate(rows):
        for j, col in enumerate(cols):
            rec = evaluate_pair(row, col, grid, config, cache)
            a[i, j] = rec["firm_A_profit"]
            b[i, j] = rec["firm_B_profit"]
    return a, b


def best_response_to_mix(player: int, own_grid: np.ndarray, opp_support: list[int], opp_mix: np.ndarray,
                         grid: np.ndarray, config: PeakShavingConfig, cache: dict) -> tuple[int, float]:
    values = []
    for candidate in range(len(own_grid)):
        payoff = 0.0
        for weight, opp_idx in zip(opp_mix, opp_support):
            rec = evaluate_pair(candidate, opp_idx, grid, config, cache) if player == 0 else evaluate_pair(opp_idx, candidate, grid, config, cache)
            payoff += float(weight) * rec["firm_A_profit" if player == 0 else "firm_B_profit"]
        values.append(payoff)
    best_idx = int(np.argmax(values))
    return best_idx, float(values[best_idx])


def expected_metrics(rows: list[int], cols: list[int], row_mix: np.ndarray, col_mix: np.ndarray,
                     grid: np.ndarray, config: PeakShavingConfig, cache: dict) -> dict[str, float]:
    keys = ("firm_A_profit", "firm_B_profit", "system_profit", "peak_utilization", "minimum_qos")
    out = {k: 0.0 for k in keys}
    for i, row in enumerate(rows):
        for j, col in enumerate(cols):
            weight = float(row_mix[i] * col_mix[j])
            rec = evaluate_pair(row, col, grid, config, cache)
            for key in keys:
                out[key] += weight * rec[key]
    return out


def run_double_oracle(max_oracle_rounds: int = 8, fp_iterations: int = 2000) -> dict[str, Any]:
    grid = fine_candidate_grid()
    config = cfg()
    row_support, col_support = initial_supports(grid)
    cache: dict[tuple[int, int], dict] = {}
    trace = []
    for oracle_round in range(1, max_oracle_rounds + 1):
        payoff_a, payoff_b = payoff_matrix(row_support, col_support, grid, config, cache)
        row_mix, col_mix, fp_trace = empirical_fictitious_play(payoff_a, payoff_b, fp_iterations)
        in_row_reg, in_col_reg = best_response_regret(payoff_a, payoff_b, row_mix, col_mix)
        row_br, row_br_val = best_response_to_mix(0, grid, col_support, col_mix, grid, config, cache)
        col_br, col_br_val = best_response_to_mix(1, grid, row_support, row_mix, grid, config, cache)
        row_current = float(row_mix @ (payoff_a @ col_mix))
        col_current = float((row_mix @ payoff_b) @ col_mix)
        full_row_reg = max(row_br_val - row_current, 0.0)
        full_col_reg = max(col_br_val - col_current, 0.0)
        trace.append({"oracle_round": oracle_round, "row_support": len(row_support), "col_support": len(col_support),
                      "restricted_max_regret": max(in_row_reg, in_col_reg),
                      "full_max_regret": max(full_row_reg, full_col_reg), "evaluated_pairs": len(cache),
                      "fp_last_regret": fp_trace[-1]["max_regret"]})
        changed = False
        if row_br not in row_support:
            row_support.append(row_br); row_support.sort(); changed = True
        if col_br not in col_support:
            col_support.append(col_br); col_support.sort(); changed = True
        if not changed:
            break
    payoff_a, payoff_b = payoff_matrix(row_support, col_support, grid, config, cache)
    row_mix, col_mix, fp_trace = empirical_fictitious_play(payoff_a, payoff_b, fp_iterations)
    metrics = expected_metrics(row_support, col_support, row_mix, col_mix, grid, config, cache)
    return {"metadata": {"grid_size": len(grid), "qos_shape": QOS_SHAPE, "capacity": CAP.tolist(),
                         "fp_iterations": fp_iterations, "evaluated_pairs": len(cache)},
            "row_support_indices": row_support, "col_support_indices": col_support,
            "row_support_vectors": grid[row_support].tolist(), "col_support_vectors": grid[col_support].tolist(),
            "row_mix": row_mix.tolist(), "col_mix": col_mix.tolist(), "trace": trace,
            "fp_trace": fp_trace, "expected_metrics": metrics}


def plot_trace(result: dict[str, Any]) -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    xs = [r["oracle_round"] for r in result["trace"]]
    ys = [r["full_max_regret"] for r in result["trace"]]
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.plot(xs, ys, marker="o", color="#0072B2")
    ax.axhline(5.0, color="#666666", ls="--", lw=1, label="target < 5")
    ax.set_xlabel("Double-oracle round")
    ax.set_ylabel("Full-grid max regret")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.18))
    fig.tight_layout(rect=[0, 0, 1, 0.92])
    fig.savefig(FIG / "mixed_oracle_regret.pdf")
    plt.close(fig)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    result = run_double_oracle()
    (OUT / "peak_shaving_mixed_oracle.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    plot_trace(result)
    print(json.dumps({"output": str((OUT / "peak_shaving_mixed_oracle.json").relative_to(ROOT)),
                      "figure": str((FIG / "mixed_oracle_regret.pdf").relative_to(ROOT)),
                      "final_full_max_regret": result["trace"][-1]["full_max_regret"],
                      "evaluated_pairs": result["metadata"]["evaluated_pairs"]}, indent=2))
