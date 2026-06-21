"""Generate the editable Draw.io source and PNG preview for Figure 1."""
from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path
import math
import textwrap
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "figures" / "peak_shaving_diagnostics"
OUT_DRAWIO = FIG / "market_schematic_drawio_exact_2026-06-21.drawio"
OUT_PNG = FIG / "market_schematic_drawio_exact_2026-06-21.png"

W, H = 1800, 1020
FONT = "/mnt/c/Windows/Fonts/times.ttf"
BOLD = "/mnt/c/Windows/Fonts/timesbd.ttf"


@dataclass(frozen=True)
class Box:
    x: int
    y: int
    w: int
    h: int
    label: str
    fill: str
    stroke: str


def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = BOLD if bold and Path(BOLD).exists() else FONT
    if Path(path).exists():
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def center_text(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int],
                label: str, size: int, color: str = "#1F2937",
                bold: bool = False, wrap: int | None = None) -> None:
    lines: list[str] = []
    for line in label.split("\n"):
        lines.extend(textwrap.wrap(line, width=wrap) if wrap else [line])
    draw.multiline_text(
        ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2),
        "\n".join(lines),
        font=get_font(size, bold),
        fill=color,
        anchor="mm",
        align="center",
        spacing=5,
    )


def label_text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], label: str,
               size: int, color: str = "#1F2937", bold: bool = False,
               anchor: str = "mm", wrap: int | None = None) -> None:
    lines: list[str] = []
    for line in label.split("\n"):
        lines.extend(textwrap.wrap(line, width=wrap) if wrap else [line])
    draw.multiline_text(
        xy, "\n".join(lines), font=get_font(size, bold), fill=color,
        anchor=anchor, align="center", spacing=4,
    )


def rounded_box(draw: ImageDraw.ImageDraw, box: Box, radius: int = 24,
                width: int = 3, shadow: bool = False) -> None:
    xy = (box.x, box.y, box.x + box.w, box.y + box.h)
    if shadow:
        shadow_xy = (box.x + 7, box.y + 8, box.x + box.w + 7, box.y + box.h + 8)
        draw.rounded_rectangle(shadow_xy, radius=radius, fill="#D8DEE9")
    draw.rounded_rectangle(xy, radius=radius, fill=box.fill, outline=box.stroke, width=width)


def dashed_line(draw: ImageDraw.ImageDraw, a: tuple[int, int], b: tuple[int, int],
                color: str, width: int = 4, dash: int = 16, gap: int = 10) -> None:
    ax, ay = a
    bx, by = b
    dist = math.hypot(bx - ax, by - ay)
    if dist == 0:
        return
    ux, uy = (bx - ax) / dist, (by - ay) / dist
    pos = 0.0
    while pos < dist:
        end = min(pos + dash, dist)
        draw.line((ax + ux * pos, ay + uy * pos, ax + ux * end, ay + uy * end),
                  fill=color, width=width)
        pos += dash + gap


def arrow_head(draw: ImageDraw.ImageDraw, a: tuple[int, int], b: tuple[int, int],
               color: str, size: int = 18) -> None:
    angle = math.atan2(b[1] - a[1], b[0] - a[0])
    pts = [
        b,
        (int(b[0] - size * math.cos(angle - 0.45)), int(b[1] - size * math.sin(angle - 0.45))),
        (int(b[0] - size * math.cos(angle + 0.45)), int(b[1] - size * math.sin(angle + 0.45))),
    ]
    draw.polygon(pts, fill=color)


def arrow(draw: ImageDraw.ImageDraw, a: tuple[int, int], b: tuple[int, int],
          color: str, width: int = 5, dashed: bool = False) -> None:
    if dashed:
        dashed_line(draw, a, b, color, width)
    else:
        draw.line((*a, *b), fill=color, width=width)
    arrow_head(draw, a, b, color)


def poly_arrow(draw: ImageDraw.ImageDraw, pts: list[tuple[int, int]],
               color: str, width: int = 4, dashed: bool = False) -> None:
    for a, b in zip(pts, pts[1:]):
        if dashed:
            dashed_line(draw, a, b, color, width)
        else:
            draw.line((*a, *b), fill=color, width=width)
    arrow_head(draw, pts[-2], pts[-1], color)


def small_box(draw: ImageDraw.ImageDraw, box: Box, size: int = 22,
              bold: bool = True, wrap: int | None = None) -> None:
    rounded_box(draw, box, radius=16, width=2)
    center_text(draw, (box.x, box.y, box.x + box.w, box.y + box.h),
                box.label, size, bold=bold, wrap=wrap)


def draw_market_layer(draw: ImageDraw.ImageDraw) -> None:
    users = Box(65, 120, 385, 360, "", "#FFF3C4", "#C98F00")
    inter = Box(590, 120, 620, 360, "", "#EAF3FF", "#1F4E79")
    providers = Box(1350, 120, 385, 360, "", "#DDEEFF", "#2E75B6")
    for box in (users, inter, providers):
        rounded_box(draw, box, radius=26, width=3, shadow=True)
    label_text(draw, (258, 158), "Users", 34, bold=True)
    label_text(draw, (258, 196), "choose brokered, direct,\nor outside option", 22)
    label_text(draw, (900, 158), "API Intermediary", 34, bold=True)
    label_text(draw, (900, 196), "sets retail price pₜ and routing rₘ,ₜ", 24)
    label_text(draw, (1542, 158), "Inference Providers", 34, bold=True)
    label_text(draw, (1542, 196), "post prices under\nfixed GPU capacity", 22)

    small_box(draw, Box(95, 240, 325, 68, "Time-rigid users R\npeak-native demand", "#FFFDF5", "#E1A72D"), 21)
    small_box(draw, Box(95, 330, 325, 68, "Time-flexible users E\nshiftable demand", "#FFFDF5", "#E1A72D"), 21)
    small_box(draw, Box(95, 420, 325, 42, "Outside option: no purchase", "#F7F7F7", "#777777"), 20)

    small_box(draw, Box(630, 260, 160, 82, "Retail\nprice pₜ", "#FFFFFF", "#5B9BD5"), 22)
    small_box(draw, Box(815, 260, 170, 82, "Routing\nrₘ,ₜ", "#FFFFFF", "#5B9BD5"), 22)
    small_box(draw, Box(1010, 260, 160, 82, "Channel\nQoS qᴵₜ", "#FFFFFF", "#5B9BD5"), 22)
    label_text(draw, (900, 408), "Intermediary best response: prices, routing, and QoS signals", 24, bold=True)

    small_box(draw, Box(1380, 240, 325, 64, "Provider A\nlarge capacity G_A", "#F7FBFF", "#2E75B6"), 21)
    small_box(draw, Box(1380, 324, 325, 64, "Provider B\nsmaller capacity G_B", "#F7FBFF", "#2E75B6"), 21)
    small_box(draw, Box(1380, 408, 325, 44, "QoS qₘ,ₜ = qos(Lₘ,ₜ/Gₘ)", "#F7FBFF", "#2E75B6"), 20)

    arrow(draw, (450, 278), (590, 278), "#1F4E79")
    label_text(draw, (520, 248), "preferences\nand demand", 18, wrap=14)
    arrow(draw, (590, 358), (450, 358), "#1769C2")
    label_text(draw, (520, 388), "price and\nQoS signal", 18, wrap=14)
    arrow(draw, (1210, 278), (1350, 278), "#E6A400")
    label_text(draw, (1280, 248), "routed\nload", 18)
    arrow(draw, (1350, 358), (1210, 358), "#1769C2")
    label_text(draw, (1280, 388), "prices and\nQoS feedback", 18, wrap=14)
    poly_arrow(draw, [(420, 475), (500, 520), (1320, 520), (1385, 480)], "#1769C2", dashed=True)
    label_text(draw, (705, 505), "direct API access bypasses the intermediary", 19)


def draw_simulation_layer(draw: ImageDraw.ImageDraw) -> None:
    rounded_box(draw, Box(95, 570, 1610, 160, "", "#EEF6FF", "#5B9BD5"), radius=24, width=3)
    label_text(draw, (900, 600), "Simulation fixed point", 30, bold=True)
    steps = [
        ("Prices\npₜ, wₘ,ₜ, pᴰₘ,ₜ", 145),
        ("Choice shares\nsᶿₖ,ₜ and sᶿ₀", 385),
        ("Demand and routing\nDᶿₖ,ₜ, rₘ,ₜ", 635),
        ("Load and utilization\nLₘ,ₜ, uₘ,ₜ", 895),
        ("QoS and profit\nqₘ,ₜ, Π", 1155),
        ("Regret inputs\nbest responses", 1410),
    ]
    for label, x in steps:
        small_box(draw, Box(x, 640, 205, 58, label, "#FFFFFF", "#5B9BD5"), 18, wrap=22)
    for x in [350, 600, 860, 1120, 1375]:
        arrow(draw, (x, 669), (x + 35, 669), "#1F4E79", width=4)
    arrow(draw, (900, 480), (900, 570), "#0B3C5D", width=6)


def draw_diagnostic_layer(draw: ImageDraw.ImageDraw) -> None:
    rounded_box(draw, Box(190, 790, 1420, 118, "", "#FFF4D1", "#E6A400"), radius=24, width=3)
    label_text(draw, (900, 820), "Finite-grid equilibrium diagnostic", 28, bold=True)
    steps = [
        ("Provider candidate grids\n64 coarse / 225 fine", 245, 250),
        ("Intermediary response\ngrid Y", 540, 210),
        ("Regret scan\nρ = max deviation", 790, 220),
        ("Mixed oracle\n5×5 support; regret 0.203", 1070, 285),
    ]
    for label, x, width in steps:
        small_box(draw, Box(x, 852, width, 42, label, "#FFFFFF", "#E6A400"), 17, wrap=25)
    for x in [495, 750, 1010]:
        arrow(draw, (x, 873), (x + 42, 873), "#0B3C5D", width=4)
    poly_arrow(draw, [(1495, 852), (1660, 852), (1660, 452)], "#0B3C5D", width=4, dashed=True)
    label_text(draw, (1585, 695), "diagnostic\nfeedback", 17, color="#0B3C5D")


def draw_legend(draw: ImageDraw.ImageDraw) -> None:
    rounded_box(draw, Box(120, 940, 1560, 54, "", "#FFFFFF", "#AEB6BF"), radius=16, width=2)
    items = [
        ("#1F4E79", "user demand / QoS status", False),
        ("#1769C2", "price, signal, or direct access", True),
        ("#E6A400", "routed load", False),
        ("#0B3C5D", "fixed-point / regret iteration", True),
        ("#6D6D6D", "outside option", False),
    ]
    xs = [180, 500, 850, 1120, 1410]
    for x, (color, label, dashed) in zip(xs, items):
        arrow(draw, (x, 967), (x + 55, 967), color, width=4, dashed=dashed)
        label_text(draw, (x + 155, 967), label, 17)


def draw_preview() -> None:
    img = Image.new("RGB", (W, H), "#FBFCFE")
    draw = ImageDraw.Draw(img)
    label_text(draw, (900, 58), "Inference-service market and simulation workflow", 38, bold=True)
    label_text(draw, (900, 94), "users choose channels; the intermediary routes traffic; providers respond under fixed GPU capacity",
               22, color="#4B5563")
    draw_market_layer(draw)
    draw_simulation_layer(draw)
    draw_diagnostic_layer(draw)
    draw_legend(draw)
    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT_PNG, dpi=(300, 300))


class Drawio:
    def __init__(self) -> None:
        self.next_id = 2
        self.root = ET.Element("root")
        ET.SubElement(self.root, "mxCell", id="0")
        ET.SubElement(self.root, "mxCell", id="1", parent="0")

    def add_rect(self, box: Box, font_size: int = 18, bold: bool = False) -> str:
        style = (
            "rounded=1;whiteSpace=wrap;html=1;arcSize=12;"
            f"fillColor={box.fill};strokeColor={box.stroke};strokeWidth=2;"
            f"fontFamily=Times New Roman;fontSize={font_size};"
            f"fontStyle={1 if bold else 0};align=center;verticalAlign=middle;"
        )
        return self._vertex(box, style)

    def add_text(self, x: int, y: int, w: int, h: int, label: str,
                 size: int = 18, bold: bool = False, color: str = "#1F2937") -> str:
        style = (
            "text;html=1;strokeColor=none;fillColor=none;whiteSpace=wrap;"
            f"fontFamily=Times New Roman;fontSize={size};fontColor={color};"
            f"fontStyle={1 if bold else 0};align=center;verticalAlign=middle;"
        )
        return self._vertex(Box(x, y, w, h, label, "none", "none"), style)

    def add_edge(self, a: tuple[int, int], b: tuple[int, int], color: str,
                 dashed: bool = False, width: int = 3) -> None:
        style = f"endArrow=block;html=1;rounded=1;strokeColor={color};strokeWidth={width};"
        if dashed:
            style += "dashed=1;dashPattern=8 6;"
        cell = ET.SubElement(self.root, "mxCell", id=str(self.next_id), value="",
                             style=style, edge="1", parent="1")
        self.next_id += 1
        geom = ET.SubElement(cell, "mxGeometry", relative="1", attrib={"as": "geometry"})
        ET.SubElement(geom, "mxPoint", x=str(a[0]), y=str(a[1]), attrib={"as": "sourcePoint"})
        ET.SubElement(geom, "mxPoint", x=str(b[0]), y=str(b[1]), attrib={"as": "targetPoint"})

    def _vertex(self, box: Box, style: str) -> str:
        cell_id = str(self.next_id)
        self.next_id += 1
        cell = ET.SubElement(self.root, "mxCell", id=cell_id, value=self.html(box.label),
                             style=style, vertex="1", parent="1")
        ET.SubElement(cell, "mxGeometry", x=str(box.x), y=str(box.y),
                      width=str(box.w), height=str(box.h), attrib={"as": "geometry"})
        return cell_id

    @staticmethod
    def html(label: str) -> str:
        return "<div>" + "<br>".join(escape(line) for line in label.split("\n")) + "</div>"

    def write(self, path: Path) -> None:
        graph = ET.Element("mxGraphModel", dx=str(W), dy=str(H), grid="1", gridSize="10",
                           guides="1", tooltips="1", connect="1", arrows="1", fold="1",
                           page="1", pageScale="1", pageWidth=str(W), pageHeight=str(H),
                           math="0", shadow="0")
        graph.append(self.root)
        diagram = ET.Element("diagram", name="Page-1")
        diagram.append(graph)
        mxfile = ET.Element("mxfile", host="drawio", version="26.0.0")
        mxfile.append(diagram)
        tree = ET.ElementTree(mxfile)
        ET.indent(tree, space="  ")
        path.parent.mkdir(parents=True, exist_ok=True)
        tree.write(path, encoding="UTF-8", xml_declaration=True)


def build_drawio() -> None:
    dx = Drawio()
    dx.add_text(520, 30, 760, 60, "Inference-service market and simulation workflow", 30, True)
    for box in [
        Box(65, 120, 385, 360, "Users\nchoose brokered, direct,\nor outside option", "#FFF3C4", "#C98F00"),
        Box(590, 120, 620, 360, "API Intermediary\nsets retail price pₜ and routing rₘ,ₜ", "#EAF3FF", "#1F4E79"),
        Box(1350, 120, 385, 360, "Inference Providers\npost prices under\nfixed GPU capacity", "#DDEEFF", "#2E75B6"),
        Box(95, 570, 1610, 160, "Simulation fixed point", "#EEF6FF", "#5B9BD5"),
        Box(190, 790, 1420, 118, "Finite-grid equilibrium diagnostic", "#FFF4D1", "#E6A400"),
    ]:
        dx.add_rect(box, 24, True)
    for box in [
        Box(95, 240, 325, 68, "Time-rigid users R\npeak-native demand", "#FFFDF5", "#E1A72D"),
        Box(95, 330, 325, 68, "Time-flexible users E\nshiftable demand", "#FFFDF5", "#E1A72D"),
        Box(95, 420, 325, 42, "Outside option: no purchase", "#F7F7F7", "#777777"),
        Box(630, 260, 160, 82, "Retail\nprice pₜ", "#FFFFFF", "#5B9BD5"),
        Box(815, 260, 170, 82, "Routing\nrₘ,ₜ", "#FFFFFF", "#5B9BD5"),
        Box(1010, 260, 160, 82, "Channel\nQoS qᴵₜ", "#FFFFFF", "#5B9BD5"),
        Box(1380, 240, 325, 64, "Provider A\nlarge capacity G_A", "#F7FBFF", "#2E75B6"),
        Box(1380, 324, 325, 64, "Provider B\nsmaller capacity G_B", "#F7FBFF", "#2E75B6"),
        Box(1380, 408, 325, 44, "QoS qₘ,ₜ = qos(Lₘ,ₜ/Gₘ)", "#F7FBFF", "#2E75B6"),
        Box(145, 640, 205, 58, "Prices\npₜ, wₘ,ₜ, pᴰₘ,ₜ", "#FFFFFF", "#5B9BD5"),
        Box(385, 640, 205, 58, "Choice shares\nsᶿₖ,ₜ and sᶿ₀", "#FFFFFF", "#5B9BD5"),
        Box(635, 640, 205, 58, "Demand and routing\nDᶿₖ,ₜ, rₘ,ₜ", "#FFFFFF", "#5B9BD5"),
        Box(895, 640, 205, 58, "Load and utilization\nLₘ,ₜ, uₘ,ₜ", "#FFFFFF", "#5B9BD5"),
        Box(1155, 640, 205, 58, "QoS and profit\nqₘ,ₜ, Π", "#FFFFFF", "#5B9BD5"),
        Box(1410, 640, 205, 58, "Regret inputs\nbest responses", "#FFFFFF", "#5B9BD5"),
        Box(245, 852, 250, 42, "Provider candidate grids\n64 coarse / 225 fine", "#FFFFFF", "#E6A400"),
        Box(540, 852, 210, 42, "Intermediary response\ngrid Y", "#FFFFFF", "#E6A400"),
        Box(790, 852, 220, 42, "Regret scan\nρ = max deviation", "#FFFFFF", "#E6A400"),
        Box(1070, 852, 285, 42, "Mixed oracle\n5×5 support; regret 0.203", "#FFFFFF", "#E6A400"),
    ]:
        dx.add_rect(box, 17, False)
    for a, b, color, dashed in [
        ((450, 278), (590, 278), "#1F4E79", False),
        ((590, 358), (450, 358), "#1769C2", False),
        ((1210, 278), (1350, 278), "#E6A400", False),
        ((1350, 358), (1210, 358), "#1769C2", False),
        ((420, 475), (1385, 480), "#1769C2", True),
        ((900, 480), (900, 570), "#0B3C5D", False),
        ((1495, 852), (1660, 452), "#0B3C5D", True),
    ]:
        dx.add_edge(a, b, color, dashed=dashed, width=4)
    dx.write(OUT_DRAWIO)


def main() -> None:
    build_drawio()
    draw_preview()
    print({"drawio": str(OUT_DRAWIO.relative_to(ROOT)), "png": str(OUT_PNG.relative_to(ROOT))})


if __name__ == "__main__":
    main()
