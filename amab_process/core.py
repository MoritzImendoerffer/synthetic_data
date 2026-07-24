"""Core abstractions for the A-Mab drug-substance process model.

The model is a *semi-mechanistic hybrid*: the production bioreactor is described
by ODE growth/production kinetics, while the downstream unit operations use
mechanistic mass balances (yields, log-reduction values) combined with
response-surface models that map process parameters to critical quality
attributes (CQAs). Everything is driven by a single seeded RNG so that every
number and figure in the report is reproducible.

Design notes
------------
* A :class:`Stream` is the material transferred between unit operations. It
  carries an amount of product (mass of monomeric A-Mab), a volume, and a
  dictionary of quality attributes expressed in their native units
  (percentages for size/charge/glycan variants, ppm or ng/mg for impurities,
  LRV budget for viral safety).
* A :class:`UnitOperation` consumes an input :class:`Stream` plus a dict of
  process parameters and returns an output :class:`Stream` together with a
  :class:`StepResult` capturing yields, CQA changes and any derived metrics.
* Response-surface helpers (:func:`rsm`) live here so every unit operation uses
  the same coded-factor convention.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Callable, Dict, Mapping, Optional

import numpy as np

# --------------------------------------------------------------------------- #
# Quality-attribute registry
# --------------------------------------------------------------------------- #
# Canonical CQA keys used throughout the model. Units are documented so the
# report and the risk assessment stay consistent with the model output.
CQA_UNITS: Dict[str, str] = {
    "afucosylation": "% of glycans",
    "galactosylation": "% (G1+G2)",
    "high_mannose": "% of glycans",
    "aggregates_hmw": "% HMW (SEC)",
    "fragments_lmw": "% LMW (SEC)",
    "acidic_variants": "% (CEX/icIEF)",
    "basic_variants": "% (CEX/icIEF)",
    "main_charge": "% main peak",
    "hcp": "ng/mg",
    "residual_dna": "ng/dose",
    "leached_protein_a": "ppm",
    "lrv_xmulv": "log10 (cumulative)",
    "lrv_mvm": "log10 (cumulative)",
}


@dataclass
class Stream:
    """Process material transferred between unit operations.

    Attributes
    ----------
    product_mass_g:
        Mass of monomeric A-Mab (g).
    volume_l:
        Batch volume (L).
    cqas:
        Mapping of CQA key -> value in its native unit (see :data:`CQA_UNITS`).
    meta:
        Free-form annotations (e.g. VCD, viability at harvest).
    """

    product_mass_g: float
    volume_l: float
    cqas: Dict[str, float] = field(default_factory=dict)
    meta: Dict[str, float] = field(default_factory=dict)

    @property
    def titer_g_per_l(self) -> float:
        return self.product_mass_g / self.volume_l if self.volume_l else float("nan")

    def copy(self) -> "Stream":
        return replace(self, cqas=dict(self.cqas), meta=dict(self.meta))


@dataclass
class StepResult:
    """Outcome of a single unit-operation run."""

    step: str
    step_yield: float                    # fraction of product recovered (0-1)
    inp: Stream
    out: Stream
    params: Dict[str, float] = field(default_factory=dict)
    metrics: Dict[str, float] = field(default_factory=dict)

    @property
    def cumulative_note(self) -> str:
        return f"{self.step}: yield={self.step_yield:.3f}"


class UnitOperation:
    """Base class for every drug-substance unit operation.

    Subclasses set :attr:`name` and implement :meth:`run`. Parameter defaults
    (set-points) and characterization ranges are supplied from configuration so
    the modelling code stays free of hard-coded numbers.
    """

    name: str = "unit-operation"

    def __init__(self, params: Optional[Mapping[str, float]] = None):
        self.params: Dict[str, float] = dict(params or {})

    def with_params(self, **overrides: float) -> "UnitOperation":
        p = dict(self.params)
        p.update(overrides)
        return self.__class__(p)

    def run(self, inp: Stream, rng: np.random.Generator) -> StepResult:  # pragma: no cover - abstract
        raise NotImplementedError


# --------------------------------------------------------------------------- #
# Response-surface helpers
# --------------------------------------------------------------------------- #
def code(x: float, lo: float, hi: float) -> float:
    """Map a natural parameter value to a coded factor in [-1, +1].

    ``lo`` and ``hi`` are the low/high edges of the characterization range, so
    the set-point (centre) maps near 0 and the PAR edges map to +-1.
    """

    mid = 0.5 * (lo + hi)
    half = 0.5 * (hi - lo)
    if half == 0:
        return 0.0
    return (x - mid) / half


def rsm(
    intercept: float,
    linear: Mapping[str, float],
    coded: Mapping[str, float],
    quadratic: Optional[Mapping[str, float]] = None,
    interactions: Optional[Mapping[tuple, float]] = None,
) -> float:
    """Evaluate a second-order response-surface model on coded factors.

    Parameters
    ----------
    intercept:
        Response at the centre point (all coded factors = 0).
    linear:
        Main-effect coefficients keyed by factor name.
    coded:
        Coded factor values (typically in [-1, 1], but extrapolation allowed).
    quadratic:
        Optional pure-quadratic coefficients keyed by factor name.
    interactions:
        Optional two-factor interaction coefficients keyed by ``(a, b)`` tuple.
    """

    y = float(intercept)
    for k, b in linear.items():
        y += b * coded.get(k, 0.0)
    if quadratic:
        for k, b in quadratic.items():
            y += b * coded.get(k, 0.0) ** 2
    if interactions:
        for (a, b_), c in interactions.items():
            y += c * coded.get(a, 0.0) * coded.get(b_, 0.0)
    return y


def clip(value: float, lo: float = 0.0, hi: Optional[float] = None) -> float:
    """Clip a value to physically meaningful bounds."""

    if value < lo:
        value = lo
    if hi is not None and value > hi:
        value = hi
    return value


def lognormal_noise(rng: np.random.Generator, cv: float) -> float:
    """Multiplicative lognormal noise with the given coefficient of variation."""

    if cv <= 0:
        return 1.0
    sigma = np.sqrt(np.log(1.0 + cv * cv))
    return float(np.exp(rng.normal(-0.5 * sigma * sigma, sigma)))
