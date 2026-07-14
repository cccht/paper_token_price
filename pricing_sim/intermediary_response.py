from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING

import numpy as np
from scipy.optimize import minimize

from .peak_shaving_equilibrium import expand_price
from .peak_shaving_market import intermediary_profit

if TYPE_CHECKING:
    from .peak_shaving_config import PeakShavingConfig
    from .spatiotemporal_game import SpatiotemporalGameSpec


@dataclass(frozen=True)
class IntermediarySearchSpec:
    """Deterministic multistart search over retail shape and routing response."""

    retail_base_bounds: tuple[float, float] | None = None
    retail_slope_bounds: tuple[float, float] = (-1.0, 1.0)
    route_beta_bounds: tuple[float, float] = (0.0, 1_000_000.0)
    coarse_base_seeds: tuple[float, ...] = (0.7, 1.1, 1.6)
    coarse_slope_seeds: tuple[float, ...] = (-0.6, 0.0, 0.3, 0.6)
    route_region_seeds: tuple[float, ...] = (0.0, 4.0, 256.0)
    max_iterations: int = 250
    absolute_tie_tolerance: float = 1e-8
    relative_tie_tolerance: float = 1e-10

    def resolved_base_bounds(
        self, config: PeakShavingConfig
    ) -> tuple[float, float]:
        return self.retail_base_bounds or (
            float(config.price_lower),
            float(config.price_upper),
        )

    def validate(self, config: PeakShavingConfig) -> None:
        bounds = (
            self.resolved_base_bounds(config),
            self.retail_slope_bounds,
            self.route_beta_bounds,
        )
        if any(lower > upper for lower, upper in bounds):
            raise ValueError("intermediary search bounds must be ordered")
        if self.route_beta_bounds[0] < 0.0:
            raise ValueError("route beta must be nonnegative")
        if not self.coarse_base_seeds or not self.coarse_slope_seeds:
            raise ValueError("coarse retail seeds must not be empty")
        if len(self.route_region_seeds) != 3:
            raise ValueError("three route-region seeds are required")
        if self.max_iterations < 1:
            raise ValueError("max_iterations must be positive")

    def to_dict(self, config: PeakShavingConfig) -> dict:
        output = asdict(self)
        output["retail_base_bounds"] = list(self.resolved_base_bounds(config))
        return output


def _clip(value: float, bounds: tuple[float, float]) -> float:
    return float(np.clip(value, bounds[0], bounds[1]))


def _route_region_names() -> list[str]:
    return ["low", "intermediate", "near_deterministic"]


def optimize_intermediary_response_spatiotemporal(
    wholesale: np.ndarray,
    direct: np.ndarray,
    game: SpatiotemporalGameSpec,
    config: PeakShavingConfig,
    spec: IntermediarySearchSpec | None = None,
) -> tuple[object, dict]:
    """Numerically optimize the intermediary response with deterministic starts."""
    from .spatiotemporal_game import solve_spatiotemporal_joint_market

    search = spec or IntermediarySearchSpec()
    search.validate(config)
    base_bounds = search.resolved_base_bounds(config)
    slope_bounds = search.retail_slope_bounds
    beta_bounds = search.route_beta_bounds
    transformed_bounds = [
        base_bounds,
        slope_bounds,
        (float(np.log1p(beta_bounds[0])), float(np.log1p(beta_bounds[1]))),
    ]
    evaluations = 0
    records: list[dict] = []

    def evaluate(vector: np.ndarray) -> dict:
        nonlocal evaluations
        evaluations += 1
        base = _clip(float(vector[0]), base_bounds)
        slope = _clip(float(vector[1]), slope_bounds)
        beta = _clip(float(np.expm1(vector[2])), beta_bounds)
        retail = expand_price(
            base, slope, config, config.price_lower, config.price_upper
        )
        state, result = solve_spatiotemporal_joint_market(
            retail, wholesale, direct, beta, game, config
        )
        profit = (
            intermediary_profit(state, result, config)
            if result["joint_converged"]
            else -np.inf
        )
        return {
            "state": state,
            "result": result,
            "profit": float(profit),
            "vector": np.array([base, slope, np.log1p(beta)]),
            "candidate": {
                "retail_base": base,
                "retail_slope": slope,
                "route_beta": beta,
            },
        }

    def objective(vector: np.ndarray) -> float:
        record = evaluate(vector)
        records.append(record)
        return -record["profit"] if np.isfinite(record["profit"]) else 1e12

    local_runs = []
    coarse_count = 0
    for region, beta_seed in zip(_route_region_names(), search.route_region_seeds):
        region_records = []
        beta = _clip(beta_seed, beta_bounds)
        for base_seed in search.coarse_base_seeds:
            for slope_seed in search.coarse_slope_seeds:
                vector = np.array([
                    _clip(base_seed, base_bounds),
                    _clip(slope_seed, slope_bounds),
                    np.log1p(beta),
                ])
                record = evaluate(vector)
                records.append(record)
                region_records.append(record)
                coarse_count += 1
        start = max(region_records, key=lambda item: item["profit"])["vector"]
        optimized = minimize(
            objective,
            start,
            method="L-BFGS-B",
            bounds=transformed_bounds,
            options={
                "maxiter": search.max_iterations,
                "ftol": 1e-10,
                "gtol": 1e-8,
                "maxls": 30,
            },
        )
        final_record = evaluate(np.asarray(optimized.x, dtype=float))
        records.append(final_record)
        local_runs.append({
            "region": region,
            "success": bool(optimized.success),
            "status": int(optimized.status),
            "iterations": int(optimized.nit),
            "reported_function_evaluations": int(optimized.nfev),
            "profit": final_record["profit"],
        })

    converged = [
        record for record in records
        if np.isfinite(record["profit"]) and record["result"]["joint_converged"]
    ]
    if not converged:
        raise RuntimeError("no intermediary candidate reached the joint tolerance")
    best_profit = max(record["profit"] for record in converged)
    tie_tolerance = max(
        search.absolute_tie_tolerance,
        search.relative_tie_tolerance * max(abs(best_profit), 1.0),
    )
    near_best = [
        record for record in converged
        if best_profit - record["profit"] <= tie_tolerance
    ]
    selected = min(
        near_best,
        key=lambda item: (
            item["candidate"]["route_beta"],
            -item["profit"],
            abs(item["candidate"]["retail_slope"]),
        ),
    )
    candidate = selected["candidate"]
    result = selected["result"]
    routing = np.asarray(selected["state"].routing)
    result["intermediary_candidate"] = candidate
    result["intermediary_search"] = {
        "method": "deterministic_multistart_lbfgsb",
        "specification": search.to_dict(config),
        "searched_route_regions": _route_region_names(),
        "coarse_seed_count": coarse_count,
        "local_runs": local_runs,
        "successful_local_runs": sum(run["success"] for run in local_runs),
        "function_evaluations": evaluations,
        "best_profit": best_profit,
        "selected_profit": selected["profit"],
        "profit_tie_tolerance": tie_tolerance,
        "selected_at_retail_base_bound": bool(
            np.isclose(candidate["retail_base"], base_bounds).any()
        ),
        "selected_at_retail_slope_bound": bool(
            np.isclose(candidate["retail_slope"], slope_bounds).any()
        ),
        "selected_at_route_beta_bound": bool(
            np.isclose(candidate["route_beta"], beta_bounds).any()
        ),
        "routing_near_deterministic": bool(
            np.any(np.max(routing, axis=0) >= 1.0 - 1e-6)
        ),
    }
    return selected["state"], result
