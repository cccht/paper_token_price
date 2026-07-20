from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def test_vector_pair_cache_remaps_records_when_grid_indices_change(tmp_path):
    from experiments.equilibrium_cache import (
        load_vector_pair_cache,
        write_vector_pair_cache,
    )

    old_grid = np.array([
        [0.25, 0.0, 0.45, 0.0],
        [0.25, 0.2, 0.60, 0.2],
        [0.575, 0.0, 0.60, 0.0],
    ])
    records = {
        (0, 1): {"firm_A_profit": 1.0},
        (2, 0): {"firm_A_profit": 2.0},
    }
    path = tmp_path / "pairs.pkl"
    write_vector_pair_cache(path, "scenario-v1", old_grid, records)
    new_grid = np.array([old_grid[2], old_grid[0], [0.9, 0.0, 1.6, 0.0], old_grid[1]])

    loaded = load_vector_pair_cache(path, "scenario-v1", new_grid)

    assert loaded == {
        (1, 3): {"firm_A_profit": 1.0},
        (0, 1): {"firm_A_profit": 2.0},
    }
    assert load_vector_pair_cache(path, "different-scenario", new_grid) == {}


def test_pair_evaluator_checkpoints_parallel_results():
    from experiments.final_equilibrium_tools import PairEvaluator
    from experiments.run_final_spatiotemporal_equilibrium import final_case

    config, game, _ = final_case()
    grid = np.array([
        [0.25, 0.0, 0.45, 0.0],
        [0.575, 0.0, 0.60, 0.0],
    ])
    checkpoints = []
    evaluator = PairEvaluator(
        grid=grid,
        game=game,
        config=config,
        retail_base_grid=np.array([0.8]),
        retail_slope_grid=np.array([0.0]),
        route_beta_grid=np.array([2.0]),
        parallel_workers=2,
        checkpoint_callback=lambda records: checkpoints.append(len(records)),
        checkpoint_interval=2,
    )

    evaluator.evaluate_many([(0, 0), (0, 1), (1, 0), (1, 1)])

    assert checkpoints[-1] == 4
    assert any(size >= 2 for size in checkpoints)
