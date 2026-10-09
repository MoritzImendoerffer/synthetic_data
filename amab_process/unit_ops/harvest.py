"""Step 4 — Harvest / Clarification.

No product-quality impact in the A-Mab case study (p.85-86): the step clarifies
the broth and defines the feed to Protein A. Modelled as a product-yield loss;
CQAs pass through unchanged. Viral-clearance counters are initialised here.

Version 2.0 adds clarification performance (``process.harvest.model``) for the univariate study
S-HAR-UNI: centrate turbidity against centrifuge rcf, and clarified turbidity against depth filter
load. Both are metrics, not attributes, and draw nothing from ``rng``, so no stream moves.
"""

from __future__ import annotations

from typing import Dict, Optional

import numpy as np

from ..core import Stream, StepResult, lognormal_noise
from .base import BaseUnitOp


class Harvest(BaseUnitOp):
    key = "harvest"

    def turbidity(self, sp: Dict[str, float]) -> Dict[str, float]:
        """Centrate and clarified turbidity (NTU) at an operating point."""
        m = self.uo.raw["model"]
        c, f = m["centrate_turbidity"], m["clarified_turbidity"]

        def centrate(rcf):
            return c["floor_ntu"] + c["excess_ntu"] * np.exp(-(rcf - c["rcf_ref_g"]) / c["rcf_scale_g"])

        cen = centrate(sp["centrifuge_g"])
        ref = centrate(float(self.uo.param("centrifuge_g").setpoint_characterized))
        cla = (f["base_ntu"] * (cen / ref) ** f["feed_exponent"]
               + f["knee_ntu"] * np.exp((sp["depth_filter_load"] - f["capacity_l_m2"]) / f["width_l_m2"]))
        return {"centrate_turbidity_ntu": float(cen), "clarified_turbidity_ntu": float(cla)}

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
                          params=sp, metrics={"turbidity_ntu": sp.get("turbidity", 5.0),
                                              **self.turbidity(sp)})
