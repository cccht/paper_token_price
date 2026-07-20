from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "peak_shaving_dynamic_pricing_SMPT_final_2026-07-12.tex"
HIGHLIGHTS = ROOT / "peak_shaving_dynamic_pricing_SMPT_highlights_2026-07-12.txt"


def _source() -> str:
    return MANUSCRIPT.read_text(encoding="utf-8")


def test_manuscript_has_exactly_five_numbered_sections():
    sections = re.findall(r"^\\section\{([^}]+)\}", _source(), flags=re.MULTILINE)

    assert sections == [
        "Introduction",
        "Related research",
        "Methodology",
        "Experimental results",
        "Conclusion and outlook",
    ]


def test_abstract_and_highlights_meet_smpt_limits():
    source = _source()
    abstract = source.split(r"\begin{abstract}", 1)[1].split(r"\end{abstract}", 1)[0]
    words = re.findall(r"[A-Za-z0-9][A-Za-z0-9.-]*", abstract)
    highlights = HIGHLIGHTS.read_text(encoding="utf-8").splitlines()

    assert len(words) <= 250
    assert 3 <= len(highlights) <= 5
    assert all(len(line) <= 85 for line in highlights)


def test_all_final_figures_exist_and_are_referenced():
    source = _source()
    figures = re.findall(r"\\includegraphics(?:\[[^]]+\])?\{([^}]+)\}", source)

    assert figures == [
        "spatiotemporal_pricing_framework.pdf",
        "input_calibration.pdf",
        "equilibrium_profiles.pdf",
        "solver_diagnostics.pdf",
        "mechanism_decomposition.pdf",
        "resolved_sensitivity.pdf",
    ]
    for figure in figures:
        assert (ROOT / "figures" / "peak_shaving_final_20260712" / figure).exists()
    for label in re.findall(r"\\label\{(fig:[^}]+)\}", source):
        assert source.count(rf"\ref{{{label}}}") >= 1


def test_citations_resolve_to_verified_bibliography():
    source = _source()
    bibliography = (ROOT / "verified_refs.bib").read_text(encoding="utf-8")
    cited = {
        key.strip()
        for group in re.findall(r"\\cite\{([^}]+)\}", source)
        for key in group.split(",")
    }
    available = set(re.findall(r"^@\w+\{([^,]+),", bibliography, flags=re.MULTILINE))

    assert cited <= available


def test_main_claims_match_final_artifact_values():
    source = _source()

    for text in ("13.03", "17.08", "0.888", "0.976", "-37.43", "+9.41"):
        assert text in source
    assert "fictitious play" not in source.lower()
    assert "continuous-space equilibrium" in source
    assert "Total demand is 1100" in source
