import hashlib
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
ARTIFACT_DIR = ROOT / "artifacts/peak_shaving/20260712_expanded_response"
BASELINE = ARTIFACT_DIR / "spatiotemporal_equilibrium_submission.json"


def _array_sha256(values: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(values).tobytes()).hexdigest()


def _active_dynamic_vectors() -> np.ndarray:
    payload = json.loads(BASELINE.read_text(encoding="utf-8"))
    game = payload["dynamic"]
    vectors = []
    for side in ("row", "col"):
        vectors.extend(
            vector
            for vector, probability in zip(
                game[f"{side}_support_vectors"], game[f"{side}_mix"]
            )
            if probability > 1e-10
        )
    return np.asarray(vectors, dtype=float)


def test_common_uniform_design_is_deterministic_and_covers_full_bounds():
    from experiments.submission_candidate_design import (
        BASE_PRICE_BOUNDS,
        UNIFORM_DIAGNOSTIC_CENTRES,
        common_uniform_provider_candidate_grid,
    )

    first = common_uniform_provider_candidate_grid()
    second = common_uniform_provider_candidate_grid()

    assert first.shape == (800, 4)
    assert np.array_equal(first, second)
    assert np.all(first[:, [1, 3]] == 0.0)
    assert np.array_equal(first[:, [0, 2]].min(axis=0), BASE_PRICE_BOUNDS[:, 0])
    assert np.array_equal(first[:, [0, 2]].max(axis=0), BASE_PRICE_BOUNDS[:, 1])
    for wholesale, direct in UNIFORM_DIAGNOSTIC_CENTRES:
        assert np.any(np.all(first == [wholesale, 0.0, direct, 0.0], axis=1))
    assert _array_sha256(first) == (
        "516080224c67b6f7ab111e69f17d2a73801a6728f16c73336893f4729cfaa5e6"
    )


def test_common_uniform_components_have_predeclared_unique_increments():
    from experiments.submission_candidate_design import (
        common_uniform_candidate_components,
    )

    accumulated = np.empty((0, 4), dtype=float)
    increments = []
    cumulative = []
    for _, values in common_uniform_candidate_components():
        combined = np.unique(np.vstack([accumulated, values]), axis=0)
        increments.append(len(combined) - len(accumulated))
        cumulative.append(len(combined))
        accumulated = combined

    assert increments == [12, 512, 114, 81, 81]
    assert cumulative == [12, 524, 638, 719, 800]


def test_augmented_design_contains_uniform_domain_and_legacy_dynamic_grid():
    from experiments.peak_shaving_submission_tools import (
        adaptive_audit_provider_candidate_grid,
    )
    from experiments.submission_candidate_design import (
        augmented_submission_provider_candidate_grid,
        common_uniform_provider_candidate_grid,
    )

    reference = _active_dynamic_vectors()
    uniform = common_uniform_provider_candidate_grid()
    legacy = adaptive_audit_provider_candidate_grid(reference)
    augmented = augmented_submission_provider_candidate_grid(reference)
    augmented_keys = {tuple(row) for row in augmented}

    assert legacy.shape == (788, 4)
    assert augmented.shape == (1576, 4)
    assert {tuple(row) for row in uniform} < augmented_keys
    assert {tuple(row) for row in legacy} < augmented_keys
    assert _array_sha256(augmented) == (
        "01db2a6b2ef32af4413f880f3317eae0076daf79c1c381aa43d65a054ac78f4d"
    )


def test_candidate_design_metadata_binds_construction_and_array_hashes():
    from experiments.submission_candidate_design import candidate_design_metadata

    metadata = candidate_design_metadata(_active_dynamic_vectors())

    assert metadata["method"] == "common_uniform_expansion_v1"
    assert metadata["uniform_candidate_count"] == 800
    assert metadata["provider_candidate_count"] == 1576
    assert metadata["lhs"] == {"seed": 20260716, "sample_count": 512}
    assert metadata["global_lattice_shape"] == [9, 13]
    assert metadata["local_lattice_shape"] == [9, 9]
    assert metadata["local_half_width_fraction"] == 0.05
    assert metadata["component_added_unique_counts"] == [12, 512, 114, 81, 81]
    assert metadata["uniform_is_strict_subset"] is True
    assert metadata["uniform_array_sha256"] == (
        "516080224c67b6f7ab111e69f17d2a73801a6728f16c73336893f4729cfaa5e6"
    )
    assert metadata["provider_array_sha256"] == (
        "01db2a6b2ef32af4413f880f3317eae0076daf79c1c381aa43d65a054ac78f4d"
    )


def test_submission_runner_uses_archived_seed_and_persistent_pair_cache():
    from experiments import run_submission_spatiotemporal_equilibrium as module

    assert module.ARCHIVED_BASELINE_PATH.parent.name == "pre_uniform_expansion"
    assert module.SEED_PATHS == (module.ARCHIVED_BASELINE_PATH,)
    assert module.PAIR_CACHE_DIR.name == "peak_shaving_uniform_expansion_baseline"
    assert not str(module.PAIR_CACHE_DIR).startswith("/tmp/")


def test_submission_sensitivity_default_cache_is_persistent():
    from experiments import run_submission_spatiotemporal_sensitivity as module

    assert module.CACHE_ROOT.name == "peak_shaving_submission_sensitivity"
    assert not str(module.CACHE_ROOT).startswith("/tmp/")


def test_submission_offgrid_default_cache_is_persistent():
    from experiments import run_spatiotemporal_offgrid_diagnostic as module

    assert module.SUBMISSION_CACHE_DIR.name == "peak_shaving_submission_offgrid"
    assert not str(module.SUBMISSION_CACHE_DIR).startswith("/tmp/")


def test_branch_audit_reads_augmented_baseline_pair_cache():
    from experiments import run_submission_equilibrium_branch_audit as module

    assert module.CACHE_PATH.parent.name == "peak_shaving_uniform_expansion_baseline"
    assert module.CACHE_PATH.name == "dynamic.pkl"
    assert not str(module.CACHE_PATH).startswith("/tmp/")
