from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def test_selected_profiles_are_sorted_and_report_covered_mass():
    from experiments.run_submission_intermediary_audit import _selected_profiles

    game = {"active_profiles": [
        {"weight": 0.2}, {"weight": 0.5}, {"weight": 0.3},
    ]}
    selected, mass = _selected_profiles(game, 2, minimum_coverage=0.8)

    assert [item["weight"] for item in selected] == [0.5, 0.3]
    assert mass == pytest.approx(0.8)


def test_selected_profiles_stop_when_coverage_is_reached():
    from experiments.run_submission_intermediary_audit import _selected_profiles

    game = {"active_profiles": [
        {"weight": 0.6}, {"weight": 0.3}, {"weight": 0.1},
    ]}
    selected, mass = _selected_profiles(game, 3, minimum_coverage=0.75)

    assert len(selected) == 2
    assert mass == pytest.approx(0.9)


def test_selected_profiles_reject_nonpositive_limit():
    from experiments.run_submission_intermediary_audit import _selected_profiles

    with pytest.raises(ValueError, match="positive"):
        _selected_profiles({"active_profiles": []}, 0)


def test_selected_profiles_reject_invalid_coverage():
    from experiments.run_submission_intermediary_audit import _selected_profiles

    with pytest.raises(ValueError, match="minimum_coverage"):
        _selected_profiles({"active_profiles": []}, 1, minimum_coverage=0.0)


def test_selected_profiles_reject_insufficient_profile_limit():
    from experiments.run_submission_intermediary_audit import _selected_profiles

    game = {"active_profiles": [
        {"weight": 0.4}, {"weight": 0.3}, {"weight": 0.2}, {"weight": 0.1},
    ]}
    with pytest.raises(ValueError, match="covers only"):
        _selected_profiles(game, 2, minimum_coverage=0.8)


def test_search_spec_reconstructs_tuple_fields():
    from experiments.run_submission_intermediary_audit import _search_spec

    manifest = {"dynamic": {
        "retail_base_bounds": [0.45, 2.1],
        "retail_slope_bounds": [-1.0, 1.0],
        "route_beta_bounds": [0.0, 1_000_000.0],
        "coarse_base_seeds": [0.7, 1.1, 1.6],
        "coarse_slope_seeds": [-0.6, 0.0, 0.6],
        "route_region_seeds": [0.0, 4.0, 256.0],
    }}
    spec = _search_spec(manifest)

    assert spec.retail_slope_bounds == (-1.0, 1.0)
    assert spec.route_beta_bounds == (0.0, 1_000_000.0)
    assert isinstance(spec.coarse_base_seeds, tuple)


def test_audit_paths_target_submission_equilibrium():
    from experiments import run_submission_intermediary_audit as module

    assert module.EQUILIBRIUM_PATH.name == "spatiotemporal_equilibrium_submission.json"
    assert module.OUTPUT_PATH.name == "intermediary_globality_audit_submission.json"


def test_submission_audit_defaults_cover_all_active_profiles():
    from experiments import run_submission_intermediary_audit as module

    assert module.DEFAULT_MAXIMUM_PROFILES == 1_000
    assert module.DEFAULT_MINIMUM_COVERAGE == 1.0


def test_intermediary_audit_records_source_hashes():
    from experiments.run_submission_intermediary_audit import _source_hashes

    hashes = _source_hashes()

    expected = {
        "experiments/run_submission_intermediary_audit.py",
        "experiments/run_final_spatiotemporal_equilibrium.py",
        "pricing_sim/intermediary_response.py",
        "pricing_sim/peak_shaving_equilibrium.py",
        "pricing_sim/peak_shaving_market.py",
        "pricing_sim/spatiotemporal_game.py",
    }
    assert expected <= set(hashes)
    assert all(len(value) == 64 for value in hashes.values())
