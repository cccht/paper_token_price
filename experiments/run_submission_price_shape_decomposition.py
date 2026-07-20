"""Separate price-shape effects from level and equilibrium-composition effects."""
from __future__ import annotations

from datetime import datetime
import hashlib
import json
from pathlib import Path

import numpy as np

from experiments.run_final_spatiotemporal_equilibrium import ROOT, final_case
from pricing_sim.peak_shaving_equilibrium import FirmParams, expand_price
from pricing_sim.peak_shaving_market import (
    firm_profit,
    intermediary_profit,
    system_profit,
)
from pricing_sim.spatiotemporal_game import solve_spatiotemporal_joint_market
from pricing_sim.spatiotemporal_mechanism import summarize_spatiotemporal_result

OUT = ROOT / "artifacts" / "peak_shaving" / "20260712_expanded_response"
EQUILIBRIUM_PATH = OUT / "spatiotemporal_equilibrium_submission.json"
OUTPUT_PATH = OUT / "price_shape_decomposition_submission.json"
METRICS = (
    "aggregate_peak_load",
    "maximum_provider_utilization",
    "minimum_provider_qos",
    "system_profit",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        Path(__file__).resolve(),
        ROOT / "pricing_sim/peak_shaving_equilibrium.py",
        ROOT / "pricing_sim/peak_shaving_market.py",
        ROOT / "pricing_sim/spatiotemporal_game.py",
        ROOT / "pricing_sim/spatiotemporal_mechanism.py",
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def _flatten_vector(vector: np.ndarray) -> np.ndarray:
    values = np.asarray(vector, dtype=float)
    if values.shape != (4,):
        raise ValueError("provider vector must contain four coefficients")
    flattened = values.copy()
    flattened[[1, 3]] = 0.0
    return flattened


def _mean_flattened_schedule(schedule: np.ndarray) -> np.ndarray:
    values = np.asarray(schedule, dtype=float)
    if values.ndim not in (1, 2) or values.shape[-1] < 1:
        raise ValueError("price schedule must have a nonempty period axis")
    means = np.mean(values, axis=-1, keepdims=True)
    return np.repeat(means, values.shape[-1], axis=-1)


def _price_schedules(profile: dict, config, mode: str) -> tuple[np.ndarray, ...]:
    vectors = [np.asarray(profile[key], dtype=float) for key in ("row_vector", "col_vector")]
    if mode == "coefficient_base":
        vectors = [_flatten_vector(vector) for vector in vectors]
    elif mode != "period_mean":
        raise ValueError(f"unknown flattening mode: {mode}")
    firms = [FirmParams.from_vector(vector) for vector in vectors]
    wholesale = np.vstack([firm.wholesale(config) for firm in firms])
    direct = np.vstack([firm.direct(config) for firm in firms])
    response = profile["intermediary_candidate"]
    retail = expand_price(
        float(response["retail_base"]),
        0.0 if mode == "coefficient_base" else float(response["retail_slope"]),
        config,
        config.price_lower,
        config.price_upper,
    )
    if mode == "period_mean":
        wholesale = _mean_flattened_schedule(wholesale)
        direct = _mean_flattened_schedule(direct)
        retail = _mean_flattened_schedule(retail)
    return wholesale, direct, retail


def _flattened_profile_metrics(
    profile: dict, game, config, mode: str
) -> dict[str, float | bool]:
    wholesale, direct, retail = _price_schedules(profile, config, mode)
    response = profile["intermediary_candidate"]
    state, result = solve_spatiotemporal_joint_market(
        retail,
        wholesale,
        direct,
        float(response["route_beta"]),
        game,
        config,
    )
    summary = summarize_spatiotemporal_result(result)
    return {
        "aggregate_peak_load": float(summary["aggregate_peak_load"]),
        "maximum_provider_utilization": float(summary["maximum_provider_utilization"]),
        "minimum_provider_qos": float(summary["minimum_provider_qos"]),
        "firm_A_profit": firm_profit(0, state, result, config),
        "firm_B_profit": firm_profit(1, state, result, config),
        "intermediary_profit": intermediary_profit(state, result, config),
        "system_profit": system_profit(state, result, config),
        "joint_converged": bool(result["joint_converged"]),
        "joint_residual": float(result["joint_residual"]),
    }


def _weighted_flattened(game_result: dict, game, config, mode: str) -> dict:
    profiles = game_result["active_profiles"]
    if not profiles:
        raise ValueError("equilibrium has no active profiles")
    totals = {key: 0.0 for key in (*METRICS, "firm_A_profit", "firm_B_profit", "intermediary_profit")}
    mass = 0.0
    residual = 0.0
    converged = True
    for profile in profiles:
        weight = float(profile["weight"])
        values = _flattened_profile_metrics(profile, game, config, mode)
        mass += weight
        for key in totals:
            totals[key] += weight * float(values[key])
        residual = max(residual, float(values["joint_residual"]))
        converged = converged and bool(values["joint_converged"])
    return {
        **totals,
        "profile_count": len(profiles),
        "probability_mass": mass,
        "all_converged": converged,
        "maximum_joint_residual": residual,
    }


def _component_rows(uniform: dict, flattened: dict, dynamic: dict) -> list[dict]:
    rows = []
    for metric in METRICS:
        overall = float(dynamic[metric] - uniform[metric])
        shape = float(dynamic[metric] - flattened[metric])
        remainder = float(flattened[metric] - uniform[metric])
        rows.append({
            "metric": metric,
            "uniform_equilibrium": float(uniform[metric]),
            "flattened_dynamic_profiles": float(flattened[metric]),
            "dynamic_equilibrium": float(dynamic[metric]),
            "overall_change": overall,
            "shape_change": shape,
            "level_and_mix_remainder": remainder,
            "identity_error": overall - shape - remainder,
        })
    return rows


def run_decomposition(*, equilibrium_path: Path = EQUILIBRIUM_PATH) -> dict:
    equilibrium_path = Path(equilibrium_path).resolve()
    equilibrium = json.loads(equilibrium_path.read_text(encoding="utf-8"))
    config, game, _ = final_case(**equilibrium.get("scenario", {}))
    uniform = equilibrium["uniform"]["expected_metrics"]
    dynamic = equilibrium["dynamic"]["expected_metrics"]
    mean_flattened_uniform = _weighted_flattened(
        equilibrium["uniform"], game, config, "period_mean"
    )
    mean_flattened_dynamic = _weighted_flattened(
        equilibrium["dynamic"], game, config, "period_mean"
    )
    base_flattened_dynamic = _weighted_flattened(
        equilibrium["dynamic"], game, config, "coefficient_base"
    )
    uniform_error = {
        key: float(mean_flattened_uniform[key] - uniform[key]) for key in METRICS
    }
    return {
        "metadata": {
            "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "equilibrium_path": str(equilibrium_path.relative_to(ROOT)),
            "equilibrium_sha256": _sha256(equilibrium_path),
            "evidence_level": "fixed-profile price-shape decomposition",
            "source_sha256": _source_hashes(),
            "command": (
                "uv run --no-project --with numpy --with scipy python -m "
                "experiments.run_submission_price_shape_decomposition"
            ),
        },
        "control": (
            "For every active dynamic provider pair, each realised wholesale, direct, "
            "and intermediary retail schedule is replaced by its own period mean. "
            "Route beta and equilibrium pair weights are held fixed before the market "
            "fixed point is re-solved."
        ),
        "interpretation_boundary": (
            "This fixed-profile accounting decomposition is not a provider or "
            "intermediary re-equilibrium."
        ),
        "uniform_flattening_check": {
            "maximum_absolute_error": max(abs(value) for value in uniform_error.values()),
            "errors": uniform_error,
            **mean_flattened_uniform,
        },
        "mean_flattened_dynamic_profiles": mean_flattened_dynamic,
        "components": _component_rows(uniform, mean_flattened_dynamic, dynamic),
        "coefficient_base_flattened_dynamic_profiles": base_flattened_dynamic,
        "coefficient_base_components": _component_rows(
            uniform, base_flattened_dynamic, dynamic
        ),
    }


def main() -> None:
    result = run_decomposition()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
        "all_converged": result["mean_flattened_dynamic_profiles"]["all_converged"],
        "maximum_residual": result["mean_flattened_dynamic_profiles"]["maximum_joint_residual"],
    }, indent=2))


if __name__ == "__main__":
    main()
