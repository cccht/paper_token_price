from pathlib import Path
import sys

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def test_flatten_vector_preserves_bases_and_zeros_slopes():
    from experiments.run_submission_price_shape_decomposition import _flatten_vector

    vector = np.array([0.31, 1.2, 0.58, 0.4])

    assert np.array_equal(_flatten_vector(vector), np.array([0.31, 0.0, 0.58, 0.0]))


def test_mean_flattened_schedule_preserves_each_price_series_mean():
    from experiments.run_submission_price_shape_decomposition import (
        _mean_flattened_schedule,
    )

    schedule = np.array([[0.25, 0.30, 0.35], [0.60, 0.90, 1.20]])

    flattened = _mean_flattened_schedule(schedule)

    assert np.allclose(flattened, [[0.30, 0.30, 0.30], [0.90, 0.90, 0.90]])
    assert np.allclose(flattened.mean(axis=-1), schedule.mean(axis=-1))


def test_component_rows_reconstruct_total_policy_difference():
    from experiments.run_submission_price_shape_decomposition import _component_rows

    uniform = {
        "aggregate_peak_load": 220.0,
        "maximum_provider_utilization": 1.4,
        "minimum_provider_qos": 0.89,
        "system_profit": 2000.0,
    }
    flattened = {
        "aggregate_peak_load": 210.0,
        "maximum_provider_utilization": 1.3,
        "minimum_provider_qos": 0.92,
        "system_profit": 1950.0,
    }
    dynamic = {
        "aggregate_peak_load": 195.0,
        "maximum_provider_utilization": 1.2,
        "minimum_provider_qos": 0.96,
        "system_profit": 1920.0,
    }

    rows = _component_rows(uniform, flattened, dynamic)
    indexed = {row["metric"]: row for row in rows}

    peak = indexed["aggregate_peak_load"]
    assert peak["overall_change"] == pytest.approx(-25.0)
    assert peak["shape_change"] == pytest.approx(-15.0)
    assert peak["level_and_mix_remainder"] == pytest.approx(-10.0)
    assert peak["identity_error"] == pytest.approx(0.0)

    qos = indexed["minimum_provider_qos"]
    assert qos["overall_change"] == pytest.approx(0.07)
    assert qos["shape_change"] == pytest.approx(0.04)
    assert qos["level_and_mix_remainder"] == pytest.approx(0.03)


def test_price_shape_output_targets_submission_artifact():
    from experiments import run_submission_price_shape_decomposition as module

    assert module.EQUILIBRIUM_PATH.name == "spatiotemporal_equilibrium_submission.json"
    assert module.OUTPUT_PATH.name == "price_shape_decomposition_submission.json"
