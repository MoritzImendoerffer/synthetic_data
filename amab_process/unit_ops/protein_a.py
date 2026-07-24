"""Step 5 — Protein A Affinity Chromatography (capture).

Robust capture step: pool HCP is set by the step (largely independent of feed
HCP) and rises with higher protein load and lower elution pH (A-Mab Fig 4.2).
DNA is cleared; leached Protein A is introduced; aggregate passes through; yield
falls at high load x high flow. No viral-clearance claim. (p.113-126)
"""

from __future__ import annotations

from typing import Dict, Optional

import numpy as np

from ..core import Stream, StepResult, clip, lognormal_noise
from .base import BaseUnitOp


class ProteinA(BaseUnitOp):
    key = "protein_a"

    def run(self, inp: Stream, rng: np.random.Generator,
            setpoints: Optional[Dict[str, float]] = None) -> StepResult:
        sp = self.setpoints(setpoints)
        c = self.coded(sp)
        m = self.uo.model

        # HCP pool concentration (ng/mg): robust baseline modulated by load & elution pH
        hcp = m["hcp_base"] * np.exp(m["hcp_load_coef"] * c.get("load", 0)
                                     + m["hcp_ph_coef"] * c.get("elution_ph", 0))
        hcp *= lognormal_noise(rng, m["hcp_cv"])

        # yield: high load x high flow reduces recovery; wider end-collect recovers more
        step_yield = (m["yield_base"]
                      + m["yield_load_flow"] * clip(c.get("load", 0), 0) * clip(c.get("flow", 0), 0)
                      + m["yield_end_collect"] * c.get("end_collect", 0))
        step_yield = clip(step_yield * lognormal_noise(rng, m["yield_cv"]), 0.5, 0.99)

        leached = m["leached_pa_base"] * lognormal_noise(rng, m["leached_pa_cv"])

        out = inp.copy()
        out.product_mass_g = inp.product_mass_g * step_yield
        out.cqas["hcp"] = clip(hcp, 1.0)
        out.cqas["residual_dna"] = inp.cqas.get("residual_dna", 0.0) / (10 ** m["dna_lrv"])
        out.cqas["leached_protein_a"] = leached
        out.cqas["aggregates_hmw"] = inp.cqas.get("aggregates_hmw", 0.0) * m["aggregate_passthrough"]
        out.meta["pool_titer_g_per_l"] = 5.0  # elution pool ~2-6 g/L (p.123)
        return StepResult(step=self.name, step_yield=step_yield, inp=inp, out=out,
                          params=sp, metrics={"pool_hcp_ng_mg": out.cqas["hcp"],
                                              "leached_protein_a_ppm": leached})
