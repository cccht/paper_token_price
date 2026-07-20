from pathlib import Path
import hashlib
import json
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def test_active_vectors_drop_zero_probability_entries():
    from experiments.run_submission_spatiotemporal_sensitivity import _active_vectors

    game = {
        "row_support_vectors": [[1], [2]],
        "col_support_vectors": [[3], [4]],
        "row_mix": [1.0, 0.0],
        "col_mix": [1e-12, 1.0],
    }

    assert _active_vectors(game) == ([[1]], [[4]])


def test_unknown_scenario_is_rejected_before_solving(tmp_path):
    from experiments.run_submission_spatiotemporal_sensitivity import run_sensitivity

    baseline = tmp_path / "baseline.json"
    baseline.write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError, match="unknown sensitivity"):
        run_sensitivity(scenario_names=["missing"], baseline_path=baseline)


def test_submission_sensitivity_targets_audited_spaces():
    from experiments import run_submission_spatiotemporal_sensitivity as module

    assert module.BASELINE_PATH.name == "spatiotemporal_equilibrium_submission.json"
    assert module.SUMMARY_PATH.name == "spatiotemporal_sensitivity_submission.json"
    assert len(module.SCENARIOS) == 8


def test_submission_sensitivity_records_runner_hash():
    from experiments.run_submission_spatiotemporal_sensitivity import _source_hashes

    hashes = _source_hashes()

    assert "experiments/run_submission_spatiotemporal_sensitivity.py" in hashes
    assert all(len(value) == 64 for value in hashes.values())


def test_run_sensitivity_forwards_parallel_workers(tmp_path, monkeypatch):
    from experiments import run_submission_spatiotemporal_sensitivity as module

    baseline = tmp_path / "baseline.json"
    baseline.write_text(json.dumps({
        "candidate_grid": [[0.1, 0.2, 0.3, 0.4]],
        "intermediary_response": {"method": "continuous_multistart"},
        "dynamic": {
            "row_support_vectors": [[0.1, 0.2, 0.3, 0.4]],
            "col_support_vectors": [[0.1, 0.2, 0.3, 0.4]],
            "row_mix": [1.0],
            "col_mix": [1.0],
        },
    }), encoding="utf-8")
    captured = {}

    def fake_run_equilibria(**kwargs):
        captured.update(kwargs)
        return {"metadata": {"source_sha256": {}}}

    monkeypatch.setattr(module, "run_equilibria", fake_run_equilibria)
    monkeypatch.setattr(module, "_summary_row", lambda *args: {
        "scenario": args[0],
        "dynamic_full_max_regret": 0.0,
        "aggregate_peak_change_percent": 0.0,
    })
    monkeypatch.setattr(module, "_scenario_path", lambda name, output_dir=module.OUT: tmp_path / f"{name}.json")

    module.run_sensitivity(
        scenario_names=["capacity_low"],
        baseline_path=baseline,
        cache_root=tmp_path / "cache",
        output_dir=tmp_path,
        parallel_workers=3,
    )

    assert captured["parallel_workers"] == 3


def test_collect_summary_rejects_scenario_from_another_baseline(tmp_path):
    from experiments.run_submission_spatiotemporal_sensitivity import (
        collect_sensitivity_summary,
    )

    baseline = tmp_path / "baseline.json"
    baseline.write_text(json.dumps({
        "candidate_grid": [[0.1, 0.2, 0.3, 0.4]],
        "intermediary_response": {"method": "continuous_multistart"},
        "uniform": {},
        "dynamic": {},
    }), encoding="utf-8")
    scenario = tmp_path / "sensitivity_capacity_low_submission.json"
    scenario.write_text(json.dumps({
        "metadata": {"baseline_equilibrium": {"sha256": "0" * 64}},
    }), encoding="utf-8")

    with pytest.raises(ValueError, match="baseline SHA-256"):
        collect_sensitivity_summary(
            scenario_names=["capacity_low"],
            baseline_path=baseline,
            output_dir=tmp_path,
        )

    assert hashlib.sha256(baseline.read_bytes()).hexdigest() != "0" * 64
