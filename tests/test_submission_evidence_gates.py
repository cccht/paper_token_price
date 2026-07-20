import copy
import csv
import hashlib
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


BASELINE_HASH = "a" * 64
ROOT = Path(__file__).resolve().parents[1]
GATE_SOURCE = ROOT / "experiments" / "submission_evidence_gates.py"
REAL_EQUILIBRIUM = (
    ROOT
    / "artifacts/peak_shaving/20260712_expanded_response"
    / "spatiotemporal_equilibrium_submission.json"
)
REAL_BURST_METADATA = (
    ROOT
    / "data/processed/burstgpt_d895a53b_8period"
    / "burstgpt_8period_load_metadata.json"
)
REAL_BURST_PROFILE = REAL_BURST_METADATA.with_name(
    "burstgpt_8period_load_profile.csv"
)
REAL_QOS_CALIBRATION = (
    ROOT / "artifacts/peak_shaving/20260712_final/qos_calibration.json"
)


def _real_input_anchors() -> tuple[dict, dict, list[dict], dict]:
    equilibrium = json.loads(REAL_EQUILIBRIUM.read_text(encoding="utf-8"))
    load_metadata = json.loads(REAL_BURST_METADATA.read_text(encoding="utf-8"))
    with REAL_BURST_PROFILE.open(encoding="utf-8", newline="") as stream:
        load_rows = list(csv.DictReader(stream))
    qos = json.loads(REAL_QOS_CALIBRATION.read_text(encoding="utf-8"))
    return equilibrium, load_metadata, load_rows, qos


def _offgrid() -> dict:
    player = {
        "relative_offgrid_regret": 0.001,
        "maximum_joint_residual": 1e-9,
        "maximum_active_support_payoff_error": 1e-8,
        "all_joint_converged": True,
        "minimum_successful_local_runs": 1,
    }
    return {
        "metadata": {
            "equilibrium_sha256": BASELINE_HASH,
            "provider_candidate_count": 1576,
            "samples_per_player": 1024,
            "seed": 20260714,
        },
        "players": {"firm_A": copy.deepcopy(player), "firm_B": copy.deepcopy(player)},
    }


def _synthetic_sensitivity_game(*, candidate_count: int, dynamic: bool) -> dict:
    peak = 140.0 if dynamic else 150.0
    utilization = 0.8 if dynamic else 0.9
    qos = 0.97 if dynamic else 0.95
    moved = 0.31 if dynamic else 0.30
    profits = (11.0, 19.0, 6.0) if dynamic else (10.0, 20.0, 5.0)
    aggregate = [137.5] * 8
    return {
        "candidate_count": candidate_count,
        "full_max_regret": 1e-10,
        "relative_full_max_regret": 1e-12,
        "maximum_joint_residual": 1e-9,
        "evaluated_pairs": 1,
        "full_grid_verified": True,
        "expected_metrics": {
            "firm_A_profit": profits[0],
            "firm_B_profit": profits[1],
            "intermediary_profit": profits[2],
            "system_profit": sum(profits),
            "aggregate_peak_load": peak,
            "aggregate_peak_to_average": peak / 137.5,
            "maximum_provider_utilization": utilization,
            "provider_utilization_imbalance": 0.1,
            "minimum_provider_qos": qos,
            "temporal_moved_fraction": moved,
            "total_demand": 1100.0,
        },
        "expected_profiles": {
            "aggregate_load": aggregate,
            "provider_utilization": [[0.7] * 8, [utilization] * 8],
            "provider_qos": [[1.0] * 8, [qos] * 8],
            "channel_demand": [[40.0] * 8, [50.0] * 8, [47.5] * 8],
            "destination_demand_by_type": [[55.0] * 8, [82.5] * 8],
            "retail_price": [0.8] * 8,
            "direct_price": [[0.7] * 8, [0.7] * 8],
            "wholesale_price": [[0.4] * 8, [0.4] * 8],
            "routing": [[0.5] * 8, [0.5] * 8],
        },
        "row_mix": [1.0],
        "col_mix": [1.0],
        "row_support_vectors": [[0.25, 0.0, 0.45, 0.0]],
        "col_support_vectors": [[0.25, 0.0, 0.45, 0.0]],
        "row_support_indices": [0],
        "col_support_indices": [0],
        "active_profiles": [{"weight": 1.0, "joint_residual": 1e-9}],
    }


def _sensitivity() -> dict:
    uniform = _synthetic_sensitivity_game(candidate_count=800, dynamic=False)
    dynamic = _synthetic_sensitivity_game(candidate_count=1576, dynamic=True)
    uniform_metrics, dynamic_metrics = (
        uniform["expected_metrics"], dynamic["expected_metrics"]
    )
    comparison = {}
    for metric in (
        "aggregate_peak_load", "maximum_provider_utilization",
        "minimum_provider_qos", "system_profit", "temporal_moved_fraction",
    ):
        change = dynamic_metrics[metric] - uniform_metrics[metric]
        comparison[f"{metric}_change"] = change
        comparison[f"{metric}_change_percent"] = (
            100.0 * change / uniform_metrics[metric]
        )
    return {
        "metadata": {
            "full_candidate_count": 1576,
            "baseline_equilibrium": {"sha256": BASELINE_HASH},
            "source_sha256": {
                "experiments/submission_evidence_gates.py": hashlib.sha256(
                    GATE_SOURCE.read_bytes()
                ).hexdigest(),
            },
        },
        "scenario": {
            "capacity_scale": 0.85,
            "price_sensitivity_scale": 1.0,
            "migration_cost_scale": 1.0,
            "qos_threshold_shift": 0.0,
        },
        "candidate_grid": [
            [0.25 + index * 1e-6, 0.0, 0.45, 0.0]
            for index in range(1576)
        ],
        "intermediary_response": {
            "method": "continuous_multistart",
            "uniform": {"retail_slope_bounds": [0.0, 0.0]},
            "dynamic": {"retail_slope_bounds": [-1.0, 1.0]},
        },
        "uniform": uniform,
        "dynamic": dynamic,
        "comparison": comparison,
    }


def _branch_audit() -> dict:
    return {
        "metadata": {
            "baseline_sha256": BASELINE_HASH,
            "successful_starts": 65,
        },
        "candidate_count": 1576,
        "branch_count": 1,
        "single_recovered_branch": True,
        "branches": [{"full_candidate": {"max_regret": 1e-10}}],
    }


def _linked_metadata() -> dict:
    return {
        "equilibrium_sha256": BASELINE_HASH,
        "covered_probability_mass": 1.0,
        "source_sha256": {
            "experiments/submission_evidence_gates.py": hashlib.sha256(
                GATE_SOURCE.read_bytes()
            ).hexdigest(),
        },
    }


def _fixed_point_audit() -> dict:
    return {
        "metadata": _linked_metadata(),
        "all_starts_converged": True,
        "maximum_residual": 1e-9,
        "maximum_qos_span": 2e-9,
        "maximum_routing_span": 3e-9,
    }


def _intermediary_audit() -> dict:
    return {
        "metadata": _linked_metadata(),
        "maximum_relative_profit_improvement": 2e-4,
        "maximum_joint_residual": 1e-9,
    }


def _mechanism_audit() -> dict:
    metadata = _linked_metadata()
    metadata.pop("covered_probability_mass")
    rows = []
    for policy in ("uniform", "dynamic"):
        for mechanism in ("neither", "temporal_only", "spatial_only", "combined"):
            rows.append({
                "policy": policy,
                "mechanism": mechanism,
                "probability_mass": 1.0,
                "all_converged": True,
                "maximum_joint_residual": 1e-9,
            })
    return {
        "metadata": metadata,
        "mechanisms": {
            "neither": [False, False],
            "temporal_only": [True, False],
            "spatial_only": [False, True],
            "combined": [True, True],
        },
        "rows": rows,
    }


def _distribution_audit() -> dict:
    metadata = _linked_metadata()
    metadata.pop("covered_probability_mass")
    metadata["quantiles"] = [0.05, 0.5, 0.95]
    game = {
        "probability_mass": 1.0,
        "all_joint_converged": True,
        "maximum_joint_residual": 1e-9,
        "maximum_expected_metric_reconstruction_error": 1e-12,
    }
    uniform = copy.deepcopy(game)
    uniform["active_profile_count"] = 100
    dynamic = copy.deepcopy(game)
    dynamic["active_profile_count"] = 676
    return {"metadata": metadata, "uniform": uniform, "dynamic": dynamic}


def _price_shape_audit() -> dict:
    metadata = _linked_metadata()
    metadata.pop("covered_probability_mass")
    uniform = {
        "profile_count": 100,
        "probability_mass": 1.0,
        "all_converged": True,
        "maximum_joint_residual": 1e-9,
    }
    flattened = {
        "profile_count": 676,
        "probability_mass": 1.0,
        "all_converged": True,
        "maximum_joint_residual": 1e-9,
    }
    values = {
        "aggregate_peak_load": (220.0, 210.0, 195.0),
        "maximum_provider_utilization": (1.4, 1.3, 1.2),
        "minimum_provider_qos": (0.89, 0.92, 0.96),
        "system_profit": (2000.0, 1950.0, 1920.0),
    }
    components = []
    for metric, (uniform_value, flattened_value, dynamic_value) in values.items():
        overall = dynamic_value - uniform_value
        shape = dynamic_value - flattened_value
        remainder = flattened_value - uniform_value
        components.append({
            "metric": metric,
            "uniform_equilibrium": uniform_value,
            "flattened_dynamic_profiles": flattened_value,
            "dynamic_equilibrium": dynamic_value,
            "overall_change": overall,
            "shape_change": shape,
            "level_and_mix_remainder": remainder,
            "identity_error": overall - shape - remainder,
        })
    return {
        "metadata": metadata,
        "uniform_flattening_check": {"maximum_absolute_error": 0.0, **uniform},
        "mean_flattened_dynamic_profiles": flattened,
        "components": components,
    }


def _candidate_manifest(tmp_path: Path) -> dict:
    seed = tmp_path / "seed.json"
    seed.write_text("{}\n", encoding="utf-8")
    source = tmp_path / "manifest_builder.py"
    source.write_text("VALUE = 1\n", encoding="utf-8")
    return {
        "metadata": {
            "final_equilibrium_sha256": BASELINE_HASH,
            "continuation_seed_path": seed.name,
            "continuation_seed_sha256": hashlib.sha256(seed.read_bytes()).hexdigest(),
            "source_sha256": {
                source.name: hashlib.sha256(source.read_bytes()).hexdigest(),
            },
        },
        "components": [
            {"added_unique_count": added, "cumulative_unique_count": cumulative}
            for added, cumulative in zip(
                (800, 378, 120, 64, 27, 100, 69, 18),
                (800, 1178, 1298, 1362, 1389, 1489, 1558, 1576),
            )
        ],
        "verification": {
            "reference_support_entry_count": 52,
            "reference_unique_count": 48,
            "component_union_count": 1576,
            "reconstructed_candidate_count": 1576,
            "final_candidate_count": 1576,
            "exact_elementwise_match": True,
        },
    }


def _sensitivity_summary() -> dict:
    from experiments.build_submission_sensitivity_table import SCENARIO_ORDER

    rows = []
    for index, scenario in enumerate(SCENARIO_ORDER):
        rows.append({
            "scenario": scenario,
            "uniform_full_max_regret": 1e-12,
            "dynamic_full_max_regret": 2e-12,
            "maximum_joint_residual": 1e-9,
            "aggregate_peak_change_percent": -12.0 + 0.1 * index,
            "maximum_provider_utilization_change_percent": -15.0 + 0.1 * index,
            "minimum_provider_qos_change": 0.05 + 0.001 * index,
            "market_profit_change_percent": -2.0 + index,
        })
    return {
        "metadata": {"scenario_count": 9, "provider_candidate_count": 1576},
        "rows": rows,
    }


def _linked_sensitivity_summary() -> tuple[dict, dict[str, dict], dict]:
    from experiments.run_submission_spatiotemporal_sensitivity import (
        SCENARIOS,
        SOLVER_KEYS,
        _summary_row,
    )

    baseline = _sensitivity()
    baseline["scenario"] = {
        "capacity_scale": 1.0,
        "price_sensitivity_scale": 1.0,
        "migration_cost_scale": 1.0,
        "qos_threshold_shift": 0.0,
    }
    artifacts, rows = {}, []
    for name, definition in SCENARIOS.items():
        artifact = _sensitivity()
        artifact["scenario"] = copy.deepcopy(baseline["scenario"])
        artifact["scenario"].update({
            key: definition[key] for key in SOLVER_KEYS if key in definition
        })
        artifacts[name] = artifact
        rows.append(_summary_row(name, definition, artifact))
    runner = ROOT / "experiments/run_submission_spatiotemporal_sensitivity.py"
    summary = {
        "metadata": {
            "baseline_sha256": BASELINE_HASH,
            "provider_candidate_count": 1576,
            "intermediary_response_method": "continuous_multistart",
            "scenario_count": 9,
            "source_sha256": {
                str(runner.relative_to(ROOT)): hashlib.sha256(
                    runner.read_bytes()
                ).hexdigest(),
            },
        },
        "scenario_definitions": copy.deepcopy(SCENARIOS),
        "rows": [
            _summary_row(
                "baseline", {"group": "baseline", "value": 1.0}, baseline
            ),
            *rows,
        ],
    }
    return baseline, artifacts, summary


def _sensitivity_claims(summary: dict) -> tuple[dict, str]:
    from experiments.build_submission_sensitivity_claims import build_claims

    source = json.dumps(summary, sort_keys=True).encode()
    digest = hashlib.sha256(source).hexdigest()
    return build_claims(summary, source_sha256=digest), digest


def test_source_hash_gate_accepts_current_file_and_rejects_stale_hash(tmp_path):
    from experiments.submission_evidence_gates import validate_source_hashes

    source = tmp_path / "model.py"
    source.write_text("VALUE = 1\n", encoding="utf-8")
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    artifact = {"metadata": {"source_sha256": {"model.py": digest}}}

    assert validate_source_hashes(artifact, root=tmp_path)["passed"]

    artifact["metadata"]["source_sha256"]["model.py"] = "0" * 64
    with pytest.raises(ValueError, match="source SHA-256 mismatch"):
        validate_source_hashes(artifact, root=tmp_path)


def test_submission_gates_accept_valid_artifacts(tmp_path):
    from experiments.submission_evidence_gates import (
        validate_fixed_point_audit,
        validate_distribution_audit,
        validate_intermediary_audit,
        validate_mechanism_audit,
        validate_price_shape_audit,
        validate_branch_audit,
        validate_candidate_manifest,
        validate_offgrid,
        validate_sensitivity_claims,
        validate_sensitivity_scenario,
    )

    assert validate_offgrid(_offgrid(), expected_hash=BASELINE_HASH)["passed"]
    assert validate_branch_audit(
        _branch_audit(), expected_hash=BASELINE_HASH
    )["passed"]
    assert validate_candidate_manifest(
        _candidate_manifest(tmp_path), expected_hash=BASELINE_HASH, root=tmp_path
    )["passed"]
    assert validate_fixed_point_audit(
        _fixed_point_audit(), expected_hash=BASELINE_HASH
    )["passed"]
    assert validate_distribution_audit(
        _distribution_audit(), expected_hash=BASELINE_HASH
    )["passed"]
    assert validate_intermediary_audit(
        _intermediary_audit(), expected_hash=BASELINE_HASH
    )["passed"]
    assert validate_mechanism_audit(
        _mechanism_audit(), expected_hash=BASELINE_HASH
    )["passed"]
    assert validate_price_shape_audit(
        _price_shape_audit(), expected_hash=BASELINE_HASH
    )["passed"]
    assert validate_sensitivity_scenario(
        "capacity_low", _sensitivity(), expected_hash=BASELINE_HASH
    )["passed"]
    summary = _sensitivity_summary()
    claims, digest = _sensitivity_claims(summary)
    assert validate_sensitivity_claims(
        claims, summary=summary, expected_summary_hash=digest
    )["passed"]


def test_sensitivity_claim_gate_rejects_stale_hash_and_changed_range():
    from experiments.submission_evidence_gates import validate_sensitivity_claims

    summary = _sensitivity_summary()
    claims, digest = _sensitivity_claims(summary)
    claims["metadata"]["source_summary_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="summary SHA-256"):
        validate_sensitivity_claims(
            claims, summary=summary, expected_summary_hash=digest
        )

    claims, digest = _sensitivity_claims(summary)
    claims["claims"]["aggregate_peak_change_percent"]["maximum"] = -1.0
    with pytest.raises(ValueError, match="do not match"):
        validate_sensitivity_claims(
            claims, summary=summary, expected_summary_hash=digest
        )


def test_sensitivity_summary_gate_matches_all_underlying_artifacts():
    from experiments.submission_evidence_gates import validate_sensitivity_summary

    baseline, artifacts, summary = _linked_sensitivity_summary()

    assert validate_sensitivity_summary(
        summary,
        equilibrium=baseline,
        scenario_artifacts=artifacts,
        expected_hash=BASELINE_HASH,
    )["passed"]


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (
            lambda summary: summary["rows"][1].update(
                aggregate_peak_change_percent=0.0
            ),
            "summary rows",
        ),
        (
            lambda summary: summary["metadata"].update(
                baseline_sha256="b" * 64
            ),
            "baseline SHA-256",
        ),
        (
            lambda summary: summary["scenario_definitions"]["capacity_low"].update(
                value=0.9
            ),
            "scenario definitions",
        ),
        (
            lambda summary: summary["metadata"]["source_sha256"].update({
                "experiments/run_submission_spatiotemporal_sensitivity.py": "0" * 64
            }),
            "source SHA-256",
        ),
    ],
)
def test_sensitivity_summary_gate_rejects_broken_links(mutation, message):
    from experiments.submission_evidence_gates import validate_sensitivity_summary

    baseline, artifacts, summary = _linked_sensitivity_summary()
    mutation(summary)

    with pytest.raises(ValueError, match=message):
        validate_sensitivity_summary(
            summary,
            equilibrium=baseline,
            scenario_artifacts=artifacts,
            expected_hash=BASELINE_HASH,
        )


def test_total_evidence_report_includes_sensitivity_summary_gate():
    source = GATE_SOURCE.read_text(encoding="utf-8")

    assert 'checks["sensitivity_summary"] = validate_sensitivity_summary(' in source


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("relative_offgrid_regret", 0.006, "relative off-grid regret"),
        ("maximum_joint_residual", 2e-8, "joint residual"),
        ("maximum_active_support_payoff_error", 2e-6, "support payoff error"),
        ("all_joint_converged", False, "non-converged"),
        ("minimum_successful_local_runs", 0, "successful local run"),
    ],
)
def test_offgrid_gate_rejects_failed_player_checks(field, value, message):
    from experiments.submission_evidence_gates import validate_offgrid

    artifact = _offgrid()
    artifact["players"]["firm_B"][field] = value

    with pytest.raises(ValueError, match=message):
        validate_offgrid(artifact, expected_hash=BASELINE_HASH)


def test_sensitivity_gate_rejects_stale_hash_high_regret_and_residual():
    from experiments.submission_evidence_gates import validate_sensitivity_scenario

    artifact = _sensitivity()
    artifact["metadata"]["baseline_equilibrium"]["sha256"] = "b" * 64
    with pytest.raises(ValueError, match="baseline SHA-256"):
        validate_sensitivity_scenario(
            "capacity_low", artifact, expected_hash=BASELINE_HASH
        )

    artifact = _sensitivity()
    artifact["dynamic"]["full_max_regret"] = 2e-7
    with pytest.raises(ValueError, match="full-candidate regret"):
        validate_sensitivity_scenario(
            "capacity_low", artifact, expected_hash=BASELINE_HASH
        )

    artifact = _sensitivity()
    artifact["uniform"]["maximum_joint_residual"] = 2e-8
    with pytest.raises(ValueError, match="joint residual"):
        validate_sensitivity_scenario(
            "capacity_low", artifact, expected_hash=BASELINE_HASH
        )


def test_sensitivity_gate_rejects_stale_source_hash():
    from experiments.submission_evidence_gates import validate_sensitivity_scenario

    artifact = _sensitivity()
    artifact["metadata"]["source_sha256"][
        "experiments/submission_evidence_gates.py"
    ] = "0" * 64

    with pytest.raises(ValueError, match="source SHA-256 mismatch"):
        validate_sensitivity_scenario(
            "capacity_low", artifact, expected_hash=BASELINE_HASH
        )


def test_sensitivity_gate_rejects_mislabeled_scenario_parameters():
    from experiments.submission_evidence_gates import validate_sensitivity_scenario

    artifact = _sensitivity()
    artifact["scenario"]["capacity_scale"] = 1.15

    with pytest.raises(ValueError, match="scenario parameters"):
        validate_sensitivity_scenario(
            "capacity_low", artifact, expected_hash=BASELINE_HASH
        )


@pytest.mark.parametrize("field", ["candidate_grid", "intermediary_response"])
def test_sensitivity_gate_requires_the_baseline_strategy_contract(field):
    from experiments.submission_evidence_gates import validate_sensitivity_scenario

    artifact = _sensitivity()
    baseline = {
        "candidate_grid": copy.deepcopy(artifact["candidate_grid"]),
        "intermediary_response": copy.deepcopy(artifact["intermediary_response"]),
    }
    if field == "candidate_grid":
        artifact[field][0][0] = 0.9
    else:
        artifact[field]["method"] = "finite_grid"

    with pytest.raises(ValueError, match="baseline strategy contract"):
        validate_sensitivity_scenario(
            "capacity_low",
            artifact,
            expected_hash=BASELINE_HASH,
            expected_baseline=baseline,
        )


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (
            lambda artifact: artifact["uniform"].update(candidate_count=799),
            "candidate count",
        ),
        (
            lambda artifact: artifact["dynamic"]["expected_metrics"].update(
                total_demand=1099.0
            ),
            "total demand",
        ),
    ],
)
def test_sensitivity_gate_checks_game_size_and_demand_conservation(
    mutation, message
):
    from experiments.submission_evidence_gates import validate_sensitivity_scenario

    artifact = _sensitivity()
    mutation(artifact)

    with pytest.raises(ValueError, match=message):
        validate_sensitivity_scenario(
            "capacity_low", artifact, expected_hash=BASELINE_HASH
        )


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (
            lambda artifact: artifact["dynamic"]["expected_metrics"].update(
                system_profit=100.0
            ),
            "profit accounting",
        ),
        (
            lambda artifact: artifact["comparison"].update(
                aggregate_peak_load_change=0.0
            ),
            "comparison arithmetic",
        ),
        (
            lambda artifact: artifact["dynamic"]["expected_profiles"][
                "aggregate_load"
            ].pop(),
            "expected profile length",
        ),
        (
            lambda artifact: artifact["dynamic"]["active_profiles"].pop(),
            "active profile count",
        ),
    ],
)
def test_sensitivity_gate_rejects_inconsistent_outcomes(mutation, message):
    from experiments.submission_evidence_gates import validate_sensitivity_scenario

    artifact = _sensitivity()
    mutation(artifact)

    with pytest.raises(ValueError, match=message):
        validate_sensitivity_scenario(
            "capacity_low", artifact, expected_hash=BASELINE_HASH
        )


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (lambda artifact: artifact["metadata"].update(baseline_sha256="b" * 64), "baseline SHA-256"),
        (lambda artifact: artifact["metadata"].update(successful_starts=63), "successful starts"),
        (lambda artifact: artifact.update(branch_count=2), "single branch"),
        (lambda artifact: artifact.update(single_recovered_branch=False), "single branch"),
        (lambda artifact: artifact["branches"][0]["full_candidate"].update(max_regret=2e-7), "full-candidate regret"),
    ],
)
def test_branch_gate_rejects_invalid_audit(mutation, message):
    from experiments.submission_evidence_gates import validate_branch_audit

    artifact = _branch_audit()
    mutation(artifact)

    with pytest.raises(ValueError, match=message):
        validate_branch_audit(artifact, expected_hash=BASELINE_HASH)


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (lambda artifact: artifact.update(all_starts_converged=False), "converge"),
        (lambda artifact: artifact.update(maximum_residual=2e-8), "residual"),
        (lambda artifact: artifact.update(maximum_qos_span=2e-7), "QoS span"),
        (
            lambda artifact: artifact["metadata"].update(
                covered_probability_mass=0.99
            ),
            "coverage",
        ),
    ],
)
def test_fixed_point_gate_rejects_failed_quality_checks(mutation, message):
    from experiments.submission_evidence_gates import validate_fixed_point_audit

    artifact = _fixed_point_audit()
    mutation(artifact)
    with pytest.raises(ValueError, match=message):
        validate_fixed_point_audit(artifact, expected_hash=BASELINE_HASH)


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (
            lambda artifact: artifact.update(
                maximum_relative_profit_improvement=0.0011
            ),
            "profit improvement",
        ),
        (lambda artifact: artifact.update(maximum_joint_residual=2e-8), "residual"),
        (
            lambda artifact: artifact["metadata"].update(
                covered_probability_mass=0.99
            ),
            "coverage",
        ),
    ],
)
def test_intermediary_gate_rejects_failed_quality_checks(mutation, message):
    from experiments.submission_evidence_gates import validate_intermediary_audit

    artifact = _intermediary_audit()
    mutation(artifact)
    with pytest.raises(ValueError, match=message):
        validate_intermediary_audit(artifact, expected_hash=BASELINE_HASH)


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (lambda artifact: artifact["rows"][0].update(all_converged=False), "converge"),
        (
            lambda artifact: artifact["rows"][0].update(
                maximum_joint_residual=2e-8
            ),
            "residual",
        ),
        (
            lambda artifact: artifact["rows"][0].update(probability_mass=0.99),
            "probability mass",
        ),
        (lambda artifact: artifact["rows"].pop(), "eight policy-mechanism rows"),
    ],
)
def test_mechanism_gate_rejects_failed_quality_checks(mutation, message):
    from experiments.submission_evidence_gates import validate_mechanism_audit

    artifact = _mechanism_audit()
    mutation(artifact)
    with pytest.raises(ValueError, match=message):
        validate_mechanism_audit(artifact, expected_hash=BASELINE_HASH)


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (
            lambda artifact: artifact["dynamic"].update(active_profile_count=675),
            "profile count",
        ),
        (
            lambda artifact: artifact["dynamic"].update(all_joint_converged=False),
            "converge",
        ),
        (
            lambda artifact: artifact["dynamic"].update(maximum_joint_residual=2e-8),
            "residual",
        ),
        (
            lambda artifact: artifact["dynamic"].update(
                maximum_expected_metric_reconstruction_error=2e-8
            ),
            "reconstruction",
        ),
        (
            lambda artifact: artifact["dynamic"].update(probability_mass=0.99),
            "probability mass",
        ),
    ],
)
def test_distribution_gate_rejects_failed_quality_checks(mutation, message):
    from experiments.submission_evidence_gates import validate_distribution_audit

    artifact = _distribution_audit()
    mutation(artifact)
    with pytest.raises(ValueError, match=message):
        validate_distribution_audit(artifact, expected_hash=BASELINE_HASH)


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (
            lambda artifact: artifact["mean_flattened_dynamic_profiles"].update(
                profile_count=675
            ),
            "profile count",
        ),
        (
            lambda artifact: artifact["mean_flattened_dynamic_profiles"].update(
                all_converged=False
            ),
            "converge",
        ),
        (
            lambda artifact: artifact["mean_flattened_dynamic_profiles"].update(
                maximum_joint_residual=2e-8
            ),
            "residual",
        ),
        (
            lambda artifact: artifact["mean_flattened_dynamic_profiles"].update(
                probability_mass=0.99
            ),
            "probability mass",
        ),
        (
            lambda artifact: artifact["uniform_flattening_check"].update(
                maximum_absolute_error=2e-8
            ),
            "uniform flattening",
        ),
        (lambda artifact: artifact["components"].pop(), "four decomposition rows"),
        (
            lambda artifact: artifact["components"][0].update(identity_error=2e-8),
            "identity error",
        ),
        (
            lambda artifact: artifact["components"][0].update(shape_change=0.0),
            "shape arithmetic",
        ),
    ],
)
def test_price_shape_gate_rejects_failed_quality_checks(mutation, message):
    from experiments.submission_evidence_gates import validate_price_shape_audit

    artifact = _price_shape_audit()
    mutation(artifact)
    with pytest.raises(ValueError, match=message):
        validate_price_shape_audit(artifact, expected_hash=BASELINE_HASH)


def test_total_evidence_report_includes_price_shape_audit():
    source = GATE_SOURCE.read_text(encoding="utf-8")

    assert (
        '("price_shape_audit", PRICE_SHAPE_PATH, validate_price_shape_audit)'
        in source
    )


def test_real_submission_equilibrium_passes_its_own_gate():
    from experiments.submission_evidence_gates import validate_equilibrium

    artifact = json.loads(REAL_EQUILIBRIUM.read_text(encoding="utf-8"))

    assert validate_equilibrium(artifact)["passed"]


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (
            lambda artifact: artifact["metadata"].update(full_candidate_count=1575),
            "candidate count",
        ),
        (
            lambda artifact: artifact["scenario"].update(capacity_scale=0.9),
            "baseline scenario",
        ),
        (lambda artifact: artifact["candidate_grid"].pop(), "candidate grid"),
        (
            lambda artifact: artifact["dynamic"].update(full_max_regret=2e-7),
            "full-candidate regret",
        ),
        (
            lambda artifact: artifact["dynamic"].update(
                maximum_joint_residual=2e-8
            ),
            "joint residual",
        ),
        (
            lambda artifact: artifact["dynamic"]["expected_metrics"].update(
                total_demand=1099.0
            ),
            "total demand",
        ),
        (
            lambda artifact: artifact["dynamic"]["expected_metrics"].update(
                system_profit=1900.0
            ),
            "profit accounting",
        ),
        (
            lambda artifact: artifact["comparison"].update(
                aggregate_peak_load_change=0.0
            ),
            "comparison arithmetic",
        ),
        (
            lambda artifact: artifact["dynamic"]["expected_profiles"][
                "aggregate_load"
            ].pop(),
            "expected profile length",
        ),
        (
            lambda artifact: artifact["dynamic"]["active_profiles"].pop(),
            "active profile count",
        ),
    ],
)
def test_equilibrium_gate_rejects_invalid_baseline(mutation, message):
    from experiments.submission_evidence_gates import validate_equilibrium

    artifact = json.loads(REAL_EQUILIBRIUM.read_text(encoding="utf-8"))
    mutation(artifact)

    with pytest.raises(ValueError, match=message):
        validate_equilibrium(artifact)


def test_total_evidence_report_starts_with_baseline_equilibrium_gate():
    source = GATE_SOURCE.read_text(encoding="utf-8")

    assert 'checks["equilibrium"] = validate_equilibrium(equilibrium)' in source


def test_real_input_anchors_pass_the_submission_gate():
    from experiments.submission_evidence_gates import validate_input_anchors

    equilibrium, load_metadata, load_rows, qos = _real_input_anchors()

    assert validate_input_anchors(
        equilibrium=equilibrium,
        load_metadata=load_metadata,
        load_rows=load_rows,
        qos=qos,
    )["passed"]


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (
            lambda equilibrium, metadata, rows, qos: metadata.update(
                rows_read=1_429_736
            ),
            "row count",
        ),
        (
            lambda equilibrium, metadata, rows, qos: metadata["days_used"].pop(),
            "59 complete days",
        ),
        (
            lambda equilibrium, metadata, rows, qos: rows.pop(),
            "eight periods",
        ),
        (
            lambda equilibrium, metadata, rows, qos: rows[0].update(
                token_share_mean="0.5"
            ),
            "token shares",
        ),
        (
            lambda equilibrium, metadata, rows, qos: qos["points"].pop(),
            "ten QoS points",
        ),
        (
            lambda equilibrium, metadata, rows, qos: qos["points"][0].update(
                repeats=4
            ),
            "five repeats",
        ),
        (
            lambda equilibrium, metadata, rows, qos: qos["pooled_fit"].update(
                threshold=0.9
            ),
            "QoS threshold",
        ),
        (
            lambda equilibrium, metadata, rows, qos: equilibrium[
                "qos_calibration"
            ].update(strength=0.5),
            "baseline QoS calibration",
        ),
    ],
)
def test_input_anchor_gate_rejects_invalid_evidence(mutation, message):
    from experiments.submission_evidence_gates import validate_input_anchors

    equilibrium, load_metadata, load_rows, qos = _real_input_anchors()
    mutation(equilibrium, load_metadata, load_rows, qos)

    with pytest.raises(ValueError, match=message):
        validate_input_anchors(
            equilibrium=equilibrium,
            load_metadata=load_metadata,
            load_rows=load_rows,
            qos=qos,
        )


def test_total_evidence_report_includes_input_anchor_gate():
    source = GATE_SOURCE.read_text(encoding="utf-8")

    assert 'checks["input_anchors"] = validate_input_anchors(' in source


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (
            lambda artifact: artifact["metadata"].update(
                final_equilibrium_sha256="b" * 64
            ),
            "equilibrium SHA-256",
        ),
        (
            lambda artifact: artifact["verification"].update(
                exact_elementwise_match=False
            ),
            "elementwise",
        ),
        (
            lambda artifact: artifact["verification"].update(
                final_candidate_count=1575
            ),
            "candidate count",
        ),
        (
            lambda artifact: artifact["components"][0].update(
                added_unique_count=11
            ),
            "component counts",
        ),
    ],
)
def test_candidate_manifest_gate_rejects_invalid_evidence(tmp_path, mutation, message):
    from experiments.submission_evidence_gates import validate_candidate_manifest

    artifact = _candidate_manifest(tmp_path)
    mutation(artifact)

    with pytest.raises(ValueError, match=message):
        validate_candidate_manifest(
            artifact, expected_hash=BASELINE_HASH, root=tmp_path
        )


def test_candidate_manifest_gate_rejects_changed_seed(tmp_path):
    from experiments.submission_evidence_gates import validate_candidate_manifest

    artifact = _candidate_manifest(tmp_path)
    (tmp_path / "seed.json").write_text('{"changed": true}\n', encoding="utf-8")

    with pytest.raises(ValueError, match="continuation seed SHA-256"):
        validate_candidate_manifest(
            artifact, expected_hash=BASELINE_HASH, root=tmp_path
        )
