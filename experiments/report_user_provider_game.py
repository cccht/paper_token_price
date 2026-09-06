"""Summarize matched price-game comparisons and export their source data."""
from __future__ import annotations

import csv
import hashlib
import json

import numpy as np

from experiments.run_user_provider_game import OUT, ROOT
from experiments.user_provider_experiment_tools import json_ready
from pricing_sim.user_time_game import UserGameConfig, UserPopulation, prospective_costs


def comparison(before, after):
    differences = {key: after["metrics"][key] - before["metrics"][key] for key in before["metrics"]}
    utility = np.asarray(after["utility"]) - np.asarray(before["utility"])
    return {"differences": differences,
            "cost_reduction_percent": 100 * (1 - after["metrics"]["mean_generalized_cost"] / before["metrics"]["mean_generalized_cost"]),
            "bill_reduction_percent": 100 * (1 - after["metrics"]["mean_bill"] / before["metrics"]["mean_bill"]),
            "peak_reduction_percent": 100 * (1 - after["metrics"]["peak_load"] / before["metrics"]["peak_load"]),
            "higher_expected_utility_fraction": float(np.mean(utility > 1e-8)),
            "lower_expected_utility_fraction": float(np.mean(utility < -1e-8)),
            "unchanged_expected_utility_fraction": float(np.mean(np.abs(utility) <= 1e-8)),
            "per_user_expected_utility_change": utility.tolist()}


def time_switch_example(baseline):
    rep = baseline["representative"]
    config = UserGameConfig(**baseline["configuration"])
    users = UserPopulation(**{key: np.asarray(value) if value is not None else None for key, value in baseline["population"].items()})
    before, after = np.asarray(rep["before"]["actions"]), np.asarray(rep["after"]["actions"])
    candidates = np.flatnonzero(before % config.periods != after % config.periods)
    if not len(candidates):
        return None
    player = int(candidates[0])
    curves = []
    for name in ("before", "after"):
        state = rep[name]
        costs = prospective_costs(player, current=int(state["actions"][player]), counts=np.asarray(state["counts"]).ravel(),
                                  prices=np.asarray(rep["prices"]), users=users, config=config)
        utility = users.values[player] - costs
        curves.append({"state": name, "utility_by_action": [float(v) if np.isfinite(v) else None for v in utility]})
    return {"id": player, "selection": "additional post-hoc mechanism example: smallest index among time switchers; no utility-gain filter",
            "release": int(users.release[player]), "deadline": int(users.deadline[player]),
            "before_action": int(before[player]), "after_action": int(after[player]), "curves": curves,
            "utility_before": rep["before"]["utility"][player], "utility_after": rep["after"]["utility"][player]}


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_tables(data):
    b = data["baseline"]
    rows = []
    fields = (("Mean utility", "mean_utility", 4), ("Generalized cost", "mean_generalized_cost", 4),
              ("Mean bill", "mean_bill", 4), ("Mean delay cost", "mean_delay_cost", 4),
              ("Mean switching cost", "mean_switch_cost", 4), ("Mean congestion cost", "mean_congestion_cost", 4),
              ("Expected peak load", "peak_load", 2), ("Mean user QoS", "mean_qos", 4),
              ("Expected minimum user QoS", "minimum_qos", 4), ("Mean delay (hours)", "mean_delay_hours", 4),
              ("Mean flexible delay (hours)", "mean_flexible_delay_hours", 4),
              ("Time-shift fraction", "shifted_fraction", 4), ("Provider-switch fraction", "provider_switch_fraction", 4),
              ("Manufacturer A profit", "provider_A_profit", 2), ("Manufacturer B profit", "provider_B_profit", 2),
              ("Total manufacturer profit", "market_profit", 2), ("Expected max. user regret", "max_user_regret", 4))
    for label, key, digits in fields:
        values = [b["outcomes"][stage]["metrics"][key] for stage in ("tou_initial", "tou_equilibrium", "uniform_equilibrium")]
        rows.append(label + " & " + " & ".join(f"{v:.{digits}f}" for v in values) + r" \\")
    (OUT / "main_table.tex").write_text("\n".join(rows) + "\n")
    rows = []
    for level in b["menus"]:
        u, d = level["uniform"], level["dynamic"]
        regret = d.get("deviation_on_final_menu", {"absolute": d["provider_regret"]})["absolute"]
        rows.append(f"{level['axis_count']} & {u['rule_count']} / {d['rule_count']} & "
                    f"{u['expected_metrics']['mean_utility']:.4f} & {d['expected_metrics']['mean_utility']:.4f} & "
                    f"{regret[0]:.4f} & {regret[1]:.4f}" + r" \\")
    (OUT / "menu_table.tex").write_text("\n".join(rows) + "\n")
    rows = []
    for case in [{"name": "Baseline", **b["menus"][-1]}, *data["boundary_cases"], *data["replications"]]:
        u, d = (case[key]["expected_metrics"] for key in ("uniform", "dynamic"))
        name = case["name"].replace("_", r"\_")
        rows.append(f"{name} & {u['mean_utility']:.4f} & {d['mean_utility']:.4f} & "
                    f"{d['mean_utility'] - u['mean_utility']:+.4f} & {u['peak_load']:.2f} & {d['peak_load']:.2f}" + r" \\")
    (OUT / "boundary_table.tex").write_text("\n".join(rows) + "\n")
    rows = []
    for name, game in (("Uniform", b["menus"][-1]["uniform"]), ("TOU", b["menus"][-1]["dynamic"])):
        for m, mix in enumerate((game["row_mix"], game["col_mix"])):
            for i, weight in enumerate(mix):
                if weight > 0:
                    rule = game["rules"][i]
                    rows.append(f"{name} & {'AB'[m]} & {i} & {rule['base']:.3f} & {rule['slope']:.3f} & {weight:.6f}" + r" \\")
    (OUT / "price_support_table.tex").write_text("\n".join(rows) + "\n")


def main():
    path = OUT / "experiment.json"
    data = json.loads(path.read_text())
    if not data["metadata"].get("complete") or data["metadata"]["baseline_only"]:
        raise ValueError("the full predefined experiment must finish before reporting")
    for file, digest in data["metadata"]["source_sha256"].items():
        if hashlib.sha256((ROOT / file).read_bytes()).hexdigest() != digest:
            raise ValueError(f"experiment source changed: {file}")
    b, outcomes = data["baseline"], data["baseline"]["outcomes"]
    analysis = {
        "experiment_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "same_prices_user_algorithm": comparison(outcomes["tou_initial"], outcomes["tou_equilibrium"]),
        "uniform_user_algorithm": comparison(outcomes["uniform_initial"], outcomes["uniform_equilibrium"]),
        "fair_tariff_comparison": comparison(outcomes["uniform_equilibrium"], outcomes["tou_equilibrium"]),
        "fixed_mean_comparison": comparison(b["mean_price_control"]["uniform"], b["mean_price_control"]["dynamic"]),
        "time_switch_example": time_switch_example(b),
        "scope": "Within-price best-response convergence and cross-regime welfare are different comparisons",
    }
    repetitions = [b["menus"][-1], *data["replications"]]
    gains = [case["dynamic"]["expected_metrics"]["mean_utility"] - case["uniform"]["expected_metrics"]["mean_utility"] for case in repetitions]
    analysis["replications"] = {"seeds": list(range(20260906, 20260911)), "utility_changes": gains,
                                "mean_change": float(np.mean(gains)), "minimum_change": min(gains), "maximum_change": max(gains),
                                "positive_count": sum(v > 0 for v in gains)}
    (OUT / "analysis.json").write_text(json.dumps(json_ready(analysis), indent=2, allow_nan=False) + "\n")
    write_csv(OUT / "outcomes.csv", [{"stage": name, **record["metrics"]} for name, record in outcomes.items()])
    users = b["population"]
    user_rows = []
    for i in range(len(users["release"])):
        user_rows.append({"id": i, "release_period": users["release"][i] + 1, "deadline_period": users["deadline"][i] + 1,
                          "flexible": users["flexible"][i],
                          **{f"{stage}_{key}": outcomes[stage][key][i] for stage in outcomes for key in ("utility", "bill", "delay_hours", "congestion_cost")}})
    write_csv(OUT / "user_outcomes.csv", user_rows)
    period_rows = []
    for stage, record in outcomes.items():
        for m in range(2):
            for t in range(8):
                period_rows.append({"stage": stage, "provider": "AB"[m], "period": t + 1, "expected_load": record["counts"][m][t],
                                    "expected_price": record["prices"][m][t], "expected_qos": record["qos"][m][t]})
    write_csv(OUT / "period_outcomes.csv", period_rows)
    write_csv(OUT / "convergence.csv", b["representative"]["trace"])
    boundary_rows = []
    for case in [{"name": "baseline", **b["menus"][-1]}, *data["boundary_cases"], *data["replications"]]:
        u, d = (case[key]["expected_metrics"] for key in ("uniform", "dynamic"))
        boundary_rows.append({"case": case.get("name", "baseline"), "uniform_utility": u["mean_utility"],
                              "tou_utility": d["mean_utility"], "utility_change": d["mean_utility"] - u["mean_utility"],
                              "uniform_peak": u["peak_load"], "tou_peak": d["peak_load"],
                              "uniform_profit": u["market_profit"], "tou_profit": d["market_profit"],
                              "provider_regret": max(*case["uniform"]["provider_regret"], *case["dynamic"]["provider_regret"]),
                              "user_regret": max(case["uniform"]["maximum_offpath_user_regret"], case["dynamic"]["maximum_offpath_user_regret"])})
    write_csv(OUT / "boundary_cases.csv", boundary_rows)
    write_tables(data)
    print(json.dumps({key: value for key, value in analysis.items() if key not in ("time_switch_example",)
                      and not isinstance(value, dict)}, indent=2))
    print(json.dumps({key: {k: v for k, v in value.items() if k != "per_user_expected_utility_change"}
                      for key, value in analysis.items() if key in ("same_prices_user_algorithm", "fair_tariff_comparison", "replications")}, indent=2))


if __name__ == "__main__":
    main()
