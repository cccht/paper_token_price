"""Replay every price pair and audit utilities with independent direct equations."""
from __future__ import annotations

import hashlib
import json
import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import get_context

import numpy as np

from experiments.run_user_provider_game import OUT, ROOT, population
from experiments.user_provider_experiment_tools import json_ready
from pricing_sim.user_time_game import UserGameConfig, UserPopulation, solve_user_game

_USERS = _CONFIG = None


def independent_state(actions, prices, users, config):
    actions, prices = np.asarray(actions), np.asarray(prices)
    times, providers = actions % config.periods, actions // config.periods
    assert np.all((times >= users.release) & (times <= users.deadline))
    counts = np.zeros((2, config.periods), dtype=int)
    np.add.at(counts, (providers, times), 1)
    assert counts.sum() == users.size
    ratio = counts / np.asarray(config.capacities)[:, None]
    quality = np.exp(-config.qos_strength * np.maximum(ratio - config.qos_threshold, 0) ** 2)
    bills = prices[providers, times]
    delay_hours = (times - users.release) * config.period_hours
    delay = users.delay_cost * delay_hours
    switch = config.switch_cost * (providers != users.home)
    qos_user = quality[providers, times]
    congestion = config.quality_weight * (1 - qos_user)
    utility = users.values - bills - delay - switch - congestion
    profit = np.sum(prices * counts, axis=1) - np.asarray(config.variable_cost) * counts.sum(axis=1)
    profit -= config.capacity_cost * config.periods * np.asarray(config.capacities)
    assert abs(bills.sum() - np.sum(prices * counts)) < 1e-9
    best = utility.copy()
    # Each alternative is checked at its prospective load, including the mover.
    for m in range(2):
        for t in range(config.periods):
            prospective_load = counts[m, t] + 1 - ((providers == m) & (times == t))
            q = np.exp(-config.qos_strength * np.maximum(prospective_load / config.capacities[m] - config.qos_threshold, 0) ** 2)
            alternative = users.values - prices[m, t] - users.delay_cost * config.period_hours * (t - users.release)
            alternative -= config.switch_cost * (m != users.home) + config.quality_weight * (1 - q)
            feasible = (users.release <= t) & (t <= users.deadline)
            best[feasible] = np.maximum(best[feasible], alternative[feasible])
    regret = float(np.max(best - utility))
    metrics = {"mean_utility": float(utility.mean()), "mean_generalized_cost": float((users.values - utility).mean()),
               "mean_bill": float(bills.mean()), "mean_delay_cost": float(delay.mean()), "mean_switch_cost": float(switch.mean()),
               "mean_congestion_cost": float(congestion.mean()), "total_bill": float(bills.sum()),
               "mean_qos": float(qos_user.mean()), "minimum_qos": float(qos_user.min()),
               "peak_load": float(counts.sum(axis=0).max()), "maximum_utilization": float(ratio.max()),
               "mean_delay_hours": float(delay_hours.mean()),
               "mean_flexible_delay_hours": float(delay_hours[users.flexible].mean()) if users.flexible.any() else 0.0,
               "shifted_fraction": float(np.mean(delay_hours > 0)),
               "provider_switch_fraction": float(np.mean(providers != users.home)),
               "provider_A_profit": float(profit[0]), "provider_B_profit": float(profit[1]),
               "market_profit": float(profit.sum()), "max_user_regret": regret}
    return {"metrics": metrics, "profits": profit, "utility": utility}


def initialize(users, config):
    global _USERS, _CONFIG
    _USERS, _CONFIG = users, config


def replay(key):
    result = solve_user_game(np.array(key), _USERS, _CONFIG)
    direct = independent_state(result["actions"], key, _USERS, _CONFIG)
    assert np.max(np.abs(direct["utility"] - result["utility"])) < 1e-10
    assert direct["metrics"]["max_user_regret"] < 1e-8
    return key, {"metrics": direct["metrics"], "profits": direct["profits"].tolist()}


def key_for(game, i, j):
    return tuple(game["rules"][i]["prices"]), tuple(game["rules"][j]["prices"])


def verify_case(name, users, config, games):
    keys = list(dict.fromkeys(key_for(g, i, j) for g in games for i in range(g["rule_count"]) for j in range(g["rule_count"])))
    cached = {}
    with ProcessPoolExecutor(max_workers=4, mp_context=get_context("spawn"), initializer=initialize,
                             initargs=(users, config)) as pool:
        for k, (key, value) in enumerate(pool.map(replay, keys, chunksize=8), 1):
            cached[key] = value
            if k % 2048 == 0 or k == len(keys):
                print(f"Independent replay {name}: {k}/{len(keys)}", flush=True)
    max_payoff_error = max_metric_error = max_provider_regret = 0.0
    for game in games:
        x, y = np.asarray(game["row_mix"]), np.asarray(game["col_mix"])
        assert min(x.min(), y.min()) >= -1e-12
        assert abs(x.sum() - 1) < 1e-10 and abs(y.sum() - 1) < 1e-10
        for rule in game["rules"]:
            assert abs(np.mean(rule["prices"]) - rule["base"]) < 1e-10
            assert min(rule["prices"]) >= .3 - 1e-10 and max(rule["prices"]) <= 1.35 + 1e-10
        matrices = np.array([cached[key_for(game, i, j)]["profits"] for i in range(len(x)) for j in range(len(y))]).reshape(len(x), len(y), 2)
        row, col = matrices[:, :, 0], matrices[:, :, 1]
        max_payoff_error = max(max_payoff_error, np.max(np.abs(row - game["payoff_A"])), np.max(np.abs(col - game["payoff_B"])))
        max_provider_regret = max(max_provider_regret, (row @ y).max() - x @ row @ y, (x @ col).max() - x @ col @ y)
        for field, expected in game["expected_metrics"].items():
            actual = sum(weight * cached[key_for(game, i, j)]["metrics"][field] for i, j, weight in game["active_pairs"])
            max_metric_error = max(max_metric_error, abs(actual - expected))
        assert game["maximum_offpath_user_regret"] <= 1e-8
    assert max_payoff_error < 1e-9 and max_metric_error < 1e-9 and max_provider_regret < 1e-7
    return {"name": name, "distinct_price_pairs": len(keys), "games_checked": len(games),
            "maximum_payoff_error": float(max_payoff_error), "maximum_metric_error": float(max_metric_error),
            "maximum_provider_regret": float(max_provider_regret),
            "maximum_independent_user_regret": max(r["metrics"]["max_user_regret"] for r in cached.values())}


def brute_force_representative(rep, users, config):
    prices = np.asarray(rep["prices"])
    maximum = count = 0
    actions = np.asarray(rep["after"]["actions"])
    current = independent_state(actions, prices, users, config)["utility"]
    for i in range(users.size):
        for m in range(2):
            for t in range(users.release[i], users.deadline[i] + 1):
                alternative = actions.copy()
                alternative[i] = m * config.periods + t
                utility = independent_state(alternative, prices, users, config)["utility"][i]
                maximum = max(maximum, utility - current[i])
                count += 1
    assert maximum <= 1e-8
    return {"full_assignment_rebuilds": count, "maximum_regret": maximum}


def main():
    start = time.monotonic()
    file = OUT / "experiment.json"
    data = json.loads(file.read_text())
    assert data["metadata"]["complete"] and not data["metadata"]["baseline_only"]
    assert data["metadata"]["maximum_level"] == 9
    for path, digest in data["metadata"]["source_sha256"].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    assert len(data["boundary_cases"]) == len(data["replications"]) == 4
    b = data["baseline"]
    config = UserGameConfig(**b["configuration"])
    users = UserPopulation(**{key: np.asarray(value) if value is not None else None for key, value in b["population"].items()})
    games = [g[k] for g in b["menus"] for k in ("uniform", "dynamic")]
    games += [b["mean_price_control"][k] for k in ("uniform_game", "dynamic_game")]
    results = [verify_case("baseline", users, config, games)]
    for case in [*data["boundary_cases"], *data["replications"]]:
        pop = population(data["native_profile"], config, seed=case["seed"], flexible_share=case["flexible_share"], window=case["window"])
        assert hashlib.sha256(json.dumps(json_ready(pop), sort_keys=True).encode()).hexdigest() == case["population_sha256"]
        results.append(verify_case(case["name"], pop, config, [case["uniform"], case["dynamic"]]))
    brute = brute_force_representative(b["representative"], users, config)
    trace = b["representative"]["trace"]
    assert np.max(np.diff([r["potential"] for r in trace])) <= 1e-9
    assert trace[-1]["max_user_regret"] <= 1e-8
    result = {"passed": True, "experiment_sha256": hashlib.sha256(file.read_bytes()).hexdigest(),
              "validator_sha256": hashlib.sha256((ROOT / "experiments/verify_user_provider_game.py").read_bytes()).hexdigest(),
              "elapsed_seconds": time.monotonic() - start, "cases": results, "representative_brute_force": brute,
              "scope": "All declared finite price pairs replayed; independent utility/accounting/deviation equations. Not a continuous-price or empirical-market certificate."}
    (OUT / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
