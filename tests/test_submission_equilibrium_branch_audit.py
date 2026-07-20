from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from experiments.run_submission_equilibrium_branch_audit import (
    cluster_mixed_candidates,
    full_candidate_regret,
    restricted_game_regret,
    weighted_outcome_metrics,
)


def test_restricted_game_regret_is_zero_for_matching_pennies_equilibrium():
    row_payoff = np.array([[1.0, -1.0], [-1.0, 1.0]])
    col_payoff = -row_payoff
    mix = np.array([0.5, 0.5])

    result = restricted_game_regret(row_payoff, col_payoff, mix, mix)

    assert result["row_regret"] == 0.0
    assert result["col_regret"] == 0.0
    assert result["max_regret"] == 0.0


def test_cluster_mixed_candidates_separates_distinct_equilibrium_branches():
    candidates = [
        {"row_mix": [1.0, 0.0], "col_mix": [1.0, 0.0], "source": "a"},
        {
            "row_mix": [1.0 - 1e-8, 1e-8],
            "col_mix": [1.0, 0.0],
            "source": "b",
        },
        {"row_mix": [0.0, 1.0], "col_mix": [0.0, 1.0], "source": "c"},
    ]

    clusters = cluster_mixed_candidates(candidates, tolerance=1e-6)

    assert len(clusters) == 2
    assert clusters[0]["source_count"] == 2
    assert clusters[0]["sources"] == ["a", "b"]
    assert clusters[1]["source_count"] == 1


def test_full_candidate_regret_detects_omitted_profitable_deviation():
    restricted_row = np.array([[1.0]])
    restricted_col = np.array([[2.0]])
    row_full = np.array([[1.0], [1.5]])
    col_full = np.array([[2.0, 2.25]])

    result = full_candidate_regret(
        restricted_row,
        restricted_col,
        row_full,
        col_full,
        np.array([1.0]),
        np.array([1.0]),
    )

    assert result["row_regret"] == 0.5
    assert result["col_regret"] == 0.25
    assert result["max_regret"] == 0.5


def test_weighted_outcome_metrics_uses_independent_product_weights():
    records = {
        (10, 20): {"aggregate_peak_load": 100.0, "minimum_provider_qos": 0.9},
        (10, 21): {"aggregate_peak_load": 120.0, "minimum_provider_qos": 0.8},
        (11, 20): {"aggregate_peak_load": 140.0, "minimum_provider_qos": 0.7},
        (11, 21): {"aggregate_peak_load": 160.0, "minimum_provider_qos": 0.6},
    }

    result = weighted_outcome_metrics(
        records,
        [10, 11],
        [20, 21],
        np.array([0.25, 0.75]),
        np.array([0.4, 0.6]),
        ("aggregate_peak_load", "minimum_provider_qos"),
    )

    assert np.isclose(result["aggregate_peak_load"], 142.0)
    assert np.isclose(result["minimum_provider_qos"], 0.69)
