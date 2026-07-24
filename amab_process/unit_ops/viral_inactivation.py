"""Step 6 — Low-pH Viral Inactivation.

Inactivates enveloped virus (XMuLV). pH is a CPP (narrow range, high consequence);
hold time and temperature are WC-CPPs; protein concentration is a GPP. Aggregate
rises with hold time and temperature (A-Mab Table 4.16: 1.8 -> 2.5% over 0-180 min);
XMuLV log-reduction rises at lower pH, longer time, higher temperature. (p.127-133)
"""

from __future__ import annotations

from typing import Dict, Optional

import numpy as np

from ..core import Stream, StepResult, clip, lognormal_noise
from .base import BaseUnitOp


class ViralInactivation(BaseUnitOp):
    key = "viral_inactivation"

    def run(self, inp: Stream, rng: np.random.Generator,
            setpoints: Optional[Dict[str, float]] = None) -> StepResult:
        sp = self.setpoints(setpoints)
        c = self.coded(sp)
        m = self.uo.model

        # aggregate delta (%) scaled by absolute hold time (0..180) + temperature
        agg_delta = m["agg_delta_180"] * (sp["hold_time"] / 180.0) \
            + m["agg_temp_coef"] * c.get("temperature", 0)
        agg_delta *= lognormal_noise(rng, m["agg_cv"])

        # XMuLV log-reduction (LRF)
        lrv = (m["lrv_base"] + m["lrv_ph_coef"] * c.get("ph", 0)
               + m["lrv_time_coef"] * c.get("hold_time", 0)
               + m["lrv_temp_coef"] * c.get("temperature", 0))
        lrv = clip(lrv * lognormal_noise(rng, m["lrv_cv"]), 0.0)

        out = inp.copy()
        out.cqas["aggregates_hmw"] = clip(inp.cqas.get("aggregates_hmw", 0.0) + agg_delta, 0.0)
        out.cqas["acidic_variants"] = inp.cqas.get("acidic_variants", 0.0) \
            + m["acidic_delta"] * (sp["hold_time"] / 180.0)
        out.cqas["lrv_xmulv"] = inp.cqas.get("lrv_xmulv", 0.0) + lrv
        out.product_mass_g = inp.product_mass_g * 0.99  # minimal loss (pH adjust/filter)
        return StepResult(step=self.name, step_yield=0.99, inp=inp, out=out, params=sp,
                          metrics={"xmulv_lrf": lrv, "aggregate_delta_pct": agg_delta,
                                   "aggregate_out_pct": out.cqas["aggregates_hmw"]})
