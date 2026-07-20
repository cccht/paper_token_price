"""Build an exact, human-readable manifest of the submission candidate set."""
from __future__ import annotations

from datetime import datetime
import hashlib
import json
from pathlib import Path

import numpy as np

from experiments.submission_candidate_design import (
    augmented_submission_provider_candidate_grid,
    common_uniform_provider_candidate_grid,
)


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = ROOT / "artifacts" / "peak_shaving" / "20260712_expanded_response"
FINAL_PATH = ARTIFACT_DIR / "spatiotemporal_equilibrium_submission.json"
SEED_PATH = (
    ARTIFACT_DIR / "pre_uniform_expansion" / "spatiotemporal_equilibrium_submission.json"
)
OUTPUT_PATH = ARTIFACT_DIR / "candidate_manifest_submission.json"
ACTIVE_TOLERANCE = 1e-10


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        Path(__file__).resolve(),
        ROOT / "experiments/peak_shaving_submission_tools.py",
        ROOT / "experiments/submission_candidate_design.py",
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def _active_reference_vectors(seed: dict) -> np.ndarray:
    game = seed["dynamic"]
    vectors: list[list[float]] = []
    for prefix in ("row", "col"):
        vectors.extend(
            vector
            for vector, probability in zip(
                game[f"{prefix}_support_vectors"], game[f"{prefix}_mix"]
            )
            if probability > ACTIVE_TOLERANCE
        )
    return np.asarray(vectors, dtype=float)


def _uniform_candidates() -> np.ndarray:
    return common_uniform_provider_candidate_grid()


def _mid_candidates() -> np.ndarray:
    return np.array([
        (0.25, slope, direct, direct_slope)
        for slope in (0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80)
        for direct in (
            0.5071875, 0.5175, 0.5278125, 0.538125,
            0.5484375, 0.55875, 0.5690625,
        )
        for direct_slope in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6)
    ])


def _wholesale_base_guards() -> np.ndarray:
    return np.array([
        (base, slope, direct, direct_slope)
        for base in (0.258125, 0.26625)
        for slope in (0.45, 0.55, 0.65, 0.75, 0.85)
        for direct in (0.5175, 0.538125, 0.55875, 0.579375)
        for direct_slope in (0.2, 0.4, 0.6)
    ])


def _low_slope_candidates() -> np.ndarray:
    return np.array([
        (0.25, slope, direct, direct_slope)
        for slope in (0.0, 0.1, 0.2, 0.3)
        for direct in (0.496875, 0.5175, 0.538125, 0.55875)
        for direct_slope in (0.1, 0.2, 0.3, 0.4)
    ])


def _high_slope_candidates() -> np.ndarray:
    return np.array([
        (0.25, slope, direct, direct_slope)
        for slope in (1.3, 1.5, 1.7)
        for direct in (0.538125, 0.55875, 0.579375)
        for direct_slope in (0.1, 0.3, 0.5)
    ])


def _boundary_guards() -> np.ndarray:
    wholesale = [
        (0.25, slope, direct, direct_slope)
        for slope in (0.6, 1.0, 1.5, 2.0, 3.0)
        for direct in (0.45, 0.60)
        for direct_slope in (0.0, 0.4, 0.8, 1.2, 2.0, 3.0)
    ]
    direct = [
        (0.25, slope, price, direct_slope)
        for slope in (0.0, 0.4, 0.8, 1.2, 2.0, 3.0)
        for price in (0.45, 0.60)
        for direct_slope in (1.0, 1.5, 2.0, 3.0)
    ]
    return np.asarray(wholesale + direct, dtype=float)


def _audited_local_candidates() -> np.ndarray:
    provider_a = [
        (0.25, slope, direct, direct_slope)
        for slope in (0.20, 0.25, 0.30)
        for direct in (0.5175, 0.5278125, 0.538125)
        for direct_slope in (0.1, 0.2, 0.3)
    ]
    provider_b = [
        (base, slope, direct, direct_slope)
        for base in (0.25, 0.258125)
        for slope in (0.95, 1.05, 1.15)
        for direct in (0.5175, 0.5278125, 0.538125)
        for direct_slope in (0.3, 0.4, 0.5)
    ]
    return np.asarray(provider_a + provider_b, dtype=float)


def _component_arrays(reference: np.ndarray) -> list[tuple[str, str, np.ndarray]]:
    return [
        ("uniform", "Full 800-rule zero-slope comparison domain", _uniform_candidates()),
        ("mid_slope", "Mid-slope local lattice", _mid_candidates()),
        ("wholesale_base_guard", "Two wholesale-base guard layers", _wholesale_base_guards()),
        ("low_slope", "Low-slope local lattice", _low_slope_candidates()),
        ("high_slope", "High-slope local lattice", _high_slope_candidates()),
        ("boundary_guards", "Wholesale and direct high-slope guards", _boundary_guards()),
        ("audited_local", "Two fourth-audit local lattices", _audited_local_candidates()),
        ("continuation", "Positive-probability vectors from the preceding solve", reference),
    ]


def _component_summary(
    components: list[tuple[str, str, np.ndarray]],
) -> tuple[list[dict], np.ndarray]:
    accumulated = np.empty((0, 4), dtype=float)
    rows: list[dict] = []
    for name, description, values in components:
        unique_values = np.unique(values, axis=0)
        combined = np.unique(np.vstack([accumulated, unique_values]), axis=0)
        rows.append({
            "name": name,
            "description": description,
            "raw_count": int(len(values)),
            "within_component_unique_count": int(len(unique_values)),
            "added_unique_count": int(len(combined) - len(accumulated)),
            "cumulative_unique_count": int(len(combined)),
        })
        accumulated = combined
    return rows, accumulated


def _continuation_only(
    components: list[tuple[str, str, np.ndarray]],
) -> np.ndarray:
    deterministic = np.unique(
        np.vstack([values for _, _, values in components[:-1]]), axis=0
    )
    deterministic_keys = {tuple(row) for row in deterministic}
    reference = np.unique(components[-1][2], axis=0)
    return np.asarray(
        [row for row in reference if tuple(row) not in deterministic_keys], dtype=float
    )


def build_manifest(*, final_path: Path, seed_path: Path) -> dict:
    final = json.loads(final_path.read_text(encoding="utf-8"))
    seed = json.loads(seed_path.read_text(encoding="utf-8"))
    reference = _active_reference_vectors(seed)
    components = _component_arrays(reference)
    rows, component_union = _component_summary(components)
    reconstructed = augmented_submission_provider_candidate_grid(reference)
    final_grid = np.asarray(final["candidate_grid"], dtype=float)
    exact_match = final_grid.shape == reconstructed.shape and np.array_equal(
        final_grid, reconstructed
    )
    return {
        "metadata": {
            "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "final_equilibrium_path": str(final_path.relative_to(ROOT)),
            "final_equilibrium_sha256": _sha256(final_path),
            "continuation_seed_path": str(seed_path.relative_to(ROOT)),
            "continuation_seed_sha256": _sha256(seed_path),
            "active_probability_tolerance": ACTIVE_TOLERANCE,
            "source_sha256": _source_hashes(),
            "command": (
                "uv run --no-project --with-requirements requirements.txt python -m "
                "experiments.build_submission_candidate_manifest"
            ),
        },
        "components": rows,
        "continuation_only_vectors": _continuation_only(components).tolist(),
        "verification": {
            "reference_support_entry_count": int(len(reference)),
            "reference_unique_count": int(len(np.unique(reference, axis=0))),
            "component_union_count": int(len(component_union)),
            "reconstructed_candidate_count": int(len(reconstructed)),
            "final_candidate_count": int(len(final_grid)),
            "exact_elementwise_match": bool(exact_match),
        },
    }


def main() -> None:
    manifest = build_manifest(final_path=FINAL_PATH, seed_path=SEED_PATH)
    if not manifest["verification"]["exact_elementwise_match"]:
        raise ValueError("reconstructed candidate grid does not match final artifact")
    OUTPUT_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
        "verification": manifest["verification"],
    }, indent=2))


if __name__ == "__main__":
    main()
