"""Run reviewer-requested sensitivity experiments for SCI revision."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
import sys
from typing import Any, Iterable

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
for import_path in (PROJECT_ROOT, SCRIPT_DIR):
    path_text = str(import_path)
    if path_text not in sys.path:
        sys.path.insert(0, path_text)

from experiments.run_intermediary_realism_experiments import (  # noqa: E402
    market_metric_row,
    uniform_result,
    user_protected_config,
)
from pricing_sim.direct_access_game import (  # noqa: E402
    direct_api_config,
    optimize_direct_access_stackelberg,
)
from pricing_sim.intermediary_market import IntermediaryConfig  # noqa: E402
from pricing_sim.three_stage_game import optimize_three_stage_stackelberg  # noqa: E402


DEFAULT_TRIALS = 4
DEFAULT_MAXITER = 70
RETAIL_CAPS = (0.80, 0.82, 0.85, 0.90, 1.00)
WHOLESALE_CAPS = (0.60, 0.70, 0.80, 0.90)
DIRECT_API_PRICES = (0.75, 0.82, 0.90, 1.00)
DIRECT_API_CAPACITIES = (500.0, 1000.0, 1500.0, 2000.0)
COLORS = ["#0072B2", "#D55E00", "#009E73", "#E69F00", "#CC79A7"]

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "font.size": 8,
})


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


def _bounded_config(
    config: IntermediaryConfig,
    *,
    retail_cap: float,
    wholesale_cap: float,
) -> IntermediaryConfig:
    data = {**config.__dict__}
    data["retail_upper_bound"] = min(config.retail_upper_bound, retail_cap)
    data["wholesale_upper_bound"] = min(config.wholesale_upper_bound, wholesale_cap)
    return IntermediaryConfig.default(**data)


def pareto_flags(rows: list[dict[str, Any]], metric_keys: Iterable[str]) -> list[bool]:
    metrics = tuple(metric_keys)
    flags = []
    for row in rows:
        dominated = False
        for other in rows:
            weakly_better = all(float(other[key]) >= float(row[key]) for key in metrics)
            strictly_better = any(float(other[key]) > float(row[key]) for key in metrics)
            dominated = weakly_better and strictly_better
            if dominated:
                break
        flags.append(not dominated)
    return flags


def _add_uniform_deltas(row: dict[str, Any], reference: dict[str, Any]) -> None:
    row["platform_revenue_gain_vs_uniform"] = row["platform_revenue"] - reference["platform_revenue"]
    row["inclusive_value_gain_vs_uniform"] = row["inclusive_value"] - reference["inclusive_value"]
    row["demand_weighted_qos_gain_vs_uniform"] = row["demand_weighted_qos"] - reference["demand_weighted_qos"]
    row["active_min_qos_gain_vs_uniform"] = row["active_min_qos"] - reference["active_min_qos"]


def user_protection_sweep_rows(
    *,
    trials: int,
    maxiter: int,
    retail_caps: Iterable[float] = RETAIL_CAPS,
    wholesale_caps: Iterable[float] = WHOLESALE_CAPS,
) -> list[dict[str, Any]]:
    base = IntermediaryConfig.default(optimizer_trials=trials, optimizer_maxiter=maxiter)
    uniform = market_metric_row("uniform_retail", uniform_result(base), base)
    rows = []
    for retail_cap in retail_caps:
        for wholesale_cap in wholesale_caps:
            config = _bounded_config(base, retail_cap=retail_cap, wholesale_cap=wholesale_cap)
            result = optimize_three_stage_stackelberg(config, policy="user_protection_sweep")
            row = market_metric_row("user_protection_sweep", result, config, extra={
                "experiment": "user_protection_sweep",
                "retail_price_cap": float(retail_cap),
                "wholesale_price_cap": float(wholesale_cap),
            })
            _add_uniform_deltas(row, uniform)
            rows.append(row)
    flags = pareto_flags(rows, ["platform_revenue", "inclusive_value", "active_min_qos"])
    for row, flag in zip(rows, flags):
        row["pareto_efficient"] = bool(flag)
    return rows


def _add_protected_deltas(row: dict[str, Any], reference: dict[str, Any]) -> None:
    row["platform_revenue_gain_vs_protected"] = row["platform_revenue"] - reference["platform_revenue"]
    row["inclusive_value_gain_vs_protected"] = row["inclusive_value"] - reference["inclusive_value"]
    row["system_profit_gain_vs_protected"] = row["system_profit"] - reference["system_profit"]


def direct_api_sensitivity_rows(
    *,
    trials: int,
    maxiter: int,
    direct_prices: Iterable[float] = DIRECT_API_PRICES,
    direct_capacities: Iterable[float] = DIRECT_API_CAPACITIES,
) -> list[dict[str, Any]]:
    base = IntermediaryConfig.default(optimizer_trials=trials, optimizer_maxiter=maxiter)
    protected = user_protected_config(base)
    uniform = market_metric_row("uniform_retail", uniform_result(base), base)
    protected_result = optimize_three_stage_stackelberg(protected, policy="user_protected_revenue")
    protected_row = market_metric_row("user_protected_revenue", protected_result, protected)
    rows = []
    for price in direct_prices:
        for capacity in direct_capacities:
            result = optimize_direct_access_stackelberg(
                protected,
                direct_retail_price=float(price),
                direct_capacity=float(capacity),
            )
            config = direct_api_config(protected, direct_capacity=float(capacity))
            row = market_metric_row("direct_api_sensitivity", result, config, extra={
                "experiment": "direct_api_sensitivity",
                "direct_api_price": float(price),
                "direct_api_capacity": float(capacity),
                "direct_api_share": result.diagnostics["direct_api_share"],
            })
            _add_uniform_deltas(row, uniform)
            _add_protected_deltas(row, protected_row)
            rows.append(row)
    flags = pareto_flags(rows, ["platform_revenue", "inclusive_value", "system_profit"])
    for row, flag in zip(rows, flags):
        row["pareto_efficient"] = bool(flag)
    return rows


def _plot_user_protection(rows: list[dict[str, Any]], path: Path) -> None:
    fig, axis = plt.subplots(figsize=(4.8, 3.4))
    for idx, wholesale_cap in enumerate(sorted({row["wholesale_price_cap"] for row in rows})):
        selected = [row for row in rows if row["wholesale_price_cap"] == wholesale_cap]
        axis.plot(
            [row["inclusive_value"] for row in selected],
            [row["platform_revenue"] for row in selected],
            "o-",
            color=COLORS[idx % len(COLORS)],
            label=f"w cap={wholesale_cap:.2f}",
        )
    frontier = [row for row in rows if row["pareto_efficient"]]
    axis.scatter(
        [row["inclusive_value"] for row in frontier],
        [row["platform_revenue"] for row in frontier],
        marker="s",
        facecolors="none",
        edgecolors="black",
        label="Pareto",
    )
    axis.set_xlabel("Inclusive value")
    axis.set_ylabel("Platform revenue")
    axis.grid(alpha=0.25)
    axis.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(path.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


def _plot_direct_api(rows: list[dict[str, Any]], path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.2))
    capacities = sorted({row["direct_api_capacity"] for row in rows})
    for idx, capacity in enumerate(capacities):
        selected = [row for row in rows if row["direct_api_capacity"] == capacity]
        x = [row["direct_api_price"] for row in selected]
        axes[0].plot(x, [row["inclusive_value"] for row in selected], "o-", color=COLORS[idx], label=f"{capacity:.0f}")
        axes[1].plot(x, [row["platform_revenue"] for row in selected], "o-", color=COLORS[idx], label=f"{capacity:.0f}")
    axes[0].set_title("Inclusive value")
    axes[1].set_title("Platform revenue")
    for axis in axes:
        axis.set_xlabel("Direct API price")
        axis.grid(alpha=0.25)
        axis.legend(title="Capacity", fontsize=7, title_fontsize=7)
    fig.tight_layout()
    fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(path.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


def run_experiments(*, trials: int, maxiter: int) -> dict[str, list[dict[str, Any]]]:
    return {
        "user_protection_sweep": user_protection_sweep_rows(trials=trials, maxiter=maxiter),
        "direct_api_sensitivity": direct_api_sensitivity_rows(trials=trials, maxiter=maxiter),
    }


def write_artifacts(results: dict[str, list[dict[str, Any]]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "review_strengthening_records.json").write_text(
        json.dumps(_jsonable(results), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    for name, rows in results.items():
        _write_csv(rows, output_dir / f"{name}.csv")
    _plot_user_protection(results["user_protection_sweep"], output_dir / "user_protection_frontier")
    _plot_direct_api(results["direct_api_sensitivity"], output_dir / "direct_api_sensitivity")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, default=PROJECT_ROOT / "artifacts" / "review_strengthening")
    parser.add_argument("--trials", type=int, default=DEFAULT_TRIALS)
    parser.add_argument("--maxiter", type=int, default=DEFAULT_MAXITER)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    output_dir = args.output_root / datetime.now().strftime("%Y%m%d-%H%M%S")
    write_artifacts(run_experiments(trials=args.trials, maxiter=args.maxiter), output_dir)
    print(f"output={output_dir}")


if __name__ == "__main__":
    main()
