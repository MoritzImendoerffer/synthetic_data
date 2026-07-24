"""Shared plotting style for the process characterization report.

Uses the validated dataviz reference palette (light mode; the report is print).
Categorical hues are assigned in fixed order and never cycled; specification
limits use the reserved ``critical`` status colour; NOR bands use a recessive
blue wash; set-points a neutral ink line. Figures are saved at 200 dpi.
"""

from __future__ import annotations

from typing import Optional, Sequence

import matplotlib as mpl
import matplotlib.pyplot as plt

# --- reference palette (light) ------------------------------------------------
CATEGORICAL = ["#2a78d6", "#008300", "#e87ba4", "#eda100",
               "#1baf7a", "#eb6834", "#4a3aa7", "#e34948"]
SEQUENTIAL = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
STATUS = {"good": "#0ca30c", "warning": "#fab219", "serious": "#ec835a", "critical": "#d03b3b"}

INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
SURFACE = "#fcfcfb"
NOR_WASH = "#cde2fb"
SPEC = STATUS["critical"]
SETPOINT = INK


def apply_style() -> None:
    mpl.rcParams.update({
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Arial", "Liberation Sans"],
        "font.size": 10,
        "axes.edgecolor": "#c3c2b7",
        "axes.labelcolor": INK,
        "axes.titlecolor": INK,
        "axes.titlesize": 11,
        "axes.titleweight": "bold",
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": GRID,
        "grid.linewidth": 0.8,
        "xtick.color": INK2,
        "ytick.color": INK2,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
        "figure.dpi": 120,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
    })


def spec_lines(ax, low: Optional[float] = None, high: Optional[float] = None,
               label: str = "Acceptance limit") -> None:
    """Draw acceptance/specification limits as dashed critical-red lines."""
    done = False
    for y in (low, high):
        if y is not None:
            ax.axhline(y, color=SPEC, ls="--", lw=1.4,
                       label=(label if not done else None))
            done = True


def nor_band(ax, lo: float, hi: float, setpoint: Optional[float] = None,
             vertical: bool = False, label: str = "NOR") -> None:
    """Shade the normal operating range and mark the set-point."""
    if vertical:
        ax.axvspan(lo, hi, color=NOR_WASH, alpha=0.55, lw=0, label=label)
        if setpoint is not None:
            ax.axvline(setpoint, color=SETPOINT, lw=1.2, ls=":", label="Set-point")
    else:
        ax.axhspan(lo, hi, color=NOR_WASH, alpha=0.55, lw=0, label=label)
        if setpoint is not None:
            ax.axhline(setpoint, color=SETPOINT, lw=1.2, ls=":", label="Set-point")


def savefig(fig, path: str) -> str:
    fig.savefig(path)
    plt.close(fig)
    return path
