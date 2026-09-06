"""Create and verify a scoped, self-contained new-game archive, copy-first."""
from __future__ import annotations

import hashlib
import json
import zipfile

from experiments.run_user_provider_game import OUT, ROOT


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def members():
    exp = json.loads((OUT / "experiment.json").read_text())
    paths = {ROOT / path for path in exp["metadata"]["source_sha256"]}
    for path in (
        "requirements.txt", "requirements-user-game-20260906.txt", "experiments/__init__.py", "pricing_sim/__init__.py", "pricing_sim/config.py",
        "pricing_sim/peak_shaving_config.py", "experiments/plot_style.py",
        "experiments/report_user_provider_game.py", "experiments/plot_user_provider_game.py",
        "experiments/verify_user_provider_game.py", "experiments/check_user_game_document.py",
        "experiments/package_user_provider_game.py", "experiments/build_burstgpt_load_anchor.py",
        "experiments/build_final_qos_calibration.py",
        "figure_sources/build_user_game_framework.py", "figure_sources/build_iot_framework.py",
        "figure_sources/build_peak_shaving_framework_drawio.py", "figure_sources/user_game_framework_20260906.drawio",
        "llm_user_provider_game_2026-09-06.tex", "llm_user_provider_game_2026-09-06.pdf", "verified_refs.bib",
        "tests/test_user_time_game.py", "tests/test_user_provider_pricing.py", "tests/test_user_provider_artifacts.py",
        "docs/reviews/user_provider_figure_contract_2026-09-06.md", "docs/reviews/user_provider_visual_review_2026-09-06.md",
        "docs/reviews/user_provider_bundle_readme_2026-09-06.md",
        "artifacts/peak_shaving/20260619_submission/vllm_qos_anchor_points.csv",
        "artifacts/peak_shaving/20260619_submission/vllm_qos_anchor_summary.json",
    ):
        paths.add(ROOT / path)
    for folder in (ROOT / "data/processed/burstgpt_d895a53b_8period", ROOT / "figure_sources/llm_user_framework_assets",
                   ROOT / "figures/user_provider_game_20260906", OUT / "document_preview"):
        paths.update(p for p in folder.iterdir() if p.is_file())
    paths.update(p for p in OUT.iterdir() if p.is_file() and p.suffix in (".json", ".csv", ".tex", ".md")
                 and p.name not in ("bundle_manifest.json", "bundle_verification.json"))
    result = {str(p.relative_to(ROOT)): p for p in sorted(paths)}
    result["README.md"] = ROOT / "docs/reviews/user_provider_bundle_readme_2026-09-06.md"
    return result


def main():
    experiment = OUT / "experiment.json"
    data = json.loads(experiment.read_text())
    certificate = json.loads((OUT / "verification.json").read_text())
    assert certificate["passed"] and certificate["experiment_sha256"] == sha(experiment)
    assert certificate["validator_sha256"] == sha(ROOT / "experiments/verify_user_provider_game.py")
    for path, digest in data["metadata"]["source_sha256"].items():
        assert sha(ROOT / path) == digest
    document = json.loads((OUT / "document_checks.json").read_text())
    assert document["automated_checks_passed"]
    assert document["pdf_sha256"] == sha(ROOT / "llm_user_provider_game_2026-09-06.pdf")
    assert document["tex_sha256"] == sha(ROOT / "llm_user_provider_game_2026-09-06.tex")
    files = members()
    manifest = {"scope": "Only the explicit new atomic user/manufacturer game and its reproduction inputs",
                "experiment_sha256": sha(experiment), "files": {
                    name: {"source": str(path.relative_to(ROOT)), "sha256": sha(path), "bytes": path.stat().st_size}
                    for name, path in files.items()}}
    payload = json.dumps(manifest, indent=2) + "\n"
    (OUT / "bundle_manifest.json").write_text(payload)
    archive = OUT / "reproducible_bundle.zip"
    temporary = archive.with_suffix(".zip.tmp")
    with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for name, path in files.items():
            bundle.write(path, name)
        bundle.writestr("bundle_manifest.json", payload)
    with zipfile.ZipFile(temporary) as bundle:
        assert bundle.testzip() is None
        for name, record in manifest["files"].items():
            assert hashlib.sha256(bundle.read(name)).hexdigest() == record["sha256"]
            assert sha(ROOT / record["source"]) == record["sha256"]
    temporary.replace(archive)
    report = {"passed": True, "members_verified": len(files), "zip_sha256": sha(archive),
              "zip_bytes": archive.stat().st_size, "experiment_sha256": sha(experiment),
              "manifest_sha256": sha(OUT / "bundle_manifest.json"),
              "scope": "Every archive member checked against source SHA; originals preserved"}
    (OUT / "bundle_verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
