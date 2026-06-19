"""Clean black-and-white block diagrams for publication.

Figure 2: Information interaction between stakeholders.
Figure 3: API market topology with direct channel.
"""

from __future__ import annotations
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

mpl.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix", "font.size": 10,
    "svg.fonttype": "none", "pdf.fonttype": 42,
    "figure.dpi": 200, "savefig.bbox": "tight", "savefig.pad_inches": 0.05,
})

C = {
    "bg":    (1, 1, 1),
    "box":   (0.95, 0.95, 0.97),
    "title": (0, 0, 0),
    "sub":   (0.3, 0.3, 0.3),
    "line":  (0.35, 0.35, 0.35),
    "arrow": (0.25, 0.25, 0.25),
    "dash":  (0.45, 0.45, 0.45),
    "sep":   (0.75, 0.75, 0.75),
    "num":   (0.5, 0.5, 0.5),
}


def block(ax, x, y, w, h, title, lines, bold=True, dashed=False, lw=1.0, r=0.06):
    ls = "--" if dashed else "-"
    ec = C["dash"] if dashed else C["line"]
    b = FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle=f"round,pad=0.02,rounding_size={r*min(w,h):.1f}",
                       facecolor=C["box"], edgecolor=ec, linewidth=lw, linestyle=ls, zorder=2)
    ax.add_patch(b)
    weight = "bold" if bold else "normal"
    ax.text(x, y + h/2 - 0.08, title, ha="center", va="top", fontsize=9.5,
            color=C["title"], weight=weight, zorder=3)
    for i, ln in enumerate(lines):
        ax.text(x, y + h/2 - 0.22 - i*0.09, ln, ha="center", va="top", fontsize=8,
                color=C["sub"], zorder=3)


def arrow(ax, x1, y1, x2, y2, dashed=False, lw=0.8):
    ls = (0, (4, 3)) if dashed else "solid"
    c = C["dash"] if dashed else C["arrow"]
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>,head_length=5,head_width=4",
                        color=c, linewidth=lw, linestyle=ls, zorder=1,
                        connectionstyle="arc3,rad=0")
    ax.add_patch(a)


def arrow_up(ax, x1, y1, x2, y2, dashed=False, lw=0.8):
    """Arrow going upward then right (for feedback loops)."""
    ls = (0, (4, 3)) if dashed else "solid"
    c = C["dash"] if dashed else C["arrow"]
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>,head_length=5,head_width=4",
                        color=c, linewidth=lw, linestyle=ls, zorder=1,
                        connectionstyle="arc3,rad=0.3")
    ax.add_patch(a)


def draw_info_interaction(out: Path) -> Path:
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.set_xlim(0, 7.5); ax.set_ylim(0, 4.2); ax.axis("off")

    w, h = 2.05, 1.15   # block size
    mx = 0.5             # margin
    gap = 0.18
    x0, x1, x2 = mx + w/2 + 0.00, mx + w*1.5 + gap + 0.00, mx + w*2.5 + gap*2 + 0.00
    y_top, y_bot = 3.15, 1.30

    # Row 1
    block(ax, x0, y_top, w, h, "Exogenous API Supply",
          ["token capacity, API cost,", "reliability inputs"], dashed=True)
    block(ax, x1, y_top, w, h, "Stage 1: Platform",
          ["wholesale price $w_t$;", "anticipates responses"])
    block(ax, x2, y_top, w, h, "Stage 2: API Brokers",
          ["retail price $p_{jt}$,", "allocate capacity $g_{jt}$"])

    # Row 2
    block(ax, x0, y_bot, w, h, "Objective Diagnostics",
          ["platform / broker / system payoff;", "user inclusive value"], dashed=True)
    block(ax, x1, y_bot, w, h, "QoS Monitor",
          ["$u_{jt},\\, q_{jt}$; served demand", "$D_{jt}\\,q_{jt}$"])
    block(ax, x2, y_bot, w, h, "Stage 3: Users",
          ["broker $\\times$ period choice;", "cross-period migration"])

    # Arrows
    ax_off = w/2 + 0.02
    arrow(ax, x0+ax_off, y_top, x1-ax_off, y_top)
    arrow(ax, x1+ax_off, y_top, x2-ax_off, y_top)
    arrow(ax, x2, y_top-h/2-0.02, x2, y_bot+h/2+0.02)
    arrow(ax, x2-ax_off, y_bot, x1+ax_off, y_bot)
    arrow(ax, x1-ax_off, y_bot, x0+ax_off, y_bot)
    # Feedback
    arrow_up(ax, x0, y_bot+h/2+0.02, x1, y_top-h/2-0.02, dashed=True)
    ax.text(0.82, 2.18, "feedback", fontsize=7.5, color=C["dash"], style="italic")

    # Labels
    positions = [
        (x0, y_top+h/2+0.25, "Exogenous Input", 8.5),
        (x1, y_top+h/2+0.25, "Upper Layer (Platform)", 8.5),
        (x2, y_top+h/2+0.25, "Middle Layer (Brokers)", 8.5),
        (x2, y_bot+h/2+0.25, "Lower Layer (Users)", 8.5),
        (x1, y_bot+h/2+0.25, "QoS & Diagnostics", 8.5),
    ]
    for px, py, label, fs in positions:
        ax.text(px, py, label, ha="center", va="bottom", fontsize=fs,
                color=C["num"], weight="bold")

    path = out / "information_interaction"
    fig.savefig(f"{path}.pdf"); fig.savefig(f"{path}.svg"); fig.savefig(f"{path}.png", dpi=300)
    plt.close()
    return path.with_suffix(".pdf")


def draw_api_topology(out: Path) -> Path:
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    ax.set_xlim(0, 7.2); ax.set_ylim(0, 5.0); ax.axis("off")

    # Top: supply
    block(ax, 3.6, 4.55, 4.8, 0.75, "Exogenous Model API Supply",
          ["DeepSeek / Claude / GPT / Gemini, Qwen and other API inputs"],
          dashed=True, r=0.04)

    # Platform
    block(ax, 3.6, 3.55, 3.8, 0.85, "Platform Wholesale Layer",
          ["sets wholesale price $w_t$; observes settlement and QoS"])

    # Broker + Direct
    bw, bh = 2.6, 1.35
    block(ax, 1.5, 2.15, bw, bh, "Brokered Retail APIs",
          ["Broker 1: $p_{1t},g_{1t}$", "Broker 2: $p_{2t},g_{2t}$",
           "Broker 3: $p_{3t},g_{3t}$"], r=0.05)
    block(ax, 5.7, 2.15, bw, bh, "Direct API Channel",
          ["$j=0$ outside option; $p_t^D,g_t^D$",
           "platform self-operated, SLA reserve"], r=0.05)

    # Users
    block(ax, 3.6, 0.55, 3.6, 0.55, "User Classes & Time Slots",
          ["choose broker / direct channel / shift across periods"], r=0.04)

    # Arrows
    arrow(ax, 3.6, 4.55-0.38, 3.6, 3.55+0.43)           # supply→platform
    arrow(ax, 2.5, 3.55-0.3, 1.5, 2.15+0.68)               # platform→broker
    arrow(ax, 4.7, 3.55-0.3, 5.7, 2.15+0.68)               # platform→direct
    arrow(ax, 1.5, 2.15-0.68, 2.5, 0.55+0.28)              # broker→users
    arrow(ax, 5.7, 2.15-0.68, 4.7, 0.55+0.28)              # direct→users

    # Labels
    ax.text(0.5, 1.85, "Brokered\npath", fontsize=7.5, color=C["num"], ha="center")
    ax.text(6.7, 1.85, "Outside\noption", fontsize=7.5, color=C["num"], ha="center")

    # Section dividers
    for yy, label in [(3.15, "Wholesale Layer"), (2.95, "Retail Layer"), (1.03, "User Layer")]:
        ax.axhline(y=yy, xmin=0.04, xmax=0.96, color=C["sep"], lw=0.4, zorder=0)

    path = out / "api_market_topology"
    fig.savefig(f"{path}.pdf"); fig.savefig(f"{path}.svg"); fig.savefig(f"{path}.png", dpi=300)
    plt.close()
    return path.with_suffix(".pdf")


if __name__ == "__main__":
    out = Path("/root/paper_code/0427_tokenrl/paper_token_cross_survey/figures/reference_aligned")
    draw_info_interaction(out)
    draw_api_topology(out)
    print("Generated black/white diagrams")
