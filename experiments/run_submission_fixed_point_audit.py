"""Audit initialization sensitivity of active routing--QoS fixed points."""
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
import hashlib
import json
from multiprocessing import get_context
import os
from pathlib import Path

for _thread_variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_thread_variable] = "1"

import numpy as np  # noqa: E402

from experiments.run_final_spatiotemporal_equilibrium import final_case  # noqa: E402
from experiments.run_submission_intermediary_audit import (  # noqa: E402
    DEFAULT_MAXIMUM_PROFILES,
    DEFAULT_MINIMUM_COVERAGE,
    _provider_prices,
    _selected_profiles,
)
from pricing_sim.peak_shaving_equilibrium import expand_price  # noqa: E402
from pricing_sim.peak_shaving_market import (  # noqa: E402
    FIXED_POINT_MAX_ITER,
    FIXED_POINT_TOL,
    QOS_DAMPING,
)
from pricing_sim.spatiotemporal_game import _joint_target  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "artifacts" / "peak_shaving" / "20260712_expanded_response"
EQUILIBRIUM_PATH = OUT / "spatiotemporal_equilibrium_submission.json"
OUTPUT_PATH = OUT / "fixed_point_multistart_audit_submission.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        Path(__file__).resolve(),
        ROOT / "experiments/run_final_spatiotemporal_equilibrium.py",
        ROOT / "experiments/run_submission_intermediary_audit.py",
        ROOT / "pricing_sim/peak_shaving_equilibrium.py",
        ROOT / "pricing_sim/peak_shaving_market.py",
        ROOT / "pricing_sim/spatiotemporal_game.py",
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def _random_routing(rng: np.random.Generator, periods: int) -> np.ndarray:
    first = rng.uniform(0.0, 1.0, size=periods)
    return np.vstack([first, 1.0 - first])


def _solve_from_initial(
    retail: np.ndarray,
    wholesale: np.ndarray,
    direct: np.ndarray,
    route_beta: float,
    game,
    config,
    qos: np.ndarray,
    routing: np.ndarray,
) -> dict:
    prices = np.vstack([retail[None, :], direct])
    qos = np.asarray(qos, dtype=float).copy()
    routing = np.asarray(routing, dtype=float).copy()
    iterations = 0
    for iterations in range(1, FIXED_POINT_MAX_ITER + 1):
        _, _, _, target_qos, target_routing = _joint_target(
            prices, wholesale, routing, qos, route_beta, game, config
        )
        residual = max(
            float(np.max(np.abs(target_qos - qos))),
            float(np.max(np.abs(target_routing - routing))),
        )
        if residual <= FIXED_POINT_TOL:
            break
        qos += QOS_DAMPING * (target_qos - qos)
        routing += QOS_DAMPING * (target_routing - routing)
    _, _, _, target_qos, target_routing = _joint_target(
        prices, wholesale, routing, qos, route_beta, game, config
    )
    residual = max(
        float(np.max(np.abs(target_qos - qos))),
        float(np.max(np.abs(target_routing - routing))),
    )
    return {
        "qos": qos,
        "routing": routing,
        "iterations": iterations,
        "residual": residual,
        "converged": residual <= FIXED_POINT_TOL,
    }


def _audit_profile(profile: dict, *, starts: int, seed: int, game, config) -> dict:
    if starts < 1:
        raise ValueError("starts must be positive")
    wholesale, direct = _provider_prices(profile, config)
    candidate = profile["intermediary_candidate"]
    retail = expand_price(
        candidate["retail_base"], candidate["retail_slope"], config,
        config.price_lower, config.price_upper,
    )
    rng = np.random.default_rng(seed)
    outcomes = []
    for _ in range(starts):
        outcomes.append(_solve_from_initial(
            retail, wholesale, direct, candidate["route_beta"], game, config,
            rng.uniform(0.0, 1.0, size=(2, config.num_periods)),
            _random_routing(rng, config.num_periods),
        ))
    qos = np.stack([item["qos"] for item in outcomes])
    routing = np.stack([item["routing"] for item in outcomes])
    return {
        "row_index": profile["row_index"],
        "col_index": profile["col_index"],
        "equilibrium_weight": profile["weight"],
        "starts": starts,
        "converged_starts": sum(item["converged"] for item in outcomes),
        "maximum_iterations": max(item["iterations"] for item in outcomes),
        "maximum_residual": max(item["residual"] for item in outcomes),
        "maximum_qos_span": float(np.max(np.ptp(qos, axis=0))),
        "maximum_routing_span": float(np.max(np.ptp(routing, axis=0))),
    }


def _audit_profile_task(payload: tuple) -> dict:
    profile, index, starts, seed, game, config = payload
    return _audit_profile(
        profile, starts=starts, seed=seed + index, game=game, config=config
    )


def _run_profile_tasks(payloads: list[tuple], workers: int) -> list[dict]:
    if workers == 1:
        return [_audit_profile_task(payload) for payload in payloads]
    with ProcessPoolExecutor(
        max_workers=min(workers, len(payloads)),
        mp_context=get_context("spawn"),
    ) as executor:
        return list(executor.map(_audit_profile_task, payloads, chunksize=1))


def _audit_metadata(
    *,
    equilibrium_path: Path,
    maximum_profiles: int,
    minimum_coverage: float,
    covered_mass: float,
    starts_per_profile: int,
    seed: int,
    workers: int,
) -> dict:
    return {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "equilibrium_path": str(equilibrium_path.relative_to(ROOT)),
        "equilibrium_sha256": _sha256(equilibrium_path),
        "maximum_profiles": maximum_profiles,
        "minimum_coverage": minimum_coverage,
        "covered_probability_mass": covered_mass,
        "starts_per_profile": starts_per_profile,
        "seed": seed,
        "parallel_workers": workers,
        "source_sha256": _source_hashes(),
        "command": (
            "uv run --no-project --with numpy python -m "
            "experiments.run_submission_fixed_point_audit"
        ),
    }


def _audit_summary(records: list[dict]) -> dict:
    return {
        "all_starts_converged": all(
            item["converged_starts"] == item["starts"] for item in records
        ),
        "maximum_residual": max(item["maximum_residual"] for item in records),
        "maximum_qos_span": max(item["maximum_qos_span"] for item in records),
        "maximum_routing_span": max(item["maximum_routing_span"] for item in records),
    }


def run_audit(
    *,
    equilibrium_path: Path = EQUILIBRIUM_PATH,
    maximum_profiles: int = DEFAULT_MAXIMUM_PROFILES,
    minimum_coverage: float = DEFAULT_MINIMUM_COVERAGE,
    starts_per_profile: int = 32,
    seed: int = 20260713,
    parallel_workers: int | None = None,
) -> dict:
    equilibrium_path = Path(equilibrium_path).resolve()
    equilibrium = json.loads(equilibrium_path.read_text(encoding="utf-8"))
    config, game, _ = final_case(**equilibrium.get("scenario", {}))
    profiles, covered_mass = _selected_profiles(
        equilibrium["dynamic"], maximum_profiles, minimum_coverage
    )
    workers = parallel_workers or min(16, os.cpu_count() or 1)
    if workers < 1:
        raise ValueError("parallel_workers must be positive")
    payloads = [
        (profile, index, starts_per_profile, seed, game, config)
        for index, profile in enumerate(profiles)
    ]
    records = _run_profile_tasks(payloads, workers)
    return {
        "metadata": _audit_metadata(
            equilibrium_path=equilibrium_path,
            maximum_profiles=maximum_profiles,
            minimum_coverage=minimum_coverage,
            covered_mass=covered_mass,
            starts_per_profile=starts_per_profile,
            seed=seed,
            workers=workers,
        ),
        "records": records,
        **_audit_summary(records),
        "interpretation_boundary": (
            "Random-initialization diagnostic on the highest-weight active profiles; "
            "not an analytical uniqueness proof."
        ),
    }


def main() -> None:
    result = run_audit()
    OUT.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
        "covered_probability_mass": result["metadata"]["covered_probability_mass"],
        "all_starts_converged": result["all_starts_converged"],
        "maximum_qos_span": result["maximum_qos_span"],
        "maximum_routing_span": result["maximum_routing_span"],
    }, indent=2))


if __name__ == "__main__":
    main()
