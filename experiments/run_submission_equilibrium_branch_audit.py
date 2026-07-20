"""Audit mixed-equilibrium branch sensitivity on the frozen baseline payoff cache."""
from __future__ import annotations
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path

for _thread_variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_thread_variable] = "1"

import numpy as np  # noqa: E402

from experiments.equilibrium_cache import load_vector_pair_cache  # noqa: E402
from pricing_sim.complementarity_solver import complementarity_candidate  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "peak_shaving" / "20260712_expanded_response"
BASELINE_PATH = OUT / "spatiotemporal_equilibrium_submission.json"
CACHE_PATH = (
    Path.home() / ".cache" / "peak_shaving_uniform_expansion_baseline" / "dynamic.pkl"
)
OUTPUT_PATH = OUT / "equilibrium_branch_audit_submission.json"
MAIN_METRICS = (
    "aggregate_peak_load", "maximum_provider_utilization",
    "minimum_provider_qos", "system_profit",
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def restricted_game_regret(
    payoff_row: np.ndarray,
    payoff_col: np.ndarray,
    row_mix: np.ndarray,
    col_mix: np.ndarray,
) -> dict[str, float]:
    row_values = np.asarray(payoff_row) @ np.asarray(col_mix)
    col_values = np.asarray(row_mix) @ np.asarray(payoff_col)
    row_current = float(np.asarray(row_mix) @ row_values)
    col_current = float(col_values @ np.asarray(col_mix))
    row_regret = max(float(np.max(row_values)) - row_current, 0.0)
    col_regret = max(float(np.max(col_values)) - col_current, 0.0)
    return {
        "row_expected_payoff": row_current,
        "col_expected_payoff": col_current,
        "row_regret": row_regret,
        "col_regret": col_regret,
        "max_regret": max(row_regret, col_regret),
    }


def full_candidate_regret(
    restricted_row: np.ndarray,
    restricted_col: np.ndarray,
    row_full: np.ndarray,
    col_full: np.ndarray,
    row_mix: np.ndarray,
    col_mix: np.ndarray,
) -> dict[str, float]:
    result = restricted_game_regret(
        restricted_row, restricted_col, row_mix, col_mix
    )
    row_values = np.asarray(row_full) @ np.asarray(col_mix)
    col_values = np.asarray(row_mix) @ np.asarray(col_full)
    row_regret = max(float(np.max(row_values)) - result["row_expected_payoff"], 0.0)
    col_regret = max(float(np.max(col_values)) - result["col_expected_payoff"], 0.0)
    scale = max(
        abs(result["row_expected_payoff"]),
        abs(result["col_expected_payoff"]),
        1.0,
    )
    return {
        **result,
        "row_regret": row_regret,
        "col_regret": col_regret,
        "max_regret": max(row_regret, col_regret),
        "relative_max_regret": max(row_regret, col_regret) / scale,
    }


def _mix_distance(first: dict, second: dict) -> float:
    row_distance = np.max(np.abs(
        np.asarray(first["row_mix"]) - np.asarray(second["row_mix"])
    ))
    col_distance = np.max(np.abs(
        np.asarray(first["col_mix"]) - np.asarray(second["col_mix"])
    ))
    return float(max(row_distance, col_distance))


def cluster_mixed_candidates(
    candidates: list[dict], *, tolerance: float = 1e-6
) -> list[dict]:
    clusters: list[dict] = []
    for candidate in candidates:
        match = next(
            (item for item in clusters if _mix_distance(candidate, item) <= tolerance),
            None,
        )
        if match is None:
            clusters.append({
                **candidate,
                "sources": [candidate["source"]],
                "source_count": 1,
            })
        else:
            match["sources"].append(candidate["source"])
            match["source_count"] += 1
    return clusters


def weighted_outcome_metrics(
    records: dict,
    row_indices: list[int],
    col_indices: list[int],
    row_mix: np.ndarray,
    col_mix: np.ndarray,
    metric_names: tuple[str, ...] = MAIN_METRICS,
) -> dict[str, float]:
    output = {name: 0.0 for name in metric_names}
    for i, row_index in enumerate(row_indices):
        for j, col_index in enumerate(col_indices):
            weight = float(row_mix[i] * col_mix[j])
            if weight <= 0.0:
                continue
            record = records[(row_index, col_index)]
            for name in metric_names:
                output[name] += weight * float(record[name])
    return output


def _load_cache(baseline: dict, cache_path: Path) -> dict:
    grid = np.asarray(baseline["candidate_grid"], dtype=float)
    signature = baseline["metadata"]["pair_cache"]["dynamic"]["signature"]
    records = load_vector_pair_cache(cache_path, signature, grid)
    expected = baseline["dynamic"]["evaluated_pairs"]
    if len(records) != expected:
        raise ValueError(f"loaded {len(records)} cached pairs; expected {expected}")
    return records


def _payoff_arrays(
    records: dict, row_indices: list[int], col_indices: list[int], candidate_count: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    restricted_row = np.empty((len(row_indices), len(col_indices)))
    restricted_col = np.empty_like(restricted_row)
    row_full = np.empty((candidate_count, len(col_indices)))
    col_full = np.empty((len(row_indices), candidate_count))
    for i, row_index in enumerate(row_indices):
        for j, col_index in enumerate(col_indices):
            record = records[(row_index, col_index)]
            restricted_row[i, j] = record["firm_A_profit"]
            restricted_col[i, j] = record["firm_B_profit"]
    for candidate in range(candidate_count):
        for j, col_index in enumerate(col_indices):
            row_full[candidate, j] = records[(candidate, col_index)]["firm_A_profit"]
        for i, row_index in enumerate(row_indices):
            col_full[i, candidate] = records[(row_index, candidate)]["firm_B_profit"]
    return restricted_row, restricted_col, row_full, col_full


def _initial_mixes(game: dict, random_starts: int, seed: int) -> list[tuple[str, tuple]]:
    row_size = len(game["row_support_indices"])
    col_size = len(game["col_support_indices"])
    rng = np.random.default_rng(seed)
    starts = [
        ("reported", (np.asarray(game["row_mix"]), np.asarray(game["col_mix"]))),
        ("uniform", (np.full(row_size, 1 / row_size), np.full(col_size, 1 / col_size))),
    ]
    for index in range(random_starts):
        starts.append((
            f"dirichlet_{index:03d}",
            (rng.dirichlet(np.ones(row_size)), rng.dirichlet(np.ones(col_size))),
        ))
    return starts


def _solve_from_starts(
    payoff_row: np.ndarray,
    payoff_col: np.ndarray,
    starts: list[tuple[str, tuple]],
) -> tuple[list[dict], list[str]]:
    candidates, failures = [], []
    for source, initial in starts:
        pair = complementarity_candidate(payoff_row, payoff_col, initial)
        if pair is None:
            failures.append(source)
            continue
        check = restricted_game_regret(payoff_row, payoff_col, pair[0], pair[1])
        if check["max_regret"] > 1e-6:
            failures.append(source)
            continue
        candidates.append({
            "source": source,
            "row_mix": pair[0].tolist(),
            "col_mix": pair[1].tolist(),
            "restricted_regret": check["max_regret"],
        })
    return candidates, failures


def _assess_branches(
    clusters: list[dict], arrays: tuple, records: dict, rows: list[int], cols: list[int]
) -> list[dict]:
    restricted_row, restricted_col, row_full, col_full = arrays
    output = []
    for index, cluster in enumerate(clusters):
        row_mix = np.asarray(cluster["row_mix"])
        col_mix = np.asarray(cluster["col_mix"])
        output.append({
            **cluster,
            "branch_index": index,
            "row_support_count": int(np.sum(row_mix > 1e-10)),
            "col_support_count": int(np.sum(col_mix > 1e-10)),
            "full_candidate": full_candidate_regret(
                restricted_row, restricted_col, row_full, col_full, row_mix, col_mix
            ),
            "expected_metrics": weighted_outcome_metrics(
                records, rows, cols, row_mix, col_mix
            ),
        })
    return output


def _metric_spans(branches: list[dict]) -> dict[str, dict[str, float]]:
    output = {}
    for metric in MAIN_METRICS:
        values = [branch["expected_metrics"][metric] for branch in branches]
        output[metric] = {"minimum": min(values), "maximum": max(values), "span": max(values) - min(values)}
    return output


def run_branch_audit(
    *,
    baseline_path: Path = BASELINE_PATH,
    cache_path: Path = CACHE_PATH,
    random_starts: int = 64,
    seed: int = 20260715,
) -> dict:
    if random_starts < 1:
        raise ValueError("random_starts must be positive")
    baseline_path, cache_path = Path(baseline_path), Path(cache_path)
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    game = baseline["dynamic"]
    records = _load_cache(baseline, cache_path)
    rows = [int(value) for value in game["row_support_indices"]]
    cols = [int(value) for value in game["col_support_indices"]]
    arrays = _payoff_arrays(records, rows, cols, len(baseline["candidate_grid"]))
    starts = _initial_mixes(game, random_starts, seed)
    candidates, failures = _solve_from_starts(arrays[0], arrays[1], starts)
    clusters = cluster_mixed_candidates(candidates)
    if not clusters:
        raise RuntimeError("no valid mixed equilibrium was recovered")
    branches = _assess_branches(clusters, arrays, records, rows, cols)
    return {
        "metadata": {
            "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "baseline_path": str(baseline_path.relative_to(ROOT)),
            "baseline_sha256": _sha256(baseline_path),
            "cache_path": str(cache_path),
            "cache_sha256": _sha256(cache_path),
            "cache_signature": baseline["metadata"]["pair_cache"]["dynamic"]["signature"],
            "source_sha256": {str(Path(__file__).relative_to(ROOT)): _sha256(Path(__file__))},
            "seed": seed,
            "random_starts": random_starts,
            "total_starts": len(starts),
            "successful_starts": len(candidates),
            "failed_starts": failures,
            "cluster_tolerance": 1e-6,
        },
        "restricted_shape": [len(rows), len(cols)],
        "candidate_count": len(baseline["candidate_grid"]),
        "branch_count": len(branches),
        "single_recovered_branch": len(branches) == 1,
        "branches": branches,
        "metric_spans": _metric_spans(branches),
        "claim_boundary": (
            "A multistart numerical branch audit on the frozen restricted payoff matrix; "
            "it does not enumerate or prove uniqueness of all bimatrix equilibria."
        ),
    }


def main() -> None:
    result = run_branch_audit()
    OUTPUT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
        "successful_starts": result["metadata"]["successful_starts"],
        "branch_count": result["branch_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
