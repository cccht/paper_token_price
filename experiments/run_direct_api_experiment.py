"""Run direct manufacturer API outside-option experiments."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
import sys
from typing import Any

import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
for import_path in (PROJECT_ROOT, SCRIPT_DIR):
    path_text = str(import_path)
    if path_text not in sys.path:
        sys.path.insert(0, path_text)

from pricing_sim.direct_access_game import direct_api_config, optimize_direct_access_stackelberg
from pricing_sim.intermediary_market import IntermediaryConfig
from experiments.run_intermediary_realism_experiments import (
    market_metric_row,
    uniform_result,
    user_protected_config,
)
from pricing_sim.three_stage_game import optimize_three_stage_stackelberg


DEFAULT_TRIALS = 4
DEFAULT_MAXITER = 70


def _jsonable(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    return value


def _write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    keys = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def _direct_share(result: Any) -> float:
    direct_idx = result.demand.shape[0] - 1
    return float(np.sum(result.demand[direct_idx]) / max(np.sum(result.demand), 1e-12))


def direct_api_rows(*, trials: int, maxiter: int) -> list[dict[str, Any]]:
    base = IntermediaryConfig.default(optimizer_trials=trials, optimizer_maxiter=maxiter)
    protected = user_protected_config(base)
    direct_config = direct_api_config(protected)
    direct = optimize_direct_access_stackelberg(protected)
    rows = [
        market_metric_row("uniform_retail", uniform_result(base), base, extra={"experiment": "direct_api_choice"}),
        market_metric_row(
            "user_protected_revenue",
            optimize_three_stage_stackelberg(protected, policy="user_protected_revenue"),
            protected,
            extra={"experiment": "direct_api_choice"},
        ),
        market_metric_row(
            "direct_api_user_choice",
            direct,
            direct_config,
            extra={"experiment": "direct_api_choice", "direct_api_share": _direct_share(direct)},
        ),
    ]
    reference = rows[0]
    for row in rows:
        row["platform_revenue_gain_vs_uniform"] = row["platform_revenue"] - reference["platform_revenue"]
        row["inclusive_value_gain_vs_uniform"] = row["inclusive_value"] - reference["inclusive_value"]
        row["demand_weighted_qos_gain_vs_uniform"] = row["demand_weighted_qos"] - reference["demand_weighted_qos"]
    return rows


def write_artifacts(rows: list[dict[str, Any]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(rows, output_dir / "direct_api_choice.csv")
    (output_dir / "direct_api_records.json").write_text(
        json.dumps(_jsonable(rows), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, default=PROJECT_ROOT / "artifacts" / "direct_api")
    parser.add_argument("--trials", type=int, default=DEFAULT_TRIALS)
    parser.add_argument("--maxiter", type=int, default=DEFAULT_MAXITER)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    output_dir = args.output_root / datetime.now().strftime("%Y%m%d-%H%M%S")
    write_artifacts(direct_api_rows(trials=args.trials, maxiter=args.maxiter), output_dir)
    print(f"output={output_dir}")


if __name__ == "__main__":
    main()
