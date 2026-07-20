from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def test_final_figure_builder_loads_augmented_numerical_audits():
    from experiments import build_final_submission_figures as module

    assert module.UNIFORM_OFFGRID_PATH.name == (
        "uniform_offgrid_sensitivity_submission.json"
    )
    assert module.INTERMEDIARY_PAYOFF_SENSITIVITY_PATH.name == (
        "intermediary_payoff_sensitivity_submission.json"
    )
    source = Path(module.__file__).read_text(encoding="utf-8")
    assert '"uniform_offgrid"' in source
    assert '"intermediary_payoff_sensitivity"' in source


def test_framework_blueprint_reports_augmented_finite_candidate_scope():
    source = (
        ROOT / "figure_sources/build_final_spatiotemporal_framework_drawio.py"
    ).read_text(encoding="utf-8")

    assert "Full 1,576-candidate regret" in source
    assert "Full 788-candidate regret" not in source
