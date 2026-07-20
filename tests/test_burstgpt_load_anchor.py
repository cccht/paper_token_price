from importlib import import_module, util
from pathlib import Path
import csv
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def _write_trace(path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "Timestamp", "Model", "Request tokens", "Response tokens",
            "Total tokens", "Log Type",
        ])
        for day in range(3):
            for period in range(8):
                writer.writerow([
                    day * 86400 + period * 10800 + 1,
                    "ChatGPT", 1, period, period + 1, "API log",
                ])


def test_burstgpt_anchor_uses_complete_days_and_normalizes_daily_profiles(tmp_path):
    module_spec = util.find_spec("experiments.build_burstgpt_load_anchor")
    assert module_spec is not None
    module = import_module("experiments.build_burstgpt_load_anchor")
    aggregate = getattr(module, "aggregate_trace", None)
    assert callable(aggregate)
    trace = tmp_path / "trace.csv"
    _write_trace(trace)

    result = aggregate(trace, periods=8, exclude_edge_days=True)

    expected_token_share = np.arange(1.0, 9.0) / np.sum(np.arange(1.0, 9.0))
    assert result["rows_read"] == 24
    assert result["days_used"] == [1]
    assert np.allclose(result["request_share_mean"], np.full(8, 1.0 / 8.0))
    assert np.allclose(result["token_share_mean"], expected_token_share)
    assert np.isclose(np.mean(result["normalized_token_load"]), 0.0)
    assert np.isclose(np.max(np.abs(result["normalized_token_load"])), 1.0)
    assert np.allclose(result["token_share_std"], 0.0)


def test_download_rejects_partial_cache_and_completes_source(tmp_path):
    module = import_module("experiments.build_burstgpt_load_anchor")
    source = tmp_path / "source.csv"
    cache = tmp_path / "cache.csv"
    source.write_bytes(b"0123456789")
    cache.write_bytes(b"0123")

    result = module.download_trace(
        source.as_uri(), cache, expected_bytes=source.stat().st_size
    )

    assert result == cache
    assert cache.read_bytes() == source.read_bytes()
