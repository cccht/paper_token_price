from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from experiments.peak_shaving_submission_tools import (
    best_response_regret,
    build_parameter_scenarios,
    empirical_fictitious_play,
    fine_candidate_grid,
    nearest_candidate,
)
from pricing_sim.peak_shaving_config import PeakShavingConfig


def test_fine_candidate_grid_matches_documented_size():
    grid = fine_candidate_grid()
    assert grid.shape == (225, 4)
    assert np.allclose(grid[0], [0.27, -0.4, 0.60, -0.4])
    assert np.allclose(grid[-1], [0.88, 0.4, 1.60, 0.4])


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
