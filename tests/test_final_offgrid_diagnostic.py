import json
from pathlib import Path
import sys

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def _equilibrium_fixture(path: Path, *, response_method: str = "continuous_multistart"):
    payload = {
        "scenario": {
            "capacity_scale": 1.0,
            "price_sensitivity_scale": 1.0,
            "migration_cost_scale": 1.0,
            "qos_threshold_shift": 0.0,
        },
        "provider_strategy_grid": {"candidate_count": 1370},
        "intermediary_response": {
            "method": response_method,
            "dynamic": {
                "retail_base_bounds": [0.45, 2.1],
                "retail_slope_bounds": [-1.0, 1.0],
                "route_beta_bounds": [0.0, 1_000_000.0],
                "coarse_base_seeds": [0.7, 1.1, 1.6],
                "coarse_slope_seeds": [-0.6, 0.0, 0.6],
                "route_region_seeds": [0.0, 4.0, 256.0],
                "max_iterations": 250,
                "absolute_tie_tolerance": 1e-8,
                "relative_tie_tolerance": 1e-10,
            },
        },
        "dynamic": {
            "row_support_vectors": [[0.25, 0.0, 0.45, 0.6]],
            "col_support_vectors": [[0.25, 0.2, 0.6, 0.4]],
            "row_mix": [1.0],
            "col_mix": [1.0],
            "expected_metrics": {"firm_A_profit": 10.0, "firm_B_profit": 9.0},
        },
    }
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_candidate_design_covers_support_bounds_and_slope_guards():
    from experiments.offgrid_diagnostic_tools import _candidate_design

    support = np.array([[0.25, 1.5, 0.60, 0.4]])
    domain = {
        "wholesale_base": [0.25, 0.90],
        "wholesale_slope": [-4.0, 4.0],
        "direct_base": [0.45, 2.10],
        "direct_slope": [-4.0, 4.0],
    }
    vectors, sources = _candidate_design(support, domain, samples=8, seed=17)

    assert any(np.allclose(vector, support[0]) for vector in vectors)
    assert set(sources) >= {"active_support", "latin_hypercube", "axis_guard"}
    for dimension, bounds in enumerate(domain.values()):
        for bound in bounds:
            assert any(np.isclose(vector[dimension], bound) for vector in vectors)
    assert np.all(vectors[:, 0] >= 0.25) and np.all(vectors[:, 0] <= 0.90)
    assert np.all(vectors[:, 2] >= 0.45) and np.all(vectors[:, 2] <= 2.10)
    assert np.any(np.isclose(vectors[:, 1], 4.0))
    assert np.any(np.isclose(vectors[:, 3], -4.0))


def test_pairwise_refinement_stays_bounded_and_changes_two_dimensions():
    from experiments.offgrid_diagnostic_tools import _pairwise_refinement

    center = np.array([0.2825, 1.0, 0.6, 0.2])
    domain = {
        "wholesale_base": [0.25, 0.90],
        "wholesale_slope": [-4.0, 4.0],
        "direct_base": [0.45, 2.10],
        "direct_slope": [-4.0, 4.0],
    }
    vectors = _pairwise_refinement(center, domain)

    bounds = np.asarray(list(domain.values()))
    assert len(vectors) > 100
    assert np.all(vectors >= bounds[:, 0])
    assert np.all(vectors <= bounds[:, 1])
    changed = np.sum(~np.isclose(vectors, center), axis=1)
    assert np.all(changed <= 2)
    assert np.any(changed == 2)
    assert any(
        np.isclose(vector[0], 0.25) and not np.isclose(vector[1], center[1])
        for vector in vectors
    )


def test_offgrid_diagnostic_uses_expanded_equilibrium_and_continuous_response(
    tmp_path, monkeypatch
):
    import experiments.run_spatiotemporal_offgrid_diagnostic as module

    equilibrium_path = tmp_path / "equilibrium.json"
    _equilibrium_fixture(equilibrium_path)
    calls = []

    def fake_search(player, game, samples, seed, **kwargs):
        calls.append((player, samples, seed, kwargs))
        payoff = game["expected_metrics"][
            "firm_A_profit" if player == "firm_A" else "firm_B_profit"
        ]
        return {
            "equilibrium_payoff": payoff,
            "best_payoff": payoff,
            "best_vector": [0.25, 0.0, 0.45, 0.0],
            "offgrid_regret": 0.0,
            "relative_offgrid_regret": 0.0,
            "evaluated_candidates": samples + 1,
            "all_joint_converged": True,
            "maximum_joint_residual": 0.0,
            "top_candidates": [],
        }

    monkeypatch.setattr(module, "_search_player", fake_search)
    result = module.run_offgrid_diagnostic(
        samples_per_player=4,
        seed=17,
        equilibrium_path=equilibrium_path,
        parallel_workers=3,
    )

    assert result["metadata"]["seed"] == 17
    assert module.SUBMISSION_SAMPLES_PER_PLAYER == 1024
    assert module.SUBMISSION_RANDOM_SEED == 20260714
    assert module.EQUILIBRIUM_PATH.name == "spatiotemporal_equilibrium_submission.json"
    assert module.OUTPUT_PATH.name == "spatiotemporal_offgrid_diagnostic_submission.json"
    assert result["metadata"]["provider_candidate_count"] == 1370
    assert result["metadata"]["intermediary_response_method"] == "continuous_multistart"
    assert result["metadata"]["parallel_workers"] == 3
    assert result["search_domain"] == {
        "wholesale_base": [0.25, 0.9],
        "wholesale_slope": [-4.0, 4.0],
        "direct_base": [0.45, 2.1],
        "direct_slope": [-4.0, 4.0],
    }
    assert [call[:3] for call in calls] == [
        ("firm_A", 4, 17),
        ("firm_B", 4, 18),
    ]
    assert all(call[3]["parallel_workers"] == 3 for call in calls)
    assert all(call[3]["intermediary_search_spec"] is not None for call in calls)
    assert all(
        call[3]["cache_path"].parent.name
        == "peak_shaving_submission_offgrid_fourth_grid"
        for call in calls
    )


def test_offgrid_diagnostic_rejects_old_finite_intermediary_grid(tmp_path):
    from experiments.run_spatiotemporal_offgrid_diagnostic import (
        run_offgrid_diagnostic,
    )

    equilibrium_path = tmp_path / "equilibrium.json"
    _equilibrium_fixture(equilibrium_path, response_method="finite_grid")

    with pytest.raises(ValueError, match="continuous intermediary response"):
        run_offgrid_diagnostic(
            samples_per_player=2,
            equilibrium_path=equilibrium_path,
        )


def test_offgrid_diagnostic_records_equilibrium_and_source_hashes(
    tmp_path, monkeypatch
):
    import experiments.run_spatiotemporal_offgrid_diagnostic as module

    equilibrium_path = tmp_path / "equilibrium.json"
    _equilibrium_fixture(equilibrium_path)
    monkeypatch.setattr(
        module,
        "_search_player",
        lambda *args, **kwargs: {
            "equilibrium_payoff": 1.0,
            "best_payoff": 1.0,
            "best_vector": [0.25, 0.0, 0.45, 0.0],
            "offgrid_regret": 0.0,
            "relative_offgrid_regret": 0.0,
            "evaluated_candidates": 1,
            "all_joint_converged": True,
            "maximum_joint_residual": 0.0,
            "top_candidates": [],
        },
    )

    result = module.run_offgrid_diagnostic(
        samples_per_player=2,
        seed=3,
        equilibrium_path=equilibrium_path,
    )

    assert len(result["metadata"]["equilibrium_sha256"]) == 64
    assert all(
        len(digest) == 64
        for digest in result["metadata"]["source_sha256"].values()
    )
