from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex"


def _source() -> str:
    return MANUSCRIPT.read_text(encoding="utf-8")


def test_manuscript_uses_generated_result_inputs_and_resolved_sensitivity():
    source = _source()

    assert "submission_result_macros.tex" in source
    assert "submission_sensitivity_table.tex" in source
    assert "resolved_sensitivity.pdf" in source
    assert "FINAL_SENSITIVITY_RESULTS" not in source


def test_manuscript_reports_augmented_candidate_scope_without_old_counts():
    source = _source()

    assert "1,576" in source
    assert "800" in source
    assert not re.search(r"\b788\b", source)
    assert "12 zero-slope candidates" not in source


def test_manuscript_distinguishes_uniform_and_dynamic_offgrid_evidence():
    source = _source().lower()

    assert "nine-scenario uniform-price off-grid" in source
    assert "baseline four-dimensional off-grid" in source
    assert "active-support provider-payoff" in source
    assert "continuous-strategy equilibrium" in source


def test_manuscript_removes_provisional_old_comparison_values():
    source = _source()

    for obsolete in ("12.32", "15.70", "0.890", "0.959", "2.81"):
        assert obsolete not in source
    assert "aggregate market-side profit falls in the main case" not in source
