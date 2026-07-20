"""Validate provenance and numerical gates before building submission outputs."""
from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path

from experiments.build_submission_sensitivity_claims import (
    validate_claims as validate_sensitivity_claims,
)
from experiments.run_submission_spatiotemporal_sensitivity import (
    SCENARIOS,
    SOLVER_KEYS,
    _summary_row,
)


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = ROOT / "artifacts" / "peak_shaving" / "20260712_expanded_response"
EQUILIBRIUM_PATH = ARTIFACT_DIR / "spatiotemporal_equilibrium_submission.json"
CANDIDATE_MANIFEST_PATH = ARTIFACT_DIR / "candidate_manifest_submission.json"
OFFGRID_PATH = ARTIFACT_DIR / "spatiotemporal_offgrid_diagnostic_submission.json"
UNIFORM_OFFGRID_PATH = ARTIFACT_DIR / "uniform_offgrid_sensitivity_submission.json"
BRANCH_PATH = ARTIFACT_DIR / "equilibrium_branch_audit_submission.json"
FIXED_POINT_PATH = ARTIFACT_DIR / "fixed_point_multistart_audit_submission.json"
INTERMEDIARY_PATH = ARTIFACT_DIR / "intermediary_globality_audit_submission.json"
INTERMEDIARY_PAYOFF_SENSITIVITY_PATH = (
    ARTIFACT_DIR / "intermediary_payoff_sensitivity_submission.json"
)
MECHANISM_PATH = ARTIFACT_DIR / "mechanism_decomposition_submission.json"
PRICE_SHAPE_PATH = ARTIFACT_DIR / "price_shape_decomposition_submission.json"
DISTRIBUTION_PATH = ARTIFACT_DIR / "mixed_outcome_distribution_submission.json"
SENSITIVITY_SUMMARY_PATH = ARTIFACT_DIR / "spatiotemporal_sensitivity_submission.json"
SENSITIVITY_CLAIMS_PATH = ARTIFACT_DIR / "sensitivity_claims_submission.json"
REPORT_PATH = ARTIFACT_DIR / "submission_evidence_gate_report.json"
BURST_ANCHOR_DIR = ROOT / "data/processed/burstgpt_d895a53b_8period"
BURST_METADATA_PATH = BURST_ANCHOR_DIR / "burstgpt_8period_load_metadata.json"
BURST_PROFILE_PATH = BURST_ANCHOR_DIR / "burstgpt_8period_load_profile.csv"
QOS_CALIBRATION_PATH = ROOT / "artifacts/peak_shaving/20260712_final/qos_calibration.json"
SENSITIVITY_NAMES = tuple(SCENARIOS)
SCENARIO_DEFAULTS = {
    "capacity_scale": 1.0,
    "price_sensitivity_scale": 1.0,
    "migration_cost_scale": 1.0,
    "qos_threshold_shift": 0.0,
}


@dataclass(frozen=True)
class GateThresholds:
    provider_candidate_count: int = 1576
    uniform_candidate_count: int = 800
    offgrid_samples_per_player: int = 1024
    maximum_relative_offgrid_regret: float = 0.005
    maximum_joint_residual: float = 1e-8
    maximum_support_payoff_error: float = 1e-6
    minimum_successful_local_runs: int = 1
    minimum_successful_branch_starts: int = 64
    maximum_full_candidate_regret: float = 1e-7
    maximum_total_demand_error: float = 1e-8
    minimum_active_profile_coverage: float = 1.0 - 1e-9
    maximum_fixed_point_span: float = 1e-7
    maximum_relative_intermediary_gain: float = 1e-3
    maximum_distribution_reconstruction_error: float = 1e-8
    maximum_decomposition_identity_error: float = 1e-8
    uniform_active_profile_count: int = 100
    dynamic_active_profile_count: int = 676


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def active_profile_count(game: dict) -> int:
    """Return the Cartesian size of the strictly positive mixed supports."""
    row_count = sum(float(value) > 1e-12 for value in game["row_mix"])
    col_count = sum(float(value) > 1e-12 for value in game["col_mix"])
    return row_count * col_count


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def validate_source_hashes(artifact: dict, *, root: Path = ROOT) -> dict:
    manifest = artifact.get("metadata", {}).get("source_sha256")
    _require(isinstance(manifest, dict) and bool(manifest), "source hashes are missing")
    root = Path(root).resolve()
    for relative, recorded_hash in manifest.items():
        source = (root / relative).resolve()
        _require(
            source.is_relative_to(root),
            f"source path escapes the repository: {relative}",
        )
        _require(source.is_file(), f"source file is missing: {relative}")
        _require(
            _sha256(source) == recorded_hash,
            f"{relative}: source SHA-256 mismatch",
        )
    return {"passed": True, "source_count": len(manifest)}


def _validate_burst_anchor(metadata: dict, rows: list[dict]) -> dict:
    _require(metadata.get("rows_read") == 1_429_737, "BurstGPT row count differs")
    _require(metadata.get("rows_skipped") == 0, "BurstGPT rows were skipped")
    _require(
        metadata.get("days_used") == list(range(1, 60)),
        "BurstGPT anchor does not use the declared 59 complete days",
    )
    _require(
        metadata.get("source_commit") == "d895a53bb7b8ec137d0d2fe203b335835a78c10a"
        and len(metadata.get("source_sha256", "")) == 64,
        "BurstGPT source provenance differs",
    )
    _require(len(rows) == 8, "BurstGPT anchor does not contain eight periods")
    _require([int(row["period"]) for row in rows] == list(range(1, 9)), "period order differs")
    numeric = {
        name: [float(row[name]) for row in rows]
        for name in (
            "request_share_mean", "request_share_std", "token_share_mean",
            "token_share_std", "normalized_token_load",
        )
    }
    _require(
        all(math.isfinite(value) for values in numeric.values() for value in values),
        "BurstGPT anchor contains a non-finite value",
    )
    _require(
        abs(sum(numeric["request_share_mean"]) - 1.0) <= 1e-12,
        "BurstGPT request shares do not sum to one",
    )
    _require(
        abs(sum(numeric["token_share_mean"]) - 1.0) <= 1e-12,
        "BurstGPT token shares do not sum to one",
    )
    load = numeric["normalized_token_load"]
    _require(
        abs(sum(load)) <= 1e-12 and abs(max(abs(value) for value in load) - 1.0) <= 1e-12,
        "BurstGPT normalized load is not centered and scaled",
    )
    return {"period_count": len(rows), "day_count": len(metadata["days_used"])}


def _validate_qos_points(points: list[dict]) -> None:
    _require(len(points) == 10, "calibration does not contain ten QoS points")
    expected_counts = {"vllm-0.5b": 5, "vllm-3b": 5}
    counts = {
        profile: sum(point.get("profile") == profile for point in points)
        for profile in expected_counts
    }
    _require(counts == expected_counts, "QoS profile point counts differ")
    _require(
        all(point.get("repeats") == 5 for point in points),
        "QoS points do not all use five repeats",
    )
    for point in points:
        values = [
            float(point[name])
            for name in (
                "normalized_utilization", "observed_qos", "observed_qos_ci95",
                "pooled_fitted_qos",
            )
        ]
        _require(all(math.isfinite(value) for value in values), "non-finite QoS point")
        _require(
            values[0] > 0.0 and 0.0 <= values[1] <= 1.0
            and values[2] >= 0.0 and 0.0 <= values[3] <= 1.0,
            "QoS point is outside its declared range",
        )


def _validate_qos_anchor(qos: dict, equilibrium: dict) -> dict:
    provenance = validate_source_hashes(qos)
    _validate_qos_points(qos.get("points", []))
    fit = qos["pooled_fit"]
    _require(fit.get("optimizer_success") is True, "QoS optimizer did not succeed")
    _require(
        float(fit["threshold"]) >= 1.0,
        "QoS threshold violates the declared fit constraint",
    )
    _require(
        float(fit["strength"]) > 0.0 and 0.0 <= float(fit["rmse"]) <= 0.1,
        "QoS fit strength or RMSE is outside the gate",
    )
    embedded = equilibrium["qos_calibration"]
    _require(
        all(
            abs(float(embedded[name]) - float(fit[name])) <= 1e-12
            for name in ("threshold", "strength")
        ),
        "baseline QoS calibration does not match the fitted anchor",
    )
    loo = qos.get("leave_one_profile_out", {})
    _require(
        len(loo) == 2
        and all(0.0 <= float(values["test_rmse"]) <= 0.15 for values in loo.values()),
        "leave-one-profile-out QoS errors are incomplete or non-finite",
    )
    return {"provenance": provenance, "point_count": len(qos["points"])}


def _validate_anchor_file_links(equilibrium: dict) -> None:
    manifest = equilibrium["metadata"]["source_sha256"]
    for path in (BURST_PROFILE_PATH, QOS_CALIBRATION_PATH):
        relative = str(path.relative_to(ROOT))
        _require(
            manifest.get(relative) == _sha256(path),
            f"baseline input SHA-256 does not match: {relative}",
        )


def validate_input_anchors(
    *, equilibrium: dict, load_metadata: dict, load_rows: list[dict], qos: dict
) -> dict:
    _validate_anchor_file_links(equilibrium)
    burst = _validate_burst_anchor(load_metadata, load_rows)
    qos_result = _validate_qos_anchor(qos, equilibrium)
    return {
        "passed": True,
        "burstgpt": burst,
        "qos": qos_result,
        "load_metadata_sha256": _sha256(BURST_METADATA_PATH),
    }


def _nested_shape(values: object, *, label: str) -> tuple[int, ...]:
    if not isinstance(values, list):
        return ()
    _require(bool(values), f"{label}: expected profile length is zero")
    child_shapes = [_nested_shape(value, label=label) for value in values]
    _require(
        all(shape == child_shapes[0] for shape in child_shapes),
        f"{label}: expected profile length is ragged",
    )
    return (len(values), *child_shapes[0])


def _finite_values(values: object) -> list[float]:
    if isinstance(values, list):
        return [number for value in values for number in _finite_values(value)]
    return [float(values)]


def _validate_expected_profiles(game: dict, *, label: str, gate: GateThresholds) -> None:
    expected_shapes = {
        "aggregate_load": (8,),
        "provider_utilization": (2, 8),
        "provider_qos": (2, 8),
        "channel_demand": (3, 8),
        "destination_demand_by_type": (2, 8),
        "retail_price": (8,),
        "direct_price": (2, 8),
        "wholesale_price": (2, 8),
        "routing": (2, 8),
    }
    profiles = game["expected_profiles"]
    _require(set(profiles) == set(expected_shapes), f"{label}: expected profiles differ")
    for name, expected_shape in expected_shapes.items():
        shape = _nested_shape(profiles[name], label=f"{label} {name}")
        _require(shape == expected_shape, f"{label}: expected profile length differs")
        _require(
            all(math.isfinite(value) for value in _finite_values(profiles[name])),
            f"{label}: expected profile contains a non-finite value",
        )
    _validate_profile_metric_links(game, label=label, gate=gate)


def _validate_profile_metric_links(
    game: dict, *, label: str, gate: GateThresholds
) -> None:
    profiles, metrics = game["expected_profiles"], game["expected_metrics"]
    aggregate = _finite_values(profiles["aggregate_load"])
    _require(
        abs(float(metrics["total_demand"]) - sum(aggregate))
        <= gate.maximum_total_demand_error,
        f"{label}: total demand does not match the expected load profile",
    )


def _validate_equilibrium_support(
    game: dict, *, label: str, expected_count: int, gate: GateThresholds
) -> None:
    profiles = game["active_profiles"]
    _require(
        len(profiles) == expected_count,
        f"{label}: active profile count does not match",
    )
    weights = [float(profile["weight"]) for profile in profiles]
    _require(
        all(weight >= 0.0 and math.isfinite(weight) for weight in weights)
        and abs(sum(weights) - 1.0) <= gate.maximum_total_demand_error,
        f"{label}: active profile probability mass does not sum to one",
    )
    _require(
        max(float(profile["joint_residual"]) for profile in profiles)
        <= gate.maximum_joint_residual,
        f"{label}: active profile joint residual exceeds the gate",
    )
    for side in ("row", "col"):
        mix = [float(value) for value in game[f"{side}_mix"]]
        support = game[f"{side}_support_vectors"]
        indices = game[f"{side}_support_indices"]
        _require(
            len(mix) == len(support) == len(indices),
            f"{label}: support and mixture dimensions do not match",
        )
        _require(
            all(value >= 0.0 and math.isfinite(value) for value in mix)
            and abs(sum(mix) - 1.0) <= gate.maximum_total_demand_error,
            f"{label}: support mixture probability mass does not sum to one",
        )


def _validate_equilibrium_accounting(
    game: dict, *, label: str, gate: GateThresholds
) -> None:
    metrics = game["expected_metrics"]
    required = {
        "firm_A_profit", "firm_B_profit", "intermediary_profit", "system_profit",
        "aggregate_peak_load", "aggregate_peak_to_average",
        "maximum_provider_utilization", "provider_utilization_imbalance",
        "minimum_provider_qos", "temporal_moved_fraction", "total_demand",
    }
    _require(required <= set(metrics), f"{label}: expected metrics are incomplete")
    _require(
        all(math.isfinite(float(metrics[name])) for name in required),
        f"{label}: expected metrics contain a non-finite value",
    )
    profit_sum = sum(float(metrics[name]) for name in (
        "firm_A_profit", "firm_B_profit", "intermediary_profit"
    ))
    _require(
        abs(float(metrics["system_profit"]) - profit_sum)
        <= gate.maximum_total_demand_error,
        f"{label}: profit accounting identity does not hold",
    )
    peak_to_average = float(metrics["aggregate_peak_load"]) / (
        float(metrics["total_demand"]) / 8.0
    )
    _require(
        abs(float(metrics["aggregate_peak_to_average"]) - peak_to_average)
        <= gate.maximum_total_demand_error,
        f"{label}: peak-to-average arithmetic does not hold",
    )


def _validate_equilibrium_comparison(
    artifact: dict, *, gate: GateThresholds
) -> None:
    uniform = artifact["uniform"]["expected_metrics"]
    dynamic = artifact["dynamic"]["expected_metrics"]
    comparison = artifact["comparison"]
    for metric in (
        "aggregate_peak_load", "maximum_provider_utilization",
        "minimum_provider_qos", "system_profit", "temporal_moved_fraction",
    ):
        change = float(dynamic[metric]) - float(uniform[metric])
        percent = 100.0 * change / float(uniform[metric])
        _require(
            abs(float(comparison[f"{metric}_change"]) - change)
            <= gate.maximum_total_demand_error
            and abs(float(comparison[f"{metric}_change_percent"]) - percent)
            <= gate.maximum_total_demand_error,
            f"{metric}: comparison arithmetic does not reconstruct",
        )


def validate_equilibrium(
    artifact: dict, *, thresholds: GateThresholds | None = None
) -> dict:
    gate = thresholds or GateThresholds()
    provenance = validate_source_hashes(artifact)
    _require(
        artifact["metadata"].get("full_candidate_count")
        == gate.provider_candidate_count,
        "baseline provider candidate count is not 1576",
    )
    _require(artifact.get("scenario") == SCENARIO_DEFAULTS, "baseline scenario differs")
    candidates = artifact.get("candidate_grid", [])
    candidate_tuples = [tuple(float(value) for value in row) for row in candidates]
    _require(
        len(candidates) == gate.provider_candidate_count
        and all(len(row) == 4 for row in candidates)
        and len(set(candidate_tuples)) == gate.provider_candidate_count
        and all(math.isfinite(value) for row in candidate_tuples for value in row),
        "baseline candidate grid is not the declared unique 1576-vector set",
    )
    _require(
        artifact.get("intermediary_response", {}).get("method")
        == "continuous_multistart",
        "baseline intermediary response method differs",
    )
    games = _validate_sensitivity_games(
        artifact, gate, expected_total_demand=1100.0
    )
    for label in ("uniform", "dynamic"):
        expected_count = active_profile_count(artifact[label])
        _validate_equilibrium_accounting(artifact[label], label=label, gate=gate)
        _validate_expected_profiles(artifact[label], label=label, gate=gate)
        _validate_equilibrium_support(
            artifact[label], label=label, expected_count=expected_count, gate=gate
        )
    _validate_equilibrium_comparison(artifact, gate=gate)
    return {"passed": True, "provenance": provenance, "games": games}


def validate_offgrid(
    artifact: dict,
    *,
    expected_hash: str,
    thresholds: GateThresholds | None = None,
) -> dict:
    gate = thresholds or GateThresholds()
    metadata = artifact["metadata"]
    _require(
        metadata.get("equilibrium_sha256") == expected_hash,
        "off-grid equilibrium SHA-256 does not match the baseline",
    )
    _require(
        metadata.get("provider_candidate_count") == gate.provider_candidate_count,
        "off-grid provider candidate count is not 1576",
    )
    _require(
        metadata.get("samples_per_player", 0) >= gate.offgrid_samples_per_player,
        "off-grid sample count is below the submission gate",
    )
    _require(metadata.get("seed") == 20260714, "off-grid seed is not independent")
    summaries = {}
    for player in ("firm_A", "firm_B"):
        summaries[player] = _validate_offgrid_player(
            player, artifact["players"][player], gate
        )
    return {"passed": True, "players": summaries}


def _validate_offgrid_player(
    player: str,
    values: dict,
    gate: GateThresholds,
    *,
    require_local_runs: bool = True,
) -> dict:
    prefix = f"{player}: "
    _require(values["all_joint_converged"], prefix + "non-converged fixed point")
    _require(
        values["relative_offgrid_regret"] <= gate.maximum_relative_offgrid_regret,
        prefix + "relative off-grid regret exceeds the gate",
    )
    _require(
        values["maximum_joint_residual"] <= gate.maximum_joint_residual,
        prefix + "joint residual exceeds the gate",
    )
    _require(
        values["maximum_active_support_payoff_error"]
        <= gate.maximum_support_payoff_error,
        prefix + "support payoff error exceeds the gate",
    )
    if require_local_runs:
        _require(
            values["minimum_successful_local_runs"]
            >= gate.minimum_successful_local_runs,
            prefix + "no successful local run for at least one deviation pair",
        )
    summary = {
        key: values[key]
        for key in (
            "relative_offgrid_regret",
            "maximum_joint_residual",
            "maximum_active_support_payoff_error",
        )
    }
    if require_local_runs:
        summary["minimum_successful_local_runs"] = values[
            "minimum_successful_local_runs"
        ]
    return summary


def validate_uniform_offgrid_sensitivity(
    artifact: dict,
    *,
    expected_hash: str,
    thresholds: GateThresholds | None = None,
    require_provenance: bool = False,
) -> dict:
    gate = thresholds or GateThresholds()
    metadata = artifact["metadata"]
    _require(
        metadata.get("baseline_sha256") == expected_hash,
        "uniform off-grid baseline SHA-256 does not match",
    )
    _require(
        metadata.get("samples_per_player", 0) >= gate.offgrid_samples_per_player,
        "uniform off-grid sample count is below the submission gate",
    )
    _require(metadata.get("seed") == 20260718, "uniform off-grid seed differs")
    scenarios = artifact.get("scenarios", [])
    expected_names = ("baseline", *SCENARIOS)
    _require(
        metadata.get("scenario_count") == 9
        and len(scenarios) == 9
        and tuple(item.get("scenario") for item in scenarios) == expected_names,
        "uniform off-grid audit must contain all nine scenarios in order",
    )
    if require_provenance:
        validate_source_hashes(artifact)
    summaries = {}
    for scenario in scenarios:
        summaries[scenario["scenario"]] = {
            player: _validate_offgrid_player(
                f"{scenario['scenario']}/{player}",
                scenario["players"][player],
                gate,
                require_local_runs=False,
            )
            for player in ("firm_A", "firm_B")
        }
    return {"passed": True, "scenarios": summaries}


def validate_branch_audit(
    artifact: dict,
    *,
    expected_hash: str,
    thresholds: GateThresholds | None = None,
) -> dict:
    gate = thresholds or GateThresholds()
    metadata = artifact["metadata"]
    _require(
        metadata.get("baseline_sha256") == expected_hash,
        "branch audit baseline SHA-256 does not match",
    )
    _require(
        artifact.get("candidate_count") == gate.provider_candidate_count,
        "branch audit provider candidate count is not 1576",
    )
    _require(
        metadata.get("successful_starts", 0) >= gate.minimum_successful_branch_starts,
        "branch audit has too few successful starts",
    )
    _require(
        artifact.get("branch_count") == 1
        and artifact.get("single_recovered_branch") is True
        and len(artifact.get("branches", [])) == 1,
        "branch audit did not recover a single branch",
    )
    regret = artifact["branches"][0]["full_candidate"]["max_regret"]
    _require(
        regret <= gate.maximum_full_candidate_regret,
        "branch audit full-candidate regret exceeds the gate",
    )
    return {
        "passed": True,
        "successful_starts": metadata["successful_starts"],
        "branch_count": artifact["branch_count"],
        "full_candidate_regret": regret,
    }


def _validate_linked_artifact(
    artifact: dict,
    *,
    expected_hash: str,
    gate: GateThresholds,
    require_coverage: bool,
) -> dict:
    metadata = artifact["metadata"]
    _require(
        metadata.get("equilibrium_sha256") == expected_hash,
        "dependent artifact equilibrium SHA-256 does not match",
    )
    if require_coverage:
        _require(
            metadata.get("covered_probability_mass", 0.0)
            >= gate.minimum_active_profile_coverage,
            "active-profile coverage is below the gate",
        )
    return validate_source_hashes(artifact)


def validate_fixed_point_audit(
    artifact: dict,
    *,
    expected_hash: str,
    thresholds: GateThresholds | None = None,
) -> dict:
    gate = thresholds or GateThresholds()
    provenance = _validate_linked_artifact(
        artifact, expected_hash=expected_hash, gate=gate, require_coverage=True
    )
    _require(artifact["all_starts_converged"], "fixed-point starts did not converge")
    _require(
        artifact["maximum_residual"] <= gate.maximum_joint_residual,
        "fixed-point residual exceeds the gate",
    )
    _require(
        artifact["maximum_qos_span"] <= gate.maximum_fixed_point_span,
        "fixed-point QoS span exceeds the gate",
    )
    _require(
        artifact["maximum_routing_span"] <= gate.maximum_fixed_point_span,
        "fixed-point routing span exceeds the gate",
    )
    return {"passed": True, "provenance": provenance}


def validate_intermediary_audit(
    artifact: dict,
    *,
    expected_hash: str,
    thresholds: GateThresholds | None = None,
) -> dict:
    gate = thresholds or GateThresholds()
    provenance = _validate_linked_artifact(
        artifact, expected_hash=expected_hash, gate=gate, require_coverage=True
    )
    _require(
        artifact["maximum_relative_profit_improvement"]
        <= gate.maximum_relative_intermediary_gain,
        "intermediary profit improvement exceeds the gate",
    )
    _require(
        artifact["maximum_joint_residual"] <= gate.maximum_joint_residual,
        "intermediary residual exceeds the gate",
    )
    return {"passed": True, "provenance": provenance}


def validate_intermediary_payoff_sensitivity(
    artifact: dict,
    *,
    expected_hash: str,
    thresholds: GateThresholds | None = None,
    require_provenance: bool = False,
) -> dict:
    gate = thresholds or GateThresholds()
    metadata = artifact["metadata"]
    _require(
        metadata.get("equilibrium_sha256") == expected_hash,
        "provider-payoff equilibrium SHA-256 does not match",
    )
    if require_provenance:
        validate_source_hashes(artifact)
    summary = artifact["summary"]
    _require(
        summary.get("covered_probability_mass", 0.0)
        >= gate.minimum_active_profile_coverage,
        "provider-payoff active-profile coverage is below the gate",
    )
    _require(
        summary["maximum_joint_residual"] <= gate.maximum_joint_residual,
        "provider-payoff residual exceeds the gate",
    )
    _require(
        summary.get("all_joint_converged", True),
        "provider-payoff fixed points did not converge",
    )
    regret = float(summary["maximum_active_support_regret"])
    _require(
        math.isfinite(regret) and regret >= 0.0,
        "provider-payoff active-support regret is invalid",
    )
    return {
        "passed": True,
        "covered_probability_mass": summary["covered_probability_mass"],
        "maximum_active_support_regret": regret,
    }


def validate_mechanism_audit(
    artifact: dict,
    *,
    expected_hash: str,
    thresholds: GateThresholds | None = None,
) -> dict:
    gate = thresholds or GateThresholds()
    provenance = _validate_linked_artifact(
        artifact, expected_hash=expected_hash, gate=gate, require_coverage=False
    )
    expected = {
        (policy, mechanism)
        for policy in ("uniform", "dynamic")
        for mechanism in ("neither", "temporal_only", "spatial_only", "combined")
    }
    rows = artifact.get("rows", [])
    observed = {(row.get("policy"), row.get("mechanism")) for row in rows}
    _require(len(rows) == 8 and observed == expected, "expected eight policy-mechanism rows")
    for row in rows:
        _require(row["all_converged"], "mechanism fixed points did not converge")
        _require(
            row["maximum_joint_residual"] <= gate.maximum_joint_residual,
            "mechanism residual exceeds the gate",
        )
        _require(
            abs(row["probability_mass"] - 1.0) <= gate.maximum_total_demand_error,
            "mechanism probability mass does not sum to one",
        )
    return {"passed": True, "provenance": provenance, "row_count": len(rows)}


def _validate_price_shape_profile(
    values: dict,
    *,
    label: str,
    expected_count: int,
    gate: GateThresholds,
) -> None:
    _require(
        values["profile_count"] == expected_count,
        f"{label} profile count does not match",
    )
    _require(values["all_converged"], f"{label} fixed points did not converge")
    _require(
        values["maximum_joint_residual"] <= gate.maximum_joint_residual,
        f"{label} residual exceeds the gate",
    )
    _require(
        abs(values["probability_mass"] - 1.0) <= gate.maximum_total_demand_error,
        f"{label} probability mass does not sum to one",
    )


def validate_price_shape_audit(
    artifact: dict,
    *,
    expected_hash: str,
    thresholds: GateThresholds | None = None,
    expected_active_counts: dict[str, int] | None = None,
) -> dict:
    gate = thresholds or GateThresholds()
    provenance = _validate_linked_artifact(
        artifact, expected_hash=expected_hash, gate=gate, require_coverage=False
    )
    uniform = artifact["uniform_flattening_check"]
    dynamic = artifact["mean_flattened_dynamic_profiles"]
    counts = expected_active_counts or {
        "uniform": gate.uniform_active_profile_count,
        "dynamic": gate.dynamic_active_profile_count,
    }
    _validate_price_shape_profile(
        uniform,
        label="uniform flattening",
        expected_count=counts["uniform"],
        gate=gate,
    )
    _validate_price_shape_profile(
        dynamic,
        label="mean-flattened dynamic",
        expected_count=counts["dynamic"],
        gate=gate,
    )
    _require(
        uniform["maximum_absolute_error"]
        <= gate.maximum_decomposition_identity_error,
        "uniform flattening error exceeds the gate",
    )
    expected_metrics = {
        "aggregate_peak_load",
        "maximum_provider_utilization",
        "minimum_provider_qos",
        "system_profit",
    }
    components = artifact.get("components", [])
    _require(
        len(components) == 4
        and {row.get("metric") for row in components} == expected_metrics,
        "expected four decomposition rows",
    )
    for row in components:
        _validate_price_shape_component(row, gate)
    return {"passed": True, "provenance": provenance, "row_count": len(components)}


def _validate_price_shape_component(row: dict, gate: GateThresholds) -> None:
    limit = gate.maximum_decomposition_identity_error
    uniform = float(row["uniform_equilibrium"])
    flattened = float(row["flattened_dynamic_profiles"])
    dynamic = float(row["dynamic_equilibrium"])
    values = (uniform, flattened, dynamic, float(row["identity_error"]))
    _require(all(math.isfinite(value) for value in values), "non-finite decomposition value")
    _require(
        abs(float(row["overall_change"]) - (dynamic - uniform)) <= limit,
        "overall arithmetic does not reconstruct",
    )
    _require(
        abs(float(row["shape_change"]) - (dynamic - flattened)) <= limit,
        "shape arithmetic does not reconstruct",
    )
    _require(
        abs(float(row["level_and_mix_remainder"]) - (flattened - uniform)) <= limit,
        "remainder arithmetic does not reconstruct",
    )
    _require(abs(float(row["identity_error"])) <= limit, "identity error exceeds the gate")


def validate_distribution_audit(
    artifact: dict,
    *,
    expected_hash: str,
    thresholds: GateThresholds | None = None,
    expected_active_counts: dict[str, int] | None = None,
) -> dict:
    gate = thresholds or GateThresholds()
    provenance = _validate_linked_artifact(
        artifact, expected_hash=expected_hash, gate=gate, require_coverage=False
    )
    _require(
        artifact["metadata"].get("quantiles") == [0.05, 0.5, 0.95],
        "distribution quantiles do not match the declared values",
    )
    expected_counts = expected_active_counts or {
        "uniform": gate.uniform_active_profile_count,
        "dynamic": gate.dynamic_active_profile_count,
    }
    for name, expected_count in expected_counts.items():
        game = artifact[name]
        _require(
            game["active_profile_count"] == expected_count,
            f"{name} distribution profile count does not match",
        )
        _require(game["all_joint_converged"], f"{name} distribution did not converge")
        _require(
            game["maximum_joint_residual"] <= gate.maximum_joint_residual,
            f"{name} distribution residual exceeds the gate",
        )
        _require(
            game["maximum_expected_metric_reconstruction_error"]
            <= gate.maximum_distribution_reconstruction_error,
            f"{name} distribution reconstruction error exceeds the gate",
        )
        _require(
            abs(game["probability_mass"] - 1.0) <= gate.maximum_total_demand_error,
            f"{name} distribution probability mass does not sum to one",
        )
    return {"passed": True, "provenance": provenance}


def validate_candidate_manifest(
    artifact: dict,
    *,
    expected_hash: str,
    root: Path = ROOT,
    thresholds: GateThresholds | None = None,
) -> dict:
    gate = thresholds or GateThresholds()
    root = Path(root).resolve()
    metadata = artifact["metadata"]
    _require(
        metadata.get("final_equilibrium_sha256") == expected_hash,
        "candidate manifest equilibrium SHA-256 does not match",
    )
    provenance = validate_source_hashes(artifact, root=root)
    seed_path = (root / metadata.get("continuation_seed_path", "")).resolve()
    _require(
        seed_path.is_relative_to(root) and seed_path.is_file(),
        "candidate manifest continuation seed is missing",
    )
    _require(
        _sha256(seed_path) == metadata.get("continuation_seed_sha256"),
        "candidate manifest continuation seed SHA-256 does not match",
    )
    verification = artifact["verification"]
    _require(
        verification.get("exact_elementwise_match") is True,
        "candidate manifest is not an exact elementwise match",
    )
    _require(
        verification.get("component_union_count") == gate.provider_candidate_count
        and verification.get("reconstructed_candidate_count")
        == gate.provider_candidate_count
        and verification.get("final_candidate_count") == gate.provider_candidate_count,
        "candidate manifest candidate count is not 1576",
    )
    expected_added = [800, 378, 120, 64, 27, 100, 69, 18]
    expected_cumulative = [800, 1178, 1298, 1362, 1389, 1489, 1558, 1576]
    components = artifact.get("components", [])
    _require(
        [row.get("added_unique_count") for row in components] == expected_added
        and [row.get("cumulative_unique_count") for row in components]
        == expected_cumulative,
        "candidate manifest component counts do not match",
    )
    return {
        "passed": True,
        "provenance": provenance,
        "candidate_count": gate.provider_candidate_count,
    }


def _strategy_contract(artifact: dict) -> dict:
    response = artifact.get("intermediary_response", {})
    return {
        "candidate_grid": artifact.get("candidate_grid"),
        "intermediary_response": {
            key: response.get(key)
            for key in ("method", "uniform", "dynamic")
        },
    }


def _validate_sensitivity_games(
    artifact: dict,
    gate: GateThresholds,
    *,
    expected_total_demand: float | None,
) -> dict:
    expected_counts = {
        "uniform": gate.uniform_candidate_count,
        "dynamic": gate.provider_candidate_count,
    }
    games, totals = {}, {}
    for game_name, expected_count in expected_counts.items():
        game = artifact[game_name]
        _require(
            game["candidate_count"] == expected_count,
            f"{game_name}: candidate count does not match the declared game",
        )
        _require(game["full_grid_verified"], f"{game_name}: grid not verified")
        _require(
            game["full_max_regret"] <= gate.maximum_full_candidate_regret,
            f"{game_name}: full-candidate regret exceeds the gate",
        )
        _require(
            game["maximum_joint_residual"] <= gate.maximum_joint_residual,
            f"{game_name}: joint residual exceeds the gate",
        )
        total = float(game["expected_metrics"]["total_demand"])
        _require(math.isfinite(total), f"{game_name}: total demand is not finite")
        totals[game_name] = total
        games[game_name] = {
            "full_max_regret": game["full_max_regret"],
            "maximum_joint_residual": game["maximum_joint_residual"],
        }
    _require(
        abs(totals["uniform"] - totals["dynamic"])
        <= gate.maximum_total_demand_error,
        "uniform and dynamic total demand do not match",
    )
    if expected_total_demand is not None:
        _require(
            max(abs(total - expected_total_demand) for total in totals.values())
            <= gate.maximum_total_demand_error,
            "sensitivity total demand does not match the baseline",
        )
    return games


def _validate_sensitivity_outcomes(artifact: dict, gate: GateThresholds) -> dict:
    active_counts = {}
    for label in ("uniform", "dynamic"):
        game = artifact[label]
        row_count = sum(float(value) > 1e-12 for value in game["row_mix"])
        col_count = sum(float(value) > 1e-12 for value in game["col_mix"])
        expected_count = row_count * col_count
        _require(expected_count > 0, f"{label}: mixed support is empty")
        _validate_equilibrium_accounting(game, label=label, gate=gate)
        _validate_expected_profiles(game, label=label, gate=gate)
        _validate_equilibrium_support(
            game,
            label=label,
            expected_count=expected_count,
            gate=gate,
        )
        active_counts[label] = expected_count
    _validate_equilibrium_comparison(artifact, gate=gate)
    return active_counts


def validate_sensitivity_scenario(
    name: str,
    artifact: dict,
    *,
    expected_hash: str,
    expected_baseline: dict | None = None,
    thresholds: GateThresholds | None = None,
) -> dict:
    gate = thresholds or GateThresholds()
    metadata = artifact["metadata"]
    _require(name in SCENARIOS, f"{name}: unknown sensitivity scenario")
    expected_scenario = dict(SCENARIO_DEFAULTS)
    expected_scenario.update({
        key: SCENARIOS[name][key]
        for key in SOLVER_KEYS
        if key in SCENARIOS[name]
    })
    _require(
        artifact.get("scenario") == expected_scenario,
        f"{name}: scenario parameters do not match the declared perturbation",
    )
    if expected_baseline is None and EQUILIBRIUM_PATH.is_file():
        if _sha256(EQUILIBRIUM_PATH) == expected_hash:
            expected_baseline = _read_json(EQUILIBRIUM_PATH)
    if expected_baseline is not None:
        _require(
            _strategy_contract(artifact) == _strategy_contract(expected_baseline),
            f"{name}: baseline strategy contract does not match",
        )
    recorded_hash = metadata.get("baseline_equilibrium", {}).get("sha256")
    _require(recorded_hash == expected_hash, f"{name}: baseline SHA-256 mismatch")
    provenance = validate_source_hashes(artifact)
    _require(
        metadata.get("full_candidate_count") == gate.provider_candidate_count,
        f"{name}: provider candidate count is not 1576",
    )
    expected_total = None
    if expected_baseline is not None:
        expected_total = (
            expected_baseline.get("uniform", {})
            .get("expected_metrics", {})
            .get("total_demand")
        )
    games = _validate_sensitivity_games(
        artifact,
        gate,
        expected_total_demand=expected_total,
    )
    active_counts = _validate_sensitivity_outcomes(artifact, gate)
    return {
        "passed": True,
        "provenance": provenance,
        "games": games,
        "active_profile_counts": active_counts,
    }


def validate_sensitivity_summary(
    summary: dict,
    *,
    equilibrium: dict,
    scenario_artifacts: dict[str, dict],
    expected_hash: str,
    thresholds: GateThresholds | None = None,
) -> dict:
    gate = thresholds or GateThresholds()
    metadata = summary["metadata"]
    _require(
        metadata.get("baseline_sha256") == expected_hash,
        "sensitivity summary baseline SHA-256 does not match",
    )
    _require(
        metadata.get("provider_candidate_count") == gate.provider_candidate_count
        and metadata.get("scenario_count") == 1 + len(SCENARIOS)
        and metadata.get("intermediary_response_method")
        == equilibrium["intermediary_response"]["method"],
        "sensitivity summary metadata differs",
    )
    _require(
        summary.get("scenario_definitions") == SCENARIOS,
        "sensitivity summary scenario definitions differ",
    )
    provenance = validate_source_hashes(summary)
    expected_rows = [
        _summary_row(
            "baseline", {"group": "baseline", "value": 1.0}, equilibrium
        )
    ]
    for name, definition in SCENARIOS.items():
        _require(name in scenario_artifacts, f"missing sensitivity artifact: {name}")
        expected_rows.append(
            _summary_row(name, definition, scenario_artifacts[name])
        )
    _require(
        summary.get("rows") == expected_rows,
        "sensitivity summary rows do not match the underlying artifacts",
    )
    return {
        "passed": True,
        "provenance": provenance,
        "row_count": len(expected_rows),
    }


def build_gate_report(
    *,
    equilibrium_path: Path = EQUILIBRIUM_PATH,
    offgrid_path: Path = OFFGRID_PATH,
    artifact_dir: Path = ARTIFACT_DIR,
) -> dict:
    expected_hash = _sha256(equilibrium_path)
    thresholds = GateThresholds()
    checks, failures = {}, []
    equilibrium = _read_json(equilibrium_path)
    try:
        checks["equilibrium"] = validate_equilibrium(equilibrium)
    except (KeyError, TypeError, ValueError) as error:
        failures.append(f"equilibrium: {error}")
    try:
        checks["input_anchors"] = validate_input_anchors(
            equilibrium=equilibrium,
            load_metadata=_read_json(BURST_METADATA_PATH),
            load_rows=_read_csv(BURST_PROFILE_PATH),
            qos=_read_json(QOS_CALIBRATION_PATH),
        )
    except (FileNotFoundError, KeyError, TypeError, ValueError) as error:
        failures.append(f"input_anchors: {error}")
    try:
        checks["offgrid"] = validate_offgrid(
            _read_json(offgrid_path), expected_hash=expected_hash, thresholds=thresholds
        )
    except (KeyError, ValueError) as error:
        failures.append(str(error))
    try:
        checks["uniform_offgrid"] = validate_uniform_offgrid_sensitivity(
            _read_json(UNIFORM_OFFGRID_PATH),
            expected_hash=expected_hash,
            thresholds=thresholds,
            require_provenance=True,
        )
    except (FileNotFoundError, KeyError, ValueError) as error:
        failures.append(f"uniform_offgrid: {error}")
    try:
        checks["equilibrium_branch"] = validate_branch_audit(
            _read_json(BRANCH_PATH), expected_hash=expected_hash, thresholds=thresholds
        )
    except (FileNotFoundError, KeyError, ValueError) as error:
        failures.append(f"equilibrium_branch: {error}")
    try:
        checks["candidate_manifest"] = validate_candidate_manifest(
            _read_json(CANDIDATE_MANIFEST_PATH),
            expected_hash=expected_hash,
            thresholds=thresholds,
        )
    except (FileNotFoundError, KeyError, TypeError, ValueError) as error:
        failures.append(f"candidate_manifest: {error}")
    dependent_audits = {
        "fixed_point_audit": (FIXED_POINT_PATH, validate_fixed_point_audit),
        "intermediary_audit": (INTERMEDIARY_PATH, validate_intermediary_audit),
        "mechanism_audit": (MECHANISM_PATH, validate_mechanism_audit),
    }
    for name, (path, validator) in dependent_audits.items():
        try:
            checks[name] = validator(
                _read_json(path), expected_hash=expected_hash, thresholds=thresholds
            )
        except (FileNotFoundError, KeyError, ValueError) as error:
            failures.append(f"{name}: {error}")
    active_counts = {
        name: active_profile_count(equilibrium[name])
        for name in ("uniform", "dynamic")
    }
    for name, path, validator in (
        ("price_shape_audit", PRICE_SHAPE_PATH, validate_price_shape_audit),
        ("distribution_audit", DISTRIBUTION_PATH, validate_distribution_audit),
    ):
        try:
            checks[name] = validator(
                _read_json(path),
                expected_hash=expected_hash,
                thresholds=thresholds,
                expected_active_counts=active_counts,
            )
        except (FileNotFoundError, KeyError, ValueError) as error:
            failures.append(f"{name}: {error}")
    try:
        checks["intermediary_payoff_sensitivity"] = (
            validate_intermediary_payoff_sensitivity(
                _read_json(INTERMEDIARY_PAYOFF_SENSITIVITY_PATH),
                expected_hash=expected_hash,
                thresholds=thresholds,
                require_provenance=True,
            )
        )
    except (FileNotFoundError, KeyError, ValueError) as error:
        failures.append(f"intermediary_payoff_sensitivity: {error}")
    sensitivity_artifacts = {}
    for name in SENSITIVITY_NAMES:
        path = artifact_dir / f"sensitivity_{name}_submission.json"
        try:
            artifact = _read_json(path)
            checks[name] = validate_sensitivity_scenario(
                name, artifact, expected_hash=expected_hash,
                thresholds=thresholds,
            )
            sensitivity_artifacts[name] = artifact
        except (FileNotFoundError, KeyError, ValueError) as error:
            failures.append(f"{name}: {error}")
    summary = None
    try:
        summary = _read_json(SENSITIVITY_SUMMARY_PATH)
        checks["sensitivity_summary"] = validate_sensitivity_summary(
            summary,
            equilibrium=equilibrium,
            scenario_artifacts=sensitivity_artifacts,
            expected_hash=expected_hash,
            thresholds=thresholds,
        )
    except (FileNotFoundError, KeyError, ValueError) as error:
        failures.append(f"sensitivity_summary: {error}")
    try:
        if summary is None:
            summary = _read_json(SENSITIVITY_SUMMARY_PATH)
        checks["sensitivity_claims"] = validate_sensitivity_claims(
            _read_json(SENSITIVITY_CLAIMS_PATH),
            summary=summary,
            expected_summary_hash=_sha256(SENSITIVITY_SUMMARY_PATH),
        )
    except (FileNotFoundError, KeyError, ValueError) as error:
        failures.append(f"sensitivity_claims: {error}")
    return {
        "metadata": {
            "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "equilibrium_path": str(equilibrium_path.relative_to(ROOT)),
            "equilibrium_sha256": expected_hash,
            "thresholds": asdict(thresholds),
            "gate_script_sha256": _sha256(Path(__file__).resolve()),
        },
        "passed": not failures,
        "checks": checks,
        "failures": failures,
    }


def main() -> None:
    report = build_gate_report()
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(REPORT_PATH.relative_to(ROOT)), **report}))
    if not report["passed"]:
        raise ValueError("submission evidence gates did not pass")


if __name__ == "__main__":
    main()
