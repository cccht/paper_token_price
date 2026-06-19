import numpy as np

from pricing_sim.config import SimulationConfig
from pricing_sim.demand import compute_demand
from pricing_sim.economics import evaluate_policy
from pricing_sim.qos import qos_factor


def test_qos_factor_is_one_below_threshold_and_decreases_above_it():
    utilization = np.array([0.50, 0.82, 0.90, 1.00])

    quality = qos_factor(utilization, threshold=0.82, strength=15.0)

    assert np.allclose(quality[:2], 1.0)
    assert 1.0 > quality[2] > quality[3] > 0.0


def test_policy_evaluation_exposes_consistent_profit_and_welfare_components():
    config = SimulationConfig.default()

    result = evaluate_policy(np.full(config.num_periods, config.posted_price_cap), config)

    assert result.prices.shape == (config.num_periods,)
    assert result.demand.total.shape == (config.num_periods,)
    assert result.qos.shape == (config.num_periods,)
    assert np.isclose(result.profit, sum(result.profit_components.values()))
    assert np.isclose(result.welfare, sum(result.welfare_components.values()))


def test_qos_feedback_variant_changes_flexible_demand():
    prices = np.full(8, 0.80)
    prices[5] = 0.45
    baseline = SimulationConfig.default()
    feedback = SimulationConfig.default(qos_feedback_weight=2.0)

    baseline_demand = compute_demand(prices, baseline).flexible
    feedback_result = compute_demand(prices, feedback)
    feedback_demand = feedback_result.flexible

    assert not np.allclose(feedback_demand, baseline_demand)
    assert feedback_result.converged
    assert feedback_result.iterations > 0


def test_full_billing_does_not_discount_revenue_by_qos():
    prices = np.full(8, 0.80)
    effective = evaluate_policy(
        prices,
        SimulationConfig.default(billing_mode="effective"),
    )
    full = evaluate_policy(
        prices,
        SimulationConfig.default(billing_mode="full"),
    )

    assert full.profit_components["revenue"] > effective.profit_components["revenue"]


def test_sla_penalty_billing_exposes_penalty_component():
    result = evaluate_policy(
        np.full(8, 0.80),
        SimulationConfig.default(billing_mode="sla_penalty", sla_penalty_rate=0.25),
    )

    assert result.profit_components["sla_penalty"] < 0.0
