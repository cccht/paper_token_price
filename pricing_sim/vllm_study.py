from __future__ import annotations

import math
import random
import statistics
from dataclasses import dataclass
from typing import Any, Iterable

from pricing_sim.system_benchmark import DEFAULT_PROMPT


@dataclass(frozen=True)
class RequestSpec:
    prompt: str
    max_tokens: int
    workload_name: str = "fixed"


def randomized_orders(levels: tuple[int, ...], *, repeats: int, seed: int) -> list[list[int]]:
    rng = random.Random(seed)
    orders = []
    for _ in range(repeats):
        order = list(levels)
        rng.shuffle(order)
        orders.append(order)
    return orders


def validate_controlled_scan(levels: tuple[int, ...], *, requests_per_level: int) -> None:
    if requests_per_level < max(levels):
        raise ValueError("requests per level must cover the highest concurrency")


def poisson_offsets(*, requests: int, arrival_rate_rps: float, seed: int) -> list[float]:
    if requests <= 0 or arrival_rate_rps <= 0:
        raise ValueError("requests and arrival rate must be positive")
    rng = random.Random(seed)
    offsets = [0.0]
    for _ in range(requests - 1):
        offsets.append(offsets[-1] + rng.expovariate(arrival_rate_rps))
    return offsets


def mixed_request_specs(*, requests: int, seed: int) -> list[RequestSpec]:
    rng = random.Random(seed)
    choices = ((1, 64), (4, 128), (12, 256))
    specs = []
    for _ in range(requests):
        prompt_repeat, max_tokens = rng.choice(choices)
        specs.append(
            RequestSpec(
                prompt=" ".join([DEFAULT_PROMPT] * prompt_repeat),
                max_tokens=max_tokens,
                workload_name="mixed",
            )
        )
    return specs


def _summary(group: list[dict[str, Any]], field: str) -> dict[str, float]:
    values = [float(row[field]) for row in group if row.get(field) is not None]
    if not values:
        return {f"{field}_mean": None, f"{field}_std": None, f"{field}_ci95": None}
    std = statistics.stdev(values) if len(values) > 1 else 0.0
    return {
        f"{field}_mean": statistics.mean(values),
        f"{field}_std": std,
        f"{field}_ci95": 1.96 * std / math.sqrt(len(values)),
    }


def aggregate_repeats(
    rows: Iterable[dict[str, Any]],
    group_field: str,
    metric_fields: tuple[str, ...],
) -> list[dict[str, Any]]:
    groups: dict[Any, list[dict[str, Any]]] = {}
    for row in rows:
        groups.setdefault(row[group_field], []).append(row)
    results = []
    for value, group in sorted(groups.items()):
        result = {group_field: value, "repeats": len(group)}
        for field in metric_fields:
            result.update(_summary(group, field))
        results.append(result)
    return results
