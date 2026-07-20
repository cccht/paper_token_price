from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from experiments.peak_shaving_smpt_tools import (
    congested_base,
    evaluate_params,
    params_from_vectors,
    record_from_state,
)
from pricing_sim.peak_shaving_config import PeakShavingConfig
from pricing_sim.peak_shaving_equilibrium import _solve_with_routing, routing_from_beta
from pricing_sim.peak_shaving_market import (
    MarketState,
    qos_factor,
    solve_market_fixed_point,
    system_profit,
)


def _asymmetric_case() -> tuple[PeakShavingConfig, MarketState, dict]:
    config = PeakShavingConfig.default().evolve(
        firm_capacity=np.array([500.0, 150.0]),
        pop_rigid=0.4,
        pop_elastic=0.6,
    )
    periods = config.num_periods
    state = MarketState(
        retail=np.linspace(0.8, 1.3, periods),
        direct=np.vstack([
            np.linspace(0.5, 0.9, periods),
            np.linspace(0.9, 0.6, periods),
        ]),
        wholesale=np.vstack([
            np.linspace(0.25, 0.45, periods),
            np.linspace(0.85, 0.55, periods),
        ]),
        routing=np.vstack([
            np.linspace(0.2, 0.7, periods),
            np.linspace(0.8, 0.3, periods),
        ]),
    )
    result = solve_market_fixed_point(
        state.channel_prices(), state.routing, config, qos_shape="sigmoid"
    )
    assert result["converged"]
    return config, state, result


def test_internal_wholesale_transfers_cancel_from_system_profit():
    config, state, result = _asymmetric_case()
    config = config.evolve(capacity_cost=0.0, degrade_cost=0.0)
    result = solve_market_fixed_point(
        state.channel_prices(), state.routing, config, qos_shape="sigmoid"
    )
    demand = result["demand"]
    external_revenue = config.period_hours * (
        np.sum(state.retail * demand[0] * result["qos_channel"][0])
        + np.sum(state.direct * demand[1:] * result["qos_firm"])
    )

    assert np.isclose(system_profit(state, result, config), external_revenue, atol=1e-9)


def test_average_paid_price_uses_completed_demand_weights():
    config, state, result = _asymmetric_case()
    record = record_from_state("asymmetric", state, result, config)
    completed = result["demand"] * result["qos_channel"]
    expected = float(np.sum(result["prices"] * completed) / np.sum(completed))

    assert np.isclose(record["average_paid_price"], expected, atol=1e-12)


def test_joint_routing_qos_solver_reports_verified_final_residual():
    config = PeakShavingConfig.default().evolve(
        firm_capacity=np.array([500.0, 150.0]),
        pop_rigid=0.4,
        pop_elastic=0.6,
    )
    periods = config.num_periods
    retail = np.linspace(0.8, 1.2, periods)
    wholesale = np.vstack([
        np.linspace(0.3, 0.45, periods),
        np.linspace(0.7, 0.55, periods),
    ])
    direct = np.vstack([
        np.linspace(0.6, 0.9, periods),
        np.linspace(0.9, 0.65, periods),
    ])
    route_beta = 4.0

    state, result = _solve_with_routing(
        retail, wholesale, direct, route_beta, config, qos_shape="sigmoid"
    )

    assert "joint_residual" in result
    target_routing = routing_from_beta(
        wholesale, result["qos_firm"], route_beta, config
    )
    target_qos = qos_factor(result["utilization"], config, shape="sigmoid")
    independently_checked = max(
        float(np.max(np.abs(target_routing - state.routing))),
        float(np.max(np.abs(target_qos - result["qos_firm"]))),
    )
    assert result["joint_converged"]
    assert np.isclose(result["joint_residual"], independently_checked, atol=1e-12)
    assert result["joint_residual"] <= 1e-8


def test_smpt_record_exposes_joint_fixed_point_evidence():
    params = params_from_vectors([
        [0.575, 0.2, 0.6, -0.2],
        [0.575, 0.4, 0.6, 0.2],
    ])

    record = evaluate_params("joint_record", params, congested_base())

    assert record["joint_fixed_point_converged"]
    assert record["joint_fixed_point_residual"] <= 1e-8
    assert record["joint_qos_residual"] <= 1e-8
    assert record["joint_routing_residual"] <= 1e-8
