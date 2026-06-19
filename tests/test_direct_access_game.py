from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pricing_sim.direct_access_game import (
    DIRECT_API_CAPACITY,
    direct_api_config,
    optimize_direct_access_stackelberg,
)
from pricing_sim.intermediary_market import IntermediaryConfig


def test_direct_api_option_enters_user_choice_and_gets_positive_demand():
    base = IntermediaryConfig.default(optimizer_trials=1, optimizer_maxiter=20)

    result = optimize_direct_access_stackelberg(base)
    direct_idx = result.retail_prices.shape[0] - 1

    assert result.retail_prices.shape[0] == base.num_intermediaries + 1
    assert result.demand[direct_idx].sum() > 0.0
    assert result.shares[direct_idx].sum() > 0.0
    assert result.diagnostics["direct_api_share"] > 0.0
    assert result.diagnostics["broker_count"] == base.num_intermediaries
    assert np.isclose(result.capacity[direct_idx].sum(), DIRECT_API_CAPACITY)


def test_direct_api_config_preserves_existing_brokers_and_adds_platform_channel():
    base = IntermediaryConfig.default()

    config = direct_api_config(base)

    assert config.num_intermediaries == base.num_intermediaries + 1
    assert np.allclose(config.intermediary_capacity[:-1], base.intermediary_capacity)
    assert np.isclose(config.intermediary_capacity[-1], DIRECT_API_CAPACITY)
