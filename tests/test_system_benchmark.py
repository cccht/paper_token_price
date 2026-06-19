import json

from pricing_sim.system_benchmark import (
    BenchmarkConfig,
    _gpu_summary,
    parse_stream_lines,
    summarize_requests,
    write_benchmark_artifacts,
)


def test_parse_stream_lines_extracts_generation_metrics():
    lines = [
        json.dumps({"response": "A", "done": False}),
        json.dumps({"thinking": "B", "done": False}),
        json.dumps(
            {
                "done": True,
                "eval_count": 20,
                "eval_duration": 2_000_000_000,
                "prompt_eval_count": 8,
                "prompt_eval_duration": 400_000_000,
            }
        ),
    ]

    result = parse_stream_lines(lines)

    assert result["stream_chunks"] == 2
    assert result["generated_tokens"] == 20
    assert result["output_characters"] == 2
    assert result["tokens_per_second"] == 10.0
    assert result["tpot_seconds"] == 0.1


def test_summarize_requests_reports_tail_latency_and_success_rate():
    records = [
        {
            "concurrency": 2,
            "success": True,
            "latency_seconds": 1.0,
            "ttft_seconds": 0.2,
            "tokens_per_second": 10.0,
            "generated_tokens": 10,
            "prompt_tokens": 8,
        },
        {
            "concurrency": 2,
            "success": True,
            "latency_seconds": 3.0,
            "ttft_seconds": 0.6,
            "tokens_per_second": 20.0,
            "generated_tokens": 20,
            "prompt_tokens": 12,
        },
        {
            "concurrency": 2,
            "success": False,
            "latency_seconds": 4.0,
            "error": "timeout",
        },
    ]

    summary = summarize_requests(records, elapsed_seconds=4.0)

    assert summary["concurrency"] == 2
    assert summary["requests"] == 3
    assert summary["success_rate"] == 2 / 3
    assert summary["p95_latency_seconds"] == 3.0
    assert summary["mean_ttft_seconds"] == 0.4
    assert summary["throughput_tokens_per_second"] == 7.5
    assert summary["mean_prompt_tokens"] == 10
    assert summary["ttft_sla_0_5_rate"] == 1 / 3
    assert summary["ttft_sla_1_0_rate"] == 2 / 3


def test_benchmark_config_rejects_non_positive_concurrency():
    try:
        BenchmarkConfig(model="test", concurrency_levels=(0,))
    except ValueError as error:
        assert "concurrency" in str(error)
    else:
        raise AssertionError("Expected invalid concurrency to fail")


def test_benchmark_config_rejects_non_positive_gpu_sample_interval():
    try:
        BenchmarkConfig(model="test", gpu_sample_interval_seconds=0)
    except ValueError as error:
        assert "sample interval" in str(error)
    else:
        raise AssertionError("Expected invalid GPU sample interval to fail")


def test_artifact_writer_persists_runtime_metadata(tmp_path):
    config = BenchmarkConfig(model="test")
    records = [{"request_id": 1}]
    summaries = [{"concurrency": 1, "requests": 1}]

    artifact_dir = write_benchmark_artifacts(
        config,
        records,
        summaries,
        output_root=tmp_path,
        run_id="test-run",
        runtime_metadata={"gpu_name": "test-gpu"},
    )

    metadata = json.loads((artifact_dir / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["runtime"]["gpu_name"] == "test-gpu"


def test_artifact_writer_persists_gpu_time_series(tmp_path):
    config = BenchmarkConfig(model="test")

    artifact_dir = write_benchmark_artifacts(
        config,
        [{"request_id": 1}],
        [{"concurrency": 1, "requests": 1}],
        output_root=tmp_path,
        run_id="test-run",
        gpu_samples=[{"sampled_at_unix_seconds": 1.5, "gpu_utilization_percent": 80.0}],
    )

    lines = (artifact_dir / "gpu_samples.jsonl").read_text(encoding="utf-8").splitlines()
    assert json.loads(lines[0])["gpu_utilization_percent"] == 80.0


def test_gpu_summary_reports_temperature_power_and_memory_peaks():
    summary = _gpu_summary([
        {
            "gpu_utilization_percent": 80.0,
            "gpu_memory_used_mib": 12000.0,
            "gpu_temperature_celsius": 65.0,
            "gpu_power_draw_watts": 300.0,
        },
        {
            "gpu_utilization_percent": 95.0,
            "gpu_memory_used_mib": 18000.0,
            "gpu_temperature_celsius": 72.0,
            "gpu_power_draw_watts": 420.0,
        },
    ])

    assert summary["peak_gpu_memory_used_mib"] == 18000.0
    assert summary["peak_gpu_temperature_celsius"] == 72.0
    assert summary["peak_gpu_power_draw_watts"] == 420.0
