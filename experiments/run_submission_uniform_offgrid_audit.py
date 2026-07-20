"""Run independent uniform-policy off-grid audits for all submission cases."""
from __future__ import annotations

from datetime import datetime
import hashlib
import json
import os
from pathlib import Path

for _thread_variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_thread_variable] = "1"

from experiments.offgrid_diagnostic_tools import _intermediary_spec  # noqa: E402
from experiments.run_final_spatiotemporal_equilibrium import (  # noqa: E402
    ROOT,
    final_case,
)
from experiments.run_submission_spatiotemporal_sensitivity import (  # noqa: E402
    SCENARIOS,
)
from experiments.uniform_offgrid_diagnostic_tools import (  # noqa: E402
    BASE_PRICE_BOUNDS,
    search_uniform_player,
)


OUT = ROOT / "artifacts" / "peak_shaving" / "20260712_expanded_response"
BASELINE_PATH = OUT / "spatiotemporal_equilibrium_submission.json"
SCENARIO_PATHS = {
    "baseline": BASELINE_PATH,
    **{
        name: OUT / f"sensitivity_{name}_submission.json"
        for name in SCENARIOS
    },
}
OUTPUT_PATH = OUT / "uniform_offgrid_sensitivity_submission.json"
CACHE_ROOT = Path.home() / ".cache" / "peak_shaving_uniform_offgrid"
SUBMISSION_SAMPLES_PER_PLAYER = 1024
SUBMISSION_RANDOM_SEED = 20260718
MAX_PARALLEL_WORKERS = 16


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        Path(__file__).resolve(),
        ROOT / "experiments/uniform_offgrid_diagnostic_tools.py",
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def _validated_artifact(
    name: str, path: Path, baseline_hash: str
) -> tuple[Path, dict]:
    path = Path(path).resolve()
    artifact = json.loads(path.read_text(encoding="utf-8"))
    if name != "baseline":
        recorded = artifact.get("metadata", {}).get("baseline_equilibrium", {}).get(
            "sha256"
        )
        if recorded != baseline_hash:
            raise ValueError(f"{name}: sensitivity artifact baseline SHA-256 differs")
    if artifact["uniform"]["candidate_count"] != 800:
        raise ValueError(f"{name}: uniform candidate count is not 800")
    return path, artifact


def _audit_scenario(
    name: str,
    path: Path,
    artifact: dict,
    *,
    samples_per_player: int,
    seed: int,
    workers: int,
    cache_root: Path,
) -> dict:
    equilibrium_hash = _sha256(path)
    config, game_spec, _ = final_case(**artifact.get("scenario", {}))
    response_spec = _intermediary_spec(artifact["intermediary_response"])
    players = {}
    for offset, player in enumerate(("firm_A", "firm_B")):
        players[player] = search_uniform_player(
            player,
            artifact["uniform"],
            samples_per_player,
            seed + offset,
            config=config,
            game_spec=game_spec,
            intermediary_search_spec=response_spec,
            parallel_workers=workers,
            cache_path=cache_root / name / f"{player}.pkl",
            equilibrium_hash=equilibrium_hash,
        )
    return {
        "scenario": name,
        "equilibrium_artifact": str(path.relative_to(ROOT)),
        "equilibrium_sha256": equilibrium_hash,
        "players": players,
    }


def run_uniform_offgrid_audit(
    *,
    scenario_paths: dict[str, Path] = SCENARIO_PATHS,
    baseline_path: Path = BASELINE_PATH,
    samples_per_player: int = SUBMISSION_SAMPLES_PER_PLAYER,
    seed: int = SUBMISSION_RANDOM_SEED,
    parallel_workers: int | None = None,
    cache_root: Path = CACHE_ROOT,
) -> dict:
    if samples_per_player < 1:
        raise ValueError("samples_per_player must be positive")
    if tuple(scenario_paths) != ("baseline", *SCENARIOS):
        raise ValueError("uniform off-grid audit requires the declared nine scenarios")
    workers = parallel_workers or min(MAX_PARALLEL_WORKERS, os.cpu_count() or 1)
    if workers < 1:
        raise ValueError("parallel_workers must be positive")
    baseline_path = Path(baseline_path).resolve()
    baseline_hash = _sha256(baseline_path)
    outputs = []
    for name, path in scenario_paths.items():
        resolved, artifact = _validated_artifact(name, path, baseline_hash)
        outputs.append(
            _audit_scenario(
                name,
                resolved,
                artifact,
                samples_per_player=samples_per_player,
                seed=seed,
                workers=workers,
                cache_root=Path(cache_root),
            )
        )
    return {
        "metadata": {
            "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "baseline_sha256": baseline_hash,
            "samples_per_player": samples_per_player,
            "seed": seed,
            "scenario_count": len(outputs),
            "parallel_workers": workers,
            "source_sha256": _source_hashes(),
            "command": (
                "uv run --no-project --with numpy --with scipy --with nashpy "
                "python -m experiments.run_submission_uniform_offgrid_audit"
            ),
        },
        "search_domain": {
            "wholesale_base": BASE_PRICE_BOUNDS[0].tolist(),
            "direct_base": BASE_PRICE_BOUNDS[1].tolist(),
            "wholesale_slope": [0.0, 0.0],
            "direct_slope": [0.0, 0.0],
        },
        "scenarios": outputs,
        "interpretation_boundary": (
            "Each uniform game is checked with an independent bounded two-dimensional "
            "sample and local refinement; this is not a continuous-space Nash proof."
        ),
    }


def main() -> None:
    result = run_uniform_offgrid_audit()
    OUTPUT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
        "scenario_count": result["metadata"]["scenario_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
