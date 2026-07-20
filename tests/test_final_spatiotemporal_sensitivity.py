from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

def _small_grid() -> np.ndarray:
    return np.array([
        [0.35, 0.0, 0.80, 0.0],
        [0.55, 0.0, 1.00, 0.0],
        [0.35, 0.2, 0.80, 0.2],
        [0.55, -0.2, 1.00, -0.2],
    ])


def test_sensitivity_definitions_cover_four_requested_dimensions():
    from experiments.run_final_spatiotemporal_sensitivity import SCENARIOS

    assert set(SCENARIOS) == {
        "baseline",
        "capacity_low",
        "capacity_high",
        "price_sensitivity_low",
        "price_sensitivity_high",
        "migration_cost_low",
        "migration_cost_high",
        "qos_threshold_low",
        "qos_threshold_high",
    }


def test_sensitivity_scenario_is_fully_resolved_on_supplied_grid():
    from experiments.run_final_spatiotemporal_sensitivity import run_sensitivity

    result = run_sensitivity(
        scenario_names=["capacity_low"],
        candidate_grid=_small_grid(),
        max_oracle_rounds=4,
        retail_base_grid=np.array([0.8]),
        dynamic_retail_slope_grid=np.array([0.0]),
        route_beta_grid=np.array([2.0]),
        write_checkpoints=False,
    )

    assert len(result["rows"]) == 1
    row = result["rows"][0]
    assert row["scenario"] == "capacity_low"
    assert row["group"] == "capacity_scale"
    assert row["value"] == 0.85
    assert row["uniform_full_grid_verified"]
    assert row["dynamic_full_grid_verified"]
    assert row["dynamic_full_max_regret"] <= 1e-7
    assert np.isclose(row["dynamic_total_demand"], 1100.0)
    assert result["metadata"]["fully_resolved"] is True
