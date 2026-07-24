"""Step 4 — Harvest / Clarification.

No product-quality impact in the A-Mab case study (p.85-86): the step clarifies
the broth and defines the feed to Protein A. Modelled as a product-yield loss;
CQAs pass through unchanged. Viral-clearance counters are initialised here.
"""

from __future__ import annotations

from typing import Dict, Optional

import numpy as np

from ..core import Stream, StepResult, lognormal_noise
from .base import BaseUnitOp


class Harvest(BaseUnitOp):
    key = "harvest"

    def run(self, inp: Stream, rng: np.random.Generator,
            setpoints: Optional[Dict[str, float]] = None) -> StepResult:
        sp = self.setpoints(setpoints)
        y = self.uo.raw["yield"]
        step_yield = y["base"] * lognormal_noise(rng, y["cv"])
        out = inp.copy()
        out.product_mass_g = inp.product_mass_g * step_yield
        # initialise cumulative viral log-reduction counters
        out.cqas.setdefault("lrv_xmulv", 0.0)
        out.cqas.setdefault("lrv_mvm", 0.0)
        out.cqas.setdefault("leached_protein_a", 0.0)
        return StepResult(step=self.name, step_yield=step_yield, inp=inp, out=out,
                          params=sp, metrics={"turbidity_ntu": sp.get("turbidity", 5.0)})
