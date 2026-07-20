import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
ARTIFACT_DIR = ROOT / "artifacts" / "peak_shaving" / "20260712_expanded_response"
FINAL = ARTIFACT_DIR / "spatiotemporal_equilibrium_submission.json"
SEED = ARTIFACT_DIR / "pre_uniform_expansion/spatiotemporal_equilibrium_submission.json"


def test_candidate_manifest_reconstructs_final_grid_exactly():
    from experiments.build_submission_candidate_manifest import build_manifest

    manifest = build_manifest(final_path=FINAL, seed_path=SEED)

    assert manifest["verification"]["exact_elementwise_match"] is True
    assert manifest["verification"]["final_candidate_count"] == 1576
    assert manifest["verification"]["reconstructed_candidate_count"] == 1576


def test_candidate_manifest_reports_disjoint_increment_counts():
    from experiments.build_submission_candidate_manifest import build_manifest

    manifest = build_manifest(final_path=FINAL, seed_path=SEED)
    rows = manifest["components"]

    assert [row["added_unique_count"] for row in rows] == [
        800,
        378,
        120,
        64,
        27,
        100,
        69,
        18,
    ]
    assert [row["cumulative_unique_count"] for row in rows] == [
        800,
        1178,
        1298,
        1362,
        1389,
        1489,
        1558,
        1576,
    ]
    assert len(manifest["continuation_only_vectors"]) == 18


def test_candidate_manifest_records_source_hashes(tmp_path):
    from experiments.build_submission_candidate_manifest import build_manifest

    manifest = build_manifest(final_path=FINAL, seed_path=SEED)
    output = tmp_path / "manifest.json"
    output.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    assert len(manifest["metadata"]["final_equilibrium_sha256"]) == 64
    assert manifest["metadata"]["continuation_seed_sha256"].startswith("d3717445")
    assert set(manifest["metadata"]["source_sha256"]) == {
        "experiments/build_submission_candidate_manifest.py",
        "experiments/peak_shaving_submission_tools.py",
        "experiments/submission_candidate_design.py",
    }
    assert "generated_at" in manifest["metadata"]
    assert "command" in manifest["metadata"]
    assert json.loads(output.read_text(encoding="utf-8")) == manifest
