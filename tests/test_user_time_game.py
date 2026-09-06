from dataclasses import replace

import numpy as np
import pytest


def example():
    from pricing_sim.user_time_game import UserGameConfig, UserPopulation

    config = UserGameConfig(capacities=(1.0, 1.0), periods=2, period_hours=1.0)
    users = UserPopulation(release=np.array([0, 0, 0, 0]), deadline=np.array([0, 1, 1, 1]),
                           home=np.zeros(4, dtype=int), delay_cost=np.array([0.02] * 4),
                           flexible=np.array([False, True, True, True]), values=np.full(4, 2.0))
    return users, config, np.full((2, 2), 0.6)


def test_prospective_costs_include_the_deviating_users_own_load():
    from pricing_sim.user_time_game import prospective_costs

    users, config, prices = example()
    counts = np.array([1, 0, 1, 0])
    costs = prospective_costs(0, current=2, counts=counts, prices=prices, users=users, config=config)
    expected = 0.6 + 2 * (1 - np.exp(-config.qos_strength))
    assert costs[0] == pytest.approx(expected)
    assert costs[2] == pytest.approx(0.6 + config.switch_cost)
    assert np.isinf(costs[1]) and np.isinf(costs[3])


def test_exact_potential_difference_matches_individual_cost_change():
    from pricing_sim.user_time_game import evaluate_assignment, potential

    users, config, prices = example()
    before = np.zeros(4, dtype=int)
    after = before.copy()
    after[1] = 3
    expected = (evaluate_assignment(after, prices, users, config)["cost"][1]
                - evaluate_assignment(before, prices, users, config)["cost"][1])
    actual = potential(after, prices, users, config) - potential(before, prices, users, config)
    assert actual == pytest.approx(expected, abs=1e-12)


def test_best_response_terminates_at_an_exhaustively_checked_user_nash():
    from pricing_sim.user_time_game import evaluate_assignment, solve_user_game

    users, config, prices = example()
    result = solve_user_game(prices, users, config, record_trace=True)
    actions = result["actions"]
    current = result["utility"]
    for player in range(4):
        for action in range(4):
            if not users.release[player] <= action % 2 <= users.deadline[player]:
                continue
            changed = actions.copy()
            changed[player] = action
            utility = evaluate_assignment(changed, prices, users, config)["utility"][player]
            assert utility <= current[player] + config.user_tolerance
    assert result["max_user_regret"] <= config.user_tolerance
    assert np.all(np.diff([row["potential"] for row in result["trace"]]) <= 1e-10)


def test_released_work_never_moves_before_release_or_after_deadline():
    from pricing_sim.user_time_game import solve_user_game

    users, config, prices = example()
    users = replace(users, release=np.ones(4, dtype=int), deadline=np.ones(4, dtype=int))
    prices[:, 0] = 0.01
    result = solve_user_game(prices, users, config)
    assert np.all(result["actions"] % 2 == 1)


def test_tied_best_responses_keep_the_current_action():
    from pricing_sim.user_time_game import solve_user_game

    users, config, prices = example()
    config = replace(config, quality_weight=0, switch_cost=0)
    users = replace(users, delay_cost=np.zeros(4))
    initial = np.array([2, 1, 3, 0])
    result = solve_user_game(prices, users, config, initial=initial)
    np.testing.assert_array_equal(initial, result["actions"])
    assert result["moves"] == 0


def test_accounting_collects_exactly_the_users_posted_payments():
    from pricing_sim.user_time_game import evaluate_assignment

    users, config, prices = example()
    result = evaluate_assignment(np.array([0, 1, 2, 3]), prices, users, config)
    assert result["bill"].sum() == pytest.approx((result["counts"] * prices).sum())
    np.testing.assert_allclose(users.values - result["cost"], result["utility"])
