#!/usr/bin/env python3
"""Build the editable framework figure for the peak-shaving manuscript."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import quote

PROJECT = Path(__file__).resolve().parents[1]
ICON_ROOT = PROJECT / "figure_sources" / "iot_icon_candidates" / "streamline_ultimate_color"
OUTPUT = PROJECT / "figure_sources" / "peak_shaving_framework_2026-07-11.drawio"

INK = "#191919"
CYAN = "#168AA8"
CYAN_FILL = "#EAFBFF"
YELLOW = "#B98513"
YELLOW_FILL = "#FFF9D6"
CORAL = "#C94F5B"
CORAL_FILL = "#FFF0F2"
GREEN = "#238B45"
GREEN_FILL = "#ECFBEF"
GRAY = "#667085"
GRAY_FILL = "#F7F8FA"
WHITE = "#FFFFFF"

FONT = "fontFamily=Times New Roman;fontColor=#191919;"
PANEL = (
    "rounded=1;whiteSpace=wrap;html=1;container=1;pointerEvents=0;"
    "fillColor=#FFFFFF;strokeColor=#191919;strokeWidth=1.8;dashed=1;"
    "dashPattern=9 7;arcSize=6;"
)
BOX = (
    "rounded=1;whiteSpace=wrap;html=1;container=1;pointerEvents=1;"
    "strokeWidth=1.5;arcSize=6;"
)
TEXT = (
    "text;html=1;strokeColor=none;fillColor=none;whiteSpace=wrap;"
    "align=center;verticalAlign=middle;"
)

def math_var(symbol: str, subscript: str = "", superscript: str = "") -> str:
    """Return a compact HTML math label supported by Draw.io exports."""
    value = f"<i>{symbol}</i>"
    if superscript:
        value += f"<sup>{superscript}</sup>"
    if subscript:
        value += f"<sub>{subscript}</sub>"
    return value

def svg_data_uri(relative_path: str) -> str:
    payload = (ICON_ROOT / relative_path).read_text(encoding="utf-8")
    return f"data:image/svg+xml,{quote(payload, safe='')}"


class Diagram:
    def __init__(self) -> None:
        self.mxfile = ET.Element(
            "mxfile",
            host="Electron",
            modified="2026-07-11T03:55:00.000Z",
            agent="Codex drawio-skill",
            version="30.3.6",
            type="device",
        )
        diagram = ET.SubElement(self.mxfile, "diagram", id="peak-shaving-framework", name="Page-1")
        model = ET.SubElement(
            diagram,
            "mxGraphModel",
            dx="1900",
            dy="1160",
            grid="1",
            gridSize="10",
            guides="1",
            tooltips="1",
            connect="1",
            arrows="1",
            fold="1",
            page="1",
            pageScale="1",
            pageWidth="1900",
            pageHeight="1160",
            math="0",
            shadow="0",
        )
        self.root = ET.SubElement(model, "root")
        ET.SubElement(self.root, "mxCell", id="0")
        ET.SubElement(self.root, "mxCell", id="1", parent="0")

    def vertex(self, cell_id: str, value: str, style: str, geometry: tuple[float, float, float, float], parent: str = "1") -> ET.Element:
        cell = ET.SubElement(
            self.root,
            "mxCell",
            id=cell_id,
            value=value,
            style=style,
            vertex="1",
            parent=parent,
        )
        x, y, width, height = geometry
        ET.SubElement(
            cell,
            "mxGeometry",
            x=str(x),
            y=str(y),
            width=str(width),
            height=str(height),
            **{"as": "geometry"},
        )
        return cell

    def text(self, cell_id: str, value: str, geometry: tuple[float, float, float, float], parent: str = "1", size: int = 16, bold: bool = False, color: str = INK, align: str = "center") -> ET.Element:
        bold_style = "fontStyle=1;" if bold else ""
        style = f"{TEXT}{FONT}fontSize={size};fontColor={color};{bold_style}align={align};"
        return self.vertex(cell_id, value, style, geometry, parent)

    def box(self, cell_id: str, value: str, geometry: tuple[float, float, float, float], parent: str, fill: str, stroke: str, size: int = 18) -> ET.Element:
        style = f"{BOX}{FONT}fillColor={fill};strokeColor={stroke};fontSize={size};"
        return self.vertex(cell_id, value, style, geometry, parent)

    def icon(self, cell_id: str, relative_path: str, geometry: tuple[float, float, float, float], parent: str) -> ET.Element:
        style = (
            "shape=image;html=1;imageAspect=0;aspect=fixed;strokeColor=none;"
            "fillColor=none;verticalLabelPosition=bottom;verticalAlign=top;align=center;"
            f"image={svg_data_uri(relative_path)};"
        )
        return self.vertex(cell_id, "", style, geometry, parent)

    def edge(self, cell_id: str, source: str, target: str, parent: str, value: str = "", dashed: bool = False, both: bool = False, color: str = INK, points: tuple[tuple[float, float], ...] = (), anchors: str = "", orthogonal: bool = False, size: int = 16) -> ET.Element:
        dash = "dashed=1;dashPattern=7 5;" if dashed else ""
        start = "startArrow=classicThin;startFill=1;" if both else "startArrow=none;"
        edge_layout = (
            "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;"
            if orthogonal
            else "edgeStyle=none;rounded=0;"
        )
        style = (
            f"{edge_layout}html=1;endArrow=classicThin;endFill=1;strokeWidth=2;"
            f"strokeColor={color};{dash}{start}{FONT}fontSize={size};"
            f"labelBackgroundColor=#FFFFFF;{anchors}"
        )
        cell = ET.SubElement(
            self.root,
            "mxCell",
            id=cell_id,
            value=value,
            style=style,
            edge="1",
            parent=parent,
            source=source,
            target=target,
        )
        geometry = ET.SubElement(cell, "mxGeometry", relative="1", **{"as": "geometry"})
        if points:
            array = ET.SubElement(geometry, "Array", **{"as": "points"})
            for x, y in points:
                ET.SubElement(array, "mxPoint", x=str(x), y=str(y))
        return cell

    def save(self) -> None:
        tree = ET.ElementTree(self.mxfile)
        ET.indent(tree, space="  ")
        tree.write(OUTPUT, encoding="utf-8", xml_declaration=True)

def add_user_group(diagram: Diagram, cell_id: str, title: str, note: str, y: int, fill: str, stroke: str, icons: tuple[str, str, str]) -> None:
    diagram.box(cell_id, "", (25, y, 285, 225), "market_panel", fill, stroke)
    diagram.text(f"{cell_id}_title", title, (18, 12, 249, 38), cell_id, 22, True, stroke)
    for index, icon_path in enumerate(icons):
        diagram.icon(f"{cell_id}_icon_{index}", icon_path, (20 + index * 88, 58, 70, 70), cell_id)
    diagram.text(f"{cell_id}_note", note, (15, 142, 255, 62), cell_id, 16, False, INK)

def add_choice_box(diagram: Diagram) -> None:
    diagram.box("channel_choice", "", (360, 85, 300, 540), "market_panel", GRAY_FILL, GRAY)
    diagram.text("choice_title", "Channel-period choice", (15, 12, 270, 44), "channel_choice", 22, True)
    choices = (
        ("choice_direct_a", "Direct Provider A", "svg/market_actors/direct_user.svg", 75, GREEN_FILL, GREEN),
        ("choice_intermediary", "API intermediary", "svg/api_routing/server_sharing.svg", 175, CYAN_FILL, CYAN),
        ("choice_direct_b", "Direct Provider B", "svg/market_actors/direct_user.svg", 365, YELLOW_FILL, YELLOW),
        ("choice_exit", "Outside option", "svg/market_actors/market_exit.svg", 455, CORAL_FILL, CORAL),
    )
    for cell_id, label, icon_path, y, fill, stroke in choices:
        diagram.box(cell_id, "", (25, y, 250, 70), "channel_choice", fill, stroke, 16)
        diagram.icon(f"{cell_id}_icon", icon_path, (10, 10, 48, 48), cell_id)
        diagram.text(f"{cell_id}_label", label, (62, 12, 178, 46), cell_id, 18, True, stroke, "left")

def add_intermediary(diagram: Diagram) -> None:
    diagram.box("intermediary", "", (760, 240, 320, 200), "market_panel", CYAN_FILL, CYAN)
    diagram.text("intermediary_title", "API intermediary", (20, 8, 280, 38), "intermediary", 22, True, CYAN)
    diagram.icon("intermediary_server", "svg/api_routing/server_sharing.svg", (58, 48, 68, 68), "intermediary")
    diagram.icon("intermediary_split", "svg/api_routing/flow_split.svg", (205, 53, 58, 58), "intermediary")
    diagram.text("intermediary_price", f"Retail price {math_var('p', 't')}", (25, 116, 270, 27), "intermediary", 18, True)
    diagram.text("intermediary_route", "Routes by wholesale price and QoS", (20, 144, 280, 28), "intermediary", 16)
    diagram.box("outside_option", "", (795, 530, 250, 90), "market_panel", CORAL_FILL, CORAL)
    diagram.icon("outside_icon", "svg/market_actors/market_exit.svg", (18, 14, 58, 58), "outside_option")
    diagram.text("outside_label", "No purchase / exit", (78, 18, 155, 49), "outside_option", 19, True, CORAL)

def add_provider(diagram: Diagram, suffix: str, y: int, title: str, fill: str, stroke: str, server_icon: str) -> None:
    provider = f"provider_{suffix}"
    notation = suffix.upper()
    wholesale_price = math_var("w", f"{notation},t")
    direct_price = math_var("p", f"{notation},t", "D")
    utilization = math_var("u", f"{notation},t")
    load = math_var("L", f"{notation},t")
    capacity_symbol = math_var("G", notation)
    qos = math_var("q", f"{notation},t")
    diagram.box(provider, "", (1200, y, 620, 240), "market_panel", fill, stroke)
    diagram.text(f"{provider}_title", title, (20, 6, 580, 36), provider, 22, True, stroke)
    diagram.text(f"{provider}_prices", f"Wholesale {wholesale_price} &nbsp;&middot;&nbsp; direct {direct_price}", (35, 47, 550, 30), provider, 18)
    diagram.icon(f"{provider}_compute", server_icon, (70, 85, 82, 82), provider)
    diagram.icon(f"{provider}_util", "svg/gpu_capacity_qos/utilization_gauge.svg", (270, 85, 82, 82), provider)
    diagram.icon(f"{provider}_qos", "svg/gpu_capacity_qos/sla_passed.svg", (475, 85, 82, 82), provider)
    diagram.text(f"{provider}_capacity", f"Fixed capacity {capacity_symbol}", (15, 170, 190, 42), provider, 18, True)
    diagram.text(f"{provider}_util_label", f"{utilization} = {load} / {capacity_symbol}", (205, 170, 210, 42), provider, 18)
    diagram.text(f"{provider}_qos_label", f"{qos} = {math_var('Q')}({utilization})", (415, 170, 190, 42), provider, 18)
    diagram.edge(f"{provider}_load_edge", f"{provider}_compute", f"{provider}_util", provider)
    diagram.edge(f"{provider}_qos_edge", f"{provider}_util", f"{provider}_qos", provider)

def add_market_flows(diagram: Diagram) -> None:
    direct_demand_a = math_var("D", "A,t", "D")
    direct_demand_b = math_var("D", "B,t", "D")
    routed_demand_a = f"{math_var('r', 'A,t')}{math_var('D', 't', 'I')}"
    routed_demand_b = f"{math_var('r', 'B,t')}{math_var('D', 't', 'I')}"
    intermediary_signal = f"{math_var('p', 't')}, {math_var('q', 't', 'I')}"
    wholesale_signal_a = f"{math_var('w', 'A,t')}, {math_var('q', 'A,t')}"
    wholesale_signal_b = f"{math_var('w', 'B,t')}, {math_var('q', 'B,t')}"
    direct_signal_a = f"{math_var('p', 'A,t', 'D')}, {math_var('q', 'A,t')}"
    direct_signal_b = f"{math_var('p', 'B,t', 'D')}, {math_var('q', 'B,t')}"
    diagram.edge("rigid_to_choice", "rigid_users", "channel_choice", "market_panel", anchors="exitX=1;exitY=0.5;entryX=0;entryY=0.19;")
    diagram.edge("flexible_to_choice", "flexible_users", "channel_choice", "market_panel", anchors="exitX=1;exitY=0.5;entryX=0;entryY=0.73;")
    diagram.edge("traffic_to_intermediary", "choice_intermediary", "intermediary", "market_panel", anchors="exitX=1;exitY=0.45;entryX=0;entryY=0.2575;")
    diagram.edge("traffic_direct_a", "choice_direct_a", "provider_a", "market_panel", direct_demand_a, anchors="exitX=1;exitY=0.743;entryX=0;entryY=0.571;")
    diagram.edge("traffic_direct_b", "choice_direct_b", "provider_b", "market_panel", direct_demand_b, anchors="exitX=1;exitY=0.8;entryX=0;entryY=0.546;")
    diagram.edge("traffic_exit", "choice_exit", "outside_option", "market_panel", anchors="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    diagram.edge("route_to_a", "intermediary", "provider_a", "market_panel", routed_demand_a, color=CYAN, anchors="exitX=1;exitY=0.075;entryX=0;entryY=0.75;")
    diagram.edge("route_to_b", "intermediary", "provider_b", "market_panel", routed_demand_b, color=CYAN, anchors="exitX=1;exitY=0.7;entryX=0;entryY=0.0208;")
    diagram.edge("signal_retail", "intermediary", "choice_intermediary", "market_panel", intermediary_signal, True, color=CYAN, anchors="exitX=0;exitY=0.373;entryX=1;entryY=0.78;")
    diagram.edge("signal_wholesale_a", "provider_a", "intermediary", "market_panel", wholesale_signal_a, True, color=GREEN, anchors="exitX=0;exitY=0.925;entryX=1;entryY=0.285;")
    diagram.edge("signal_wholesale_b", "provider_b", "intermediary", "market_panel", wholesale_signal_b, True, color=YELLOW, anchors="exitX=0;exitY=0.196;entryX=1;entryY=0.91;")
    diagram.edge("signal_direct_a", "provider_a", "choice_direct_a", "market_panel", direct_signal_a, True, color=GREEN, anchors="exitX=0;exitY=0.396;entryX=1;entryY=0.143;")
    diagram.edge("signal_direct_b", "provider_b", "choice_direct_b", "market_panel", direct_signal_b, True, color=YELLOW, anchors="exitX=0;exitY=0.371;entryX=1;entryY=0.2;")
    diagram.edge("nash_competition", "provider_a", "provider_b", "market_panel", "Simultaneous finite-grid price choices", True, True, CORAL, anchors="exitX=0.85;exitY=1;entryX=0.85;entryY=0;")

def add_solver_panel(diagram: Diagram) -> None:
    diagram.vertex("solver_panel", "", PANEL, (20, 700, 1860, 430))
    diagram.text("solver_title", "(b) Simulation evaluation and finite-grid diagnostics", (390, 3, 1080, 48), "solver_panel", 27, True)
    nodes = (
        ("step_price_grids", "Provider price-shape candidates", "svg/pricing_time/dynamic_price.svg", CYAN_FILL, CYAN, 25),
        ("step_intermediary", "Intermediary response grid", "svg/api_routing/server_sharing.svg", CYAN_FILL, CYAN, 250),
        ("step_user_choice", "Channel-period logit choice", "svg/api_routing/network_users.svg", GREEN_FILL, GREEN, 475),
        ("step_fixed_point", "Joint routing-QoS fixed point", "svg/api_routing/bidirectional_transfer.svg", YELLOW_FILL, YELLOW, 700),
        ("step_payoff_matrix", "Intermediary best response<br>Provider payoff matrix", "svg/simulation_evidence/optimization_result.svg", CORAL_FILL, CORAL, 925),
        ("step_solver", "Fictitious play<br>Double oracle", "svg/simulation_evidence/iterative_solver.svg", GRAY_FILL, GRAY, 1150),
    )
    for cell_id, label, icon_path, fill, stroke, x in nodes:
        diagram.box(cell_id, "", (x, 80, 195, 205), "solver_panel", fill, stroke)
        diagram.icon(f"{cell_id}_icon", icon_path, (58, 27, 80, 80), cell_id)
        diagram.text(f"{cell_id}_label", label, (10, 115, 175, 75), cell_id, 18, True, stroke)
    for index, (source, target) in enumerate(zip((node[0] for node in nodes[:-1]), (node[0] for node in nodes[1:])), 1):
        diagram.edge(f"solver_flow_{index}", source, target, "solver_panel", anchors="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    diagram.edge("solver_feedback", "step_fixed_point", "step_user_choice", "solver_panel", "update QoS-dependent choice", True, color=CYAN, points=((795, 340), (570, 340)), anchors="exitX=0.5;exitY=1;entryX=0.5;entryY=1;", orthogonal=True)
    add_evidence_block(diagram)

def add_evidence_block(diagram: Diagram) -> None:
    diagram.box("evidence_block", "", (1390, 65, 430, 315), "solver_panel", WHITE, INK)
    diagram.text("evidence_title", "Evidence reported", (25, 10, 380, 40), "evidence_block", 22, True)
    evidence = (
        ("evidence_regret", "Finite-grid regret", "exploitability certificate", "svg/simulation_evidence/time_series_results.svg", CYAN),
        ("evidence_qos", "QoS protection", "directional simulation evidence", "svg/gpu_capacity_qos/sla_passed.svg", GREEN),
        ("evidence_profit", "Profit boundary", "effect varies across re-solves", "svg/simulation_evidence/market_share_results.svg", CORAL),
    )
    for index, (cell_id, title, note, icon_path, color) in enumerate(evidence):
        y = 60 + index * 80
        diagram.icon(f"{cell_id}_icon", icon_path, (28, y, 56, 56), "evidence_block")
        diagram.text(cell_id, f"<b>{title}</b><br>{note}", (92, y, 310, 60), "evidence_block", 17, False, color, "left")
    diagram.edge("solver_to_evidence", "step_solver", "evidence_block", "solver_panel", anchors="exitX=1;exitY=0.5;entryX=0;entryY=0.373;")

def build() -> None:
    diagram = Diagram()
    diagram.vertex("market_panel", "", PANEL, (20, 20, 1860, 650))
    diagram.text("market_title", "(a) Market and serving mechanism", (420, 3, 680, 48), "market_panel", 28, True)
    diagram.text("capacity_order", f"{math_var('G', 'A')} &gt; {math_var('G', 'B')}", (1130, 8, 165, 34), "market_panel", 18, True, GRAY)
    add_user_group(diagram, "rigid_users", "Time-rigid users", "Interactive requests<br>Higher migration cost", 75, CYAN_FILL, CYAN, ("svg/market_actors/user_population.svg", "svg/iot_endpoints/network_camera.svg", "svg/pricing_time/runtime.svg"))
    add_user_group(diagram, "flexible_users", "Time-flexible users", "Scheduled and shiftable workloads<br>Lower migration cost", 365, GREEN_FILL, GREEN, ("svg/market_actors/user_population.svg", "svg/iot_endpoints/laptop.svg", "svg/iot_endpoints/smart_home_endpoint.svg"))
    add_choice_box(diagram)
    add_intermediary(diagram)
    add_provider(diagram, "a", 75, "Provider A: higher fixed capacity", GREEN_FILL, GREEN, "svg/gpu_capacity_qos/high_capacity_provider.svg")
    add_provider(diagram, "b", 375, "Provider B: lower fixed capacity", YELLOW_FILL, YELLOW, "svg/api_routing/server_sharing.svg")
    add_market_flows(diagram)
    diagram.text("traffic_legend", "→  Requests / traffic", (1330, 12, 210, 32), "market_panel", 16, False, INK, "left")
    diagram.text("signal_legend", "--→  Price / QoS signal", (1545, 12, 260, 32), "market_panel", 16, False, GRAY, "left")
    add_solver_panel(diagram)
    diagram.save()
    print(OUTPUT)

if __name__ == "__main__":
    build()
