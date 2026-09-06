"""Finite pricing menus with exact atomic-user response certification."""
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict
from multiprocessing import get_context

import numpy as np

from pricing_sim.finite_game import enumerate_bimatrix_equilibria
from pricing_sim.user_time_game import evaluate_assignment, solve_user_game

PROVIDER_TOLERANCE = 1e-7
PRICE_LOWER, PRICE_UPPER = 0.30, 1.35
_WORKER_USERS = None
_WORKER_CONFIG = None


def price_menu(signal, *, base_count, slope_count, fixed_mean=None):
    bases = [fixed_mean] if fixed_mean is not None else np.linspace(0.45, 1.05, base_count)
    slopes = [0.0] if slope_count == 1 else np.linspace(-0.30, 0.30, slope_count)
    rules, seen = [], set()
    for base in bases:
        for slope in slopes:
            prices = np.round(base + slope * np.asarray(signal), 12)
            key = tuple(prices)
            if prices.min() < PRICE_LOWER - 1e-10 or prices.max() > PRICE_UPPER + 1e-10 or key in seen:
                continue
            seen.add(key)
            rules.append({"base": float(base), "slope": float(slope), "prices": prices.tolist()})
    return rules


def summary(result, users):
    flexible = users.flexible
    delayed = result["delay_hours"] > 0
    return {
        "mean_utility": float(result["utility"].mean()),
        "mean_generalized_cost": float(result["cost"].mean()),
        "mean_bill": float(result["bill"].mean()),
        "mean_delay_cost": float(result["delay_cost"].mean()),
        "mean_switch_cost": float(result["switch_cost"].mean()),
        "mean_congestion_cost": float(result["congestion_cost"].mean()),
        "total_bill": float(result["bill"].sum()),
        "mean_qos": float(result["qos_by_user"].mean()),
        "minimum_qos": float(result["qos_by_user"].min()),
        "peak_load": float(result["counts"].sum(axis=0).max()),
        "maximum_utilization": float(result["utilization"].max()),
        "mean_delay_hours": float(result["delay_hours"].mean()),
        "mean_flexible_delay_hours": float(result["delay_hours"][flexible].mean()) if flexible.any() else 0.0,
        "shifted_fraction": float(delayed.mean()),
        "provider_switch_fraction": float((result["switch_cost"] > 0).mean()),
        "provider_A_profit": float(result["provider_profit"][0]),
        "provider_B_profit": float(result["provider_profit"][1]),
        "market_profit": float(result["provider_profit"].sum()),
        "max_user_regret": result["max_user_regret"],
    }


def _initialize(users, config):
    global _WORKER_USERS, _WORKER_CONFIG
    _WORKER_USERS, _WORKER_CONFIG = users, config


def _evaluate_pair(key):
    prices = np.asarray(key)
    result = solve_user_game(prices, _WORKER_USERS, _WORKER_CONFIG)
    return key, {"summary": summary(result, _WORKER_USERS), "profits": result["provider_profit"].tolist(),
                 "sweeps": result["sweeps"], "moves": result["moves"],
                 "potential_identity_error": result["potential_identity_error"]}


def _price_key(row, col):
    return tuple(row["prices"]), tuple(col["prices"])


def solve_price_matrix(row, col):
    candidates = enumerate_bimatrix_equilibria(row, col)
    pure = [c for c in candidates if c["method"] == "pure_best_response"]
    if pure:
        chosen = min(pure, key=lambda c: (int(np.argmax(c["row_mix"])), int(np.argmax(c["col_mix"]))))
    else:
        chosen = min(candidates, key=lambda c: c["restricted_max_regret"])
    x, y = chosen["row_mix"], chosen["col_mix"]
    expected = [float(x @ row @ y), float(x @ col @ y)]
    deviations = [max(float(np.max(row @ y)) - expected[0], 0),
                  max(float(np.max(x @ col)) - expected[1], 0)]
    if max(deviations) > PROVIDER_TOLERANCE:
        raise RuntimeError(f"manufacturer Nash check failed: {deviations}")
    return {"row_mix": x.tolist(), "col_mix": y.tolist(), "expected_profit": expected,
            "provider_regret": deviations, "provider_nash_verified": True,
            "method": chosen["method"], "pure_equilibria_found": len(pure),
            "selection": "lexicographically first pure equilibrium, else smallest verified mixed regret"}


class PricingEvaluator:
    def __init__(self, users, config, *, workers=4, name="baseline"):
        self.users, self.config, self.workers, self.name = users, config, workers, name
        self.cache = {}

    def matrices(self, rules):
        keys = [_price_key(a, b) for a in rules for b in rules]
        missing = list(dict.fromkeys(k for k in keys if k not in self.cache))
        if missing:
            with ProcessPoolExecutor(max_workers=self.workers, mp_context=get_context("spawn"),
                                     initializer=_initialize, initargs=(self.users, self.config)) as pool:
                for index, (key, record) in enumerate(pool.map(_evaluate_pair, missing, chunksize=8), start=1):
                    self.cache[key] = record
                    if index % 512 == 0 or index == len(missing):
                        print(f"{self.name}: {index}/{len(missing)} new price pairs; {len(self.cache)} cached", flush=True)
        size = len(rules)
        values = np.asarray([self.cache[key]["profits"] for key in keys]).reshape(size, size, 2)
        max_regret = max(self.cache[key]["summary"]["max_user_regret"] for key in keys)
        return values[:, :, 0], values[:, :, 1], max_regret

    def game(self, rules, *, name):
        row, col, user_regret = self.matrices(rules)
        equilibrium = solve_price_matrix(row, col)
        x, y = np.asarray(equilibrium["row_mix"]), np.asarray(equilibrium["col_mix"])
        active = [(i, j, float(a * b)) for i, a in enumerate(x) for j, b in enumerate(y) if a * b > 0]
        sample = self.cache[_price_key(rules[0], rules[0])]["summary"]
        expected = {key: sum(weight * self.cache[_price_key(rules[i], rules[j])]["summary"][key]
                             for i, j, weight in active) for key in sample}
        equilibrium.update({"name": name, "rules": rules, "rule_count": len(rules),
                            "payoff_A": row.tolist(), "payoff_B": col.tolist(),
                            "maximum_offpath_user_regret": user_regret,
                            "expected_metrics": expected, "active_pairs": active,
                            "all_price_pairs_verified": True})
        print(f"{self.name}/{name}: rules={len(rules)}, support={np.count_nonzero(x)}/{np.count_nonzero(y)}, "
              f"provider regret={max(equilibrium['provider_regret']):.2g}, user regret={user_regret:.2g}", flush=True)
        return equilibrium

    def outcome(self, game, *, original_schedule=False):
        results, weights = [], []
        for i, j, weight in game["active_pairs"]:
            prices = np.array([game["rules"][i]["prices"], game["rules"][j]["prices"]])
            if original_schedule:
                initial = self.users.home * self.config.periods + self.users.release
                state = evaluate_assignment(initial, prices, self.users, self.config)
            else:
                state = solve_user_game(prices, self.users, self.config)
            results.append(state)
            weights.append(weight)
        weights = np.asarray(weights)
        fields = ("utility", "cost", "bill", "delay_hours", "delay_cost", "switch_cost", "congestion_cost",
                  "qos_by_user", "counts", "qos", "utilization", "provider_profit", "provider_revenue")
        outcome = {key: np.tensordot(weights, np.asarray([r[key] for r in results]), axes=(0, 0)) for key in fields}
        metrics = [summary(r, self.users) for r in results]
        outcome["metrics"] = {key: float(np.dot(weights, [m[key] for m in metrics])) for key in metrics[0]}
        outcome["prices"] = sum(weight * np.array([game["rules"][i]["prices"], game["rules"][j]["prices"]])
                                for i, j, weight in game["active_pairs"])
        outcome["user_nash_verified"] = not original_schedule
        return outcome


def extended_menu_regret(coarse, fine):
    lookup = {tuple(rule["prices"]): index for index, rule in enumerate(fine["rules"])}
    indices = [lookup[tuple(rule["prices"])] for rule in coarse["rules"]]
    row, col = np.asarray(fine["payoff_A"]), np.asarray(fine["payoff_B"])
    x, y = np.asarray(coarse["row_mix"]), np.asarray(coarse["col_mix"])
    expected = [float(x @ row[np.ix_(indices, indices)] @ y), float(x @ col[np.ix_(indices, indices)] @ y)]
    regret = [max(float((row[:, indices] @ y).max()) - expected[0], 0),
              max(float((x @ col[indices, :]).max()) - expected[1], 0)]
    return {"absolute": regret, "relative": [v / max(abs(p), 1) for v, p in zip(regret, expected)]}


def json_ready(value):
    if hasattr(value, "__dataclass_fields__"):
        return json_ready(asdict(value))
    if isinstance(value, dict):
        return {str(k): json_ready(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [json_ready(v) for v in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    return value
