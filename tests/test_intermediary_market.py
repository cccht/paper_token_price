from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pricing_sim.fixed_capacity_game import optimize_fixed_capacity_stackelberg
from pricing_sim.intermediary_game import finite_player_potential, player_payoff
from pricing_sim.intermediary_market import (
    IntermediaryConfig,
    _choice_shares,
    _default_capacity,
    evaluate_three_layer_policy,
    run_three_layer_smoke,
)
from pricing_sim.three_stage_game import (
    _candidate_wholesale,
    optimize_three_stage_stackelberg,
    solve_middle_stage_nash,
)
from experiments.run_intermediary_experiment import _record


def test_user_choice_probabilities_sum_to_one():
    config = IntermediaryConfig.default()
    wholesale = np.full(config.num_periods, config.base_wholesale_price)
    retail = np.full((config.num_intermediaries, config.num_periods), config.base_retail_price)
    capacity = np.tile(config.intermediary_capacity[:, None] / config.num_periods, (1, config.num_periods))

    result = evaluate_three_layer_policy(wholesale, retail, capacity, config)

    assert np.isclose(np.sum(result.shares), 1.0)
    assert result.shares.shape == (config.num_intermediaries, config.num_periods)


def test_native_period_distribution_is_separate_from_time_preference():
    base = IntermediaryConfig.default()
    native = np.zeros(base.num_periods)
    native[0] = 1.0
    shifted = IntermediaryConfig.default(native_period_distribution=native)
    wholesale = np.full(base.num_periods, base.base_wholesale_price)
    retail = np.full((base.num_intermediaries, base.num_periods), base.base_retail_price)
    capacity = _default_capacity(base)

    base_result = evaluate_three_layer_policy(wholesale, retail, capacity, base)
    shifted_result = evaluate_three_layer_policy(wholesale, retail, capacity, shifted)

    assert np.isclose(np.sum(shifted.native_period_distribution), 1.0)
    assert not np.allclose(base_result.shares, shifted_result.shares)


def test_returned_choice_shares_match_returned_qos_fixed_point():
    config = IntermediaryConfig.default()
    wholesale = np.full(config.num_periods, config.base_wholesale_price)
    retail = np.full((config.num_intermediaries, config.num_periods), config.base_retail_price)
    capacity_share = config.time_preference / np.sum(config.time_preference)
    capacity = config.intermediary_capacity[:, None] * capacity_share[None, :]

    result = evaluate_three_layer_policy(wholesale, retail, capacity, config)
    expected = _choice_shares(result.retail_prices, result.qos, config)

    assert result.diagnostics["converged"]
    assert np.allclose(result.shares, expected, atol=1e-8)


def test_capacity_allocation_satisfies_nonnegative_total_capacity_constraints():
    config = IntermediaryConfig.default(optimizer_trials=1, optimizer_maxiter=20)
    records = run_three_layer_smoke(config)
    aware = records["three_layer_qos_aware"]

    assert np.all(aware.capacity >= 0.0)
    assert np.allclose(
        np.sum(aware.capacity, axis=1),
        config.intermediary_capacity,
        atol=1e-6,
    )


def test_single_intermediary_baseline_uses_total_market_capacity():
    config = IntermediaryConfig.default(optimizer_trials=1, optimizer_maxiter=20)
    records = run_three_layer_smoke(config)
    single = records["single_intermediary"]

    assert single.capacity.shape == (1, config.num_periods)
    assert np.isclose(np.sum(single.capacity), np.sum(config.intermediary_capacity))


def test_direct_platform_merges_retail_margin_into_platform_accounting():
    config = IntermediaryConfig.default(optimizer_trials=1, optimizer_maxiter=20)
    records = run_three_layer_smoke(config)
    uniform = records["uniform_retail"]
    direct = records["direct_platform"]

    assert np.isclose(direct.platform_revenue, uniform.system_profit)
    assert np.isclose(direct.intermediary_profit, 0.0)
    assert np.isclose(direct.system_profit, uniform.system_profit)
    assert np.isclose(sum(direct.intermediary_components.values()), 0.0)


def test_profit_components_are_consistent():
    config = IntermediaryConfig.default(optimizer_trials=1, optimizer_maxiter=20)
    records = run_three_layer_smoke(config)
    result = records["three_layer_qos_aware"]

    assert np.isclose(result.intermediary_profit, sum(result.intermediary_components.values()))
    assert np.isclose(result.system_profit, result.platform_revenue + result.intermediary_profit)
    assert result.platform_revenue > 0.0


def test_user_potential_difference_matches_single_player_deviation():
    config = IntermediaryConfig.default(num_players=9)
    actions = [(0, 0), (0, 0), (1, 1), (1, 2), (2, 2), (2, 2), (0, 1), (1, 0), (2, 1)]
    before = actions.copy()
    after = actions.copy()
    player = 3
    old_action = before[player]
    new_action = (0, 2)
    after[player] = new_action

    potential_delta = finite_player_potential(after, config) - finite_player_potential(before, config)
    payoff_delta = (
        player_payoff(player, new_action, before, config)
        - player_payoff(player, old_action, before, config)
    )

    assert np.isclose(potential_delta, payoff_delta)


def test_smoke_records_expose_prices_capacity_qos_profit_and_diagnostics():
    config = IntermediaryConfig.default(optimizer_trials=1, optimizer_maxiter=20)
    records = run_three_layer_smoke(config)

    assert {
        "uniform_retail",
        "direct_platform",
        "single_intermediary",
        "no_qos_pricing",
        "three_layer_qos_aware",
    } <= set(records)
    for result in records.values():
        assert result.wholesale_prices.shape == (config.num_periods,)
        assert result.retail_prices.shape == (result.capacity.shape[0], config.num_periods)
        assert result.demand.shape == result.retail_prices.shape
        assert result.qos.shape == result.retail_prices.shape
        assert "converged" in result.diagnostics
        assert "objective_evaluations" in result.diagnostics


def test_serialized_records_include_choice_shares():
    config = IntermediaryConfig.default(optimizer_trials=1, optimizer_maxiter=20)
    records = run_three_layer_smoke(config)
    serialized = _record(records["three_layer_qos_aware"], config)

    shares = np.asarray(serialized["shares"], dtype=float)
    assert shares.shape == records["three_layer_qos_aware"].retail_prices.shape
    assert np.isclose(np.sum(shares), 1.0)


def test_serialized_single_intermediary_config_matches_capacity():
    config = IntermediaryConfig.default(optimizer_trials=1, optimizer_maxiter=20)
    records = run_three_layer_smoke(config)
    serialized = _record(records["single_intermediary"], config)

    capacity = np.asarray(serialized["capacity"], dtype=float)
    serialized_budget = np.asarray(serialized["config"]["intermediary_capacity"], dtype=float)
    assert capacity.shape[0] == 1
    assert serialized_budget.shape == (1,)
    assert np.isclose(np.sum(capacity), serialized_budget[0])


def test_middle_stage_nash_optimizes_capacity_as_a_strategy():
    config = IntermediaryConfig.default(optimizer_maxiter=25)
    wholesale = np.full(config.num_periods, config.base_wholesale_price)

    result = solve_middle_stage_nash(wholesale, config)
    default_capacity = _default_capacity(config)

    assert np.all(result.policy.capacity >= 0.0)
    assert np.allclose(np.sum(result.policy.capacity, axis=1), config.intermediary_capacity)
    assert not np.allclose(result.policy.capacity, default_capacity)
    assert result.max_regret < 1e-3


def test_three_stage_stackelberg_reports_platform_and_nash_diagnostics():
    config = IntermediaryConfig.default(optimizer_trials=1, optimizer_maxiter=25)

    result = optimize_three_stage_stackelberg(config, policy="three_layer_qos_aware")

    assert result.diagnostics["platform_objective"] == "platform_revenue"
    assert result.diagnostics["nash_converged"]
    assert "max_nash_regret" in result.diagnostics
    assert result.diagnostics["max_nash_regret"] < 1e-3
    assert np.allclose(np.sum(result.capacity, axis=1), config.intermediary_capacity)


def test_congestion_proxy_search_reports_proxy_weight():
    from pricing_sim.three_stage_game import optimize_congestion_proxy_stackelberg

    config = IntermediaryConfig.default(optimizer_trials=1, optimizer_maxiter=25)

    result = optimize_congestion_proxy_stackelberg(config, proxy_weight=0.2)

    assert result.policy == "congestion_proxy_pricing"
    assert result.diagnostics["qos_aware_search"] is False
    assert result.diagnostics["congestion_proxy_weight"] == 0.2
    assert np.allclose(np.sum(result.capacity, axis=1), config.intermediary_capacity)


def test_stackelberg_random_seed_controls_platform_candidates():
    first = IntermediaryConfig.default(random_seed=7)
    second = IntermediaryConfig.default(random_seed=8)

    first_candidate = _candidate_wholesale(first, np.random.default_rng(first.random_seed), 1)
    second_candidate = _candidate_wholesale(second, np.random.default_rng(second.random_seed), 1)

    assert not np.allclose(first_candidate, second_candidate)


def test_fixed_capacity_ablation_keeps_default_capacity_and_reports_regret():
    config = IntermediaryConfig.default(optimizer_trials=1, optimizer_maxiter=25)

    result = optimize_fixed_capacity_stackelberg(config)

    assert result.diagnostics["capacity_strategic"] is False
    assert "max_nash_regret" in result.diagnostics
    assert np.allclose(result.capacity, _default_capacity(config))
    assert np.allclose(np.sum(result.capacity, axis=1), config.intermediary_capacity)
