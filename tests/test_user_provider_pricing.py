import numpy as np


def test_price_menus_are_nested_bounded_and_preserve_their_mean():
    from experiments.run_user_provider_game import inputs
    from experiments.user_provider_experiment_tools import price_menu

    _, signal, _ = inputs()
    previous = set()
    for level in (3, 5, 9):
        rules = price_menu(signal, base_count=level, slope_count=level)
        vectors = {tuple(r["prices"]) for r in rules}
        assert previous <= vectors
        for rule in rules:
            assert min(rule["prices"]) >= 0.30 - 1e-10
            assert max(rule["prices"]) <= 1.35 + 1e-10
            assert abs(np.mean(rule["prices"]) - rule["base"]) < 1e-10
        previous = vectors


def test_two_manufacturers_have_full_menu_deviation_checks():
    from experiments.user_provider_experiment_tools import solve_price_matrix

    a = np.array([[2.0, 0.0], [0.0, 1.0]])
    b = a.copy()
    result = solve_price_matrix(a, b)
    np.testing.assert_array_equal([1, 0], result["row_mix"])
    np.testing.assert_array_equal([1, 0], result["col_mix"])
    assert max(result["provider_regret"]) < 1e-10


def test_mixed_price_game_is_checked_without_a_pure_equilibrium():
    from experiments.user_provider_experiment_tools import solve_price_matrix

    a = np.array([[1.0, -1.0], [-1.0, 1.0]])
    result = solve_price_matrix(a, -a)
    np.testing.assert_allclose([0.5, 0.5], result["row_mix"], atol=1e-6)
    assert max(result["provider_regret"]) <= 1e-7


def test_population_comparisons_reuse_arrivals_costs_and_order():
    from experiments.run_user_provider_game import inputs, population

    profile, _, config = inputs()
    low = population(profile, config, flexible_share=0.25)
    high = population(profile, config, flexible_share=0.75)
    for field in ("release", "home", "delay_cost", "values", "order"):
        np.testing.assert_array_equal(getattr(low, field), getattr(high, field))
    assert np.all(~low.flexible | high.flexible)
    assert np.all(low.deadline >= low.release)
    assert np.all(high.deadline < config.periods)
