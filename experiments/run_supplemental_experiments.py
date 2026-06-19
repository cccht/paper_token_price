"""Generate supplemental pricing and empirical-calibration artifacts."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
import sys
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
for import_path in (PROJECT_ROOT, SCRIPT_DIR):
    path_text = str(import_path)
    if path_text not in sys.path:
        sys.path.insert(0, path_text)

from pricing_sim.calibration import fit_qos_curve, load_controlled_aggregate
from pricing_sim.config import SimulationConfig
from pricing_sim.supplemental_experiments import (
    billing_ablation_records,
    coarse_grid_reference_records,
    constraint_ablation_records,
    empirical_profile_records,
    fairness_records,
    rule_baseline_records,
    scalability_records,
)


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _calibration_row(result) -> dict[str, Any]:
    return {
        "capacity_concurrency": result.capacity_concurrency,
        "threshold": result.threshold,
        "strength": result.strength,
        "rmse": result.rmse,
    }


def _calibration_points(source: Path, result) -> list[dict[str, Any]]:
    return [
        {
            "source": str(source),
            "concurrency": concurrency,
            "normalized_utilization": utilization,
            "observed_qos": observed,
            "fitted_qos": fitted,
        }
        for concurrency, utilization, observed, fitted in zip(
            result.concurrency,
            result.utilization,
            result.observed_qos,
            result.fitted_qos,
        )
    ]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vllm-aggregate", type=Path, action="append", required=True)
    parser.add_argument("--output-root", type=Path, default=PROJECT_ROOT / "artifacts" / "supplemental")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    output = args.output_root / datetime.now().strftime("%Y%m%d-%H%M%S")
    output.mkdir(parents=True)
    config = SimulationConfig.default()
    tables = {
        "billing_ablation": billing_ablation_records(config),
        "coarse_grid_reference": coarse_grid_reference_records(config),
        "constraint_ablation": constraint_ablation_records(config),
        "rule_baselines": rule_baseline_records(config),
        "scalability": scalability_records(config),
        "fairness": fairness_records(config),
    }
    for name, rows in tables.items():
        _write_csv(output / f"{name}.csv", rows)
    calibrations = []
    calibration_points = []
    profiles = []
    for source in args.vllm_aggregate:
        result = fit_qos_curve(load_controlled_aggregate(source))
        calibrations.append({"source": str(source), **_calibration_row(result)})
        calibration_points.extend(_calibration_points(source, result))
        profiles.append((source.parent.parent.name, result.threshold, result.strength))
    _write_csv(output / "qos_calibration.csv", calibrations)
    _write_csv(output / "qos_calibration_points.csv", calibration_points)
    _write_csv(output / "empirical_profiles.csv", empirical_profile_records(config, profiles=tuple(profiles)))
    (output / "metadata.json").write_text(
        json.dumps({"config": asdict(config), "inputs": [str(path) for path in args.vllm_aggregate]}, default=str, indent=2),
        encoding="utf-8",
    )
    print(f"artifacts={output}")


if __name__ == "__main__":
    main()
