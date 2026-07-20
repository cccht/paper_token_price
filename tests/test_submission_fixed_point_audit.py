from pathlib import Path
import sys

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def test_random_routing_is_periodwise_conserved():
    from experiments.run_submission_fixed_point_audit import _random_routing

    routing = _random_routing(np.random.default_rng(4), 8)

    assert routing.shape == (2, 8)
    assert np.all((routing >= 0.0) & (routing <= 1.0))
    assert np.allclose(routing.sum(axis=0), 1.0)


def test_audit_profile_rejects_nonpositive_starts():
    from experiments.run_submission_fixed_point_audit import _audit_profile

    with pytest.raises(ValueError, match="positive"):
        _audit_profile({}, starts=0, seed=1, game=None, config=None)


def test_audit_paths_target_submission_equilibrium():
    from experiments import run_submission_fixed_point_audit as module

    assert module.EQUILIBRIUM_PATH.name == "spatiotemporal_equilibrium_submission.json"
    assert module.OUTPUT_PATH.name == "fixed_point_multistart_audit_submission.json"


def test_fixed_point_audit_reuses_full_profile_coverage_defaults():
    from experiments import run_submission_fixed_point_audit as module

    assert module.DEFAULT_MAXIMUM_PROFILES == 1_000
    assert module.DEFAULT_MINIMUM_COVERAGE == 1.0


def test_fixed_point_audit_records_source_hashes():
    from experiments.run_submission_fixed_point_audit import _source_hashes

    hashes = _source_hashes()

    expected = {
        "experiments/run_submission_fixed_point_audit.py",
        "experiments/run_final_spatiotemporal_equilibrium.py",
        "experiments/run_submission_intermediary_audit.py",
        "pricing_sim/peak_shaving_equilibrium.py",
        "pricing_sim/peak_shaving_market.py",
        "pricing_sim/spatiotemporal_game.py",
    }
    assert expected <= set(hashes)
    assert all(len(value) == 64 for value in hashes.values())
