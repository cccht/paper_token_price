"""Run the three-layer intermediary pricing experiment."""

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

from pricing_sim.intermediary_market import IntermediaryConfig, ThreeLayerResult, run_three_layer_smoke
from experiments.pub_figures import plot_policy_detail, plot_baseline_comparison
import numpy as np


def _jsonable(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    return value


def _record_config(result: ThreeLayerResult, config: IntermediaryConfig) -> IntermediaryConfig:
    if result.policy != "single_intermediary":
        return config
    data = {**config.__dict__}
    data["intermediary_capacity"] = np.array([float(np.sum(config.intermediary_capacity))])
    data["brand_quality"] = np.array([1.0])
    return IntermediaryConfig.default(**data)


def _record(result: ThreeLayerResult, config: IntermediaryConfig) -> dict[str, Any]:
    record_config = _record_config(result, config)
    return _jsonable({
        "policy": result.policy,
        "config": asdict(record_config),
        "wholesale_prices": result.wholesale_prices,
        "retail_prices": result.retail_prices,
        "capacity": result.capacity,
        "shares": result.shares,
        "demand": result.demand,
        "utilization": result.utilization,
        "qos": result.qos,
        "platform_revenue": result.platform_revenue,
        "intermediary_profit": result.intermediary_profit,
        "system_profit": result.system_profit,
        "intermediary_components": result.intermediary_components,
        "diagnostics": result.diagnostics,
    })


def _summary_row(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "policy": record["policy"],
        "platform_revenue": record["platform_revenue"],
        "intermediary_profit": record["intermediary_profit"],
        "system_profit": record["system_profit"],
        "min_qos": min(min(row) for row in record["qos"]),
        "max_utilization": max(max(row) for row in record["utilization"]),
        "objective_evaluations": record["diagnostics"]["objective_evaluations"],
        "converged": record["diagnostics"]["converged"],
    }


def _write_artifacts(records: list[dict[str, Any]], output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_path = output_dir / "three_layer_records.json"
    summary_path = output_dir / "three_layer_summary.csv"
    raw_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    rows = [_summary_row(record) for record in records]
    with summary_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return {"raw": raw_path, "summary": summary_path}


def _plot_baselines(records: list[dict[str, Any]], output_dir: Path) -> Path:
    return plot_baseline_comparison(records, output_dir)


def _plot_policy_detail(record: dict[str, Any], output_dir: Path) -> Path:
    return plot_policy_detail(record, output_dir)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--smoke", action="store_true")
    group.add_argument("--full", action="store_true")
    parser.add_argument("--output-root", type=Path, default=PROJECT_ROOT / "artifacts" / "intermediary")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    trials = 2 if args.smoke else 8
    maxiter = 40 if args.smoke else 140
    config = IntermediaryConfig.default(optimizer_trials=trials, optimizer_maxiter=maxiter)
    results = run_three_layer_smoke(config)
    records = [_record(result, config) for result in results.values()]
    output_dir = args.output_root / run_id
    paths = _write_artifacts(records, output_dir)
    baseline_plot = _plot_baselines(records, output_dir)
    detail_plot = _plot_policy_detail(_record(results["three_layer_qos_aware"], config), output_dir)
    print(f"mode={'smoke' if args.smoke else 'full'}")
    print(f"records={len(records)}")
    print(f"raw={paths['raw']}")
    print(f"summary={paths['summary']}")
    print(f"plot={baseline_plot}")
    print(f"plot={detail_plot}")


if __name__ == "__main__":
    main()
