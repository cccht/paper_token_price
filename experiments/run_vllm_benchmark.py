"""Run controlled single-GPU vLLM inference measurements."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
for import_path in (PROJECT_ROOT, SCRIPT_DIR):
    path_text = str(import_path)
    if path_text not in sys.path:
        sys.path.insert(0, path_text)

from pricing_sim.system_benchmark import (
    BenchmarkConfig,
    DEFAULT_PROMPT,
    write_benchmark_artifacts,
)
from pricing_sim.system_runtime import collect_vllm_runtime_metadata
from pricing_sim.vllm_benchmark import run_benchmark


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--endpoint", default="http://127.0.0.1:8000")
    parser.add_argument("--concurrency", type=int, nargs="+", default=[1, 2, 4])
    parser.add_argument("--requests-per-level", type=int, default=6)
    parser.add_argument("--warmup-requests", type=int, default=1)
    parser.add_argument("--max-tokens", type=int, default=64)
    parser.add_argument("--prompt-repeat", type=int, default=1)
    parser.add_argument("--timeout-seconds", type=float, default=120.0)
    parser.add_argument("--gpu-sample-interval-seconds", type=float, default=0.25)
    parser.add_argument("--output-root", type=Path, default=PROJECT_ROOT / "artifacts")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    if args.prompt_repeat <= 0:
        raise ValueError("prompt repeat must be positive")
    config = BenchmarkConfig(
        model=args.model,
        endpoint=args.endpoint,
        concurrency_levels=tuple(args.concurrency),
        requests_per_level=args.requests_per_level,
        warmup_requests=args.warmup_requests,
        max_tokens=args.max_tokens,
        prompt=" ".join([DEFAULT_PROMPT] * args.prompt_repeat),
        timeout_seconds=args.timeout_seconds,
        gpu_sample_interval_seconds=args.gpu_sample_interval_seconds,
    )
    gpu_samples = []
    records, summaries = run_benchmark(config, gpu_samples_sink=gpu_samples)
    runtime = collect_vllm_runtime_metadata(args.endpoint, args.model)
    artifact_dir = write_benchmark_artifacts(
        config,
        records,
        summaries,
        output_root=args.output_root,
        runtime_metadata=runtime,
        gpu_samples=gpu_samples,
    )
    print(f"artifacts={artifact_dir}")
    for summary in summaries:
        print(summary)


if __name__ == "__main__":
    main()
