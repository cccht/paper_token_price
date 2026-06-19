from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from experiments.run_review_strengthening_experiments import (
    direct_api_sensitivity_rows,
    pareto_flags,
    user_protection_sweep_rows,
)


def test_pareto_flags_marks_only_dominated_rows_false():
    rows = [
        {"platform_revenue": 10.0, "inclusive_value": 1.0, "active_min_qos": 1.0},
        {"platform_revenue": 9.0, "inclusive_value": 1.1, "active_min_qos": 1.0},
        {"platform_revenue": 8.0, "inclusive_value": 0.8, "active_min_qos": 0.9},
    ]

    flags = pareto_flags(rows, ["platform_revenue", "inclusive_value", "active_min_qos"])

    assert flags == [True, True, False]


def test_user_protection_sweep_rows_include_caps_and_frontier_flag():
    rows = user_protection_sweep_rows(
        trials=1,
        maxiter=20,
        retail_caps=(0.82,),
        wholesale_caps=(0.70,),
    )

    assert len(rows) == 1
    row = rows[0]
    assert row["retail_price_cap"] == 0.82
    assert row["wholesale_price_cap"] == 0.70
    assert row["pareto_efficient"] is True
    assert row["platform_revenue_gain_vs_uniform"] > 0.0
    assert np.isfinite(row["inclusive_value_gain_vs_uniform"])


def test_direct_api_sensitivity_rows_include_price_capacity_and_share():
    rows = direct_api_sensitivity_rows(
        trials=1,
        maxiter=20,
        direct_prices=(0.82,),
        direct_capacities=(1500.0,),
    )

    assert len(rows) == 1
    row = rows[0]
    assert row["direct_api_price"] == 0.82
    assert row["direct_api_capacity"] == 1500.0
    assert 0.0 < row["direct_api_share"] < 1.0
    assert np.isfinite(row["platform_revenue_gain_vs_protected"])
