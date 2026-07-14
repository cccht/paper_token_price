"""Re-solve uniform and dynamic finite games with conserved BurstGPT demand."""
from __future__ import annotations

from dataclasses import replace
import json
import os
from pathlib import Path

import numpy as np

from experiments.equilibrium_run_support import (
    comparison,
    configure_pair_cache,
    evaluation_cache_sources,
    make_evaluator,
    mapped_support,
)
from experiments.final_equilibrium_tools import solve_candidate_game
from experiments.final_reproducibility import equilibrium_metadata
from experiments.peak_shaving_submission_tools import (
    third_audit_enriched_provider_candidate_grid,
)
from experiments.run_spatiotemporal_mechanism_decomposition import (
    FIXED_CHANNEL_SHARES,
    load_burstgpt_profile,
)
from pricing_sim.peak_shaving_config import PeakShavingConfig
from pricing_sim.intermediary_response import IntermediarySearchSpec
from pricing_sim.spatiotemporal_game import SpatiotemporalGameSpec
from pricing_sim.spatiotemporal_mechanism import DemandResponseSpec

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "artifacts" / "peak_shaving" / "20260712_final"
QOS_CALIBRATION = OUT / "qos_calibration.json"
TOTAL_DEMAND = 1100.0
CAPACITY = np.array([180.0, 72.0])
MAX_PARALLEL_WORKERS = 16
DEFAULT_PAIR_CACHE_DIR = Path("/tmp/peak_shaving_audit_enriched_equilibrium")


def _qos_calibration() -> dict[str, float]:
    if not QOS_CALIBRATION.exists():
        from experiments.build_final_qos_calibration import (
            build_calibration,
            write_calibration,
        )

        write_calibration(build_calibration())
    artifact = json.loads(QOS_CALIBRATION.read_text(encoding="utf-8"))
    fit = artifact["pooled_fit"]
    return {"threshold": float(fit["threshold"]), "strength": float(fit["strength"])}


def final_case(
    *,
    capacity_scale: float = 1.0,
    price_sensitivity_scale: float = 1.0,
    migration_cost_scale: float = 1.0,
    qos_threshold_shift: float = 0.0,
) -> tuple[PeakShavingConfig, SpatiotemporalGameSpec, dict]:
    if min(capacity_scale, price_sensitivity_scale, migration_cost_scale) <= 0.0:
        raise ValueError("sensitivity scales must be positive")
    native_profile, load_shape = load_burstgpt_profile()
    calibration = _qos_calibration()
    config = PeakShavingConfig.default().evolve(
        firm_capacity=CAPACITY * capacity_scale,
        pop_rigid=0.4,
        pop_elastic=0.6,
        load_shape_hat=load_shape,
        qos_threshold=calibration["threshold"] + qos_threshold_shift,
        qos_strength=calibration["strength"],
    )
    native = TOTAL_DEMAND * np.array([0.4, 0.6])[:, None] * native_profile
    demand = DemandResponseSpec(
        native_demand=native,
        price_sensitivity=np.array([2.0, 5.0]) * price_sensitivity_scale,
        flexible_fraction=np.array([0.0, 0.8]),
        migration_cost=np.array([2.0, 0.35]) * migration_cost_scale,
        max_shift=np.array([0, 2]),
        channel_brand=np.array([1.05, 1.0, 1.0]),
        qos_weight=1.0,
    )
    game = SpatiotemporalGameSpec(
        demand=demand,
        fixed_channel_shares=FIXED_CHANNEL_SHARES,
        temporal_enabled=True,
        spatial_enabled=True,
        qos_shape="threshold",
    )
    return config, game, calibration


def run_equilibria(
    *,
    candidate_grid: np.ndarray | None = None,
    max_oracle_rounds: int = 12,
    retail_base_grid: np.ndarray | None = None,
    dynamic_retail_slope_grid: np.ndarray | None = None,
    route_beta_grid: np.ndarray | None = None,
    intermediary_search_spec: IntermediarySearchSpec | None = None,
    parallel_workers: int | None = None,
    capacity_scale: float = 1.0,
    price_sensitivity_scale: float = 1.0,
    migration_cost_scale: float = 1.0,
    qos_threshold_shift: float = 0.0,
    initial_dynamic_vectors: tuple[list[list[float]], list[list[float]]] | None = None,
    pair_cache_dir: Path | None = None,
) -> dict:
    scenario = {
        "capacity_scale": capacity_scale,
        "price_sensitivity_scale": price_sensitivity_scale,
        "migration_cost_scale": migration_cost_scale,
        "qos_threshold_shift": qos_threshold_shift,
    }
    config, game, calibration = final_case(**scenario)
    grid = (
        third_audit_enriched_provider_candidate_grid()
        if candidate_grid is None else np.asarray(candidate_grid)
    )
    uniform_mask = np.isclose(grid[:, 1], 0.0) & np.isclose(grid[:, 3], 0.0)
    uniform_grid = grid[uniform_mask]
    if not len(uniform_grid):
        raise ValueError("candidate grid must include at least one uniform strategy")
    grid_response_requested = any(
        value is not None
        for value in (
            retail_base_grid,
            dynamic_retail_slope_grid,
            route_beta_grid,
        )
    )
    if grid_response_requested and intermediary_search_spec is not None:
        raise ValueError("choose either grid or continuous intermediary response")
    workers = (
        int(parallel_workers)
        if parallel_workers is not None
        else (1 if grid_response_requested else min(MAX_PARALLEL_WORKERS, os.cpu_count() or 1))
    )
    if workers < 1:
        raise ValueError("parallel_workers must be positive")
    if grid_response_requested:
        bases = np.asarray(
            [0.8, 1.1, 1.5] if retail_base_grid is None else retail_base_grid
        )
        dynamic_slopes = np.asarray(
            [-0.3, 0.0, 0.3]
            if dynamic_retail_slope_grid is None else dynamic_retail_slope_grid
        )
        betas = np.asarray(
            [1.5, 4.0] if route_beta_grid is None else route_beta_grid
        )
        uniform_evaluator = make_evaluator(
            uniform_grid, game, config, bases, np.array([0.0]), betas,
            parallel_workers=workers,
        )
        dynamic_evaluator = make_evaluator(
            grid, game, config, bases, dynamic_slopes, betas,
            parallel_workers=workers,
        )
        response_manifest = {
            "method": "finite_grid",
            "retail_base_grid": bases.tolist(),
            "dynamic_retail_slope_grid": dynamic_slopes.tolist(),
            "route_beta_grid": betas.tolist(),
            "parallel_workers": workers,
        }
    else:
        dynamic_search = intermediary_search_spec or IntermediarySearchSpec()
        uniform_search = replace(dynamic_search, retail_slope_bounds=(0.0, 0.0))
        uniform_evaluator = make_evaluator(
            uniform_grid, game, config, search_spec=uniform_search,
            parallel_workers=workers,
        )
        dynamic_evaluator = make_evaluator(
            grid, game, config, search_spec=dynamic_search,
            parallel_workers=workers,
        )
        response_manifest = {
            "method": "continuous_multistart",
            "uniform": uniform_search.to_dict(config),
            "dynamic": dynamic_search.to_dict(config),
            "parallel_workers": workers,
        }
    cache_sources = evaluation_cache_sources(ROOT, QOS_CALIBRATION)
    cache_response_manifest = {
        key: value
        for key, value in response_manifest.items()
        if key != "parallel_workers"
    }
    cache_manifest = {}
    for name, evaluator in (("uniform", uniform_evaluator), ("dynamic", dynamic_evaluator)):
        cache_manifest[name] = configure_pair_cache(
            evaluator,
            pair_cache_dir,
            name,
            {"scenario": scenario, "response": cache_response_manifest, "game": name},
            cache_sources,
        )
    uniform = solve_candidate_game(
        uniform_evaluator,
        max_oracle_rounds=max_oracle_rounds,
    )
    initial_vectors = initial_dynamic_vectors or (
        uniform["row_support_vectors"], uniform["col_support_vectors"]
    )
    initial_rows = mapped_support(initial_vectors[0], grid)
    initial_cols = mapped_support(initial_vectors[1], grid)
    dynamic = solve_candidate_game(
        dynamic_evaluator,
        row_support=initial_rows,
        col_support=initial_cols,
        max_oracle_rounds=max_oracle_rounds,
    )
    cache_manifest["uniform"]["stored_pairs"] = len(uniform_evaluator.cache)
    cache_manifest["dynamic"]["stored_pairs"] = len(dynamic_evaluator.cache)
    metadata = equilibrium_metadata(
            ROOT,
            QOS_CALIBRATION,
            Path(__file__).resolve(),
            len(grid),
            response_manifest["method"],
        )
    metadata["pair_cache"] = cache_manifest
    return {
        "metadata": metadata,
        "scenario": scenario,
        "model_config": {
            "capacity": config.firm_capacity.tolist(),
            "period_hours": config.period_hours,
            "qos_shape": game.qos_shape,
            "fixed_channel_shares": FIXED_CHANNEL_SHARES.tolist(),
        },
        "qos_calibration": calibration,
        "demand_spec": {
            "native_demand": game.demand.native_demand.tolist(),
            "price_sensitivity": game.demand.price_sensitivity.tolist(),
            "flexible_fraction": game.demand.flexible_fraction.tolist(),
            "migration_cost": game.demand.migration_cost.tolist(),
            "max_shift": game.demand.max_shift.tolist(),
        },
        "candidate_grid": grid.tolist(),
        "provider_strategy_grid": {
            "candidate_count": len(grid),
            "structure": "base grid, high-slope guards, and three audited local refinement layers",
            "wholesale_base": np.unique(grid[:, 0]).tolist(),
            "wholesale_slope": np.unique(grid[:, 1]).tolist(),
            "direct_base": np.unique(grid[:, 2]).tolist(),
            "direct_slope": np.unique(grid[:, 3]).tolist(),
        },
        "intermediary_response": response_manifest,
        "uniform": uniform,
        "dynamic": dynamic,
        "comparison": comparison(uniform, dynamic),
        "claim_boundary": (
            "Finite provider candidate game with a numerically optimized "
            "intermediary response; BurstGPT calibrates load shape only. "
            "Behavioral parameters and capacities remain synthetic."
        ),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    result = run_equilibria(pair_cache_dir=DEFAULT_PAIR_CACHE_DIR)
    path = OUT / "spatiotemporal_equilibrium.json"
    path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({
        "output": str(path.relative_to(ROOT)),
        "uniform_regret": result["uniform"]["full_max_regret"],
        "dynamic_regret": result["dynamic"]["full_max_regret"],
    }, indent=2))


if __name__ == "__main__":
    main()
