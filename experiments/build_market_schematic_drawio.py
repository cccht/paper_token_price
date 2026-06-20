"""Generate a Draw.io source and preview for the peak-shaving market schematic."""
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

W, H = 1800, 1080
FONT = "/mnt/c/Windows/Fonts/times.ttf"
BOLD = "/mnt/c/Windows/Fonts/timesbd.ttf"


@dataclass(frozen=True)
class Rect:
    x: int
    y: int
    w: int
    h: int
    label: str
    fill: str
    stroke: str


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = BOLD if bold and Path(BOLD).exists() else FONT
    if Path(path).exists():
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], body: str, size: int,
         color: str = "#1D2636", bold: bool = False, anchor: str = "mm",
         align: str = "center", width: int | None = None) -> None:
    lines: list[str] = []
    for line in body.split("\n"):
        if width:
            lines.extend(textwrap.wrap(line, width=width) or [""])
        else:
            lines.append(line)
    draw.multiline_text(
        xy, "\n".join(lines), font=font(size, bold), fill=color,
        anchor=anchor, align=align, spacing=3,
    )


def rounded(draw: ImageDraw.ImageDraw, rect: Rect, radius: int = 22,
            dash: bool = False, width: int = 3) -> None:
    box = (rect.x, rect.y, rect.x + rect.w, rect.y + rect.h)
    draw.rounded_rectangle(box, radius=radius, fill=rect.fill, outline=None)
    if dash:
        dashed_round_rect(draw, box, rect.stroke, radius, width)
    else:
        draw.rounded_rectangle(box, radius=radius, outline=rect.stroke, width=width)


def dashed_round_rect(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int],
                      color: str, radius: int, width: int) -> None:
    x1, y1, x2, y2 = box
    segments = [(x1 + radius, y1, x2 - radius, y1), (x2, y1 + radius, x2, y2 - radius),
                (x1 + radius, y2, x2 - radius, y2), (x1, y1 + radius, x1, y2 - radius)]
    for x_start, y_start, x_end, y_end in segments:
        dashed_line(draw, (x_start, y_start), (x_end, y_end), color, width)
    draw.arc((x1, y1, x1 + 2 * radius, y1 + 2 * radius), 180, 270, fill=color, width=width)
    draw.arc((x2 - 2 * radius, y1, x2, y1 + 2 * radius), 270, 360, fill=color, width=width)
    draw.arc((x2 - 2 * radius, y2 - 2 * radius, x2, y2), 0, 90, fill=color, width=width)
    draw.arc((x1, y2 - 2 * radius, x1 + 2 * radius, y2), 90, 180, fill=color, width=width)


def dashed_line(draw: ImageDraw.ImageDraw, a: tuple[int, int], b: tuple[int, int],
                color: str, width: int = 3, dash: int = 12, gap: int = 8) -> None:
    ax, ay = a
    bx, by = b
    dist = math.hypot(bx - ax, by - ay)
    if dist == 0:
        return
    ux, uy = (bx - ax) / dist, (by - ay) / dist
    pos = 0.0
    while pos < dist:
        end = min(pos + dash, dist)
        draw.line((ax + ux * pos, ay + uy * pos, ax + ux * end, ay + uy * end), fill=color, width=width)
        pos += dash + gap


def arrow(draw: ImageDraw.ImageDraw, a: tuple[int, int], b: tuple[int, int],
          color: str, width: int = 5, dashed: bool = False) -> None:
    if dashed:
        dashed_line(draw, a, b, color, width)
    else:
        draw.line((*a, *b), fill=color, width=width)
    angle = math.atan2(b[1] - a[1], b[0] - a[0])
    head = 18
    pts = [
        b,
        (int(b[0] - head * math.cos(angle - 0.45)), int(b[1] - head * math.sin(angle - 0.45))),
        (int(b[0] - head * math.cos(angle + 0.45)), int(b[1] - head * math.sin(angle + 0.45))),
    ]
    draw.polygon(pts, fill=color)


def draw_icon(draw: ImageDraw.ImageDraw, kind: str, x: int, y: int, color: str) -> None:
    if kind == "users":
        for dx in (0, 28, 56):
            draw.ellipse((x + dx, y, x + dx + 28, y + 28), outline=color, width=3)
            draw.rounded_rectangle((x + dx - 6, y + 35, x + dx + 34, y + 72), 10, outline=color, width=3)
    elif kind == "cloud":
        draw.ellipse((x, y + 20, x + 95, y + 95), outline=color, width=5)
        draw.ellipse((x + 55, y, x + 160, y + 100), outline=color, width=5)
        draw.ellipse((x + 125, y + 25, x + 220, y + 100), outline=color, width=5)
        draw.line((x + 35, y + 100, x + 190, y + 100), fill=color, width=5)
    elif kind == "server":
        for i in range(3):
            draw.rounded_rectangle((x, y + i * 28, x + 82, y + 22 + i * 28), 4, outline=color, width=3)
            draw.ellipse((x + 64, y + 7 + i * 28, x + 73, y + 16 + i * 28), fill=color)
    elif kind == "grid":
        for i in range(4):
            for j in range(5):
                draw.ellipse((x + j * 22, y + i * 22, x + j * 22 + 10, y + i * 22 + 10), fill=color)


class Drawio:
    def __init__(self) -> None:
        self.next_id = 2
        self.root = ET.Element("root")
        ET.SubElement(self.root, "mxCell", id="0")
        ET.SubElement(self.root, "mxCell", id="1", parent="0")

    def add_rect(self, rect: Rect, dashed: bool = False, radius: int = 18,
                 font_size: int = 18, bold: bool = False) -> str:
        style = (
            "rounded=1;whiteSpace=wrap;html=1;arcSize=10;"
            f"fillColor={rect.fill};strokeColor={rect.stroke};strokeWidth=2;"
            f"fontFamily=Times New Roman;fontSize={font_size};"
            f"fontStyle={1 if bold else 0};"
        )
        if dashed:
            style += "dashed=1;dashPattern=8 6;"
        cell_id = str(self.next_id); self.next_id += 1
        cell = ET.SubElement(self.root, "mxCell", id=cell_id, value=self.html(rect.label),
                             style=style, vertex="1", parent="1")
        ET.SubElement(cell, "mxGeometry", x=str(rect.x), y=str(rect.y), width=str(rect.w),
                      height=str(rect.h), attrib={"as": "geometry"})
        return cell_id

    def add_label(self, x: int, y: int, w: int, h: int, label: str,
                  size: int = 18, bold: bool = False, color: str = "#1D2636") -> str:
        style = (
            "text;html=1;strokeColor=none;fillColor=none;whiteSpace=wrap;"
            f"fontFamily=Times New Roman;fontSize={size};fontColor={color};"
            f"fontStyle={1 if bold else 0};align=center;verticalAlign=middle;"
        )
        cell_id = str(self.next_id); self.next_id += 1
        cell = ET.SubElement(self.root, "mxCell", id=cell_id, value=self.html(label),
                             style=style, vertex="1", parent="1")
        ET.SubElement(cell, "mxGeometry", x=str(x), y=str(y), width=str(w), height=str(h),
                      attrib={"as": "geometry"})
        return cell_id

    def add_edge(self, a: tuple[int, int], b: tuple[int, int], color: str,
                 dashed: bool = False, width: int = 3) -> str:
        style = f"endArrow=block;html=1;rounded=1;strokeColor={color};strokeWidth={width};"
        if dashed:
            style += "dashed=1;dashPattern=8 6;"
        cell_id = str(self.next_id); self.next_id += 1
        cell = ET.SubElement(self.root, "mxCell", id=cell_id, value="", style=style, edge="1", parent="1")
        geom = ET.SubElement(cell, "mxGeometry", relative="1", attrib={"as": "geometry"})
        ET.SubElement(geom, "mxPoint", x=str(a[0]), y=str(a[1]), attrib={"as": "sourcePoint"})
        ET.SubElement(geom, "mxPoint", x=str(b[0]), y=str(b[1]), attrib={"as": "targetPoint"})
        return cell_id

    @staticmethod
    def html(label: str) -> str:
        return "<div>" + "<br>".join(escape(line) for line in label.split("\n")) + "</div>"

    def write(self, path: Path) -> None:
        graph = ET.Element("mxGraphModel", dx="1800", dy="1080", grid="1", gridSize="10",
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


def draw_preview() -> None:
    img = Image.new("RGB", (W, H), "#FFFFFF")
    d = ImageDraw.Draw(img)
    draw_panels(d)
    draw_edges(d)
    draw_cards(d)
    draw_legend(d)
    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT_PNG, dpi=(300, 300))


def draw_panels(d: ImageDraw.ImageDraw) -> None:
    rounded(d, Rect(35, 50, 430, 455, "", "#FFF4CF", "#E69F00"), dash=True)
    rounded(d, Rect(610, 50, 575, 455, "", "#EAF6FF", "#1266B0"), dash=True)
    rounded(d, Rect(1335, 50, 430, 455, "", "#FCEBE8", "#D04A3A"), dash=True)
    rounded(d, Rect(70, 570, 1660, 150, "", "#F1F8E9", "#5A9E45"), dash=True)
    rounded(d, Rect(175, 775, 1450, 150, "", "#F3ECFA", "#8E56C2"), dash=True)
    text(d, (250, 85), "Users", 34, bold=True)
    text(d, (250, 125), "Channel choice", 27)
    text(d, (897, 83), "API Intermediary I", 33, bold=True)
    text(d, (897, 124), "chooses retail price pₜ and routing rₘ,ₜ", 24)
    text(d, (1550, 83), "Inference Providers", 33, bold=True)
    text(d, (1550, 124), "fixed GPU serving capacity", 24)
    text(d, (900, 605), "Simulation fixed point", 29, bold=True)
    text(d, (900, 812), "Finite-grid equilibrium diagnostic", 29, bold=True)


def draw_cards(d: ImageDraw.ImageDraw) -> None:
    cards = [
        Rect(60, 160, 380, 85, "Time-rigid users R\npeak-native demand; high switching cost", "#FFF9E8", "#E9B13B"),
        Rect(60, 270, 380, 85, "Time-flexible users E\nshiftable demand; higher price sensitivity", "#FFF9E8", "#E9B13B"),
        Rect(60, 380, 380, 85, "Outside option\nutility u₀; exit share sᶿ₀", "#FFF9E8", "#E9B13B"),
        Rect(635, 295, 120, 95, "Retail price\npₜ", "#FFFFFF", "#5AA1DF"),
        Rect(770, 295, 120, 95, "Routing\nrₘ,ₜ", "#FFFFFF", "#5AA1DF"),
        Rect(905, 295, 120, 95, "Demand\nDᴵₜ", "#FFFFFF", "#5AA1DF"),
        Rect(1040, 295, 120, 95, "Channel QoS\nqᴵₜ", "#FFFFFF", "#5AA1DF"),
        Rect(1360, 155, 380, 78, "Provider A\nlarge capacity G_A", "#FFF8F6", "#D7655B"),
        Rect(1360, 250, 380, 78, "Provider B\nsmall capacity G_B; G_A > G_B", "#FFF8F6", "#D7655B"),
        Rect(1360, 345, 380, 78, "Provider prices\nwholesale wₘ,ₜ; direct pᴰₘ,ₜ", "#FFF8F6", "#D7655B"),
        Rect(1360, 440, 380, 58, "QoS qₘ,ₜ = qos(Lₘ,ₜ / Gₘ)", "#FFF8F6", "#D7655B"),
    ]
    for card in cards:
        rounded(d, card, radius=16)
        text(d, (card.x + card.w // 2, card.y + card.h // 2), card.label, 21, width=30, bold="Provider" in card.label)
    text(d, (897, 220), "Intermediary best response\npₜ, rₘ,ₜ, qᴵₜ", 25, bold=True)
    text(d, (897, 445), "Σₘ rₘ,ₜ = 1;  qᴵₜ = Σₘ rₘ,ₜ qₘ,ₜ", 24, bold=True)
    draw_flow_boxes(d)


def draw_flow_boxes(d: ImageDraw.ImageDraw) -> None:
    labels = [
        "Prices\npₜ, wₘ,ₜ, pᴰₘ,ₜ",
        "Logit shares\nsᶿₖ,ₜ and sᶿ₀",
        "Demand\nDᶿₖ,ₜ",
        "Routing\nrₘ,ₜ",
        "Load\nLₘ,ₜ",
        "Utilization\nuₘ,ₜ",
        "QoS\nqₘ,ₜ and qᴵₜ",
        "Profit\nΠₘ, Πᴵ, Πˢʸˢ",
    ]
    xs = [90, 300, 510, 720, 920, 1120, 1320, 1520]
    for x, label in zip(xs, labels):
        rounded(d, Rect(x, 625, 170, 58, label, "#FFFFFF", "#7EB66B"), radius=13)
        text(d, (x + 85, 654), label, 17, bold=True, width=20)
    for x in [260, 470, 680, 890, 1090, 1290, 1490]:
        arrow(d, (x, 654), (x + 28, 654), "#4E9A3A", 4)
    p_labels = ["Provider candidate grids\n64 coarse / 225 fine", "Intermediary response grid Y", "Joint QoS-routing\nfixed point", "Regret scan\nρ=max deviation", "Mixed oracle\n5x5 support\nmax regret 0.203"]
    xs2 = [220, 510, 780, 1040, 1325]
    ws = [220, 210, 210, 210, 240]
    for x, w, label in zip(xs2, ws, p_labels):
        rounded(d, Rect(x, 836, w, 66, label, "#FFFFFF", "#9D70C9"), radius=13)
        text(d, (x + w // 2, 869), label, 18, bold=True, width=24)
    for x in [440, 720, 990, 1250]:
        arrow(d, (x, 869), (x + 45, 869), "#7A3EB1", 4)


def draw_edges(d: ImageDraw.ImageDraw) -> None:
    arrow(d, (465, 210), (610, 210), "#2B8A3E", 5)
    text(d, (535, 180), "preferences\nand demand", 19, width=14)
    arrow(d, (610, 335), (465, 335), "#1769C2", 5)
    text(d, (535, 305), "retail price pₜ\nQoS signal qᴵₜ", 18, width=16)
    arrow(d, (1185, 205), (1335, 205), "#F07818", 5)
    text(d, (1260, 175), "routed load\nrₘ,ₜ Dᴵₜ", 19, width=14)
    arrow(d, (1335, 300), (1185, 300), "#2B8A3E", 5)
    text(d, (1260, 270), "capacity and\nQoS status", 19, width=14)
    arrow(d, (1335, 395), (1185, 395), "#1769C2", 5)
    text(d, (1260, 365), "wholesale prices\nwₘ,ₜ", 18, width=16)
    dashed_line(d, (470, 535), (1335, 535), "#1769C2", 4)
    arrow(d, (1335, 535), (1390, 505), "#1769C2", 4, dashed=True)
    d.rounded_rectangle((545, 514, 790, 574), 10, fill="#FFFFFF", outline=None)
    text(d, (660, 546), "direct-provider API\noption pᴰₘ,ₜ", 18)
    arrow(d, (250, 465), (250, 540), "#6D6D6D", 4)
    text(d, (250, 555), "exit / no purchase", 18)
    arrow(d, (897, 505), (897, 570), "#7A3EB1", 8)
    arrow(d, (897, 720), (897, 775), "#7A3EB1", 8)
    dashed_line(d, (1690, 775), (1690, 510), "#7A3EB1", 4)
    arrow(d, (1690, 510), (1690, 490), "#7A3EB1", 4, dashed=True)


def draw_legend(d: ImageDraw.ImageDraw) -> None:
    rounded(d, Rect(70, 960, 1660, 75, "", "#FFFFFF", "#ADB5BD"), radius=16)
    items = [("#2B8A3E", "Information flow\n(preferences, QoS status)", False),
             ("#1769C2", "Price / signal flow\n(pₜ, wₘ,ₜ, qᴵₜ)", False),
             ("#F07818", "Token / load flow\n(rₘ,ₜ Dᴵₜ)", False),
             ("#7A3EB1", "Feedback / iteration\n(equilibrium refinement)", False),
             ("#1769C2", "Direct API access\n(user bypasses I)", True),
             ("#6D6D6D", "Exit option\n(no purchase)", False)]
    x_positions = [105, 385, 665, 945, 1225, 1500]
    for x, (color, label, dashed) in zip(x_positions, items):
        arrow(d, (x, 998), (x + 55, 998), color, 4, dashed=dashed)
        text(d, (x + 155, 998), label, 16, anchor="mm", width=21)


def build_drawio() -> None:
    dx = Drawio()
    for rect, dashed in [
        (Rect(35, 50, 430, 455, "", "#FFF4CF", "#E69F00"), True),
        (Rect(610, 50, 575, 455, "", "#EAF6FF", "#1266B0"), True),
        (Rect(1335, 50, 430, 455, "", "#FCEBE8", "#D04A3A"), True),
        (Rect(70, 570, 1660, 150, "", "#F1F8E9", "#5A9E45"), True),
        (Rect(175, 775, 1450, 150, "", "#F3ECFA", "#8E56C2"), True),
        (Rect(70, 960, 1660, 75, "", "#FFFFFF", "#ADB5BD"), False),
    ]:
        dx.add_rect(rect, dashed=dashed)
    add_drawio_labels(dx)
    add_drawio_boxes(dx)
    add_drawio_edges(dx)
    add_drawio_overlay_labels(dx)
    dx.write(OUT_DRAWIO)


def add_drawio_labels(dx: Drawio) -> None:
    labels = [(100, 60, 300, 80, "Users\nChannel choice"), (690, 60, 410, 80, "API Intermediary I\nchooses retail price pₜ and routing rₘ,ₜ"),
              (1410, 60, 300, 80, "Inference Providers\nfixed GPU serving capacity"),
              (735, 575, 330, 45, "Simulation fixed point"), (625, 780, 550, 45, "Finite-grid equilibrium diagnostic"),
              (760, 150, 280, 110, "Intermediary best response\npₜ, rₘ,ₜ, qᴵₜ"),
              (675, 425, 445, 45, "Σₘ rₘ,ₜ = 1; qᴵₜ = Σₘ rₘ,ₜ qₘ,ₜ"),
              (490, 160, 105, 55, "preferences\nand demand"),
              (480, 292, 110, 60, "retail price pₜ\nQoS signal qᴵₜ"),
              (1215, 155, 95, 55, "routed load\nrₘ,ₜ Dᴵₜ"),
              (1215, 255, 105, 60, "capacity and\nQoS status"),
              (1210, 352, 115, 55, "wholesale prices\nwₘ,ₜ"),
              (170, 540, 160, 35, "exit / no purchase"),
              (185, 972, 180, 50, "Information flow\n(preferences, QoS status)"),
              (460, 972, 190, 50, "Price / signal flow\n(pₜ, wₘ,ₜ, qᴵₜ)"),
              (735, 972, 190, 50, "Token / load flow\n(rₘ,ₜ Dᴵₜ)"),
              (1010, 972, 210, 50, "Feedback / iteration\n(equilibrium refinement)"),
              (1295, 972, 175, 50, "Direct API access\n(user bypasses I)"),
              (1570, 972, 175, 50, "Exit option\n(no purchase)")]
    for x, y, w, h, label in labels:
        dx.add_label(x, y, w, h, label, size=26 if h > 70 else 18, bold=h > 70)


def add_drawio_overlay_labels(dx: Drawio) -> None:
    dx.add_rect(
        Rect(545, 514, 245, 60, "direct-provider API\noption pᴰₘ,ₜ", "#FFFFFF", "#FFFFFF"),
        radius=10,
        font_size=17,
    )


def add_drawio_boxes(dx: Drawio) -> None:
    rects = [
        Rect(60, 160, 380, 85, "Time-rigid users R\npeak-native demand; high switching cost", "#FFF9E8", "#E9B13B"),
        Rect(60, 270, 380, 85, "Time-flexible users E\nshiftable demand; higher price sensitivity", "#FFF9E8", "#E9B13B"),
        Rect(60, 380, 380, 85, "Outside option\nutility u₀; exit share sᶿ₀", "#FFF9E8", "#E9B13B"),
        Rect(635, 295, 120, 95, "Retail price\npₜ", "#FFFFFF", "#5AA1DF"),
        Rect(770, 295, 120, 95, "Routing\nrₘ,ₜ", "#FFFFFF", "#5AA1DF"),
        Rect(905, 295, 120, 95, "Demand\nDᴵₜ", "#FFFFFF", "#5AA1DF"),
        Rect(1040, 295, 120, 95, "Channel QoS\nqᴵₜ", "#FFFFFF", "#5AA1DF"),
        Rect(1360, 155, 380, 78, "Provider A\nlarge capacity G_A", "#FFF8F6", "#D7655B"),
        Rect(1360, 250, 380, 78, "Provider B\nsmall capacity G_B; G_A > G_B", "#FFF8F6", "#D7655B"),
        Rect(1360, 345, 380, 78, "Provider prices\nwholesale wₘ,ₜ; direct pᴰₘ,ₜ", "#FFF8F6", "#D7655B"),
        Rect(1360, 440, 380, 58, "QoS qₘ,ₜ = qos(Lₘ,ₜ / Gₘ)", "#FFF8F6", "#D7655B"),
    ]
    flow = [
        Rect(90, 625, 170, 58, "Prices\npₜ, wₘ,ₜ, pᴰₘ,ₜ", "#FFFFFF", "#7EB66B"),
        Rect(300, 625, 170, 58, "Logit shares\nsᶿₖ,ₜ and sᶿ₀", "#FFFFFF", "#7EB66B"),
        Rect(510, 625, 170, 58, "Demand\nDᶿₖ,ₜ", "#FFFFFF", "#7EB66B"),
        Rect(720, 625, 170, 58, "Routing\nrₘ,ₜ", "#FFFFFF", "#7EB66B"),
        Rect(920, 625, 170, 58, "Load\nLₘ,ₜ", "#FFFFFF", "#7EB66B"),
        Rect(1120, 625, 170, 58, "Utilization\nuₘ,ₜ", "#FFFFFF", "#7EB66B"),
        Rect(1320, 625, 170, 58, "QoS\nqₘ,ₜ and qᴵₜ", "#FFFFFF", "#7EB66B"),
        Rect(1520, 625, 170, 58, "Profit\nΠₘ, Πᴵ, Πˢʸˢ", "#FFFFFF", "#7EB66B"),
        Rect(220, 840, 220, 58, "Provider candidate grids\n64 coarse / 225 fine", "#FFFFFF", "#9D70C9"),
        Rect(510, 840, 210, 58, "Intermediary response grid Y", "#FFFFFF", "#9D70C9"),
        Rect(780, 840, 210, 58, "Joint QoS-routing\nfixed point", "#FFFFFF", "#9D70C9"),
        Rect(1040, 840, 210, 58, "Regret scan\nρ=max deviation", "#FFFFFF", "#9D70C9"),
        Rect(1325, 836, 240, 66, "Mixed oracle\n5x5 support\nmax regret 0.203", "#FFFFFF", "#9D70C9"),
    ]
    for r in rects + flow:
        dx.add_rect(r, font_size=17, bold=False)


def add_drawio_edges(dx: Drawio) -> None:
    for a, b, c, dashed, w in [
        ((465, 210), (610, 210), "#2B8A3E", False, 4), ((610, 335), (465, 335), "#1769C2", False, 4),
        ((1185, 205), (1335, 205), "#F07818", False, 4), ((1335, 300), (1185, 300), "#2B8A3E", False, 4),
        ((1335, 395), (1185, 395), "#1769C2", False, 4), ((470, 535), (1390, 505), "#1769C2", True, 3),
        ((250, 465), (250, 540), "#6D6D6D", False, 3), ((897, 505), (897, 570), "#7A3EB1", False, 5),
        ((897, 720), (897, 775), "#7A3EB1", False, 5), ((1690, 775), (1690, 490), "#7A3EB1", True, 3),
    ]:
        dx.add_edge(a, b, c, dashed=dashed, width=w)
    for x in [260, 470, 680, 890, 1090, 1290, 1490]:
        dx.add_edge((x, 654), (x + 28, 654), "#4E9A3A")
    for x in [440, 720, 990, 1250]:
        dx.add_edge((x, 869), (x + 45, 869), "#7A3EB1")
    for a, b, c, dashed in [
        ((105, 998), (160, 998), "#2B8A3E", False),
        ((385, 998), (440, 998), "#1769C2", False),
        ((665, 998), (720, 998), "#F07818", False),
        ((945, 998), (1000, 998), "#7A3EB1", False),
        ((1225, 998), (1280, 998), "#1769C2", True),
        ((1500, 998), (1555, 998), "#6D6D6D", False),
    ]:
        dx.add_edge(a, b, c, dashed=dashed)


def main() -> None:
    build_drawio()
    draw_preview()
    print({"drawio": str(OUT_DRAWIO.relative_to(ROOT)), "png": str(OUT_PNG.relative_to(ROOT))})


if __name__ == "__main__":
    main()
