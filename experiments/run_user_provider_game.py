"""Price competition with strategic user timing: matched before/after experiments."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import time
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

import numpy as np
import scipy

from experiments.user_provider_experiment_tools import (
    PricingEvaluator,
    extended_menu_regret,
    json_ready,
    price_menu,
    summary,
)
from pricing_sim.user_time_game import (
    UserGameConfig,
    UserPopulation,
    evaluate_assignment,
    prospective_costs,
    solve_user_game,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/user_provider_game/20260906"
LOAD = ROOT / "data/processed/burstgpt_d895a53b_8period/burstgpt_8period_load_profile.csv"
QOS = ROOT / "artifacts/peak_shaving/20260712_final/qos_calibration.json"
SEED = 20260906
LEVELS = (3, 5, 9)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inputs():
    with LOAD.open(newline="") as stream:
        profile = np.array([float(row["token_share_mean"]) for row in csv.DictReader(stream)])
    profile /= profile.sum()
    centered = profile - profile.mean()
    signal = centered / np.max(np.abs(centered))
    fit = json.loads(QOS.read_text())["pooled_fit"]
    return profile, signal, UserGameConfig(qos_threshold=fit["threshold"], qos_strength=fit["strength"])


def population(profile, config, *, seed=SEED, size=240, flexible_share=0.5, window=2):
    rng = np.random.default_rng(seed)
    release = rng.choice(config.periods, size=size, p=profile)
    home = rng.choice(2, size=size, p=np.array(config.capacities) / sum(config.capacities))
    delay = rng.uniform(0.01, 0.03, size=size)
    ranking = rng.permutation(size)
    flexible = np.zeros(size, dtype=bool)
    flexible[ranking[:round(size * flexible_share)]] = True
    deadline = np.minimum(release + flexible * window, config.periods - 1)
    return UserPopulation(release=release, deadline=deadline, home=home, delay_cost=delay,
                          flexible=flexible, values=np.full(size, 2.0), order=rng.permutation(size))


def representative_details(evaluator, game):
    i, j, weight = min(game["active_pairs"], key=lambda item: (-item[2], item[0], item[1]))
    prices = np.array([game["rules"][i]["prices"], game["rules"][j]["prices"]])
    users, config = evaluator.users, evaluator.config
    final = solve_user_game(prices, users, config, record_trace=True)
    initial = evaluate_assignment(users.home * config.periods + users.release, prices, users, config)
    eligible = np.flatnonzero(users.deadline > users.release)
    player = int(eligible[0]) if len(eligible) else 0
    candidates = []
    for name, state in (("before", initial), ("after", final)):
        costs = prospective_costs(player, current=int(state["actions"][player]), counts=state["counts"].ravel(),
                                  prices=prices, users=users, config=config)
        utility = users.values[player] - costs
        candidates.append({"state": name, "utility_by_action": [float(v) if np.isfinite(v) else None for v in utility]})
    return {"selection": "highest-probability price pair; lexicographic tie break", "row": i, "col": j,
            "weight": weight, "prices": prices, "trace": final["trace"],
            "before": initial, "after": final,
            "example_user": {"selection": "first user index with a nontrivial feasible window", "id": player,
                             "release": int(users.release[player]), "deadline": int(users.deadline[player]),
                             "before_action": int(initial["actions"][player]), "after_action": int(final["actions"][player]),
                             "curves": candidates}}


def order_audit(evaluator, game):
    users, config = evaluator.users, evaluator.config
    orders = [np.arange(users.size), np.arange(users.size)[::-1], np.random.default_rng(SEED + 77).permutation(users.size)]
    output = []
    for index, order in enumerate(orders):
        expected = None
        maximum_regret = 0
        for i, j, weight in game["active_pairs"]:
            prices = np.array([game["rules"][i]["prices"], game["rules"][j]["prices"]])
            result = solve_user_game(prices, users, config, order=order)
            record = summary(result, users)
            if expected is None:
                expected = {key: 0.0 for key in record}
            for key, value in record.items():
                expected[key] += weight * value
            maximum_regret = max(maximum_regret, result["max_user_regret"])
        output.append({"order": ("natural", "reverse", "independent_permutation")[index],
                       "expected_metrics": expected, "max_user_regret": maximum_regret,
                       "provider_equilibrium_recertified": False})
    return output


def main_case(users, config, signal, *, workers=4, levels=LEVELS):
    evaluator = PricingEvaluator(users, config, workers=workers)
    results = []
    for level in levels:
        u = evaluator.game(price_menu(signal, base_count=level, slope_count=1), name=f"uniform_{level}")
        d = evaluator.game(price_menu(signal, base_count=level, slope_count=level), name=f"tou_{level}")
        results.append({"axis_count": level, "uniform": u, "dynamic": d})
    final = results[-1]
    for level in results[:-1]:
        for regime in ("uniform", "dynamic"):
            level[regime]["deviation_on_final_menu"] = extended_menu_regret(level[regime], final[regime])
    outcomes = {
        "uniform_initial": evaluator.outcome(final["uniform"], original_schedule=True),
        "uniform_equilibrium": evaluator.outcome(final["uniform"]),
        "tou_initial": evaluator.outcome(final["dynamic"], original_schedule=True),
        "tou_equilibrium": evaluator.outcome(final["dynamic"]),
    }
    representative = representative_details(evaluator, final["dynamic"])
    fixed_u = evaluator.game(price_menu(signal, base_count=1, slope_count=1, fixed_mean=0.75), name="fixed_mean_uniform")
    fixed_d = evaluator.game(price_menu(signal, base_count=1, slope_count=levels[-1], fixed_mean=0.75), name="fixed_mean_tou")
    return {"population": asdict(users), "configuration": asdict(config), "menus": results, "outcomes": outcomes,
            "representative": representative, "order_audit": order_audit(evaluator, final["dynamic"]),
            "mean_price_control": {"uniform_game": fixed_u, "dynamic_game": fixed_d,
                                   "uniform": evaluator.outcome(fixed_u), "dynamic": evaluator.outcome(fixed_d)},
            "cached_price_pairs": len(evaluator.cache)}


def secondary_case(profile, config, signal, *, name, workers, seed=SEED, flexible_share=0.5, window=2, level=9):
    users = population(profile, config, seed=seed, flexible_share=flexible_share, window=window)
    evaluator = PricingEvaluator(users, config, workers=workers, name=name)
    u = evaluator.game(price_menu(signal, base_count=level, slope_count=1), name="uniform")
    d = evaluator.game(price_menu(signal, base_count=level, slope_count=level), name="tou")
    return {"name": name, "seed": seed, "flexible_share": flexible_share, "window": window,
            "axis_count": level, "uniform": u, "dynamic": d,
            "population_sha256": hashlib.sha256(json.dumps(json_ready(users), sort_keys=True).encode()).hexdigest()}


def write(payload, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    temporary = output_dir / "experiment.json.tmp"
    temporary.write_text(json.dumps(json_ready(payload), indent=2, allow_nan=False) + "\n")
    temporary.replace(output_dir / "experiment.json")


def run(*, workers=4, baseline_only=False, maximum_level=9):
    profile, signal, config = inputs()
    users = population(profile, config)
    levels = tuple(level for level in LEVELS if level <= maximum_level)
    if not levels or workers < 1:
        raise ValueError("invalid computation level or worker count")
    source_paths = (Path(__file__), ROOT / "experiments/user_provider_experiment_tools.py",
                    ROOT / "pricing_sim/user_time_game.py", ROOT / "pricing_sim/peak_shaving_market.py",
                    ROOT / "pricing_sim/finite_game.py", ROOT / "pricing_sim/bimatrix_solver.py",
                    ROOT / "pricing_sim/complementarity_solver.py", ROOT / "pricing_sim/milp_equilibrium_solver.py",
                    ROOT / "docs/reviews/user_provider_game_protocol_2026-09-06.md", LOAD, QOS)
    payload = {"metadata": {"started_at": datetime.now().astimezone().isoformat(timespec="seconds"),
                            "model": "finite manufacturer price game with atomic user Nash subgames",
                            "seed": SEED, "workers": workers, "python": platform.python_version(),
                            "numpy": np.__version__, "scipy": scipy.__version__,
                            "source_sha256": {str(p.relative_to(ROOT)): sha(p) for p in source_paths},
                            "scope": "synthetic equal-workload request agents; finite price menu only",
                            "old_logit_results_reused": False}, "native_profile": profile, "price_signal": signal}
    start = time.monotonic()
    payload["baseline"] = main_case(users, config, signal, workers=workers, levels=levels)
    payload["boundary_cases"] = []
    payload["replications"] = []
    write(payload, OUT)
    if not baseline_only:
        for name, share, window in (("flex_25", 0.25, 2), ("flex_75", 0.75, 2), ("window_1", 0.5, 1), ("no_time_flexibility", 0.0, 0)):
            payload["boundary_cases"].append(secondary_case(profile, config, signal, name=name, workers=workers,
                                                          flexible_share=share, window=window, level=levels[-1]))
            write(payload, OUT)
        for seed in range(SEED + 1, SEED + 5):
            payload["replications"].append(secondary_case(profile, config, signal, name=f"seed_{seed}", workers=workers,
                                                        seed=seed, level=levels[-1]))
            write(payload, OUT)
    payload["metadata"].update({"elapsed_seconds": time.monotonic() - start, "complete": True,
                                "baseline_only": baseline_only, "maximum_level": maximum_level})
    write(payload, OUT)
    print(json.dumps({"elapsed_seconds": payload["metadata"]["elapsed_seconds"],
                      "metrics": {k: v["metrics"] for k, v in payload["baseline"]["outcomes"].items()}}, indent=2))
    return payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--baseline-only", action="store_true")
    parser.add_argument("--maximum-level", type=int, choices=LEVELS, default=9)
    args = parser.parse_args()
    run(workers=args.workers, baseline_only=args.baseline_only, maximum_level=args.maximum_level)
