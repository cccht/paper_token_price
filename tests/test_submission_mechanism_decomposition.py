from pathlib import Path
import sys

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def test_aggregate_policy_requires_active_profiles():
    from experiments.run_submission_mechanism_decomposition import _aggregate_policy

    with pytest.raises(ValueError, match="no active profiles"):
        _aggregate_policy("dynamic", {"active_profiles": []}, None, None)


def test_submission_decomposition_targets_mixed_equilibrium():
    from experiments import run_submission_mechanism_decomposition as module

    assert module.EQUILIBRIUM_PATH.name == "spatiotemporal_equilibrium_submission.json"
    assert module.OUTPUT_PATH.name == "mechanism_decomposition_submission.json"
    assert module.MECHANISMS == {
        "neither": (False, False),
        "temporal_only": (True, False),
        "spatial_only": (False, True),
        "combined": (True, True),
    }


def test_submission_decomposition_records_source_hashes():
    from experiments.run_submission_mechanism_decomposition import _source_hashes

    hashes = _source_hashes()

    expected = {
        "experiments/final_equilibrium_tools.py",
        "experiments/run_final_spatiotemporal_equilibrium.py",
        "experiments/run_submission_intermediary_audit.py",
        "experiments/run_submission_mechanism_decomposition.py",
        "pricing_sim/peak_shaving_equilibrium.py",
        "pricing_sim/peak_shaving_market.py",
        "pricing_sim/spatiotemporal_game.py",
        "pricing_sim/spatiotemporal_mechanism.py",
    }
    assert expected <= set(hashes)
    assert all(len(value) == 64 for value in hashes.values())


def test_spatially_disabled_decomposition_fixes_intermediary_routing():
    from experiments.run_final_spatiotemporal_equilibrium import final_case
    from experiments.run_submission_mechanism_decomposition import _solve_profile_market

    config, game, _ = final_case()
    periods = config.num_periods
    state, result = _solve_profile_market(
        retail=np.full(periods, 0.9),
        wholesale=np.vstack([np.full(periods, 0.25), np.full(periods, 0.9)]),
        direct=np.vstack([np.full(periods, 0.7), np.full(periods, 1.1)]),
        route_beta=1_000.0,
        temporal=True,
        spatial=False,
        base_game=game,
        config=config,
    )

    expected = np.repeat(
        (config.firm_capacity / config.firm_capacity.sum())[:, None], periods, axis=1
    )
    assert result["joint_converged"]
    assert np.allclose(state.routing, expected)


def test_policy_comparison_pairs_uniform_and_dynamic_by_mechanism():
    from experiments.run_submission_mechanism_decomposition import _policy_comparisons

    rows = []
    for policy, offset in (("uniform", 0.0), ("dynamic", -10.0)):
        for mechanism in ("neither", "temporal_only", "spatial_only", "combined"):
            rows.append({
                "policy": policy,
                "mechanism": mechanism,
                "aggregate_peak_load": 100.0 + offset,
                "maximum_provider_utilization": 1.0 + offset / 100.0,
                "minimum_provider_qos": 0.8 - offset / 100.0,
                "system_profit": 200.0 + offset,
            })

    comparisons = _policy_comparisons(rows)

    assert len(comparisons) == 4
    assert comparisons[0]["aggregate_peak_load_change"] == pytest.approx(-10.0)
    assert comparisons[0]["aggregate_peak_load_change_percent"] == pytest.approx(-10.0)
    assert comparisons[0]["minimum_provider_qos_change"] == pytest.approx(0.1)
