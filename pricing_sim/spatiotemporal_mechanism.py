from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .peak_shaving_config import PeakShavingConfig
from .peak_shaving_market import (
    FIXED_POINT_MAX_ITER,
    FIXED_POINT_TOL,
    QOS_DAMPING,
    _firm_loads,
    qos_factor,
)


@dataclass(frozen=True)
class DemandResponseSpec:
    native_demand: np.ndarray
    price_sensitivity: np.ndarray
    flexible_fraction: np.ndarray
    migration_cost: np.ndarray
    max_shift: np.ndarray
    channel_brand: np.ndarray
    qos_weight: float = 1.0


def _softmax(values: np.ndarray, axis: int = 0) -> np.ndarray:
    centered = values - np.max(values, axis=axis, keepdims=True)
    weights = np.exp(centered)
    return weights / np.sum(weights, axis=axis, keepdims=True)


def conserved_temporal_flows(
    native_demand: np.ndarray,
    destination_utility: np.ndarray,
    *,
    flexible_fraction: float,
    migration_cost: float,
    max_shift: int,
) -> np.ndarray:
    """Allocate each origin's mass over an allowed destination window."""
    native = np.asarray(native_demand, dtype=float)
    utility = np.asarray(destination_utility, dtype=float)
    if native.ndim != 1 or utility.shape != native.shape:
        raise ValueError("native demand and destination utility must be aligned vectors")
    if np.any(native < 0.0):
        raise ValueError("native demand must be nonnegative")
    if not 0.0 <= flexible_fraction <= 1.0:
        raise ValueError("flexible fraction must lie in [0, 1]")
    if migration_cost < 0.0 or max_shift < 0:
        raise ValueError("migration cost and max shift must be nonnegative")

    flows = np.zeros((native.size, native.size), dtype=float)
    for origin, mass in enumerate(native):
        flows[origin, origin] = (1.0 - flexible_fraction) * mass
        lo = max(0, origin - max_shift)
        hi = min(native.size, origin + max_shift + 1)
        destinations = np.arange(lo, hi)
        scores = utility[destinations] - migration_cost * np.abs(destinations - origin)
        probabilities = _softmax(scores, axis=0)
        flows[origin, destinations] += flexible_fraction * mass * probabilities
    return flows


def _validated_fixed_shares(shares: np.ndarray, channels: int, periods: int) -> np.ndarray:
    values = np.asarray(shares, dtype=float)
    if values.ndim == 1:
        values = np.repeat(values[:, None], periods, axis=1)
    if values.shape != (channels, periods) or np.any(values < 0.0):
        raise ValueError("fixed channel shares must be nonnegative and channel-period aligned")
    totals = np.sum(values, axis=0, keepdims=True)
    if np.any(totals <= 0.0):
        raise ValueError("fixed channel shares must have positive period totals")
    return values / totals


def _validate_spec(spec: DemandResponseSpec, channels: int, periods: int) -> None:
    native = np.asarray(spec.native_demand)
    if native.ndim != 2 or native.shape[1] != periods:
        raise ValueError("native demand must have shape (user_types, periods)")
    types = native.shape[0]
    for name in ("price_sensitivity", "flexible_fraction", "migration_cost", "max_shift"):
        if np.asarray(getattr(spec, name)).shape != (types,):
            raise ValueError(f"{name} must have one value per user type")
    if np.asarray(spec.channel_brand).shape != (channels,):
        raise ValueError("channel brand must have one value per channel")


def _channel_utility(
    prices: np.ndarray,
    qos: np.ndarray,
    spec: DemandResponseSpec,
    user_type: int,
) -> np.ndarray:
    brand = np.log(np.maximum(np.asarray(spec.channel_brand, dtype=float), 1e-12))[:, None]
    alpha = float(spec.price_sensitivity[user_type])
    return brand - alpha * prices - spec.qos_weight * (1.0 - qos)


def allocate_spatiotemporal_demand(
    prices: np.ndarray,
    qos: np.ndarray,
    spec: DemandResponseSpec,
    *,
    temporal_enabled: bool,
    spatial_enabled: bool,
    fixed_channel_shares: np.ndarray,
) -> dict[str, np.ndarray]:
    """Separate conserved temporal reallocation from within-period channel choice."""
    prices = np.asarray(prices, dtype=float)
    qos = np.asarray(qos, dtype=float)
    if prices.ndim != 2 or qos.shape != prices.shape:
        raise ValueError("prices and QoS must be aligned channel-period matrices")
    channels, periods = prices.shape
    _validate_spec(spec, channels, periods)
    fixed = _validated_fixed_shares(fixed_channel_shares, channels, periods)
    types = spec.native_demand.shape[0]
    flows = np.zeros((types, periods, periods), dtype=float)
    destination = np.zeros((types, periods), dtype=float)
    channel_by_type = np.zeros((types, channels, periods), dtype=float)

    for user_type in range(types):
        channel_utility = _channel_utility(prices, qos, spec, user_type)
        if spatial_enabled:
            destination_utility = np.log(np.sum(np.exp(channel_utility), axis=0))
            channel_shares = _softmax(channel_utility, axis=0)
        else:
            destination_utility = np.sum(fixed * channel_utility, axis=0)
            channel_shares = fixed
        if temporal_enabled:
            flows[user_type] = conserved_temporal_flows(
                spec.native_demand[user_type],
                destination_utility,
                flexible_fraction=float(spec.flexible_fraction[user_type]),
                migration_cost=float(spec.migration_cost[user_type]),
                max_shift=int(spec.max_shift[user_type]),
            )
        else:
            flows[user_type] = np.diag(spec.native_demand[user_type])
        destination[user_type] = np.sum(flows[user_type], axis=0)
        channel_by_type[user_type] = channel_shares * destination[user_type][None, :]

    return {
        "temporal_flows": flows,
        "destination_demand_by_type": destination,
        "channel_demand_by_type": channel_by_type,
        "channel_demand": np.sum(channel_by_type, axis=0),
    }


def _spatiotemporal_state(
    prices: np.ndarray,
    routing: np.ndarray,
    spec: DemandResponseSpec,
    *,
    config: PeakShavingConfig,
    qos_firm: np.ndarray,
    temporal_enabled: bool,
    spatial_enabled: bool,
    fixed_channel_shares: np.ndarray,
    qos_shape: str,
) -> tuple[dict[str, np.ndarray], np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    qos_channel = np.vstack([np.sum(routing * qos_firm, axis=0)[None, :], qos_firm])
    allocation = allocate_spatiotemporal_demand(
        prices,
        qos_channel,
        spec,
        temporal_enabled=temporal_enabled,
        spatial_enabled=spatial_enabled,
        fixed_channel_shares=fixed_channel_shares,
    )
    demand = allocation["channel_demand"]
    loads = _firm_loads(demand, routing)
    utilization = loads / np.maximum(config.firm_capacity[:, None], 1e-12)
    target_qos = qos_factor(utilization, config, qos_shape)
    return allocation, qos_channel, loads, utilization, target_qos


def solve_spatiotemporal_qos_fixed_point(
    prices: np.ndarray,
    routing: np.ndarray,
    spec: DemandResponseSpec,
    *,
    config: PeakShavingConfig,
    temporal_enabled: bool,
    spatial_enabled: bool,
    fixed_channel_shares: np.ndarray,
    qos_shape: str = "sigmoid",
) -> dict[str, np.ndarray | float | int | bool]:
    """Solve QoS feedback for a fixed routing and an identified demand mechanism."""
    prices = np.asarray(prices, dtype=float)
    routing = np.asarray(routing, dtype=float)
    if prices.shape != (3, config.num_periods):
        raise ValueError("prices must have shape (3, periods)")
    if routing.shape != (2, config.num_periods):
        raise ValueError("routing must have shape (2, periods)")
    qos_firm = np.ones((2, config.num_periods), dtype=float)
    iterations = 0
    for iterations in range(1, FIXED_POINT_MAX_ITER + 1):
        state = _spatiotemporal_state(
            prices, routing, spec, config=config, qos_firm=qos_firm,
            temporal_enabled=temporal_enabled, spatial_enabled=spatial_enabled,
            fixed_channel_shares=fixed_channel_shares, qos_shape=qos_shape,
        )
        residual = float(np.max(np.abs(state[-1] - qos_firm)))
        if residual <= FIXED_POINT_TOL:
            break
        qos_firm = QOS_DAMPING * state[-1] + (1.0 - QOS_DAMPING) * qos_firm
    allocation, qos_channel, loads, utilization, target_qos = _spatiotemporal_state(
        prices, routing, spec, config=config, qos_firm=qos_firm,
        temporal_enabled=temporal_enabled, spatial_enabled=spatial_enabled,
        fixed_channel_shares=fixed_channel_shares, qos_shape=qos_shape,
    )
    residual = float(np.max(np.abs(target_qos - qos_firm)))
    return {
        **allocation, "prices": prices, "routing": routing,
        "demand": allocation["channel_demand"], "loads": loads,
        "utilization": utilization, "qos_firm": qos_firm,
        "qos_channel": qos_channel, "fixed_point_residual": residual,
        "iterations": iterations, "converged": residual <= FIXED_POINT_TOL,
    }


def summarize_spatiotemporal_result(result: dict) -> dict[str, float | list[float]]:
    loads = np.asarray(result["loads"], dtype=float)
    utilization = np.asarray(result["utilization"], dtype=float)
    flows = np.asarray(result["temporal_flows"], dtype=float)
    destination = np.asarray(result["destination_demand_by_type"], dtype=float)
    aggregate = np.sum(loads, axis=0)
    diagonal = np.trace(flows, axis1=1, axis2=2).sum()
    total = float(np.sum(flows))
    periods = np.arange(1, destination.shape[1] + 1, dtype=float)
    centroids = [
        float(np.sum(periods * row) / max(np.sum(row), 1e-12))
        for row in destination
    ]
    return {
        "aggregate_peak_load": float(np.max(aggregate)),
        "aggregate_peak_to_average": float(np.max(aggregate) / np.mean(aggregate)),
        "maximum_provider_utilization": float(np.max(utilization)),
        "provider_utilization_imbalance": float(np.max(np.ptp(utilization, axis=0))),
        "minimum_provider_qos": float(np.min(result["qos_firm"])),
        "temporal_moved_fraction": float((total - diagonal) / max(total, 1e-12)),
        "destination_centroid_by_type": centroids,
        "total_demand": total,
    }
