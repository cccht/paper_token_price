"""Mechanism decomposition for a mixed submission equilibrium."""
from __future__ import annotations

from dataclasses import replace
from datetime import datetime
import hashlib
import json
from pathlib import Path

import numpy as np

from experiments.final_equilibrium_tools import SCALAR_KEYS
from experiments.run_final_spatiotemporal_equilibrium import final_case
from experiments.run_submission_intermediary_audit import _provider_prices
from pricing_sim.peak_shaving_equilibrium import expand_price
from pricing_sim.peak_shaving_market import (
    MarketState,
    firm_profit,
    intermediary_profit,
    system_profit,
)
from pricing_sim.spatiotemporal_game import solve_spatiotemporal_joint_market
from pricing_sim.spatiotemporal_mechanism import (
    solve_spatiotemporal_qos_fixed_point,
    summarize_spatiotemporal_result,
)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "artifacts" / "peak_shaving" / "20260712_expanded_response"
EQUILIBRIUM_PATH = OUT / "spatiotemporal_equilibrium_submission.json"
OUTPUT_PATH = OUT / "mechanism_decomposition_submission.json"
MECHANISMS = {
    "neither": (False, False),
    "temporal_only": (True, False),
    "spatial_only": (False, True),
    "combined": (True, True),
}
DIAGNOSTIC_KEYS = (
    "provider_A_maximum_utilization",
    "provider_B_maximum_utilization",
    "provider_A_minimum_qos",
    "provider_B_minimum_qos",
    "intermediary_weighted_route_to_A",
)
POLICY_COMPARISON_METRICS = (
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
        ROOT / "experiments/final_equilibrium_tools.py",
        ROOT / "experiments/run_final_spatiotemporal_equilibrium.py",
        ROOT / "experiments/run_submission_intermediary_audit.py",
        ROOT / "pricing_sim/spatiotemporal_game.py",
        ROOT / "pricing_sim/spatiotemporal_mechanism.py",
        ROOT / "pricing_sim/peak_shaving_market.py",
        ROOT / "pricing_sim/peak_shaving_equilibrium.py",
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def _solve_profile_market(
    *, retail, wholesale, direct, route_beta, temporal, spatial, base_game, config
):
    game = replace(base_game, temporal_enabled=temporal, spatial_enabled=spatial)
    if spatial:
        return solve_spatiotemporal_joint_market(
            retail, wholesale, direct, route_beta, game, config
        )
    routing_share = config.firm_capacity / np.sum(config.firm_capacity)
    routing = np.repeat(routing_share[:, None], config.num_periods, axis=1)
    result = solve_spatiotemporal_qos_fixed_point(
        np.vstack([retail[None, :], direct]),
        routing,
        game.demand,
        config=config,
        temporal_enabled=temporal,
        spatial_enabled=False,
        fixed_channel_shares=game.fixed_channel_shares,
        qos_shape=game.qos_shape,
    )
    result["joint_converged"] = result["converged"]
    result["joint_residual"] = result["fixed_point_residual"]
    return MarketState(retail, direct, wholesale, routing), result


def _profile_metrics(profile: dict, mechanism: tuple[bool, bool], base_game, config) -> dict:
    temporal, spatial = mechanism
    wholesale, direct = _provider_prices(profile, config)
    candidate = profile["intermediary_candidate"]
    retail = expand_price(
        candidate["retail_base"], candidate["retail_slope"], config,
        config.price_lower, config.price_upper,
    )
    state, result = _solve_profile_market(
        retail=retail,
        wholesale=wholesale,
        direct=direct,
        route_beta=candidate["route_beta"],
        temporal=temporal,
        spatial=spatial,
        base_game=base_game,
        config=config,
    )
    metrics = summarize_spatiotemporal_result(result)
    metrics.pop("destination_centroid_by_type")
    intermediary_demand = np.asarray(result["demand"][0], dtype=float)
    routed_total = float(np.sum(intermediary_demand))
    return {
        **metrics,
        "provider_A_maximum_utilization": float(np.max(result["utilization"][0])),
        "provider_B_maximum_utilization": float(np.max(result["utilization"][1])),
        "provider_A_minimum_qos": float(np.min(result["qos_firm"][0])),
        "provider_B_minimum_qos": float(np.min(result["qos_firm"][1])),
        "intermediary_weighted_route_to_A": float(
            np.sum(state.routing[0] * intermediary_demand) / max(routed_total, 1e-12)
        ),
        "firm_A_profit": firm_profit(0, state, result, config),
        "firm_B_profit": firm_profit(1, state, result, config),
        "intermediary_profit": intermediary_profit(state, result, config),
        "system_profit": system_profit(state, result, config),
        "joint_converged": result["joint_converged"],
        "joint_residual": result["joint_residual"],
    }


def _aggregate_mechanism(
    *, policy: str, name: str, mechanism: tuple, profiles: list[dict], base_game, config
) -> dict:
    aggregate = {key: 0.0 for key in (*SCALAR_KEYS, *DIAGNOSTIC_KEYS)}
    maximum_residual = 0.0
    all_converged = True
    for profile in profiles:
        weight = float(profile["weight"])
        values = _profile_metrics(profile, mechanism, base_game, config)
        for key in aggregate:
            aggregate[key] += weight * float(values[key])
        maximum_residual = max(maximum_residual, float(values["joint_residual"]))
        all_converged = all_converged and bool(values["joint_converged"])
    return {
        "policy": policy,
        "mechanism": name,
        "temporal_enabled": mechanism[0],
        "spatial_enabled": mechanism[1],
        "profile_count": len(profiles),
        "probability_mass": sum(float(item["weight"]) for item in profiles),
        "all_converged": all_converged,
        "maximum_joint_residual": maximum_residual,
        **aggregate,
    }


def _add_neither_changes(rows: list[dict]) -> None:
    baseline = next(item for item in rows if item["mechanism"] == "neither")
    for row in rows:
        for metric in (
            "aggregate_peak_load",
            "maximum_provider_utilization",
            "minimum_provider_qos",
        ):
            row[f"{metric}_change_vs_neither"] = row[metric] - baseline[metric]


def _aggregate_policy(policy: str, game_result: dict, base_game, config) -> list[dict]:
    profiles = game_result["active_profiles"]
    if not profiles:
        raise ValueError(f"{policy} equilibrium has no active profiles")
    rows = [
        _aggregate_mechanism(
            policy=policy,
            name=name,
            mechanism=mechanism,
            profiles=profiles,
            base_game=base_game,
            config=config,
        )
        for name, mechanism in MECHANISMS.items()
    ]
    _add_neither_changes(rows)
    return rows


def _policy_comparisons(rows: list[dict]) -> list[dict]:
    indexed = {(row["policy"], row["mechanism"]): row for row in rows}
    output = []
    for mechanism in MECHANISMS:
        uniform = indexed[("uniform", mechanism)]
        dynamic = indexed[("dynamic", mechanism)]
        values = {"mechanism": mechanism}
        for metric in POLICY_COMPARISON_METRICS:
            change = dynamic[metric] - uniform[metric]
            values[f"{metric}_change"] = change
            values[f"{metric}_change_percent"] = (
                100.0 * change / max(abs(uniform[metric]), 1e-12)
            )
        output.append(values)
    return output


def run_decomposition(*, equilibrium_path: Path = EQUILIBRIUM_PATH) -> dict:
    equilibrium_path = Path(equilibrium_path).resolve()
    equilibrium = json.loads(equilibrium_path.read_text(encoding="utf-8"))
    config, game, _ = final_case(**equilibrium.get("scenario", {}))
    rows = _aggregate_policy("uniform", equilibrium["uniform"], game, config)
    rows.extend(_aggregate_policy("dynamic", equilibrium["dynamic"], game, config))
    return {
        "metadata": {
            "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "equilibrium_path": str(equilibrium_path.relative_to(ROOT)),
            "equilibrium_sha256": _sha256(equilibrium_path),
            "evidence_level": "fixed-policy mixed-profile mechanism decomposition",
            "source_sha256": _source_hashes(),
            "command": (
                "uv run --no-project --with numpy python -m "
                "experiments.run_submission_mechanism_decomposition"
            ),
        },
        "policy_control": (
            "Provider and intermediary price vectors are held fixed. When spatial response "
            "is disabled, channel shares and capacity-proportional provider routing are "
            "fixed; otherwise routing and QoS are jointly re-solved."
        ),
        "expectation_order": (
            "Metrics are evaluated for each active provider pair and then averaged with "
            "equilibrium probability weights."
        ),
        "mechanisms": MECHANISMS,
        "rows": rows,
        "policy_comparisons": _policy_comparisons(rows),
    }


def main() -> None:
    result = run_decomposition()
    OUT.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
        "rows": len(result["rows"]),
        "all_converged": all(item["all_converged"] for item in result["rows"]),
    }, indent=2))


if __name__ == "__main__":
    main()
