"""Step 7 — Cation Exchange Chromatography (bind-elute).

Main aggregate-polishing step (2-3x reduction) and HCP reduction (50-100x). Both
clearances weaken at higher protein load; HCP clearance also weakens at lower
load/wash conductivity (A-Mab DOE, Fig 4.5). Also clears DNA and leached Protein A.
Charge/glycan variants are not discriminated. (p.134-140)
"""

from __future__ import annotations

from typing import Dict, Optional

import numpy as np

from ..core import Stream, StepResult, clip, lognormal_noise
from .base import BaseUnitOp


class CEX(BaseUnitOp):
    key = "cex"

    def run(self, inp: Stream, rng: np.random.Generator,
            setpoints: Optional[Dict[str, float]] = None) -> StepResult:
        sp = self.setpoints(setpoints)
        c = self.coded(sp)
        m = self.uo.model

        # aggregate clearance (fold) — weakens with load, elution pH, stop-collect
        agg_fold = m["agg_clearance_base"] * (1 + m["agg_load_coef"] * c.get("load", 0)
                                              + m["agg_ph_coef"] * c.get("elution_ph", 0)
                                              + m["agg_stopcollect_coef"] * c.get("stop_collect", 0))
        agg_fold = max(agg_fold, 1.05) * lognormal_noise(rng, m["agg_cv"])

        # HCP clearance (fold) — weakens with load, strengthens with wash conductivity
        hcp_fold = m["hcp_clearance_base"] * np.exp(m["hcp_load_coef"] * c.get("load", 0)
                                                    + m["hcp_wash_cond_coef"] * c.get("wash_cond", 0))
        hcp_fold = max(hcp_fold, 1.5) * lognormal_noise(rng, m["hcp_cv"])

        step_yield = clip((m["yield_base"] + m["yield_load_coef"] * c.get("load", 0))
                          * lognormal_noise(rng, m["yield_cv"]), 0.6, 0.99)

        out = inp.copy()
        out.product_mass_g = inp.product_mass_g * step_yield
        out.cqas["aggregates_hmw"] = clip(inp.cqas.get("aggregates_hmw", 0.0) / agg_fold, 0.0)
        out.cqas["hcp"] = clip(inp.cqas.get("hcp", 0.0) / hcp_fold, 0.5)
        out.cqas["residual_dna"] = inp.cqas.get("residual_dna", 0.0) / (10 ** m["dna_lrv"])
        out.cqas["leached_protein_a"] = inp.cqas.get("leached_protein_a", 0.0) / (10 ** m["leached_pa_lrv"])
        return StepResult(step=self.name, step_yield=step_yield, inp=inp, out=out, params=sp,
                          metrics={"aggregate_clearance_fold": agg_fold,
                                   "hcp_clearance_fold": hcp_fold,
                                   "aggregate_out_pct": out.cqas["aggregates_hmw"],
                                   "hcp_out_ng_mg": out.cqas["hcp"]})
