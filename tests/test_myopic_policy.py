import numpy as np

from pricing_sim.config import SimulationConfig
from pricing_sim.optimize import optimize_myopic, optimize_qos_aware, uniform_pricing


def test_myopic_policy_is_evaluated_under_actual_qos_model():
    config = SimulationConfig.default(optimizer_trials=4, optimizer_maxiter=120)

    result = optimize_myopic(config, seed=7)

    assert result.search_qos_strength == 0.0
    assert result.evaluation_qos_strength == config.qos_strength
    assert np.min(result.policy.qos) < 1.0


def test_optimized_policies_satisfy_posted_price_cap():
    config = SimulationConfig.default(optimizer_trials=4, optimizer_maxiter=120)

    for result in [optimize_myopic(config, seed=3), optimize_qos_aware(config, seed=3)]:
        assert result.diagnostics.success
        assert result.diagnostics.solver_success
        assert result.diagnostics.cap_residual <= 1e-8
        assert result.diagnostics.lower_bound_residual <= 1e-12
        assert result.diagnostics.upper_bound_residual <= 1e-12


def test_bill_protection_limits_qos_aware_posted_bill_to_uniform_baseline():
    config = SimulationConfig.default(
        enforce_bill_protection=True,
        optimizer_trials=4,
        optimizer_maxiter=160,
    )

    uniform = uniform_pricing(config).policy
    protected = optimize_qos_aware(config, seed=3)

    assert protected.diagnostics.success
    assert isinstance(protected.diagnostics.solver_success, bool)
    assert protected.policy.posted_bill <= uniform.posted_bill + 1e-6
    assert protected.diagnostics.bill_cap_residual <= 1e-6
