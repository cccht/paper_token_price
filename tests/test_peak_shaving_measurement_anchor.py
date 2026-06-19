import csv
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from experiments.build_peak_shaving_measurement_anchor import (
    AnchorSource,
    build_anchor,
    plot_anchor,
    write_csv,
)


def _write_aggregate(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "concurrency",
                "repeats",
                "ttft_sla_0_5_rate_mean",
                "ttft_sla_0_5_rate_ci95",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def test_build_anchor_fits_two_profiles(tmp_path):
    first = tmp_path / "a.csv"
    second = tmp_path / "b.csv"
    meta = tmp_path / "meta.json"
    meta.write_text(json.dumps({"runtime": {"backend": "vllm"}}), encoding="utf-8")
    _write_aggregate(first, [
        {"concurrency": 64, "repeats": 3, "ttft_sla_0_5_rate_mean": 1.0, "ttft_sla_0_5_rate_ci95": 0.0},
        {"concurrency": 128, "repeats": 3, "ttft_sla_0_5_rate_mean": 1.0, "ttft_sla_0_5_rate_ci95": 0.0},
        {"concurrency": 256, "repeats": 3, "ttft_sla_0_5_rate_mean": 0.7, "ttft_sla_0_5_rate_ci95": 0.02},
    ])
    _write_aggregate(second, [
        {"concurrency": 32, "repeats": 2, "ttft_sla_0_5_rate_mean": 1.0, "ttft_sla_0_5_rate_ci95": 0.0},
        {"concurrency": 64, "repeats": 2, "ttft_sla_0_5_rate_mean": 1.0, "ttft_sla_0_5_rate_ci95": 0.0},
        {"concurrency": 128, "repeats": 2, "ttft_sla_0_5_rate_mean": 0.5, "ttft_sla_0_5_rate_ci95": 0.03},
    ])

    profiles, points, metadata = build_anchor([
        AnchorSource("vllm-0.5b", "small", first, meta),
        AnchorSource("vllm-3b", "large", second, meta),
    ])

    assert metadata["qos_definition"] == "TTFT SLA rate with threshold 0.5 seconds"
    assert len(profiles) == 2
    assert len(points) == 6
    assert profiles[0]["capacity_concurrency"] == 128.0
    assert profiles[1]["first_sla_drop_concurrency"] == 128.0


def test_write_csv_and_plot_anchor_create_outputs(tmp_path):
    profiles = [{
        "profile": "vllm-0.5b",
        "model": "small",
        "qos_threshold": 1.0,
        "qos_strength": 1.0,
    }]
    points = [
        {
            "profile": "vllm-0.5b",
            "model": "small",
            "source": "aggregate.csv",
            "concurrency": 64,
            "repeats": 2,
            "normalized_utilization": 1.0,
            "observed_qos": 1.0,
            "observed_qos_ci95": 0.0,
            "fitted_qos": 1.0,
        },
        {
            "profile": "vllm-0.5b",
            "model": "small",
            "source": "aggregate.csv",
            "concurrency": 128,
            "repeats": 2,
            "normalized_utilization": 2.0,
            "observed_qos": 0.5,
            "observed_qos_ci95": 0.03,
            "fitted_qos": 0.37,
        },
    ]

    csv_path = tmp_path / "points.csv"
    figure_path = tmp_path / "anchor.pdf"
    write_csv(csv_path, points)
    plot_anchor(profiles, points, figure_path)

    assert csv_path.exists()
    assert figure_path.exists()
    assert figure_path.with_suffix(".png").exists()
