"""Step 8 — Anion Exchange Chromatography (flow-through).

Final polish: removes HCP, DNA, leached Protein A and endotoxin, and provides a
viral-clearance claim (XMuLV, MVM). HCP removal falls as load pH decreases and
Equil/Wash-1 conductivity increases; viral clearance falls as load pH decreases and
load conductivity increases (A-Mab Figs 4.6-4.8). Product passes through in the
flow-through, so yield is high. (p.140-151)
"""

from __future__ import annotations

from typing import Dict, Optional

import numpy as np

from ..core import Stream, StepResult, clip, lognormal_noise
from .base import BaseUnitOp


class AEX(BaseUnitOp):
    key = "aex"

    def run(self, inp: Stream, rng: np.random.Generator,
            setpoints: Optional[Dict[str, float]] = None) -> StepResult:
        sp = self.setpoints(setpoints)
        c = self.coded(sp)
        m = self.uo.model

        # HCP clearance (fold): stronger at higher pH, weaker at higher Eq/Wash-1 conductivity
        hcp_fold = m["hcp_clearance_base"] * np.exp(m["hcp_ph_coef"] * c.get("load_ph", 0)
                                                    + m["hcp_cond_coef"] * c.get("wash1_cond", 0))
        hcp_fold = max(hcp_fold, 1.2) * lognormal_noise(rng, m["hcp_cv"])

        # viral log-reduction: falls as pH drops and conductivity rises
        lrv_xmulv = (m["lrv_xmulv_base"] + m["lrv_ph_coef"] * c.get("load_ph", 0)
                     + m["lrv_cond_coef"] * c.get("load_cond", 0)) * lognormal_noise(rng, m["lrv_cv"])
        lrv_mvm = (m["lrv_mvm_base"] + m["lrv_ph_coef"] * c.get("load_ph", 0)
                   + m["lrv_cond_coef"] * c.get("load_cond", 0)) * lognormal_noise(rng, m["lrv_cv"])

        step_yield = clip(m["yield_base"] * lognormal_noise(rng, m["yield_cv"]), 0.7, 0.995)

        out = inp.copy()
        out.product_mass_g = inp.product_mass_g * step_yield
        out.cqas["hcp"] = clip(inp.cqas.get("hcp", 0.0) / hcp_fold, 0.2)
        out.cqas["residual_dna"] = inp.cqas.get("residual_dna", 0.0) / (10 ** m["dna_lrv"])
        out.cqas["leached_protein_a"] = inp.cqas.get("leached_protein_a", 0.0) / (10 ** m["leached_pa_lrv"])
        out.cqas["lrv_xmulv"] = inp.cqas.get("lrv_xmulv", 0.0) + clip(lrv_xmulv, 0.0)
        out.cqas["lrv_mvm"] = inp.cqas.get("lrv_mvm", 0.0) + clip(lrv_mvm, 0.0)
        return StepResult(step=self.name, step_yield=step_yield, inp=inp, out=out, params=sp,
                          metrics={"hcp_clearance_fold": hcp_fold, "xmulv_lrf": lrv_xmulv,
                                   "mvm_lrf": lrv_mvm, "hcp_out_ng_mg": out.cqas["hcp"]})
