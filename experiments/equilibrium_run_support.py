from __future__ import annotations

from pathlib import Path

import numpy as np

from experiments.equilibrium_cache import (
    cache_signature,
    load_vector_pair_cache,
    write_vector_pair_cache,
)
from experiments.final_equilibrium_tools import PairEvaluator
from pricing_sim.intermediary_response import IntermediarySearchSpec
from pricing_sim.spatiotemporal_game import SpatiotemporalGameSpec


def mapped_support(vectors: list[list[float]], grid: np.ndarray) -> list[int]:
    indices = []
    for vector in vectors:
        distance = np.linalg.norm(grid - np.asarray(vector)[None, :], axis=1)
        indices.append(int(np.argmin(distance)))
    return sorted(set(indices))


def make_evaluator(
    grid: np.ndarray,
    game: SpatiotemporalGameSpec,
    config: object,
    bases: np.ndarray | None = None,
    slopes: np.ndarray | None = None,
    betas: np.ndarray | None = None,
    search_spec: IntermediarySearchSpec | None = None,
    parallel_workers: int = 1,
) -> PairEvaluator:
    return PairEvaluator(
        grid=grid,
        game=game,
        config=config,
        retail_base_grid=None if bases is None else np.asarray(bases, dtype=float),
        retail_slope_grid=None if slopes is None else np.asarray(slopes, dtype=float),
        route_beta_grid=None if betas is None else np.asarray(betas, dtype=float),
        intermediary_search_spec=search_spec,
        parallel_workers=parallel_workers,
    )


def comparison(uniform: dict, dynamic: dict) -> dict[str, float]:
    mapping = {
        "aggregate_peak_load": "aggregate_peak_load_change",
        "maximum_provider_utilization": "maximum_provider_utilization_change",
        "minimum_provider_qos": "minimum_provider_qos_change",
        "system_profit": "system_profit_change",
        "temporal_moved_fraction": "temporal_moved_fraction_change",
    }
    output = {}
    for metric, name in mapping.items():
        baseline = uniform["expected_metrics"][metric]
        value = dynamic["expected_metrics"][metric]
        output[name] = value - baseline
        output[f"{name}_percent"] = 100.0 * (value - baseline) / max(abs(baseline), 1e-12)
    return output


def evaluation_cache_sources(root: Path, qos_calibration: Path) -> tuple[Path, ...]:
    return (
        root / "pricing_sim/spatiotemporal_mechanism.py",
        root / "pricing_sim/spatiotemporal_game.py",
        root / "pricing_sim/intermediary_response.py",
        root / "pricing_sim/peak_shaving_market.py",
        root / "pricing_sim/peak_shaving_equilibrium.py",
        root / "pricing_sim/peak_shaving_config.py",
        qos_calibration,
        root / "data/processed/burstgpt_d895a53b_8period/burstgpt_8period_load_profile.csv",
    )


def configure_pair_cache(
    evaluator: PairEvaluator,
    cache_dir: Path | None,
    name: str,
    identity: dict,
    source_paths: tuple[Path, ...],
) -> dict:
    if cache_dir is None:
        return {"enabled": False, "loaded_pairs": 0, "stored_pairs": 0}
    path = Path(cache_dir) / f"{name}.pkl"
    signature = cache_signature(identity, source_paths)
    loaded = load_vector_pair_cache(path, signature, evaluator.grid)
    evaluator.cache.update(loaded)
    def checkpoint(records: dict) -> None:
        write_vector_pair_cache(path, signature, evaluator.grid, records)
        print(f"{name} cache checkpoint: {len(records)} pairs", flush=True)

    evaluator.checkpoint_callback = checkpoint
    return {
        "enabled": True,
        "file": path.name,
        "signature": signature,
        "loaded_pairs": len(loaded),
        "stored_pairs": len(loaded),
    }
