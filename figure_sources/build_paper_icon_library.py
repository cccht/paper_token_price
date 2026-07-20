from __future__ import annotations

import base64
import json
import textwrap
from dataclasses import dataclass
from html import escape
from pathlib import Path
from xml.etree import ElementTree

import cairosvg


PROJECT = Path(__file__).resolve().parents[1]
LIBRARY_DIR = PROJECT / "figure_sources" / "paper_icon_library"
MANIFEST_PATH = LIBRARY_DIR / "manifest.json"
DRAWIO_LIBRARY_PATH = LIBRARY_DIR / "paper-icons.xml"
PREVIEW_SVG = PROJECT / "figures" / "paper_icon_library_2026-07-10.svg"
PREVIEW_PNG = PROJECT / "figures" / "paper_icon_library_2026-07-10.png"
PREVIEW_PDF = PROJECT / "figures" / "paper_icon_library_2026-07-10.pdf"
CANVAS_WIDTH = 3200
CANVAS_HEIGHT = 2240
FONT_FAMILY = "Times New Roman"
CJK_FONT_FAMILY = "SimSun"


@dataclass(frozen=True)
class Box:
    x: float
    y: float
    width: float
    height: float


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def flatten_icons(manifest: dict) -> list[dict]:
    entries = []
    for category in manifest["categories"]:
        for icon in category["icons"]:
            entries.append({**icon, "category": category["id"], "color": category["color"]})
    return entries


def validate_sources(manifest: dict) -> None:
    categories = manifest["categories"]
    icons = flatten_icons(manifest)
    if len(categories) != 6 or any(len(category["icons"]) != 8 for category in categories):
        raise ValueError("The library must contain six categories with eight icons each")
    if len({icon["id"] for icon in icons}) != len(icons):
        raise ValueError("Icon IDs must be unique")
    for icon in icons:
        path = LIBRARY_DIR / "upstream_svg" / icon["source"]
        root = ElementTree.fromstring(path.read_text(encoding="utf-8"))
        if root.attrib.get("viewBox") != "0 0 48 48":
            raise ValueError(f"Unexpected viewBox for {icon['id']}")


def lighten(color: str, amount: float = 0.72) -> str:
    rgb = [int(color[index : index + 2], 16) for index in (1, 3, 5)]
    mixed = [round(channel + (255 - channel) * amount) for channel in rgb]
    return "#" + "".join(f"{channel:02X}" for channel in mixed)


def themed_svg(icon: dict) -> str:
    source = LIBRARY_DIR / "upstream_svg" / icon["source"]
    svg = source.read_text(encoding="utf-8")
    primary = icon["color"]
    secondary = lighten(primary, 0.58)
    substitutions = {
        'stroke="black"': f'stroke="{primary}"',
        'fill="black"': f'fill="{primary}"',
        'fill="#2F88FF"': f'fill="{primary}"',
        'fill="#43CCF8"': f'fill="{secondary}"',
    }
    for original, replacement in substitutions.items():
        svg = svg.replace(original, replacement)
    marker = (
        "<!-- Colour-modified from ByteDance IconPark commit "
        "8dc132da4c85671ba6a5962c87aa2bdafbf158e9. -->"
    )
    insert_at = svg.find(">") + 1
    return svg[:insert_at] + "\n" + marker + svg[insert_at:]


def svg_data_uri(svg: str) -> str:
    payload = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{payload}"


def build_drawio_library(manifest: dict) -> None:
    entries = []
    for icon in flatten_icons(manifest):
        entries.append(
            {
                "id": icon["id"],
                "title": f"{icon['label_en']} / {icon['label_zh']}",
                "data": svg_data_uri(themed_svg(icon)),
                "w": 48,
                "h": 48,
                "aspect": "fixed",
            }
        )
    payload = json.dumps(entries, ensure_ascii=False, separators=(",", ":"))
    DRAWIO_LIBRARY_PATH.write_text(f"<mxlibrary>{payload}</mxlibrary>\n", encoding="utf-8")


def rounded_rect(box: Box, style: str) -> str:
    return (
        f'<rect x="{box.x}" y="{box.y}" width="{box.width}" height="{box.height}" '
        f'rx="18" {style}/>'
    )


def text_node(content: str, position: tuple[float, float], style: str) -> str:
    x, y = position
    return f'<text x="{x}" y="{y}" {style}>{escape(content)}</text>'


def category_title_node(category: dict, index: int, position: tuple[float, float]) -> str:
    x, y = position
    english = escape(f"{index + 1}. {category['label_en']} / ")
    chinese = escape(category["label_zh"])
    return (
        f'<text x="{x}" y="{y}" font-family="{FONT_FAMILY}" font-size="30" '
        f'font-weight="bold" fill="{category["color"]}">{english}'
        f'<tspan font-family="{CJK_FONT_FAMILY}">{chinese}</tspan></text>'
    )


def label_nodes(icon: dict, box: Box) -> list[str]:
    lines = textwrap.wrap(icon["label_en"], width=22)[:2]
    base_y = box.y + 190 - (len(lines) - 1) * 14
    style = f'font-family="{FONT_FAMILY}" font-size="23" fill="#344054" text-anchor="middle"'
    nodes = [text_node(line, (box.x + box.width / 2, base_y + 28 * index), style) for index, line in enumerate(lines)]
    zh_style = f'font-family="{CJK_FONT_FAMILY}" font-size="19" fill="#667085" text-anchor="middle"'
    nodes.append(text_node(icon["label_zh"], (box.x + box.width / 2, box.y + 244), zh_style))
    return nodes


def icon_card(icon: dict, box: Box) -> str:
    core = icon["priority"] == "core"
    border = icon["color"] if core else "#C8CED8"
    dash = "" if core else 'stroke-dasharray="8 7"'
    card = [rounded_rect(box, f'fill="#FFFFFF" stroke="{border}" stroke-width="2" {dash}')]
    image_x = box.x + box.width / 2 - 56
    card.append(
        f'<image x="{image_x}" y="{box.y + 40}" width="112" height="112" '
        f'href="{svg_data_uri(themed_svg(icon))}"/>'
    )
    card.extend(label_nodes(icon, box))
    badge_fill = icon["color"] if core else "#E9EDF2"
    badge_text = "Core" if core else "Optional"
    text_fill = "#FFFFFF" if core else "#596579"
    badge = Box(box.x + box.width - 92, box.y + 14, 76, 28)
    card.append(rounded_rect(badge, f'fill="{badge_fill}" stroke="none"'))
    badge_style = f'font-family="{FONT_FAMILY}" font-size="15" fill="{text_fill}" text-anchor="middle"'
    card.append(text_node(badge_text, (badge.x + badge.width / 2, badge.y + 20), badge_style))
    return "".join(card)


def category_panel(category: dict, index: int) -> str:
    column = index % 2
    row = index // 2
    panel = Box(70 + column * 1575, 205 + row * 665, 1510, 615)
    color = category["color"]
    parts = [rounded_rect(panel, f'fill="{lighten(color, 0.94)}" stroke="{color}" stroke-width="2.5"')]
    parts.append(category_title_node(category, index, (panel.x + 30, panel.y + 48)))
    parts.append(
        f'<line x1="{panel.x + 30}" y1="{panel.y + 66}" x2="{panel.x + panel.width - 30}" '
        f'y2="{panel.y + 66}" stroke="{color}" stroke-width="2" opacity="0.35"/>'
    )
    card_width = 348
    card_height = 252
    for icon_index, icon in enumerate(category["icons"]):
        card_column = icon_index % 4
        card_row = icon_index // 4
        box = Box(
            panel.x + 30 + card_column * 368,
            panel.y + 83 + card_row * 266,
            card_width,
            card_height,
        )
        parts.append(icon_card({**icon, "color": color}, box))
    return "".join(parts)


def build_contact_sheet(manifest: dict) -> str:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_WIDTH}" height="{CANVAS_HEIGHT}" ',
        f'viewBox="0 0 {CANVAS_WIDTH} {CANVAS_HEIGHT}">',
        '<rect width="100%" height="100%" fill="#FFFFFF"/>',
    ]
    title_style = f'font-family="{FONT_FAMILY}" font-size="54" font-weight="bold" fill="#243B53"'
    subtitle_style = f'font-family="{FONT_FAMILY}" font-size="23" fill="#596579"'
    parts.append(text_node("Inference Pricing Paper Icon Library", (70, 78), title_style))
    parts.append(
        text_node(
            "48 editable IconPark SVG assets | 30 core icons + 18 optional materials | Apache-2.0",
            (72, 122),
            subtitle_style,
        )
    )
    parts.append(text_node("Core", (2600, 76), subtitle_style))
    parts.append('<rect x="2548" y="58" width="32" height="22" rx="5" fill="#24557A"/>')
    parts.append(text_node("Optional", (2825, 76), subtitle_style))
    parts.append('<rect x="2767" y="58" width="34" height="22" rx="5" fill="#E9EDF2" stroke="#C8CED8"/>')
    parts.extend(category_panel(category, index) for index, category in enumerate(manifest["categories"]))
    footer_style = f'font-family="{FONT_FAMILY}" font-size="19" fill="#667085"'
    footer = "Use core icons in the manuscript; optional materials are reserved for applied IoT or diagnostic variants."
    parts.append(text_node(footer, (70, 2210), footer_style))
    parts.append("</svg>")
    return "".join(parts)


def write_contact_sheet(svg: str) -> None:
    PREVIEW_SVG.write_text(svg, encoding="utf-8")
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(PREVIEW_PNG))
    cairosvg.svg2pdf(bytestring=svg.encode("utf-8"), write_to=str(PREVIEW_PDF))


def main() -> None:
    manifest = load_manifest()
    validate_sources(manifest)
    build_drawio_library(manifest)
    svg = build_contact_sheet(manifest)
    write_contact_sheet(svg)
    print(f"icons={len(flatten_icons(manifest))}")
    print(f"drawio={DRAWIO_LIBRARY_PATH}")
    print(f"preview={PREVIEW_PNG}")
    print(f"pdf={PREVIEW_PDF}")


if __name__ == "__main__":
    main()
