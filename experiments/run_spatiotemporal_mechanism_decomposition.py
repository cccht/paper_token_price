"""Controlled temporal-versus-spatial mechanism decomposition."""
from __future__ import annotations

import argparse
import csv
from datetime import datetime
import hashlib
import json
from pathlib import Path
import platform
import subprocess

import numpy as np

from pricing_sim.peak_shaving_config import PeakShavingConfig
from pricing_sim.peak_shaving_equilibrium import expand_policy_price
from pricing_sim.spatiotemporal_mechanism import (
    DemandResponseSpec,
    solve_spatiotemporal_qos_fixed_point,
    summarize_spatiotemporal_result,
)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "artifacts" / "peak_shaving" / "20260712_route_c"
BURST_DIR = ROOT / "data" / "processed" / "burstgpt_d895a53b_8period"
BURST_PROFILE = BURST_DIR / "burstgpt_8period_load_profile.csv"
BURST_METADATA = BURST_DIR / "burstgpt_8period_load_metadata.json"
BURST_BUILDER = ROOT / "experiments" / "build_burstgpt_load_anchor.py"
FIXED_CHANNEL_SHARES = np.array([0.12, 0.50, 0.38])
MECHANISMS = {
    "neither": {"temporal_enabled": False, "spatial_enabled": False},
    "temporal_only": {"temporal_enabled": True, "spatial_enabled": False},
    "spatial_only": {"temporal_enabled": False, "spatial_enabled": True},
    "combined": {"temporal_enabled": True, "spatial_enabled": True},
}


def controlled_config(*, load_shape: np.ndarray | None = None) -> PeakShavingConfig:
    overrides = {
        "firm_capacity": np.array([300.0, 120.0]),
        "pop_rigid": 0.4,
        "pop_elastic": 0.6,
    }
    if load_shape is not None:
        overrides["load_shape_hat"] = np.asarray(load_shape, dtype=float)
    return PeakShavingConfig.default().evolve(
        **overrides,
    )


def controlled_demand_spec(
    config: PeakShavingConfig,
    *,
    native_profile: np.ndarray | None = None,
) -> DemandResponseSpec:
    total_mass = 1100.0
    if native_profile is None:
        profiles = np.vstack([config.native_rigid, config.native_elastic])
    else:
        profile = np.asarray(native_profile, dtype=float)
        profile = profile / np.sum(profile)
        profiles = np.vstack([profile, profile])
    native = total_mass * np.array([config.pop_rigid, config.pop_elastic])[:, None] * profiles
    return DemandResponseSpec(
        native_demand=native,
        price_sensitivity=np.array([2.0, 5.0]),
        flexible_fraction=np.array([0.0, 0.8]),
        migration_cost=np.array([2.0, 0.35]),
        max_shift=np.array([0, 2]),
        channel_brand=np.array([1.05, 1.0, 1.0]),
        qos_weight=1.0,
    )


def _channel_price(config: PeakShavingConfig, base: float, mode: str) -> np.ndarray:
    return expand_policy_price(
        base, 0.2, config, lower=config.price_lower,
        upper=config.price_upper, mode=mode,
    )


def controlled_policies(config: PeakShavingConfig) -> dict[str, np.ndarray]:
    bases = (1.10, 0.72, 0.72)
    uniform = np.vstack([_channel_price(config, base, "uniform") for base in bases])
    symmetric = np.vstack([_channel_price(config, base, "symmetric") for base in bases])
    asymmetric = np.vstack([
        _channel_price(config, bases[0], "symmetric"),
        _channel_price(config, bases[1], "reverse_diagnostic"),
        _channel_price(config, bases[2], "symmetric"),
    ])
    return {
        "uniform": uniform,
        "symmetric_tou": symmetric,
        "asymmetric_capacity_balance": asymmetric,
    }


def load_burstgpt_profile() -> tuple[np.ndarray, np.ndarray]:
    with BURST_PROFILE.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    token_share = np.array([float(row["token_share_mean"]) for row in rows])
    load_shape = np.array([float(row["normalized_token_load"]) for row in rows])
    if token_share.shape != (8,) or not np.isclose(np.sum(token_share), 1.0):
        raise ValueError("BurstGPT profile must contain eight normalized periods")
    return token_share, load_shape


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_output(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    )
    return completed.stdout.strip()


def build_manifest(
    config: PeakShavingConfig,
    *,
    data_source: str,
    load_source: str,
    extra_sources: tuple[Path, ...] = (),
) -> dict:
    sources = [
        ROOT / "pricing_sim/peak_shaving_config.py",
        ROOT / "pricing_sim/peak_shaving_market.py",
        ROOT / "pricing_sim/peak_shaving_equilibrium.py",
        ROOT / "pricing_sim/spatiotemporal_mechanism.py",
        Path(__file__).resolve(),
        *extra_sources,
    ]
    return {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "evidence_level": "controlled_prototype",
        "data_source": data_source,
        "git_commit": _git_output("rev-parse", "HEAD"),
        "git_dirty": bool(_git_output("status", "--porcelain")),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "command": (
            "uv run --no-project --with numpy --with scipy python -m "
            "experiments.run_spatiotemporal_mechanism_decomposition "
            f"--load-source {load_source}"
        ),
        "model_config": {
            "capacity": config.firm_capacity.tolist(),
            "qos_shape": "sigmoid",
            "qos_threshold": config.qos_threshold,
            "qos_feedback_weight": config.qos_feedback_weight,
            "period_hours": config.period_hours,
            "load_shape_hat": config.load_shape_hat.tolist(),
        },
        "source_sha256": {str(path.relative_to(ROOT)): _sha256(path) for path in sources},
    }


def _add_policy_deltas(rows: list[dict]) -> None:
    for policy in {row["policy"] for row in rows}:
        baseline = next(
            row for row in rows
            if row["policy"] == policy and row["mechanism"] == "neither"
        )
        for row in rows:
            if row["policy"] != policy:
                continue
            row["aggregate_peak_change_vs_neither"] = (
                row["aggregate_peak_load"] - baseline["aggregate_peak_load"]
            )
            row["provider_peak_change_vs_neither"] = (
                row["maximum_provider_utilization"]
                - baseline["maximum_provider_utilization"]
            )
            row["minimum_qos_change_vs_neither"] = (
                row["minimum_provider_qos"] - baseline["minimum_provider_qos"]
            )


def run_decomposition(*, load_source: str = "synthetic") -> dict:
    if load_source == "synthetic":
        config = controlled_config()
        spec = controlled_demand_spec(config)
        data_source = "synthetic conserved native demand"
        extra_sources: tuple[Path, ...] = ()
    elif load_source == "burstgpt":
        native_profile, load_shape = load_burstgpt_profile()
        config = controlled_config(load_shape=load_shape)
        spec = controlled_demand_spec(config, native_profile=native_profile)
        data_source = "BurstGPT token profile"
        extra_sources = (BURST_PROFILE, BURST_METADATA, BURST_BUILDER)
    else:
        raise ValueError(f"unknown load source {load_source}")
    routing_share = config.firm_capacity / np.sum(config.firm_capacity)
    routing = np.repeat(routing_share[:, None], config.num_periods, axis=1)
    rows = []
    for policy, prices in controlled_policies(config).items():
        for mechanism, switches in MECHANISMS.items():
            temporal = switches["temporal_enabled"]
            spatial = switches["spatial_enabled"]
            result = solve_spatiotemporal_qos_fixed_point(
                prices, routing, spec, config=config,
                temporal_enabled=temporal, spatial_enabled=spatial,
                fixed_channel_shares=FIXED_CHANNEL_SHARES, qos_shape="sigmoid",
            )
            metrics = summarize_spatiotemporal_result(result)
            centroids = metrics.pop("destination_centroid_by_type")
            rows.append({
                "policy": policy, "mechanism": mechanism,
                "temporal_enabled": temporal, "spatial_enabled": spatial,
                "converged": result["converged"],
                "fixed_point_iterations": result["iterations"],
                "fixed_point_residual": result["fixed_point_residual"],
                "rigid_centroid": centroids[0], "elastic_centroid": centroids[1],
                **metrics,
            })
    _add_policy_deltas(rows)
    return {
        "metadata": build_manifest(
            config, data_source=data_source, load_source=load_source,
            extra_sources=extra_sources,
        ),
        "load_source": load_source,
        "rows": rows,
        "demand_spec": {
            "native_demand": spec.native_demand.tolist(),
            "price_sensitivity": spec.price_sensitivity.tolist(),
            "flexible_fraction": spec.flexible_fraction.tolist(),
            "migration_cost": spec.migration_cost.tolist(),
            "max_shift": spec.max_shift.tolist(),
            "channel_brand": spec.channel_brand.tolist(),
            "qos_weight": spec.qos_weight,
        },
        "fixed_channel_shares": FIXED_CHANNEL_SHARES.tolist(),
        "mechanism_definitions": MECHANISMS,
        "routing": routing.tolist(),
        "policies": {k: v.tolist() for k, v in controlled_policies(config).items()},
    }


def write_outputs(result: dict) -> tuple[Path, Path]:
    OUT.mkdir(parents=True, exist_ok=True)
    suffix = "" if result["load_source"] == "synthetic" else "_burstgpt"
    stem = f"spatiotemporal_mechanism_decomposition{suffix}"
    json_path = OUT / f"{stem}.json"
    csv_path = OUT / f"{stem}.csv"
    json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result["rows"][0]))
        writer.writeheader()
        writer.writerows(result["rows"])
    return json_path, csv_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--load-source", choices=("synthetic", "burstgpt"), default="synthetic")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_decomposition(load_source=args.load_source)
    paths = write_outputs(result)
    print(json.dumps({
        "outputs": [str(path.relative_to(ROOT)) for path in paths],
        "rows": len(result["rows"]),
        "all_converged": all(row["converged"] for row in result["rows"]),
    }, indent=2))


if __name__ == "__main__":
    main()
