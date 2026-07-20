"""Shared publication plotting style for peak-shaving figures."""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
from matplotlib import font_manager
import numpy as np

SCI_PALETTE = {
    "primary": "#3C5488",
    "secondary": "#6F83B5",
    "contrast": "#A86464",
    "neutral": "#7A7A7A",
    "light": "#B8C4D9",
}

TIMES_FONT_FILES = (
    Path("/mnt/c/Windows/Fonts/times.ttf"),
    Path("/mnt/c/Windows/Fonts/timesbd.ttf"),
    Path("/mnt/c/Windows/Fonts/timesi.ttf"),
    Path("/mnt/c/Windows/Fonts/timesbi.ttf"),
)


def configure_times_new_roman(font_size: float = 9.0) -> None:
    for font_path in TIMES_FONT_FILES:
        if font_path.exists():
            font_manager.fontManager.addfont(str(font_path))
    mpl.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman"],
        "font.size": font_size,
        "mathtext.fontset": "stix",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": False,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.04,
    })


def plot_end_user_prices(ax, periods, uniform: dict, dynamic: dict) -> None:
    colors = SCI_PALETTE
    direct_uniform = np.mean(np.asarray(uniform["direct_price"]), axis=0)
    ax.plot(periods, uniform["retail_price"], "--", color=colors["neutral"],
            label="Intermediary, uniform")
    ax.plot(periods, direct_uniform, ":", color=colors["neutral"],
            label="Direct, uniform")
    ax.plot(periods, dynamic["retail_price"], "-", color=colors["primary"],
            label="Intermediary, dynamic")
    ax.plot(periods, dynamic["direct_price"][0], "-", color=colors["secondary"],
            label="Direct A, dynamic")
    ax.plot(periods, dynamic["direct_price"][1], "-", color=colors["contrast"],
            label="Direct B, dynamic")
    ax.set(xlabel="Period", ylabel="Normalized end-user price")
    ax.legend(frameon=False, fontsize=6.2, loc="lower center",
              bbox_to_anchor=(0.5, 1.01), ncol=2)
    ax.grid(alpha=0.18)
