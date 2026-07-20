from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def test_continuous_intermediary_search_improves_on_the_legacy_response_grid():
    from experiments.run_final_spatiotemporal_equilibrium import final_case
    from pricing_sim.intermediary_response import (
        IntermediarySearchSpec,
        optimize_intermediary_response_spatiotemporal,
    )
    from pricing_sim.peak_shaving_equilibrium import FirmParams
    from pricing_sim.peak_shaving_market import intermediary_profit
    from pricing_sim.spatiotemporal_game import (
        intermediary_best_response_spatiotemporal,
    )

    config, game, _ = final_case()
    firms = [
        FirmParams.from_vector(np.array([0.575, 0.2, 0.6, 0.2])),
        FirmParams.from_vector(np.array([0.575, 0.4, 0.6, 0.4])),
    ]
    wholesale = np.vstack([firm.wholesale(config) for firm in firms])
    direct = np.vstack([firm.direct(config) for firm in firms])
    legacy_state, legacy_result = intermediary_best_response_spatiotemporal(
        wholesale,
        direct,
        game,
        config,
        retail_base_grid=np.array([0.8, 1.1, 1.5]),
        retail_slope_grid=np.array([-0.3, 0.0, 0.3]),
        route_beta_grid=np.array([1.5, 4.0]),
    )

    state, result = optimize_intermediary_response_spatiotemporal(
        wholesale,
        direct,
        game,
        config,
        IntermediarySearchSpec(),
    )

    legacy_profit = intermediary_profit(legacy_state, legacy_result, config)
    candidate = result["intermediary_candidate"]
    search = result["intermediary_search"]
    assert intermediary_profit(state, result, config) > legacy_profit + 10.0
    assert candidate["route_beta"] > 4.0
    assert search["method"] == "deterministic_multistart_lbfgsb"
    assert search["function_evaluations"] >= search["coarse_seed_count"]
    assert search["successful_local_runs"] == 3
    assert result["joint_converged"]


def test_continuous_intermediary_search_checks_low_route_sensitivity_basin():
    from experiments.peak_shaving_submission_tools import fine_candidate_grid
    from experiments.run_final_spatiotemporal_equilibrium import final_case
    from pricing_sim.intermediary_response import (
        IntermediarySearchSpec,
        optimize_intermediary_response_spatiotemporal,
    )
    from pricing_sim.peak_shaving_equilibrium import FirmParams

    config, game, _ = final_case()
    grid = fine_candidate_grid()
    firms = [FirmParams.from_vector(grid[224]), FirmParams.from_vector(grid[0])]
    wholesale = np.vstack([firm.wholesale(config) for firm in firms])
    direct = np.vstack([firm.direct(config) for firm in firms])

    _, result = optimize_intermediary_response_spatiotemporal(
        wholesale,
        direct,
        game,
        config,
        IntermediarySearchSpec(),
    )

    assert result["intermediary_candidate"]["route_beta"] < 1e-6
    assert result["intermediary_search"]["searched_route_regions"] == [
        "low",
        "intermediate",
        "near_deterministic",
    ]


def test_low_route_search_covers_the_interior_positive_slope_basin():
    from experiments.run_final_spatiotemporal_equilibrium import final_case
    from pricing_sim.intermediary_response import (
        IntermediarySearchSpec,
        optimize_intermediary_response_spatiotemporal,
    )
    from pricing_sim.peak_shaving_equilibrium import FirmParams
    from pricing_sim.peak_shaving_market import intermediary_profit

    config, game, _ = final_case()
    firms = [
        FirmParams.from_vector(np.array([0.315, 0.8, 0.579375, 0.4])),
        FirmParams.from_vector(np.array([0.25, 1.1, 0.55875, 0.3])),
    ]
    wholesale = np.vstack([firm.wholesale(config) for firm in firms])
    direct = np.vstack([firm.direct(config) for firm in firms])

    state, result = optimize_intermediary_response_spatiotemporal(
        wholesale, direct, game, config, IntermediarySearchSpec()
    )

    candidate = result["intermediary_candidate"]
    assert intermediary_profit(state, result, config) > 296.9
    assert candidate["route_beta"] < 1e-6
    assert 0.2 < candidate["retail_slope"] < 0.35
