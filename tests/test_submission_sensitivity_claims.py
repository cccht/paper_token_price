import hashlib
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def _rows():
    from experiments.build_submission_sensitivity_table import SCENARIO_ORDER

    rows = []
    for index, scenario in enumerate(SCENARIO_ORDER):
        rows.append({
            "scenario": scenario,
            "uniform_full_max_regret": 1e-12 * (index + 1),
            "dynamic_full_max_regret": 2e-12 * (index + 1),
            "maximum_joint_residual": 1e-10 * (index + 1),
            "aggregate_peak_change_percent": -15.0 + index,
            "maximum_provider_utilization_change_percent": -20.0 + index,
            "minimum_provider_qos_change": 0.01 + 0.005 * index,
            "market_profit_change_percent": -4.0 + index,
        })
    return rows


def test_claim_summary_reports_ranges_directions_and_profit_signs():
    from experiments.build_submission_sensitivity_claims import summarize_rows

    result = summarize_rows(_rows())

    assert result["scenario_count"] == 9
    assert result["aggregate_peak_change_percent"] == {
        "minimum": -15.0,
        "maximum": -7.0,
        "all_improve": True,
    }
    assert result["maximum_provider_utilization_change_percent"] == {
        "minimum": -20.0,
        "maximum": -12.0,
        "all_improve": True,
    }
    assert result["minimum_provider_qos_change"] == {
        "minimum": 0.01,
        "maximum": 0.05,
        "all_improve": True,
    }
    assert result["market_profit_change_percent"] == {
        "minimum": -4.0,
        "maximum": 4.0,
        "negative_count": 4,
        "zero_count": 1,
        "positive_count": 4,
        "sign_robust": False,
    }
    assert result["maximum_full_regret"] == pytest.approx(1.8e-11)
    assert result["maximum_joint_residual"] == pytest.approx(9e-10)


def test_claim_builder_requires_the_locked_nine_scenario_order():
    from experiments.build_submission_sensitivity_claims import build_claims

    summary = {
        "metadata": {"scenario_count": 9, "provider_candidate_count": 1576},
        "rows": list(reversed(_rows())),
    }

    with pytest.raises(ValueError, match="scenario order"):
        build_claims(summary, source_sha256="0" * 64)


def test_claim_builder_records_summary_hash_and_candidate_scope():
    from experiments.build_submission_sensitivity_claims import build_claims

    digest = hashlib.sha256(b"summary").hexdigest()
    result = build_claims(
        {
            "metadata": {"scenario_count": 9, "provider_candidate_count": 1576},
            "rows": _rows(),
        },
        source_sha256=digest,
    )

    metadata = result["metadata"]
    assert metadata["source_summary_sha256"] == digest
    assert metadata["provider_candidate_count"] == 1576
    assert metadata["scope"] == (
        "baseline and eight local finite-game re-solves"
    )
    assert "all nine cases" in result["interpretation_boundary"]
    assert "four-dimensional dynamic-policy off-grid" in result[
        "interpretation_boundary"
    ]
    assert set(metadata["source_sha256"]) == {
        "experiments/build_submission_sensitivity_claims.py",
        "experiments/build_submission_sensitivity_table.py",
    }
    assert all(len(value) == 64 for value in metadata["source_sha256"].values())


def test_claim_summary_does_not_treat_numerical_noise_as_improvement():
    from experiments.build_submission_sensitivity_claims import summarize_rows

    rows = _rows()
    rows[0]["aggregate_peak_change_percent"] = -1e-12
    rows[0]["minimum_provider_qos_change"] = 1e-12

    result = summarize_rows(rows)

    assert not result["aggregate_peak_change_percent"]["all_improve"]
    assert not result["minimum_provider_qos_change"]["all_improve"]


def test_claim_summary_rejects_non_finite_regret():
    from experiments.build_submission_sensitivity_claims import summarize_rows

    rows = _rows()
    rows[0]["dynamic_full_max_regret"] = float("nan")

    with pytest.raises(ValueError, match="dynamic_full_max_regret"):
        summarize_rows(rows)
