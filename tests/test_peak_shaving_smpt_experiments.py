from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from experiments.peak_shaving_smpt_tools import (
    admitted_fraction_for_threshold,
    build_phase_grid,
    congested_base,
    discount_only_params,
    evaluate_params,
    load_policy_vectors,
    params_from_vectors,
    peak_only_params,
    summarize_records,
    trace_fixed_point_residuals,
)
from pricing_sim.peak_shaving_equilibrium import FirmParams


def test_load_policy_vectors_contains_reported_cases():
    policies = load_policy_vectors()

    assert set(policies) == {"uniform", "dynamic_coarse", "dynamic_fine"}
    assert len(policies["dynamic_coarse"]) == 2
    assert all(len(vec) == 4 for vectors in policies.values() for vec in vectors)


def test_discount_only_removes_peak_surcharge():
    source = FirmParams(0.8, 0.3, 1.0, 0.2)
    transformed = discount_only_params(source)

    assert transformed.delta <= 0.0
    assert transformed.delta_d <= 0.0
    assert transformed.wbar == source.wbar
    assert transformed.pdbar == source.pdbar


def test_peak_only_removes_off_peak_discount():
    source = FirmParams(0.8, -0.3, 1.0, -0.2)
    transformed = peak_only_params(source)

    assert transformed.delta >= 0.0
    assert transformed.delta_d >= 0.0
    assert transformed.wbar == source.wbar
    assert transformed.pdbar == source.pdbar


def test_admitted_fraction_for_threshold_bounds_values():
    util = np.array([[0.5, 0.9], [0.4, 0.7]])
    fractions = admitted_fraction_for_threshold(util, threshold=0.8)

    assert fractions.shape == (2,)
    assert np.all(fractions >= 0.0)
    assert np.all(fractions <= 1.0)
    assert fractions[0] == 1.0
    assert np.isclose(fractions[1], 0.8 / 0.9)


def test_summarize_records_reports_reference_gains():
    records = [
        {"case": "uniform", "system_profit": 100.0, "minimum_qos": 0.7, "peak_utilization": 0.9},
        {"case": "candidate", "system_profit": 110.0, "minimum_qos": 0.8, "peak_utilization": 0.7},
    ]
    summary = summarize_records(records, reference_case="uniform")

    candidate = summary["candidate"]
    assert candidate["profit_gain_pct_vs_reference"] == 10.0
    assert np.isclose(candidate["qos_gain_vs_reference"], 0.1)
    assert np.isclose(candidate["peak_reduction_vs_reference"], 0.2)


def test_build_phase_grid_crosses_two_dimensions():
    rows = build_phase_grid(capacity_scales=[0.9, 1.1], alpha_scales=[0.8, 1.2])

    assert len(rows) == 4
    assert {row["capacity_scale"] for row in rows} == {0.9, 1.1}
    assert {row["alpha_scale"] for row in rows} == {0.8, 1.2}


def test_trace_fixed_point_residuals_reports_final_residual():
    policies = load_policy_vectors()
    params = params_from_vectors(policies["uniform"])
    record = evaluate_params("uniform", params, congested_base())
    trace = trace_fixed_point_residuals(record["prices"], record["routing"], congested_base())

    assert trace["iterations"] >= 1
    assert trace["final_residual"] >= 0.0
    assert len(trace["residuals"]) == trace["iterations"]


def test_trace_fixed_point_residuals_accepts_initial_qos_and_damping():
    policies = load_policy_vectors()
    params = params_from_vectors(policies["dynamic_coarse"])
    record = evaluate_params("dynamic_coarse", params, congested_base())
    trace = trace_fixed_point_residuals(
        record["prices"],
        record["routing"],
        congested_base(),
        initial_qos=0.5,
        damping=0.5,
    )

    assert trace["iterations"] >= 1
    assert trace["initial_qos"] == 0.5
    assert trace["damping"] == 0.5
    assert trace["final_residual"] >= 0.0


def test_static_shape_reproduces_congested_uniform_baseline():
    policies = load_policy_vectors()
    params = params_from_vectors(policies["uniform"])
    record = evaluate_params("uniform", params, congested_base(), static_shape=True)

    assert np.isclose(record["peak_utilization"], 0.7822217827449163)
    assert np.isclose(record["minimum_qos"], 0.756455957358171)
