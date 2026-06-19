from __future__ import annotations

import csv
import json
import statistics
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

import requests


DEFAULT_PROMPT = (
    "Explain in two concise sentences why batching can improve GPU inference "
    "throughput. Do not use a list."
)


@dataclass(frozen=True)
class BenchmarkConfig:
    model: str
    endpoint: str = "http://127.0.0.1:11434"
    concurrency_levels: tuple[int, ...] = (1, 2, 4)
    requests_per_level: int = 6
    warmup_requests: int = 1
    max_tokens: int = 64
    timeout_seconds: float = 120.0
    prompt: str = DEFAULT_PROMPT
    gpu_sample_interval_seconds: float = 0.25

    def __post_init__(self) -> None:
        if not self.model:
            raise ValueError("model must not be empty")
        if not self.concurrency_levels or min(self.concurrency_levels) <= 0:
            raise ValueError("concurrency levels must be positive")
        if self.requests_per_level <= 0 or self.max_tokens <= 0:
            raise ValueError("request count and max tokens must be positive")
        if self.gpu_sample_interval_seconds <= 0:
            raise ValueError("GPU sample interval must be positive")


def _nanoseconds_to_seconds(value: Any) -> float | None:
    return None if value is None else float(value) / 1_000_000_000


def parse_stream_lines(lines: Iterable[str]) -> dict[str, Any]:
    chunks = 0
    characters = 0
    final: dict[str, Any] = {}
    for line in lines:
        payload = json.loads(line)
        text = payload.get("response", "") or payload.get("thinking", "")
        if text:
            chunks += 1
            characters += len(text)
        if payload.get("done"):
            final = payload
    tokens = int(final.get("eval_count", 0))
    eval_seconds = _nanoseconds_to_seconds(final.get("eval_duration"))
    return {
        "stream_chunks": chunks,
        "output_characters": characters,
        "generated_tokens": tokens,
        "prompt_tokens": int(final.get("prompt_eval_count", 0)),
        "eval_seconds": eval_seconds,
        "prompt_eval_seconds": _nanoseconds_to_seconds(final.get("prompt_eval_duration")),
        "load_seconds": _nanoseconds_to_seconds(final.get("load_duration")),
        "backend_total_seconds": _nanoseconds_to_seconds(final.get("total_duration")),
        "tokens_per_second": tokens / eval_seconds if eval_seconds else None,
        "tpot_seconds": eval_seconds / tokens if tokens else None,
    }


def _percentile(values: list[float], percentile: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, int(len(ordered) * percentile + 0.999999) - 1))
    return ordered[index]


def summarize_requests(
    records: list[dict[str, Any]],
    *,
    elapsed_seconds: float,
) -> dict[str, Any]:
    successful = [record for record in records if record["success"]]
    latencies = [float(record["latency_seconds"]) for record in successful]
    ttfts = [float(record["ttft_seconds"]) for record in successful]
    rates = [
        float(record["tokens_per_second"])
        for record in successful
        if record.get("tokens_per_second") is not None
    ]
    tpots = [
        float(record["tpot_seconds"])
        for record in successful
        if record.get("tpot_seconds") is not None
    ]
    prompt_tokens = [
        int(record["prompt_tokens"])
        for record in successful
        if record.get("prompt_tokens") is not None
    ]
    tokens = sum(int(record["generated_tokens"]) for record in successful)
    sla_rates = {
        f"ttft_sla_{threshold:.1f}".replace(".", "_") + "_rate": (
            sum(value <= threshold for value in ttfts) / len(records)
        )
        for threshold in (0.5, 1.0, 2.0)
    }
    return {
        "concurrency": records[0]["concurrency"],
        "requests": len(records),
        "successful_requests": len(successful),
        "success_rate": len(successful) / len(records),
        "elapsed_seconds": elapsed_seconds,
        "mean_latency_seconds": statistics.mean(latencies) if latencies else None,
        "p95_latency_seconds": _percentile(latencies, 0.95),
        "mean_ttft_seconds": statistics.mean(ttfts) if ttfts else None,
        "p95_ttft_seconds": _percentile(ttfts, 0.95),
        "mean_tpot_seconds": statistics.mean(tpots) if tpots else None,
        "mean_prompt_tokens": statistics.mean(prompt_tokens) if prompt_tokens else None,
        "mean_request_tokens_per_second": statistics.mean(rates) if rates else None,
        "throughput_tokens_per_second": tokens / elapsed_seconds,
        "generated_tokens": tokens,
        **sla_rates,
    }


def _run_request(config: BenchmarkConfig, concurrency: int, request_id: int) -> dict[str, Any]:
    started = time.perf_counter()
    first_chunk: float | None = None
    lines = []
    try:
        response = requests.post(
            f"{config.endpoint}/api/generate",
            json={
                "model": config.model,
                "prompt": config.prompt,
                "stream": True,
                "options": {"temperature": 0, "num_predict": config.max_tokens},
            },
            stream=True,
            timeout=config.timeout_seconds,
        )
        response.raise_for_status()
        for raw_line in response.iter_lines(decode_unicode=True):
            if not raw_line:
                continue
            lines.append(raw_line)
            payload = json.loads(raw_line)
            if first_chunk is None and (payload.get("response") or payload.get("thinking")):
                first_chunk = time.perf_counter()
        metrics = parse_stream_lines(lines)
        ended = time.perf_counter()
        return {
            "request_id": request_id,
            "concurrency": concurrency,
            "success": True,
            "latency_seconds": ended - started,
            "ttft_seconds": (first_chunk or ended) - started,
            **metrics,
        }
    except Exception as error:  # noqa: BLE001
        return {
            "request_id": request_id,
            "concurrency": concurrency,
            "success": False,
            "latency_seconds": time.perf_counter() - started,
            "error": f"{type(error).__name__}: {error}",
        }


def _gpu_sample() -> dict[str, float] | None:
    command = [
        "nvidia-smi",
        "--query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu,power.draw",
        "--format=csv,noheader,nounits",
    ]
    result = subprocess.run(command, capture_output=True, text=True, timeout=5, check=False)
    if result.returncode:
        return None
    utilization, memory_used, memory_total, temperature, power_draw = (
        result.stdout.splitlines()[0].split(",")
    )
    return {
        "sampled_at_unix_seconds": time.time(),
        "gpu_utilization_percent": float(utilization.strip()),
        "gpu_memory_used_mib": float(memory_used.strip()),
        "gpu_memory_total_mib": float(memory_total.strip()),
        "gpu_temperature_celsius": float(temperature.strip()),
        "gpu_power_draw_watts": float(power_draw.strip()),
    }


def _sample_gpu(stop: threading.Event, interval: float, samples: list[dict[str, float]]) -> None:
    while not stop.is_set():
        sample = _gpu_sample()
        if sample:
            samples.append(sample)
        stop.wait(interval)


def _gpu_summary(samples: list[dict[str, float]]) -> dict[str, float | None]:
    if not samples:
        return {
            "mean_gpu_utilization_percent": None,
            "peak_gpu_memory_used_mib": None,
            "peak_gpu_temperature_celsius": None,
            "peak_gpu_power_draw_watts": None,
        }
    return {
        "mean_gpu_utilization_percent": statistics.mean(
            sample["gpu_utilization_percent"] for sample in samples
        ),
        "peak_gpu_memory_used_mib": max(sample["gpu_memory_used_mib"] for sample in samples),
        "peak_gpu_temperature_celsius": max(
            sample["gpu_temperature_celsius"] for sample in samples
        ),
        "peak_gpu_power_draw_watts": max(sample["gpu_power_draw_watts"] for sample in samples),
    }


def run_level(config: BenchmarkConfig, concurrency: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    stop = threading.Event()
    samples: list[dict[str, float]] = []
    sampler = threading.Thread(
        target=_sample_gpu,
        args=(stop, config.gpu_sample_interval_seconds, samples),
        daemon=True,
    )
    sampler.start()
    started = time.perf_counter()
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [
            executor.submit(_run_request, config, concurrency, request_id)
            for request_id in range(config.requests_per_level)
        ]
        records = [future.result() for future in as_completed(futures)]
    elapsed = time.perf_counter() - started
    stop.set()
    sampler.join(timeout=2)
    return records, {**summarize_requests(records, elapsed_seconds=elapsed), **_gpu_summary(samples)}


def run_benchmark(config: BenchmarkConfig) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    for request_id in range(config.warmup_requests):
        _run_request(config, 1, -request_id - 1)
    records = []
    summaries = []
    for concurrency in config.concurrency_levels:
        level_records, summary = run_level(config, concurrency)
        records.extend(level_records)
        summaries.append(summary)
    return records, summaries


def write_benchmark_artifacts(
    config: BenchmarkConfig,
    records: list[dict[str, Any]],
    summaries: list[dict[str, Any]],
    *,
    output_root: Path,
    run_id: str | None = None,
    runtime_metadata: dict[str, Any] | None = None,
    gpu_samples: list[dict[str, Any]] | None = None,
) -> Path:
    artifact_dir = output_root / "system" / (run_id or datetime.now().strftime("%Y%m%d-%H%M%S"))
    artifact_dir.mkdir(parents=True, exist_ok=True)
    (artifact_dir / "raw_requests.jsonl").write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
        encoding="utf-8",
    )
    (artifact_dir / "gpu_samples.jsonl").write_text(
        "".join(json.dumps(sample, ensure_ascii=False) + "\n" for sample in (gpu_samples or [])),
        encoding="utf-8",
    )
    (artifact_dir / "summary.json").write_text(
        json.dumps(summaries, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    with (artifact_dir / "summary.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summaries[0]))
        writer.writeheader()
        writer.writerows(summaries)
    metadata = {
        "config": asdict(config),
        "runtime": runtime_metadata or {},
        "generated_at": datetime.now().isoformat(),
    }
    (artifact_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return artifact_dir
