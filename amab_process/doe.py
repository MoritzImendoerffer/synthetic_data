"""Design-of-experiments helpers for scale-down characterization studies.

Provides coded designs used by the characterization scripts:

* :func:`full_factorial` / :func:`two_level_fractional` — screening designs.
* :func:`central_composite` — face-centred CCD for response-surface / design-space
  studies (matches the A-Mab case-study approach: screening 2-level
  design -> face-centred CCD).
* :func:`decode` — map a coded design back to natural parameter units.

All designs are returned as ``pandas.DataFrame`` of coded factors in {-1, 0, +1}
(CCD uses +-1 axial points because the design is *face-centred*, alpha = 1).
"""

from __future__ import annotations

import itertools
from typing import Dict, List, Sequence

import numpy as np
import pandas as pd


def full_factorial(factors: Sequence[str], center_points: int = 3) -> pd.DataFrame:
    """Full two-level factorial with replicated centre points."""
    rows = [dict(zip(factors, combo)) for combo in itertools.product([-1, 1], repeat=len(factors))]
    df = pd.DataFrame(rows)
    for _ in range(center_points):
        df = pd.concat([df, pd.DataFrame([{f: 0 for f in factors}])], ignore_index=True)
    df.insert(0, "run_type", ["factorial"] * (len(df) - center_points) + ["center"] * center_points)
    return df


def two_level_fractional(factors: Sequence[str], generators: Dict[str, Sequence[str]],
                         base_factors: Sequence[str], center_points: int = 3) -> pd.DataFrame:
    """Two-level fractional factorial.

    ``base_factors`` span the full 2^k base design; each extra factor in
    ``generators`` is aliased to a product of base factors (e.g. ``E = A*B*C``
    for a resolution-V 2^(5-1)). This reproduces the A-Mab screening designs.
    """
    base = list(base_factors)
    rows = []
    for combo in itertools.product([-1, 1], repeat=len(base)):
        row = dict(zip(base, combo))
        for extra, gen in generators.items():
            v = 1
            for g in gen:
                v *= row[g]
            row[extra] = v
        rows.append(row)
    df = pd.DataFrame(rows)[list(factors)]
    for _ in range(center_points):
        df = pd.concat([df, pd.DataFrame([{f: 0 for f in factors}])], ignore_index=True)
    df.insert(0, "run_type", ["factorial"] * (len(df) - center_points) + ["center"] * center_points)
    return df


def central_composite(factors: Sequence[str], center_points: int = 3,
                      face_centered: bool = True) -> pd.DataFrame:
    """(Face-centred) central-composite design.

    Cube (2^k factorial) + 2k axial points + centre replicates. ``face_centered``
    keeps axial points on the cube faces (alpha = 1) so all runs stay within the
    characterized range — the approach used in the A-Mab response-surface studies.
    """
    factors = list(factors)
    k = len(factors)
    alpha = 1.0 if face_centered else float(k) ** 0.25
    rows, kinds = [], []
    for combo in itertools.product([-1, 1], repeat=k):
        rows.append(dict(zip(factors, combo)))
        kinds.append("factorial")
    for i, f in enumerate(factors):
        for s in (-alpha, alpha):
            r = {ff: 0.0 for ff in factors}
            r[f] = s
            rows.append(r)
            kinds.append("axial")
    for _ in range(center_points):
        rows.append({f: 0.0 for f in factors})
        kinds.append("center")
    df = pd.DataFrame(rows)
    df.insert(0, "run_type", kinds)
    return df


def decode(design: pd.DataFrame, ranges: Dict[str, Sequence[float]]) -> pd.DataFrame:
    """Map a coded design to natural units given per-factor [lo, hi] edges."""
    out = design.copy()
    for f, (lo, hi) in ranges.items():
        if f in out.columns:
            mid = 0.5 * (lo + hi)
            half = 0.5 * (hi - lo)
            out[f] = mid + out[f] * half
    return out
