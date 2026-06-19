"""Run bounded single-GPU vLLM capacity scans with automatic stop conditions."""

from __future__ import annotations

import argparse
import shutil
import time
from datetime import datetime
from pathlib import Path
import sys

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
for import_path in (PROJECT_ROOT, SCRIPT_DIR):
    path_text = str(import_path)
    if path_text not in sys.path:
        sys.path.insert(0, path_text)

from pricing_sim.system_benchmark import BenchmarkConfig, DEFAULT_PROMPT, write_benchmark_artifacts
from pricing_sim.system_runtime import collect_vllm_runtime_metadata
from pricing_sim.vllm_benchmark import run_level
from pricing_sim.vllm_extreme import (
    SafetyLimits,
    build_prompt_for_token_target,
    health_session,
    stop_reason,
    write_scan_checkpoint,
)
from pricing_sim.vllm_study import RequestSpec


def _healthy(endpoint: str) -> bool:
    try:
        return health_session().get(f"{endpoint}/v1/models", timeout=10).ok
    except requests.RequestException:
        return False


def _prompt_from_args(args: argparse.Namespace) -> str:
    if args.prompt_token_target is None:
        return " ".join([DEFAULT_PROMPT] * args.prompt_repeat)
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(args.model, local_files_only=True)
    return build_prompt_for_token_target(
        DEFAULT_PROMPT,
        args.prompt_token_target,
        count_tokens=lambda text: len(tokenizer.encode(text, add_special_tokens=False)),
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--endpoint", default="http://127.0.0.1:8000")
    parser.add_argument("--concurrency", type=int, nargs="+", required=True)
    parser.add_argument("--request-multiplier", type=int, default=4)
    parser.add_argument("--prompt-repeat", type=int, default=1)
    parser.add_argument("--prompt-token-target", type=int)
    parser.add_argument("--max-tokens", type=int, default=128)
    parser.add_argument("--cooldown-seconds", type=float, default=15.0)
    parser.add_argument("--timeout-seconds", type=float, default=180.0)
    parser.add_argument("--gpu-sample-interval-seconds", type=float, default=0.1)
    parser.add_argument("--max-temperature-celsius", type=float, default=82.0)
    parser.add_argument("--max-failure-rate", type=float, default=0.10)
    parser.add_argument("--min-free-disk-gib", type=float, default=30.0)
    parser.add_argument("--safety-disk-path", type=Path)
    parser.add_argument("--output-root", type=Path, default=PROJECT_ROOT / "artifacts" / "vllm-extreme")
    return parser.parse_args()


def _validate_args(args: argparse.Namespace) -> None:
    if args.request_multiplier <= 0 or args.prompt_repeat <= 0:
        raise ValueError("request multiplier and prompt repeat must be positive")
    if args.prompt_token_target is not None and args.prompt_token_target <= 0:
        raise ValueError("prompt token target must be positive")


def _run_scan_level(
    args: argparse.Namespace,
    concurrency: int,
    *,
    root: Path,
    runtime: dict,
    prompt: str,
    limits: SafetyLimits,
) -> dict:
    requests_per_level = concurrency * args.request_multiplier
    config = BenchmarkConfig(
        model=args.model,
        endpoint=args.endpoint,
        concurrency_levels=(concurrency,),
        requests_per_level=requests_per_level,
        warmup_requests=0,
        max_tokens=args.max_tokens,
        prompt=prompt,
        timeout_seconds=args.timeout_seconds,
        gpu_sample_interval_seconds=args.gpu_sample_interval_seconds,
    )
    specs = [RequestSpec(prompt, args.max_tokens, "extreme") for _ in range(requests_per_level)]
    samples: list[dict] = []
    records, summary = run_level(config, concurrency, request_specs=specs, gpu_samples_sink=samples)
    free_disk_gib = shutil.disk_usage(args.safety_disk_path or root).free / (1024**3)
    summary["stop_reason"] = stop_reason(
        summary,
        samples,
        free_disk_gib=free_disk_gib,
        service_healthy=_healthy(args.endpoint),
        limits=limits,
    )
    summary.update({
        "request_multiplier": args.request_multiplier,
        "prompt_repeat": args.prompt_repeat,
        "prompt_token_target": args.prompt_token_target,
        "free_disk_gib": free_disk_gib,
    })
    write_benchmark_artifacts(
        config,
        records,
        [summary],
        output_root=root / "levels",
        run_id=f"concurrency-{concurrency}",
        runtime_metadata=runtime,
        gpu_samples=samples,
    )
    return summary


def main() -> None:
    args = _parse_args()
    _validate_args(args)
    root = args.output_root / datetime.now().strftime("%Y%m%d-%H%M%S")
    root.mkdir(parents=True)
    runtime = collect_vllm_runtime_metadata(args.endpoint, args.model)
    prompt = _prompt_from_args(args)
    limits = SafetyLimits(args.max_temperature_celsius, args.max_failure_rate, args.min_free_disk_gib)
    summaries = []
    for concurrency in args.concurrency:
        summary = _run_scan_level(
            args, concurrency, root=root, runtime=runtime, prompt=prompt, limits=limits,
        )
        summaries.append(summary)
        write_scan_checkpoint(
            root,
            summaries,
            {"arguments": vars(args), "runtime": runtime},
        )
        print(summary, flush=True)
        if summary["stop_reason"]:
            break
        time.sleep(args.cooldown_seconds)
    write_scan_checkpoint(root, summaries, {"arguments": vars(args), "runtime": runtime})
    print(f"artifacts={root}")


if __name__ == "__main__":
    main()
