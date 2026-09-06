"""Evidence-linked before/after figures for the atomic user pricing game."""
from __future__ import annotations

import hashlib
import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from experiments.plot_style import configure_times_new_roman
from experiments.run_user_provider_game import OUT, ROOT

FIG = ROOT / "figures/user_provider_game_20260906"
BEFORE, AFTER, RED, BLUE = "#83888D", "#167E7B", "#B05258", "#4C71A4"


def title(ax, letter, text):
    ax.set_title(f"{letter}  {text}", loc="left", fontsize=10, fontweight="bold", pad=9)
    ax.tick_params(length=3)


def save(fig, name, records):
    for suffix in ("pdf", "svg", "png"):
        path = FIG / f"{name}.{suffix}"
        fig.savefig(path, dpi=400, facecolor="white")
        records[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    plt.close(fig)


def bars(ax, values, labels, ylabel, *, digits=3, colors=(BEFORE, AFTER)):
    ax.bar([0, 1], values, width=0.54, color=colors)
    top = max(values)
    ax.set(xticks=[0, 1], xticklabels=labels, ylabel=ylabel, ylim=(0, top * 1.24 if top else 1))
    for i, value in enumerate(values):
        ax.text(i, value + top * .035, f"{value:.{digits}f}", ha="center", fontsize=10)


def same_prices(b, a, records):
    before, after = (b["outcomes"][key] for key in ("tou_initial", "tou_equilibrium"))
    bm, am = before["metrics"], after["metrics"]
    fig = plt.figure(figsize=(7.15, 5.5), layout="constrained")
    gs = fig.add_gridspec(2, 3, height_ratios=[1.25, 1], hspace=.12, wspace=.14)
    ax = fig.add_subplot(gs[0, :2])
    for rec, name, color, style in ((before, "Before: original schedule", BEFORE, "--"),
                                  (after, "After: user equilibrium", AFTER, "-")):
        ax.plot(range(1, 9), np.asarray(rec["counts"]).sum(axis=0), style, marker="o", ms=4, color=color, label=name)
    ax.set(xlabel="Execution period (3 h each)", ylabel="Expected total load", xticks=range(1, 9), ylim=(0, 72))
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.text(.98, .92, f"Expected peak\n59.00 to 53.06\n({a['same_prices_user_algorithm']['peak_reduction_percent']:.2f}% lower)",
            transform=ax.transAxes, ha="right", va="top", fontsize=9)
    title(ax, "a", "Load before and after user responses")
    ax = fig.add_subplot(gs[0, 2])
    bottom = np.zeros(2)
    for key, label, color in (("mean_bill", "Bill", "#AEB4BA"), ("mean_congestion_cost", "Congestion", BLUE),
                              ("mean_delay_cost", "Delay", "#D5AA64"), ("mean_switch_cost", "Switch", AFTER)):
        values = np.array([bm[key], am[key]])
        ax.bar([0, 1], values, bottom=bottom, color=color, width=.52, label=label)
        bottom += values
    ax.set(xticks=[0, 1], xticklabels=["Before", "After"], ylabel="Mean generalized cost", ylim=(0, 1.38))
    ax.legend(frameon=False, ncol=2, fontsize=7, loc="upper center", columnspacing=.7, handlelength=1)
    for i, v in enumerate(bottom):
        ax.text(i, v + .025, f"{v:.3f}", ha="center", fontsize=9)
    title(ax, "b", "Cost components")
    for k, key, label, text in ((0, "mean_utility", "Mean utility (absolute units)", "Utility: +0.0502"),
                               (1, "mean_bill", "Mean bill", "Bill: -6.52%"),
                               (2, "max_user_regret", "Expected maximum user regret", "No profitable user deviation")):
        ax = fig.add_subplot(gs[1, k])
        bars(ax, [bm[key], am[key]], ["Before", "After"], label)
        title(ax, "cde"[k], text)
    save(fig, "same_price_before_after", records)


def fair_comparison(b, a, records):
    u, d = (b["outcomes"][key]["metrics"] for key in ("uniform_equilibrium", "tou_equilibrium"))
    fig = plt.figure(figsize=(7.15, 5.4), layout="constrained")
    gs = fig.add_gridspec(2, 3, hspace=.18, wspace=.1)
    for k, key, label, heading in ((0, "mean_utility", "Mean utility", "User utility falls"),
                                  (1, "mean_bill", "Mean bill", "Bills rise by 13.66%"),
                                  (2, "market_profit", "Total manufacturer profit", "Manufacturers gain")):
        ax = fig.add_subplot(gs[0, k])
        bars(ax, [u[key], d[key]], ["Uniform", "TOU"], label, digits=3 if k < 2 else 2)
        title(ax, "abc"[k], heading)
    ax = fig.add_subplot(gs[1, :2])
    for key, label, color in (("same_prices_user_algorithm", "Same TOU prices: after - before", AFTER),
                              ("fair_tariff_comparison", "Both equilibria: TOU - uniform", RED)):
        values = np.sort(a[key]["per_user_expected_utility_change"])
        ax.plot(range(1, 241), values, color=color, lw=1.5, label=label)
    ax.axhline(0, color=BEFORE, lw=.7)
    ax.set(xlabel="User rank (sorted separately for each comparison)", ylabel="Expected utility change", xlim=(1, 240))
    ax.legend(frameon=False, fontsize=7.5, loc="upper left")
    title(ax, "d", "Individual gains do not follow the average")
    ax = fig.add_subplot(gs[1, 2])
    vals = a["replications"]["utility_changes"]
    ax.bar(range(5), vals, color=RED, width=.6)
    ax.axhline(0, color=BEFORE, lw=.7)
    ax.set(xticks=range(5), xticklabels=[str(s)[-2:] for s in a["replications"]["seeds"]],
           xlabel="Seed suffix (202609xx)", ylabel="Utility: TOU - uniform", ylim=(-.16, .015))
    title(ax, "e", "Five matched cohorts")
    save(fig, "fair_tariff_comparison", records)


def user_curves(b, a, records):
    rep = b["representative"]
    fig, axes = plt.subplots(1, 2, figsize=(7.15, 3.45), layout="constrained")
    examples = [rep["example_user"], a["time_switch_example"]]
    for idx, (ax, case) in enumerate(zip(axes, examples)):
        for curve in case["curves"]:
            for m, color in enumerate((BLUE, AFTER)):
                values = np.array([np.nan if v is None else v for v in curve["utility_by_action"]]).reshape(2, 8)[m]
                times = np.arange(1, 9)
                ax.plot(times, values, "--" if curve["state"] == "before" else "-", color=color, marker="o", ms=4,
                        label=f"{'AB'[m]}, {curve['state']}")
        for state, marker, color in (("before", "s", BEFORE), ("after", "*", RED)):
            action = case[f"{state}_action"]
            value = rep[state]["utility"][case["id"]]
            ax.scatter(action % 8 + 1, value, marker=marker, color=color, s=85 if state == "after" else 44,
                       zorder=5, label=f"Chosen {state}")
        gain = rep["after"]["utility"][case["id"]] - rep["before"]["utility"][case["id"]]
        ax.set(xlabel="Feasible execution period", ylabel="Prospective individual utility",
               xticks=range(case["release"] + 1, case["deadline"] + 2),
               xlim=(case["release"] + .85, case["deadline"] + 1.15))
        ax.margins(y=.18)
        title(ax, "ab"[idx], f"User {case['id']}: final - initial = {gain:+.4f}")
        ax.legend(frameon=False, fontsize=7.5, ncol=2, loc="upper center", bbox_to_anchor=(.5, -.23))
    save(fig, "individual_time_choices", records)


def convergence(b, records):
    trace = b["representative"]["trace"]
    fig, axes = plt.subplots(1, 3, figsize=(7.15, 2.65), layout="constrained")
    for ax, key, letter, heading, ylabel in zip(axes,
            ("potential", "max_user_regret", "mean_utility"), "abc",
            ("Exact potential decreases", "User deviations vanish", "Mean utility is not monotone"),
            ("Potential", "Maximum user regret", "Mean utility")):
        ax.plot([r["sweep"] for r in trace], [r[key] for r in trace], color=AFTER, marker="o", ms=4)
        ax.set(xlabel="Completed response sweep", ylabel=ylabel, xticks=[0, 2, 4, 6])
        title(ax, letter, heading)
    save(fig, "user_convergence", records)


def provider_times(b, records):
    fig, axes = plt.subplots(2, 2, figsize=(7.15, 4.65), layout="constrained")
    for m in range(2):
        for row, field, ylabel in ((0, "counts", "Expected task load"), (1, "qos", "Expected resource QoS")):
            ax = axes[row, m]
            for key, label, color, style in (("tou_initial", "Before", BEFORE, "--"),
                                             ("tou_equilibrium", "After", AFTER, "-")):
                ax.plot(range(1, 9), b["outcomes"][key][field][m], style, marker="o", ms=4, color=color, label=label)
            ax.set(xticks=range(1, 9), xlabel="Period", ylabel=ylabel)
            if row == 0:
                ax.axhline(b["configuration"]["capacities"][m], ls=":", color=RED, lw=1, label="Reference capacity")
                ax.set_ylim(0, 50)
                ax.legend(frameon=False, fontsize=8)
            else:
                ax.set_ylim(.70, 1.025)
            title(ax, "abcd"[row * 2 + m], f"Manufacturer {'AB'[m]}")
    save(fig, "provider_load_quality", records)


def main():
    configure_times_new_roman(9)
    plt.rcParams.update({"axes.labelsize": 9, "xtick.labelsize": 8, "ytick.labelsize": 8})
    data = json.loads((OUT / "experiment.json").read_text())
    analysis = json.loads((OUT / "analysis.json").read_text())
    if analysis["experiment_sha256"] != hashlib.sha256((OUT / "experiment.json").read_bytes()).hexdigest():
        raise ValueError("analysis is not bound to the current experiment")
    FIG.mkdir(parents=True, exist_ok=True)
    records = {}
    same_prices(data["baseline"], analysis, records)
    fair_comparison(data["baseline"], analysis, records)
    user_curves(data["baseline"], analysis, records)
    convergence(data["baseline"], records)
    provider_times(data["baseline"], records)
    manifest = {"experiment_sha256": analysis["experiment_sha256"],
                "analysis_sha256": hashlib.sha256((OUT / "analysis.json").read_bytes()).hexdigest(),
                "script_sha256": hashlib.sha256((ROOT / "experiments/plot_user_provider_game.py").read_bytes()).hexdigest(),
                "figures_sha256": records, "dpi": 400,
                "statistics": "Exact expectations over independent manufacturer mixed strategies; no sampling error bars.",
                "peak_note": "Expected maximum load is not maximum expected load; manuscript reports the former."}
    (FIG / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Exported {len(records)} files to {FIG}")


if __name__ == "__main__":
    main()
