#!/usr/bin/env python3
"""Build Figure 1 from attributed web icons and a shared editable scene."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from figure_sources.build_peak_shaving_framework_drawio import Diagram

PIN = "52d750c9ce051e51cb181b7a78932120c48541d0"
REMOTE = f"https://raw.githubusercontent.com/webalys-hq/streamline-vectors/{PIN}/"
ASSETS = PROJECT / "figure_sources/iot_framework_assets"
OUT = PROJECT / "figures/iot_framework_20260906"
SOURCE = PROJECT / "figure_sources/iot_framework_20260906.drawio"
ICONS = {
    "vision": "ultimate/colors/computers-devices-electronics/webcam-2.svg",
    "factory": "ultimate/colors/business-products/style-three-pin-factory.svg",
    "wearable": "ultimate/colors/computers-devices-electronics/smart-watch-square-wifi.svg",
    "home": "ultimate/colors/computers-devices-electronics/house-signal.svg",
    "gateway": "ultimate/colors/internet-networks-servers/router-signal.svg",
    "intermediary": "ultimate/colors/internet-networks-servers/server-share.svg",
    "provider_a": "ultimate/colors/internet-networks-servers/server-star-1.svg",
    "provider_b": "ultimate/colors/computers-devices-electronics/computer-chip-core.svg",
    "data": "ultimate/colors/business-products/analytics-board-graph-line.svg",
    "response": "ultimate/colors/interface-essential/synchronize-arrows-three.svg",
    "prices": "ultimate/colors/business-products/cash-payment-coin-dollar.svg",
    "audit": "ultimate/colors/programing-apps-websites/programming-apps-websites/shield-check-1.svg",
}
INK, MUTED = "#24323D", "#596975"
TEAL, TEAL_FILL = "#237D81", "#EFF8F7"
BLUE, BLUE_FILL = "#466A9B", "#F0F4FA"
RUST, RUST_FILL = "#A76745", "#FCF4EE"
LINE = "#D5DFE4"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def svg_node(parent, tag, **attributes):
    return ET.SubElement(parent, f"{{{NS}}}{tag}", {k: str(v) for k, v in attributes.items()})


def fetch_icons():
    ASSETS.mkdir(parents=True, exist_ok=True)
    manifest = []
    for name, upstream in ICONS.items():
        url = REMOTE + upstream
        with urlopen(url, timeout=45) as response:
            payload = response.read()
        assert ET.fromstring(payload).tag.endswith("svg"), url
        (ASSETS / f"{name}.svg").write_bytes(payload)
        manifest.append({"file": f"{name}.svg", "url": url,
                         "sha256": hashlib.sha256(payload).hexdigest()})
        print(f"Fetched {name}", flush=True)
    (ASSETS / "sources.json").write_text(json.dumps({
        "author": "Streamline", "homepage": "https://streamlinehq.com",
        "license": "CC BY 4.0", "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "commit": PIN, "retrieved": "2026-09-06", "modifications": "None; scaled in the diagram.",
        "icons": manifest,
    }, indent=2) + "\n", encoding="utf-8")


class Scene:
    """Keep vector exports and Draw.io geometry on the same coordinates."""
    def __init__(self):
        self.diagram = Diagram()
        self.boxes = {}
        self.diagram.mxfile.set("modified", "2026-09-06T00:00:00Z")
        model = self.diagram.mxfile.find(".//mxGraphModel")
        model.set("pageWidth", "1600")
        model.set("pageHeight", "1190")
        self.svg = ET.Element(f"{{{NS}}}svg", {
            "width": "180mm", "height": "133.875mm", "viewBox": "0 0 1600 1190",
        })
        svg_node(self.svg, "rect", x=0, y=0, width=1600, height=1190, fill="white")
        defs = svg_node(self.svg, "defs")
        for name, color in (("traffic", INK), ("signal", TEAL)):
            marker = svg_node(defs, "marker", id=name, viewBox="0 0 10 10", refX=9,
                              refY=5, markerWidth=7, markerHeight=7, orient="auto-start-reverse")
            svg_node(marker, "path", d="M 0 0 L 10 5 L 0 10 z", fill=color)

    def box(self, key, xywh, fill="white", stroke=LINE):
        x, y, w, h = xywh
        self.boxes[key] = xywh
        self.diagram.box(key, "", xywh, "1", fill, stroke)
        svg_node(self.svg, "rect", x=x, y=y, width=w, height=h, rx=8,
                 fill=fill, stroke=stroke, **{"stroke-width": 1.8})

    def text(self, key, lines, xywh, size=25, bold=False, color=INK, align="center"):
        x, y, w, h = xywh
        lines = lines.split("\n")
        self.diagram.text(key, "<br>".join(lines), xywh, size=size,
                          bold=bold, color=color, align=align)
        xpos = x + (w / 2 if align == "center" else 0)
        step = size * 1.22
        baseline = y + (h - step * (len(lines) - 1)) / 2 + size * .33
        text = svg_node(self.svg, "text", x=xpos, fill=color, **{
            "font-family": "Times New Roman, Liberation Serif, serif", "font-size": size,
            "font-weight": "bold" if bold else "normal",
            "text-anchor": "middle" if align == "center" else "start",
        })
        for index, line in enumerate(lines):
            svg_node(text, "tspan", x=xpos, y=baseline + index * step).text = line

    def icon(self, key, name, xywh):
        x, y, w, h = xywh
        payload = (ASSETS / f"{name}.svg").read_text(encoding="utf-8")
        image_style = ("shape=image;html=1;imageAspect=1;aspect=fixed;strokeColor=none;"
                       f"image=data:image/svg+xml,{quote(payload, safe='')};")
        self.diagram.vertex(key, "", image_style, xywh)
        icon = ET.fromstring(payload)
        icon.attrib.update(x=str(x), y=str(y), width=str(w), height=str(h))
        self.svg.append(icon)

    def line(self, key, points, *, dashed=False, arrow=True, both=False):
        color = TEAL if dashed else INK
        attrs = {"points": " ".join(f"{x},{y}" for x, y in points), "fill": "none",
                 "stroke": color, "stroke-width": 2.2, "stroke-linejoin": "round"}
        if dashed:
            attrs["stroke-dasharray"] = "8 6"
        if arrow:
            attrs["marker-end"] = f"url(#{'signal' if dashed else 'traffic'})"
        if both:
            attrs["marker-start"] = f"url(#{'signal' if dashed else 'traffic'})"
        svg_node(self.svg, "polyline", **attrs)
        style = (f"edgeStyle=none;rounded=0;html=1;strokeWidth=2.2;strokeColor={color};"
                 f"endArrow={'classicThin' if arrow else 'none'};"
                 f"startArrow={'classicThin' if both else 'none'};"
                 + ("dashed=1;dashPattern=8 6;" if dashed else ""))
        edge = ET.SubElement(self.diagram.root, "mxCell", id=key, edge="1", parent="1", style=style)
        geometry = ET.SubElement(edge, "mxGeometry", relative="1", **{"as": "geometry"})
        for role, (x, y) in (("sourcePoint", points[0]), ("targetPoint", points[-1])):
            ET.SubElement(geometry, "mxPoint", x=str(x), y=str(y), **{"as": role})
        if len(points) > 2:
            array = ET.SubElement(geometry, "Array", **{"as": "points"})
            for x, y in points[1:-1]:
                ET.SubElement(array, "mxPoint", x=str(x), y=str(y))

    def save(self, *, stem="figure1_iot"):
        import cairosvg
        OUT.mkdir(parents=True, exist_ok=True)
        # Parent labels and icons to their containers in the editable source.
        for cell in self.diagram.root.findall('mxCell[@vertex="1"]'):
            geometry = cell.find("mxGeometry")
            x, y, w, h = (float(geometry.get(k)) for k in ("x", "y", "width", "height"))
            containers = [(bw * bh, key, bx, by) for key, (bx, by, bw, bh) in self.boxes.items()
                          if key != cell.get("id") and bx <= x and by <= y
                          and x + w <= bx + bw and y + h <= by + bh]
            if containers:
                _, parent, bx, by = min(containers)
                cell.set("parent", parent)
                geometry.set("x", str(x - bx))
                geometry.set("y", str(y - by))
        ET.indent(self.diagram.mxfile)
        ET.ElementTree(self.diagram.mxfile).write(SOURCE, encoding="utf-8", xml_declaration=True)
        svg = ET.tostring(self.svg, encoding="utf-8", xml_declaration=True)
        (OUT / f"{stem}.svg").write_bytes(svg)
        cairosvg.svg2pdf(bytestring=svg, write_to=str(OUT / f"{stem}.pdf"))
        cairosvg.svg2png(bytestring=svg, output_width=4252, write_to=str(OUT / f"{stem}.png"))
        cairosvg.svg2png(bytestring=svg, output_width=2000, write_to=str(OUT / f"{stem}_preview.png"))


def application_layer(s):
    s.text("a_title", "(a) IoT applications and network access", (30, 15, 1000, 42), 30, True, align="left")
    s.text("scope", "Illustrative deployment context", (1120, 20, 450, 32), 24, color=MUTED)
    for key, name, title, note, x in (
        ("vision_source", "vision", "Connected vision", "Camera-based sensing", 30),
        ("industry_source", "factory", "Industrial IoT", "Equipment monitoring", 300),
        ("wearable_source", "wearable", "Wearable sensing", "Connected measurements", 570),
        ("home_source", "home", "Smart buildings", "Home and building sensors", 840),
    ):
        s.icon(key, name, (x + 74, 80, 108, 108))
        s.text(f"{key}_title", title, (x, 195, 256, 32), 27, True)
        s.text(f"{key}_note", note, (x - 3, 233, 262, 27), 23, color=MUTED)
        s.line(f"{key}_uplink", ((x + 128, 265), (x + 128, 290)), arrow=False)
    s.line("access_bus", ((158, 290), (1140, 290), (1140, 173), (1200, 173)))
    s.box("gateway", (1200, 90, 370, 168), TEAL_FILL, TEAL)
    s.icon("gateway_icon", "gateway", (1220, 128, 85, 85))
    s.text("gateway_title", "IoT access gateways", (1308, 106, 250, 64), 27, True, TEAL)
    s.text("gateway_note", "Application / API clients", (1308, 179, 250, 51), 24)
    s.text("aggregate_requests", "Aggregated inference requests", (1200, 267, 370, 34), 24, color=TEAL)


def market_layer(s):
    s.text("b_title", "(b) Conserved demand and the inference-service market", (30, 330, 1100, 42), 30, True, align="left")
    s.box("request_types", (30, 470, 235, 245), "#F7F9FA", LINE)
    s.text("rigid", "Time-rigid requests", (40, 480, 215, 44), 24, True)
    s.text("rigid_note", "Native period retained", (35, 525, 225, 42), 24, color=MUTED)
    s.text("flexible", "Flexible requests", (35, 596, 225, 42), 26, True)
    s.text("flexible_note", "Shift within a window", (35, 640, 225, 42), 24, color=MUTED)
    s.line("types_to_time", ((265, 594), (315, 594)))
    s.box("temporal_allocation", (315, 475, 265, 240), TEAL_FILL, TEAL)
    s.text("time_title", "OD time allocation", (325, 485, 245, 42), 27, True, TEAL)
    s.text("time_subtitle", "Select a destination period", (321, 532, 253, 36), 23)
    for i, label in enumerate(("t - 1", "t", "t + 1")):
        s.box(f"slot_{i}", (336 + i * 76, 582, 69, 43), "white", TEAL)
        s.text(f"slot_{i}_label", label, (336 + i * 76, 582, 69, 43), 25)
    s.line("time_shift", ((372, 646), (524, 646)), both=True)
    s.text("conservation", "Demand conserved", (324, 665, 247, 36), 27, True, TEAL)
    s.line("time_to_channels", ((580, 594), (607, 594)), arrow=False)
    s.line("channel_bus", ((607, 495), (607, 765)), arrow=False)
    for name, y in (("a", 495), ("api", 630), ("b", 765)):
        s.line(f"channel_branch_{name}", ((607, y), (635, y)))
    s.text("channel_title", "Channel choice", (635, 410, 230, 38), 27, True)
    for key, label, y, color, fill in (
        ("direct_a", "Direct access to A", 460, BLUE, BLUE_FILL),
        ("api_access", "Via intermediary", 595, TEAL, TEAL_FILL),
        ("direct_b", "Direct access to B", 730, RUST, RUST_FILL),
    ):
        s.box(key, (635, y, 230, 70), fill, color)
        s.text(f"{key}_label", label, (640, y + 8, 220, 54), 26, True, color)
    s.box("intermediary", (930, 590, 245, 125), TEAL_FILL, TEAL)
    s.text("broker_title", "API intermediary", (935, 599, 235, 37), 27, True, TEAL)
    s.icon("broker_icon", "intermediary", (945, 650, 45, 45))
    s.text("broker_note", "Retail price\nRouting by QoS", (996, 644, 172, 60), 24)
    for key, title, y, color, fill in (
        ("provider_a", "Inference provider A", 430, BLUE, BLUE_FILL),
        ("provider_b", "Inference provider B", 685, RUST, RUST_FILL),
    ):
        s.box(key, (1240, y, 330, 155), fill, color)
        s.text(f"{key}_title", title, (1250, y + 8, 310, 36), 28, True, color)
        s.icon(f"{key}_icon", key, (1267, y + 61, 70, 70))
        s.text(f"{key}_body", "Fixed capacity\nLoad-dependent QoS", (1345, y + 58, 218, 76), 24)
    s.line("direct_to_a", ((865, 495), (1240, 495)))
    s.line("access_to_broker", ((865, 630), (930, 630)))
    s.line("direct_to_b", ((865, 765), (1240, 765)))
    s.line("routed_a", ((1175, 612), (1207, 612), (1207, 548), (1240, 548)))
    s.line("routed_b", ((1175, 685), (1207, 685), (1207, 735), (1240, 735)))
    s.text("route_label", "Traffic split", (930, 722, 245, 31), 23, color=TEAL)
    s.line("competition", ((1485, 595), (1485, 675)), dashed=True, both=True)
    s.text("competition_label", "Price competition\nUnequal capacities", (1235, 602, 240, 62), 23, color=MUTED)
    s.line("signal_a", ((1240, 451), (1190, 451), (1190, 405), (748, 405), (748, 408)), dashed=True)
    s.text("signal_label", "Price and QoS information", (851, 374, 325, 26), 23, color=TEAL)
    s.line("signal_b", ((1405, 840), (1405, 865), (447, 865), (447, 725)), dashed=True)
    s.text("feedback_label", "Price and QoS feedback to allocation and routing", (635, 869, 755, 34), 24, color=TEAL)


def computation_layer(s):
    s.text("c_title", "(c) Numerical solution and verification", (30, 925, 980, 42), 30, True, align="left")
    steps = (
        ("inputs", "Input anchors", "BurstGPT load shape\nMeasured QoS curve", "data", 30),
        ("payoffs", "Follower response", "Bounded follower optimization\nJoint market fixed point", "response", 425),
        ("equilibrium", "Provider pricing game", "Finite price-rule candidates\nMixed-strategy equilibrium", "prices", 820),
        ("checks", "Deviation checks", "Full candidate scan\nOff-grid and independent audits", "audit", 1215),
    )
    for key, title, note, icon, x in steps:
        s.box(key, (x, 988, 355, 133), "#F8FAFB", LINE)
        s.icon(f"{key}_icon", icon, (x + 13, 1004, 43, 43))
        s.text(f"{key}_title", title, (x + 65, 998, 276, 46), 26, True)
        s.text(f"{key}_note", note, (x + 9, 1050, 337, 62), 23)
    for index in range(3):
        x = steps[index][4] + 355
        s.line(f"solve_{index}", ((x, 1055), (steps[index + 1][4], 1055)))
    s.text("outputs", "Reported outcomes: peak load, provider QoS and profit; variation across mixed-strategy realizations.",
           (55, 1143, 1490, 36), 25, color=MUTED)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fetch-icons", action="store_true")
    args = parser.parse_args()
    if args.fetch_icons:
        fetch_icons()
    scene = Scene()
    application_layer(scene)
    market_layer(scene)
    computation_layer(scene)
    scene.save()
    print(OUT)


if __name__ == "__main__":
    main()
