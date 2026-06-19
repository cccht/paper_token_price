import json

from pricing_sim.config import SimulationConfig
from pricing_sim.experiments import run_smoke_matrix
from pricing_sim.plots import write_plots
from pricing_sim.reporting import write_artifacts


def test_smoke_matrix_contains_required_policies_and_diagnostics(tmp_path):
    config = SimulationConfig.default(optimizer_trials=2, optimizer_maxiter=60)

    records = run_smoke_matrix(config)

    policies = {record["policy"] for record in records}
    assert {"uniform", "myopic", "qos_aware"} <= policies
    for record in records:
        assert record["diagnostics"]["cap_residual"] <= 1e-8
        assert "config" in record
        assert "prices" in record["policy_evaluation"]


def test_artifact_writer_persists_jsonl_and_summary(tmp_path):
    config = SimulationConfig.default(optimizer_trials=1, optimizer_maxiter=30)
    records = run_smoke_matrix(config)

    paths = write_artifacts(records, output_root=tmp_path, run_id="test-run")

    assert paths.raw_jsonl.exists()
    assert paths.summary_json.exists()
    assert paths.summary_csv.exists()
    assert paths.aggregate_json.exists()
    assert paths.aggregate_csv.exists()
    first = json.loads(paths.raw_jsonl.read_text(encoding="utf-8").splitlines()[0])
    assert first["experiment"] == "baseline"
    summary = json.loads(paths.summary_json.read_text(encoding="utf-8"))
    aggregate = json.loads(paths.aggregate_json.read_text(encoding="utf-8"))
    assert {"posted_bill", "effective_bill", "bill_cap_residual", "solver_success"} <= set(summary[0])
    assert {"posted_bill_mean", "effective_bill_mean"} <= set(aggregate[0])


def test_plot_writer_creates_baseline_figure(tmp_path):
    config = SimulationConfig.default(optimizer_trials=1, optimizer_maxiter=30)
    records = run_smoke_matrix(config)

    paths = write_plots(records, output_root=tmp_path, run_id="test-run")

    assert len(paths) >= 2
    assert all(path.exists() for path in paths)
