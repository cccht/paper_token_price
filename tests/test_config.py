import numpy as np
import pytest

from pricing_sim.config import SimulationConfig


def test_default_config_has_compatible_period_vectors():
    config = SimulationConfig.default()

    assert config.num_periods == 8
    assert config.rigid_baseline.shape == (config.num_periods,)
    assert config.time_preference.shape == (config.num_periods,)
    assert config.native_period_distribution.shape == (config.num_periods,)
    assert np.isclose(np.sum(config.native_period_distribution), 1.0)


def test_config_rejects_infeasible_posted_price_cap():
    with pytest.raises(ValueError, match="posted_price_cap"):
        SimulationConfig.default(posted_price_cap=0.30)


def test_config_rejects_mismatched_period_vectors():
    with pytest.raises(ValueError, match="rigid_baseline"):
        SimulationConfig(
            rigid_baseline=np.array([1.0, 2.0]),
            time_preference=np.array([1.0]),
        )


def test_config_rejects_mismatched_native_period_distribution():
    with pytest.raises(ValueError, match="native_period_distribution"):
        SimulationConfig.default(native_period_distribution=np.array([1.0, 0.0]))


def test_config_rejects_unknown_billing_mode():
    with pytest.raises(ValueError, match="billing_mode"):
        SimulationConfig.default(billing_mode="unknown")


def test_config_rejects_negative_sla_penalty_rate():
    with pytest.raises(ValueError, match="sla_penalty_rate"):
        SimulationConfig.default(sla_penalty_rate=-0.1)


def test_config_rejects_non_positive_bill_cap_ratio():
    with pytest.raises(ValueError, match="bill_cap_ratio"):
        SimulationConfig.default(bill_cap_ratio=0.0)
