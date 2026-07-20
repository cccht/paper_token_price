"""Measure provider-payoff sensitivity to independently audited responses."""
from __future__ import annotations

from datetime import datetime
import hashlib
import json
from pathlib import Path

import numpy as np

from experiments.run_final_spatiotemporal_equilibrium import ROOT, final_case
from pricing_sim.peak_shaving_equilibrium import FirmParams, expand_price
from pricing_sim.peak_shaving_market import firm_profit
from pricing_sim.spatiotemporal_game import solve_spatiotemporal_joint_market


OUT = ROOT / "artifacts" / "peak_shaving" / "20260712_expanded_response"
EQUILIBRIUM_PATH = OUT / "spatiotemporal_equilibrium_submission.json"
INTERMEDIARY_AUDIT_PATH = OUT / "intermediary_globality_audit_submission.json"
OUTPUT_PATH = OUT / "intermediary_payoff_sensitivity_submission.json"
PROVIDERS = ("firm_A", "firm_B")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _expected_active_profiles(game: dict) -> set[tuple[int, int]]:
    return {
        (int(row), int(col))
        for row in game["row_support_indices"]
        for col in game["col_support_indices"]
    }


def _validated_records(records: list[dict], game: dict) -> dict[tuple[int, int], dict]:
    indexed = {
        (int(record["row_index"]), int(record["col_index"])): record
        for record in records
    }
    expected = _expected_active_profiles(game)
    if len(indexed) != len(records) or set(indexed) != expected:
        raise ValueError("records must form a complete active profile matrix")
    return indexed


def _weighted_provider_change(records: list[dict], provider: str) -> dict:
    changes = [
        float(record["global_provider_payoffs"][provider])
        - float(record["stored_provider_payoffs"][provider])
        for record in records
    ]
    weights = [float(record["equilibrium_weight"]) for record in records]
    return {
        "weighted_signed_change": float(np.dot(weights, changes)),
        "weighted_absolute_change": float(np.dot(weights, np.abs(changes))),
    }


def _active_support_regret(
    indexed: dict[tuple[int, int], dict], game: dict, provider: str
) -> float:
    row_indices = [int(value) for value in game["row_support_indices"]]
    col_indices = [int(value) for value in game["col_support_indices"]]
    row_mix = np.asarray(game["row_mix"], dtype=float)
    col_mix = np.asarray(game["col_mix"], dtype=float)
    if provider == "firm_A":
        payoffs = np.asarray([
            sum(
                col_mix[j]
                * indexed[(row, col)]["global_provider_payoffs"][provider]
                for j, col in enumerate(col_indices)
            )
            for row in row_indices
        ])
        expected = float(np.dot(row_mix, payoffs))
    else:
        payoffs = np.asarray([
            sum(
                row_mix[i]
                * indexed[(row, col)]["global_provider_payoffs"][provider]
                for i, row in enumerate(row_indices)
            )
            for col in col_indices
        ])
        expected = float(np.dot(col_mix, payoffs))
    return max(float(np.max(payoffs) - expected), 0.0)


def summarize_provider_payoff_sensitivity(records: list[dict], game: dict) -> dict:
    """Summarize response-induced payoff changes on the active profile matrix."""
    indexed = _validated_records(records, game)
    summary = {
        "covered_probability_mass": sum(
            float(record["equilibrium_weight"]) for record in records
        )
    }
    profile_changes = []
    for provider in PROVIDERS:
        values = _weighted_provider_change(records, provider)
        values["active_support_regret"] = _active_support_regret(
            indexed, game, provider
        )
        summary[provider] = values
        for record in records:
            change = (
                float(record["global_provider_payoffs"][provider])
                - float(record["stored_provider_payoffs"][provider])
            )
            profile_changes.append((abs(change), provider, change, record))
    _, provider, change, record = max(profile_changes, key=lambda item: item[0])
    summary["maximum_active_support_regret"] = max(
        summary[provider]["active_support_regret"] for provider in PROVIDERS
    )
    summary["maximum_absolute_profile_change"] = {
        "provider": provider,
        "change": change,
        "row_index": int(record["row_index"]),
        "col_index": int(record["col_index"]),
    }
    return summary


def _provider_prices(profile: dict, config) -> tuple[np.ndarray, np.ndarray]:
    firms = [
        FirmParams.from_vector(np.asarray(profile[key], dtype=float))
        for key in ("row_vector", "col_vector")
    ]
    return (
        np.vstack([firm.wholesale(config) for firm in firms]),
        np.vstack([firm.direct(config) for firm in firms]),
    )


def _provider_payoffs(candidate: dict, profile: dict, game, config) -> dict:
    wholesale, direct = _provider_prices(profile, config)
    retail = expand_price(
        float(candidate["retail_base"]),
        float(candidate["retail_slope"]),
        config,
        config.price_lower,
        config.price_upper,
    )
    state, result = solve_spatiotemporal_joint_market(
        retail,
        wholesale,
        direct,
        float(candidate["route_beta"]),
        game,
        config,
    )
    return {
        "provider_payoffs": {
            "firm_A": firm_profit(0, state, result, config),
            "firm_B": firm_profit(1, state, result, config),
        },
        "joint_converged": bool(result["joint_converged"]),
        "joint_residual": float(result["joint_residual"]),
    }


def _build_records(equilibrium: dict, audit: dict, game, config) -> list[dict]:
    profiles = {
        (int(item["row_index"]), int(item["col_index"])): item
        for item in equilibrium["dynamic"]["active_profiles"]
    }
    records = []
    for audit_record in audit["records"]:
        key = (int(audit_record["row_index"]), int(audit_record["col_index"]))
        profile = profiles[key]
        stored = _provider_payoffs(audit_record["stored_candidate"], profile, game, config)
        global_result = _provider_payoffs(
            audit_record["global_candidate"], profile, game, config
        )
        records.append({
            "row_index": key[0],
            "col_index": key[1],
            "equilibrium_weight": float(audit_record["equilibrium_weight"]),
            "stored_provider_payoffs": stored["provider_payoffs"],
            "global_provider_payoffs": global_result["provider_payoffs"],
            "stored_joint_converged": stored["joint_converged"],
            "global_joint_converged": global_result["joint_converged"],
            "stored_joint_residual": stored["joint_residual"],
            "global_joint_residual": global_result["joint_residual"],
        })
    _validated_records(records, equilibrium["dynamic"])
    return records


def build_payoff_sensitivity(
    *,
    equilibrium_path: Path = EQUILIBRIUM_PATH,
    intermediary_audit_path: Path = INTERMEDIARY_AUDIT_PATH,
) -> dict:
    equilibrium_path = Path(equilibrium_path).resolve()
    intermediary_audit_path = Path(intermediary_audit_path).resolve()
    equilibrium = json.loads(equilibrium_path.read_text(encoding="utf-8"))
    audit = json.loads(intermediary_audit_path.read_text(encoding="utf-8"))
    equilibrium_hash = _sha256(equilibrium_path)
    if audit["metadata"]["equilibrium_sha256"] != equilibrium_hash:
        raise ValueError("intermediary audit is not bound to the equilibrium artifact")
    config, game, _ = final_case(**equilibrium.get("scenario", {}))
    records = _build_records(equilibrium, audit, game, config)
    summary = summarize_provider_payoff_sensitivity(records, equilibrium["dynamic"])
    summary["maximum_joint_residual"] = max(
        max(record["stored_joint_residual"], record["global_joint_residual"])
        for record in records
    )
    summary["all_joint_converged"] = all(
        record["stored_joint_converged"] and record["global_joint_converged"]
        for record in records
    )
    sources = (Path(__file__).resolve(),)
    return {
        "metadata": {
            "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "equilibrium_sha256": equilibrium_hash,
            "intermediary_audit_sha256": _sha256(intermediary_audit_path),
            "active_profile_count": len(records),
            "source_sha256": {
                str(path.relative_to(ROOT)): _sha256(path) for path in sources
            },
            "command": (
                "uv run --no-project --with numpy --with scipy python -m "
                "experiments.build_submission_intermediary_payoff_sensitivity"
            ),
        },
        "summary": summary,
        "records": records,
        "interpretation_boundary": (
            "Provider-payoff sensitivity is evaluated only on the complete active "
            "equilibrium profile matrix, not on all 1,576 unilateral deviations."
        ),
    }


def main() -> None:
    result = build_payoff_sensitivity()
    OUTPUT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
        "maximum_active_support_regret": result["summary"][
            "maximum_active_support_regret"
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
