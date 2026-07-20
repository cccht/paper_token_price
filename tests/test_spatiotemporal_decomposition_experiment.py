from importlib import import_module, util
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def test_controlled_decomposition_returns_all_policy_mechanism_cells():
    module_spec = util.find_spec(
        "experiments.run_spatiotemporal_mechanism_decomposition"
    )
    assert module_spec is not None
    module = import_module(
        "experiments.run_spatiotemporal_mechanism_decomposition"
    )
    run = getattr(module, "run_decomposition", None)
    assert callable(run)

    result = run()
    rows = result["rows"]

    assert len(rows) == 12
    assert {row["policy"] for row in rows} == {
        "uniform",
        "symmetric_tou",
        "asymmetric_capacity_balance",
    }
    assert {row["mechanism"] for row in rows} == {
        "neither",
        "temporal_only",
        "spatial_only",
        "combined",
    }
    assert all(row["converged"] for row in rows)
    totals = np.array([row["total_demand"] for row in rows])
    assert np.allclose(totals, totals[0])
    assert all("aggregate_peak_load" in row for row in rows)
    assert all("maximum_provider_utilization" in row for row in rows)
    assert all("temporal_moved_fraction" in row for row in rows)
    assert result["metadata"]["evidence_level"] == "controlled_prototype"
    assert result["metadata"]["git_commit"]
    assert result["metadata"]["model_config"]["qos_threshold"] == 0.82
    assert result["demand_spec"]["flexible_fraction"] == [0.0, 0.8]
    assert result["fixed_channel_shares"] == [0.12, 0.5, 0.38]
    assert result["mechanism_definitions"]["combined"] == {
        "temporal_enabled": True,
        "spatial_enabled": True,
    }
    assert all(
        len(digest) == 64
        for digest in result["metadata"]["source_sha256"].values()
    )


def test_burstgpt_decomposition_uses_observed_profile_for_both_user_types():
    module = import_module(
        "experiments.run_spatiotemporal_mechanism_decomposition"
    )

    result = module.run_decomposition(load_source="burstgpt")

    native = np.asarray(result["demand_spec"]["native_demand"])
    normalized_by_type = native / native.sum(axis=1, keepdims=True)
    assert len(result["rows"]) == 12
    assert result["metadata"]["data_source"] == "BurstGPT token profile"
    assert "--load-source burstgpt" in result["metadata"]["command"]
    assert np.allclose(normalized_by_type[0], normalized_by_type[1])
    assert np.isclose(native.sum(), 1100.0)
    assert any(
        "burstgpt_8period_load_profile.csv" in path
        for path in result["metadata"]["source_sha256"]
    )
    assert any(
        "build_burstgpt_load_anchor.py" in path
        for path in result["metadata"]["source_sha256"]
    )
