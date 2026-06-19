"""Reviewer-response diagnostics for the intermediary pricing game."""

from __future__ import annotations

import numpy as np

from .capacity_only_game import optimize_capacity_only
from .fixed_capacity_game import optimize_fixed_capacity_stackelberg
from .intermediary_market import (
    IntermediaryConfig,
    ThreeLayerResult,
    _choice_shares,
    _default_capacity,
    evaluate_three_layer_policy,
    qos_factor,
)
from .three_stage_game import (
    _intermediary_profit,
    optimize_congestion_proxy_stackelberg,
    optimize_three_stage_stackelberg,
)


def metric_row(experiment: str, result: ThreeLayerResult, extra: dict[str, object] | None = None) -> dict[str, object]:
    row: dict[str, object] = {
        "experiment": experiment,
        "policy": result.policy,
        "platform_revenue": result.platform_revenue,
        "intermediary_profit": result.intermediary_profit,
        "system_profit": result.system_profit,
        "min_qos": float(np.min(result.qos)),
        "max_utilization": float(np.max(result.utilization)),
        "max_solver_regret": result.diagnostics.get("max_nash_regret", ""),
        "objective_evaluations": result.diagnostics.get("objective_evaluations", 1),
    }
    row.update(extra or {})
    return row


def attribution_rows(config: IntermediaryConfig) -> list[dict[str, object]]:
    uniform = _uniform_result(config)
    rows = [
        metric_row("attribution", uniform, {"mechanism": "none"}),
        metric_row("attribution", optimize_capacity_only(config), {"mechanism": "capacity_only"}),
        metric_row("attribution", optimize_fixed_capacity_stackelberg(config), {"mechanism": "price_only"}),
        metric_row(
            "attribution",
            optimize_three_stage_stackelberg(config, qos_aware=False, policy="price_capacity_no_qos"),
            {"mechanism": "price_and_capacity_without_qos_internalization"},
        ),
        metric_row(
            "attribution",
            optimize_congestion_proxy_stackelberg(config),
            {"mechanism": "price_capacity_with_congestion_proxy"},
        ),
        metric_row(
            "attribution",
            optimize_three_stage_stackelberg(config, policy="three_layer_qos_aware"),
            {"mechanism": "price_capacity_and_qos_internalization"},
        ),
    ]
    base = float(rows[0]["system_profit"])
    full_gain = max(float(rows[-1]["system_profit"]) - base, 1e-12)
    for row in rows:
        gain = float(row["system_profit"]) - base
        row["system_gain_vs_uniform"] = gain
        row["share_of_full_gain"] = gain / full_gain
    return rows


def profit_slice_rows(
    result: ThreeLayerResult,
    config: IntermediaryConfig,
    *,
    points: int = 41,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rows = _retail_slice(result, config, points) + _capacity_transfer_slice(result, config, points)
    summaries = []
    for slice_name in sorted({str(row["slice"]) for row in rows}):
        profits = np.array([float(row["profit"]) for row in rows if row["slice"] == slice_name])
        summaries.append({
            "slice": slice_name,
            "points": int(profits.size),
            "local_peak_count": _local_peak_count(profits),
            "max_profit": float(np.max(profits)),
            "min_profit": float(np.min(profits)),
            "single_peak_diagnostic": _local_peak_count(profits) <= 1,
        })
    return rows, summaries


def finite_bridge_rows(
    result: ThreeLayerResult,
    config: IntermediaryConfig,
    *,
    player_counts: tuple[int, ...] = (60, 120, 240),
    seeds: tuple[int, ...] = (0, 1, 2, 3),
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rows = []
    target = result.shares / max(float(np.sum(result.shares)), 1e-12)
    for players in player_counts:
        for seed in seeds:
            empirical, sweeps, converged = _finite_psne_distribution(result, config, players, seed)
            rows.append(_bridge_metric_row(players, seed, empirical, target, sweeps, converged))
    return rows, _bridge_summary_rows(rows)


def _uniform_result(config: IntermediaryConfig) -> ThreeLayerResult:
    wholesale = np.full(config.num_periods, config.base_wholesale_price)
    retail = np.full((config.num_intermediaries, config.num_periods), config.base_retail_price)
    return evaluate_three_layer_policy(wholesale, retail, _default_capacity(config), config, policy="uniform_retail")


def _retail_slice(result: ThreeLayerResult, config: IntermediaryConfig, points: int) -> list[dict[str, object]]:
    broker = 0
    period = int(np.argmax(config.time_preference))
    current = float(result.retail_prices[broker, period])
    values = np.linspace(max(config.retail_lower_bound, current - 0.55), min(config.retail_upper_bound, current + 0.55), points)
    rows = []
    for value in values:
        retail = result.retail_prices.copy()
        retail[broker, period] = value
        profit = _profit_for(result.wholesale_prices, retail, result.capacity, config, broker)
        rows.append({"slice": "retail_peak_period", "broker": broker + 1, "period": period + 1, "x": value, "profit": profit})
    return rows


def _capacity_transfer_slice(result: ThreeLayerResult, config: IntermediaryConfig, points: int) -> list[dict[str, object]]:
    broker = 0
    source = int(np.argmin(config.time_preference))
    target = int(np.argmax(config.time_preference))
    row = result.capacity[broker]
    span = min(float(row[source] - 1e-6), float(row[target] - 1e-6), 140.0)
    deltas = np.linspace(-span, span, points)
    rows = []
    for delta in deltas:
        capacity = result.capacity.copy()
        capacity[broker, source] -= delta
        capacity[broker, target] += delta
        profit = _profit_for(result.wholesale_prices, result.retail_prices, capacity, config, broker)
        rows.append({"slice": "capacity_offpeak_to_peak", "broker": broker + 1, "source_period": source + 1, "target_period": target + 1, "x": delta, "profit": profit})
    return rows


def _profit_for(
    wholesale: np.ndarray,
    retail: np.ndarray,
    capacity: np.ndarray,
    config: IntermediaryConfig,
    broker: int,
) -> float:
    candidate = evaluate_three_layer_policy(wholesale, retail, capacity, config)
    return _intermediary_profit(candidate, config, broker)


def _finite_psne_distribution(
    result: ThreeLayerResult,
    config: IntermediaryConfig,
    players: int,
    seed: int,
) -> tuple[np.ndarray, int, bool]:
    rng = np.random.default_rng(seed)
    actions = _action_grid(config)
    deterministic = _deterministic_action_utility(result, config, actions)
    shocks = rng.gumbel(size=(players, len(actions)))
    choices = np.argmax(deterministic[None, :] + shocks, axis=1)
    unit_demand = float(np.sum(result.demand)) / max(players, 1)
    for sweep in range(1, 81):
        changed = False
        counts = np.bincount(choices, minlength=len(actions))
        for player in range(players):
            best = _best_finite_action(player, choices, counts, deterministic, shocks, result, config, actions, unit_demand)
            if best != choices[player]:
                counts[choices[player]] -= 1
                counts[best] += 1
                choices[player] = best
                changed = True
        if not changed:
            return _empirical_share(choices, actions, config), sweep, True
    return _empirical_share(choices, actions, config), 80, False


def _best_finite_action(
    player: int,
    choices: np.ndarray,
    counts: np.ndarray,
    deterministic: np.ndarray,
    shocks: np.ndarray,
    result: ThreeLayerResult,
    config: IntermediaryConfig,
    actions: list[tuple[int, int]],
    unit_demand: float,
) -> int:
    scores = np.empty(len(actions), dtype=float)
    current = int(choices[player])
    for action_idx, (broker, period) in enumerate(actions):
        action_count = counts[action_idx] + (0 if action_idx == current else 1)
        if action_idx == current:
            action_count = max(action_count, 1)
        load = action_count * unit_demand / max(float(result.capacity[broker, period]), 1e-8)
        qos = float(qos_factor(np.array([load]), config)[0])
        scores[action_idx] = deterministic[action_idx] - config.qos_feedback_weight * (1.0 - qos) + shocks[player, action_idx]
    return int(np.argmax(scores))


def _deterministic_action_utility(
    result: ThreeLayerResult,
    config: IntermediaryConfig,
    actions: list[tuple[int, int]],
) -> np.ndarray:
    values = []
    for broker, period in actions:
        move_cost = config.inconvenience_cost * (1.0 - config.native_period_distribution[period])
        utility = np.log(config.brand_quality[broker] + 1e-10) + np.log(config.time_preference[period] + 1e-10)
        utility -= config.price_sensitivity * (result.retail_prices[broker, period] + move_cost - config.base_retail_price)
        values.append(float(utility))
    return np.asarray(values, dtype=float)


def _bridge_metric_row(
    players: int,
    seed: int,
    empirical: np.ndarray,
    target: np.ndarray,
    sweeps: int,
    converged: bool,
) -> dict[str, object]:
    diff = empirical - target
    return {
        "players": players,
        "seed": seed,
        "l1_share_gap": float(np.sum(np.abs(diff))),
        "max_cell_gap": float(np.max(np.abs(diff))),
        "cosine_similarity": _cosine_similarity(empirical, target),
        "sweeps": sweeps,
        "converged": converged,
    }


def _bridge_summary_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    summaries = []
    for players in sorted({int(row["players"]) for row in rows}):
        selected = [row for row in rows if int(row["players"]) == players]
        summaries.append({
            "players": players,
            "runs": len(selected),
            "l1_share_gap_mean": float(np.mean([row["l1_share_gap"] for row in selected])),
            "max_cell_gap_mean": float(np.mean([row["max_cell_gap"] for row in selected])),
            "cosine_similarity_mean": float(np.mean([row["cosine_similarity"] for row in selected])),
            "converged_runs": int(sum(bool(row["converged"]) for row in selected)),
        })
    return summaries


def _action_grid(config: IntermediaryConfig) -> list[tuple[int, int]]:
    return [(broker, period) for broker in range(config.num_intermediaries) for period in range(config.num_periods)]


def _empirical_share(choices: np.ndarray, actions: list[tuple[int, int]], config: IntermediaryConfig) -> np.ndarray:
    shares = np.zeros((config.num_intermediaries, config.num_periods), dtype=float)
    for action_idx, (broker, period) in enumerate(actions):
        shares[broker, period] = float(np.sum(choices == action_idx)) / max(len(choices), 1)
    return shares


def _local_peak_count(values: np.ndarray) -> int:
    return int(sum(values[idx] >= values[idx - 1] and values[idx] >= values[idx + 1] for idx in range(1, len(values) - 1)))


def _cosine_similarity(left: np.ndarray, right: np.ndarray) -> float:
    denom = float(np.linalg.norm(left) * np.linalg.norm(right))
    if denom <= 1e-12:
        return 0.0
    return float(np.sum(left * right) / denom)
