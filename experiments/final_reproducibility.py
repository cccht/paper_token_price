from __future__ import annotations

from datetime import datetime
import hashlib
from importlib.metadata import version
import os
from pathlib import Path
import platform
import subprocess

import numpy as np


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True, text=True
    ).stdout.strip()


def equilibrium_metadata(
    root: Path,
    qos_calibration: Path,
    runner: Path,
    candidate_count: int,
    response_method: str,
) -> dict:
    sources = (
        root / "pricing_sim/peak_shaving_config.py",
        root / "pricing_sim/peak_shaving_equilibrium.py",
        root / "pricing_sim/peak_shaving_market.py",
        root / "pricing_sim/spatiotemporal_mechanism.py",
        root / "pricing_sim/spatiotemporal_game.py",
        root / "pricing_sim/intermediary_response.py",
        root / "pricing_sim/finite_game.py",
        root / "pricing_sim/bimatrix_solver.py",
        root / "pricing_sim/complementarity_solver.py",
        root / "pricing_sim/milp_equilibrium_solver.py",
        root / "experiments/equilibrium_cache.py",
        root / "experiments/equilibrium_run_support.py",
        root / "experiments/final_equilibrium_tools.py",
        root / "experiments/peak_shaving_submission_tools.py",
        root / "experiments/run_spatiotemporal_mechanism_decomposition.py",
        Path(__file__).resolve(),
        runner,
        qos_calibration,
        root / "data/processed/burstgpt_d895a53b_8period/burstgpt_8period_load_profile.csv",
    )
    return {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "load_source": "BurstGPT token profile",
        "evidence_level": (
            "finite provider game with full-grid deviation scan and "
            f"{response_method} intermediary response"
        ),
        "full_candidate_count": candidate_count,
        "git_commit": _git(root, "rev-parse", "HEAD"),
        "git_dirty": bool(_git(root, "status", "--porcelain")),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": version("scipy"),
        "nashpy": version("nashpy"),
        "command": (
            "uv run --no-project --with numpy --with scipy --with nashpy "
            "python -m experiments.run_final_spatiotemporal_equilibrium"
        ),
        "environment": {
            "OMP_NUM_THREADS": os.environ.get("OMP_NUM_THREADS"),
            "OPENBLAS_NUM_THREADS": os.environ.get("OPENBLAS_NUM_THREADS"),
            "MKL_NUM_THREADS": os.environ.get("MKL_NUM_THREADS"),
        },
        "source_sha256": {
            str(path.relative_to(root)): _sha256(path) for path in sources
        },
    }
