"""Run reproducible QoS-aware token-pricing simulations."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
for import_path in (PROJECT_ROOT, SCRIPT_DIR):
    path_text = str(import_path)
    if path_text not in sys.path:
        sys.path.insert(0, path_text)

from pricing_sim.config import SimulationConfig
from pricing_sim.experiments import run_full_matrix, run_smoke_matrix
from pricing_sim.plots import write_plots
from pricing_sim.reporting import write_artifacts


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--smoke", action="store_true")
    mode.add_argument("--full", action="store_true")
    parser.add_argument(
        "--output-root",
        type=Path,
        default=PROJECT_ROOT / "artifacts",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    mode = "smoke" if args.smoke else "full"
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    config = SimulationConfig.default()
    if args.smoke:
        config = SimulationConfig.default(optimizer_trials=2, optimizer_maxiter=60)
        records = run_smoke_matrix(config)
    else:
        records = run_full_matrix(config)
    paths = write_artifacts(records, output_root=args.output_root, run_id=run_id)
    plots = write_plots(records, output_root=args.output_root, run_id=run_id)
    print(f"mode={mode}")
    print(f"records={len(records)}")
    print(f"raw={paths.raw_jsonl}")
    print(f"summary={paths.summary_csv}")
    for plot in plots:
        print(f"plot={plot}")


if __name__ == "__main__":
    main()
