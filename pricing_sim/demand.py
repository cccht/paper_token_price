from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.special import expit

from .config import SimulationConfig


@dataclass(frozen=True)
class DemandResult:
    rigid: np.ndarray
    flexible: np.ndarray
    total: np.ndarray
    converged: bool = True
    iterations: int = 0


def rigid_demand(prices: np.ndarray, config: SimulationConfig) -> np.ndarray:
    response = expit(config.rigid_churn_rate * (config.rigid_wtp - prices))
    return config.rigid_baseline * response


def _flexible_share(
    prices: np.ndarray,
    config: SimulationConfig,
    qos: np.ndarray | None = None,
) -> np.ndarray:
    effective_price = prices + config.inconvenience_cost * (1.0 - config.native_period_distribution)
    utility = -config.price_sensitivity * (effective_price - config.posted_price_cap)
    utility += np.log(config.time_preference + 1e-10)
    if qos is not None:
        utility -= config.qos_feedback_weight * (1.0 - qos)
    exp_utility = np.exp(utility - np.max(utility))
    return exp_utility / np.sum(exp_utility)


def flexible_demand(
    prices: np.ndarray,
    config: SimulationConfig,
    qos: np.ndarray | None = None,
) -> np.ndarray:
    share = _flexible_share(prices, config, qos)
    effective_price = prices + config.inconvenience_cost * (1.0 - config.native_period_distribution)
    average_effective_price = float(np.sum(share * effective_price))
    participation = expit(-config.price_sensitivity * (
        average_effective_price - config.posted_price_cap
    ))
    growth = 1.0 + config.market_growth * max(
        config.posted_price_cap - average_effective_price,
        0.0,
    )
    return config.flexible_baseline * growth * participation * share


def _combine_demand(
    prices: np.ndarray,
    config: SimulationConfig,
    qos: np.ndarray | None = None,
) -> DemandResult:
    rigid = rigid_demand(prices, config)
    flexible = flexible_demand(prices, config, qos)
    return DemandResult(rigid=rigid, flexible=flexible, total=rigid + flexible)


def compute_demand(prices: np.ndarray, config: SimulationConfig) -> DemandResult:
    result = _combine_demand(prices, config)
    if config.qos_feedback_weight <= 0:
        return result
    from .qos import qos_factor

    for iteration in range(1, 51):
        qos = qos_factor(
            result.total / config.capacity,
            threshold=config.qos_threshold,
            strength=config.qos_strength,
        )
        updated = _combine_demand(prices, config, qos)
        if np.max(np.abs(updated.total - result.total)) <= 1e-8:
            return DemandResult(
                updated.rigid,
                updated.flexible,
                updated.total,
                converged=True,
                iterations=iteration,
            )
        result = updated
    return DemandResult(
        result.rigid,
        result.flexible,
        result.total,
        converged=False,
        iterations=50,
    )
