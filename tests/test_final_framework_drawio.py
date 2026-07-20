import hashlib
import re
from pathlib import Path
from urllib.parse import unquote_to_bytes
from xml.etree import ElementTree

from PIL import Image, ImageChops

PROJECT = Path(__file__).resolve().parents[1]
DRAWIO = PROJECT / "figure_sources" / "spatiotemporal_pricing_framework_final_2026-07-14.drawio"
FIGURE_DIR = PROJECT / "figures" / "peak_shaving_final_20260714"
PNG = FIGURE_DIR / "spatiotemporal_pricing_framework.png"
SVG = FIGURE_DIR / "spatiotemporal_pricing_framework.svg"
PDF = FIGURE_DIR / "spatiotemporal_pricing_framework.pdf"
ICON_ROOT = (
    PROJECT
    / "figure_sources"
    / "iot_icon_candidates"
    / "streamline_ultimate_color"
)


def _cells() -> dict[str, ElementTree.Element]:
    tree = ElementTree.parse(DRAWIO)
    return {cell.attrib["id"]: cell for cell in tree.findall(".//mxCell")}


def test_final_framework_contains_only_the_final_model_sequence():
    cells = _cells()
    required = {
        "market_panel",
        "solver_panel",
        "rigid_users",
        "flexible_users",
        "temporal_allocation",
        "channel_choice",
        "intermediary",
        "provider_a",
        "provider_b",
        "step_inputs",
        "step_prices",
        "step_demand",
        "step_fixed_point",
        "step_payoffs",
        "step_nash",
        "step_deviation",
        "evidence_block",
    }
    assert required <= cells.keys()
    values = "\n".join(cell.attrib.get("value", "") for cell in cells.values())
    for text in (
        "Native arrivals",
        "Conserved OD temporal allocation",
        "Within-period channel choice",
        "Fixed total demand",
        "BurstGPT load shape",
        "Measured QoS fit",
        "Audit-adaptive bounded linear",
        "Bounded continuous",
        "Complementarity mixed equilibrium",
        "Full 1,576-candidate regret",
        "Bounded off-grid search",
        "Aggregate peak",
        "Provider hotspot and QoS",
        "Profit boundary",
    ):
        assert text in values
    for obsolete in (
        "Outside option", "Channel-period logit", "Fictitious play",
        "Nashpy restricted equilibrium", "Full 225-point deviation scan",
    ):
        assert obsolete not in values


def test_final_framework_connectors_match_the_conserved_market_logic():
    cells = _cells()
    edges = [cell for cell in cells.values() if cell.attrib.get("edge") == "1"]
    pairs = {(cell.attrib.get("source"), cell.attrib.get("target")) for cell in edges}
    expected = {
        ("rigid_users", "temporal_allocation"),
        ("flexible_users", "temporal_allocation"),
        ("temporal_allocation", "channel_choice"),
        ("choice_intermediary", "intermediary"),
        ("choice_direct_a", "provider_a"),
        ("choice_direct_b", "provider_b"),
        ("intermediary", "provider_a"),
        ("intermediary", "provider_b"),
        ("step_inputs", "step_prices"),
        ("step_prices", "step_demand"),
        ("step_demand", "step_fixed_point"),
        ("step_fixed_point", "step_payoffs"),
        ("step_payoffs", "step_nash"),
        ("step_nash", "step_deviation"),
        ("step_deviation", "evidence_block"),
    }
    assert expected <= pairs
    assert cells["solver_feedback"].attrib["source"] == "step_fixed_point"
    assert cells["solver_feedback"].attrib["target"] == "step_demand"
    for edge in edges:
        assert edge.find("mxGeometry") is not None


def test_final_framework_uses_embedded_icons_and_readable_times_text():
    cells = _cells()
    visible = [cell for cell in cells.values() if cell.attrib.get("value")]
    for cell in visible:
        style = cell.attrib.get("style", "")
        assert "fontFamily=Times New Roman" in style, cell.attrib["id"]
        match = re.search(r"fontSize=(\d+)", style)
        assert match and int(match.group(1)) >= 16, cell.attrib["id"]
    images = [cell for cell in cells.values() if "shape=image" in cell.attrib.get("style", "")]
    assert len(images) >= 20
    for cell in images:
        match = re.search(r"image=(data:image/svg\+xml,([^;]+));", cell.attrib["style"])
        assert match is not None
        payload = unquote_to_bytes(match.group(2))
        assert ElementTree.fromstring(payload).tag.endswith("svg")


def test_embedded_icons_match_the_pinned_streamline_archive():
    expected_hashes = {
        line.split(maxsplit=1)[0]
        for line in (ICON_ROOT / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines()
        if line.strip()
    }
    attribution = (ICON_ROOT / "ATTRIBUTION.md").read_text(encoding="utf-8")
    assert "52d750c9ce051e51cb181b7a78932120c48541d0" in attribution
    assert "Creative Commons Attribution 4.0" in attribution
    assert (ICON_ROOT / "LICENSE-CC-BY-4.0.txt").stat().st_size > 10_000

    images = [
        cell for cell in _cells().values()
        if "shape=image" in cell.attrib.get("style", "")
    ]
    embedded_hashes = set()
    for cell in images:
        match = re.search(r"image=(data:image/svg\+xml,([^;]+));", cell.attrib["style"])
        assert match is not None
        payload = unquote_to_bytes(match.group(2))
        embedded_hashes.add(hashlib.sha256(payload).hexdigest())

    assert embedded_hashes
    assert embedded_hashes <= expected_hashes


def test_final_framework_small_text_is_readable_after_manuscript_scaling():
    cells = _cells()
    expected_minimums = {
        "rigid_users_note": 18,
        "flexible_users_note": 18,
        "od_formula": 19,
        "mass_formula": 19,
        "intermediary_formula": 19,
        "intermediary_note": 18,
        "provider_a_prices": 19,
        "provider_a_util_label": 19,
        "provider_a_qos_label": 19,
        "provider_b_prices": 19,
        "provider_b_util_label": 19,
        "provider_b_qos_label": 19,
        "step_inputs_label": 19,
        "step_prices_label": 19,
        "step_demand_label": 19,
        "step_fixed_point_label": 19,
        "step_payoffs_label": 19,
        "step_nash_label": 19,
        "step_deviation_label": 19,
        "evidence_peak": 19,
        "evidence_qos": 19,
        "evidence_profit": 19,
        "choice_to_a": 18,
        "choice_to_b": 18,
        "route_to_a": 18,
        "route_to_b": 18,
        "provider_signal_a": 18,
        "provider_signal_b": 18,
        "provider_competition": 18,
        "solver_feedback": 18,
    }
    for cell_id, minimum in expected_minimums.items():
        match = re.search(r"fontSize=(\d+)", cells[cell_id].attrib["style"])
        assert match and int(match.group(1)) >= minimum, cell_id


def test_final_framework_exports_are_nonblank_and_vector_backed():
    with Image.open(PNG) as image:
        assert image.width >= 2800
        assert image.height >= 1500
        white = Image.new("RGB", image.size, "white")
        assert ImageChops.difference(image.convert("RGB"), white).getbbox() is not None
    assert ElementTree.parse(SVG).getroot().tag.endswith("svg")
    assert SVG.stat().st_size > 100_000
    assert PDF.read_bytes().startswith(b"%PDF-")
    assert PDF.stat().st_size > 50_000


def test_final_framework_uses_restrained_sci_panel_colors():
    allowed = {
        "#191919",
        "#FFFFFF",
        "#3C5488",
        "#6F83B5",
        "#A86464",
        "#6F6F6F",
        "#E9EDF5",
        "#F0F3F8",
        "#F6ECEC",
        "#F5F5F5",
    }
    for cell in _cells().values():
        style = cell.attrib.get("style", "")
        if "shape=image" in style:
            continue
        assert set(re.findall(r"#[0-9A-Fa-f]{6}", style)) <= allowed, cell.attrib["id"]
