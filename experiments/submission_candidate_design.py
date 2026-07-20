"""Deterministic common candidate design for the augmented submission games."""
from __future__ import annotations

import hashlib

import numpy as np
from scipy.stats import qmc

from experiments.peak_shaving_submission_tools import (
    adaptive_audit_provider_candidate_grid,
    second_audit_enriched_provider_candidate_grid,
)


BASE_PRICE_BOUNDS = np.array([[0.25, 0.90], [0.45, 2.10]])
UNIFORM_DIAGNOSTIC_CENTRES = np.array([
    [0.5749170632537669, 0.6136488523190929],
    [0.4978125, 0.76625],
])
UNIFORM_LHS_SEED = 20260716
UNIFORM_LHS_SAMPLES = 512
GLOBAL_LATTICE_SHAPE = (9, 13)
LOCAL_LATTICE_SHAPE = (9, 9)
LOCAL_HALF_WIDTH_FRACTION = 0.05


def _array_sha256(values: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(values).tobytes()).hexdigest()


def _uniform_anchors() -> np.ndarray:
    base = second_audit_enriched_provider_candidate_grid()
    mask = np.isclose(base[:, 1], 0.0) & np.isclose(base[:, 3], 0.0)
    return base[mask]


def _uniform_latin_hypercube() -> np.ndarray:
    unit = qmc.LatinHypercube(d=2, seed=UNIFORM_LHS_SEED).random(
        UNIFORM_LHS_SAMPLES
    )
    points = qmc.scale(unit, BASE_PRICE_BOUNDS[:, 0], BASE_PRICE_BOUNDS[:, 1])
    zeros = np.zeros(UNIFORM_LHS_SAMPLES)
    return np.column_stack([points[:, 0], zeros, points[:, 1], zeros])


def _uniform_global_lattice() -> np.ndarray:
    wholesale = np.linspace(*BASE_PRICE_BOUNDS[0], GLOBAL_LATTICE_SHAPE[0])
    direct = np.linspace(*BASE_PRICE_BOUNDS[1], GLOBAL_LATTICE_SHAPE[1])
    return np.asarray([
        (wholesale_base, 0.0, direct_base, 0.0)
        for wholesale_base in wholesale
        for direct_base in direct
    ])


def _uniform_local_lattice(centre: np.ndarray) -> np.ndarray:
    spans = BASE_PRICE_BOUNDS[:, 1] - BASE_PRICE_BOUNDS[:, 0]
    axes = [
        np.linspace(
            centre[index] - LOCAL_HALF_WIDTH_FRACTION * spans[index],
            centre[index] + LOCAL_HALF_WIDTH_FRACTION * spans[index],
            LOCAL_LATTICE_SHAPE[index],
        )
        for index in range(2)
    ]
    return np.asarray([
        (wholesale_base, 0.0, direct_base, 0.0)
        for wholesale_base in axes[0]
        for direct_base in axes[1]
    ])


def common_uniform_candidate_components() -> tuple[tuple[str, np.ndarray], ...]:
    """Return the declared uniform components in deterministic union order."""
    return (
        ("legacy_uniform_anchors", _uniform_anchors()),
        ("latin_hypercube", _uniform_latin_hypercube()),
        ("global_lattice", _uniform_global_lattice()),
        ("local_lattice_primary", _uniform_local_lattice(UNIFORM_DIAGNOSTIC_CENTRES[0])),
        ("local_lattice_secondary", _uniform_local_lattice(UNIFORM_DIAGNOSTIC_CENTRES[1])),
    )


def common_uniform_provider_candidate_grid() -> np.ndarray:
    """Build the 800-rule zero-slope game shared by all scenarios."""
    components = [values for _, values in common_uniform_candidate_components()]
    return np.unique(np.vstack(components), axis=0)


def augmented_submission_provider_candidate_grid(
    reference_vectors: np.ndarray | list[list[float]],
) -> np.ndarray:
    """Merge the legacy dynamic grid with the full uniform comparison domain."""
    reference = np.asarray(reference_vectors, dtype=float)
    legacy = adaptive_audit_provider_candidate_grid(reference)
    uniform = common_uniform_provider_candidate_grid()
    return np.unique(np.vstack([legacy, uniform]), axis=0)


def _component_increments() -> tuple[list[int], list[int]]:
    accumulated = np.empty((0, 4), dtype=float)
    increments, cumulative = [], []
    for _, values in common_uniform_candidate_components():
        combined = np.unique(np.vstack([accumulated, values]), axis=0)
        increments.append(int(len(combined) - len(accumulated)))
        cumulative.append(int(len(combined)))
        accumulated = combined
    return increments, cumulative


def candidate_design_metadata(
    reference_vectors: np.ndarray | list[list[float]],
) -> dict:
    """Describe and bind the exact arrays used by the augmented games."""
    uniform = common_uniform_provider_candidate_grid()
    augmented = augmented_submission_provider_candidate_grid(reference_vectors)
    increments, cumulative = _component_increments()
    return {
        "method": "common_uniform_expansion_v1",
        "uniform_candidate_count": int(len(uniform)),
        "provider_candidate_count": int(len(augmented)),
        "lhs": {"seed": UNIFORM_LHS_SEED, "sample_count": UNIFORM_LHS_SAMPLES},
        "global_lattice_shape": list(GLOBAL_LATTICE_SHAPE),
        "local_lattice_shape": list(LOCAL_LATTICE_SHAPE),
        "local_half_width_fraction": LOCAL_HALF_WIDTH_FRACTION,
        "component_added_unique_counts": increments,
        "component_cumulative_unique_counts": cumulative,
        "uniform_is_strict_subset": len(uniform) < len(augmented),
        "uniform_array_sha256": _array_sha256(uniform),
        "provider_array_sha256": _array_sha256(augmented),
    }
