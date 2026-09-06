"""Editable application-to-user-game framework with a measured utility inset."""
from __future__ import annotations

import hashlib
import json

from experiments.run_user_provider_game import OUT as DATA_DIR
from experiments.run_user_provider_game import ROOT
from figure_sources import build_iot_framework as drawing

OUT = ROOT / "figures/user_provider_game_20260906"


def build():
    data = json.loads((DATA_DIR / "analysis.json").read_text())
    case = data["time_switch_example"]
    drawing.ASSETS = ROOT / "figure_sources/llm_user_framework_assets"
    drawing.OUT = OUT
    drawing.SOURCE = ROOT / "figure_sources/user_game_framework_20260906.drawio"
    s = drawing.Scene()
    s.svg.set("viewBox", "0 0 1600 790")
    s.svg.set("height", "88.875mm")
    s.diagram.mxfile.find(".//mxGraphModel").set("pageHeight", "790")
    for key, label, x, w in (("clients", "LLM applications", 20, 410),
                             ("users", "Users choose their own time", 490, 535),
                             ("firms", "Competing manufacturers", 1210, 375)):
        s.text(key, label, (x, 20, w, 45), 29, True)
    for key, label, x, y in (("coding", "Coding", 40, 175), ("conversation", "Dialogue", 250, 175),
                            ("word", "Writing", 40, 430), ("excel", "Data analysis", 250, 430)):
        s.icon(key, key, (x + 30, y, 110, 110))
        s.text(key + "_label", label, (x, y + 125, 180, 36), 27, True)
    s.line("request", ((430, 373), (495, 373)))
    s.text("request_label", "Requests", (350, 330, 145, 30), 22)
    s.box("user_choice", (495, 100, 515, 570), "white", drawing.TEAL)
    s.text("objective", "Maximize individual net utility", (510, 119, 485, 40), 28, True, drawing.TEAL)
    s.text("tradeoff", "Bill + delay + switching + congestion", (510, 166, 485, 35), 25)
    for t in range(8):
        s.box(f"period_{t}", (524 + 59 * t, 223, 47, 38), drawing.TEAL_FILL if t < 3 else "#F4F4F4", drawing.LINE)
        s.text(f"period_label_{t}", str(t + 1), (524 + 59 * t, 223, 47, 38), 24)
    s.text("feasible", "Example: release 1, deadline 3", (515, 278, 475, 33), 24)
    s.text("curve_title", "User 37: utility at manufacturer B", (515, 325, 475, 34), 25, True)
    s.line("y_axis", ((575, 556), (575, 378)), arrow=False)
    s.line("x_axis", ((575, 556), (958, 556)), arrow=False)
    for value in (1.15, 1.25, 1.35):
        y = 550 - (value - 1.10) / .25 * 165
        s.text(f"tick_{value}", f"{value:.2f}", (512, y - 13, 55, 26), 20)
    for index in range(3):
        s.text(f"time_{index}", str(index + 1), (591 + index * 165, 562, 32, 26), 22)
    for curve in case["curves"]:
        color = "#83888D" if curve["state"] == "before" else drawing.TEAL
        values = curve["utility_by_action"][8:11]
        points = tuple((607 + i * 165, 550 - (v - 1.10) / .25 * 165) for i, v in enumerate(values))
        key = "curve_" + curve["state"]
        s.line(key, points, dashed=curve["state"] == "before", arrow=False)
        s.svg[-1].set("stroke", color)
        s.svg[-1].set("stroke-width", "3.5")
        cell = s.diagram.root.find(f"mxCell[@id='{key}']")
        cell.set("style", cell.get("style").replace("strokeColor=#237D81", f"strokeColor={color}").replace("strokeColor=#24323D", f"strokeColor={color}"))
    s.text("legend", "Before (dashed); after (solid)", (517, 595, 475, 30), 22)
    s.text("actual_move", "Chosen time: period 1 to period 2", (517, 632, 475, 30), 24, True)
    s.line("choices", ((1010, 450), (1100, 450), (1100, 256), (1220, 256)))
    s.line("choices_b", ((1100, 450), (1100, 532), (1220, 532)))
    s.text("choice_label", "User choices", (1015, 181, 198, 38), 23)
    for key, label, y, cap, fill, color in (("provider_a", "Manufacturer A", 140, 30, drawing.BLUE_FILL, drawing.BLUE),
                                           ("provider_b", "Manufacturer B", 445, 12, drawing.RUST_FILL, drawing.RUST)):
        s.box(key + "_box", (1220, y, 350, 180), fill, color)
        s.text(key + "_title", label, (1230, y + 10, 330, 38), 28, True, color)
        s.icon(key, key, (1238, y + 69, 80, 80))
        s.text(key + "_detail", f"Set period prices\nReference capacity: {cap}", (1325, y + 67, 235, 86), 23)
    s.line("competition", ((1395, 328), (1395, 433)), dashed=True, both=True)
    s.text("competition_label", "Price competition", (1214, 366, 175, 39), 22)
    s.line("feedback", ((1460, 640), (1460, 721), (750, 721), (750, 675)), dashed=True)
    s.text("feedback_label", "Posted prices and load-dependent QoS", (901, 728, 620, 38), 25, color=drawing.TEAL)
    s.text("scope", "Direct access; intermediary is an extension", (27, 694, 580, 40), 23, color=drawing.MUTED)
    s.save(stem="user_game_framework")
    manifest = {"experiment_sha256": data["experiment_sha256"],
                "analysis_sha256": hashlib.sha256((DATA_DIR / "analysis.json").read_bytes()).hexdigest(),
                "script_sha256": hashlib.sha256((ROOT / "figure_sources/build_user_game_framework.py").read_bytes()).hexdigest(),
                "example_selection": case["selection"], "user_id": case["id"],
                "icon_sources": "figure_sources/llm_user_framework_assets/sources.json"}
    (OUT / "framework_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(OUT)


if __name__ == "__main__":
    build()
