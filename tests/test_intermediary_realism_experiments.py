from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pricing_sim.intermediary_market import IntermediaryConfig
from experiments.run_intermediary_realism_experiments import (
    arrival_rate_pattern,
    market_metric_row,
    scaled_market_config,
    uniform_result,
    user_protected_revenue_rows,
)


def test_arrival_rate_pattern_resamples_positive_rates():
    rows = [
        {"arrival_rate_rps": 8.0},
        {"arrival_rate_rps": 16.0},
        {"arrival_rate_rps": 32.0},
    ]

    pattern = arrival_rate_pattern(rows, periods=8)

    assert pattern.shape == (8,)
    assert np.all(pattern > 0.0)
    assert np.isclose(np.mean(pattern), 1.0)
    assert pattern[-1] > pattern[0]


def test_market_metric_row_reports_user_and_qos_metrics():
    config = IntermediaryConfig.default()
    result = uniform_result(config)

    row = market_metric_row("uniform", result, config, extra={})

    assert np.isfinite(row["inclusive_value"])
    assert np.isclose(row["average_retail_price"], config.base_retail_price)
    assert 0.0 < row["demand_weighted_qos"] <= 1.0
    assert row["active_min_qos"] >= row["min_qos"]


def test_scaled_market_config_changes_demand_and_capacity():
    config = IntermediaryConfig.default()

    scaled = scaled_market_config(config, demand_scale=1.2, capacity_scale=0.9)

    assert np.allclose(scaled.rigid_baseline, config.rigid_baseline * 1.2)
    assert np.isclose(scaled.flexible_baseline, config.flexible_baseline * 1.2)
    assert np.allclose(scaled.intermediary_capacity, config.intermediary_capacity * 0.9)


def test_user_protected_revenue_rows_improve_platform_and_user_metrics():
    rows = user_protected_revenue_rows(trials=1, maxiter=20)
    by_policy = {row["policy"]: row for row in rows}

    uniform = by_policy["uniform_retail"]
    protected = by_policy["user_protected_revenue"]

    assert protected["platform_revenue"] > uniform["platform_revenue"]
    assert protected["inclusive_value"] > uniform["inclusive_value"]
    assert protected["demand_weighted_qos"] > uniform["demand_weighted_qos"]
    assert protected["active_min_qos"] > uniform["active_min_qos"]
    assert protected["average_retail_price"] <= protected["retail_price_cap"] + 1e-9
