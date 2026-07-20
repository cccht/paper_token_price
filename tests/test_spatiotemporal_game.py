from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pricing_sim.peak_shaving_config import PeakShavingConfig
from pricing_sim.peak_shaving_market import intermediary_profit, system_profit
from pricing_sim.spatiotemporal_mechanism import DemandResponseSpec


def _case():
    from pricing_sim.spatiotemporal_game import SpatiotemporalGameSpec

    config = PeakShavingConfig.default().evolve(
        base_rigid=np.array([20.0, 80.0, 20.0]),
        time_preference=np.ones(3),
        native_rigid=np.array([0.2, 0.6, 0.2]),
        native_elastic=np.array([0.2, 0.6, 0.2]),
        load_shape_hat=np.array([-1.0, 1.0, -1.0]),
        firm_capacity=np.array([120.0, 60.0]),
        qos_threshold=0.9,
        qos_strength=3.0,
    )
    demand = DemandResponseSpec(
        native_demand=np.array([[20.0, 80.0, 20.0], [20.0, 80.0, 20.0]]),
        price_sensitivity=np.array([1.0, 3.0]),
        flexible_fraction=np.array([0.0, 0.8]),
        migration_cost=np.array([2.0, 0.2]),
        max_shift=np.array([0, 1]),
        channel_brand=np.array([1.05, 1.0, 1.0]),
        qos_weight=1.0,
    )
    game = SpatiotemporalGameSpec(
        demand=demand,
        fixed_channel_shares=np.array([0.2, 0.5, 0.3]),
        temporal_enabled=True,
        spatial_enabled=True,
        qos_shape="threshold",
    )
    return config, game


def test_joint_market_conserves_demand_and_solves_routing_qos_fixed_point():
    from pricing_sim.spatiotemporal_game import solve_spatiotemporal_joint_market

    config, game = _case()
    periods = config.num_periods
    retail = np.array([0.8, 1.1, 0.8])
    wholesale = np.vstack([np.full(periods, 0.4), np.full(periods, 0.6)])
    direct = np.array([[0.8, 0.9, 0.8], [0.9, 1.2, 0.9]])

    state, result = solve_spatiotemporal_joint_market(
        retail, wholesale, direct, 3.0, game, config
    )

    assert result["joint_converged"]
    assert result["joint_residual"] <= 1e-8
    assert np.allclose(state.routing.sum(axis=0), 1.0)
    assert np.isclose(result["demand"].sum(), game.demand.native_demand.sum())
    assert np.allclose(
        result["temporal_flows"].sum(axis=2), game.demand.native_demand
    )


def test_internal_wholesale_transfer_cancels_in_spatiotemporal_state():
    from pricing_sim.spatiotemporal_game import solve_spatiotemporal_joint_market

    config, game = _case()
    config = config.evolve(capacity_cost=0.0, degrade_cost=0.0)
    periods = config.num_periods
    retail = np.full(periods, 0.9)
    wholesale = np.vstack([np.full(periods, 0.35), np.full(periods, 0.65)])
    direct = np.vstack([np.full(periods, 0.8), np.full(periods, 1.0)])
    state, result = solve_spatiotemporal_joint_market(
        retail, wholesale, direct, 2.0, game, config
    )

    hours = config.period_hours
    external_revenue = hours * (
        np.sum(retail * result["demand"][0] * result["qos_channel"][0])
        + np.sum(direct * result["demand"][1:] * result["qos_firm"])
    )

    assert np.isclose(system_profit(state, result, config), external_revenue)


def test_intermediary_best_response_includes_the_reference_candidate():
    from pricing_sim.spatiotemporal_game import (
        intermediary_best_response_spatiotemporal,
        solve_spatiotemporal_joint_market,
    )

    config, game = _case()
    periods = config.num_periods
    wholesale = np.vstack([np.full(periods, 0.4), np.full(periods, 0.6)])
    direct = np.vstack([np.full(periods, 0.85), np.full(periods, 1.0)])
    reference_state, reference_result = solve_spatiotemporal_joint_market(
        np.full(periods, 0.8), wholesale, direct, 2.0, game, config
    )
    reference_profit = intermediary_profit(
        reference_state, reference_result, config
    )

    best_state, best_result = intermediary_best_response_spatiotemporal(
        wholesale,
        direct,
        game,
        config,
        retail_base_grid=np.array([0.8, 1.1]),
        retail_slope_grid=np.array([0.0, 0.2]),
        route_beta_grid=np.array([2.0, 4.0]),
    )

    assert best_result["joint_converged"]
    assert intermediary_profit(best_state, best_result, config) >= reference_profit - 1e-9


def test_pair_evaluator_reports_both_peak_definitions_and_finite_payoffs():
    from pricing_sim.spatiotemporal_game import evaluate_firm_pair_spatiotemporal

    config, game = _case()
    record = evaluate_firm_pair_spatiotemporal(
        np.array([0.35, 0.2, 0.75, -0.2]),
        np.array([0.55, 0.2, 0.95, 0.2]),
        game,
        config,
        retail_base_grid=np.array([0.8]),
        retail_slope_grid=np.array([0.0, 0.2]),
        route_beta_grid=np.array([2.0]),
    )

    assert np.isfinite(record["firm_A_profit"])
    assert np.isfinite(record["firm_B_profit"])
    assert record["joint_converged"]
    assert record["aggregate_peak_load"] == np.max(
        np.sum(record["result"]["loads"], axis=0)
    )
    assert record["maximum_provider_utilization"] == np.max(
        record["result"]["utilization"]
    )
