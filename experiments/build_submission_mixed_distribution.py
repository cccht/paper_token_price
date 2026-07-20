"""Build weighted outcome distributions for the mixed submission equilibrium."""
from __future__ import annotations

from datetime import datetime
import hashlib
import json
from pathlib import Path

import numpy as np

from experiments.final_equilibrium_tools import SCALAR_KEYS
from experiments.run_final_spatiotemporal_equilibrium import final_case
from experiments.run_submission_intermediary_audit import _provider_prices
from pricing_sim.peak_shaving_equilibrium import expand_price
from pricing_sim.peak_shaving_market import firm_profit, intermediary_profit, system_profit
from pricing_sim.spatiotemporal_game import solve_spatiotemporal_joint_market
from pricing_sim.spatiotemporal_mechanism import summarize_spatiotemporal_result

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "artifacts" / "peak_shaving" / "20260712_expanded_response"
EQUILIBRIUM_PATH = OUT / "spatiotemporal_equilibrium_submission.json"
OUTPUT_PATH = OUT / "mixed_outcome_distribution_submission.json"
QUANTILES = (0.05, 0.50, 0.95)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        Path(__file__).resolve(),
        ROOT / "experiments/run_submission_intermediary_audit.py",
        ROOT / "pricing_sim/spatiotemporal_game.py",
        ROOT / "pricing_sim/spatiotemporal_mechanism.py",
        ROOT / "pricing_sim/peak_shaving_market.py",
        ROOT / "pricing_sim/peak_shaving_equilibrium.py",
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def weighted_quantile(values: np.ndarray, weights: np.ndarray, quantiles=QUANTILES) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    weights = np.asarray(weights, dtype=float)
    requested = np.asarray(quantiles, dtype=float)
    if values.ndim != 1 or weights.shape != values.shape:
        raise ValueError("values and weights must be one-dimensional with equal length")
    if not np.all(np.isfinite(values)):
        raise ValueError("values must be finite")
    if not np.all(np.isfinite(weights)) or np.any(weights < 0.0) or not np.sum(weights) > 0.0:
        raise ValueError("weights must be nonnegative with positive total mass")
    if not np.all(np.isfinite(requested)) or np.any((requested < 0.0) | (requested > 1.0)):
        raise ValueError("quantiles must lie in [0, 1]")
    order = np.argsort(values)
    ordered_values = values[order]
    ordered_weights = weights[order]
    cumulative = np.cumsum(ordered_weights) / np.sum(ordered_weights)
    cumulative[-1] = 1.0
    indices = np.searchsorted(cumulative, requested, side="left")
    return ordered_values[np.minimum(indices, ordered_values.size - 1)]


def _evaluate_profile(profile: dict, game, config) -> dict:
    wholesale, direct = _provider_prices(profile, config)
    candidate = profile["intermediary_candidate"]
    retail = expand_price(
        candidate["retail_base"], candidate["retail_slope"], config,
        config.price_lower, config.price_upper,
    )
    state, result = solve_spatiotemporal_joint_market(
        retail, wholesale, direct, candidate["route_beta"], game, config
    )
    metrics = summarize_spatiotemporal_result(result)
    metrics.pop("destination_centroid_by_type")
    intermediary_demand = np.asarray(result["demand"][0], dtype=float)
    metrics.update({
        "firm_A_profit": firm_profit(0, state, result, config),
        "firm_B_profit": firm_profit(1, state, result, config),
        "intermediary_profit": intermediary_profit(state, result, config),
        "system_profit": system_profit(state, result, config),
        "retail_base": candidate["retail_base"],
        "retail_slope": candidate["retail_slope"],
        "route_beta": candidate["route_beta"],
        "intermediary_weighted_route_to_A": float(
            np.sum(state.routing[0] * intermediary_demand)
            / max(float(np.sum(intermediary_demand)), 1e-12)
        ),
        "joint_residual": result["joint_residual"],
        "joint_converged": result["joint_converged"],
    })
    return metrics


def _distribution(game_result: dict, game, config) -> dict:
    profiles = game_result["active_profiles"]
    weights = np.asarray([item["weight"] for item in profiles], dtype=float)
    weights /= np.sum(weights)
    records = [_evaluate_profile(item, game, config) for item in profiles]
    metric_names = (
        *SCALAR_KEYS,
        "retail_base",
        "retail_slope",
        "route_beta",
        "intermediary_weighted_route_to_A",
    )
    summary = {}
    maximum_mean_error = 0.0
    for metric in metric_names:
        values = np.asarray([item[metric] for item in records], dtype=float)
        mean = float(np.sum(weights * values))
        quantile = weighted_quantile(values, weights)
        summary[metric] = {
            "mean": mean,
            "p05": float(quantile[0]),
            "p50": float(quantile[1]),
            "p95": float(quantile[2]),
            "minimum": float(np.min(values)),
            "maximum": float(np.max(values)),
        }
        if metric in game_result["expected_metrics"]:
            maximum_mean_error = max(
                maximum_mean_error,
                abs(mean - float(game_result["expected_metrics"][metric])),
            )
    return {
        "active_profile_count": len(profiles),
        "probability_mass": float(np.sum(weights)),
        "all_joint_converged": all(item["joint_converged"] for item in records),
        "maximum_joint_residual": max(item["joint_residual"] for item in records),
        "maximum_expected_metric_reconstruction_error": maximum_mean_error,
        "metrics": summary,
    }


def build_distribution(*, equilibrium_path: Path = EQUILIBRIUM_PATH) -> dict:
    equilibrium_path = Path(equilibrium_path).resolve()
    equilibrium = json.loads(equilibrium_path.read_text(encoding="utf-8"))
    config, game, _ = final_case(**equilibrium.get("scenario", {}))
    return {
        "metadata": {
            "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "equilibrium_path": str(equilibrium_path.relative_to(ROOT)),
            "equilibrium_sha256": _sha256(equilibrium_path),
            "quantiles": list(QUANTILES),
            "source_sha256": _source_hashes(),
            "command": (
                "uv run --no-project --with numpy python -m "
                "experiments.build_submission_mixed_distribution"
            ),
        },
        "uniform": _distribution(equilibrium["uniform"], game, config),
        "dynamic": _distribution(equilibrium["dynamic"], game, config),
        "interpretation_boundary": (
            "Quantiles describe outcomes across independently mixed provider strategies; "
            "they are not sampling uncertainty or confidence intervals."
        ),
    }


def main() -> None:
    result = build_distribution()
    OUTPUT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
        "dynamic_profiles": result["dynamic"]["active_profile_count"],
        "maximum_reconstruction_error": result["dynamic"][
            "maximum_expected_metric_reconstruction_error"
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
