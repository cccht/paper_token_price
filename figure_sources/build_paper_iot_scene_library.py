from __future__ import annotations

import json
import math
from html import escape
from pathlib import Path

import cairosvg

from build_paper_icon_library import (
    CJK_FONT_FAMILY,
    FONT_FAMILY,
    flatten_icons,
    lighten,
    load_manifest as load_base_manifest,
    svg_data_uri,
    themed_svg,
)


PROJECT = Path(__file__).resolve().parents[1]
SCENE_DIR = PROJECT / "figure_sources" / "paper_iot_scene_library"
SCENE_MANIFEST = SCENE_DIR / "manifest.json"
SCENES_OUTPUT = SCENE_DIR / "scenes"
DRAWIO_LIBRARY = SCENE_DIR / "paper-iot-scenes.xml"
PREVIEW_SVG = PROJECT / "figures" / "paper_iot_scene_library_2026-07-10.svg"
PREVIEW_PNG = PROJECT / "figures" / "paper_iot_scene_library_2026-07-10.png"
PREVIEW_PDF = PROJECT / "figures" / "paper_iot_scene_library_2026-07-10.pdf"
SCENE_WIDTH = 480
SCENE_HEIGHT = 300
SHEET_WIDTH = 3600
SHEET_HEIGHT = 2050


def load_scene_manifest() -> dict:
    return json.loads(SCENE_MANIFEST.read_text(encoding="utf-8"))


def base_icons_by_id() -> dict[str, dict]:
    return {icon["id"]: icon for icon in flatten_icons(load_base_manifest())}


def component_center(component: dict) -> tuple[float, float]:
    half = component["size"] / 2
    return component["x"] + half, component["y"] + half


def shortened_edge(source: dict, target: dict) -> tuple[float, float, float, float]:
    sx, sy = component_center(source)
    tx, ty = component_center(target)
    dx, dy = tx - sx, ty - sy
    distance = max(math.hypot(dx, dy), 1)
    ux, uy = dx / distance, dy / distance
    source_gap = source["size"] * 0.58
    target_gap = target["size"] * 0.58
    return sx + ux * source_gap, sy + uy * source_gap, tx - ux * target_gap, ty - uy * target_gap


def marker_def(marker_id: str, color: str) -> str:
    return (
        f'<marker id="{marker_id}" markerWidth="10" markerHeight="10" refX="9" refY="3" '
        f'orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="{color}"/></marker>'
    )


def link_svg(scene: dict, link: dict, index: int) -> tuple[str, str]:
    source = scene["components"][link["from"]]
    target = scene["components"][link["to"]]
    sx, sy, tx, ty = shortened_edge(source, target)
    color = link.get("color", scene["accent"])
    marker_id = f"arrow-{index}"
    dash = ' stroke-dasharray="8 7"' if link["kind"] in {"dashed", "feedback"} else ""
    if link["kind"] == "feedback":
        control_y = 258
        path = f'M {sx:.1f} {sy:.1f} C {sx:.1f} {control_y} {tx:.1f} {control_y} {tx:.1f} {ty:.1f}'
    else:
        path = f'M {sx:.1f} {sy:.1f} L {tx:.1f} {ty:.1f}'
    node = (
        f'<path d="{path}" fill="none" stroke="{color}" stroke-width="4" '
        f'stroke-linecap="round" marker-end="url(#{marker_id})"{dash}/>'
    )
    return marker_def(marker_id, color), node


def component_svg(scene: dict, component: dict, icons: dict[str, dict]) -> str:
    x, y, size = component["x"], component["y"], component["size"]
    color = component.get("color", scene["accent"])
    icon = {**icons[component["icon"]], "color": color}
    parts = []
    if component.get("panel", True):
        parts.append(
            f'<rect x="{x - 10}" y="{y - 4}" width="{size + 20}" height="{size + 20}" '
            f'rx="18" fill="#000000" opacity="0.09" transform="translate(5 7)"/>'
        )
        parts.append(
            f'<rect x="{x - 10}" y="{y - 4}" width="{size + 20}" height="{size + 20}" '
            f'rx="18" fill="#FFFFFF" stroke="{lighten(color, 0.35)}" stroke-width="2.5"/>'
        )
    parts.append(
        f'<image x="{x}" y="{y}" width="{size}" height="{size}" href="{svg_data_uri(themed_svg(icon))}"/>'
    )
    return "".join(parts)


def badge_svg(badge: dict) -> str:
    width = max(58, 18 + len(badge["text"]) * 10)
    x, y, color = badge["x"], badge["y"], badge["color"]
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="34" rx="17" fill="{color}"/>'
        f'<text x="{x + width / 2}" y="{y + 23}" font-family="{FONT_FAMILY}" font-size="18" '
        f'font-weight="bold" fill="#FFFFFF" text-anchor="middle">{escape(badge["text"])}</text>'
    )


def spatial_base(scene: dict) -> str:
    accent = scene["accent"]
    shadow = '<path d="M25 223 L184 139 L457 195 L294 284 Z" fill="#000000" opacity="0.08" transform="translate(0 7)"/>'
    plate = (
        f'<path d="M25 223 L184 139 L457 195 L294 284 Z" fill="{lighten(accent, 0.91)}" '
        f'stroke="{lighten(accent, 0.25)}" stroke-width="2.5"/>'
    )
    grid = (
        f'<path d="M82 228 L238 151 M153 244 L308 166 M225 260 L378 181 M298 276 L448 197" '
        f'stroke="{accent}" opacity="0.10" stroke-width="2"/>'
    )
    return shadow + plate + grid


def render_scene(scene: dict, icons: dict[str, dict]) -> str:
    marker_defs, links = [], []
    for index, link in enumerate(scene.get("links", [])):
        marker, node = link_svg(scene, link, index)
        marker_defs.append(marker)
        links.append(node)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SCENE_WIDTH}" height="{SCENE_HEIGHT}" ',
        f'viewBox="0 0 {SCENE_WIDTH} {SCENE_HEIGHT}">',
        f'<defs>{"".join(marker_defs)}</defs>',
        spatial_base(scene),
        "".join(links),
    ]
    parts.extend(component_svg(scene, component, icons) for component in scene["components"])
    parts.extend(badge_svg(badge) for badge in scene.get("badges", []))
    parts.append("</svg>")
    return "".join(parts)


def write_scene_assets(manifest: dict, icons: dict[str, dict]) -> dict[str, str]:
    SCENES_OUTPUT.mkdir(parents=True, exist_ok=True)
    rendered = {}
    for scene in manifest["scenes"]:
        svg = render_scene(scene, icons)
        rendered[scene["id"]] = svg
        (SCENES_OUTPUT / f"{scene['id']}.svg").write_text(svg, encoding="utf-8")
    return rendered


def write_drawio_library(manifest: dict, rendered: dict[str, str]) -> None:
    entries = []
    for scene in manifest["scenes"]:
        entries.append(
            {
                "id": scene["id"],
                "title": f"{scene['label_en']} / {scene['label_zh']}",
                "data": svg_data_uri(rendered[scene["id"]]),
                "w": SCENE_WIDTH,
                "h": SCENE_HEIGHT,
                "aspect": "fixed",
            }
        )
    payload = json.dumps(entries, ensure_ascii=False, separators=(",", ":"))
    DRAWIO_LIBRARY.write_text(f"<mxlibrary>{payload}</mxlibrary>\n", encoding="utf-8")


def contact_card(scene: dict, svg: str, index: int) -> str:
    column, row = index % 6, index // 6
    x, y = 45 + column * 590, 170 + row * 610
    accent = scene["accent"]
    optional = scene["priority"] == "optional"
    dash = 'stroke-dasharray="10 8"' if optional else ""
    parts = [
        f'<rect x="{x}" y="{y}" width="560" height="580" rx="20" fill="#FFFFFF" '
        f'stroke="{accent}" stroke-width="2.5" {dash}/>',
        f'<image x="{x + 40}" y="{y + 34}" width="480" height="300" href="{svg_data_uri(svg)}"/>',
    ]
    title_style = f'font-family="{FONT_FAMILY}" font-size="27" font-weight="bold" fill="#344054" text-anchor="middle"'
    parts.append(f'<text x="{x + 280}" y="{y + 390}" {title_style}>{escape(scene["label_en"])}</text>')
    parts.append(
        f'<text x="{x + 280}" y="{y + 432}" font-family="{CJK_FONT_FAMILY}" font-size="23" '
        f'fill="#667085" text-anchor="middle">{escape(scene["label_zh"])}</text>'
    )
    priority = "Core" if not optional else "Optional"
    fill = accent if not optional else "#E9EDF2"
    text_fill = "#FFFFFF" if not optional else "#596579"
    parts.append(f'<rect x="{x + 423}" y="{y + 507}" width="112" height="38" rx="19" fill="{fill}"/>')
    parts.append(
        f'<text x="{x + 479}" y="{y + 533}" font-family="{FONT_FAMILY}" font-size="18" '
        f'fill="{text_fill}" text-anchor="middle">{priority}</text>'
    )
    group = scene["group"].replace("_", " ").title()
    parts.append(
        f'<text x="{x + 28}" y="{y + 533}" font-family="{FONT_FAMILY}" font-size="18" '
        f'fill="{accent}">{escape(group)}</text>'
    )
    return "".join(parts)


def build_contact_sheet(manifest: dict, rendered: dict[str, str]) -> str:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SHEET_WIDTH}" height="{SHEET_HEIGHT}" ',
        f'viewBox="0 0 {SHEET_WIDTH} {SHEET_HEIGHT}">',
        '<rect width="100%" height="100%" fill="#FFFFFF"/>',
        f'<text x="45" y="76" font-family="{FONT_FAMILY}" font-size="56" font-weight="bold" fill="#243B53">',
        "Inference Pricing IoT Scene Library</text>",
        f'<text x="47" y="121" font-family="{FONT_FAMILY}" font-size="24" fill="#596579">',
        "18 editable multi-object SVG scenes | composed from the licensed IconPark base library | no generative artwork</text>",
    ]
    parts.extend(
        contact_card(scene, rendered[scene["id"]], index)
        for index, scene in enumerate(manifest["scenes"])
    )
    parts.append("</svg>")
    return "".join(parts)


def write_contact_sheet(svg: str) -> None:
    PREVIEW_SVG.write_text(svg, encoding="utf-8")
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(PREVIEW_PNG))
    cairosvg.svg2pdf(bytestring=svg.encode("utf-8"), write_to=str(PREVIEW_PDF))


def main() -> None:
    manifest = load_scene_manifest()
    icons = base_icons_by_id()
    rendered = write_scene_assets(manifest, icons)
    write_drawio_library(manifest, rendered)
    write_contact_sheet(build_contact_sheet(manifest, rendered))
    print(f"scenes={len(rendered)}")
    print(f"drawio={DRAWIO_LIBRARY}")
    print(f"preview={PREVIEW_PNG}")


if __name__ == "__main__":
    main()
