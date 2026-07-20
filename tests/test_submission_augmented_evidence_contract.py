from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _sensitivity_summary() -> dict:
    from experiments.build_submission_sensitivity_table import SCENARIO_ORDER

    rows = []
    for scenario in SCENARIO_ORDER:
        rows.append({
            "scenario": scenario,
            "uniform_full_max_regret": 1e-12,
            "dynamic_full_max_regret": 2e-12,
            "maximum_joint_residual": 1e-9,
            "aggregate_peak_change_percent": -10.0,
            "maximum_provider_utilization_change_percent": -12.0,
            "minimum_provider_qos_change": 0.04,
            "market_profit_change_percent": -1.0,
        })
    return {
        "metadata": {"scenario_count": 9, "provider_candidate_count": 1576},
        "rows": rows,
    }


def test_submission_gate_declares_augmented_common_candidate_counts():
    from experiments.submission_evidence_gates import GateThresholds

    gate = GateThresholds()

    assert gate.uniform_candidate_count == 800
    assert gate.provider_candidate_count == 1576


def test_current_submission_docs_use_augmented_scope_and_baseline_results():
    manifest = (ROOT / "ARTIFACT_MANIFEST.md").read_text(encoding="utf-8")
    reproducibility = (ROOT / "REPRODUCIBILITY.md").read_text(encoding="utf-8")
    highlights = (
        ROOT / "docs/submission/simpat_highlights_final_2026-07-16.txt"
    ).read_text(encoding="utf-8")
    author_actions = (
        ROOT / "docs/submission/smpt_author_actions_2026-07-16.md"
    ).read_text(encoding="utf-8")

    for source in (manifest, reproducibility):
        assert "800/1,576" in source
        assert "788-rule provider candidate set" not in source
        assert "12/788 game sizes" not in source
    assert "70a3b64050c2b0621bbcf0c5a418c43ba554f61b3ee10c2ca4d48fbf26bed226" in manifest
    assert "all eight local sensitivity" in manifest
    assert "perturbations have passed" in manifest
    assert "baseline artifact's recorded source hashes no longer pass" in manifest
    assert "Its 20 recorded numerical source hashes pass" not in manifest
    assert "one of eight local sensitivity" not in manifest
    assert "two of eight local sensitivity" not in manifest
    assert "three of eight local sensitivity" not in manifest
    assert "four of eight local sensitivity" not in manifest
    assert "five of eight local sensitivity" not in manifest
    assert "six of eight local sensitivity" not in manifest
    assert "seven of eight local sensitivity" not in manifest
    assert "three red gates" not in manifest
    assert "1,576 rules" in highlights
    assert "12.50%" in highlights
    assert "rises by 2.23%" in highlights
    assert all(len(line) <= 85 for line in highlights.splitlines())
    assert "有限 1,576 候选" in author_actions


def test_current_evidence_map_uses_augmented_baseline_and_sensitivity_status():
    evidence_map = (
        ROOT / "docs/reviews/smpt_submission_evidence_map_2026-07-14.md"
    ).read_text(encoding="utf-8")

    assert "70a3b64050c2b0621bbcf0c5a418c43ba554f61b3ee10c2ca4d48fbf26bed226" in evidence_map
    assert "完整 800 条零斜率规则" in evidence_map
    assert "共同 1,576 条规则" in evidence_map
    assert (
        "`capacity_low`、`capacity_high`、`price_sensitivity_low`、"
        "`price_sensitivity_high`、`migration_cost_low`、"
        "`migration_cost_high`、`qos_threshold_low` 和 `qos_threshold_high`"
    ) in evidence_map
    assert "其余 1 个场景正在续算或排队" not in evidence_map
    assert "当前 `uniform` 仅 12 个零斜率候选" not in evidence_map
    assert "当前支持 baseline plus eight verified perturbations" in evidence_map
    assert "当前只支持 five verified" not in evidence_map
    assert "当前只支持 six verified" not in evidence_map
    assert "当前只支持 seven verified" not in evidence_map


def test_active_profile_count_is_derived_from_positive_mixes():
    from experiments.submission_evidence_gates import active_profile_count

    game = {
        "row_mix": [0.25, 0.75, 0.0],
        "col_mix": [0.4, 0.6, 0.0],
    }

    assert active_profile_count(game) == 4


def test_sensitivity_table_accepts_augmented_candidate_scope():
    from experiments.build_submission_sensitivity_table import build_table

    source = build_table(_sensitivity_summary(), source_sha256="a" * 64)

    assert "common 1,576-candidate set" in source


def test_sensitivity_claims_accept_augmented_candidate_scope():
    from experiments.build_submission_sensitivity_claims import build_claims

    claims = build_claims(_sensitivity_summary(), source_sha256="b" * 64)

    assert claims["metadata"]["provider_candidate_count"] == 1576


def test_submission_gate_declares_augmented_audit_paths():
    from experiments import submission_evidence_gates as module

    assert module.UNIFORM_OFFGRID_PATH.name == (
        "uniform_offgrid_sensitivity_submission.json"
    )
    assert module.INTERMEDIARY_PAYOFF_SENSITIVITY_PATH.name == (
        "intermediary_payoff_sensitivity_submission.json"
    )


def test_uniform_offgrid_gate_requires_all_nine_scenarios():
    from experiments.build_submission_sensitivity_table import SCENARIO_ORDER
    from experiments.submission_evidence_gates import (
        GateThresholds,
        validate_uniform_offgrid_sensitivity,
    )

    player = {
        "relative_offgrid_regret": 0.001,
        "all_joint_converged": True,
        "maximum_joint_residual": 1e-9,
        "maximum_active_support_payoff_error": 1e-10,
    }
    artifact = {
        "metadata": {
            "baseline_sha256": "a" * 64,
            "samples_per_player": 1024,
            "seed": 20260718,
            "scenario_count": 9,
        },
        "scenarios": [
            {
                "scenario": scenario,
                "players": {"firm_A": player, "firm_B": player},
            }
            for scenario in SCENARIO_ORDER
        ],
    }

    result = validate_uniform_offgrid_sensitivity(
        artifact,
        expected_hash="a" * 64,
        thresholds=GateThresholds(),
    )

    assert result["passed"] is True
    artifact["scenarios"].pop()
    try:
        validate_uniform_offgrid_sensitivity(
            artifact,
            expected_hash="a" * 64,
            thresholds=GateThresholds(),
        )
    except ValueError as error:
        assert "nine" in str(error)
    else:
        raise AssertionError("missing uniform off-grid scenario was accepted")


def test_provider_payoff_sensitivity_gate_checks_coverage_and_residual():
    from experiments.submission_evidence_gates import (
        GateThresholds,
        validate_intermediary_payoff_sensitivity,
    )

    artifact = {
        "metadata": {"equilibrium_sha256": "c" * 64},
        "summary": {
            "covered_probability_mass": 1.0,
            "maximum_active_support_regret": 0.9,
            "maximum_joint_residual": 1e-9,
        },
    }

    result = validate_intermediary_payoff_sensitivity(
        artifact,
        expected_hash="c" * 64,
        thresholds=GateThresholds(),
    )

    assert result["passed"] is True
    artifact["summary"]["covered_probability_mass"] = 0.99
    try:
        validate_intermediary_payoff_sensitivity(
            artifact,
            expected_hash="c" * 64,
            thresholds=GateThresholds(),
        )
    except ValueError as error:
        assert "coverage" in str(error)
    else:
        raise AssertionError("incomplete provider-payoff coverage was accepted")
