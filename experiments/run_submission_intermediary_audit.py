"""Audit active intermediary responses with an independent global optimizer."""
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from dataclasses import fields
from datetime import datetime
import hashlib
import json
from multiprocessing import get_context
import os
from pathlib import Path

for _thread_variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_thread_variable] = "1"

import numpy as np  # noqa: E402
from scipy.optimize import differential_evolution  # noqa: E402

from experiments.run_final_spatiotemporal_equilibrium import final_case  # noqa: E402
from pricing_sim.intermediary_response import IntermediarySearchSpec  # noqa: E402
from pricing_sim.peak_shaving_equilibrium import FirmParams, expand_price  # noqa: E402
from pricing_sim.peak_shaving_market import intermediary_profit  # noqa: E402
from pricing_sim.spatiotemporal_game import (  # noqa: E402
    solve_spatiotemporal_joint_market,
)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "artifacts" / "peak_shaving" / "20260712_expanded_response"
EQUILIBRIUM_PATH = OUT / "spatiotemporal_equilibrium_submission.json"
OUTPUT_PATH = OUT / "intermediary_globality_audit_submission.json"
DEFAULT_MAXIMUM_PROFILES = 1_000
DEFAULT_MINIMUM_COVERAGE = 1.0


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        Path(__file__).resolve(),
        ROOT / "experiments/run_final_spatiotemporal_equilibrium.py",
        ROOT / "pricing_sim/intermediary_response.py",
        ROOT / "pricing_sim/peak_shaving_equilibrium.py",
        ROOT / "pricing_sim/spatiotemporal_game.py",
        ROOT / "pricing_sim/peak_shaving_market.py",
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def _search_spec(manifest: dict) -> IntermediarySearchSpec:
    raw = manifest["dynamic"]
    allowed = {item.name for item in fields(IntermediarySearchSpec)}
    values = {key: raw[key] for key in allowed if key in raw}
    for key in tuple(values):
        if key.endswith(("bounds", "seeds")):
            values[key] = tuple(values[key])
    return IntermediarySearchSpec(**values)


def _selected_profiles(
    game: dict,
    maximum_profiles: int,
    minimum_coverage: float = 0.8,
) -> tuple[list[dict], float]:
    if maximum_profiles < 1:
        raise ValueError("maximum_profiles must be positive")
    if not 0.0 < minimum_coverage <= 1.0:
        raise ValueError("minimum_coverage must lie in (0, 1]")
    profiles = sorted(game["active_profiles"], key=lambda item: item["weight"], reverse=True)
    selected = []
    covered = 0.0
    for profile in profiles[:maximum_profiles]:
        selected.append(profile)
        covered += float(profile["weight"])
        if covered >= minimum_coverage:
            break
    if covered + 1e-12 < minimum_coverage:
        raise ValueError(
            f"maximum_profiles={maximum_profiles} covers only {covered:.3%}; "
            f"minimum_coverage={minimum_coverage:.3%}"
        )
    return selected, covered


def _provider_prices(profile: dict, config) -> tuple[np.ndarray, np.ndarray]:
    firms = [
        FirmParams.from_vector(np.asarray(profile["row_vector"], dtype=float)),
        FirmParams.from_vector(np.asarray(profile["col_vector"], dtype=float)),
    ]
    return (
        np.vstack([firm.wholesale(config) for firm in firms]),
        np.vstack([firm.direct(config) for firm in firms]),
    )


def _evaluate(
    vector: np.ndarray,
    wholesale: np.ndarray,
    direct: np.ndarray,
    game,
    config,
    spec: IntermediarySearchSpec,
) -> tuple[float, dict, float]:
    base_bounds = spec.resolved_base_bounds(config)
    base = float(np.clip(vector[0], *base_bounds))
    slope = float(np.clip(vector[1], *spec.retail_slope_bounds))
    beta = float(np.clip(np.expm1(vector[2]), *spec.route_beta_bounds))
    retail = expand_price(base, slope, config, config.price_lower, config.price_upper)
    state, result = solve_spatiotemporal_joint_market(
        retail, wholesale, direct, beta, game, config
    )
    profit = intermediary_profit(state, result, config) if result["joint_converged"] else -np.inf
    return float(profit), {
        "retail_base": base,
        "retail_slope": slope,
        "route_beta": beta,
    }, float(result["joint_residual"])


def _audit_profile(
    profile: dict,
    *,
    game,
    config,
    spec: IntermediarySearchSpec,
    seed: int,
    max_iterations: int,
    population_size: int,
) -> dict:
    wholesale, direct = _provider_prices(profile, config)
    bounds = [
        spec.resolved_base_bounds(config),
        spec.retail_slope_bounds,
        (float(np.log1p(spec.route_beta_bounds[0])), float(np.log1p(spec.route_beta_bounds[1]))),
    ]

    def objective(vector: np.ndarray) -> float:
        profit, _, _ = _evaluate(vector, wholesale, direct, game, config, spec)
        return -profit if np.isfinite(profit) else 1e12

    optimized = differential_evolution(
        objective,
        bounds,
        seed=seed,
        maxiter=max_iterations,
        popsize=population_size,
        polish=True,
        updating="immediate",
        workers=1,
        atol=1e-8,
        tol=1e-8,
    )
    global_profit, candidate, residual = _evaluate(
        np.asarray(optimized.x), wholesale, direct, game, config, spec
    )
    stored_profit = float(profile["intermediary_profit"])
    return {
        "row_index": profile["row_index"],
        "col_index": profile["col_index"],
        "equilibrium_weight": profile["weight"],
        "stored_candidate": profile["intermediary_candidate"],
        "stored_profit": stored_profit,
        "global_candidate": candidate,
        "global_profit": global_profit,
        "profit_improvement": global_profit - stored_profit,
        "relative_profit_improvement": (global_profit - stored_profit) / max(abs(stored_profit), 1.0),
        "joint_residual": residual,
        "optimizer_success": bool(optimized.success),
        "optimizer_message": str(optimized.message),
        "function_evaluations": int(optimized.nfev),
    }


def _audit_profile_task(payload: tuple) -> dict:
    profile, index, game, config, spec, seed, max_iterations, population_size = payload
    return _audit_profile(
        profile,
        game=game,
        config=config,
        spec=spec,
        seed=seed + index,
        max_iterations=max_iterations,
        population_size=population_size,
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
    seed: int,
    max_iterations: int,
    population_size: int,
    workers: int,
) -> dict:
    return {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "equilibrium_path": str(equilibrium_path.relative_to(ROOT)),
        "equilibrium_sha256": _sha256(equilibrium_path),
        "maximum_profiles": maximum_profiles,
        "minimum_coverage": minimum_coverage,
        "covered_probability_mass": covered_mass,
        "seed": seed,
        "max_iterations": max_iterations,
        "population_size": population_size,
        "parallel_workers": workers,
        "method": "scipy differential_evolution with polishing",
        "source_sha256": _source_hashes(),
        "command": (
            "uv run --no-project --with numpy --with scipy python -m "
            "experiments.run_submission_intermediary_audit"
        ),
    }


def _audit_summary(records: list[dict]) -> dict:
    return {
        "maximum_profit_improvement": max(
            item["profit_improvement"] for item in records
        ),
        "maximum_relative_profit_improvement": max(
            item["relative_profit_improvement"] for item in records
        ),
        "maximum_joint_residual": max(item["joint_residual"] for item in records),
    }


def run_audit(
    *,
    equilibrium_path: Path = EQUILIBRIUM_PATH,
    maximum_profiles: int = DEFAULT_MAXIMUM_PROFILES,
    minimum_coverage: float = DEFAULT_MINIMUM_COVERAGE,
    seed: int = 20260713,
    max_iterations: int = 35,
    population_size: int = 8,
    parallel_workers: int | None = None,
) -> dict:
    equilibrium_path = Path(equilibrium_path).resolve()
    equilibrium = json.loads(equilibrium_path.read_text(encoding="utf-8"))
    if equilibrium["intermediary_response"]["method"] != "continuous_multistart":
        raise ValueError("globality audit requires a continuous intermediary response")
    config, game, _ = final_case(**equilibrium.get("scenario", {}))
    spec = _search_spec(equilibrium["intermediary_response"])
    profiles, covered_mass = _selected_profiles(
        equilibrium["dynamic"], maximum_profiles, minimum_coverage
    )
    workers = parallel_workers or min(16, os.cpu_count() or 1)
    if workers < 1:
        raise ValueError("parallel_workers must be positive")
    payloads = [
        (profile, index, game, config, spec, seed, max_iterations, population_size)
        for index, profile in enumerate(profiles)
    ]
    records = _run_profile_tasks(payloads, workers)
    return {
        "metadata": _audit_metadata(
            equilibrium_path=equilibrium_path,
            maximum_profiles=maximum_profiles,
            minimum_coverage=minimum_coverage,
            covered_mass=covered_mass,
            seed=seed,
            max_iterations=max_iterations,
            population_size=population_size,
            workers=workers,
        ),
        "records": records,
        **_audit_summary(records),
        "interpretation_boundary": (
            "Independent stochastic global-search diagnostic on the highest-weight active "
            "profiles; not a proof of a global optimum for every provider pair."
        ),
    }


def main() -> None:
    result = run_audit()
    OUT.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
        "covered_probability_mass": result["metadata"]["covered_probability_mass"],
        "maximum_profit_improvement": result["maximum_profit_improvement"],
    }, indent=2))


if __name__ == "__main__":
    main()
