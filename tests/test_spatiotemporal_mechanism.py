from importlib import import_module, util
from pathlib import Path
import sys

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pricing_sim.peak_shaving_equilibrium as equilibrium
from pricing_sim.peak_shaving_config import PeakShavingConfig


def test_explicit_tou_price_modes_have_their_named_signs():
    expand = getattr(equilibrium, "expand_policy_price", None)
    assert callable(expand)
    config = PeakShavingConfig.default()
    shape = config.load_shape_hat
    base = 1.0

    uniform = expand(base, 0.2, config, lower=0.1, upper=2.0, mode="uniform")
    peak_only = expand(base, 0.2, config, lower=0.1, upper=2.0, mode="peak_surcharge")
    offpeak_only = expand(base, 0.2, config, lower=0.1, upper=2.0, mode="off_peak_discount")
    symmetric = expand(base, 0.2, config, lower=0.1, upper=2.0, mode="symmetric")
    reverse = expand(base, 0.2, config, lower=0.1, upper=2.0, mode="reverse_diagnostic")

    assert np.allclose(uniform, base)
    assert np.allclose(peak_only[shape <= 0.0], base)
    assert np.all(peak_only[shape > 0.0] > base)
    assert np.allclose(offpeak_only[shape >= 0.0], base)
    assert np.all(offpeak_only[shape < 0.0] < base)
    assert np.all(symmetric[shape > 0.0] > base)
    assert np.all(symmetric[shape < 0.0] < base)
    assert np.all(reverse[shape > 0.0] < base)
    assert np.all(reverse[shape < 0.0] > base)
    with pytest.raises(ValueError, match="nonnegative"):
        expand(base, -0.2, config, lower=0.1, upper=2.0, mode="symmetric")


def test_temporal_flows_conserve_each_origin_and_respect_shift_window():
    module_spec = util.find_spec("pricing_sim.spatiotemporal_mechanism")
    assert module_spec is not None
    module = import_module("pricing_sim.spatiotemporal_mechanism")
    reallocate = getattr(module, "conserved_temporal_flows", None)
    assert callable(reallocate)
    native = np.array([0.0, 100.0, 0.0, 0.0])
    destination_utility = np.array([0.0, 0.0, 3.0, 0.0])

    flows = reallocate(
        native,
        destination_utility,
        flexible_fraction=1.0,
        migration_cost=0.1,
        max_shift=1,
    )

    assert np.allclose(flows.sum(axis=1), native)
    origins, destinations = np.indices(flows.shape)
    assert np.allclose(flows[np.abs(origins - destinations) > 1], 0.0)
    assert flows[1, 2] > flows[1, 1]

    rigid = reallocate(
        native,
        destination_utility,
        flexible_fraction=0.0,
        migration_cost=0.1,
        max_shift=1,
    )
    assert np.allclose(rigid, np.diag(native))


def test_nested_allocation_separates_temporal_and_spatial_choices():
    module_spec = util.find_spec("pricing_sim.spatiotemporal_mechanism")
    assert module_spec is not None
    module = import_module("pricing_sim.spatiotemporal_mechanism")
    demand_spec = module.DemandResponseSpec(
        native_demand=np.array([
            [10.0, 40.0, 10.0],
            [10.0, 40.0, 10.0],
        ]),
        price_sensitivity=np.array([1.0, 4.0]),
        flexible_fraction=np.array([0.0, 1.0]),
        migration_cost=np.array([2.0, 0.1]),
        max_shift=np.array([0, 1]),
        channel_brand=np.ones(3),
        qos_weight=1.0,
    )
    prices = np.array([
        [1.0, 1.0, 1.0],
        [0.8, 1.4, 0.5],
        [1.2, 1.2, 1.2],
    ])
    qos = np.ones_like(prices)
    fixed_shares = np.array([0.2, 0.5, 0.3])

    neither = module.allocate_spatiotemporal_demand(
        prices,
        qos,
        demand_spec,
        temporal_enabled=False,
        spatial_enabled=False,
        fixed_channel_shares=fixed_shares,
    )
    combined = module.allocate_spatiotemporal_demand(
        prices,
        qos,
        demand_spec,
        temporal_enabled=True,
        spatial_enabled=True,
        fixed_channel_shares=fixed_shares,
    )

    total_native = float(np.sum(demand_spec.native_demand))
    assert np.isclose(np.sum(neither["channel_demand"]), total_native)
    assert np.isclose(np.sum(combined["channel_demand"]), total_native)
    assert np.allclose(
        neither["channel_demand"],
        fixed_shares[:, None] * demand_spec.native_demand.sum(axis=0)[None, :],
    )
    assert combined["channel_demand"][1, 2] > combined["channel_demand"][2, 2]
    assert combined["destination_demand_by_type"][1, 2] > neither["destination_demand_by_type"][1, 2]


def test_spatiotemporal_qos_solver_conserves_mass_and_reports_both_peak_metrics():
    module = import_module("pricing_sim.spatiotemporal_mechanism")
    solve = getattr(module, "solve_spatiotemporal_qos_fixed_point", None)
    summarize = getattr(module, "summarize_spatiotemporal_result", None)
    assert callable(solve)
    assert callable(summarize)
    demand_spec = module.DemandResponseSpec(
        native_demand=np.array([
            [20.0, 80.0, 20.0],
            [20.0, 80.0, 20.0],
        ]),
        price_sensitivity=np.array([1.0, 3.0]),
        flexible_fraction=np.array([0.0, 0.8]),
        migration_cost=np.array([2.0, 0.2]),
        max_shift=np.array([0, 1]),
        channel_brand=np.ones(3),
        qos_weight=1.0,
    )
    config = PeakShavingConfig.default().evolve(
        base_rigid=np.array([20.0, 80.0, 20.0]),
        time_preference=np.ones(3),
        native_rigid=np.array([0.2, 0.6, 0.2]),
        native_elastic=np.array([0.2, 0.6, 0.2]),
        load_shape_hat=np.array([-1.0, 1.0, -1.0]),
        firm_capacity=np.array([180.0, 90.0]),
    )
    prices = np.array([
        [0.8, 1.1, 0.8],
        [0.8, 0.9, 0.8],
        [0.8, 1.3, 0.8],
    ])
    routing = np.repeat(np.array([[2.0 / 3.0], [1.0 / 3.0]]), 3, axis=1)

    result = solve(
        prices,
        routing,
        demand_spec,
        config=config,
        temporal_enabled=True,
        spatial_enabled=True,
        fixed_channel_shares=np.array([0.2, 0.5, 0.3]),
        qos_shape="sigmoid",
    )
    metrics = summarize(result)

    assert result["converged"]
    assert result["fixed_point_residual"] <= 1e-8
    assert np.isclose(np.sum(result["demand"]), np.sum(demand_spec.native_demand))
    assert metrics["aggregate_peak_load"] == pytest.approx(
        np.max(np.sum(result["loads"], axis=0))
    )
    assert metrics["maximum_provider_utilization"] == pytest.approx(
        np.max(result["utilization"])
    )
    assert 0.0 < metrics["temporal_moved_fraction"] < 1.0
