from pathlib import Path
import sys

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def test_uniform_candidate_design_is_independent_bounded_and_zero_slope():
    from experiments.uniform_offgrid_diagnostic_tools import (
        BASE_PRICE_BOUNDS,
        uniform_candidate_design,
    )

    support = np.array([
        [0.45, 0.0, 0.70, 0.0],
        [0.55, 0.0, 0.80, 0.0],
    ])
    vectors, sources = uniform_candidate_design(
        support, samples=16, seed=20260718
    )

    assert vectors.shape[1] == 4
    assert np.all(vectors[:, [1, 3]] == 0.0)
    assert set(sources) >= {"active_support", "latin_hypercube", "boundary_guard"}
    assert sources.count("latin_hypercube") == 16
    assert all(any(np.array_equal(vector, item) for vector in vectors) for item in support)
    for dimension, bounds in zip((0, 2), BASE_PRICE_BOUNDS):
        assert np.all(vectors[:, dimension] >= bounds[0])
        assert np.all(vectors[:, dimension] <= bounds[1])
        assert any(vector[dimension] == bounds[0] for vector in vectors)
        assert any(vector[dimension] == bounds[1] for vector in vectors)


def test_uniform_candidate_design_rejects_nonuniform_support():
    from experiments.uniform_offgrid_diagnostic_tools import uniform_candidate_design

    with pytest.raises(ValueError, match="zero-slope"):
        uniform_candidate_design(
            np.array([[0.45, 0.1, 0.70, 0.0]]), samples=4, seed=17
        )


def test_uniform_local_refinement_is_a_bounded_17_by_17_lattice():
    from experiments.uniform_offgrid_diagnostic_tools import (
        BASE_PRICE_BOUNDS,
        uniform_local_refinement,
    )

    center = np.array([0.52, 0.0, 0.74, 0.0])
    vectors = uniform_local_refinement(
        center, points_per_axis=17, half_width_fraction=0.025
    )

    assert vectors.shape == (289, 4)
    assert np.all(vectors[:, [1, 3]] == 0.0)
    assert any(np.array_equal(vector, center) for vector in vectors)
    assert np.all(vectors[:, 0] >= BASE_PRICE_BOUNDS[0, 0])
    assert np.all(vectors[:, 0] <= BASE_PRICE_BOUNDS[0, 1])
    assert np.all(vectors[:, 2] >= BASE_PRICE_BOUNDS[1, 0])
    assert np.all(vectors[:, 2] <= BASE_PRICE_BOUNDS[1, 1])


def test_submission_uniform_offgrid_runner_declares_all_nine_scenarios():
    from experiments import run_submission_uniform_offgrid_audit as module
    from experiments.run_submission_spatiotemporal_sensitivity import SCENARIOS

    assert tuple(module.SCENARIO_PATHS) == ("baseline", *SCENARIOS)
    assert module.SUBMISSION_SAMPLES_PER_PLAYER == 1024
    assert module.SUBMISSION_RANDOM_SEED == 20260718
    assert module.OUTPUT_PATH.name == "uniform_offgrid_sensitivity_submission.json"
    assert module.CACHE_ROOT.name == "peak_shaving_uniform_offgrid"
    assert not str(module.CACHE_ROOT).startswith("/tmp/")
