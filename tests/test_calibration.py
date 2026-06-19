import csv

import numpy as np

from pricing_sim.calibration import fit_qos_curve, load_controlled_aggregate


def test_fit_qos_curve_reports_observed_points_and_rmse(tmp_path):
    source = tmp_path / "aggregate.csv"
    with source.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["concurrency", "ttft_sla_0_5_rate_mean"],
        )
        writer.writeheader()
        writer.writerows([
            {"concurrency": 64, "ttft_sla_0_5_rate_mean": 1.0},
            {"concurrency": 128, "ttft_sla_0_5_rate_mean": 1.0},
            {"concurrency": 256, "ttft_sla_0_5_rate_mean": 0.7},
            {"concurrency": 512, "ttft_sla_0_5_rate_mean": 0.4},
        ])

    points = load_controlled_aggregate(source)
    result = fit_qos_curve(points)

    assert result.capacity_concurrency == 128.0
    assert result.threshold >= 1.0
    assert result.strength > 0.0
    assert result.rmse < 0.2
    assert np.allclose(result.observed_qos, [1.0, 1.0, 0.7, 0.4])
    assert len(result.fitted_qos) == 4

