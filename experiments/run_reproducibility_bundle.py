"""Run the CPU-only reproducibility bundle for the token-pricing manuscript."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
VLLM_AGGREGATES = (
    PROJECT_ROOT / "artifacts/vllm-study/20260531-190126/controlled_aggregate.csv",
    PROJECT_ROOT / "artifacts/vllm-study-qwen25-3b/20260531-214710/controlled_aggregate.csv",
)


def build_commands(
    *,
    output_root: Path,
    smoke: bool,
    skip_tests: bool,
) -> list[list[str]]:
    mode = "--smoke" if smoke else "--full"
    commands = [[
        sys.executable,
        str(SCRIPT_DIR / "run_experiment.py"),
        mode,
        "--output-root",
        str(output_root / "economic"),
    ], [
        sys.executable,
        str(SCRIPT_DIR / "run_supplemental_experiments.py"),
        "--vllm-aggregate",
        str(VLLM_AGGREGATES[0]),
        "--vllm-aggregate",
        str(VLLM_AGGREGATES[1]),
        "--output-root",
        str(output_root / "supplemental"),
    ], [
        sys.executable,
        str(SCRIPT_DIR / "run_calibration_uncertainty_experiments.py"),
        "--trials",
        "1" if smoke else "2",
        "--maxiter",
        "30",
        "--output-root",
        str(output_root / "calibration_uncertainty"),
    ]]
    if not skip_tests:
        commands.append([sys.executable, "-m", "pytest", "-q"])
    return commands


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--skip-tests", action="store_true")
    parser.add_argument(
        "--output-root",
        type=Path,
        default=PROJECT_ROOT / "artifacts/reproducibility" / datetime.now().strftime("%Y%m%d-%H%M%S"),
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    for command in build_commands(
        output_root=args.output_root,
        smoke=args.smoke,
        skip_tests=args.skip_tests,
    ):
        print(subprocess.list2cmdline(command), flush=True)
        subprocess.run(command, cwd=PROJECT_ROOT, check=True)
    print(f"artifacts={args.output_root}")


if __name__ == "__main__":
    main()
