from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from experiments.run_intermediary_reality_experiments import (
    calibrated_qos_profiles,
    summarize_seed_rows,
)


def test_calibrated_qos_profiles_load_existing_vllm_measurements():
    profiles = calibrated_qos_profiles(ROOT)

    names = {profile.name for profile in profiles}
    assert {"vllm-study", "vllm-study-qwen25-3b"} <= names
    assert all(profile.threshold >= 1.0 for profile in profiles)
    assert all(profile.strength >= 0.0 for profile in profiles)
    assert all(profile.rmse >= 0.0 for profile in profiles)


def test_summarize_seed_rows_reports_mean_std_and_best_gap():
    rows = [
        {"seed": 0, "system_profit": 10.0, "min_qos": 0.90, "max_nash_regret": 1e-4},
        {"seed": 1, "system_profit": 20.0, "min_qos": 0.95, "max_nash_regret": 2e-4},
        {"seed": 2, "system_profit": 30.0, "min_qos": 1.00, "max_nash_regret": 3e-4},
    ]

    summary = summarize_seed_rows(rows)

    assert summary["runs"] == 3
    assert np.isclose(summary["system_profit_mean"], 20.0)
    assert summary["system_profit_best"] == 30.0
    assert np.isclose(summary["best_gap_vs_mean"], 10.0)
    assert np.isclose(summary["min_qos_mean"], 0.95)
