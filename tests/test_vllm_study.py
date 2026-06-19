from pricing_sim.vllm_study import (
    RequestSpec,
    aggregate_repeats,
    mixed_request_specs,
    poisson_offsets,
    randomized_orders,
    validate_controlled_scan,
)


def test_randomized_orders_preserve_levels_and_vary_order():
    levels = (64, 128, 224, 384, 512)

    orders = randomized_orders(levels, repeats=5, seed=7)

    assert len(orders) == 5
    assert all(sorted(order) == sorted(levels) for order in orders)
    assert len({tuple(order) for order in orders}) > 1


def test_poisson_offsets_are_deterministic_and_monotonic():
    offsets = poisson_offsets(requests=5, arrival_rate_rps=2.0, seed=11)

    assert offsets == poisson_offsets(requests=5, arrival_rate_rps=2.0, seed=11)
    assert offsets[0] == 0.0
    assert offsets == sorted(offsets)
    assert offsets[-1] > 0


def test_mixed_request_specs_include_multiple_lengths():
    specs = mixed_request_specs(requests=12, seed=3)

    assert len(specs) == 12
    assert all(isinstance(spec, RequestSpec) for spec in specs)
    assert len({spec.max_tokens for spec in specs}) > 1
    assert len({len(spec.prompt) for spec in specs}) > 1


def test_aggregate_repeats_reports_uncertainty():
    rows = [
        {"concurrency": 64, "throughput_tokens_per_second": 10.0},
        {"concurrency": 64, "throughput_tokens_per_second": 14.0},
    ]

    result = aggregate_repeats(rows, "concurrency", ("throughput_tokens_per_second",))

    assert result == [
        {
            "concurrency": 64,
            "repeats": 2,
            "throughput_tokens_per_second_mean": 12.0,
            "throughput_tokens_per_second_std": 2.8284271247461903,
            "throughput_tokens_per_second_ci95": 3.9199999999999995,
        }
    ]


def test_controlled_scan_rejects_request_count_below_peak_concurrency():
    try:
        validate_controlled_scan((64, 512), requests_per_level=256)
    except ValueError as error:
        assert "highest concurrency" in str(error)
    else:
        raise AssertionError("Expected undersized controlled scan to fail")


def test_aggregate_repeats_preserves_empty_metrics_for_failed_runs():
    rows = [{"concurrency": 64, "mean_ttft_seconds": None}]

    result = aggregate_repeats(rows, "concurrency", ("mean_ttft_seconds",))

    assert result[0]["mean_ttft_seconds_mean"] is None
