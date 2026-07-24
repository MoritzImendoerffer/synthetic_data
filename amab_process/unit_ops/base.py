"""Shared base for unit-operation models."""

from __future__ import annotations

from typing import Dict, Optional

import numpy as np

from ..config import Config, UnitOpConfig
from ..core import Stream, StepResult, code


class BaseUnitOp:
    """Common machinery: config access + coded-factor computation.

    Subclasses set :attr:`key` and implement :meth:`run`.
    """

    key: str = ""

    def __init__(self, cfg: Config):
        self.cfg: Config = cfg
        self.uo: UnitOpConfig = cfg.unit_op(self.key)

    # -- helpers ---------------------------------------------------------------
    def setpoints(self, overrides: Optional[Dict[str, float]] = None) -> Dict[str, float]:
        """Natural-unit operating point: config set-points updated by overrides."""
        sp = {p.key: float(p.setpoint) for p in self.uo.parameters}
        if overrides:
            sp.update(overrides)
        return sp

    def coded(self, setpoints: Dict[str, float]) -> Dict[str, float]:
        """Map a natural operating point to coded factors in [-1, +1]."""
        out = {}
        for p in self.uo.parameters:
            lo, hi = p.prange
            if p.key in setpoints and hi != lo:
                out[p.key] = code(setpoints[p.key], lo, hi)
        return out

    @property
    def name(self) -> str:
        return self.uo.name

    @property
    def step(self) -> int:
        return self.uo.step

    def run(self, inp: Stream, rng: np.random.Generator,
            setpoints: Optional[Dict[str, float]] = None) -> StepResult:  # pragma: no cover
        raise NotImplementedError
