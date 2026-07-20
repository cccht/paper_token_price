from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _game() -> dict:
    return {
        "row_support_indices": [10, 11],
        "col_support_indices": [20, 21],
        "row_mix": [0.25, 0.75],
        "col_mix": [0.4, 0.6],
    }


def _records() -> list[dict]:
    global_a = [[5.0, 1.0], [2.0, 4.0]]
    global_b = [[1.0, 4.0], [5.0, 2.0]]
    changes_a = [[1.0, -1.0], [2.0, -2.0]]
    changes_b = [[-2.0, 1.0], [-1.0, 3.0]]
    row_indices, col_indices = _game()["row_support_indices"], _game()[
        "col_support_indices"
    ]
    row_mix, col_mix = _game()["row_mix"], _game()["col_mix"]
    records = []
    for i, row_index in enumerate(row_indices):
        for j, col_index in enumerate(col_indices):
            records.append({
                "row_index": row_index,
                "col_index": col_index,
                "equilibrium_weight": row_mix[i] * col_mix[j],
                "stored_provider_payoffs": {
                    "firm_A": global_a[i][j] - changes_a[i][j],
                    "firm_B": global_b[i][j] - changes_b[i][j],
                },
                "global_provider_payoffs": {
                    "firm_A": global_a[i][j],
                    "firm_B": global_b[i][j],
                },
            })
    return records


def test_payoff_summary_reports_weighted_changes_and_active_support_regret():
    from experiments.build_submission_intermediary_payoff_sensitivity import (
        summarize_provider_payoff_sensitivity,
    )

    summary = summarize_provider_payoff_sensitivity(_records(), _game())

    assert summary["covered_probability_mass"] == pytest.approx(1.0)
    assert summary["firm_A"]["weighted_signed_change"] == pytest.approx(-0.35)
    assert summary["firm_A"]["weighted_absolute_change"] == pytest.approx(1.75)
    assert summary["firm_B"]["weighted_signed_change"] == pytest.approx(1.0)
    assert summary["firm_B"]["weighted_absolute_change"] == pytest.approx(2.0)
    assert summary["firm_A"]["active_support_regret"] == pytest.approx(0.15)
    assert summary["firm_B"]["active_support_regret"] == pytest.approx(0.9)
    assert summary["maximum_active_support_regret"] == pytest.approx(0.9)
    assert summary["maximum_absolute_profile_change"]["provider"] == "firm_B"
    assert summary["maximum_absolute_profile_change"]["change"] == pytest.approx(3.0)


def test_payoff_summary_rejects_incomplete_active_profile_matrix():
    from experiments.build_submission_intermediary_payoff_sensitivity import (
        summarize_provider_payoff_sensitivity,
    )

    with pytest.raises(ValueError, match="complete active profile matrix"):
        summarize_provider_payoff_sensitivity(_records()[:-1], _game())


def test_payoff_sensitivity_paths_bind_equilibrium_and_globality_audit():
    from experiments import build_submission_intermediary_payoff_sensitivity as module

    assert module.EQUILIBRIUM_PATH.name == "spatiotemporal_equilibrium_submission.json"
    assert module.INTERMEDIARY_AUDIT_PATH.name == (
        "intermediary_globality_audit_submission.json"
    )
    assert module.OUTPUT_PATH.name == "intermediary_payoff_sensitivity_submission.json"
