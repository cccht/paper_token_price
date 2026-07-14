from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from pricing_sim.peak_shaving_config import PeakShavingConfig

FOURTH_AUDIT_CENTRES = (
    (0.25, 0.25, 0.5278125, 0.2),
    (0.25, 1.05, 0.5278125, 0.4),
)


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


def expanded_provider_candidate_grid() -> np.ndarray:
    """Provider price-shape grid with exact lower bounds and slope guards."""
    wholesale_base = np.array([0.25, 0.575, 0.90])
    slopes = np.array([-0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8])
    direct_base = np.array([0.45, 0.60, 1.10, 1.60])
    return np.array([
        (wbar, wslope, direct, dslope)
        for wbar in wholesale_base
        for wslope in slopes
        for direct in direct_base
        for dslope in slopes
    ], dtype=float)


def guard_enriched_provider_candidate_grid() -> np.ndarray:
    """Add high-slope guard layers near the active low-price region."""
    base = expanded_provider_candidate_grid()
    wholesale_guard = np.array([
        (0.25, wslope, direct, dslope)
        for wslope in (1.0, 1.2, 1.5, 2.0, 3.0)
        for direct in (0.45, 0.60)
        for dslope in (0.0, 0.2, 0.4, 0.6, 0.8, 1.2)
    ])
    direct_guard = np.array([
        (0.25, wslope, direct, dslope)
        for wslope in (0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5)
        for direct in (0.45, 0.60)
        for dslope in (1.0, 1.2, 1.5, 2.0, 3.0)
    ])
    return np.unique(np.vstack([base, wholesale_guard, direct_guard]), axis=0)


def audit_enriched_provider_candidate_grid() -> np.ndarray:
    """Add deterministic local layers around audited profitable deviations."""
    base = guard_enriched_provider_candidate_grid()
    provider_a_region = np.array([
        (wbar, wslope, direct, dslope)
        for wbar in (0.25, 0.26625, 0.2825, 0.29875, 0.315)
        for wslope in (0.8, 0.9, 1.0, 1.1, 1.2)
        for direct in (0.55875, 0.579375, 0.60, 0.620625)
        for dslope in (0.2, 0.3, 0.4)
    ])
    provider_b_region = np.array([
        (wbar, wslope, direct, dslope)
        for wbar in (0.25, 0.26625, 0.2825)
        for wslope in (0.0, 0.2, 0.4, 0.6)
        for direct in (0.538125, 0.55875, 0.579375, 0.60)
        for dslope in (0.3, 0.4, 0.5, 0.6)
    ])
    return np.unique(
        np.vstack([base, provider_a_region, provider_b_region]), axis=0
    )


def second_audit_enriched_provider_candidate_grid() -> np.ndarray:
    """Add interaction layers identified by the second off-grid audit."""
    base = audit_enriched_provider_candidate_grid()
    low_slope_region = np.array([
        (wbar, wslope, direct, dslope)
        for wbar in (0.25, 0.258125, 0.26625)
        for wslope in (0.0, 0.05, 0.1, 0.15, 0.2, 0.3)
        for direct in (
            0.4865625, 0.496875, 0.5071875, 0.5175,
            0.5278125, 0.538125, 0.5484375, 0.55875,
        )
        for dslope in (0.1, 0.2, 0.3, 0.4)
    ])
    high_slope_region = np.array([
        (wbar, wslope, direct, dslope)
        for wbar in (0.25, 0.258125, 0.26625, 0.274375, 0.2825)
        for wslope in (1.3, 1.4, 1.5, 1.6, 1.7, 1.8)
        for direct in (0.538125, 0.55875, 0.579375)
        for dslope in (0.1, 0.2, 0.3, 0.4, 0.5)
    ])
    return np.unique(
        np.vstack([base, low_slope_region, high_slope_region]), axis=0
    )


def third_audit_enriched_provider_candidate_grid() -> np.ndarray:
    """Add the mid-slope interaction region found by the third off-grid audit."""
    base = second_audit_enriched_provider_candidate_grid()
    mid_slope_region = np.array([
        (wbar, wslope, direct, dslope)
        for wbar in (0.25, 0.258125)
        for wslope in (
            0.35, 0.40, 0.45, 0.50, 0.55, 0.60,
            0.65, 0.70, 0.75, 0.80, 0.85,
        )
        for direct in (
            0.496875, 0.5071875, 0.5175, 0.5278125, 0.538125,
            0.5484375, 0.55875, 0.5690625, 0.579375,
        )
        for dslope in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7)
    ])
    upper_wbar_guard = np.array([
        (0.26625, wslope, direct, dslope)
        for wslope in (0.40, 0.50, 0.60, 0.70, 0.80, 0.85)
        for direct in (0.5175, 0.538125, 0.55875, 0.579375)
        for dslope in (0.1, 0.3, 0.5, 0.7)
    ])
    return np.unique(
        np.vstack([base, mid_slope_region, upper_wbar_guard]), axis=0
    )


def adaptive_audit_provider_candidate_grid(
    reference_vectors: np.ndarray,
) -> np.ndarray:
    """Build a compact candidate set around audited deviations and prior support."""
    reference = np.asarray(reference_vectors, dtype=float)
    if reference.ndim != 2 or reference.shape[1] != 4 or not len(reference):
        raise ValueError("reference_vectors must be a nonempty N-by-4 array")
    base = second_audit_enriched_provider_candidate_grid()
    uniform = base[np.isclose(base[:, 1], 0.0) & np.isclose(base[:, 3], 0.0)]
    mid = np.array([
        (0.25, wslope, direct, dslope)
        for wslope in (0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80)
        for direct in (
            0.5071875, 0.5175, 0.5278125, 0.538125,
            0.5484375, 0.55875, 0.5690625,
        )
        for dslope in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6)
    ])
    wbar_guard = np.array([
        (wbar, wslope, direct, dslope)
        for wbar in (0.258125, 0.26625)
        for wslope in (0.45, 0.55, 0.65, 0.75, 0.85)
        for direct in (0.5175, 0.538125, 0.55875, 0.579375)
        for dslope in (0.2, 0.4, 0.6)
    ])
    low = np.array([
        (0.25, wslope, direct, dslope)
        for wslope in (0.0, 0.1, 0.2, 0.3)
        for direct in (0.496875, 0.5175, 0.538125, 0.55875)
        for dslope in (0.1, 0.2, 0.3, 0.4)
    ])
    high = np.array([
        (0.25, wslope, direct, dslope)
        for wslope in (1.3, 1.5, 1.7)
        for direct in (0.538125, 0.55875, 0.579375)
        for dslope in (0.1, 0.3, 0.5)
    ])
    guards = np.array([
        (0.25, wslope, direct, dslope)
        for wslope in (0.6, 1.0, 1.5, 2.0, 3.0)
        for direct in (0.45, 0.60)
        for dslope in (0.0, 0.4, 0.8, 1.2, 2.0, 3.0)
    ] + [
        (0.25, wslope, direct, dslope)
        for wslope in (0.0, 0.4, 0.8, 1.2, 2.0, 3.0)
        for direct in (0.45, 0.60)
        for dslope in (1.0, 1.5, 2.0, 3.0)
    ])
    audited_local_regions = np.array([
        (0.25, wslope, direct, dslope)
        for wslope in (0.20, 0.25, 0.30)
        for direct in (0.5175, 0.5278125, 0.538125)
        for dslope in (0.1, 0.2, 0.3)
    ] + [
        (wbar, wslope, direct, dslope)
        for wbar in (0.25, 0.258125)
        for wslope in (0.95, 1.05, 1.15)
        for direct in (0.5175, 0.5278125, 0.538125)
        for dslope in (0.3, 0.4, 0.5)
    ])
    return np.unique(
        np.vstack([
            uniform, reference, mid, wbar_guard, low, high, guards,
            audited_local_regions,
        ]),
        axis=0,
    )


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
