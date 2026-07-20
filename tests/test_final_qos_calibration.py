from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def test_pooled_qos_fit_uses_the_same_function_as_the_market_model():
    from experiments.build_final_qos_calibration import (
        load_anchor_points,
        pooled_qos_fit,
    )
    from pricing_sim.peak_shaving_config import PeakShavingConfig
    from pricing_sim.peak_shaving_market import qos_factor

    points = load_anchor_points()
    fit = pooled_qos_fit(points)
    config = PeakShavingConfig.default().evolve(
        qos_threshold=fit["threshold"],
        qos_strength=fit["strength"],
    )
    utilization = np.array([point["normalized_utilization"] for point in points])
    model_values = qos_factor(utilization, config, "threshold")

    assert len(points) == 10
    assert 1.0 <= fit["threshold"] <= 1.3
    assert fit["strength"] > 0.0
    assert fit["rmse"] < 0.12
    assert np.allclose(model_values, fit["fitted_qos"])
    assert set(fit["rmse_by_profile"]) == {"vllm-0.5b", "vllm-3b"}


def test_qos_calibration_artifact_records_sources_and_leave_profile_out_error():
    from experiments.build_final_qos_calibration import build_calibration

    artifact = build_calibration()

    assert artifact["metadata"]["fit_function"].startswith("q(u)=exp")
    assert len(artifact["metadata"]["source_sha256"]) >= 3
    assert set(artifact["leave_one_profile_out"]) == {
        "train_vllm-0.5b_test_vllm-3b",
        "train_vllm-3b_test_vllm-0.5b",
    }
    assert all(
        value["test_rmse"] >= 0.0
        for value in artifact["leave_one_profile_out"].values()
    )
