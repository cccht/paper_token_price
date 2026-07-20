from pathlib import Path
import json
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def _game(metrics, *, candidates, regret=0.0, relative=0.0, pairs=12):
    return {
        "candidate_count": candidates,
        "row_mix": [1.0],
        "col_mix": [1.0],
        "evaluated_pairs": pairs,
        "full_max_regret": regret,
        "relative_full_max_regret": relative,
        "maximum_joint_residual": 1e-10,
        "expected_metrics": metrics,
    }


def test_equilibrium_macros_are_derived_from_artifact_values():
    from experiments.build_submission_result_macros import build_macros

    uniform_metrics = {
        "aggregate_peak_load": 200.0,
        "aggregate_peak_to_average": 1.6,
        "maximum_provider_utilization": 1.2,
        "minimum_provider_qos": 0.8,
        "temporal_moved_fraction": 0.2,
        "firm_A_profit": 60.0,
        "firm_B_profit": 40.0,
        "intermediary_profit": 20.0,
        "system_profit": 100.0,
    }
    dynamic_metrics = {
        "aggregate_peak_load": 180.0,
        "aggregate_peak_to_average": 1.44,
        "maximum_provider_utilization": 1.0,
        "minimum_provider_qos": 0.9,
        "temporal_moved_fraction": 0.3,
        "firm_A_profit": 57.0,
        "firm_B_profit": 42.0,
        "intermediary_profit": 21.0,
        "system_profit": 99.0,
    }
    equilibrium = {
        "uniform": _game(uniform_metrics, candidates=12),
        "dynamic": _game(dynamic_metrics, candidates=2380, pairs=1234),
        "comparison": {
            "aggregate_peak_load_change_percent": -10.0,
            "maximum_provider_utilization_change_percent": -16.666,
            "minimum_provider_qos_change": 0.1,
            "system_profit_change_percent": -1.0,
        },
    }

    source = build_macros(equilibrium)

    assert r"\newcommand{\ProviderCandidateCount}{2380}" in source
    assert r"\newcommand{\DynamicAggregatePeak}{180.000}" in source
    assert r"\newcommand{\AggregatePeakChangePercent}{-10.00}" in source
    assert r"\newcommand{\AggregatePeakReductionPercent}{10.00}" in source
    assert r"\newcommand{\MaximumUtilisationReductionPercent}{16.67}" in source
    assert r"\newcommand{\DynamicEvaluatedPairs}{1,234}" in source
    assert r"\newcommand{\UniformPeakToAverage}{1.600}" in source
    assert r"\newcommand{\DynamicPeakToAverage}{1.440}" in source
    assert r"\newcommand{\MovedFractionChange}{0.1000}" in source
    assert r"\newcommand{\ProviderAProfitChangePercent}{-5.00}" in source
    assert r"\newcommand{\UniformProviderBProfit}{40.000}" in source
    assert r"\newcommand{\ProviderBProfitChangePercent}{5.00}" in source
    assert r"\newcommand{\UniformIntermediaryProfit}{20.000}" in source
    assert r"\newcommand{\IntermediaryProfitChangePercent}{5.00}" in source


def test_macro_paths_target_submission_artifacts():
    from experiments import build_submission_result_macros as module

    assert module.EQUILIBRIUM_PATH.name == "spatiotemporal_equilibrium_submission.json"
    assert module.OUTPUT_PATH.name == "submission_result_macros.tex"
    assert module.UNIFORM_OFFGRID_PATH.name == (
        "uniform_offgrid_sensitivity_submission.json"
    )
    assert module.INTERMEDIARY_PAYOFF_SENSITIVITY_PATH.name == (
        "intermediary_payoff_sensitivity_submission.json"
    )


def test_macro_builder_rejects_audit_from_another_equilibrium(tmp_path):
    from experiments.build_submission_result_macros import _validated_audit

    path = tmp_path / "audit.json"
    path.write_text(
        '{"metadata": {"equilibrium_sha256": "old"}}', encoding="utf-8"
    )

    with pytest.raises(ValueError, match="equilibrium SHA-256"):
        _validated_audit(path, "current")


def test_macro_builder_allows_missing_optional_audit(tmp_path):
    from experiments.build_submission_result_macros import _validated_audit

    assert _validated_audit(tmp_path / "missing.json", "current") is None


def _write_audit(tmp_path, name, payload):
    path = tmp_path / name
    payload["metadata"] = {"equilibrium_sha256": "current"}
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_macro_builder_rejects_offgrid_regret_above_gate(tmp_path):
    from experiments.build_submission_result_macros import _validated_audit

    path = _write_audit(tmp_path, "spatiotemporal_offgrid_diagnostic_submission.json", {
        "players": {
            "firm_A": {
                "relative_offgrid_regret": 0.0051,
                "all_joint_converged": True,
                "maximum_joint_residual": 1e-9,
            },
            "firm_B": {
                "relative_offgrid_regret": 0.0,
                "all_joint_converged": True,
                "maximum_joint_residual": 1e-9,
            },
        }
    })

    with pytest.raises(ValueError, match="off-grid quality gate"):
        _validated_audit(path, "current")


def test_macro_builder_rejects_material_intermediary_improvement(tmp_path):
    from experiments.build_submission_result_macros import _validated_audit

    path = _write_audit(tmp_path, "intermediary_globality_audit_submission.json", {
        "maximum_relative_profit_improvement": 0.0011,
        "maximum_joint_residual": 1e-9,
    })

    with pytest.raises(ValueError, match="intermediary quality gate"):
        _validated_audit(path, "current")


@pytest.mark.parametrize(
    ("name", "payload"),
    [
        (
            "intermediary_globality_audit_submission.json",
            {
                "maximum_relative_profit_improvement": 0.0,
                "maximum_joint_residual": 1e-9,
            },
        ),
        (
            "fixed_point_multistart_audit_submission.json",
            {
                "all_starts_converged": True,
                "maximum_residual": 1e-9,
                "maximum_qos_span": 1e-9,
                "maximum_routing_span": 1e-9,
            },
        ),
    ],
)
def test_macro_builder_requires_full_active_profile_coverage(tmp_path, name, payload):
    from experiments.build_submission_result_macros import _validated_audit

    path = _write_audit(tmp_path, name, payload)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["metadata"]["covered_probability_mass"] = 0.999
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="coverage"):
        _validated_audit(path, "current")


def test_macro_builder_rejects_unstable_fixed_point_audit(tmp_path):
    from experiments.build_submission_result_macros import _validated_audit

    path = _write_audit(tmp_path, "fixed_point_multistart_audit_submission.json", {
        "all_starts_converged": True,
        "maximum_residual": 1e-9,
        "maximum_qos_span": 2e-7,
        "maximum_routing_span": 1e-9,
    })

    with pytest.raises(ValueError, match="fixed-point quality gate"):
        _validated_audit(path, "current")
