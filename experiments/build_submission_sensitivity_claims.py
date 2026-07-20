"""Build machine-readable claims from the validated sensitivity summary."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from experiments.build_submission_sensitivity_table import SCENARIO_ORDER

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = ROOT / "artifacts" / "peak_shaving" / "20260712_expanded_response"
SUMMARY_PATH = ARTIFACT_DIR / "spatiotemporal_sensitivity_submission.json"
OUTPUT_PATH = ARTIFACT_DIR / "sensitivity_claims_submission.json"
ZERO_TOLERANCE = 1e-9
EFFECT_TOLERANCE = 1e-9


def _source_hashes() -> dict[str, str]:
    paths = (
        Path(__file__).resolve(),
        ROOT / "experiments/build_submission_sensitivity_table.py",
    )
    return {
        str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in paths
    }


def _values(rows: list[dict], key: str) -> list[float]:
    values = [float(row[key]) for row in rows]
    if not all(math.isfinite(value) for value in values):
        raise ValueError(f"{key} contains a non-finite value")
    return values


def _improvement_range(rows: list[dict], key: str, *, positive: bool) -> dict:
    values = _values(rows, key)
    improved = all(value > EFFECT_TOLERANCE for value in values) if positive else all(
        value < -EFFECT_TOLERANCE for value in values
    )
    return {
        "minimum": min(values),
        "maximum": max(values),
        "all_improve": improved,
    }


def _profit_summary(rows: list[dict]) -> dict:
    values = _values(rows, "market_profit_change_percent")
    negative = sum(value < -ZERO_TOLERANCE for value in values)
    positive = sum(value > ZERO_TOLERANCE for value in values)
    zero = len(values) - negative - positive
    return {
        "minimum": min(values),
        "maximum": max(values),
        "negative_count": negative,
        "zero_count": zero,
        "positive_count": positive,
        "sign_robust": negative == len(values) or positive == len(values),
    }


def summarize_rows(rows: list[dict]) -> dict:
    uniform_regret = _values(rows, "uniform_full_max_regret")
    dynamic_regret = _values(rows, "dynamic_full_max_regret")
    return {
        "scenario_count": len(rows),
        "aggregate_peak_change_percent": _improvement_range(
            rows, "aggregate_peak_change_percent", positive=False
        ),
        "maximum_provider_utilization_change_percent": _improvement_range(
            rows, "maximum_provider_utilization_change_percent", positive=False
        ),
        "minimum_provider_qos_change": _improvement_range(
            rows, "minimum_provider_qos_change", positive=True
        ),
        "market_profit_change_percent": _profit_summary(rows),
        "maximum_full_regret": max((*uniform_regret, *dynamic_regret)),
        "maximum_joint_residual": max(
            _values(rows, "maximum_joint_residual")
        ),
    }


def build_claims(summary: dict, *, source_sha256: str) -> dict:
    metadata = summary.get("metadata", {})
    rows = summary.get("rows", [])
    if metadata.get("scenario_count") != len(SCENARIO_ORDER):
        raise ValueError("sensitivity scenario count is not nine")
    if metadata.get("provider_candidate_count") != 1576:
        raise ValueError("provider candidate count is not 1576")
    if tuple(row.get("scenario") for row in rows) != SCENARIO_ORDER:
        raise ValueError("sensitivity scenario order is invalid")
    return {
        "metadata": {
            "source_summary_sha256": source_sha256,
            "source_sha256": _source_hashes(),
            "provider_candidate_count": 1576,
            "scope": "baseline and eight local finite-game re-solves",
        },
        "claims": summarize_rows(rows),
        "interpretation_boundary": (
            "Ranges and directions apply only to the declared common finite candidate "
            "set and the eight local perturbations; they are not continuous-domain or "
            "production guarantees. Two-dimensional uniform-policy off-grid checks cover "
            "all nine cases; the four-dimensional dynamic-policy off-grid and active-profile "
            "audits cover the baseline only."
        ),
    }


def validate_claims(
    artifact: dict,
    *,
    summary: dict,
    expected_summary_hash: str,
) -> dict:
    recorded_hash = artifact.get("metadata", {}).get("source_summary_sha256")
    if recorded_hash != expected_summary_hash:
        raise ValueError("sensitivity claims summary SHA-256 mismatch")
    expected = build_claims(summary, source_sha256=expected_summary_hash)
    if artifact != expected:
        raise ValueError("sensitivity claims do not match the summary")
    return {
        "passed": True,
        "scenario_count": expected["claims"]["scenario_count"],
        "provider_candidate_count": expected["metadata"][
            "provider_candidate_count"
        ],
    }


def main() -> None:
    source = SUMMARY_PATH.read_bytes()
    claims = build_claims(
        json.loads(source),
        source_sha256=hashlib.sha256(source).hexdigest(),
    )
    OUTPUT_PATH.write_text(json.dumps(claims, indent=2), encoding="utf-8")
    print(OUTPUT_PATH.relative_to(ROOT))


if __name__ == "__main__":
    main()
