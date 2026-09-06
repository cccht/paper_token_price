"""Atomic user time-choice congestion game with an exact potential."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .peak_shaving_market import qos_factor


@dataclass(frozen=True)
class UserGameConfig:
    capacities: tuple[float, float] = (30.0, 12.0)
    periods: int = 8
    period_hours: float = 3.0
    quality_weight: float = 2.0
    switch_cost: float = 0.03
    qos_threshold: float = 1.0
    qos_strength: float = 0.5747
    variable_cost: tuple[float, float] = (0.20, 0.18)
    capacity_cost: float = 0.015
    improvement_tolerance: float = 1e-10
    user_tolerance: float = 1e-8
    max_sweeps: int = 500


@dataclass(frozen=True)
class UserPopulation:
    release: np.ndarray
    deadline: np.ndarray
    home: np.ndarray
    delay_cost: np.ndarray
    flexible: np.ndarray
    values: np.ndarray
    order: np.ndarray | None = None

    @property
    def size(self):
        return len(self.release)


def _prepare(prices, users, config):
    prices = np.asarray(prices, dtype=float)
    n, t = users.size, config.periods
    arrays = (users.release, users.deadline, users.home, users.delay_cost, users.flexible, users.values)
    if n < 1 or prices.shape != (2, t) or any(np.asarray(a).shape != (n,) for a in arrays):
        raise ValueError("invalid user/price dimensions")
    if (not np.all(np.isfinite(prices)) or np.any(prices < 0)
            or not all(np.all(np.isfinite(a)) for a in arrays)):
        raise ValueError("prices and user data must be finite and nonnegative where applicable")
    if (np.any(users.release < 0) or np.any(users.deadline >= t) or np.any(users.release > users.deadline)
            or np.any((users.home < 0) | (users.home > 1)) or np.any(users.delay_cost < 0)
            or min(config.capacities) <= 0 or config.quality_weight < 0 or config.switch_cost < 0
            or config.period_hours <= 0 or config.max_sweeps < 1):
        raise ValueError("invalid feasible window, cost, or capacity")
    if any(np.any(np.asarray(a) != np.asarray(a, dtype=int)) for a in (users.release, users.deadline, users.home)):
        raise ValueError("release, deadline, and home must be integer indices")
    periods = np.tile(np.arange(t), 2)
    provider = np.repeat(np.arange(2), t)
    delay = config.period_hours * (periods[None, :] - users.release[:, None])
    static = prices.ravel()[None, :] + users.delay_cost[:, None] * delay
    static += config.switch_cost * (provider[None, :] != users.home[:, None])
    feasible = (periods[None, :] >= users.release[:, None]) & (periods[None, :] <= users.deadline[:, None])
    static = np.where(feasible, static, np.inf)
    ratio = np.arange(n + 2)[None, :] / np.repeat(config.capacities, t)[:, None]
    resource_cost = config.quality_weight * (1 - qos_factor(ratio, config, "threshold"))
    return static, resource_cost


def _valid_actions(actions, users, config):
    actions = np.asarray(actions)
    if (actions.shape != (users.size,) or not np.all(np.isfinite(actions))
            or np.any(actions != actions.astype(int)) or np.any(actions < 0)
            or np.any(actions >= 2 * config.periods)):
        raise ValueError("invalid user action indices")
    times = actions % config.periods
    if np.any(times < users.release) or np.any(times > users.deadline):
        raise ValueError("assignment violates a release time or deadline")
    return actions.astype(int)


def prospective_costs(player, *, current, counts, prices, users, config):
    static, resources = _prepare(prices, users, config)
    loads = np.asarray(counts, dtype=int).copy() + 1
    loads[current] -= 1
    return static[player] + resources[np.arange(2 * config.periods), loads]


def potential(actions, prices, users, config):
    actions = _valid_actions(actions, users, config)
    static, resources = _prepare(prices, users, config)
    counts = np.bincount(actions, minlength=2 * config.periods)
    cumulative = np.cumsum(resources, axis=1)
    return float(static[np.arange(users.size), actions].sum()
                 + cumulative[np.arange(2 * config.periods), counts].sum())


def _regrets(actions, counts, static, resources):
    resource_ids = np.arange(len(counts))
    candidates = static + resources[resource_ids, counts + 1][None, :]
    current = static[np.arange(len(actions)), actions] + resources[actions, counts[actions]]
    candidates[np.arange(len(actions)), actions] = current
    return np.maximum(current - candidates.min(axis=1), 0.0)


def evaluate_assignment(actions, prices, users, config):
    actions = _valid_actions(actions, users, config)
    static, resources = _prepare(prices, users, config)
    counts = np.bincount(actions, minlength=2 * config.periods)
    costs = static[np.arange(users.size), actions] + resources[actions, counts[actions]]
    times, providers = actions % config.periods, actions // config.periods
    bill = np.asarray(prices).ravel()[actions]
    delay_hours = config.period_hours * (times - users.release)
    delay_cost = users.delay_cost * delay_hours
    switch_cost = config.switch_cost * (providers != users.home)
    loads = counts.reshape(2, config.periods)
    utilization = loads / np.asarray(config.capacities)[:, None]
    qos = qos_factor(utilization, config, "threshold")
    revenue = (np.asarray(prices) * loads).sum(axis=1)
    variable = np.asarray(config.variable_cost) * loads.sum(axis=1)
    holding = config.capacity_cost * config.periods * np.asarray(config.capacities)
    regrets = _regrets(actions, counts, static, resources)
    return {"actions": actions, "counts": loads, "utility": users.values - costs,
            "cost": costs, "bill": bill, "delay_hours": delay_hours, "delay_cost": delay_cost,
            "switch_cost": switch_cost, "congestion_cost": resources[actions, counts[actions]],
            "qos_by_user": qos.ravel()[actions], "utilization": utilization, "qos": qos,
            "provider_revenue": revenue, "provider_profit": revenue - variable - holding,
            "provider_variable_cost": variable, "provider_holding_cost": holding,
            "user_regret": regrets, "max_user_regret": float(regrets.max())}


def solve_user_game(prices, users, config, *, initial=None, order=None, record_trace=False):
    static, resources = _prepare(prices, users, config)
    actions = users.home * config.periods + users.release if initial is None else initial
    actions = _valid_actions(actions, users, config).copy()
    order = users.order if order is None else order
    order = np.arange(users.size) if order is None else np.asarray(order, dtype=int)
    if not np.array_equal(np.sort(order), np.arange(users.size)):
        raise ValueError("user order must be a permutation")
    counts = np.bincount(actions, minlength=2 * config.periods)
    ids = np.arange(2 * config.periods)
    cumulative = np.cumsum(resources, axis=1)

    def phi():
        return float(static[np.arange(users.size), actions].sum() + cumulative[ids, counts].sum())

    def record(sweep, moves):
        own = static[np.arange(users.size), actions] + resources[actions, counts[actions]]
        return {"sweep": sweep, "moves": moves, "potential": phi(),
                "mean_utility": float((users.values - own).mean()),
                "max_user_regret": float(_regrets(actions, counts, static, resources).max())}

    trace = [record(0, 0)] if record_trace else []
    total_moves, accumulated_phi = 0, phi()
    max_identity_error = 0.0
    for sweep in range(1, config.max_sweeps + 1):
        moves = 0
        for player in order:
            current = actions[player]
            alternatives = static[player] + resources[ids, counts + 1]
            alternatives[current] = static[player, current] + resources[current, counts[current]]
            best = int(np.argmin(alternatives))
            delta = float(alternatives[best] - alternatives[current])
            if delta < -config.improvement_tolerance:
                counts[current] -= 1
                counts[best] += 1
                actions[player] = best
                accumulated_phi += delta
                moves += 1
        total_moves += moves
        max_identity_error = max(max_identity_error, abs(phi() - accumulated_phi))
        if record_trace:
            trace.append(record(sweep, total_moves))
        if not moves:
            break
    result = evaluate_assignment(actions, prices, users, config)
    if result["max_user_regret"] > config.user_tolerance:
        raise RuntimeError(f"user Nash tolerance not attained: {result['max_user_regret']}")
    if max_identity_error > 1e-7:
        raise RuntimeError("potential/individual-improvement identity failed")
    result.update({"sweeps": sweep, "moves": total_moves, "potential_identity_error": max_identity_error,
                   "trace": trace, "potential": phi(), "user_nash_verified": True})
    return result
