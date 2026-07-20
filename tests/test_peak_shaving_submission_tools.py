from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from experiments.peak_shaving_submission_tools import (
    adaptive_audit_provider_candidate_grid,
    audit_enriched_provider_candidate_grid,
    best_response_regret,
    build_parameter_scenarios,
    empirical_fictitious_play,
    expanded_provider_candidate_grid,
    fine_candidate_grid,
    guard_enriched_provider_candidate_grid,
    nearest_candidate,
    second_audit_enriched_provider_candidate_grid,
    third_audit_enriched_provider_candidate_grid,
)
from pricing_sim.peak_shaving_config import PeakShavingConfig


def test_fine_candidate_grid_matches_documented_size():
    grid = fine_candidate_grid()
    assert grid.shape == (225, 4)
    assert np.allclose(grid[0], [0.27, -0.4, 0.60, -0.4])
    assert np.allclose(grid[-1], [0.88, 0.4, 1.60, 0.4])


def test_expanded_provider_grid_includes_price_bounds_and_slope_guards():
    grid = expanded_provider_candidate_grid()

    assert grid.shape == (768, 4)
    assert len(np.unique(grid, axis=0)) == 768
    assert np.allclose(grid[0], [0.25, -0.6, 0.45, -0.6])
    assert np.allclose(grid[-1], [0.90, 0.8, 1.60, 0.8])
    assert any(np.allclose(row, [0.25, 0.0, 0.60, 0.0]) for row in grid)
    assert any(np.allclose(row, [0.25, 0.6, 0.60, 0.2]) for row in grid)


def test_guard_enriched_grid_adds_interior_high_slope_candidates():
    grid = guard_enriched_provider_candidate_grid()

    assert grid.shape == (892, 4)
    assert len(np.unique(grid, axis=0)) == 892
    assert any(np.allclose(row, [0.25, 1.5, 0.60, 0.4]) for row in grid)
    assert any(np.allclose(row, [0.25, 3.0, 0.60, 1.2]) for row in grid)
    assert any(np.allclose(row, [0.25, 1.2, 0.60, 3.0]) for row in grid)


def test_audit_enriched_grid_adds_both_offgrid_deviation_regions():
    guard = guard_enriched_provider_candidate_grid()
    grid = audit_enriched_provider_candidate_grid()
    keys = {tuple(np.round(row, 12)) for row in grid}

    assert 1200 < len(grid) < 1500
    assert len(np.unique(grid, axis=0)) == len(grid)
    assert all(tuple(np.round(old, 12)) in keys for old in guard)
    assert any(np.allclose(row, [0.2825, 1.0, 0.579375, 0.4]) for row in grid)
    assert any(np.allclose(row, [0.25, 0.4, 0.55875, 0.4]) for row in grid)
    assert any(np.allclose(row, [0.315, 1.2, 0.620625, 0.3]) for row in grid)
    assert any(np.allclose(row, [0.2825, 0.0, 0.538125, 0.6]) for row in grid)


def test_second_audit_grid_covers_low_and_high_slope_interaction_regions():
    previous = audit_enriched_provider_candidate_grid()
    grid = second_audit_enriched_provider_candidate_grid()
    keys = {tuple(np.round(row, 12)) for row in grid}

    assert 2000 < len(grid) < 2600
    assert len(np.unique(grid, axis=0)) == len(grid)
    assert all(tuple(np.round(old, 12)) in keys for old in previous)
    assert any(np.allclose(row, [0.25, 0.1, 0.5175, 0.3]) for row in grid)
    assert any(np.allclose(row, [0.25, 0.05, 0.496875, 0.1]) for row in grid)
    assert any(np.allclose(row, [0.26625, 1.5, 0.55875, 0.2]) for row in grid)
    assert any(np.allclose(row, [0.2825, 1.8, 0.579375, 0.5]) for row in grid)


def test_third_audit_grid_covers_mid_slope_interaction_region():
    previous = second_audit_enriched_provider_candidate_grid()
    grid = third_audit_enriched_provider_candidate_grid()
    keys = {tuple(np.round(row, 12)) for row in grid}

    assert 3500 < len(grid) < 4500
    assert len(np.unique(grid, axis=0)) == len(grid)
    assert all(tuple(np.round(old, 12)) in keys for old in previous)
    assert any(np.allclose(row, [0.25, 0.55, 0.538125, 0.2]) for row in grid)
    assert any(np.allclose(row, [0.25, 0.70, 0.538125, 0.4]) for row in grid)
    assert any(np.allclose(row, [0.258125, 0.45, 0.5071875, 0.0]) for row in grid)
    assert any(np.allclose(row, [0.26625, 0.85, 0.579375, 0.7]) for row in grid)


def test_adaptive_audit_grid_keeps_reference_support_and_audit_guards():
    reference = np.array([
        [0.25, 0.55, 0.538125, 0.2],
        [0.575, -0.2, 1.10, 0.4],
    ])
    grid = adaptive_audit_provider_candidate_grid(reference)

    assert 750 < len(grid) < 850
    assert len(np.unique(grid, axis=0)) == len(grid)
    assert all(any(np.allclose(row, old) for row in grid) for old in reference)
    assert any(np.allclose(row, [0.25, 0.70, 0.538125, 0.4]) for row in grid)
    assert any(np.allclose(row, [0.25, 0.10, 0.5175, 0.3]) for row in grid)
    assert any(np.allclose(row, [0.25, 1.50, 0.55875, 0.3]) for row in grid)
    assert any(np.allclose(row, [0.25, 3.00, 0.60, 1.2]) for row in grid)


def test_adaptive_audit_grid_covers_fourth_audit_deviation_neighbourhoods():
    reference = np.array([
        [0.25, 0.55, 0.538125, 0.2],
        [0.575, -0.2, 1.10, 0.4],
    ])
    grid = adaptive_audit_provider_candidate_grid(reference)

    expected = np.array([
        [0.25, 0.25, 0.5278125, 0.2],
        [0.25, 0.30, 0.5175, 0.3],
        [0.25, 1.05, 0.5278125, 0.4],
        [0.258125, 1.15, 0.538125, 0.5],
    ])
    assert all(any(np.allclose(row, target) for row in grid) for target in expected)


def test_nearest_candidate_returns_grid_member():
    grid = fine_candidate_grid()
    target = np.array([0.579, 0.278, 0.607, 0.205])
    nearest = nearest_candidate(target, grid)
    assert nearest.shape == (4,)
    assert any(np.allclose(nearest, row) for row in grid)
    assert np.allclose(nearest, [0.575, 0.2, 0.60, 0.2])


def test_empirical_fictitious_play_solves_matching_pennies():
    payoff_row = np.array([[1.0, -1.0], [-1.0, 1.0]])
    payoff_col = -payoff_row
    row_mix, col_mix, trace = empirical_fictitious_play(payoff_row, payoff_col, iterations=400)
    row_reg, col_reg = best_response_regret(payoff_row, payoff_col, row_mix, col_mix)
    assert np.allclose(row_mix, [0.5, 0.5], atol=0.08)
    assert np.allclose(col_mix, [0.5, 0.5], atol=0.08)
    assert max(row_reg, col_reg) < 0.08
    assert trace[-1]["max_regret"] < trace[0]["max_regret"]


def test_build_parameter_scenarios_names_and_baseline():
    cfg = PeakShavingConfig.default()
    scenarios = build_parameter_scenarios(cfg)
    names = [s.name for s in scenarios]
    assert names[0] == "baseline"
    assert "capacity_scale_0.85" in names
    assert "alpha_scale_1.20" in names
    assert "switch_cost_scale_1.30" in names
    assert "qos_threshold_0.86" in names
    assert len(names) == len(set(names))
    assert scenarios[0].config.firm_capacity.tolist() == cfg.firm_capacity.tolist()
