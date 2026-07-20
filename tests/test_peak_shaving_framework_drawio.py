import re
from pathlib import Path
from urllib.parse import unquote_to_bytes
from xml.etree import ElementTree

from PIL import Image, ImageChops


PROJECT = Path(__file__).resolve().parents[1]
DRAWIO = PROJECT / "figure_sources" / "peak_shaving_framework_2026-07-11.drawio"
PREVIEW_PNG = PROJECT / "figures" / "peak_shaving_framework_2026-07-11.png"
EXPORT_SVG = PROJECT / "figures" / "peak_shaving_framework_2026-07-11.svg"
EXPORT_PDF = PROJECT / "figures" / "peak_shaving_framework_2026-07-11.pdf"


def cells_by_id() -> dict[str, ElementTree.Element]:
    tree = ElementTree.parse(DRAWIO)
    return {cell.attrib["id"]: cell for cell in tree.findall(".//mxCell")}


def absolute_top(cells: dict[str, ElementTree.Element], cell_id: str) -> float:
    top = 0.0
    cell = cells[cell_id]
    while cell is not None:
        geometry = cell.find("mxGeometry")
        if geometry is not None:
            top += float(geometry.attrib.get("y", 0))
        cell = cells.get(cell.attrib.get("parent", ""))
    return top


def edge_endpoint_y(cells: dict[str, ElementTree.Element], edge_id: str, source: bool) -> float:
    edge = cells[edge_id]
    endpoint_id = edge.attrib["source" if source else "target"]
    geometry = cells[endpoint_id].find("mxGeometry")
    assert geometry is not None
    anchor = "exitY" if source else "entryY"
    match = re.search(rf"{anchor}=([0-9.]+)", edge.attrib["style"])
    assert match is not None
    return absolute_top(cells, endpoint_id) + float(geometry.attrib["height"]) * float(match.group(1))


def test_drawio_contains_required_market_and_solver_nodes() -> None:
    cells = cells_by_id()
    required = {
        "market_panel",
        "solver_panel",
        "rigid_users",
        "flexible_users",
        "channel_choice",
        "choice_intermediary",
        "choice_direct_a",
        "choice_direct_b",
        "choice_exit",
        "intermediary",
        "provider_a",
        "provider_b",
        "outside_option",
        "step_price_grids",
        "step_intermediary",
        "step_user_choice",
        "step_fixed_point",
        "step_payoff_matrix",
        "step_solver",
        "evidence_block",
    }
    assert required <= cells.keys()

    values = "\n".join(cell.attrib.get("value", "") for cell in cells.values())
    for text in (
        "Time-rigid users",
        "Time-flexible users",
        "API intermediary",
        "Provider A",
        "Provider B",
        "<i>G</i><sub>A</sub> &gt; <i>G</i><sub>B</sub>",
        "Fictitious play",
        "Double oracle",
        "Finite-grid regret",
        "QoS protection",
        "Profit boundary",
    ):
        assert text in values


def test_connectors_preserve_market_and_feedback_semantics() -> None:
    cells = cells_by_id()
    edges = [cell for cell in cells.values() if cell.attrib.get("edge") == "1"]
    pairs = {(cell.attrib.get("source"), cell.attrib.get("target")) for cell in edges}
    expected_pairs = {
        ("rigid_users", "channel_choice"),
        ("flexible_users", "channel_choice"),
        ("choice_intermediary", "intermediary"),
        ("choice_direct_a", "provider_a"),
        ("choice_direct_b", "provider_b"),
        ("choice_exit", "outside_option"),
        ("intermediary", "provider_a"),
        ("intermediary", "provider_b"),
        ("step_price_grids", "step_intermediary"),
        ("step_intermediary", "step_user_choice"),
        ("step_user_choice", "step_fixed_point"),
        ("step_fixed_point", "step_payoff_matrix"),
        ("step_payoff_matrix", "step_solver"),
        ("step_solver", "evidence_block"),
    }
    assert expected_pairs <= pairs

    for edge in edges:
        assert edge.attrib.get("source") in cells
        assert edge.attrib.get("target") in cells
        assert edge.find("mxGeometry") is not None

    for edge_id in ("signal_direct_a", "signal_direct_b", "signal_wholesale_a", "signal_wholesale_b", "solver_feedback"):
        assert "dashed=1" in cells[edge_id].attrib["style"]
    for edge_id in ("traffic_to_intermediary", "traffic_direct_a", "traffic_direct_b", "route_to_a", "route_to_b"):
        assert "dashed=1" not in cells[edge_id].attrib["style"]

    feedback = cells["solver_feedback"]
    assert feedback.attrib["source"] == "step_fixed_point"
    assert feedback.attrib["target"] == "step_user_choice"


def test_forward_connectors_are_straight() -> None:
    cells = cells_by_id()
    edges = [cell for cell in cells.values() if cell.attrib.get("edge") == "1"]

    for edge in edges:
        style = edge.attrib["style"]
        geometry = edge.find("mxGeometry")
        assert geometry is not None
        if edge.attrib["id"] == "solver_feedback":
            assert "edgeStyle=orthogonalEdgeStyle" in style
            assert geometry.find("Array") is not None
            continue

        assert "edgeStyle=none" in style
        assert "rounded=0" in style
        assert geometry.find("Array") is None


def test_solver_sequence_matches_the_manuscript() -> None:
    cells = cells_by_id()
    values = "\n".join(cell.attrib.get("value", "") for cell in cells.values())

    for text in (
        "Provider price-shape candidates",
        "Intermediary response grid",
        "Channel-period logit choice",
        "Joint routing-QoS fixed point",
        "Intermediary best response",
        "Provider payoff matrix",
        "Fictitious play",
        "Double oracle",
    ):
        assert text in values


def test_solver_to_evidence_arrow_is_horizontal() -> None:
    cells = cells_by_id()
    source_y = edge_endpoint_y(cells, "solver_to_evidence", True)
    target_y = edge_endpoint_y(cells, "solver_to_evidence", False)
    assert abs(source_y - target_y) <= 0.5


def test_parallel_formula_labels_have_vertical_clearance() -> None:
    cells = cells_by_id()
    pairs = (
        ("signal_direct_a", "traffic_direct_a"),
        ("traffic_direct_a", "route_to_a"),
        ("route_to_a", "signal_wholesale_a"),
        ("route_to_b", "signal_wholesale_b"),
        ("signal_wholesale_b", "signal_direct_b"),
        ("signal_direct_b", "traffic_direct_b"),
    )
    for first_id, second_id in pairs:
        first_source = edge_endpoint_y(cells, first_id, True)
        first_target = edge_endpoint_y(cells, first_id, False)
        second_source = edge_endpoint_y(cells, second_id, True)
        second_target = edge_endpoint_y(cells, second_id, False)
        assert abs(first_source - first_target) <= 0.5, first_id
        assert abs(second_source - second_target) <= 0.5, second_id
        first_level = (first_source + first_target) / 2
        second_level = (second_source + second_target) / 2
        assert abs(first_level - second_level) >= 40, (first_id, second_id)


def test_provider_notation_matches_manuscript() -> None:
    cells = cells_by_id()
    values = "\n".join(cell.attrib.get("value", "") for cell in cells.values())

    expected_markup = {
        "capacity_order": ("<i>G</i><sub>A</sub>", "<i>G</i><sub>B</sub>"),
        "intermediary_price": ("<i>p</i><sub>t</sub>",),
        "provider_a_prices": ("<i>w</i><sub>A,t</sub>", "<i>p</i><sup>D</sup><sub>A,t</sub>"),
        "provider_a_capacity": ("<i>G</i><sub>A</sub>",),
        "provider_a_util_label": ("<i>u</i><sub>A,t</sub>", "<i>L</i><sub>A,t</sub>", "<i>G</i><sub>A</sub>"),
        "provider_a_qos_label": ("<i>q</i><sub>A,t</sub>", "<i>Q</i>(<i>u</i><sub>A,t</sub>)"),
        "provider_b_prices": ("<i>w</i><sub>B,t</sub>", "<i>p</i><sup>D</sup><sub>B,t</sub>"),
        "provider_b_capacity": ("<i>G</i><sub>B</sub>",),
        "provider_b_util_label": ("<i>u</i><sub>B,t</sub>", "<i>L</i><sub>B,t</sub>", "<i>G</i><sub>B</sub>"),
        "provider_b_qos_label": ("<i>q</i><sub>B,t</sub>", "<i>Q</i>(<i>u</i><sub>B,t</sub>)"),
        "route_to_a": ("<i>r</i><sub>A,t</sub>", "<i>D</i><sup>I</sup><sub>t</sub>"),
        "route_to_b": ("<i>r</i><sub>B,t</sub>", "<i>D</i><sup>I</sup><sub>t</sub>"),
        "traffic_direct_a": ("<i>D</i><sup>D</sup><sub>A,t</sub>",),
        "traffic_direct_b": ("<i>D</i><sup>D</sup><sub>B,t</sub>",),
        "signal_direct_a": ("<i>p</i><sup>D</sup><sub>A,t</sub>", "<i>q</i><sub>A,t</sub>"),
        "signal_direct_b": ("<i>p</i><sup>D</sup><sub>B,t</sub>", "<i>q</i><sub>B,t</sub>"),
        "signal_retail": ("<i>p</i><sub>t</sub>", "<i>q</i><sup>I</sup><sub>t</sub>"),
        "signal_wholesale_a": ("<i>w</i><sub>A,t</sub>", "<i>q</i><sub>A,t</sub>"),
        "signal_wholesale_b": ("<i>w</i><sub>B,t</sub>", "<i>q</i><sub>B,t</sub>"),
    }
    for cell_id, fragments in expected_markup.items():
        for fragment in fragments:
            assert fragment in cells[cell_id].attrib["value"]

    for text in ("w_A,t", "p^D_A,t", "u_A,t", "w_B,t", "p^D_B,t", "u_B,t", "w_a,t", "G_a", "w_b,t", "G_b"):
        assert text not in values


def test_visible_text_uses_times_new_roman_and_readable_sizes() -> None:
    cells = cells_by_id()
    visible = [cell for cell in cells.values() if cell.attrib.get("value")]

    for cell in visible:
        style = cell.attrib.get("style", "")
        assert "fontFamily=Times New Roman" in style, cell.attrib["id"]
        match = re.search(r"fontSize=(\d+)", style)
        assert match is not None, cell.attrib["id"]
        assert int(match.group(1)) >= 16, cell.attrib["id"]

    for cell_id in (
        "capacity_order",
        "provider_a_prices",
        "provider_a_capacity",
        "provider_a_util_label",
        "provider_a_qos_label",
        "provider_b_prices",
        "provider_b_capacity",
        "provider_b_util_label",
        "provider_b_qos_label",
    ):
        match = re.search(r"fontSize=(\d+)", cells[cell_id].attrib["style"])
        assert match is not None
        assert int(match.group(1)) >= 18, cell_id

    for cell_id in ("market_title", "solver_title"):
        match = re.search(r"fontSize=(\d+)", cells[cell_id].attrib["style"])
        assert match is not None
        assert int(match.group(1)) >= 26, cell_id


def test_drawio_embeds_local_streamline_icons_as_svg() -> None:
    cells = cells_by_id()
    image_cells = [cell for cell in cells.values() if "shape=image" in cell.attrib.get("style", "")]
    assert len(image_cells) >= 24

    for cell in image_cells:
        style = cell.attrib["style"]
        match = re.search(r"image=(data:image/svg\+xml,([^;]+));", style)
        assert match is not None, cell.attrib["id"]
        payload = unquote_to_bytes(match.group(2))
        root = ElementTree.fromstring(payload)
        assert root.tag.endswith("svg")
        assert root.attrib.get("viewBox")
        assert b"<script" not in payload
        assert b'href="http' not in payload


def test_exports_are_nonblank_and_publication_sized() -> None:
    with Image.open(PREVIEW_PNG) as image:
        assert image.width >= 2800
        assert image.height >= 1500
        assert 1.45 <= image.width / image.height <= 1.9
        white = Image.new("RGB", image.size, "white")
        difference = ImageChops.difference(image.convert("RGB"), white)
        assert difference.getbbox() is not None
        colors = image.convert("RGB").getcolors(maxcolors=image.width * image.height)
        assert colors is not None
        assert len(colors) >= 80

    svg_root = ElementTree.parse(EXPORT_SVG).getroot()
    assert svg_root.tag.endswith("svg")
    assert EXPORT_SVG.stat().st_size > 100_000
    assert EXPORT_PDF.read_bytes().startswith(b"%PDF-")
    assert EXPORT_PDF.stat().st_size > 50_000
