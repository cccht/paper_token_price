"""Checks for the reported atomic-user game, including adverse comparisons."""
import hashlib
import json

import numpy as np
import pytest

from experiments.run_user_provider_game import OUT, ROOT
from experiments.verify_user_provider_game import independent_state
from pricing_sim.user_time_game import UserGameConfig, UserPopulation


@pytest.fixture(scope="module")
def data():
    return json.loads((OUT / "experiment.json").read_text())


def test_sources_and_independent_certificate_are_current(data):
    for file, digest in data["metadata"]["source_sha256"].items():
        assert hashlib.sha256((ROOT / file).read_bytes()).hexdigest() == digest
    v = json.loads((OUT / "verification.json").read_text())
    assert v["passed"]
    assert v["experiment_sha256"] == hashlib.sha256((OUT / "experiment.json").read_bytes()).hexdigest()
    assert v["validator_sha256"] == hashlib.sha256((ROOT / "experiments/verify_user_provider_game.py").read_bytes()).hexdigest()
    assert sum(c["distinct_price_pairs"] for c in v["cases"]) == 50625


def test_prospective_utility_matches_stored_case(data):
    b = data["baseline"]
    users = UserPopulation(**{k: np.array(v) if v is not None else None for k, v in b["population"].items()})
    config = UserGameConfig(**b["configuration"])
    for name in ("before", "after"):
        state = b["representative"][name]
        actual = independent_state(state["actions"], b["representative"]["prices"], users, config)
        np.testing.assert_allclose(actual["utility"], state["utility"], atol=1e-12)
    assert actual["metrics"]["max_user_regret"] <= 1e-8


def test_comparisons_do_not_conflate_fixed_prices_and_price_games(data):
    analysis = json.loads((OUT / "analysis.json").read_text())
    o = data["baseline"]["outcomes"]
    np.testing.assert_allclose(analysis["same_prices_user_algorithm"]["per_user_expected_utility_change"],
                               np.array(o["tou_equilibrium"]["utility"]) - o["tou_initial"]["utility"])
    np.testing.assert_allclose(analysis["fair_tariff_comparison"]["per_user_expected_utility_change"],
                               np.array(o["tou_equilibrium"]["utility"]) - o["uniform_equilibrium"]["utility"])
    assert analysis["same_prices_user_algorithm"]["differences"]["mean_utility"] > 0
    assert analysis["fair_tariff_comparison"]["differences"]["mean_utility"] < 0
    assert analysis["replications"]["positive_count"] == 0


def test_plot_files_are_bound_to_experiment(data):
    manifest = json.loads((ROOT / "figures/user_provider_game_20260906/manifest.json").read_text())
    assert manifest["experiment_sha256"] == hashlib.sha256((OUT / "experiment.json").read_bytes()).hexdigest()
    for file, digest in manifest["figures_sha256"].items():
        assert hashlib.sha256((ROOT / file).read_bytes()).hexdigest() == digest
