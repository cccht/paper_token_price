"""Cross-layer comparison: three-layer vs two-layer baselines.

Runs the full three-layer intermediary game alongside two-layer
(Platform→Users) variants on a consistent benchmark.  Produces a
feature-comparison table suitable for the EJOR manuscript.

Usage:
    python experiments/run_two_layer_comparison.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np

_PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_PROJECT))

from pricing_sim.intermediary_market import (
    IntermediaryConfig,
    ThreeLayerResult,
    run_three_layer_smoke,
)
from pricing_sim.two_layer_game import (
    TwoLayerResult,
    run_two_layer_baselines,
)


def _header() -> str:
    return (
        f"{'Policy':<32s} {'SysProfit':>10s}  {'MinQoS':>8s}  "
        f"{'PeakUtil':>9s}  {'AvgPrice':>9s}  {'InclValue':>10s}  {'Ev':>6s}"
    )


def _three_inclusive(r: ThreeLayerResult, cfg: IntermediaryConfig) -> float:
    return float(np.log(np.sum(np.exp(
        np.log(cfg.time_preference + 1e-10)[None, :]
        + np.log(cfg.brand_quality + 1e-10)[:, None]
        - cfg.price_sensitivity * (
            r.retail_prices
            + cfg.inconvenience_cost * (1.0 - cfg.native_period_distribution)[None, :]
            - cfg.base_retail_price
        )
        - cfg.qos_feedback_weight * (1.0 - r.qos)
    ))))


def _row_three(name: str, r: ThreeLayerResult, cfg: IntermediaryConfig) -> str:
    avg_price = float(np.mean(r.retail_prices))
    return (
        f"{name:<32s} {r.system_profit:>10.2f}  {r.diagnostics['min_qos']:>8.4f}  "
        f"{r.diagnostics['max_utilization']:>9.4f}  {avg_price:>9.4f}  "
        f"{_three_inclusive(r, cfg):>10.4f}  {r.diagnostics.get('objective_evaluations', 0):>6d}"
    )


def _row_two(name: str, r: TwoLayerResult) -> str:
    avg_price = float(np.mean(r.retail_prices))
    return (
        f"{name:<32s} {r.system_profit:>10.2f}  {r.diagnostics['min_qos']:>8.4f}  "
        f"{r.diagnostics['max_utilization']:>9.4f}  {avg_price:>9.4f}  "
        f"{r.inclusive_value:>10.4f}  {r.diagnostics.get('objective_evaluations', 0):>6d}"
    )


def main() -> None:
    config = IntermediaryConfig.default(
        optimizer_trials=8,
        optimizer_maxiter=160,
        random_seed=42,
    )

    print("=" * 98)
    print("  Three-layer baselines (Platform → Intermediaries → Users)")
    print("=" * 98)
    three = run_three_layer_smoke(config)

    print(_header())
    print("-" * 98)
    order3 = [
        "uniform_retail",
        "direct_platform",
        "single_intermediary",
        "no_qos_pricing",
        "three_layer_qos_aware",
    ]
    for key in order3:
        print(_row_three(key, three[key], config))

    print()
    print("=" * 98)
    print("  Two-layer baselines (Platform → Users)  --  NEW")
    print("=" * 98)
    two = run_two_layer_baselines(config)

    print(_header())
    print("-" * 98)
    order2 = [
        "two_layer_uniform",
        "two_layer_centralized",
        "two_layer_revenue_only",
        "two_layer_user_protected",
    ]
    for key in order2:
        print(_row_two(key, two[key]))

    print()
    print("=" * 98)
    print("  Cross-layer comparison")
    print("=" * 98)
    print(f"{'Metric':<30s} {'3L-Uniform':>12s} {'2L-Cent':>12s} {'3L-QoS':>12s}")
    print("-" * 98)
    comparisons = [
        ("System Profit", "system_profit", "system_profit", "system_profit"),
        ("Min QoS", "diagnostics.min_qos", "diagnostics.min_qos", "diagnostics.min_qos"),
    ]
    ul = three["uniform_retail"]
    two_cent = two["two_layer_centralized"]
    tl = three["three_layer_qos_aware"]

    print(f"{'System Profit':<30s} {ul.system_profit:>12.2f} {two_cent.system_profit:>12.2f} {tl.system_profit:>12.2f}")
    print(f"{'Min QoS':<30s} {ul.diagnostics['min_qos']:>12.4f} {two_cent.diagnostics['min_qos']:>12.4f} {tl.diagnostics['min_qos']:>12.4f}")
    print(f"{'Peak Utilization':<30s} {ul.diagnostics['max_utilization']:>12.4f} {two_cent.diagnostics['max_utilization']:>12.4f} {tl.diagnostics['max_utilization']:>12.4f}")

    inc_ul = _three_inclusive(ul, config)
    inc_tl = _three_inclusive(tl, config)

    print(f"{'Inclusive Value':<30s} {inc_ul:>12.4f} {two_cent.inclusive_value:>12.4f} {inc_tl:>12.4f}")

    artifacts = _PROJECT / "artifacts" / "two_layer_comparison"
    artifacts.mkdir(parents=True, exist_ok=True)

    unified_fields = [
        "layer", "policy", "system_profit", "platform_revenue",
        "intermediary_profit", "gross_revenue", "capacity_cost",
        "qos_cost", "min_qos", "max_utilization", "inclusive_value",
        "avg_retail_price", "objective_evaluations",
    ]
    summary: list[dict] = []
    for key in order3:
        r = three[key]
        summary.append({
            "layer": "three",
            "policy": key,
            "system_profit": r.system_profit,
            "platform_revenue": r.platform_revenue,
            "intermediary_profit": r.intermediary_profit,
            "gross_revenue": "",
            "capacity_cost": "",
            "qos_cost": "",
            "min_qos": r.diagnostics["min_qos"],
            "max_utilization": r.diagnostics["max_utilization"],
            "inclusive_value": _three_inclusive(r, config),
            "avg_retail_price": float(np.mean(r.retail_prices)),
            "objective_evaluations": r.diagnostics.get("objective_evaluations", 0),
        })
    for key in order2:
        r = two[key]
        summary.append({
            "layer": "two",
            "policy": key,
            "system_profit": r.system_profit,
            "platform_revenue": r.gross_revenue,
            "intermediary_profit": "",
            "gross_revenue": r.gross_revenue,
            "capacity_cost": r.capacity_cost,
            "qos_cost": r.qos_cost,
            "min_qos": r.diagnostics["min_qos"],
            "max_utilization": r.diagnostics["max_utilization"],
            "inclusive_value": r.inclusive_value,
            "avg_retail_price": float(np.mean(r.retail_prices)),
            "objective_evaluations": r.diagnostics.get("objective_evaluations", 0),
        })

    with open(artifacts / "cross_layer_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    import csv
    with open(artifacts / "cross_layer_summary.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=unified_fields)
        writer.writeheader()
        writer.writerows(summary)

    print(f"\nArtifacts saved to {artifacts}")


if __name__ == "__main__":
    main()
