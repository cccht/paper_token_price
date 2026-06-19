from pricing_sim.config import SimulationConfig
from pricing_sim.supplemental_experiments import (
    billing_ablation_records,
    constraint_ablation_records,
    coarse_grid_reference_records,
    empirical_profile_records,
    fairness_records,
    rule_baseline_records,
    scalability_records,
)


def test_rule_baselines_satisfy_posted_price_cap():
    config = SimulationConfig.default(optimizer_trials=2, optimizer_maxiter=40)

    records = rule_baseline_records(config)

    assert {"uniform", "time_of_use", "queue_aware", "best_observed"} <= {
        row["policy"] for row in records
    }
    assert all(row["cap_residual"] <= 1e-8 for row in records)


def test_billing_ablation_compares_three_modes():
    config = SimulationConfig.default(optimizer_trials=2, optimizer_maxiter=40)

    records = billing_ablation_records(config)

    assert {row["billing_mode"] for row in records} == {
        "effective",
        "full",
        "sla_penalty",
    }


def test_constraint_ablation_compares_fixed_mean_and_bill_protection():
    config = SimulationConfig.default(optimizer_trials=2, optimizer_maxiter=80)

    records = constraint_ablation_records(config)

    assert {row["constraint_mode"] for row in records} == {
        "fixed_mean",
        "fixed_mean_with_bill_protection",
    }
    protected = next(
        row for row in records
        if row["constraint_mode"] == "fixed_mean_with_bill_protection"
    )
    assert protected["bill_ratio_vs_uniform"] <= 1.0 + 1e-6


def test_coarse_grid_reference_enumerates_feasible_small_instance():
    config = SimulationConfig.default(optimizer_trials=2, optimizer_maxiter=80)

    records = coarse_grid_reference_records(config, periods=3, grid_step=0.20)

    assert len(records) == 1
    assert records[0]["periods"] == 3
    assert records[0]["feasible_grid_points"] > 0
    assert records[0]["slsqp_profit"] >= records[0]["grid_profit"] - 1e-6


def test_scalability_records_include_runtime_and_feasibility():
    config = SimulationConfig.default(optimizer_trials=1, optimizer_maxiter=20)

    records = scalability_records(config, period_counts=(8, 16), trial_counts=(1,))

    assert [row["periods"] for row in records] == [8, 16]
    assert all(row["runtime_seconds"] >= 0.0 for row in records)
    assert all(row["cap_residual"] <= 1e-8 for row in records)


def test_fairness_records_include_user_segments():
    config = SimulationConfig.default()

    records = fairness_records(config)

    assert {row["segment"] for row in records} == {
        "low_sensitivity",
        "medium_sensitivity",
        "high_sensitivity",
    }
    assert all(row["mean_effective_price"] > 0.0 for row in records)
    assert all(row["mean_qos"] > 0.0 for row in records)
    assert all(row["effective_spending"] > 0.0 for row in records)


def test_empirical_profile_records_compare_fitted_qos_parameters():
    config = SimulationConfig.default(optimizer_trials=2, optimizer_maxiter=40)

    records = empirical_profile_records(
        config,
        profiles=(("measured", 1.0, 0.5),),
    )

    assert {row["profile"] for row in records} == {"synthetic_default", "measured"}
    assert all(row["cap_residual"] <= 1e-8 for row in records)
