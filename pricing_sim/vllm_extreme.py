from __future__ import annotations

from collections.abc import Callable
import csv
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

import requests


@dataclass(frozen=True)
class SafetyLimits:
    max_temperature_celsius: float = 82.0
    max_failure_rate: float = 0.10
    min_free_disk_gib: float = 30.0


def health_session() -> requests.Session:
    session = requests.Session()
    session.trust_env = False
    return session


def write_scan_checkpoint(
    root: Path,
    summaries: list[dict[str, Any]],
    metadata: dict[str, Any],
) -> None:
    root.mkdir(parents=True, exist_ok=True)
    if summaries:
        with (root / "summary.csv").open("w", newline="", encoding="utf-8-sig") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(summaries[0]))
            writer.writeheader()
            writer.writerows(summaries)
    (root / "metadata.json").write_text(
        json.dumps(metadata, default=str, indent=2),
        encoding="utf-8",
    )


def build_prompt_for_token_target(
    base_prompt: str,
    token_target: int,
    *,
    count_tokens: Callable[[str], int],
) -> str:
    if not base_prompt.strip():
        raise ValueError("base prompt must not be empty")
    if token_target <= 0:
        raise ValueError("token target must be positive")
    prompt = base_prompt
    token_count = count_tokens(prompt)
    if token_count <= 0:
        raise ValueError("base prompt must produce tokens")
    while token_count < token_target:
        prompt = f"{prompt} {base_prompt}"
        next_token_count = count_tokens(prompt)
        if next_token_count <= token_count:
            raise ValueError("repeated prompt must increase token count")
        token_count = next_token_count
    return prompt


def stop_reason(
    summary: dict[str, Any],
    gpu_samples: list[dict[str, Any]],
    *,
    free_disk_gib: float,
    service_healthy: bool,
    limits: SafetyLimits,
) -> str | None:
    if free_disk_gib < limits.min_free_disk_gib:
        return f"free disk below {limits.min_free_disk_gib:.1f} GiB"
    if not service_healthy:
        return "vLLM health check failed"
    failure_rate = 1.0 - float(summary["success_rate"])
    if failure_rate > limits.max_failure_rate:
        return f"request failure rate exceeded {limits.max_failure_rate:.0%}"
    temperatures = [
        float(sample["gpu_temperature_celsius"])
        for sample in gpu_samples
        if sample.get("gpu_temperature_celsius") is not None
    ]
    if temperatures and max(temperatures) > limits.max_temperature_celsius:
        return f"gpu temperature exceeded {limits.max_temperature_celsius:.1f} C"
    return None
