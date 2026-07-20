"""Fully re-solve the final finite game under local parameter perturbations."""
from __future__ import annotations

import csv
from datetime import datetime
import hashlib
import json
from pathlib import Path

import numpy as np

from experiments.run_final_spatiotemporal_equilibrium import run_equilibria

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "artifacts" / "peak_shaving" / "20260712_final"
BASELINE_PATH = OUT / "spatiotemporal_equilibrium.json"
SCENARIOS = {
    "baseline": {"group": "baseline", "value": 1.0},
    "capacity_low": {"group": "capacity_scale", "value": 0.85, "capacity_scale": 0.85},
    "capacity_high": {"group": "capacity_scale", "value": 1.15, "capacity_scale": 1.15},
    "price_sensitivity_low": {
        "group": "price_sensitivity_scale", "value": 0.8,
        "price_sensitivity_scale": 0.8,
    },
    "price_sensitivity_high": {
        "group": "price_sensitivity_scale", "value": 1.2,
        "price_sensitivity_scale": 1.2,
    },
    "migration_cost_low": {
        "group": "migration_cost_scale", "value": 0.7,
        "migration_cost_scale": 0.7,
    },
    "migration_cost_high": {
        "group": "migration_cost_scale", "value": 1.3,
        "migration_cost_scale": 1.3,
    },
    "qos_threshold_low": {
        "group": "qos_threshold", "value": -0.05,
        "qos_threshold_shift": -0.05,
    },
    "qos_threshold_high": {
        "group": "qos_threshold", "value": 0.05,
        "qos_threshold_shift": 0.05,
    },
}
SOLVER_KEYS = {
    "capacity_scale",
    "price_sensitivity_scale",
    "migration_cost_scale",
    "qos_threshold_shift",
}


def _active_vectors(result: dict) -> tuple[list[list[float]], list[list[float]]]:
    game = result["dynamic"]
    vectors = []
    for prefix in ("row", "col"):
        support = game[f"{prefix}_support_vectors"]
        mix = game[f"{prefix}_mix"]
        vectors.append([
            vector for vector, probability in zip(support, mix)
            if probability > 1e-10
        ])
    return vectors[0], vectors[1]


def _scenario_kwargs(definition: dict) -> dict:
    return {key: definition[key] for key in SOLVER_KEYS if key in definition}


def _summary_row(name: str, definition: dict, result: dict) -> dict:
    uniform = result["uniform"]
    dynamic = result["dynamic"]
    comparison = result["comparison"]
    return {
        "scenario": name,
        "group": definition["group"],
        "value": definition["value"],
        "uniform_full_grid_verified": uniform["full_grid_verified"],
        "dynamic_full_grid_verified": dynamic["full_grid_verified"],
        "uniform_full_max_regret": uniform["full_max_regret"],
        "dynamic_full_max_regret": dynamic["full_max_regret"],
        "dynamic_relative_regret": dynamic["relative_full_max_regret"],
        "maximum_joint_residual": max(
            uniform["maximum_joint_residual"],
            dynamic["maximum_joint_residual"],
        ),
        "dynamic_total_demand": dynamic["expected_metrics"]["total_demand"],
        "uniform_aggregate_peak": uniform["expected_metrics"]["aggregate_peak_load"],
        "dynamic_aggregate_peak": dynamic["expected_metrics"]["aggregate_peak_load"],
        "aggregate_peak_change_percent": comparison["aggregate_peak_load_change_percent"],
        "uniform_max_provider_utilization": uniform["expected_metrics"]["maximum_provider_utilization"],
        "dynamic_max_provider_utilization": dynamic["expected_metrics"]["maximum_provider_utilization"],
        "max_provider_utilization_change_percent": comparison[
            "maximum_provider_utilization_change_percent"
        ],
        "uniform_minimum_qos": uniform["expected_metrics"]["minimum_provider_qos"],
        "dynamic_minimum_qos": dynamic["expected_metrics"]["minimum_provider_qos"],
        "minimum_qos_change": comparison["minimum_provider_qos_change"],
        "uniform_system_profit": uniform["expected_metrics"]["system_profit"],
        "dynamic_system_profit": dynamic["expected_metrics"]["system_profit"],
        "system_profit_change_percent": comparison["system_profit_change_percent"],
        "dynamic_evaluated_pairs": dynamic["evaluated_pairs"],
    }


def _write_scenario(name: str, result: dict) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"sensitivity_{name}.json"
    path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    if name == "baseline":
        BASELINE_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return path


def _source_hashes() -> dict[str, str]:
    paths = (
        Path(__file__).resolve(),
        ROOT / "experiments/run_final_spatiotemporal_equilibrium.py",
        ROOT / "experiments/final_equilibrium_tools.py",
        ROOT / "pricing_sim/spatiotemporal_game.py",
    )
    return {
        str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in paths
    }


def run_sensitivity(
    *,
    scenario_names: list[str] | None = None,
    candidate_grid: np.ndarray | None = None,
    max_oracle_rounds: int = 12,
    retail_base_grid: np.ndarray | None = None,
    dynamic_retail_slope_grid: np.ndarray | None = None,
    route_beta_grid: np.ndarray | None = None,
    write_checkpoints: bool = True,
) -> dict:
    names = list(SCENARIOS) if scenario_names is None else scenario_names
    unknown = set(names) - set(SCENARIOS)
    if unknown:
        raise ValueError(f"unknown sensitivity scenarios: {sorted(unknown)}")
    initial_vectors = None
    if "baseline" not in names and candidate_grid is None and BASELINE_PATH.exists():
        initial_vectors = _active_vectors(
            json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
        )
    rows = []
    outputs = []
    for name in names:
        definition = SCENARIOS[name]
        print(f"starting sensitivity scenario: {name}", flush=True)
        result = run_equilibria(
            candidate_grid=candidate_grid,
            max_oracle_rounds=max_oracle_rounds,
            retail_base_grid=retail_base_grid,
            dynamic_retail_slope_grid=dynamic_retail_slope_grid,
            route_beta_grid=route_beta_grid,
            initial_dynamic_vectors=initial_vectors,
            **_scenario_kwargs(definition),
        )
        row = _summary_row(name, definition, result)
        rows.append(row)
        if name == "baseline":
            initial_vectors = _active_vectors(result)
        if write_checkpoints:
            outputs.append(str(_write_scenario(name, result).relative_to(ROOT)))
        print(
            f"finished {name}: regret={row['dynamic_full_max_regret']:.6g}, "
            f"peak={row['aggregate_peak_change_percent']:.3f}%",
            flush=True,
        )
    fully_resolved = all(
        row["uniform_full_grid_verified"] and row["dynamic_full_grid_verified"]
        for row in rows
    )
    return {
        "metadata": {
            "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "fully_resolved": fully_resolved,
            "scenario_count": len(rows),
            "candidate_count": result["metadata"]["full_candidate_count"],
            "command": (
                "uv run --no-project --with numpy --with scipy --with nashpy "
                "python -m experiments.run_final_spatiotemporal_sensitivity"
            ),
            "source_sha256": _source_hashes(),
            "scenario_outputs": outputs,
        },
        "scenario_definitions": SCENARIOS,
        "rows": rows,
    }


def write_summary(result: dict) -> tuple[Path, Path]:
    OUT.mkdir(parents=True, exist_ok=True)
    json_path = OUT / "spatiotemporal_sensitivity.json"
    csv_path = OUT / "spatiotemporal_sensitivity.csv"
    json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result["rows"][0]))
        writer.writeheader()
        writer.writerows(result["rows"])
    return json_path, csv_path


def main() -> None:
    paths = write_summary(run_sensitivity())
    print(json.dumps({"outputs": [str(path.relative_to(ROOT)) for path in paths]}))


if __name__ == "__main__":
    main()
