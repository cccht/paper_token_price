from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from pricing_sim.peak_shaving_config import PeakShavingConfig


@dataclass(frozen=True)
class ParameterScenario:
    name: str
    group: str
    value: float
    config: PeakShavingConfig


def fine_candidate_grid() -> np.ndarray:
    wb = np.linspace(0.27, 0.88, 3)
    delta = np.linspace(-0.4, 0.4, 5)
    pd = np.linspace(0.60, 1.60, 3)
    delta_d = np.linspace(-0.4, 0.4, 5)
    return np.array([(a, b, c, d) for a in wb for b in delta for c in pd for d in delta_d], dtype=float)


def nearest_candidate(target: np.ndarray, grid: np.ndarray) -> np.ndarray:
    target = np.asarray(target, dtype=float)
    distances = np.linalg.norm(grid - target[None, :], axis=1)
    return grid[int(np.argmin(distances))].copy()


def best_response_regret(
    payoff_row: np.ndarray,
    payoff_col: np.ndarray,
    row_mix: np.ndarray,
    col_mix: np.ndarray,
) -> tuple[float, float]:
    row_values = payoff_row @ col_mix
    col_values = row_mix @ payoff_col
    row_regret = float(np.max(row_values) - row_mix @ row_values)
    col_regret = float(np.max(col_values) - col_values @ col_mix)
    return max(row_regret, 0.0), max(col_regret, 0.0)


def empirical_fictitious_play(
    payoff_row: np.ndarray,
    payoff_col: np.ndarray,
    iterations: int = 1000,
) -> tuple[np.ndarray, np.ndarray, list[dict[str, float]]]:
    n_rows, n_cols = payoff_row.shape
    row_counts = np.ones(n_rows, dtype=float)
    col_counts = np.ones(n_cols, dtype=float)
    trace: list[dict[str, float]] = []
    for step in range(1, iterations + 1):
        row_mix = row_counts / row_counts.sum()
        col_mix = col_counts / col_counts.sum()
        row_br = int(np.argmax(payoff_row @ col_mix))
        col_br = int(np.argmax(row_mix @ payoff_col))
        row_counts[row_br] += 1.0
        col_counts[col_br] += 1.0
        if step == 1 or step == iterations or step % max(iterations // 10, 1) == 0:
            row_mix = row_counts / row_counts.sum()
            col_mix = col_counts / col_counts.sum()
            row_reg, col_reg = best_response_regret(payoff_row, payoff_col, row_mix, col_mix)
            trace.append({"iteration": float(step), "max_regret": max(row_reg, col_reg)})
    return row_counts / row_counts.sum(), col_counts / col_counts.sum(), trace


def build_parameter_scenarios(base: PeakShavingConfig) -> list[ParameterScenario]:
    scenarios = [ParameterScenario("baseline", "baseline", 1.0, base)]
    for scale in (0.85, 1.15):
        scenarios.append(ParameterScenario(f"capacity_scale_{scale:.2f}", "capacity_scale", scale,
                                           base.evolve(firm_capacity=base.firm_capacity * scale)))
    for scale in (0.80, 1.20):
        scenarios.append(ParameterScenario(f"alpha_scale_{scale:.2f}", "alpha_scale", scale,
                                           base.evolve(alpha_rigid=base.alpha_rigid * scale,
                                                       alpha_elastic=base.alpha_elastic * scale)))
    for scale in (0.70, 1.30):
        scenarios.append(ParameterScenario(f"switch_cost_scale_{scale:.2f}", "switch_cost_scale", scale,
                                           base.evolve(switch_cost_rigid=base.switch_cost_rigid * scale,
                                                       switch_cost_elastic=base.switch_cost_elastic * scale)))
    for threshold in (0.78, 0.86):
        scenarios.append(ParameterScenario(f"qos_threshold_{threshold:.2f}", "qos_threshold", threshold,
                                           base.evolve(qos_threshold=threshold)))
    return scenarios
