from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from experiments.run_calibration_uncertainty_experiments import (
    measured_qos_stress_rows,
    parameter_audit_rows,
    uncertainty_sweep_rows,
)


def test_parameter_audit_rows_separate_measured_and_synthetic_inputs():
    rows = parameter_audit_rows()

    names = {row["parameter"] for row in rows}

    assert "qos_threshold" in names
    assert "price_sensitivity" in names
    assert "direct_api_preference" in names
    assert {row["source_type"] for row in rows} >= {"measured", "synthetic", "assumed"}


def test_uncertainty_sweep_rows_report_survival_flags():
    rows = uncertainty_sweep_rows(
        trials=1,
        maxiter=20,
        variants=("low_elasticity",),
    )

    assert len(rows) == 2
    policies = {row["policy"] for row in rows}
    assert policies == {"user_protected_revenue", "direct_api_user_choice"}
    for row in rows:
        assert row["variant"] == "low_elasticity"
        assert np.isfinite(row["platform_revenue_gain_vs_uniform"])
        assert np.isfinite(row["inclusive_value_gain_vs_uniform"])
        assert isinstance(row["improves_revenue_and_user_experience"], bool)


def test_measured_qos_stress_rows_include_adaptation_baseline():
    rows = measured_qos_stress_rows(
        ROOT,
        trials=1,
        maxiter=20,
        demand_scales=(1.15,),
        capacity_scales=(0.85,),
    )

    policies = {row["policy"] for row in rows}

    assert "measured_qos_fixed_capacity" in policies
    assert "measured_qos_adaptive_capacity" in policies
    for row in rows:
        assert row["experiment"] == "measured_qos_stress"
        assert row["capacity_scale"] == 0.85
        assert row["demand_scale"] == 1.15
        assert "profile" in row
