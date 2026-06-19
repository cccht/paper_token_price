from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pricing_sim.capacity_only_game import optimize_capacity_only
from pricing_sim.intermediary_market import IntermediaryConfig, _default_capacity, evaluate_three_layer_policy
from pricing_sim.reviewer_diagnostics import attribution_rows, finite_bridge_rows, profit_slice_rows


def test_capacity_only_keeps_prices_fixed_and_capacity_feasible():
    config = IntermediaryConfig.default(optimizer_trials=1, optimizer_maxiter=20)

    result = optimize_capacity_only(config)

    assert np.allclose(result.wholesale_prices, config.base_wholesale_price)
    assert np.allclose(result.retail_prices, config.base_retail_price)
    assert np.allclose(np.sum(result.capacity, axis=1), config.intermediary_capacity)
    assert result.diagnostics["retail_strategic"] is False


def test_attribution_rows_report_gain_share_fields():
    config = IntermediaryConfig.default(optimizer_trials=1, optimizer_maxiter=20)

    rows = attribution_rows(config)
    mechanisms = {row["mechanism"] for row in rows}

    assert "capacity_only" in mechanisms
    assert "price_only" in mechanisms
    assert "price_capacity_with_congestion_proxy" in mechanisms
    assert "price_capacity_and_qos_internalization" in mechanisms
    assert all("system_gain_vs_uniform" in row for row in rows)
    assert all("share_of_full_gain" in row for row in rows)


def test_profit_slice_summary_reports_single_peak_diagnostic():
    config = IntermediaryConfig.default()
    wholesale = np.full(config.num_periods, config.base_wholesale_price)
    retail = np.full((config.num_intermediaries, config.num_periods), config.base_retail_price)
    result = evaluate_three_layer_policy(wholesale, retail, _default_capacity(config), config)

    rows, summary = profit_slice_rows(result, config, points=9)

    assert len(rows) == 18
    assert {row["slice"] for row in summary} == {"capacity_offpeak_to_peak", "retail_peak_period"}
    assert all("local_peak_count" in row for row in summary)


def test_finite_bridge_rows_compare_empirical_and_logit_shares():
    config = IntermediaryConfig.default()
    wholesale = np.full(config.num_periods, config.base_wholesale_price)
    retail = np.full((config.num_intermediaries, config.num_periods), config.base_retail_price)
    result = evaluate_three_layer_policy(wholesale, retail, _default_capacity(config), config)

    rows, summary = finite_bridge_rows(result, config, player_counts=(24,), seeds=(0, 1))

    assert len(rows) == 2
    assert summary[0]["players"] == 24
    assert 0.0 <= summary[0]["cosine_similarity_mean"] <= 1.0
    assert summary[0]["l1_share_gap_mean"] >= 0.0
