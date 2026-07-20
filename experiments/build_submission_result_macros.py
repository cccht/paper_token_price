"""Generate LaTeX result macros from the audited submission artifacts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARTIFACT_DIR = ROOT / "artifacts" / "peak_shaving" / "20260712_expanded_response"
EQUILIBRIUM_PATH = ARTIFACT_DIR / "spatiotemporal_equilibrium_submission.json"
OFFGRID_PATH = ARTIFACT_DIR / "spatiotemporal_offgrid_diagnostic_submission.json"
INTERMEDIARY_AUDIT_PATH = ARTIFACT_DIR / "intermediary_globality_audit_submission.json"
FIXED_POINT_AUDIT_PATH = ARTIFACT_DIR / "fixed_point_multistart_audit_submission.json"
UNIFORM_OFFGRID_PATH = ARTIFACT_DIR / "uniform_offgrid_sensitivity_submission.json"
INTERMEDIARY_PAYOFF_SENSITIVITY_PATH = (
    ARTIFACT_DIR / "intermediary_payoff_sensitivity_submission.json"
)
OUTPUT_PATH = ARTIFACT_DIR / "submission_result_macros.tex"
MAX_RELATIVE_OFFGRID_REGRET = 0.005
MAX_RELATIVE_INTERMEDIARY_GAIN = 0.001
MAX_AUDIT_RESIDUAL = 1e-8
MAX_FIXED_POINT_SPAN = 1e-7
MIN_ACTIVE_PROFILE_COVERAGE = 1.0 - 1e-9


def _active_count(game: dict, prefix: str) -> int:
    return sum(float(value) > 1e-10 for value in game[f"{prefix}_mix"])


def _macro(name: str, value: str) -> str:
    return rf"\newcommand{{\{name}}}{{{value}}}"


def equilibrium_macros(equilibrium: dict) -> dict[str, str]:
    uniform = equilibrium["uniform"]
    dynamic = equilibrium["dynamic"]
    um = uniform["expected_metrics"]
    dm = dynamic["expected_metrics"]
    change = equilibrium["comparison"]
    return {
        "ProviderCandidateCount": str(dynamic["candidate_count"]),
        "UniformCandidateCount": str(uniform["candidate_count"]),
        "DynamicRowSupportCount": str(_active_count(dynamic, "row")),
        "DynamicColSupportCount": str(_active_count(dynamic, "col")),
        "DynamicEvaluatedPairs": f"{dynamic['evaluated_pairs']:,}",
        "DynamicGridRegret": f"{dynamic['full_max_regret']:.3g}",
        "DynamicRelativeGridRegret": f"{dynamic['relative_full_max_regret']:.3g}",
        "MaximumJointResidual": f"{max(uniform['maximum_joint_residual'], dynamic['maximum_joint_residual']):.3g}",
        "UniformAggregatePeak": f"{um['aggregate_peak_load']:.3f}",
        "DynamicAggregatePeak": f"{dm['aggregate_peak_load']:.3f}",
        "UniformPeakToAverage": f"{um['aggregate_peak_to_average']:.3f}",
        "DynamicPeakToAverage": f"{dm['aggregate_peak_to_average']:.3f}",
        "AggregatePeakChangePercent": f"{change['aggregate_peak_load_change_percent']:.2f}",
        "AggregatePeakReductionPercent": f"{abs(change['aggregate_peak_load_change_percent']):.2f}",
        "UniformMaximumUtilisation": f"{um['maximum_provider_utilization']:.3f}",
        "DynamicMaximumUtilisation": f"{dm['maximum_provider_utilization']:.3f}",
        "MaximumUtilisationChangePercent": f"{change['maximum_provider_utilization_change_percent']:.2f}",
        "MaximumUtilisationReductionPercent": f"{abs(change['maximum_provider_utilization_change_percent']):.2f}",
        "UniformMinimumQoS": f"{um['minimum_provider_qos']:.3f}",
        "DynamicMinimumQoS": f"{dm['minimum_provider_qos']:.3f}",
        "MinimumQoSChange": f"{change['minimum_provider_qos_change']:.3f}",
        "UniformMovedFraction": f"{um['temporal_moved_fraction']:.3f}",
        "DynamicMovedFraction": f"{dm['temporal_moved_fraction']:.3f}",
        "MovedFractionChange": f"{dm['temporal_moved_fraction'] - um['temporal_moved_fraction']:.4f}",
        "UniformMarketProfit": f"{um['system_profit']:.3f}",
        "DynamicMarketProfit": f"{dm['system_profit']:.3f}",
        "MarketProfitChangePercent": f"{change['system_profit_change_percent']:.2f}",
        "UniformProviderAProfit": f"{um['firm_A_profit']:.3f}",
        "DynamicProviderAProfit": f"{dm['firm_A_profit']:.3f}",
        "ProviderAProfitChangePercent": f"{100.0 * (dm['firm_A_profit'] - um['firm_A_profit']) / um['firm_A_profit']:.2f}",
        "UniformProviderBProfit": f"{um['firm_B_profit']:.3f}",
        "DynamicProviderBProfit": f"{dm['firm_B_profit']:.3f}",
        "ProviderBProfitChangePercent": f"{100.0 * (dm['firm_B_profit'] - um['firm_B_profit']) / um['firm_B_profit']:.2f}",
        "UniformIntermediaryProfit": f"{um['intermediary_profit']:.3f}",
        "DynamicIntermediaryProfit": f"{dm['intermediary_profit']:.3f}",
        "IntermediaryProfitChangePercent": f"{100.0 * (dm['intermediary_profit'] - um['intermediary_profit']) / um['intermediary_profit']:.2f}",
    }


def audit_macros(
    offgrid: dict | None,
    intermediary: dict | None,
    fixed_point: dict | None,
    uniform_offgrid: dict | None = None,
    payoff_sensitivity: dict | None = None,
) -> dict[str, str]:
    output = {}
    if offgrid:
        output.update({
            "ProviderAOffgridRegret": f"{offgrid['players']['firm_A']['offgrid_regret']:.3g}",
            "ProviderBOffgridRegret": f"{offgrid['players']['firm_B']['offgrid_regret']:.3g}",
            "ProviderARelativeOffgridRegret": f"{offgrid['players']['firm_A']['relative_offgrid_regret']:.3g}",
            "ProviderBRelativeOffgridRegret": f"{offgrid['players']['firm_B']['relative_offgrid_regret']:.3g}",
        })
    if intermediary:
        output.update({
            "IntermediaryAuditCoverage": f"{100.0 * intermediary['metadata']['covered_probability_mass']:.1f}",
            "IntermediaryAuditMaxGain": f"{intermediary['maximum_profit_improvement']:.3g}",
            "IntermediaryAuditMaxRelativeGain": f"{intermediary['maximum_relative_profit_improvement']:.3g}",
        })
    if fixed_point:
        output.update({
            "FixedPointAuditCoverage": f"{100.0 * fixed_point['metadata']['covered_probability_mass']:.1f}",
            "FixedPointMaximumQoSSpan": f"{fixed_point['maximum_qos_span']:.3g}",
            "FixedPointMaximumRoutingSpan": f"{fixed_point['maximum_routing_span']:.3g}",
        })
    if uniform_offgrid:
        players = [
            values
            for scenario in uniform_offgrid["scenarios"]
            for values in scenario["players"].values()
        ]
        output.update({
            "UniformOffgridMaximumRelativeRegret": f"{max(item['relative_offgrid_regret'] for item in players):.3g}",
            "UniformOffgridMaximumResidual": f"{max(item['maximum_joint_residual'] for item in players):.3g}",
        })
    if payoff_sensitivity:
        summary = payoff_sensitivity["summary"]
        output.update({
            "ProviderPayoffActiveSupportRegret": f"{summary['maximum_active_support_regret']:.3g}",
            "ProviderPayoffMaximumProfileChange": f"{abs(summary['maximum_absolute_profile_change']['change']):.3g}",
        })
    return output


def build_macros(
    equilibrium: dict,
    *,
    offgrid: dict | None = None,
    intermediary: dict | None = None,
    fixed_point: dict | None = None,
    uniform_offgrid: dict | None = None,
    payoff_sensitivity: dict | None = None,
) -> str:
    values = equilibrium_macros(equilibrium)
    values.update(
        audit_macros(
            offgrid,
            intermediary,
            fixed_point,
            uniform_offgrid,
            payoff_sensitivity,
        )
    )
    header = "% Generated from machine-readable submission artifacts. Do not edit."
    return "\n".join([header] + [_macro(name, value) for name, value in sorted(values.items())]) + "\n"


def _validated_audit(path: Path, equilibrium_hash: str) -> dict | None:
    if not path.exists():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    metadata = payload.get("metadata", {})
    recorded_hash = metadata.get(
        "equilibrium_sha256", metadata.get("baseline_sha256")
    )
    if recorded_hash != equilibrium_hash:
        raise ValueError(
            f"{path.name} equilibrium SHA-256 is {recorded_hash!r}; "
            f"expected {equilibrium_hash!r}"
        )
    _validate_audit_quality(path, payload)
    return payload


def _offgrid_failed(payload: dict) -> bool:
    return any(
        item["relative_offgrid_regret"] > MAX_RELATIVE_OFFGRID_REGRET
        or not item["all_joint_converged"]
        or item["maximum_joint_residual"] > MAX_AUDIT_RESIDUAL
        for item in payload["players"].values()
    )


def _intermediary_audit_failed(payload: dict) -> bool:
    return (
        payload["maximum_relative_profit_improvement"]
        > MAX_RELATIVE_INTERMEDIARY_GAIN
        or payload["maximum_joint_residual"] > MAX_AUDIT_RESIDUAL
    )


def _fixed_point_audit_failed(payload: dict) -> bool:
    return (
        not payload["all_starts_converged"]
        or payload["maximum_residual"] > MAX_AUDIT_RESIDUAL
        or payload["maximum_qos_span"] > MAX_FIXED_POINT_SPAN
        or payload["maximum_routing_span"] > MAX_FIXED_POINT_SPAN
    )


def _uniform_offgrid_failed(payload: dict) -> bool:
    players = [
        values
        for scenario in payload.get("scenarios", [])
        for values in scenario["players"].values()
    ]
    return len(payload.get("scenarios", [])) != 9 or any(
        item["relative_offgrid_regret"] > MAX_RELATIVE_OFFGRID_REGRET
        or not item["all_joint_converged"]
        or item["maximum_joint_residual"] > MAX_AUDIT_RESIDUAL
        for item in players
    )


def _provider_payoff_failed(payload: dict) -> bool:
    summary = payload["summary"]
    return (
        summary["covered_probability_mass"] < MIN_ACTIVE_PROFILE_COVERAGE
        or not summary["all_joint_converged"]
        or summary["maximum_joint_residual"] > MAX_AUDIT_RESIDUAL
    )


def _validate_audit_quality(path: Path, payload: dict) -> None:
    validators = {
        OFFGRID_PATH.name: ("off-grid", _offgrid_failed),
        INTERMEDIARY_AUDIT_PATH.name: ("intermediary", _intermediary_audit_failed),
        FIXED_POINT_AUDIT_PATH.name: ("fixed-point", _fixed_point_audit_failed),
        UNIFORM_OFFGRID_PATH.name: ("uniform off-grid", _uniform_offgrid_failed),
        INTERMEDIARY_PAYOFF_SENSITIVITY_PATH.name: (
            "provider-payoff",
            _provider_payoff_failed,
        ),
    }
    if path.name in validators:
        label, failed = validators[path.name]
        if failed(payload):
            raise ValueError(f"{path.name} failed the {label} quality gate")
    if path.name in {INTERMEDIARY_AUDIT_PATH.name, FIXED_POINT_AUDIT_PATH.name}:
        coverage = payload.get("metadata", {}).get("covered_probability_mass", 0.0)
        if coverage < MIN_ACTIVE_PROFILE_COVERAGE:
            raise ValueError(f"{path.name} failed the active-profile coverage gate")


def main() -> None:
    equilibrium = json.loads(EQUILIBRIUM_PATH.read_text(encoding="utf-8"))
    equilibrium_hash = hashlib.sha256(EQUILIBRIUM_PATH.read_bytes()).hexdigest()
    source = build_macros(
        equilibrium,
        offgrid=_validated_audit(OFFGRID_PATH, equilibrium_hash),
        intermediary=_validated_audit(INTERMEDIARY_AUDIT_PATH, equilibrium_hash),
        fixed_point=_validated_audit(FIXED_POINT_AUDIT_PATH, equilibrium_hash),
        uniform_offgrid=_validated_audit(UNIFORM_OFFGRID_PATH, equilibrium_hash),
        payoff_sensitivity=_validated_audit(
            INTERMEDIARY_PAYOFF_SENSITIVITY_PATH, equilibrium_hash
        ),
    )
    OUTPUT_PATH.write_text(source, encoding="utf-8")
    print(OUTPUT_PATH.relative_to(ROOT))


if __name__ == "__main__":
    main()
