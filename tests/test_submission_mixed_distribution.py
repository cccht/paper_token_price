from pathlib import Path
import sys

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def test_weighted_quantile_respects_probability_mass():
    from experiments.build_submission_mixed_distribution import weighted_quantile

    values = np.array([1.0, 2.0, 10.0])
    weights = np.array([0.1, 0.8, 0.1])
    result = weighted_quantile(values, weights, quantiles=(0.05, 0.5, 0.95))

    assert result == pytest.approx([1.0, 2.0, 10.0])


def test_weighted_quantile_uses_discrete_inverse_cdf_at_mass_boundary():
    from experiments.build_submission_mixed_distribution import weighted_quantile

    values = np.array([10.0, 1.0, 2.0])
    weights = np.array([0.1, 0.1, 0.8])

    result = weighted_quantile(values, weights, quantiles=(0.1, 0.9))

    assert result == pytest.approx([1.0, 2.0])


def test_weighted_quantile_rejects_invalid_weights():
    from experiments.build_submission_mixed_distribution import weighted_quantile

    with pytest.raises(ValueError, match="weights"):
        weighted_quantile(np.array([1.0]), np.array([0.0]))


def test_distribution_paths_target_submission_equilibrium():
    from experiments import build_submission_mixed_distribution as module

    assert module.EQUILIBRIUM_PATH.name == "spatiotemporal_equilibrium_submission.json"
    assert module.OUTPUT_PATH.name == "mixed_outcome_distribution_submission.json"


def test_distribution_records_source_hashes():
    from experiments.build_submission_mixed_distribution import _source_hashes

    hashes = _source_hashes()

    assert "pricing_sim/spatiotemporal_game.py" in hashes
    assert all(len(value) == 64 for value in hashes.values())
