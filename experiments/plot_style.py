"""Shared publication plotting style for peak-shaving figures."""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
from matplotlib import font_manager

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

