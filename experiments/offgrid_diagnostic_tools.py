from __future__ import annotations

from collections import Counter
from dataclasses import fields
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import pickle

import numpy as np
from scipy.stats import qmc

from experiments.final_equilibrium_tools import PairEvaluator
from pricing_sim.intermediary_response import IntermediarySearchSpec

SLOPE_BOUNDS = (-4.0, 4.0)
CANDIDATE_BATCH_SIZE = 64


def _active_support(game: dict, player: str) -> tuple[np.ndarray, np.ndarray]:
    prefix = "row" if player == "firm_A" else "col"
    vectors = np.asarray(game[f"{prefix}_support_vectors"], dtype=float)
    mix = np.asarray(game[f"{prefix}_mix"], dtype=float)
    active = mix > 1e-10
    weights = mix[active]
    return vectors[active], weights / np.sum(weights)


def _search_domain(config) -> dict[str, list[float]]:
    return {
        "wholesale_base": [float(config.wholesale_lower), float(config.wholesale_upper)],
        "wholesale_slope": list(SLOPE_BOUNDS),
        "direct_base": [float(config.price_lower), float(config.price_upper)],
        "direct_slope": list(SLOPE_BOUNDS),
    }


def _latin_hypercube(samples: int, seed: int, domain: dict) -> np.ndarray:
    unit = qmc.LatinHypercube(d=4, seed=seed).random(samples)
    bounds = np.asarray(list(domain.values()), dtype=float)
    return qmc.scale(unit, bounds[:, 0], bounds[:, 1])


def _axis_guards(support: np.ndarray, domain: dict) -> np.ndarray:
    bounds = np.asarray(list(domain.values()), dtype=float)
    guards = []
    for vector in support:
        for dimension in range(4):
            for bound in bounds[dimension]:
                candidate = vector.copy()
                candidate[dimension] = bound
                guards.append(candidate)
    return np.asarray(guards, dtype=float)


def _local_guards(support: np.ndarray, domain: dict) -> np.ndarray:
    bounds = np.asarray(list(domain.values()), dtype=float)
    guards = []
    for vector in support:
        for dimension in range(4):
            span = bounds[dimension, 1] - bounds[dimension, 0]
            for fraction in (-0.15, -0.05, 0.05, 0.15):
                candidate = vector.copy()
                candidate[dimension] = np.clip(
                    candidate[dimension] + fraction * span, *bounds[dimension]
                )
                guards.append(candidate)
    return np.asarray(guards, dtype=float)


def _candidate_design(
    support: np.ndarray, domain: dict, *, samples: int, seed: int
) -> tuple[np.ndarray, list[str]]:
    groups = (
        (support, "active_support"),
        (_latin_hypercube(samples, seed, domain), "latin_hypercube"),
        (_axis_guards(support, domain), "axis_guard"),
        (_local_guards(support, domain), "local_guard"),
    )
    vectors, sources, seen = [], [], set()
    for group, source in groups:
        for vector in group:
            key = tuple(np.round(vector, 12))
            if key in seen:
                continue
            seen.add(key)
            vectors.append(np.asarray(vector, dtype=float))
            sources.append(source)
    return np.vstack(vectors), sources


def _pairwise_refinement(center: np.ndarray, domain: dict) -> np.ndarray:
    bounds = np.asarray(list(domain.values()), dtype=float)
    spans = bounds[:, 1] - bounds[:, 0]
    fractions = (-0.05, -0.025, -0.0125, 0.0, 0.0125, 0.025, 0.05)
    vectors, seen = [], set()
    for first, second in combinations(range(4), 2):
        for left, right in product(fractions, repeat=2):
            candidate = np.asarray(center, dtype=float).copy()
            candidate[first] += left * spans[first]
            candidate[second] += right * spans[second]
            candidate = np.clip(candidate, bounds[:, 0], bounds[:, 1])
            key = tuple(np.round(candidate, 12))
            if key in seen:
                continue
            seen.add(key)
            vectors.append(candidate)
    return np.vstack(vectors)


def _intermediary_spec(manifest: dict) -> IntermediarySearchSpec:
    if manifest.get("method") != "continuous_multistart":
        raise ValueError("off-grid audit requires a continuous intermediary response")
    raw = manifest["dynamic"]
    allowed = {item.name for item in fields(IntermediarySearchSpec)}
    values = {key: raw[key] for key in allowed if key in raw}
    tuple_fields = {key for key in values if key.endswith(("bounds", "seeds"))}
    values.update({key: tuple(values[key]) for key in tuple_fields})
    return IntermediarySearchSpec(**values)


def _cache_signature(
    equilibrium_hash: str, player: str, grid: np.ndarray, spec: IntermediarySearchSpec
) -> str:
    digest = hashlib.sha256()
    digest.update(equilibrium_hash.encode())
    digest.update(player.encode())
    digest.update(np.ascontiguousarray(grid).tobytes())
    digest.update(json.dumps(spec.__dict__, sort_keys=True).encode())
    return digest.hexdigest()


def _load_cache(path: Path | None, signature: str) -> dict:
    if path is None or not path.exists():
        return {}
    with path.open("rb") as stream:
        payload = pickle.load(stream)
    return payload["records"] if payload.get("signature") == signature else {}


def _save_cache(path: Path | None, signature: str, records: dict) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("wb") as stream:
        pickle.dump(
            {"signature": signature, "records": records},
            stream,
            protocol=pickle.HIGHEST_PROTOCOL,
        )
    temporary.replace(path)


def _candidate_records(
    player: str,
    candidates: np.ndarray,
    sources: list[str],
    opponent_mix: np.ndarray,
    evaluator: PairEvaluator,
    signature: str,
    cache_path: Path | None,
    phase: str,
) -> list[dict]:
    candidate_count = len(candidates)
    opponent_indices = range(candidate_count, len(evaluator.grid))
    payoff_key = "firm_A_profit" if player == "firm_A" else "firm_B_profit"
    records = []
    for start in range(0, candidate_count, CANDIDATE_BATCH_SIZE):
        indices = range(start, min(start + CANDIDATE_BATCH_SIZE, candidate_count))
        pairs = [
            ((candidate, opponent) if player == "firm_A" else (opponent, candidate))
            for candidate in indices for opponent in opponent_indices
        ]
        had_missing = any(pair not in evaluator.cache for pair in pairs)
        evaluator.evaluate_many(pairs)
        if had_missing:
            _save_cache(cache_path, signature, evaluator.cache)
        print(
            f"{player}/{phase}: evaluated "
            f"{min(start + CANDIDATE_BATCH_SIZE, candidate_count)}/"
            f"{candidate_count} candidates ({len(evaluator.cache)} pairs)",
            flush=True,
        )
    for candidate, (vector, source) in enumerate(zip(candidates, sources)):
        pairs = [
            evaluator.evaluate(candidate, opponent) if player == "firm_A"
            else evaluator.evaluate(opponent, candidate)
            for opponent in opponent_indices
        ]
        payoff = sum(weight * item[payoff_key] for weight, item in zip(opponent_mix, pairs))
        searches = [item["result"]["intermediary_search"] for item in pairs]
        records.append({
            "vector": vector.tolist(), "source": source, "payoff": float(payoff),
            "maximum_joint_residual": max(item["joint_residual"] for item in pairs),
            "all_joint_converged": all(item["joint_converged"] for item in pairs),
            "minimum_successful_local_runs": min(item["successful_local_runs"] for item in searches),
            "maximum_route_beta": max(item["result"]["intermediary_candidate"]["route_beta"] for item in pairs),
        })
    return records


def _summarize_player(player: str, game: dict, records: list[dict], cache_size: int) -> dict:
    records.sort(key=lambda item: item["payoff"], reverse=True)
    payoff_key = "firm_A_profit" if player == "firm_A" else "firm_B_profit"
    equilibrium_payoff = float(game["expected_metrics"][payoff_key])
    best = records[0]
    regret = max(best["payoff"] - equilibrium_payoff, 0.0)
    active_errors = [
        abs(item["payoff"] - equilibrium_payoff)
        for item in records if item["source"] == "active_support"
    ]
    return {
        "equilibrium_payoff": equilibrium_payoff,
        "best_payoff": best["payoff"],
        "best_vector": best["vector"],
        "best_source": best["source"],
        "offgrid_regret": regret,
        "relative_offgrid_regret": regret / max(abs(equilibrium_payoff), 1.0),
        "evaluated_candidates": len(records),
        "evaluated_pairs": cache_size,
        "candidate_sources": dict(Counter(item["source"] for item in records)),
        "maximum_active_support_payoff_error": max(active_errors, default=0.0),
        "all_joint_converged": all(item["all_joint_converged"] for item in records),
        "minimum_successful_local_runs": min(item["minimum_successful_local_runs"] for item in records),
        "maximum_joint_residual": max(item["maximum_joint_residual"] for item in records),
        "maximum_route_beta": max(item["maximum_route_beta"] for item in records),
        "top_candidates": records[:10],
    }


def _search_player(
    player: str, game: dict, samples: int, seed: int, *, config, game_spec, domain: dict,
    intermediary_search_spec: IntermediarySearchSpec, parallel_workers: int,
    cache_path: Path | None, equilibrium_hash: str,
) -> dict:
    own_vectors, _ = _active_support(game, player)
    opponent = "firm_B" if player == "firm_A" else "firm_A"
    opponent_vectors, opponent_mix = _active_support(game, opponent)
    candidates, sources = _candidate_design(own_vectors, domain, samples=samples, seed=seed)
    grid = np.vstack([candidates, opponent_vectors])
    signature = _cache_signature(equilibrium_hash, player, grid, intermediary_search_spec)
    evaluator = PairEvaluator(
        grid=grid, game=game_spec, config=config,
        intermediary_search_spec=intermediary_search_spec,
        parallel_workers=parallel_workers,
        cache=_load_cache(cache_path, signature),
    )
    records = _candidate_records(
        player, candidates, sources, opponent_mix, evaluator, signature, cache_path,
        "global_guard",
    )
    center = np.asarray(max(records, key=lambda item: item["payoff"])["vector"])
    refinement = _pairwise_refinement(center, domain)
    known = {tuple(np.round(vector, 12)) for vector in candidates}
    refinement = np.asarray([
        vector for vector in refinement if tuple(np.round(vector, 12)) not in known
    ])
    cache_size = len(evaluator.cache)
    if len(refinement):
        refine_grid = np.vstack([refinement, opponent_vectors])
        refine_signature = _cache_signature(
            equilibrium_hash, player, refine_grid, intermediary_search_spec
        )
        refine_path = (
            None if cache_path is None else
            cache_path.with_name(f"{cache_path.stem}_refinement{cache_path.suffix}")
        )
        refine_evaluator = PairEvaluator(
            grid=refine_grid, game=game_spec, config=config,
            intermediary_search_spec=intermediary_search_spec,
            parallel_workers=parallel_workers,
            cache=_load_cache(refine_path, refine_signature),
        )
        records.extend(_candidate_records(
            player, refinement, ["pairwise_refinement"] * len(refinement),
            opponent_mix, refine_evaluator, refine_signature, refine_path,
            "pairwise_refinement",
        ))
        cache_size += len(refine_evaluator.cache)
    return _summarize_player(player, game, records, cache_size)
