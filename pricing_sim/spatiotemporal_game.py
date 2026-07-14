from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

from .peak_shaving_config import PeakShavingConfig
from .peak_shaving_equilibrium import FirmParams, expand_price, routing_from_beta
from .peak_shaving_market import (
    FIXED_POINT_MAX_ITER,
    FIXED_POINT_TOL,
    QOS_DAMPING,
    MarketState,
    _firm_loads,
    firm_profit,
    intermediary_profit,
    qos_factor,
    system_profit,
)
from .spatiotemporal_mechanism import (
    DemandResponseSpec,
    allocate_spatiotemporal_demand,
    summarize_spatiotemporal_result,
)

if TYPE_CHECKING:
    from .intermediary_response import IntermediarySearchSpec


@dataclass(frozen=True)
class SpatiotemporalGameSpec:
    demand: DemandResponseSpec
    fixed_channel_shares: np.ndarray
    temporal_enabled: bool = True
    spatial_enabled: bool = True
    qos_shape: str = "threshold"


def _joint_target(
    prices: np.ndarray,
    wholesale: np.ndarray,
    routing: np.ndarray,
    qos_firm: np.ndarray,
    route_beta: float,
    game: SpatiotemporalGameSpec,
    config: PeakShavingConfig,
) -> tuple[dict[str, np.ndarray], np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    qos_channel = np.vstack([
        np.sum(routing * qos_firm, axis=0)[None, :],
        qos_firm,
    ])
    allocation = allocate_spatiotemporal_demand(
        prices,
        qos_channel,
        game.demand,
        temporal_enabled=game.temporal_enabled,
        spatial_enabled=game.spatial_enabled,
        fixed_channel_shares=game.fixed_channel_shares,
    )
    loads = _firm_loads(allocation["channel_demand"], routing)
    utilization = loads / np.maximum(config.firm_capacity[:, None], 1e-12)
    target_qos = qos_factor(utilization, config, game.qos_shape)
    target_routing = routing_from_beta(
        wholesale, qos_firm, route_beta, config
    )
    return allocation, loads, utilization, target_qos, target_routing


def solve_spatiotemporal_joint_market(
    retail: np.ndarray,
    wholesale: np.ndarray,
    direct: np.ndarray,
    route_beta: float,
    game: SpatiotemporalGameSpec,
    config: PeakShavingConfig,
) -> tuple[MarketState, dict]:
    """Solve the coupled demand, routing, and QoS fixed point."""
    periods = config.num_periods
    retail = np.asarray(retail, dtype=float)
    wholesale = np.asarray(wholesale, dtype=float)
    direct = np.asarray(direct, dtype=float)
    if retail.shape != (periods,):
        raise ValueError("retail must have one value per period")
    if wholesale.shape != (2, periods) or direct.shape != (2, periods):
        raise ValueError("firm prices must have shape (2, periods)")
    if route_beta < 0.0:
        raise ValueError("route beta must be nonnegative")

    prices = np.vstack([retail[None, :], direct])
    routing = np.full((2, periods), 0.5, dtype=float)
    qos_firm = np.ones((2, periods), dtype=float)
    iterations = 0
    for iterations in range(1, FIXED_POINT_MAX_ITER + 1):
        _, _, _, target_qos, target_routing = _joint_target(
            prices, wholesale, routing, qos_firm, route_beta, game, config
        )
        qos_residual = float(np.max(np.abs(target_qos - qos_firm)))
        routing_residual = float(np.max(np.abs(target_routing - routing)))
        if max(qos_residual, routing_residual) <= FIXED_POINT_TOL:
            break
        qos_firm += QOS_DAMPING * (target_qos - qos_firm)
        routing += QOS_DAMPING * (target_routing - routing)

    allocation, loads, utilization, target_qos, target_routing = _joint_target(
        prices, wholesale, routing, qos_firm, route_beta, game, config
    )
    qos_residual = float(np.max(np.abs(target_qos - qos_firm)))
    routing_residual = float(np.max(np.abs(target_routing - routing)))
    joint_residual = max(qos_residual, routing_residual)
    qos_channel = np.vstack([
        np.sum(routing * qos_firm, axis=0)[None, :],
        qos_firm,
    ])
    state = MarketState(
        retail=retail,
        direct=direct,
        wholesale=wholesale,
        routing=routing,
    )
    result = {
        **allocation,
        "prices": prices,
        "routing": routing,
        "demand": allocation["channel_demand"],
        "loads": loads,
        "utilization": utilization,
        "qos_firm": qos_firm,
        "qos_channel": qos_channel,
        "joint_converged": joint_residual <= FIXED_POINT_TOL,
        "converged": joint_residual <= FIXED_POINT_TOL,
        "joint_iterations": iterations,
        "iterations": iterations,
        "joint_residual": joint_residual,
        "qos_residual": qos_residual,
        "routing_residual": routing_residual,
    }
    return state, result


def _default_intermediary_grids(
    config: PeakShavingConfig,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    bases = np.unique(np.array([0.8, 1.1, min(config.price_upper, 1.5)]))
    return bases, np.array([-0.3, 0.0, 0.3]), np.array([1.5, 4.0])


def intermediary_best_response_spatiotemporal(
    wholesale: np.ndarray,
    direct: np.ndarray,
    game: SpatiotemporalGameSpec,
    config: PeakShavingConfig,
    *,
    retail_base_grid: np.ndarray | None = None,
    retail_slope_grid: np.ndarray | None = None,
    route_beta_grid: np.ndarray | None = None,
) -> tuple[MarketState, dict]:
    defaults = _default_intermediary_grids(config)
    bases = defaults[0] if retail_base_grid is None else np.asarray(retail_base_grid)
    slopes = defaults[1] if retail_slope_grid is None else np.asarray(retail_slope_grid)
    betas = defaults[2] if route_beta_grid is None else np.asarray(route_beta_grid)
    best: tuple[MarketState, dict] | None = None
    best_profit = -np.inf
    evaluated_candidates = 0
    converged_candidates = 0
    for base in bases:
        for slope in slopes:
            retail = expand_price(
                float(base), float(slope), config,
                config.price_lower, config.price_upper,
            )
            for route_beta in betas:
                evaluated_candidates += 1
                state, result = solve_spatiotemporal_joint_market(
                    retail, wholesale, direct, float(route_beta), game, config
                )
                if not result["joint_converged"]:
                    continue
                converged_candidates += 1
                profit = intermediary_profit(state, result, config)
                if profit > best_profit:
                    best_profit = profit
                    result["intermediary_candidate"] = {
                        "retail_base": float(base),
                        "retail_slope": float(slope),
                        "route_beta": float(route_beta),
                    }
                    best = state, result
    if best is None:
        raise RuntimeError("no intermediary candidate reached the joint tolerance")
    best[1]["intermediary_search"] = {
        "method": "finite_grid",
        "retail_base_grid": bases.tolist(),
        "retail_slope_grid": slopes.tolist(),
        "route_beta_grid": betas.tolist(),
        "evaluated_candidates": evaluated_candidates,
        "converged_candidates": converged_candidates,
        "best_profit": best_profit,
    }
    return best


def evaluate_firm_pair_spatiotemporal(
    row_vector: np.ndarray,
    col_vector: np.ndarray,
    game: SpatiotemporalGameSpec,
    config: PeakShavingConfig,
    *,
    retail_base_grid: np.ndarray | None = None,
    retail_slope_grid: np.ndarray | None = None,
    route_beta_grid: np.ndarray | None = None,
    intermediary_search_spec: IntermediarySearchSpec | None = None,
) -> dict:
    firms = [
        FirmParams.from_vector(np.asarray(row_vector, dtype=float)),
        FirmParams.from_vector(np.asarray(col_vector, dtype=float)),
    ]
    wholesale = np.vstack([firm.wholesale(config) for firm in firms])
    direct = np.vstack([firm.direct(config) for firm in firms])
    if intermediary_search_spec is None:
        state, result = intermediary_best_response_spatiotemporal(
            wholesale,
            direct,
            game,
            config,
            retail_base_grid=retail_base_grid,
            retail_slope_grid=retail_slope_grid,
            route_beta_grid=route_beta_grid,
        )
    else:
        if any(
            grid is not None
            for grid in (retail_base_grid, retail_slope_grid, route_beta_grid)
        ):
            raise ValueError("continuous intermediary search cannot use grid arguments")
        from .intermediary_response import (
            optimize_intermediary_response_spatiotemporal,
        )

        state, result = optimize_intermediary_response_spatiotemporal(
            wholesale, direct, game, config, intermediary_search_spec
        )
    metrics = summarize_spatiotemporal_result(result)
    return {
        "firm_A_profit": firm_profit(0, state, result, config),
        "firm_B_profit": firm_profit(1, state, result, config),
        "intermediary_profit": intermediary_profit(state, result, config),
        "system_profit": system_profit(state, result, config),
        "aggregate_peak_load": metrics["aggregate_peak_load"],
        "aggregate_peak_to_average": metrics["aggregate_peak_to_average"],
        "maximum_provider_utilization": metrics["maximum_provider_utilization"],
        "provider_utilization_imbalance": metrics["provider_utilization_imbalance"],
        "minimum_provider_qos": metrics["minimum_provider_qos"],
        "temporal_moved_fraction": metrics["temporal_moved_fraction"],
        "total_demand": metrics["total_demand"],
        "joint_converged": result["joint_converged"],
        "joint_residual": result["joint_residual"],
        "state": state,
        "result": result,
    }
