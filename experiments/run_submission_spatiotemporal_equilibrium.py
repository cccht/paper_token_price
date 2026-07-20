"""Resume and write the audit-adaptive submission equilibrium."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

for _thread_variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_thread_variable] = "1"

from experiments.run_final_spatiotemporal_equilibrium import (  # noqa: E402
    ROOT,
    run_equilibria,
)
from experiments.submission_candidate_design import (  # noqa: E402
    augmented_submission_provider_candidate_grid,
    candidate_design_metadata,
)

OUT = ROOT / "artifacts" / "peak_shaving" / "20260712_expanded_response"
OUTPUT_PATH = OUT / "spatiotemporal_equilibrium_submission.json"
ARCHIVED_BASELINE_PATH = (
    OUT / "pre_uniform_expansion" / "spatiotemporal_equilibrium_submission.json"
)
SEED_PATHS = (ARCHIVED_BASELINE_PATH,)
PAIR_CACHE_DIR = Path.home() / ".cache" / "peak_shaving_uniform_expansion_baseline"
MAX_ORACLE_ROUNDS = 100
PARALLEL_WORKERS = 16


def _active_vectors(game: dict) -> tuple[list[list[float]], list[list[float]]]:
    output = []
    for prefix in ("row", "col"):
        output.append([
            vector
            for vector, probability in zip(
                game[f"{prefix}_support_vectors"], game[f"{prefix}_mix"]
            )
            if probability > 1e-10
        ])
    return output[0], output[1]


def _continuation_vectors(
    paths: tuple[Path, ...] = SEED_PATHS,
) -> tuple[tuple[list[list[float]], list[list[float]]] | None, Path | None]:
    for path in paths:
        if path.exists():
            payload = json.loads(path.read_text(encoding="utf-8"))
            return _active_vectors(payload["dynamic"]), path
    return None, None


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    initial_vectors, seed_path = _continuation_vectors()
    if initial_vectors is None:
        raise FileNotFoundError("an audited equilibrium seed is required")
    reference_vectors = initial_vectors[0] + initial_vectors[1]
    candidate_grid = augmented_submission_provider_candidate_grid(reference_vectors)
    result = run_equilibria(
        candidate_grid=candidate_grid,
        max_oracle_rounds=MAX_ORACLE_ROUNDS,
        initial_dynamic_vectors=initial_vectors,
        pair_cache_dir=PAIR_CACHE_DIR,
        parallel_workers=PARALLEL_WORKERS,
    )
    runner = Path(__file__).resolve()
    design_source = ROOT / "experiments/submission_candidate_design.py"
    result["metadata"]["command"] = (
        "uv run --no-project --with numpy --with scipy --with nashpy "
        "python -m experiments.run_submission_spatiotemporal_equilibrium"
    )
    result["metadata"]["source_sha256"][str(runner.relative_to(ROOT))] = _sha256(runner)
    result["metadata"]["source_sha256"][
        str(design_source.relative_to(ROOT))
    ] = _sha256(design_source)
    result["metadata"]["continuation_seed"] = (
        None if seed_path is None else {
            "path": str(seed_path.relative_to(ROOT)),
            "sha256": _sha256(seed_path),
        }
    )
    result["metadata"]["candidate_design"] = {
        **candidate_design_metadata(reference_vectors),
        "reference_support_count": len(reference_vectors),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    temporary = OUTPUT_PATH.with_suffix(OUTPUT_PATH.suffix + ".tmp")
    temporary.write_text(json.dumps(result, indent=2), encoding="utf-8")
    temporary.replace(OUTPUT_PATH)
    print(json.dumps({
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
        "loaded_pairs": result["metadata"]["pair_cache"]["dynamic"]["loaded_pairs"],
        "uniform_regret": result["uniform"]["full_max_regret"],
        "dynamic_regret": result["dynamic"]["full_max_regret"],
        "dynamic_pairs": result["dynamic"]["evaluated_pairs"],
        "trace": result["dynamic"]["trace"],
    }, indent=2))


if __name__ == "__main__":
    main()
