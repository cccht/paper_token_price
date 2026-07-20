import hashlib
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def test_final_figure_builder_uses_only_final_artifacts(tmp_path):
    from experiments.build_final_submission_figures import (
        FIGURE_STEMS,
        build_all_figures,
        load_final_data,
    )

    data = load_final_data()
    paths = build_all_figures(output_dir=tmp_path, data=data)

    assert set(data) == {
        "burst_profile",
        "qos_calibration",
        "equilibrium",
        "distribution",
        "mechanism",
        "sensitivity",
        "offgrid",
        "fixed_point_audit",
        "intermediary_audit",
        "uniform_offgrid",
        "intermediary_payoff_sensitivity",
    }
    assert len(paths) == len(FIGURE_STEMS) * 2
    for stem in FIGURE_STEMS:
        pdf = tmp_path / f"{stem}.pdf"
        png = tmp_path / f"{stem}.png"
        assert pdf.exists() and pdf.stat().st_size > 5_000
        assert png.exists() and png.stat().st_size > 20_000


def test_final_figure_inputs_match_expected_experiment_dimensions():
    from experiments.build_final_submission_figures import load_final_data

    data = load_final_data()

    assert len(data["burst_profile"]) == 8
    assert len(data["qos_calibration"]["points"]) == 10
    assert data["equilibrium"]["metadata"]["full_candidate_count"] == 1576
    assert len(data["mechanism"]["rows"]) == 8
    assert len(data["sensitivity"]["rows"]) == 9
    assert data["offgrid"]["metadata"]["samples_per_player"] == 1_024
    assert data["distribution"]["dynamic"]["active_profile_count"] == 676
    assert data["fixed_point_audit"]["metadata"]["covered_probability_mass"] == pytest.approx(1.0)
    assert data["intermediary_audit"]["metadata"]["covered_probability_mass"] == pytest.approx(1.0)


def test_submission_figure_paths_do_not_use_legacy_final_directory():
    from experiments import build_final_submission_figures as figures

    assert figures.ARTIFACT.name == "20260712_expanded_response"
    assert figures.FIGURE_DIR.name == "peak_shaving_final_20260714"
    assert figures.EQUILIBRIUM_PATH.name == "spatiotemporal_equilibrium_submission.json"
    source = Path(figures.__file__).read_text(encoding="utf-8")
    assert "full_candidate_count\"] == 225" not in source


def test_dependent_artifact_must_match_current_equilibrium_hash(tmp_path):
    from experiments.build_final_submission_figures import _read_linked_json

    equilibrium = tmp_path / "equilibrium.json"
    equilibrium.write_text('{"candidate_grid": []}', encoding="utf-8")
    digest = hashlib.sha256(equilibrium.read_bytes()).hexdigest()
    linked = tmp_path / "linked.json"
    linked.write_text(json.dumps({"metadata": {"equilibrium_sha256": digest}}), encoding="utf-8")

    assert _read_linked_json(linked, equilibrium)["metadata"]["equilibrium_sha256"] == digest

    linked.write_text(json.dumps({"metadata": {"equilibrium_sha256": "0" * 64}}), encoding="utf-8")
    with pytest.raises(ValueError, match="equilibrium SHA-256"):
        _read_linked_json(linked, equilibrium)


def test_final_figures_use_one_restrained_sci_palette():
    from experiments import build_final_submission_figures as figures

    assert figures.SCI_PALETTE == {
        "primary": "#3C5488",
        "secondary": "#6F83B5",
        "contrast": "#A86464",
        "neutral": "#7A7A7A",
        "light": "#B8C4D9",
    }
    assert len(set(figures.MECHANISM_COLORS)) == 3
    assert set(figures.SENSITIVITY_COLORS) == {
        figures.SCI_PALETTE["neutral"],
        figures.SCI_PALETTE["primary"],
        figures.SCI_PALETTE["contrast"],
    }
    source = Path(figures.__file__).read_text(encoding="utf-8")
    for obsolete in ("#E64B35", "#00A087", "#F2B701", "#4DBBD5", "#91D1C2"):
        assert obsolete not in source


def test_final_figure_labels_use_american_english():
    from experiments import build_final_submission_figures as figures
    from experiments import plot_style

    source = Path(figures.__file__).read_text(encoding="utf-8")
    source += Path(plot_style.__file__).read_text(encoding="utf-8")

    for british in (
        "Normalised concurrency",
        "Provider utilisation",
        "Max. utilisation change",
        "Normalised end-user price",
    ):
        assert british not in source
    for american in (
        "Normalized concurrency",
        "Provider utilization",
        "Max. utilization change",
        "Normalized end-user price",
    ):
        assert american in source


def test_sensitivity_figure_accepts_submission_summary_field_names(tmp_path):
    from experiments.build_submission_sensitivity_table import SCENARIO_ORDER
    from experiments.build_final_submission_figures import (
        SENSITIVITY_FACTOR_LABELS,
        _resolved_sensitivity,
    )

    row = {
        "aggregate_peak_change_percent": -10.0,
        "maximum_provider_utilization_change_percent": -12.0,
        "minimum_provider_qos_change": 0.05,
        "market_profit_change_percent": -2.0,
    }

    rows = [{**row, "scenario": scenario} for scenario in SCENARIO_ORDER]
    paths = _resolved_sensitivity({"sensitivity": {"rows": rows}}, tmp_path)

    assert SENSITIVITY_FACTOR_LABELS == (
        "Baseline",
        "$G$",
        "$\\alpha$",
        "$\\kappa$",
        "$\\bar{u}$",
    )
    assert all(path.exists() for path in paths)


def test_sensitivity_figure_rejects_wrong_scenario_order(tmp_path):
    from experiments.build_submission_sensitivity_table import SCENARIO_ORDER
    from experiments.build_final_submission_figures import _resolved_sensitivity

    rows = [
        {
            "scenario": scenario,
            "aggregate_peak_change_percent": -10.0,
            "maximum_provider_utilization_change_percent": -12.0,
            "minimum_provider_qos_change": 0.05,
            "market_profit_change_percent": -2.0,
        }
        for scenario in reversed(SCENARIO_ORDER)
    ]

    with pytest.raises(ValueError, match="scenario order"):
        _resolved_sensitivity({"sensitivity": {"rows": rows}}, tmp_path)


def test_qos_error_bars_convert_five_repeat_normal_intervals_to_student_t():
    from experiments import build_final_submission_figures as figures

    assert figures.QOS_CI95_SCALE == pytest.approx(2.7764451051977987 / 1.96)


def test_equilibrium_figure_reports_uniform_and_dynamic_end_user_prices():
    import matplotlib.pyplot as plt
    import numpy as np

    from experiments.build_final_submission_figures import _plot_end_user_prices

    periods = np.arange(1, 4)
    uniform = {
        "retail_price": [0.9, 0.9, 0.9],
        "direct_price": [[0.6, 0.6, 0.6], [0.6, 0.6, 0.6]],
    }
    dynamic = {
        "retail_price": [0.7, 0.8, 0.9],
        "direct_price": [[0.5, 0.6, 0.7], [0.55, 0.65, 0.75]],
    }
    fig, ax = plt.subplots()

    _plot_end_user_prices(ax, periods, uniform, dynamic)

    labels = [line.get_label() for line in ax.lines]
    plt.close(fig)
    assert labels == [
        "Intermediary, uniform",
        "Direct, uniform",
        "Intermediary, dynamic",
        "Direct A, dynamic",
        "Direct B, dynamic",
    ]
