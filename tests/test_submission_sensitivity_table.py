from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


SCENARIOS = (
    "baseline",
    "capacity_low",
    "capacity_high",
    "price_sensitivity_low",
    "price_sensitivity_high",
    "migration_cost_low",
    "migration_cost_high",
    "qos_threshold_low",
    "qos_threshold_high",
)


def _summary() -> dict:
    rows = []
    for index, scenario in enumerate(SCENARIOS):
        rows.append({
            "scenario": scenario,
            "uniform_full_max_regret": 1e-12,
            "dynamic_full_max_regret": 2e-12 + index * 1e-13,
            "maximum_joint_residual": 1e-9,
            "aggregate_peak_change_percent": -12.0 + index,
            "maximum_provider_utilization_change_percent": -15.0 + index,
            "minimum_provider_qos_change": 0.06 - index * 0.001,
            "market_profit_change_percent": -3.0 + index * 0.2,
        })
    return {
        "metadata": {
            "provider_candidate_count": 1576,
            "scenario_count": 9,
        },
        "rows": rows,
    }


def test_build_sensitivity_table_contains_all_cases_and_metrics():
    from experiments.build_submission_sensitivity_table import build_table

    source = build_table(_summary(), source_sha256="a" * 64)

    assert "% Source SHA-256: " + "a" * 64 in source
    assert "\\label{tab:resolved_sensitivity}" in source
    assert "Capacity $-15\\%$" in source
    assert "Utility coefficient $-20\\%$" in source
    assert "QoS threshold $+0.05$" in source
    assert "Maximum regret" in source
    assert "Finite-game sensitivity results" in source
    assert "checks every declared unilateral provider deviation" in source
    assert "Fully re-solved" not in source
    assert "utilisation" not in source
    assert "utilization" in source
    assert r"\setlength{\tabcolsep}{2.25pt}" in source
    assert source.count(" \\\\") == 10


def test_build_sensitivity_table_rejects_wrong_order_and_count():
    from experiments.build_submission_sensitivity_table import build_table

    summary = _summary()
    summary["rows"][1], summary["rows"][2] = summary["rows"][2], summary["rows"][1]
    with pytest.raises(ValueError, match="scenario order"):
        build_table(summary, source_sha256="a" * 64)

    summary = _summary()
    summary["metadata"]["scenario_count"] = 8
    with pytest.raises(ValueError, match="scenario count"):
        build_table(summary, source_sha256="a" * 64)
