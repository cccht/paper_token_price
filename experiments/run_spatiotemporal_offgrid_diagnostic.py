"""Bounded off-grid best-response diagnostic for the expanded provider game."""
from __future__ import annotations

from datetime import datetime
import hashlib
import json
import os
from pathlib import Path

for _thread_variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_thread_variable] = "1"

from experiments.offgrid_diagnostic_tools import (  # noqa: E402
    _intermediary_spec,
    _search_domain,
    _search_player,
)
from experiments.run_final_spatiotemporal_equilibrium import final_case  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "artifacts" / "peak_shaving" / "20260712_expanded_response"
EQUILIBRIUM_PATH = OUT / "spatiotemporal_equilibrium_submission.json"
OUTPUT_PATH = OUT / "spatiotemporal_offgrid_diagnostic_submission.json"
MAX_PARALLEL_WORKERS = 16
SUBMISSION_SAMPLES_PER_PLAYER = 1024
SUBMISSION_RANDOM_SEED = 20260714
SUBMISSION_CACHE_DIR = Path.home() / ".cache" / "peak_shaving_submission_offgrid"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _metadata(
    equilibrium: dict,
    equilibrium_path: Path,
    equilibrium_hash: str,
    samples: int,
    seed: int,
    workers: int,
) -> dict:
    sources = (
        equilibrium_path,
        ROOT / "pricing_sim/intermediary_response.py",
        ROOT / "experiments/offgrid_diagnostic_tools.py",
        Path(__file__).resolve(),
    )
    return {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "samples_per_player": samples,
        "seed": seed,
        "parallel_workers": workers,
        "environment": {
            key: os.environ.get(key)
            for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")
        },
        "provider_candidate_count": equilibrium["provider_strategy_grid"]["candidate_count"],
        "intermediary_response_method": equilibrium["intermediary_response"]["method"],
        "equilibrium_sha256": equilibrium_hash,
        "command": "uv run --no-project --with numpy --with scipy python -m experiments.run_spatiotemporal_offgrid_diagnostic",
        "source_sha256": {
            str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path): _sha256(path)
            for path in sources
        },
    }


def run_offgrid_diagnostic(
    *,
    samples_per_player: int = SUBMISSION_SAMPLES_PER_PLAYER,
    seed: int = SUBMISSION_RANDOM_SEED,
    equilibrium_path: Path = EQUILIBRIUM_PATH,
    parallel_workers: int | None = None,
    cache_dir: Path | None = None,
) -> dict:
    if samples_per_player < 1:
        raise ValueError("samples per player must be positive")
    equilibrium_path = Path(equilibrium_path)
    equilibrium = json.loads(equilibrium_path.read_text(encoding="utf-8"))
    response_spec = _intermediary_spec(equilibrium["intermediary_response"])
    config, game_spec, _ = final_case(**equilibrium.get("scenario", {}))
    domain = _search_domain(config)
    workers = parallel_workers or min(MAX_PARALLEL_WORKERS, os.cpu_count() or 1)
    if workers < 1:
        raise ValueError("parallel_workers must be positive")
    equilibrium_hash = _sha256(equilibrium_path)
    cache_root = cache_dir or SUBMISSION_CACHE_DIR
    searches = {}
    for offset, player in enumerate(("firm_A", "firm_B")):
        searches[player] = _search_player(
            player, equilibrium["dynamic"], samples_per_player, seed + offset,
            config=config, game_spec=game_spec, domain=domain,
            intermediary_search_spec=response_spec, parallel_workers=workers,
            cache_path=cache_root / f"{player}.pkl", equilibrium_hash=equilibrium_hash,
        )
    return {
        "metadata": _metadata(
            equilibrium, equilibrium_path, equilibrium_hash,
            samples_per_player, seed, workers,
        ),
        "search_domain": domain,
        "players": searches,
        "interpretation_boundary": (
            "Deterministic bounded global and local sampling against the opponent mixed support; "
            "not a proof of a continuous-space Nash equilibrium."
        ),
    }


def main() -> None:
    result = run_offgrid_diagnostic()
    OUT.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
        "firm_A_regret": result["players"]["firm_A"]["offgrid_regret"],
        "firm_B_regret": result["players"]["firm_B"]["offgrid_regret"],
    }, indent=2))


if __name__ == "__main__":
    main()
