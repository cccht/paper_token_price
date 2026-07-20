#!/usr/bin/env python3
"""Build the editable framework diagram for the final conserved-demand model."""
from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path
import sys

PROJECT = Path(__file__).resolve().parents[1]
if str(PROJECT) not in sys.path:
    sys.path.insert(0, str(PROJECT))

from figure_sources.build_peak_shaving_framework_drawio import (  # noqa: E402
    Diagram,
    INK,
    PANEL,
    WHITE,
    math_var,
)

OUTPUT = PROJECT / "figure_sources" / "spatiotemporal_pricing_framework_final_2026-07-14.drawio"
GREEN = "#3C5488"
GREEN_FILL = "#E9EDF5"
CYAN = "#6F83B5"
CYAN_FILL = "#F0F3F8"
YELLOW = "#A86464"
YELLOW_FILL = "#F6ECEC"
CORAL = "#A86464"
CORAL_FILL = "#F6ECEC"
GRAY = "#6F6F6F"
GRAY_FILL = "#F5F5F5"


class FinalDiagram(Diagram):
    def save(self) -> None:
        tree = ET.ElementTree(self.mxfile)
        ET.indent(tree, space="  ")
        tree.write(OUTPUT, encoding="utf-8", xml_declaration=True)


def _user(diagram: Diagram, cell_id: str, y: int, title: str, note: str,
          fill: str, stroke: str, icons: tuple[str, str, str]) -> None:
    diagram.box(cell_id, "", (25, y, 250, 205), "market_panel", fill, stroke)
    diagram.text(f"{cell_id}_title", title, (12, 8, 226, 36), cell_id, 21, True, stroke)
    for index, icon in enumerate(icons):
        diagram.icon(f"{cell_id}_icon_{index}", icon, (17 + index * 75, 55, 58, 58), cell_id)
    diagram.text(f"{cell_id}_note", note, (15, 128, 220, 58), cell_id, 18)


def _temporal_allocation(diagram: Diagram) -> None:
    diagram.box("temporal_allocation", "", (320, 82, 285, 500),
                "market_panel", GRAY_FILL, GRAY)
    diagram.text("temporal_title", "Conserved OD temporal allocation",
                 (12, 8, 261, 46), "temporal_allocation", 21, True)
    items = (
        ("native_arrivals", "Native arrivals", "svg/pricing_time/runtime.svg", 72, CYAN_FILL, CYAN),
        ("od_flow", "Flexible OD flow", "svg/api_routing/bidirectional_transfer.svg", 205, YELLOW_FILL, YELLOW),
        ("mass_conservation", "Fixed total demand", "svg/simulation_evidence/market_share_results.svg", 350, GREEN_FILL, GREEN),
    )
    for cell_id, label, icon, y, fill, stroke in items:
        diagram.box(cell_id, "", (25, y, 235, 105), "temporal_allocation", fill, stroke)
        diagram.icon(f"{cell_id}_icon", icon, (12, 18, 58, 58), cell_id)
        diagram.text(f"{cell_id}_label", label, (78, 12, 145, 34), cell_id,
                     18, True, stroke, "left")
        if cell_id == "od_flow":
            formula = f"{math_var('F', 'o,t', 'k')}: |t-o| &le; H_k"
            diagram.text("od_formula", formula, (75, 51, 150, 34), cell_id, 19, False, INK, "left")
        if cell_id == "mass_conservation":
            formula = f"&Sigma;<sub>t</sub>{math_var('F', 'o,t', 'k')} = {math_var('N', 'o', 'k')}"
            diagram.text("mass_formula", formula, (72, 50, 155, 34), cell_id, 19, False, INK, "left")


def _channel_choice(diagram: Diagram) -> None:
    diagram.box("channel_choice", "", (650, 82, 270, 500),
                "market_panel", GRAY_FILL, GRAY)
    diagram.text("choice_title", "Within-period channel choice",
                 (12, 8, 246, 46), "channel_choice", 21, True)
    choices = (
        ("choice_direct_a", "Direct Provider A", "svg/market_actors/direct_user.svg", 78, GREEN_FILL, GREEN),
        ("choice_intermediary", "API intermediary", "svg/api_routing/server_sharing.svg", 215, CYAN_FILL, CYAN),
        ("choice_direct_b", "Direct Provider B", "svg/market_actors/direct_user.svg", 352, YELLOW_FILL, YELLOW),
    )
    for cell_id, label, icon, y, fill, stroke in choices:
        diagram.box(cell_id, "", (22, y, 226, 92), "channel_choice", fill, stroke)
        diagram.icon(f"{cell_id}_icon", icon, (10, 17, 54, 54), cell_id)
        diagram.text(f"{cell_id}_label", label, (70, 18, 146, 50), cell_id,
                     18, True, stroke, "left")


def _intermediary(diagram: Diagram) -> None:
    diagram.box("intermediary", "", (965, 235, 270, 190),
                "market_panel", CYAN_FILL, CYAN)
    diagram.text("intermediary_title", "API intermediary", (20, 10, 230, 36),
                 "intermediary", 21, True, CYAN)
    diagram.icon("intermediary_server", "svg/api_routing/server_sharing.svg",
                 (35, 58, 62, 62), "intermediary")
    diagram.icon("intermediary_route", "svg/api_routing/flow_split.svg",
                 (172, 60, 58, 58), "intermediary")
    diagram.text("intermediary_formula",
                 f"{math_var('r', 'm,t')} = R({math_var('w', 'm,t')}, {math_var('q', 'm,t')})",
                 (20, 126, 230, 30), "intermediary", 19)
    diagram.text("intermediary_note", "Retail price and QoS-aware routing",
                 (15, 160, 240, 20), "intermediary", 18)


def _provider(diagram: Diagram, suffix: str, y: int, fill: str, stroke: str,
              icon: str, title: str) -> None:
    cell_id = f"provider_{suffix.lower()}"
    diagram.box(cell_id, "", (1300, y, 510, 220), "market_panel", fill, stroke)
    diagram.text(f"{cell_id}_title", title, (20, 6, 470, 36), cell_id, 21, True, stroke)
    diagram.text(f"{cell_id}_prices",
                 f"{math_var('w', f'{suffix},t')} ; {math_var('p', f'{suffix},t', 'D')}",
                 (35, 45, 440, 28), cell_id, 19)
    diagram.icon(f"{cell_id}_compute", icon, (55, 82, 68, 68), cell_id)
    diagram.icon(f"{cell_id}_util", "svg/gpu_capacity_qos/utilization_gauge.svg",
                 (220, 82, 68, 68), cell_id)
    diagram.icon(f"{cell_id}_qos", "svg/gpu_capacity_qos/sla_passed.svg",
                 (385, 82, 68, 68), cell_id)
    diagram.text(f"{cell_id}_capacity", f"{math_var('G', suffix)} fixed",
                 (25, 158, 130, 34), cell_id, 18, True)
    diagram.text(f"{cell_id}_util_label",
                 f"{math_var('u', f'{suffix},t')}={math_var('L', f'{suffix},t')}/{math_var('G', suffix)}",
                 (165, 158, 170, 34), cell_id, 19)
    diagram.text(f"{cell_id}_qos_label",
                 f"{math_var('q', f'{suffix},t')}={math_var('Q')}({math_var('u', f'{suffix},t')})",
                 (340, 158, 145, 34), cell_id, 19)
    diagram.edge(f"{cell_id}_load", f"{cell_id}_compute", f"{cell_id}_util", cell_id)
    diagram.edge(f"{cell_id}_quality", f"{cell_id}_util", f"{cell_id}_qos", cell_id)


def _market_edges(diagram: Diagram) -> None:
    diagram.edge("rigid_to_temporal", "rigid_users", "temporal_allocation", "market_panel",
                 anchors="exitX=1;exitY=0.5;entryX=0;entryY=0.217;")
    diagram.edge("flexible_to_temporal", "flexible_users", "temporal_allocation", "market_panel",
                 anchors="exitX=1;exitY=0.5;entryX=0;entryY=0.781;")
    diagram.edge("temporal_to_choice", "temporal_allocation", "channel_choice", "market_panel")
    diagram.edge("choice_to_intermediary", "choice_intermediary", "intermediary", "market_panel",
                 anchors="exitX=1;exitY=0.5;entryX=0;entryY=0.568;")
    diagram.edge("choice_to_a", "choice_direct_a", "provider_a", "market_panel",
                 math_var("D", "A,t", "D"), anchors="exitX=1;exitY=0.5;entryX=0;entryY=0.582;",
                 size=18)
    diagram.edge("choice_to_b", "choice_direct_b", "provider_b", "market_panel",
                 math_var("D", "B,t", "D"), anchors="exitX=1;exitY=0.5;entryX=0;entryY=0.536;",
                 size=18)
    diagram.edge("route_to_a", "intermediary", "provider_a", "market_panel",
                 f"{math_var('r', 'A,t')}{math_var('D', 't', 'I')}", color=CYAN,
                 anchors="exitX=1;exitY=0.083;entryX=0;entryY=0.782;", size=18)
    diagram.edge("route_to_b", "intermediary", "provider_b", "market_panel",
                 f"{math_var('r', 'B,t')}{math_var('D', 't', 'I')}", color=CYAN,
                 anchors="exitX=1;exitY=0.863;entryX=0;entryY=0.169;", size=18)
    diagram.edge("provider_signal_a", "provider_a", "intermediary", "market_panel",
                 "Price / QoS", True, color=GREEN,
                 anchors="exitX=0;exitY=0.94;entryX=1;entryY=0.272;", size=18)
    diagram.edge("provider_signal_b", "provider_b", "intermediary", "market_panel",
                 "Price / QoS", True, color=YELLOW,
                 anchors="exitX=0;exitY=0.27;entryX=1;entryY=0.981;", size=18)
    diagram.edge("provider_competition", "provider_a", "provider_b", "market_panel",
                 "Bounded price-rule competition", True, True, CORAL,
                 anchors="exitX=0.88;exitY=1;entryX=0.88;entryY=0;", size=18)


def _solver_panel(diagram: Diagram) -> None:
    diagram.vertex("solver_panel", "", PANEL, (20, 700, 1860, 430))
    diagram.text("solver_title", "(b) Numerically audited simulation and finite-game solution",
                 (420, 4, 1020, 45), "solver_panel", 27, True)
    nodes = (
        ("step_inputs", "BurstGPT load shape<br>Measured QoS fit", "svg/simulation_evidence/time_series_results.svg", CYAN_FILL, CYAN, 20),
        ("step_prices", "Audit-adaptive bounded linear<br>provider-price candidates", "svg/pricing_time/dynamic_price.svg", YELLOW_FILL, YELLOW, 220),
        ("step_demand", "Conserved OD flow<br>Channel choice", "svg/api_routing/network_users.svg", GREEN_FILL, GREEN, 420),
        ("step_fixed_point", "Joint routing-QoS<br>fixed point", "svg/api_routing/bidirectional_transfer.svg", YELLOW_FILL, YELLOW, 620),
        ("step_payoffs", "Bounded continuous<br>intermediary response", "svg/simulation_evidence/optimization_result.svg", CORAL_FILL, CORAL, 820),
        ("step_nash", "Complementarity mixed equilibrium", "svg/simulation_evidence/iterative_solver.svg", GRAY_FILL, GRAY, 1020),
        ("step_deviation", "Full 1,576-candidate regret<br>Bounded off-grid search", "svg/simulation_evidence/time_series_results.svg", CYAN_FILL, CYAN, 1220),
    )
    for cell_id, label, icon, fill, stroke, x in nodes:
        diagram.box(cell_id, "", (x, 82, 175, 220), "solver_panel", fill, stroke)
        diagram.icon(f"{cell_id}_icon", icon, (52, 28, 70, 70), cell_id)
        diagram.text(f"{cell_id}_label", label, (8, 112, 159, 82), cell_id,
                     19, True, stroke)
    for index in range(len(nodes) - 1):
        diagram.edge(f"solver_edge_{index}", nodes[index][0], nodes[index + 1][0],
                     "solver_panel", anchors="exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    diagram.edge("solver_feedback", "step_fixed_point", "step_demand", "solver_panel",
                 "QoS-dependent demand", True, color=CYAN,
                 points=((708, 355), (508, 355)),
                 anchors="exitX=0.5;exitY=1;entryX=0.5;entryY=1;", orthogonal=True,
                 size=18)
    _evidence(diagram)


def _evidence(diagram: Diagram) -> None:
    diagram.box("evidence_block", "", (1420, 70, 410, 320), "solver_panel", WHITE, INK)
    diagram.text("evidence_title", "Evidence reported", (20, 8, 370, 38),
                 "evidence_block", 21, True)
    items = (
        ("evidence_peak", "Aggregate peak", "temporal load shifting", "svg/simulation_evidence/time_series_results.svg", CYAN),
        ("evidence_qos", "Provider hotspot and QoS", "spatial provider substitution", "svg/gpu_capacity_qos/sla_passed.svg", GREEN),
        ("evidence_profit", "Profit boundary", "market-side accounting", "svg/simulation_evidence/market_share_results.svg", CORAL),
    )
    for index, (cell_id, title, note, icon, color) in enumerate(items):
        y = 55 + index * 83
        diagram.icon(f"{cell_id}_icon", icon, (25, y, 55, 55), "evidence_block")
        diagram.text(cell_id, f"<b>{title}</b><br>{note}", (90, y, 290, 60),
                     "evidence_block", 19, False, color, "left")
    diagram.edge("solver_to_evidence", "step_deviation", "evidence_block", "solver_panel",
                 anchors="exitX=1;exitY=0.5;entryX=0;entryY=0.381;")


def build() -> None:
    diagram = FinalDiagram()
    diagram.vertex("market_panel", "", PANEL, (20, 20, 1860, 650))
    diagram.text("market_title", "(a) Conserved-demand market and serving mechanism",
                 (430, 4, 870, 44), "market_panel", 27, True)
    diagram.text("capacity_order", f"{math_var('G', 'A')} &gt; {math_var('G', 'B')}",
                 (1470, 8, 170, 32), "market_panel", 18, True, GRAY)
    _user(diagram, "rigid_users", 88, "Time-rigid requests",
          "Native period retained<br>Flexible fraction = 0", CYAN_FILL, CYAN,
          ("svg/market_actors/user_population.svg", "svg/iot_endpoints/network_camera.svg", "svg/pricing_time/runtime.svg"))
    _user(diagram, "flexible_users", 370, "Time-flexible requests",
          "Shift within a time window<br>Positive migration cost", GREEN_FILL, GREEN,
          ("svg/market_actors/user_population.svg", "svg/iot_endpoints/laptop.svg", "svg/iot_endpoints/smart_home_endpoint.svg"))
    _temporal_allocation(diagram)
    _channel_choice(diagram)
    _intermediary(diagram)
    _provider(diagram, "A", 78, GREEN_FILL, GREEN,
              "svg/gpu_capacity_qos/high_capacity_provider.svg", "Provider A: higher fixed capacity")
    _provider(diagram, "B", 362, YELLOW_FILL, YELLOW,
              "svg/api_routing/server_sharing.svg", "Provider B: lower fixed capacity")
    _market_edges(diagram)
    _solver_panel(diagram)
    diagram.save()
    print(OUTPUT)


if __name__ == "__main__":
    build()
