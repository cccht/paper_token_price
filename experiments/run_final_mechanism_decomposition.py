"""Decompose temporal and spatial responses at the final equilibrium policies."""
from __future__ import annotations

import csv
from dataclasses import replace
from datetime import datetime
import hashlib
import json
from pathlib import Path

import numpy as np

from experiments.run_final_spatiotemporal_equilibrium import final_case
from pricing_sim.peak_shaving_market import (
    firm_profit,
    intermediary_profit,
    system_profit,
)
from pricing_sim.spatiotemporal_game import (
    evaluate_firm_pair_spatiotemporal,
    solve_spatiotemporal_joint_market,
)
from pricing_sim.spatiotemporal_mechanism import summarize_spatiotemporal_result

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "artifacts" / "peak_shaving" / "20260712_final"
EQUILIBRIUM_PATH = OUT / "spatiotemporal_equilibrium.json"
RETAIL_BASE_GRID = np.array([0.8, 1.1, 1.5])
ROUTE_BETA_GRID = np.array([1.5, 4.0])
MECHANISMS = {
    "neither": (False, False),
    "temporal_only": (True, False),
    "spatial_only": (False, True),
    "combined": (True, True),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _pure_vectors(game: dict) -> tuple[np.ndarray, np.ndarray]:
    output = []
    for prefix in ("row", "col"):
        vectors = np.asarray(game[f"{prefix}_support_vectors"], dtype=float)
        mix = np.asarray(game[f"{prefix}_mix"], dtype=float)
        active = vectors[mix > 1e-10]
        if len(active) != 1:
            raise ValueError("fixed-policy decomposition requires a pure equilibrium")
        output.append(active[0])
    return output[0], output[1]


def _equilibrium_policy(
    game_result: dict,
    retail_slopes: np.ndarray,
) -> tuple[object, dict]:
    config, game, _ = final_case()
    row, col = _pure_vectors(game_result)
    record = evaluate_firm_pair_spatiotemporal(
        row,
        col,
        game,
        config,
        retail_base_grid=RETAIL_BASE_GRID,
        retail_slope_grid=retail_slopes,
        route_beta_grid=ROUTE_BETA_GRID,
    )
    return record["state"], record["result"]


def _policy_rows(policy: str, game_result: dict) -> list[dict]:
    config, base_game, _ = final_case()
    retail_slopes = np.array([0.0]) if policy == "uniform" else np.array([-0.3, 0.0, 0.3])
    reference_state, reference_result = _equilibrium_policy(
        game_result, retail_slopes
    )
    route_beta = float(reference_result["intermediary_candidate"]["route_beta"])
    rows = []
    for mechanism, (temporal, spatial) in MECHANISMS.items():
        game = replace(
            base_game,
            temporal_enabled=temporal,
            spatial_enabled=spatial,
        )
        state, result = solve_spatiotemporal_joint_market(
            reference_state.retail,
            reference_state.wholesale,
            reference_state.direct,
            route_beta,
            game,
            config,
        )
        metrics = summarize_spatiotemporal_result(result)
        centroids = metrics.pop("destination_centroid_by_type")
        rows.append({
            "policy": policy,
            "mechanism": mechanism,
            "temporal_enabled": temporal,
            "spatial_enabled": spatial,
            "converged": result["joint_converged"],
            "joint_residual": result["joint_residual"],
            "rigid_centroid": centroids[0],
            "elastic_centroid": centroids[1],
            "firm_A_profit": firm_profit(0, state, result, config),
            "firm_B_profit": firm_profit(1, state, result, config),
            "intermediary_profit": intermediary_profit(state, result, config),
            "system_profit": system_profit(state, result, config),
            **metrics,
        })
    baseline = next(row for row in rows if row["mechanism"] == "neither")
    for row in rows:
        for metric in (
            "aggregate_peak_load",
            "maximum_provider_utilization",
            "minimum_provider_qos",
        ):
            row[f"{metric}_change_vs_neither"] = row[metric] - baseline[metric]
    return rows


def run_decomposition() -> dict:
    equilibrium = json.loads(EQUILIBRIUM_PATH.read_text(encoding="utf-8"))
    rows = _policy_rows("uniform", equilibrium["uniform"])
    rows.extend(_policy_rows("dynamic", equilibrium["dynamic"]))
    sources = (
        EQUILIBRIUM_PATH,
        ROOT / "pricing_sim/spatiotemporal_game.py",
        Path(__file__).resolve(),
    )
    return {
        "metadata": {
            "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "equilibrium_sha256": _sha256(EQUILIBRIUM_PATH),
            "evidence_level": "fixed-policy mechanism decomposition",
            "source_sha256": {
                str(path.relative_to(ROOT)): _sha256(path) for path in sources
            },
        },
        "policy_control": (
            "Provider and intermediary price vectors and route-beta are fixed at "
            "their combined-mechanism equilibrium values; routing and QoS are re-solved."
        ),
        "mechanisms": MECHANISMS,
        "equilibrium_metrics": {
            "uniform": equilibrium["uniform"]["expected_metrics"],
            "dynamic": equilibrium["dynamic"]["expected_metrics"],
        },
        "rows": rows,
    }


def write_outputs(result: dict) -> tuple[Path, Path]:
    json_path = OUT / "final_mechanism_decomposition.json"
    csv_path = OUT / "final_mechanism_decomposition.csv"
    json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result["rows"][0]))
        writer.writeheader()
        writer.writerows(result["rows"])
    return json_path, csv_path


def main() -> None:
    paths = write_outputs(run_decomposition())
    print(json.dumps({"outputs": [str(path.relative_to(ROOT)) for path in paths]}))


if __name__ == "__main__":
    main()
