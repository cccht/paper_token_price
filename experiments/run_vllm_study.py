"""Run repeated, mixed-length, and Poisson-arrival vLLM measurements."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
import sys
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
for import_path in (PROJECT_ROOT, SCRIPT_DIR):
    path_text = str(import_path)
    if path_text not in sys.path:
        sys.path.insert(0, path_text)

from pricing_sim.system_benchmark import BenchmarkConfig, DEFAULT_PROMPT, write_benchmark_artifacts
from pricing_sim.system_runtime import collect_vllm_runtime_metadata
from pricing_sim.vllm_benchmark import run_benchmark, run_level
from pricing_sim.vllm_study import (
    aggregate_repeats,
    mixed_request_specs,
    poisson_offsets,
    randomized_orders,
    validate_controlled_scan,
)


METRICS = ("success_rate", "throughput_tokens_per_second", "mean_ttft_seconds", "p95_ttft_seconds", "ttft_sla_0_5_rate")


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _save_run(root: Path, run_id: str, config: BenchmarkConfig, runtime: dict[str, Any], records, summaries, samples) -> None:
    write_benchmark_artifacts(
        config,
        records,
        summaries,
        output_root=root,
        run_id=run_id,
        runtime_metadata=runtime,
        gpu_samples=samples,
    )


def _controlled(args, root: Path, runtime: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for repeat, order in enumerate(randomized_orders(tuple(args.concurrency), repeats=args.repeats, seed=args.seed), 1):
        config = _config(args, tuple(order), args.controlled_requests_per_level)
        samples: list[dict[str, Any]] = []
        records, summaries = run_benchmark(config, gpu_samples_sink=samples)
        for scan_order, summary in enumerate(summaries, 1):
            summary.update({"repeat": repeat, "scan_order": scan_order})
        _save_run(root / "controlled", f"repeat-{repeat:02d}", config, runtime, records, summaries, samples)
        rows.extend(summaries)
    return rows


def _mixed(args, root: Path, runtime: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    config = _config(args, (args.mixed_concurrency,), args.auxiliary_requests)
    for repeat in range(1, args.auxiliary_repeats + 1):
        specs = mixed_request_specs(requests=config.requests_per_level, seed=args.seed + repeat)
        samples: list[dict[str, Any]] = []
        records, summary = run_level(config, args.mixed_concurrency, request_specs=specs, gpu_samples_sink=samples)
        summary["repeat"] = repeat
        _save_run(root / "mixed", f"repeat-{repeat:02d}", config, runtime, records, [summary], samples)
        rows.append(summary)
    return rows


def _arrivals(args, root: Path, runtime: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    config = _config(args, (args.arrival_workers,), args.auxiliary_requests)
    for repeat, order in enumerate(randomized_orders(tuple(args.arrival_rate), repeats=args.auxiliary_repeats, seed=args.seed), 1):
        for scan_order, rate in enumerate(order, 1):
            offsets = poisson_offsets(requests=config.requests_per_level, arrival_rate_rps=rate, seed=args.seed + repeat + rate)
            samples: list[dict[str, Any]] = []
            records, summary = run_level(config, args.arrival_workers, submit_offsets=offsets, gpu_samples_sink=samples)
            summary.update({"arrival_rate_rps": rate, "repeat": repeat, "scan_order": scan_order})
            _save_run(root / "arrival", f"rate-{rate}-repeat-{repeat:02d}", config, runtime, records, [summary], samples)
            rows.append(summary)
    return rows


def _precondition(args, root: Path, runtime: dict[str, Any]) -> None:
    level = max(args.concurrency)
    config = _config(args, (level,), args.controlled_requests_per_level)
    samples: list[dict[str, Any]] = []
    records, summary = run_level(config, level, gpu_samples_sink=samples)
    _save_run(root / "precondition", "discarded-warmup", config, runtime, records, [summary], samples)


def _config(args, levels: tuple[int, ...], requests_per_level: int) -> BenchmarkConfig:
    return BenchmarkConfig(
        model=args.model,
        endpoint=args.endpoint,
        concurrency_levels=levels,
        requests_per_level=requests_per_level,
        warmup_requests=args.warmup_requests,
        max_tokens=args.max_tokens,
        prompt=DEFAULT_PROMPT,
        timeout_seconds=args.timeout_seconds,
        gpu_sample_interval_seconds=args.gpu_sample_interval_seconds,
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--endpoint", default="http://127.0.0.1:8000")
    parser.add_argument("--concurrency", type=int, nargs="+", default=[64, 128, 224, 384, 512])
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--controlled-requests-per-level", type=int, default=512)
    parser.add_argument("--auxiliary-requests", type=int, default=256)
    parser.add_argument("--auxiliary-repeats", type=int, default=3)
    parser.add_argument("--warmup-requests", type=int, default=2)
    parser.add_argument("--max-tokens", type=int, default=128)
    parser.add_argument("--mixed-concurrency", type=int, default=128)
    parser.add_argument("--arrival-workers", type=int, default=256)
    parser.add_argument("--arrival-rate", type=int, nargs="+", default=[8, 16, 32])
    parser.add_argument("--timeout-seconds", type=float, default=120.0)
    parser.add_argument("--gpu-sample-interval-seconds", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--mode", choices=("all", "controlled", "mixed", "arrival"), default="all")
    parser.add_argument("--output-root", type=Path, default=PROJECT_ROOT / "artifacts" / "vllm-study")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    validate_controlled_scan(tuple(args.concurrency), requests_per_level=args.controlled_requests_per_level)
    root = args.output_root / datetime.now().strftime("%Y%m%d-%H%M%S")
    root.mkdir(parents=True)
    runtime = collect_vllm_runtime_metadata(args.endpoint, args.model)
    if args.mode in ("all", "controlled"):
        _precondition(args, root, runtime)
        controlled = _controlled(args, root, runtime)
        _write_csv(root / "controlled_summary.csv", controlled)
        _write_csv(root / "controlled_aggregate.csv", aggregate_repeats(controlled, "concurrency", METRICS))
    if args.mode in ("all", "mixed"):
        mixed = _mixed(args, root, runtime)
        _write_csv(root / "mixed_summary.csv", mixed)
        _write_csv(root / "mixed_aggregate.csv", aggregate_repeats(mixed, "concurrency", METRICS))
    if args.mode in ("all", "arrival"):
        arrivals = _arrivals(args, root, runtime)
        _write_csv(root / "arrival_summary.csv", arrivals)
        _write_csv(root / "arrival_aggregate.csv", aggregate_repeats(arrivals, "arrival_rate_rps", METRICS))
    (root / "study_metadata.json").write_text(
        json.dumps({"arguments": vars(args), "runtime": runtime}, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    print(f"artifacts={root}")


if __name__ == "__main__":
    main()
