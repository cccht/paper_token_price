from __future__ import annotations

import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Iterable

import requests
from requests.adapters import HTTPAdapter

from pricing_sim.system_benchmark import (
    BenchmarkConfig,
    _gpu_sample,
    _gpu_summary,
    _sample_gpu,
    summarize_requests,
)
from pricing_sim.vllm_study import RequestSpec


SESSION = requests.Session()
SESSION.trust_env = False
SESSION.mount("http://", HTTPAdapter(pool_connections=1024, pool_maxsize=1024, pool_block=True))


def parse_completion_stream(lines: Iterable[str]) -> dict[str, Any]:
    chunks = 0
    characters = 0
    usage: dict[str, Any] = {}
    for line in lines:
        if not line.startswith("data: "):
            continue
        content = line[6:]
        if content == "[DONE]":
            continue
        payload = json.loads(content)
        text = "".join(choice.get("text", "") for choice in payload.get("choices", []))
        if text:
            chunks += 1
            characters += len(text)
        if payload.get("usage"):
            usage = payload["usage"]
    return {
        "stream_chunks": chunks,
        "output_characters": characters,
        "generated_tokens": int(usage.get("completion_tokens", 0)),
        "prompt_tokens": int(usage.get("prompt_tokens", 0)),
    }


def _run_request(
    config: BenchmarkConfig,
    concurrency: int,
    request_id: int,
    spec: RequestSpec | None = None,
) -> dict[str, Any]:
    spec = spec or RequestSpec(config.prompt, config.max_tokens)
    started_at = time.time()
    started = time.perf_counter()
    first_chunk: float | None = None
    lines = []
    try:
        response = SESSION.post(
            f"{config.endpoint}/v1/completions",
            json={
                "model": config.model,
                "prompt": spec.prompt,
                "stream": True,
                "stream_options": {"include_usage": True},
                "temperature": 0,
                "max_tokens": spec.max_tokens,
                "ignore_eos": True,
            },
            stream=True,
            timeout=config.timeout_seconds,
        )
        response.raise_for_status()
        for raw_line in response.iter_lines(decode_unicode=True):
            if not raw_line:
                continue
            lines.append(raw_line)
            if first_chunk is None and raw_line.startswith("data: {"):
                payload = json.loads(raw_line[6:])
                if any(choice.get("text") for choice in payload.get("choices", [])):
                    first_chunk = time.perf_counter()
        ended = time.perf_counter()
        metrics = parse_completion_stream(lines)
        decode_seconds = ended - (first_chunk or ended)
        tokens = metrics["generated_tokens"]
        return {
            "request_id": request_id,
            "concurrency": concurrency,
            "workload_name": spec.workload_name,
            "requested_max_tokens": spec.max_tokens,
            "request_started_at_unix_seconds": started_at,
            "request_ended_at_unix_seconds": time.time(),
            "success": True,
            "latency_seconds": ended - started,
            "ttft_seconds": (first_chunk or ended) - started,
            "tpot_seconds": decode_seconds / tokens if tokens else None,
            "tokens_per_second": tokens / decode_seconds if decode_seconds else None,
            **metrics,
        }
    except Exception as error:  # noqa: BLE001
        return {
            "request_id": request_id,
            "concurrency": concurrency,
            "workload_name": spec.workload_name,
            "requested_max_tokens": spec.max_tokens,
            "request_started_at_unix_seconds": started_at,
            "request_ended_at_unix_seconds": time.time(),
            "success": False,
            "latency_seconds": time.perf_counter() - started,
            "error": f"{type(error).__name__}: {error}",
        }


def run_level(
    config: BenchmarkConfig,
    concurrency: int,
    *,
    request_specs: list[RequestSpec] | None = None,
    submit_offsets: list[float] | None = None,
    gpu_samples_sink: list[dict[str, Any]] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
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
        futures = []
        submitted = time.perf_counter()
        for request_id in range(config.requests_per_level):
            if submit_offsets:
                time.sleep(max(0.0, submitted + submit_offsets[request_id] - time.perf_counter()))
            spec = request_specs[request_id] if request_specs else None
            futures.append(executor.submit(_run_request, config, concurrency, request_id, spec))
        records = [future.result() for future in as_completed(futures)]
    elapsed = time.perf_counter() - started
    stop.set()
    sampler.join(timeout=2)
    if gpu_samples_sink is not None:
        gpu_samples_sink.extend({**sample, "concurrency": concurrency} for sample in samples)
    return records, {**summarize_requests(records, elapsed_seconds=elapsed), **_gpu_summary(samples)}


def run_benchmark(
    config: BenchmarkConfig,
    *,
    gpu_samples_sink: list[dict[str, Any]] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    for request_id in range(config.warmup_requests):
        _run_request(config, 1, -request_id - 1)
    records = []
    summaries = []
    for concurrency in config.concurrency_levels:
        level_records, summary = run_level(
            config,
            concurrency,
            gpu_samples_sink=gpu_samples_sink,
        )
        records.extend(level_records)
        summaries.append(summary)
    return records, summaries
