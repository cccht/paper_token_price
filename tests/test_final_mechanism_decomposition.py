from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def test_final_mechanism_decomposition_uses_equilibrium_policies_and_all_switches():
    from experiments.run_final_mechanism_decomposition import run_decomposition

    result = run_decomposition()
    rows = result["rows"]

    assert len(rows) == 8
    assert {row["policy"] for row in rows} == {"uniform", "dynamic"}
    assert {row["mechanism"] for row in rows} == {
        "neither",
        "temporal_only",
        "spatial_only",
        "combined",
    }
    assert all(row["converged"] for row in rows)
    assert np.allclose([row["total_demand"] for row in rows], 1100.0)
    assert all(row["joint_residual"] <= 1e-8 for row in rows)


def test_combined_cell_reproduces_final_equilibrium_metrics():
    from experiments.run_final_mechanism_decomposition import run_decomposition

    result = run_decomposition()
    dynamic = next(
        row for row in result["rows"]
        if row["policy"] == "dynamic" and row["mechanism"] == "combined"
    )
    equilibrium = result["equilibrium_metrics"]["dynamic"]

    assert np.isclose(
        dynamic["aggregate_peak_load"], equilibrium["aggregate_peak_load"]
    )
    assert np.isclose(
        dynamic["maximum_provider_utilization"],
        equilibrium["maximum_provider_utilization"],
    )
    assert np.isclose(dynamic["minimum_provider_qos"], equilibrium["minimum_provider_qos"])
    assert len(result["metadata"]["equilibrium_sha256"]) == 64
