#!/usr/bin/env python3
"""Build the editable Draw.io framework for the inference-pricing paper."""
from __future__ import annotations
import base64
import re
import xml.etree.ElementTree as ET
from pathlib import Path
import cairosvg
PROJECT = Path(__file__).resolve().parents[1]
ICON_DIR = PROJECT / "figure_sources" / "fontawesome-free-7.3.0"
OUTPUT = PROJECT / "figure_sources" / "inference_pricing_framework_2026-07-10.drawio"
NAVY = "#174A7E"
DEEP_NAVY = "#123B63"
TEAL = "#2A7F78"
CORAL = "#D95D4F"
GOLD = "#B98513"
SKY = "#4D8FC3"
INK = "#24313F"
GRAY = "#6B7280"
LIGHT_GRAY = "#F6F8FA"
WHITE = "#FFFFFF"
def svg_uri(name: str, color: str) -> str:
    svg = (ICON_DIR / f"{name}.svg").read_text(encoding="utf-8")
    view_box = re.search(r'viewBox="0 0 ([0-9.]+) ([0-9.]+)"', svg)
    if view_box:
        svg = svg.replace("<svg ", f'<svg width="{view_box[1]}" height="{view_box[2]}" ', 1)
    svg = svg.replace("currentColor", color)
    png = cairosvg.svg2png(bytestring=svg.encode("utf-8"), output_width=512)
    encoded = base64.b64encode(png).decode("ascii")
    # Draw.io treats a literal semicolon as a style separator during export.
    return f"data:image/png%3Bbase64,{encoded}"
mxfile = ET.Element(
    "mxfile",
    host="Electron",
    modified="2026-07-10T13:00:00.000Z",
    agent="Codex drawio-skill",
    version="30.3.6",
    type="device",
)
diagram = ET.SubElement(mxfile, "diagram", id="inference-pricing-framework", name="Page-1")
model = ET.SubElement(
    diagram,
    "mxGraphModel",
    dx="1900",
    dy="1060",
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
    pageHeight="1060",
    math="0",
    shadow="0",
)
root = ET.SubElement(model, "root")
ET.SubElement(root, "mxCell", id="0")
ET.SubElement(root, "mxCell", id="1", parent="0")
def vertex(
    cell_id: str,
    value: str,
    style: str,
    x: float,
    y: float,
    width: float,
    height: float,
    parent: str = "1",
) -> ET.Element:
    cell = ET.SubElement(
        root,
        "mxCell",
        id=cell_id,
        value=value,
        style=style,
        vertex="1",
        parent=parent,
    )
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
def icon(
    cell_id: str,
    name: str,
    color: str,
    x: float,
    y: float,
    width: float,
    height: float,
    parent: str,
    value: str = "",
) -> ET.Element:
    style = (
        "shape=image;html=1;imageAspect=0;aspect=fixed;strokeColor=none;fillColor=none;"
        "verticalLabelPosition=bottom;verticalAlign=top;align=center;"
        "fontFamily=Times New Roman;fontSize=13;fontColor=#24313F;"
        f"image={svg_uri(name, color)}"
    )
    return vertex(cell_id, value, style, x, y, width, height, parent)
def edge(
    cell_id: str,
    source: str,
    target: str,
    color: str,
    value: str = "",
    parent: str = "1",
    dashed: bool = False,
    both: bool = False,
    extra: str = "",
    points: tuple[tuple[float, float], ...] = (),
) -> ET.Element:
    dash = "dashed=1;dashPattern=7 5;" if dashed else ""
    start = "startArrow=classicThin;startFill=1;" if both else "startArrow=none;"
    style = (
        "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;"
        "html=1;endArrow=classicThin;endFill=1;strokeWidth=2;"
        f"strokeColor={color};{dash}{start}"
        "fontFamily=Times New Roman;fontSize=12;fontColor=#24313F;"
        "labelBackgroundColor=#FFFFFF;"
        f"{extra}"
    )
    cell = ET.SubElement(
        root,
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
        for px, py in points:
            ET.SubElement(array, "mxPoint", x=str(px), y=str(py))
    return cell
FONT = "fontFamily=Times New Roman;fontColor=#24313F;"
PANEL = (
    "rounded=1;whiteSpace=wrap;html=1;container=1;pointerEvents=0;"
    "fillColor=#FFFFFF;strokeWidth=2;dashed=1;dashPattern=9 7;arcSize=8;"
)
TITLE = (
    "text;html=1;strokeColor=none;fillColor=none;whiteSpace=wrap;"
    "align=center;verticalAlign=middle;fontFamily=Times New Roman;"
    "fontSize=26;fontStyle=1;"
)
BOX = (
    "rounded=1;whiteSpace=wrap;html=1;container=1;pointerEvents=0;"
    f"fillColor={LIGHT_GRAY};strokeColor={GRAY};strokeWidth=1.4;arcSize=8;{FONT}"
    "fontSize=18;fontStyle=1;verticalAlign=top;spacingTop=10;"
)
NODE = (
    "rounded=1;whiteSpace=wrap;html=1;container=1;pointerEvents=1;"
    f"fillColor={WHITE};strokeWidth=1.7;arcSize=8;{FONT}"
)
TEXT = (
    "text;html=1;strokeColor=none;fillColor=none;whiteSpace=wrap;"
    f"align=center;verticalAlign=middle;{FONT}"
)
# Main panels
vertex("market", "", PANEL + f"strokeColor={CORAL};", 20, 20, 1120, 650)
vertex("serving", "", PANEL + f"strokeColor={NAVY};", 1160, 20, 720, 650)
vertex("loop", "", PANEL + f"strokeColor={NAVY};", 20, 690, 1860, 350)
vertex("market_title", "(a) Market and Decision Layer", TITLE + f"fontColor={CORAL};", 240, 5, 640, 45, "market")
vertex("serving_title", "(b) GPU Serving Layer", TITLE + f"fontColor={NAVY};", 120, 5, 480, 45, "serving")
vertex("loop_title", "(c) Simulation and Diagnostic Loop", TITLE + f"fontColor={NAVY};", 560, 5, 740, 45, "loop")
# User groups
vertex("rigid", "Time-rigid users", BOX, 25, 75, 250, 185, "market")
icon("rigid_users", "users", NAVY, 45, 70, 90, 75, "rigid")
icon("rigid_clock", "clock", NAVY, 155, 80, 62, 62, "rigid")
vertex("rigid_note", "Interactive and latency-sensitive", TEXT + "fontSize=13;", 22, 145, 206, 28, "rigid")
vertex("flex", "Time-flexible users", BOX, 25, 335, 250, 200, "market")
icon("flex_users", "users", TEAL, 45, 78, 90, 75, "flex")
icon("flex_calendar", "calendar-days", TEAL, 155, 82, 62, 62, "flex")
vertex("flex_note", "Scheduled and shiftable workloads", TEXT + "fontSize=13;", 18, 155, 214, 30, "flex")
# Channel choice and alternatives
vertex("channel", "Channel choice", BOX + f"fillColor=#FFFFFF;strokeColor={INK};", 315, 145, 220, 390, "market")
choice_base = (
    "rounded=1;whiteSpace=wrap;html=1;container=1;pointerEvents=1;"
    f"strokeWidth=1.5;arcSize=12;{FONT}fontSize=16;fontStyle=1;"
    "align=left;verticalAlign=middle;spacingLeft=48;"
)
choices = [
    ("choice_api", "API intermediary", "cloud", NAVY, "#EAF2FB", 65),
    ("choice_a", "Direct A", "server", TEAL, "#EAF6F4", 137),
    ("choice_b", "Direct B", "server", GOLD, "#FBF4E3", 209),
    ("choice_exit", "Exit", "door-open", CORAL, "#FCEDEA", 281),
]
for cid, label, glyph, color, fill, cy in choices:
    vertex(cid, label, choice_base + f"fillColor={fill};strokeColor={color};", 20, cy, 180, 54, "channel")
    icon(f"{cid}_icon", glyph, color, 12, 10, 30, 30, cid)
# Intermediary and provider pricing nodes
vertex("intermediary", "API intermediary", NODE + f"strokeColor={NAVY};fontSize=19;fontStyle=1;verticalAlign=top;spacingTop=10;", 585, 55, 225, 175, "market")
icon("intermediary_cloud", "cloud", NAVY, 65, 50, 95, 72, "intermediary")
vertex("intermediary_note", "Retail price and routing", TEXT + "fontSize=13;", 30, 135, 165, 25, "intermediary")
vertex("provider_a", "Provider A", NODE + f"strokeColor={TEAL};fontColor={TEAL};fontSize=19;fontStyle=1;verticalAlign=top;spacingTop=10;", 865, 135, 190, 150, "market")
icon("provider_a_icon", "server", TEAL, 58, 48, 74, 70, "provider_a")
vertex("provider_a_note", "Pricing operator", TEXT + f"fontColor={TEAL};fontSize=13;", 30, 120, 130, 22, "provider_a")
vertex("provider_b", "Provider B", NODE + f"strokeColor={GOLD};fontColor={GOLD};fontSize=19;fontStyle=1;verticalAlign=top;spacingTop=10;", 865, 390, 190, 150, "market")
icon("provider_b_icon", "server", GOLD, 58, 48, 74, 70, "provider_b")
vertex("provider_b_note", "Pricing operator", TEXT + f"fontColor={GOLD};fontSize=13;", 30, 120, 130, 22, "provider_b")
icon("outside", "door-open", CORAL, 700, 555, 55, 55, "market", "Outside option")
# Market traffic and information flows
edge("e_rigid_channel", "rigid", "channel", NAVY, parent="market", extra="exitX=1;exitY=0.55;entryX=0;entryY=0.28;")
edge("e_flex_channel", "flex", "channel", TEAL, parent="market", extra="exitX=1;exitY=0.45;entryX=0;entryY=0.72;")
edge("e_choice_api", "choice_api", "intermediary", NAVY, parent="market", extra="exitX=1;exitY=0.35;entryX=0;entryY=0.7;")
edge("e_direct_a", "choice_a", "provider_a", TEAL, parent="market", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.75;")
edge("e_direct_b", "choice_b", "provider_b", GOLD, parent="market", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.35;")
edge("e_exit", "choice_exit", "outside", CORAL, parent="market", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
edge("e_route_a", "intermediary", "provider_a", NAVY, parent="market", extra="exitX=1;exitY=0.55;entryX=0;entryY=0.2;")
edge("e_route_b", "intermediary", "provider_b", NAVY, parent="market", extra="exitX=0.65;exitY=1;entryX=0;entryY=0.15;", points=((830, 330),))
edge("e_retail_info", "intermediary", "choice_api", NAVY, parent="market", dashed=True, extra="exitX=0;exitY=0.25;entryX=1;entryY=0.15;")
edge("e_wholesale_a", "provider_a", "intermediary", TEAL, parent="market", dashed=True, extra="exitX=0;exitY=0.1;entryX=1;entryY=0.2;")
edge("e_wholesale_b", "provider_b", "intermediary", GOLD, parent="market", dashed=True, extra="exitX=0;exitY=0.9;entryX=1;entryY=0.85;", points=((825, 555), (825, 245)))
edge("e_direct_info_a", "provider_a", "choice_a", TEAL, parent="market", dashed=True, extra="exitX=0;exitY=0.9;entryX=1;entryY=0.9;", points=((760, 310),))
edge("e_direct_info_b", "provider_b", "choice_b", GOLD, parent="market", dashed=True, extra="exitX=0;exitY=0.2;entryX=1;entryY=0.15;", points=((770, 385),))
edge("e_nash", "provider_a", "provider_b", CORAL, parent="market", dashed=True, both=True, extra="exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
market_note = TEXT + "fontSize=11;labelBackgroundColor=#FFFFFF;"
for nid, label, x, y, w in (("m1", "Requests", 505, 183, 90), ("m2", "Retail price / QoS", 490, 105, 130), ("m3", "Routed traffic", 785, 127, 115), ("m4", "Wholesale price / QoS", 765, 78, 150), ("m5", "Direct traffic", 605, 270, 110), ("m6", "Direct price / QoS", 600, 326, 125), ("m7", "Routed traffic", 750, 315, 115), ("m8", "Wholesale price / QoS", 745, 492, 150), ("m9", "Direct traffic", 605, 414, 110), ("m10", "Direct price / QoS", 600, 365, 125), ("m11", "Nash pricing competition", 965, 315, 145)):
    vertex(nid, label, market_note, x, y, w, 28, "market")
# GPU serving clusters
cluster_style_a = NODE + f"strokeColor={TEAL};fillColor=#F7FCFB;"
cluster_style_b = NODE + f"strokeColor={GOLD};fillColor=#FFFCF5;"
vertex("cluster_a", "Provider A: higher fixed capacity", cluster_style_a + f"fontColor={TEAL};fontSize=19;fontStyle=1;verticalAlign=top;spacingTop=10;", 35, 75, 650, 245, "serving")
vertex("cluster_b", "Provider B: lower fixed capacity", cluster_style_b + f"fontColor={GOLD};fontSize=19;fontStyle=1;verticalAlign=top;spacingTop=10;", 35, 360, 650, 245, "serving")
for index, px in enumerate((45, 105, 165), start=1):
    icon(f"rack_a_{index}", "server", TEAL, px, 78, 48, 58, "cluster_a")
vertex("req_a_label", "Requests", TEXT + "fontSize=14;", 55, 150, 145, 25, "cluster_a")
icon("util_a", "gauge-high", TEAL, 295, 72, 88, 88, "cluster_a")
vertex("util_a_label", "GPU utilization", TEXT + "fontSize=14;", 270, 160, 140, 25, "cluster_a")
icon("qos_a", "shield-halved", CORAL, 500, 74, 78, 88, "cluster_a")
vertex("qos_a_label", "QoS", TEXT + "fontSize=14;", 485, 170, 108, 25, "cluster_a")
edge("e_a_req_util", "rack_a_3", "util_a", TEAL, parent="cluster_a", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
edge("e_a_util_qos", "util_a", "qos_a", TEAL, parent="cluster_a", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
edge("e_a_feedback", "qos_a", "rack_a_1", TEAL, "Utilization and QoS feedback", "cluster_a", dashed=True, extra="exitX=0.5;exitY=1;entryX=0.5;entryY=1;", points=((545, 205), (70, 205)))
icon("rack_b", "server", GOLD, 105, 82, 74, 74, "cluster_b")
vertex("req_b_label", "Requests", TEXT + "fontSize=14;", 78, 160, 130, 25, "cluster_b")
icon("util_b", "gauge-high", GOLD, 295, 72, 88, 88, "cluster_b")
vertex("util_b_label", "GPU utilization", TEXT + "fontSize=14;", 270, 160, 140, 25, "cluster_b")
icon("qos_b", "shield-halved", CORAL, 500, 74, 78, 88, "cluster_b")
vertex("qos_b_label", "QoS", TEXT + "fontSize=14;", 485, 170, 108, 25, "cluster_b")
edge("e_b_req_util", "rack_b", "util_b", GOLD, parent="cluster_b", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
edge("e_b_util_qos", "util_b", "qos_b", GOLD, parent="cluster_b", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
edge("e_b_feedback", "qos_b", "rack_b", GOLD, "Utilization and QoS feedback", "cluster_b", dashed=True, extra="exitX=0.5;exitY=1;entryX=0.5;entryY=1;", points=((545, 205), (140, 205)))
# Links between market operators and physical GPU clusters
edge("e_exec_a", "provider_a", "cluster_a", TEAL, extra="exitX=1;exitY=0.35;entryX=0;entryY=0.35;")
edge("e_telemetry_a", "cluster_a", "provider_a", TEAL, dashed=True, extra="exitX=0;exitY=0.75;entryX=1;entryY=0.75;")
edge("e_exec_b", "provider_b", "cluster_b", GOLD, extra="exitX=1;exitY=0.35;entryX=0;entryY=0.35;")
edge("e_telemetry_b", "cluster_b", "provider_b", GOLD, dashed=True, extra="exitX=0;exitY=0.75;entryX=1;entryY=0.75;")
vertex("cross_a_traffic", "Traffic", market_note, 1110, 171, 100, 24)
vertex("cross_a_info", "QoS / utilization", market_note, 1090, 253, 140, 24)
vertex("cross_b_traffic", "Traffic", market_note, 1110, 445, 100, 24)
vertex("cross_b_info", "QoS / utilization", market_note, 1090, 523, 140, 24)
# Simulation and diagnostic loop
loop_nodes = [
    ("loop_price", "Price profiles", "tags", NAVY, 30),
    ("loop_users", "User choice", "users", TEAL, 330),
    ("loop_route", "Routing", "route", GOLD, 630),
    ("loop_util", "GPU utilization", "microchip", SKY, 930),
    ("loop_qos", "QoS fixed point", "bullseye", CORAL, 1230),
    ("loop_payoff", "Payoffs and regret", "chart-column", NAVY, 1530),
]
for node_id, label, glyph, color, px in loop_nodes:
    vertex(node_id, label, NODE + f"strokeColor={color};fontSize=17;fontStyle=1;verticalAlign=bottom;spacingBottom=12;", px, 70, 260, 150, "loop")
    icon(f"{node_id}_icon", glyph, color, 95, 22, 70, 70, node_id)
for idx, (source, target) in enumerate(
    zip((item[0] for item in loop_nodes[:-1]), (item[0] for item in loop_nodes[1:])),
    start=1,
):
    edge(f"e_loop_{idx}", source, target, NAVY, parent="loop", extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
edge("e_loop_feedback", "loop_qos", "loop_route", NAVY, "iterate to convergence", "loop", dashed=True, extra="exitX=0.5;exitY=1;entryX=0.5;entryY=1;", points=((1360, 260), (760, 260)))
vertex("legend_traffic_line", "", "shape=line;html=1;strokeColor=#174A7E;strokeWidth=2;endArrow=classicThin;endFill=1;", 560, 300, 100, 1, "loop")
vertex("legend_traffic", "Traffic", TEXT + "fontSize=14;align=left;", 675, 285, 120, 30, "loop")
vertex("legend_info_line", "", "shape=line;html=1;strokeColor=#174A7E;strokeWidth=2;dashed=1;dashPattern=7 5;endArrow=classicThin;endFill=1;", 1030, 300, 100, 1, "loop")
vertex("legend_info", "Price / QoS information", TEXT + "fontSize=14;align=left;", 1145, 285, 240, 30, "loop")
tree = ET.ElementTree(mxfile)
ET.indent(tree, space="  ")
tree.write(OUTPUT, encoding="utf-8", xml_declaration=True)
print(OUTPUT)
