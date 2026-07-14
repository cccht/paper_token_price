from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field
from multiprocessing import get_context
from typing import Callable

import numpy as np

from pricing_sim.finite_game import (
    default_support,
    embed_mixed_candidate as _embed_mixed_candidate,
    enumerate_bimatrix_equilibria,
    serializable_selected,
    select_full_grid_equilibrium,
)
from pricing_sim.spatiotemporal_game import (
    SpatiotemporalGameSpec,
    evaluate_firm_pair_spatiotemporal,
)
from pricing_sim.intermediary_response import IntermediarySearchSpec

SCALAR_KEYS = (
    "firm_A_profit",
    "firm_B_profit",
    "intermediary_profit",
    "system_profit",
    "aggregate_peak_load",
    "aggregate_peak_to_average",
    "maximum_provider_utilization",
    "provider_utilization_imbalance",
    "minimum_provider_qos",
    "temporal_moved_fraction",
    "total_demand",
)


def _evaluate_pair_task(payload: tuple) -> tuple[tuple[int, int], dict]:
    (
        key,
        row_vector,
        col_vector,
        game,
        config,
        base_grid,
        slope_grid,
        beta_grid,
        search_spec,
    ) = payload
    record = evaluate_firm_pair_spatiotemporal(
        row_vector,
        col_vector,
        game,
        config,
        retail_base_grid=base_grid,
        retail_slope_grid=slope_grid,
        route_beta_grid=beta_grid,
        intermediary_search_spec=search_spec,
    )
    return key, record


@dataclass
class PairEvaluator:
    grid: np.ndarray
    game: SpatiotemporalGameSpec
    config: object
    retail_base_grid: np.ndarray | None = None
    retail_slope_grid: np.ndarray | None = None
    route_beta_grid: np.ndarray | None = None
    intermediary_search_spec: IntermediarySearchSpec | None = None
    parallel_workers: int = 1
    cache: dict[tuple[int, int], dict] = field(default_factory=dict)
    checkpoint_callback: Callable[[dict], None] | None = None
    checkpoint_interval: int = 8192

    def _task(self, key: tuple[int, int]) -> tuple:
        return (
            key,
            self.grid[key[0]],
            self.grid[key[1]],
            self.game,
            self.config,
            self.retail_base_grid,
            self.retail_slope_grid,
            self.route_beta_grid,
            self.intermediary_search_spec,
        )

    def evaluate_many(self, pairs: list[tuple[int, int]]) -> list[dict]:
        keys = [(int(row), int(col)) for row, col in pairs]
        missing = list(dict.fromkeys(key for key in keys if key not in self.cache))
        if self.parallel_workers < 1:
            raise ValueError("parallel_workers must be positive")
        if self.parallel_workers == 1 or len(missing) < 2:
            for key in missing:
                _, record = _evaluate_pair_task(self._task(key))
                self.cache[key] = record
        else:
            workers = min(self.parallel_workers, len(missing))
            with ProcessPoolExecutor(
                max_workers=workers,
                mp_context=get_context("spawn"),
            ) as executor:
                for completed, (key, record) in enumerate(executor.map(
                    _evaluate_pair_task,
                    (self._task(key) for key in missing),
                    chunksize=1,
                ), start=1):
                    self.cache[key] = record
                    if self.checkpoint_callback and completed % self.checkpoint_interval == 0:
                        self.checkpoint_callback(self.cache)
        if missing and self.checkpoint_callback:
            self.checkpoint_callback(self.cache)
        return [self.cache[key] for key in keys]

    def evaluate(self, row_index: int, col_index: int) -> dict:
        key = int(row_index), int(col_index)
        if key not in self.cache:
            self.evaluate_many([key])
        return self.cache[key]

    def restricted_payoffs(
        self, row_support: list[int], col_support: list[int]
    ) -> tuple[np.ndarray, np.ndarray]:
        row = np.zeros((len(row_support), len(col_support)))
        col = np.zeros_like(row)
        pairs = [
            (row_index, col_index)
            for row_index in row_support
            for col_index in col_support
        ]
        self.evaluate_many(pairs)
        for i, row_index in enumerate(row_support):
            for j, col_index in enumerate(col_support):
                record = self.evaluate(row_index, col_index)
                row[i, j] = record["firm_A_profit"]
                col[i, j] = record["firm_B_profit"]
        return row, col

    def full_deviation_payoffs(
        self, row_support: list[int], col_support: list[int]
    ) -> tuple[np.ndarray, np.ndarray]:
        row = np.zeros((len(self.grid), len(col_support)))
        col = np.zeros((len(row_support), len(self.grid)))
        pairs = []
        for candidate in range(len(self.grid)):
            pairs.extend((candidate, col_index) for col_index in col_support)
            pairs.extend((row_index, candidate) for row_index in row_support)
        self.evaluate_many(pairs)
        for candidate in range(len(self.grid)):
            for j, col_index in enumerate(col_support):
                row[candidate, j] = self.evaluate(
                    candidate, col_index
                )["firm_A_profit"]
            for i, row_index in enumerate(row_support):
                col[i, candidate] = self.evaluate(
                    row_index, candidate
                )["firm_B_profit"]
        return row, col


def expected_outcome(
    evaluator: PairEvaluator,
    row_support: list[int],
    col_support: list[int],
    row_mix: np.ndarray,
    col_mix: np.ndarray,
) -> tuple[dict[str, float], dict[str, list], float, list[dict]]:
    metrics = {key: 0.0 for key in SCALAR_KEYS}
    profiles: dict[str, np.ndarray] = {}
    maximum_residual = 0.0
    active_profiles = []
    for i, row_index in enumerate(row_support):
        for j, col_index in enumerate(col_support):
            weight = float(row_mix[i] * col_mix[j])
            if weight <= 0.0:
                continue
            record = evaluator.evaluate(row_index, col_index)
            result = record["result"]
            state = record["state"]
            for key in SCALAR_KEYS:
                metrics[key] += weight * float(record[key])
            arrays = {
                "aggregate_load": np.sum(result["loads"], axis=0),
                "provider_utilization": result["utilization"],
                "provider_qos": result["qos_firm"],
                "channel_demand": result["demand"],
                "destination_demand_by_type": result["destination_demand_by_type"],
                "retail_price": state.retail,
                "direct_price": state.direct,
                "wholesale_price": state.wholesale,
                "routing": state.routing,
            }
            for key, value in arrays.items():
                if key not in profiles:
                    profiles[key] = np.zeros_like(value, dtype=float)
                profiles[key] += weight * value
            maximum_residual = max(maximum_residual, record["joint_residual"])
            search = result["intermediary_search"]
            active_profiles.append({
                "row_index": int(row_index),
                "col_index": int(col_index),
                "weight": weight,
                "row_vector": evaluator.grid[row_index].tolist(),
                "col_vector": evaluator.grid[col_index].tolist(),
                "intermediary_candidate": result["intermediary_candidate"],
                "intermediary_profit": float(record["intermediary_profit"]),
                "joint_residual": float(record["joint_residual"]),
                "search_method": search["method"],
                "search_diagnostics": {
                    key: search[key]
                    for key in (
                        "function_evaluations",
                        "successful_local_runs",
                        "selected_at_retail_base_bound",
                        "selected_at_retail_slope_bound",
                        "selected_at_route_beta_bound",
                        "routing_near_deterministic",
                    )
                    if key in search
                },
            })
    return (
        metrics,
        {key: value.tolist() for key, value in profiles.items()},
        float(maximum_residual),
        active_profiles,
    )


def solve_candidate_game(
    evaluator: PairEvaluator,
    *,
    row_support: list[int] | None = None,
    col_support: list[int] | None = None,
    max_oracle_rounds: int = 12,
    regret_tolerance: float = 1e-7,
) -> dict:
    rows = sorted(set(row_support or default_support(len(evaluator.grid))))
    cols = sorted(set(col_support or default_support(len(evaluator.grid))))
    trace = []
    selected = None
    selected_rows = rows.copy()
    selected_cols = cols.copy()
    warm_candidate = None
    termination_reason = "oracle_round_limit"
    for oracle_round in range(1, max_oracle_rounds + 1):
        payoff_row, payoff_col = evaluator.restricted_payoffs(rows, cols)
        full_row, full_col = evaluator.full_deviation_payoffs(rows, cols)
        equilibria = enumerate_bimatrix_equilibria(
            payoff_row, payoff_col, initial_candidate=warm_candidate
        )
        selected = select_full_grid_equilibrium(
            equilibria, payoff_row, payoff_col, full_row, full_col
        )
        selected_rows = rows.copy()
        selected_cols = cols.copy()
        trace.append({
            "oracle_round": oracle_round,
            "row_support_size": len(rows),
            "col_support_size": len(cols),
            "restricted_equilibria": len(equilibria),
            "full_max_regret": selected["full_max_regret"],
            "relative_full_max_regret": selected["relative_full_max_regret"],
            "evaluated_pairs": len(evaluator.cache),
        })
        if selected["full_max_regret"] <= regret_tolerance:
            termination_reason = "regret_tolerance"
            break
        new_rows = sorted(set(rows + [selected["row_best_response_index"]]))
        new_cols = sorted(set(cols + [selected["col_best_response_index"]]))
        if (len(rows), len(cols)) == (len(new_rows), len(new_cols)):
            termination_reason = "no_new_best_response"
            break
        if oracle_round == max_oracle_rounds:
            break
        warm_candidate = _embed_mixed_candidate(
            rows, cols, new_rows, new_cols,
            selected["row_mix"], selected["col_mix"],
        )
        rows, cols = new_rows, new_cols
    if selected is None:
        raise RuntimeError("double oracle did not evaluate a restricted game")
    rows, cols = selected_rows, selected_cols
    row_mix = np.asarray(selected["row_mix"], dtype=float)
    col_mix = np.asarray(selected["col_mix"], dtype=float)
    metrics, profiles, maximum_residual, active_profiles = expected_outcome(
        evaluator, rows, cols, row_mix, col_mix
    )
    return {
        "candidate_count": len(evaluator.grid),
        "row_support_indices": rows,
        "col_support_indices": cols,
        "row_support_vectors": evaluator.grid[rows].tolist(),
        "col_support_vectors": evaluator.grid[cols].tolist(),
        "row_mix": row_mix.tolist(),
        "col_mix": col_mix.tolist(),
        **serializable_selected(selected),
        "full_grid_verified": selected["full_max_regret"] <= regret_tolerance,
        "regret_tolerance": regret_tolerance,
        "termination_reason": termination_reason,
        "oracle_round_limit_reached": termination_reason == "oracle_round_limit",
        "maximum_joint_residual": maximum_residual,
        "evaluated_pairs": len(evaluator.cache),
        "trace": trace,
        "expected_metrics": metrics,
        "expected_profiles": profiles,
        "active_profiles": active_profiles,
    }
