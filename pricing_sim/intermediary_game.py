from __future__ import annotations

import numpy as np

from .intermediary_market import IntermediaryConfig, qos_factor


def player_payoff(
    player: int,
    action: tuple[int, int],
    actions: list[tuple[int, int]],
    config: IntermediaryConfig,
) -> float:
    counts = _counts(actions, config)
    j, t = action
    preferred = player % config.num_periods
    price = config.base_retail_price + 0.05 * j
    capacity = config.intermediary_capacity[j] / config.num_periods
    adds_load = 1 if actions[player] != action else 0
    load = (counts[j, t] + adds_load) / max(capacity, 1e-8)
    congestion = 1.0 - float(qos_factor(np.array([load]), config)[0])
    return (
        np.log(config.time_preference[t] + 1e-10)
        - price
        - 0.2 * (t != preferred)
        - congestion
    )


def finite_player_potential(
    actions: list[tuple[int, int]],
    config: IntermediaryConfig,
) -> float:
    counts = _counts(actions, config)
    individual = 0.0
    for player, (j, t) in enumerate(actions):
        preferred = player % config.num_periods
        individual += np.log(config.time_preference[t] + 1e-10)
        individual -= config.base_retail_price + 0.05 * j
        individual -= 0.2 * (t != preferred)
    return float(individual - _congestion_potential(counts, config))


def _congestion_potential(counts: np.ndarray, config: IntermediaryConfig) -> float:
    value = 0.0
    for j in range(config.num_intermediaries):
        capacity = config.intermediary_capacity[j] / config.num_periods
        for t in range(config.num_periods):
            for k in range(1, int(counts[j, t]) + 1):
                load = k / max(capacity, 1e-8)
                value += 1.0 - float(qos_factor(np.array([load]), config)[0])
    return value


def _counts(actions: list[tuple[int, int]], config: IntermediaryConfig) -> np.ndarray:
    counts = np.zeros((config.num_intermediaries, config.num_periods), dtype=int)
    for j, t in actions:
        counts[j, t] += 1
    return counts
