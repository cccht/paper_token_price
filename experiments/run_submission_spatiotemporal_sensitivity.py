"""Re-solve submission sensitivities with the audited provider and follower spaces."""
from __future__ import annotations

from datetime import datetime
import hashlib
import json
import os
from pathlib import Path

for _thread_variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_thread_variable] = "1"

import numpy as np  # noqa: E402

from experiments.equilibrium_run_support import comparison  # noqa: E402
from experiments.run_final_spatiotemporal_equilibrium import (  # noqa: E402
    ROOT,
    run_equilibria,
)

OUT = ROOT / "artifacts" / "peak_shaving" / "20260712_expanded_response"
BASELINE_PATH = OUT / "spatiotemporal_equilibrium_submission.json"
CACHE_ROOT = Path.home() / ".cache" / "peak_shaving_submission_sensitivity"
SUMMARY_PATH = OUT / "spatiotemporal_sensitivity_submission.json"
SCENARIOS = {
    "capacity_low": {"group": "capacity_scale", "value": 0.85, "capacity_scale": 0.85},
    "capacity_high": {"group": "capacity_scale", "value": 1.15, "capacity_scale": 1.15},
    "price_sensitivity_low": {
        "group": "price_sensitivity_scale", "value": 0.8,
        "price_sensitivity_scale": 0.8,
    },
    "price_sensitivity_high": {
        "group": "price_sensitivity_scale", "value": 1.2,
        "price_sensitivity_scale": 1.2,
    },
    "migration_cost_low": {
        "group": "migration_cost_scale", "value": 0.7,
        "migration_cost_scale": 0.7,
    },
    "migration_cost_high": {
        "group": "migration_cost_scale", "value": 1.3,
        "migration_cost_scale": 1.3,
    },
    "qos_threshold_low": {
        "group": "qos_threshold_shift", "value": -0.05,
        "qos_threshold_shift": -0.05,
    },
    "qos_threshold_high": {
        "group": "qos_threshold_shift", "value": 0.05,
        "qos_threshold_shift": 0.05,
    },
}
SOLVER_KEYS = {
    "capacity_scale",
    "price_sensitivity_scale",
    "migration_cost_scale",
    "qos_threshold_shift",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def _source_hashes() -> dict[str, str]:
    runner = Path(__file__).resolve()
    return {str(runner.relative_to(ROOT)): _sha256(runner)}


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


def _summary_row(name: str, definition: dict, result: dict) -> dict:
    uniform = result["uniform"]
    dynamic = result["dynamic"]
    delta = comparison(uniform, dynamic)
    return {
        "scenario": name,
        "group": definition["group"],
        "value": definition["value"],
        "uniform_full_max_regret": uniform["full_max_regret"],
        "dynamic_full_max_regret": dynamic["full_max_regret"],
        "dynamic_relative_full_max_regret": dynamic["relative_full_max_regret"],
        "maximum_joint_residual": max(
            uniform["maximum_joint_residual"], dynamic["maximum_joint_residual"]
        ),
        "aggregate_peak_change_percent": delta["aggregate_peak_load_change_percent"],
        "maximum_provider_utilization_change_percent": delta[
            "maximum_provider_utilization_change_percent"
        ],
        "minimum_provider_qos_change": delta["minimum_provider_qos_change"],
        "market_profit_change_percent": delta["system_profit_change_percent"],
        "dynamic_evaluated_pairs": dynamic["evaluated_pairs"],
        "dynamic_row_support_count": sum(value > 1e-10 for value in dynamic["row_mix"]),
        "dynamic_col_support_count": sum(value > 1e-10 for value in dynamic["col_mix"]),
    }


def _scenario_path(name: str, output_dir: Path = OUT) -> Path:
    return Path(output_dir) / f"sensitivity_{name}_submission.json"


def _validated_names(scenario_names: list[str] | None) -> list[str]:
    names = list(SCENARIOS) if scenario_names is None else list(scenario_names)
    unknown = set(names) - set(SCENARIOS)
    if unknown:
        raise ValueError(f"unknown sensitivity scenarios: {sorted(unknown)}")
    return names


def _load_scenario_result(
    name: str,
    *,
    baseline_path: Path,
    output_dir: Path,
) -> tuple[Path, dict]:
    path = _scenario_path(name, output_dir)
    result = json.loads(path.read_text(encoding="utf-8"))
    recorded_hash = result.get("metadata", {}).get("baseline_equilibrium", {}).get(
        "sha256"
    )
    expected_hash = _sha256(baseline_path)
    if recorded_hash != expected_hash:
        raise ValueError(
            f"{path.name} baseline SHA-256 is {recorded_hash!r}; "
            f"expected {expected_hash!r}"
        )
    return path, result


def collect_sensitivity_summary(
    *,
    scenario_names: list[str] | None = None,
    baseline_path: Path = BASELINE_PATH,
    output_dir: Path = OUT,
) -> dict:
    baseline_path = Path(baseline_path).resolve()
    output_dir = Path(output_dir)
    names = _validated_names(scenario_names)
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    rows = []
    outputs = []
    for name in names:
        path, result = _load_scenario_result(
            name,
            baseline_path=baseline_path,
            output_dir=output_dir,
        )
        rows.append(_summary_row(name, SCENARIOS[name], result))
        outputs.append(_display_path(path))
    baseline_row = _summary_row(
        "baseline", {"group": "baseline", "value": 1.0}, baseline
    )
    return {
        "metadata": {
            "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "baseline_path": _display_path(baseline_path),
            "baseline_sha256": _sha256(baseline_path),
            "provider_candidate_count": len(baseline["candidate_grid"]),
            "intermediary_response_method": baseline["intermediary_response"]["method"],
            "scenario_count": 1 + len(rows),
            "scenario_outputs": outputs,
            "source_sha256": _source_hashes(),
            "command": "collect_sensitivity_summary from validated scenario artifacts",
        },
        "scenario_definitions": SCENARIOS,
        "rows": [baseline_row, *rows],
    }


def run_sensitivity(
    *,
    scenario_names: list[str] | None = None,
    baseline_path: Path = BASELINE_PATH,
    cache_root: Path = CACHE_ROOT,
    output_dir: Path = OUT,
    parallel_workers: int | None = None,
) -> dict:
    baseline_path = Path(baseline_path).resolve()
    names = _validated_names(scenario_names)
    if parallel_workers is not None and parallel_workers < 1:
        raise ValueError("parallel_workers must be positive")
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    grid = np.asarray(baseline["candidate_grid"], dtype=float)
    initial_vectors = _active_vectors(baseline["dynamic"])
    rows = []
    outputs = []
    for name in names:
        definition = SCENARIOS[name]
        kwargs = {key: definition[key] for key in SOLVER_KEYS if key in definition}
        print(f"starting submission sensitivity: {name}", flush=True)
        result = run_equilibria(
            candidate_grid=grid,
            max_oracle_rounds=100,
            initial_dynamic_vectors=initial_vectors,
            pair_cache_dir=Path(cache_root) / name,
            parallel_workers=parallel_workers,
            **kwargs,
        )
        result["metadata"]["baseline_equilibrium"] = {
            "path": _display_path(baseline_path),
            "sha256": _sha256(baseline_path),
        }
        result["metadata"]["source_sha256"].update(_source_hashes())
        path = _scenario_path(name, output_dir)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, indent=2), encoding="utf-8")
        outputs.append(_display_path(path))
        row = _summary_row(name, definition, result)
        rows.append(row)
        print(
            f"finished {name}: regret={row['dynamic_full_max_regret']:.4g}, "
            f"peak={row['aggregate_peak_change_percent']:.2f}%",
            flush=True,
        )
    baseline_row = _summary_row(
        "baseline", {"group": "baseline", "value": 1.0}, baseline
    )
    return {
        "metadata": {
            "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "baseline_path": _display_path(baseline_path),
            "baseline_sha256": _sha256(baseline_path),
            "provider_candidate_count": len(grid),
            "intermediary_response_method": baseline["intermediary_response"]["method"],
            "scenario_count": 1 + len(rows),
            "scenario_outputs": outputs,
            "source_sha256": _source_hashes(),
            "command": (
                "uv run --no-project --with numpy --with scipy --with nashpy "
                "python -m experiments.run_submission_spatiotemporal_sensitivity"
            ),
        },
        "scenario_definitions": SCENARIOS,
        "rows": [baseline_row, *rows],
    }


def main() -> None:
    result = run_sensitivity()
    SUMMARY_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({
        "output": str(SUMMARY_PATH.relative_to(ROOT)),
        "scenario_count": result["metadata"]["scenario_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
