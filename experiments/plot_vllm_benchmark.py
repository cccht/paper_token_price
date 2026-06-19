"""Render vLLM overload curves from a saved benchmark summary."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
for import_path in (PROJECT_ROOT, SCRIPT_DIR):
    path_text = str(import_path)
    if path_text not in sys.path:
        sys.path.insert(0, path_text)

from pricing_sim.vllm_plots import write_vllm_plot


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("summary_csv", type=Path)
    args = parser.parse_args()
    print(write_vllm_plot(args.summary_csv))


if __name__ == "__main__":
    main()
