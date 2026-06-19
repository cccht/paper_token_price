import csv

from pricing_sim.vllm_plots import write_vllm_plot, write_vllm_reliability_plot


def test_write_vllm_plot_creates_pdf(tmp_path):
    source = tmp_path / "summary.csv"
    with source.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "concurrency",
                "throughput_tokens_per_second",
                "mean_ttft_seconds",
                "p95_ttft_seconds",
                "ttft_sla_0_5_rate",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "concurrency": 1,
                "throughput_tokens_per_second": 100,
                "mean_ttft_seconds": 0.1,
                "p95_ttft_seconds": 0.2,
                "ttft_sla_0_5_rate": 1.0,
            }
        )

    output = write_vllm_plot(source)

    assert output.exists()


def test_write_vllm_reliability_plot_creates_pdf(tmp_path):
    source = tmp_path / "aggregate.csv"
    with source.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "concurrency",
                "throughput_tokens_per_second_mean",
                "throughput_tokens_per_second_ci95",
                "mean_ttft_seconds_mean",
                "mean_ttft_seconds_ci95",
                "ttft_sla_0_5_rate_mean",
                "ttft_sla_0_5_rate_ci95",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "concurrency": 64,
                "throughput_tokens_per_second_mean": 100,
                "throughput_tokens_per_second_ci95": 5,
                "mean_ttft_seconds_mean": 0.1,
                "mean_ttft_seconds_ci95": 0.01,
                "ttft_sla_0_5_rate_mean": 1.0,
                "ttft_sla_0_5_rate_ci95": 0.0,
            }
        )

    output = write_vllm_reliability_plot(source)

    assert output.exists()
