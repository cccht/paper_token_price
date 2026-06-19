from html import escape
from pathlib import Path
import cairosvg
W, H = 1600, 980
COLORS = {
    "ink": "#17202A",
    "muted": "#5F6F82",
    "line": "#D7E0EA",
    "soft": "#F7FAFD",
    "green": "#258B47",
    "blue": "#0B73C7",
    "navy": "#123B63",
    "orange": "#F39A12",
    "purple": "#7042A5",
    "violet": "#4D2378",
    "gray": "#8B949E",
}
def tag(name: str, attrs: dict[str, object], body: str = "") -> str:
    joined = " ".join(f'{k}="{v}"' for k, v in attrs.items() if v is not None)
    return f"<{name} {joined}>{body}</{name}>"
def text(
    x: float,
    y: float,
    body: str,
    *,
    size: int = 20,
    color: str | None = None,
    weight: int = 500,
    anchor: str = "middle",
) -> str:
    body = body if "<tspan" in body else escape(body)
    return tag(
        "text",
        {
            "x": x,
            "y": y,
            "font-size": size,
            "font-weight": weight,
            "fill": color or COLORS["ink"],
            "text-anchor": anchor,
            "font-family": "Arial, Helvetica, sans-serif",
        },
        body,
    )
def multiline(
    x: float,
    y: float,
    lines: list[str],
    *,
    size: int = 16,
    color: str | None = None,
    weight: int = 500,
    anchor: str = "middle",
    gap: int | None = None,
) -> str:
    gap = gap or int(size * 1.28)
    spans = []
    for idx, line in enumerate(lines):
        dy = 0 if idx == 0 else gap
        spans.append(f'<tspan x="{x}" dy="{dy}">{escape(line)}</tspan>')
    return text(x, y, "".join(spans), size=size, color=color, weight=weight, anchor=anchor)
def rect(
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    fill: str = "white",
    stroke: str | None = None,
    sw: float = 1.5,
    rx: int = 18,
    dashed: bool = False,
) -> str:
    attrs = {"x": x, "y": y, "width": w, "height": h, "rx": rx, "fill": fill}
    if stroke:
        attrs.update({"stroke": stroke, "stroke-width": sw})
    if dashed:
        attrs["stroke-dasharray"] = "10 8"
    return tag("rect", attrs)
def circle(cx: float, cy: float, r: float, *, fill: str, stroke: str | None = None) -> str:
    return tag("circle", {"cx": cx, "cy": cy, "r": r, "fill": fill, "stroke": stroke})
def path(d: str, color: str, *, width: float = 3.0, dashed: bool = False) -> str:
    attrs = {
        "d": d,
        "stroke": color,
        "stroke-width": width,
        "fill": "none",
        "stroke-linecap": "round",
        "stroke-linejoin": "round",
        "marker-end": f"url(#arrow-{color[1:]})",
    }
    if dashed:
        attrs["stroke-dasharray"] = "12 10"
    return tag("path", attrs)
def line(x1: float, y1: float, x2: float, y2: float, color: str, *, width: float = 3.0) -> str:
    return path(f"M{x1} {y1} L{x2} {y2}", color, width=width)
def defs() -> str:
    arrows = []
    for color in [COLORS["green"], COLORS["blue"], COLORS["orange"], COLORS["purple"], COLORS["gray"]]:
        ident = f"arrow-{color[1:]}"
        arrows.append(
            f'<marker id="{ident}" markerWidth="12" markerHeight="12" refX="10" refY="6" '
            f'orient="auto" markerUnits="strokeWidth"><path d="M2,2 L10,6 L2,10 Z" '
            f'fill="{color}"/></marker>'
        )
    shadow = (
        '<filter id="soft-shadow" x="-15%" y="-20%" width="130%" height="150%">'
        '<feDropShadow dx="0" dy="8" stdDeviation="8" flood-color="#17324A" flood-opacity="0.10"/>'
        "</filter>"
    )
    return f"<defs>{''.join(arrows)}{shadow}</defs>"
def label(x: float, y: float, title: str, subtitle: str, color: str) -> str:
    return (
        rect(x - 112, y - 31, 224, 58, fill="white", stroke="#E1E8F0", sw=1.2, rx=12)
        + text(x, y - 7, title, size=17, color=color, weight=800)
        + text(x, y + 16, subtitle, size=14, color=COLORS["muted"], weight=600)
    )
def icon(kind: str, x: float, y: float, color: str) -> str:
    if kind == "chat":
        return (
            rect(x, y, 58, 42, fill="#F3FAF5", stroke=color, sw=2, rx=14)
            + path(f"M{x + 17} {y + 42} L{x + 12} {y + 54} L{x + 30} {y + 42}", color, width=2)
            + circle(x + 20, y + 21, 3, fill=color)
            + circle(x + 31, y + 21, 3, fill=color)
            + circle(x + 42, y + 21, 3, fill=color)
        )
    if kind == "agent":
        return (
            rect(x, y, 62, 46, fill="#F3F7FC", stroke=color, sw=2, rx=8)
            + text(x + 16, y + 30, ">", size=22, color=color, weight=800)
            + tag("line", {"x1": x + 32, "y1": y + 30, "x2": x + 48, "y2": y + 30, "stroke": color, "stroke-width": 3})
        )
    if kind == "flow":
        return (
            circle(x + 12, y + 12, 8, fill="#F3FAF5", stroke=color)
            + circle(x + 50, y + 12, 8, fill="#F3FAF5", stroke=color)
            + circle(x + 31, y + 44, 8, fill="#F3FAF5", stroke=color)
            + tag("path", {"d": f"M{x + 20} {y + 12} L{x + 42} {y + 12} M{x + 16} {y + 18} L{x + 27} {y + 37} M{x + 46} {y + 18} L{x + 35} {y + 37}", "stroke": color, "stroke-width": 2.2, "fill": "none"})
        )
    return (
        text(x + 5, y + 33, "{", size=32, color=color, weight=800)
        + text(x + 31, y + 33, "/", size=28, color=color, weight=800)
        + text(x + 57, y + 33, "}", size=32, color=color, weight=800)
    )
def app_card(y: float, title: str, body: list[str], color: str, kind: str) -> str:
    x, w, h = 48, 340, 112
    return (
        rect(x, y, w, h, fill="white", stroke=COLORS["line"], sw=1.5, rx=26)
        + icon(kind, x + 28, y + 30, color)
        + text(x + 112, y + 44, title, size=22, color=color, weight=800, anchor="start")
        + multiline(x + 112, y + 73, body, size=16, color=COLORS["muted"], anchor="start")
    )
def cloud() -> str:
    return (
        tag("path", {"d": "M535 290 C548 218 615 170 690 186 C727 123 827 108 882 170 C932 161 987 194 998 249 C1059 258 1094 309 1078 364 C1065 409 1024 432 976 432 L592 432 C534 432 490 393 490 340 C490 315 505 296 535 290 Z", "fill": "#EAF6FF", "stroke": "#5DA6E8", "stroke-width": 5, "filter": "url(#soft-shadow)"})
        + rect(594, 280, 70, 104, fill="#183D63", stroke="#0D2B47", sw=2, rx=7)
        + rect(678, 260, 82, 124, fill="#183D63", stroke="#0D2B47", sw=2, rx=7)
        + rect(788, 302, 146, 74, fill="white", stroke="#7CB8E6", sw=3, rx=8)
        + tag("path", {"d": "M815 350 L856 314 L856 337 L906 337", "stroke": COLORS["blue"], "stroke-width": 4, "fill": "none", "marker-end": f"url(#arrow-{COLORS['blue'][1:]})"})
        + circle(622, 321, 6, fill="#55D58A")
        + circle(706, 302, 6, fill="#55D58A")
        + circle(706, 344, 6, fill="#55D58A")
        + text(784, 226, "OpenRouter-like", size=21, color=COLORS["navy"], weight=800)
        + text(784, 255, "API Intermediary", size=18, color=COLORS["navy"], weight=700)
    )
def tool_tile(x: float, title: str, body: str) -> str:
    return (
        rect(x, 466, 132, 92, fill="white", stroke="#5DA6E8", sw=1.7, rx=16)
        + text(x + 66, 501, title, size=20, color=COLORS["blue"], weight=800)
        + text(x + 66, 532, body, size=14, color=COLORS["muted"], weight=600)
    )
def provider_chip(x: float, y: float, name: str, color: str) -> str:
    return (
        rect(x, y, 150, 44, fill="#FBFAFF", stroke="#D9C9EF", sw=1.3, rx=13)
        + circle(x + 22, y + 22, 7, fill=color)
        + text(x + 42, y + 28, name, size=14, color=COLORS["ink"], weight=700, anchor="start")
    )
def supplier_panel() -> str:
    x, y, w = 1208, 178, 332
    chips = [
        provider_chip(x + 20, y + 72, "DeepSeek", "#2B76D2"),
        provider_chip(x + 176, y + 72, "Claude", "#C06B3E"),
        provider_chip(x + 20, y + 126, "GPT / OpenAI", "#18A67A"),
        provider_chip(x + 176, y + 126, "Gemini / Qwen", "#8E5BD3"),
    ]
    compute = [
        rect(x + 28, y + 234, 276, 78, fill="#F9FBFE", stroke="#DFE7EF", sw=1.2, rx=16),
        text(x + 58, y + 268, "GPU", size=18, color=COLORS["violet"], weight=800),
        multiline(x + 106, y + 257, ["GPU pools, cloud regions", "API quota and SLA capacity"], size=15, color=COLORS["muted"], anchor="start"),
    ]
    status = [
        rect(x + 28, y + 340, 276, 78, fill="#F9FBFE", stroke="#DFE7EF", sw=1.2, rx=16),
        text(x + 58, y + 374, "c", size=22, color=COLORS["violet"], weight=800),
        multiline(x + 106, y + 363, ["marginal cost, latency", "availability and incident state"], size=15, color=COLORS["muted"], anchor="start"),
    ]
    return (
        rect(x, y, w, 450, fill="white", stroke=COLORS["line"], sw=1.5, rx=28)
        + text(x + 166, y + 40, "Model API Providers", size=21, color=COLORS["violet"], weight=800)
        + "".join(chips)
        + tag("line", {"x1": x + 28, "y1": y + 218, "x2": x + 304, "y2": y + 218, "stroke": "#E4E9F0", "stroke-width": 2})
        + "".join(compute)
        + tag("line", {"x1": x + 28, "y1": y + 326, "x2": x + 304, "y2": y + 326, "stroke": "#E4E9F0", "stroke-width": 2})
        + "".join(status)
    )
def game_module() -> str:
    x, y = 462, 606
    steps = [
        (512, "Demand", "D_jt"),
        (678, "Retail price", "p_jt"),
        (844, "Capacity route", "g_jt"),
        (1010, "Profit / QoS", "profit, q"),
    ]
    parts = [rect(x, y, 668, 146, fill="white", stroke=COLORS["blue"], sw=2, rx=24, dashed=True)]
    parts.append(text(796, y + 36, "Dynamic Pricing & Stackelberg Game", size=22, color=COLORS["navy"], weight=800))
    for cx, title, symbol in steps:
        parts.append(rect(cx - 58, y + 64, 116, 54, fill="#F9FCFF", stroke="#B8D9F3", sw=1.3, rx=14))
        parts.append(text(cx, y + 89, symbol, size=17, color=COLORS["blue"], weight=800))
        parts.append(text(cx, y + 115, title, size=13, color=COLORS["muted"], weight=600))
    for x1 in [570, 736, 902]:
        parts.append(line(x1, y + 91, x1 + 50, y + 91, COLORS["gray"], width=2))
    return "".join(parts)
def feedback_module() -> str:
    return (
        rect(522, 804, 548, 96, fill="#FFFEFF", stroke="#B897DE", sw=2, rx=24, dashed=True)
        + text(796, 835, "Iterative Feedback (Game Equilibrium)", size=20, color=COLORS["purple"], weight=800)
        + text(640, 874, "update demand", size=15, color=COLORS["muted"], weight=700)
        + rect(742, 852, 108, 34, fill="#F7F1FF", stroke="#C8A8E8", sw=1.2, rx=17)
        + text(796, 876, "SUE / SPE", size=19, color=COLORS["purple"], weight=800)
        + text(948, 874, "update price & routing", size=15, color=COLORS["muted"], weight=700)
    )
def legend() -> str:
    items = [
        (92, COLORS["green"], "Information Flow"),
        (390, COLORS["blue"], "Price / Signal Flow"),
        (710, COLORS["orange"], "Token / Capacity Flow"),
        (1058, COLORS["purple"], "Feedback / Iteration"),
    ]
    parts = [rect(38, 928, 1524, 40, fill="white", stroke=COLORS["line"], sw=1.2, rx=13)]
    for x, color, name in items:
        parts.append(line(x, 948, x + 52, 948, color, width=3))
        parts.append(text(x + 78, 953, name, size=15, color=COLORS["ink"], anchor="start"))
    return "".join(parts)
def build_svg() -> str:
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', defs()]
    parts += [
        rect(0, 0, W, H, fill="white", rx=0),
        text(218, 52, "Users", size=27, color="#0D5C2D", weight=800),
        text(218, 84, "(Applications / API Loads)", size=18, color="#0D5C2D", weight=800),
        text(796, 52, "Cloud Platform / API Intermediary", size=27, color=COLORS["navy"], weight=800),
        text(796, 84, "(OpenRouter-like Aggregator)", size=18, color=COLORS["navy"], weight=800),
        text(1374, 52, "Model Manufacturers / Suppliers", size=27, color=COLORS["violet"], weight=800),
        text(1374, 84, "(LLM APIs & Compute Grid)", size=18, color=COLORS["violet"], weight=800),
        app_card(170, "Chat Apps", ["consumer queries", "elastic timing"], COLORS["green"], "chat"),
        app_card(302, "Coding Agents", ["batch jobs", "retry and fallback"], "#4169A8", "agent"),
        app_card(434, "Enterprise APIs", ["workflow calls", "SLA-sensitive demand"], "#23866F", "flow"),
        app_card(566, "Developers / SDK", ["client calls", "model-time choice"], "#2E8B57", "code"),
        cloud(),
        tool_tile(504, "DB", "usage data"),
        tool_tile(660, "FC", "forecast"),
        tool_tile(816, "OPT", "pricing"),
        tool_tile(972, "QoS", "monitor"),
        supplier_panel(),
        game_module(),
        feedback_module(),
        line(392, 300, 500, 300, COLORS["green"]),
        label(464, 267, "Information", "demand, preference", COLORS["green"]),
        line(500, 386, 392, 386, COLORS["blue"]),
        label(464, 431, "Price / Signals", "retail, incentives", COLORS["blue"]),
        line(1208, 300, 1088, 300, COLORS["green"]),
        label(1134, 267, "Data / Status", "capacity, cost", COLORS["green"]),
        line(1088, 386, 1208, 386, COLORS["blue"]),
        label(1134, 431, "Price / Contracts", "wholesale, quota", COLORS["blue"]),
        line(796, 560, 796, 606, COLORS["gray"], width=2.3),
        path("M390 618 C430 704 456 786 522 852", COLORS["orange"], width=3.4, dashed=True),
        label(390, 778, "Response", "load shifting", COLORS["orange"]),
        path("M1210 618 C1166 704 1138 786 1070 852", COLORS["orange"], width=3.4, dashed=True),
        label(1210, 778, "Token Supply", "quota, capacity", COLORS["orange"]),
        line(796, 752, 796, 804, COLORS["purple"], width=3),
        legend(),
        "</svg>",
    ]
    return "\n".join(parts)
def build_figure(output_base: Path) -> None:
    output_base.parent.mkdir(parents=True, exist_ok=True)
    svg = build_svg()
    svg_path = output_base.with_suffix(".svg")
    pdf_path = output_base.with_suffix(".pdf")
    png_path = output_base.with_suffix(".png")
    svg_path.write_text(svg, encoding="utf-8")
    cairosvg.svg2pdf(bytestring=svg.encode("utf-8"), write_to=str(pdf_path))
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(png_path), output_width=2400)
if __name__ == "__main__":
    build_figure(Path(__file__).resolve().parent / "three_layer_game_framework")
