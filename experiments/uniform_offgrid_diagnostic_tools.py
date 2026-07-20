"""Independent two-dimensional diagnostics for uniform provider policies."""
from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import numpy as np
from scipy.stats import qmc

from experiments.final_equilibrium_tools import PairEvaluator
from experiments.offgrid_diagnostic_tools import (
    _active_support,
    _cache_signature,
    _candidate_records,
    _load_cache,
    _summarize_player,
)
from pricing_sim.intermediary_response import IntermediarySearchSpec


BASE_PRICE_BOUNDS = np.array([[0.25, 0.90], [0.45, 2.10]])
SLOPE_INDICES = (1, 3)


def _validated_support(support: np.ndarray) -> np.ndarray:
    values = np.asarray(support, dtype=float)
    if values.ndim != 2 or values.shape[1] != 4:
        raise ValueError("active support must be a matrix of four-coefficient vectors")
    if not np.allclose(values[:, SLOPE_INDICES], 0.0, atol=1e-12):
        raise ValueError("uniform off-grid support must contain zero-slope vectors")
    return values


def _expand_base_points(points: np.ndarray) -> np.ndarray:
    points = np.asarray(points, dtype=float)
    zeros = np.zeros(len(points))
    return np.column_stack([points[:, 0], zeros, points[:, 1], zeros])


def _boundary_guards() -> np.ndarray:
    wholesale = (*BASE_PRICE_BOUNDS[0], np.mean(BASE_PRICE_BOUNDS[0]))
    direct = (*BASE_PRICE_BOUNDS[1], np.mean(BASE_PRICE_BOUNDS[1]))
    points = [
        (left, right)
        for left in wholesale
        for right in direct
        if left != wholesale[-1] or right != direct[-1]
    ]
    return _expand_base_points(np.asarray(points))


def uniform_candidate_design(
    support: np.ndarray,
    *,
    samples: int,
    seed: int,
) -> tuple[np.ndarray, list[str]]:
    """Combine active support, an independent LHS, and domain guards."""
    if samples < 1:
        raise ValueError("samples must be positive")
    active = _validated_support(support)
    unit = qmc.LatinHypercube(d=2, seed=seed).random(samples)
    lhs = _expand_base_points(
        qmc.scale(unit, BASE_PRICE_BOUNDS[:, 0], BASE_PRICE_BOUNDS[:, 1])
    )
    vectors = np.vstack([active, lhs, _boundary_guards()])
    sources = (
        ["active_support"] * len(active)
        + ["latin_hypercube"] * len(lhs)
        + ["boundary_guard"] * len(_boundary_guards())
    )
    return vectors, sources


def uniform_local_refinement(
    center: np.ndarray,
    *,
    points_per_axis: int,
    half_width_fraction: float,
) -> np.ndarray:
    """Return a bounded local lattice around one zero-slope candidate."""
    values = _validated_support(np.asarray(center, dtype=float).reshape(1, 4))[0]
    if points_per_axis < 3 or points_per_axis % 2 == 0:
        raise ValueError("points_per_axis must be an odd integer of at least three")
    if not 0.0 < half_width_fraction <= 0.5:
        raise ValueError("half_width_fraction must lie in (0, 0.5]")
    spans = BASE_PRICE_BOUNDS[:, 1] - BASE_PRICE_BOUNDS[:, 0]
    base = values[[0, 2]]
    axes = [
        np.clip(
            base[index]
            + np.linspace(-1.0, 1.0, points_per_axis)
            * half_width_fraction
            * spans[index],
            *BASE_PRICE_BOUNDS[index],
        )
        for index in range(2)
    ]
    points = np.asarray([(left, right) for left in axes[0] for right in axes[1]])
    return _expand_base_points(points)


def _evaluate_design(
    *,
    player: str,
    candidates: np.ndarray,
    sources: Sequence[str],
    opponent_vectors: np.ndarray,
    opponent_mix: np.ndarray,
    evaluator_args: dict,
    cache_path: Path,
    equilibrium_hash: str,
    phase: str,
) -> tuple[list[dict], int]:
    grid = np.vstack([candidates, opponent_vectors])
    spec = evaluator_args["intermediary_search_spec"]
    signature = _cache_signature(equilibrium_hash, player, grid, spec)
    evaluator = PairEvaluator(
        grid=grid,
        game=evaluator_args["game_spec"],
        config=evaluator_args["config"],
        intermediary_search_spec=spec,
        parallel_workers=evaluator_args["parallel_workers"],
        cache=_load_cache(cache_path, signature),
    )
    records = _candidate_records(
        player,
        candidates,
        list(sources),
        opponent_mix,
        evaluator,
        signature,
        cache_path,
        phase,
    )
    return records, len(evaluator.cache)


def search_uniform_player(
    player: str,
    game: dict,
    samples: int,
    seed: int,
    *,
    config,
    game_spec,
    intermediary_search_spec: IntermediarySearchSpec,
    parallel_workers: int,
    cache_path: Path,
    equilibrium_hash: str,
) -> dict:
    """Evaluate global guards and a 17-by-17 refinement for one provider."""
    own_vectors, _ = _active_support(game, player)
    opponent = "firm_B" if player == "firm_A" else "firm_A"
    opponent_vectors, opponent_mix = _active_support(game, opponent)
    candidates, sources = uniform_candidate_design(
        own_vectors, samples=samples, seed=seed
    )
    evaluator_args = {
        "config": config,
        "game_spec": game_spec,
        "intermediary_search_spec": intermediary_search_spec,
        "parallel_workers": parallel_workers,
    }
    records, pair_count = _evaluate_design(
        player=player,
        candidates=candidates,
        sources=sources,
        opponent_vectors=opponent_vectors,
        opponent_mix=opponent_mix,
        evaluator_args=evaluator_args,
        cache_path=cache_path,
        equilibrium_hash=equilibrium_hash,
        phase="global_guard",
    )
    center = np.asarray(max(records, key=lambda item: item["payoff"])["vector"])
    local = uniform_local_refinement(
        center, points_per_axis=17, half_width_fraction=0.025
    )
    local_records, local_pairs = _evaluate_design(
        player=player,
        candidates=local,
        sources=["local_refinement"] * len(local),
        opponent_vectors=opponent_vectors,
        opponent_mix=opponent_mix,
        evaluator_args=evaluator_args,
        cache_path=cache_path.with_name(f"{cache_path.stem}_local{cache_path.suffix}"),
        equilibrium_hash=equilibrium_hash,
        phase="local_refinement",
    )
    records.extend(local_records)
    return _summarize_player(player, game, records, pair_count + local_pairs)
