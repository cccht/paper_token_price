"""Build SMPT submission figures from provenance-linked final artifacts."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from experiments.plot_style import (
    SCI_PALETTE,
    configure_times_new_roman,
    plot_end_user_prices as _plot_end_user_prices,
)
from experiments.build_submission_sensitivity_table import SCENARIO_ORDER

ROOT = Path(__file__).resolve().parent.parent
ARTIFACT = ROOT / "artifacts" / "peak_shaving" / "20260712_expanded_response"
CALIBRATION_ARTIFACT = ROOT / "artifacts" / "peak_shaving" / "20260712_final"
BURST = ROOT / "data" / "processed" / "burstgpt_d895a53b_8period"
FIGURE_DIR = ROOT / "figures" / "peak_shaving_final_20260714"
EQUILIBRIUM_PATH = ARTIFACT / "spatiotemporal_equilibrium_submission.json"
UNIFORM_OFFGRID_PATH = ARTIFACT / "uniform_offgrid_sensitivity_submission.json"
INTERMEDIARY_PAYOFF_SENSITIVITY_PATH = (
    ARTIFACT / "intermediary_payoff_sensitivity_submission.json"
)
FIGURE_STEMS = ("input_calibration", "equilibrium_profiles", "mechanism_decomposition", "resolved_sensitivity", "solver_diagnostics")
PRIMARY = SCI_PALETTE["primary"]
SECONDARY = SCI_PALETTE["secondary"]
CONTRAST = SCI_PALETTE["contrast"]
NEUTRAL = SCI_PALETTE["neutral"]
LIGHT = SCI_PALETTE["light"]
MECHANISM_COLORS = (PRIMARY, SECONDARY, CONTRAST)
SENSITIVITY_COLORS = (NEUTRAL, PRIMARY, CONTRAST)
SENSITIVITY_FACTOR_LABELS = (
    "Baseline",
    "$G$",
    "$\\alpha$",
    "$\\kappa$",
    "$\\bar{u}$",
)
QOS_CI95_SCALE = 2.7764451051977987 / 1.96
def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_linked_json(path: Path, equilibrium_path: Path) -> dict:
    data = _read_json(path)
    metadata = data.get("metadata", {})
    recorded = metadata.get("equilibrium_sha256", metadata.get("baseline_sha256"))
    expected = _sha256(equilibrium_path)
    if recorded != expected:
        raise ValueError(
            f"{path.name} equilibrium SHA-256 {recorded!r} does not match {expected}"
        )
    return data


def _submission_artifact(name: str) -> dict:
    return _read_linked_json(ARTIFACT / name, EQUILIBRIUM_PATH)


def _read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def load_final_data() -> dict:
    equilibrium = _read_json(EQUILIBRIUM_PATH)
    return {
        "burst_profile": _read_csv(BURST / "burstgpt_8period_load_profile.csv"),
        "qos_calibration": _read_json(CALIBRATION_ARTIFACT / "qos_calibration.json"),
        "equilibrium": equilibrium,
        "distribution": _submission_artifact("mixed_outcome_distribution_submission.json"),
        "mechanism": _submission_artifact("mechanism_decomposition_submission.json"),
        "sensitivity": _submission_artifact("spatiotemporal_sensitivity_submission.json"),
        "offgrid": _submission_artifact("spatiotemporal_offgrid_diagnostic_submission.json"),
        "uniform_offgrid": _read_linked_json(
            UNIFORM_OFFGRID_PATH, EQUILIBRIUM_PATH
        ),
        "fixed_point_audit": _submission_artifact("fixed_point_multistart_audit_submission.json"),
        "intermediary_audit": _submission_artifact("intermediary_globality_audit_submission.json"),
        "intermediary_payoff_sensitivity": _read_linked_json(
            INTERMEDIARY_PAYOFF_SENSITIVITY_PATH, EQUILIBRIUM_PATH
        ),
    }


def _panel_label(ax, label: str, title: str, y: float = -0.28) -> None:
    ax.text(0.5, y, f"({label}) {title}", transform=ax.transAxes,
            ha="center", va="top", fontsize=8.5)


def _finish(fig, output_dir: Path, stem: str) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf = output_dir / f"{stem}.pdf"
    png = output_dir / f"{stem}.png"
    fig.savefig(pdf)
    fig.savefig(png, dpi=360)
    plt.close(fig)
    return [pdf, png]


def _input_calibration(data: dict, output_dir: Path) -> list[Path]:
    profile = data["burst_profile"]
    calibration = data["qos_calibration"]
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.75))
    periods = np.arange(1, 9)
    share = np.array([float(row["token_share_mean"]) for row in profile])
    std = np.array([float(row["token_share_std"]) for row in profile])
    axes[0].bar(periods, share, color=LIGHT, edgecolor=PRIMARY, linewidth=0.6,
                yerr=std, capsize=2, error_kw={"elinewidth": 0.7})
    axes[0].set(xlabel="Three-hour period", ylabel="Daily token share")
    axes[0].set_xticks(periods)
    axes[0].set_ylim(0, max(share + std) * 1.12)
    axes[0].grid(axis="y", alpha=0.18)
    _panel_label(axes[0], "a", "BurstGPT daily load shape")
    points = calibration["points"]
    series = {"vllm-0.5b": (SECONDARY, "Qwen2.5-0.5B"), "vllm-3b": (CONTRAST, "Qwen2.5-3B")}
    for profile_name, (color, label) in series.items():
        rows = [row for row in points if row["profile"] == profile_name]
        x = np.array([row["normalized_utilization"] for row in rows])
        y = np.array([row["observed_qos"] for row in rows])
        error = QOS_CI95_SCALE * np.array([row["observed_qos_ci95"] for row in rows])
        axes[1].errorbar(x, y, yerr=error, fmt="o", ms=4, color=color,
                         capsize=2, linewidth=0.8, label=label)
    fit = calibration["pooled_fit"]
    grid = np.linspace(0.1, 2.35, 240)
    fitted = np.exp(-fit["strength"] * np.maximum(grid - fit["threshold"], 0) ** 2)
    axes[1].plot(grid, fitted, color=PRIMARY, lw=1.8, label="Pooled fit")
    axes[1].axvline(1.0, color=NEUTRAL, ls="--", lw=0.9)
    axes[1].set(xlabel="Normalized concurrency", ylabel="TTFT SLA rate", ylim=(0.38, 1.03))
    axes[1].legend(frameon=False, fontsize=7, loc="lower left")
    axes[1].grid(alpha=0.18)
    _panel_label(axes[1], "b", "Measured QoS and pooled fit")
    fig.tight_layout(w_pad=2.1, rect=(0, 0.08, 1, 1))
    return _finish(fig, output_dir, "input_calibration")


def _equilibrium_profiles(data: dict, output_dir: Path) -> list[Path]:
    equilibrium = data["equilibrium"]
    uniform = equilibrium["uniform"]["expected_profiles"]
    dynamic = equilibrium["dynamic"]["expected_profiles"]
    periods = np.arange(1, 9)
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 5.6))
    axes = axes.ravel()
    axes[0].plot(periods, uniform["aggregate_load"], "o--", color=NEUTRAL, label="Uniform")
    axes[0].plot(periods, dynamic["aggregate_load"], "o-", color=PRIMARY, label="Dynamic")
    axes[0].set(xlabel="Period", ylabel="Aggregate load")
    axes[0].legend(frameon=False, fontsize=7, loc="lower center",
                   bbox_to_anchor=(0.5, 1.01), ncol=2)
    axes[0].grid(alpha=0.18)
    _plot_end_user_prices(axes[1], periods, uniform, dynamic)
    for provider, color in enumerate((PRIMARY, CONTRAST)):
        label = "Provider A" if provider == 0 else "Provider B"
        axes[2].plot(periods, uniform["provider_utilization"][provider], "--", color=color,
                     lw=1.2, label=f"{label}, uniform")
        axes[2].plot(periods, dynamic["provider_utilization"][provider], "-", color=color,
                     lw=1.8, label=f"{label}, dynamic")
    axes[2].axhline(1.0, color=NEUTRAL, ls=":", lw=0.9)
    axes[2].set(xlabel="Period", ylabel="Provider utilization")
    axes[2].legend(frameon=False, fontsize=6.2, loc="lower center",
                   bbox_to_anchor=(0.5, 1.01), ncol=2)
    axes[2].grid(alpha=0.18)
    for provider, color in enumerate((PRIMARY, CONTRAST)):
        label = "Provider A" if provider == 0 else "Provider B"
        axes[3].plot(periods, uniform["provider_qos"][provider], "--", color=color,
                     lw=1.2, label=f"{label}, uniform")
        axes[3].plot(periods, dynamic["provider_qos"][provider], "-", color=color,
                     lw=1.8, label=f"{label}, dynamic")
    axes[3].set(xlabel="Period", ylabel="TTFT SLA proxy", ylim=(0.82, 1.01))
    axes[3].legend(frameon=False, fontsize=6.2, loc="lower center",
                   bbox_to_anchor=(0.5, 1.01), ncol=2)
    axes[3].grid(alpha=0.18)
    titles = ("Aggregate demand", "End-user prices", "Capacity use", "Provider QoS")
    fig.tight_layout(h_pad=3.8, w_pad=1.6, rect=(0, 0.13, 1, 0.94))
    for ax, label, title in zip(axes, "abcd", titles):
        _panel_label(ax, label, title, y=-0.47)
    return _finish(fig, output_dir, "equilibrium_profiles")


def _mechanism_decomposition(data: dict, output_dir: Path) -> list[Path]:
    rows = data["mechanism"]["policy_comparisons"]
    order = ("temporal_only", "spatial_only", "combined")
    rows = [next(row for row in rows if row["mechanism"] == item) for item in order]
    labels = ["Temporal", "Spatial", "Combined"]
    colors = MECHANISM_COLORS
    metrics = (
        ("aggregate_peak_load_change_percent", "Aggregate peak change (%)", "a"),
        ("maximum_provider_utilization_change_percent", "Max. utilization change (%)", "b"),
        ("minimum_provider_qos_change", "Minimum QoS change", "c"),
    )
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 3.0))
    for ax, (metric, ylabel, label) in zip(axes, metrics):
        values = [row[metric] for row in rows]
        bars = ax.bar(labels, values, color=colors, edgecolor="white", linewidth=0.5)
        ax.axhline(0, color=NEUTRAL, lw=0.8)
        ax.set_ylabel(ylabel)
        ax.tick_params(axis="x", labelrotation=18, labelsize=7.5)
        ax.grid(axis="y", alpha=0.18)
        offset = max(max(abs(np.asarray(values))), 0.01) * 0.05
        for bar, value in zip(bars, values):
            if value < 0:
                y, color, va = value + offset, "white", "bottom"
            else:
                y, color, va = value + offset, "#191919", "bottom"
            ax.text(bar.get_x() + bar.get_width() / 2, y, f"{value:.3f}",
                    ha="center", va=va, fontsize=7, color=color)
        _panel_label(ax, label, ylabel, y=-0.34)
    fig.tight_layout(w_pad=1.5, rect=(0, 0.12, 1, 1))
    return _finish(fig, output_dir, "mechanism_decomposition")


def _resolved_sensitivity(data: dict, output_dir: Path) -> list[Path]:
    rows = data["sensitivity"]["rows"]
    if tuple(row.get("scenario") for row in rows) != SCENARIO_ORDER:
        raise ValueError("sensitivity scenario order is invalid")
    panels = (
        ("aggregate_peak_change_percent", "Aggregate peak change (%)", "a"),
        ("maximum_provider_utilization_change_percent", "Max. utilization change (%)", "b"),
        ("minimum_provider_qos_change", "Minimum QoS change", "c"),
        ("market_profit_change_percent", "Market-side profit change (%)", "d"),
    )
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 5.45))
    positions = np.arange(len(SENSITIVITY_FACTOR_LABELS))
    pair_width = 0.3
    lower_rows = rows[1::2]
    higher_rows = rows[2::2]
    for ax, (metric, ylabel, label) in zip(axes.ravel(), panels):
        ax.bar(
            positions[0],
            rows[0][metric],
            color=SENSITIVITY_COLORS[0],
            width=0.58,
            label="Baseline",
        )
        ax.bar(
            positions[1:] - pair_width / 2,
            [row[metric] for row in lower_rows],
            color=SENSITIVITY_COLORS[1],
            width=pair_width,
            label="Lower",
        )
        ax.bar(
            positions[1:] + pair_width / 2,
            [row[metric] for row in higher_rows],
            color=SENSITIVITY_COLORS[2],
            width=pair_width,
            label="Higher",
        )
        ax.axhline(0, color=NEUTRAL, lw=0.8)
        ax.set_ylabel(ylabel)
        ax.set_xticks(
            positions,
            SENSITIVITY_FACTOR_LABELS,
            rotation=0,
            ha="center",
            fontsize=7,
        )
        ax.grid(axis="y", alpha=0.18)
        ax.legend(
            frameon=False,
            fontsize=6.2,
            loc="lower center",
            bbox_to_anchor=(0.5, 1.01),
            ncol=3,
            handlelength=1.2,
            columnspacing=0.8,
        )
        _panel_label(ax, label, ylabel, y=-0.23)
    fig.tight_layout(h_pad=3.1, w_pad=1.8, rect=(0, 0.05, 1, 0.98))
    return _finish(fig, output_dir, "resolved_sensitivity")


def _solver_diagnostics(data: dict, output_dir: Path) -> list[Path]:
    equilibrium = data["equilibrium"]
    offgrid = data["offgrid"]
    uniform_offgrid = data["uniform_offgrid"]
    fixed_point = data["fixed_point_audit"]
    intermediary = data["intermediary_audit"]
    payoff_sensitivity = data["intermediary_payoff_sensitivity"]
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.55))
    for game_name, color in (("uniform", NEUTRAL), ("dynamic", PRIMARY)):
        trace = equilibrium[game_name]["trace"]
        axes[0].semilogy(
            [row["oracle_round"] for row in trace],
            [max(row["full_max_regret"], 1e-14) for row in trace],
            "o-", color=color, label=game_name.capitalize(),
        )
    axes[0].set(xlabel="Double-oracle round", ylabel="Full-candidate regret")
    axes[0].set_xticks(range(1, 1 + len(equilibrium["dynamic"]["trace"])))
    axes[0].legend(frameon=False, fontsize=7)
    axes[0].grid(alpha=0.18)
    dynamic_regrets = [
        100.0 * offgrid["players"][player]["relative_offgrid_regret"]
        for player in ("firm_A", "firm_B")
    ]
    uniform_regrets = [
        100.0
        * max(
            scenario["players"][player]["relative_offgrid_regret"]
            for scenario in uniform_offgrid["scenarios"]
        )
        for player in ("firm_A", "firm_B")
    ]
    axes[1].bar(
        np.arange(4),
        [*uniform_regrets, *dynamic_regrets],
        color=(SECONDARY, LIGHT, PRIMARY, CONTRAST),
    )
    axes[1].axhline(0.5, color=NEUTRAL, ls="--", lw=0.9, label="0.5% gate")
    axes[1].set(ylabel="Relative off-grid regret (%)")
    axes[1].set_xticks(
        np.arange(4), ["U-A", "U-B", "D-A", "D-B"], fontsize=6.7
    )
    axes[1].legend(frameon=False, fontsize=7)
    axes[1].grid(axis="y", alpha=0.18)
    gate_ratios = [
        fixed_point["maximum_residual"] / 1e-8,
        fixed_point["maximum_qos_span"] / 1e-7,
        fixed_point["maximum_routing_span"] / 1e-7,
        intermediary["maximum_relative_profit_improvement"] / 1e-3,
        payoff_sensitivity["summary"]["maximum_joint_residual"] / 1e-8,
    ]
    axes[2].bar(
        np.arange(5),
        gate_ratios,
        color=(PRIMARY, SECONDARY, LIGHT, CONTRAST, NEUTRAL),
    )
    axes[2].axhline(1.0, color=NEUTRAL, ls="--", lw=0.9, label="Gate")
    axes[2].set_yscale("log")
    axes[2].set(ylabel="Value / audit gate")
    axes[2].set_xticks(
        np.arange(5),
        ["Residual", "QoS span", "Route span", "Follower gain", "Payoff FP"],
        rotation=24, ha="right", fontsize=6.7,
    )
    axes[2].legend(frameon=False, fontsize=7)
    axes[2].grid(axis="y", alpha=0.18)
    fig.subplots_adjust(left=0.08, right=0.99, top=0.96, bottom=0.34, wspace=0.55)
    titles = ("Finite-candidate convergence", "Independent bounded deviations", "Fixed-point and follower checks")
    for x, label, title in zip((0.18, 0.52, 0.85), "abc", titles):
        fig.text(x, 0.045, f"({label}) {title}", ha="center", va="bottom", fontsize=8.5)
    return _finish(fig, output_dir, "solver_diagnostics")

def build_all_figures(*, output_dir: Path = FIGURE_DIR, data: dict | None = None) -> list[Path]:
    configure_times_new_roman(font_size=8.5)
    values = load_final_data() if data is None else data
    paths = []
    for builder in (
        _input_calibration,
        _equilibrium_profiles,
        _mechanism_decomposition,
        _resolved_sensitivity,
        _solver_diagnostics,
    ):
        paths.extend(builder(values, output_dir))
    return paths


def main() -> None:
    paths = build_all_figures()
    print(json.dumps({"outputs": [str(path.relative_to(ROOT)) for path in paths]}))


if __name__ == "__main__":
    main()
