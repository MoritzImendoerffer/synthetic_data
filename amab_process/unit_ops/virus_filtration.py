"""Step 9 — Small Virus Retentive Filtration.

Dedicated orthogonal virus removal by size exclusion. MVM (small parvovirus)
log-reduction falls as the volumetric load rises (A-Mab Fig 4.15: LRV >= 4.62 up
to 105 L/m2); XMuLV shows no breakthrough. Filtration volume and pressure are
WC-CPPs; the step does not affect product quality. (p.152-166)
"""

from __future__ import annotations

from typing import Dict, Optional

import numpy as np

from ..core import Stream, StepResult, clip, lognormal_noise
from .base import BaseUnitOp


class VirusFiltration(BaseUnitOp):
    key = "virus_filtration"

    def run(self, inp: Stream, rng: np.random.Generator,
            setpoints: Optional[Dict[str, float]] = None) -> StepResult:
        sp = self.setpoints(setpoints)
        m = self.uo.model
        vol = sp["filtration_volume"]
        vol_ref = self.uo.param("filtration_volume").setpoint

        lrv_mvm = m["lrv_mvm_base"] + m["lrv_mvm_volume_coef"] * (vol - vol_ref)
        lrv_mvm = clip(lrv_mvm * lognormal_noise(rng, m["lrv_cv"]), 0.0)
        lrv_xmulv = clip(m["lrv_xmulv_base"] * lognormal_noise(rng, m["lrv_cv"]), 0.0)

        step_yield = clip(m["yield_base"] * lognormal_noise(rng, m["yield_cv"]), 0.9, 0.999)

        out = inp.copy()
        out.product_mass_g = inp.product_mass_g * step_yield
        out.cqas["lrv_mvm"] = inp.cqas.get("lrv_mvm", 0.0) + lrv_mvm
        out.cqas["lrv_xmulv"] = inp.cqas.get("lrv_xmulv", 0.0) + lrv_xmulv
        return StepResult(step=self.name, step_yield=step_yield, inp=inp, out=out, params=sp,
                          metrics={"mvm_lrf": lrv_mvm, "xmulv_lrf": lrv_xmulv})
