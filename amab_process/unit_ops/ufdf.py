"""Step 10 — Ultrafiltration / Diafiltration (formulation).

NOT part of the A-Mab drug-substance characterization (p.140); included for mass
balance and to express the final drug substance. Concentrates to the DS target
and converts the tracked relative residual-DNA quantity to ng/dose.

Version 2.0 adds the effects of the univariate study S-UFDF-UNI (``process.ufdf.model``): residual
buffer falls as exp(-DV); aggregate rises a little at high final concentration and high TMP; step
yield falls a little at high concentration. Every term is zero at set-point and draws nothing from
``rng``, so no stream moves and the nominal batch is unchanged.
"""

from __future__ import annotations

from typing import Dict, Optional

import numpy as np

from ..core import Stream, StepResult, clip, lognormal_noise
from .base import BaseUnitOp

# Calibration: relative residual-DNA units -> ng/dose. Chosen so the nominal
# process (harvest DNA ~1e3 rel, ~8 logs total clearance) lands ~1e-4 ng/dose,
# an order of magnitude below the <1e-3 ng/dose acceptance criterion (p.47-48).
DNA_NG_PER_DOSE_PER_REL = 10.0


class UFDF(BaseUnitOp):
    key = "ufdf"

    def run(self, inp: Stream, rng: np.random.Generator,
            setpoints: Optional[Dict[str, float]] = None) -> StepResult:
        sp = self.setpoints(setpoints)
        y = self.uo.raw["yield"]
        m = self.uo.raw["model"]
        final_conc = sp.get("final_conc", self.cfg.meta["drug_substance_target_g_per_l"])
        cc = (final_conc - float(self.uo.param("final_conc").setpoint_characterized)) / m["conc_scale_g_l"]
        ct = (sp["tmp"] - float(self.uo.param("tmp").setpoint_characterized)) / m["tmp_scale_psi"]
        step_yield = clip(y["base"] * lognormal_noise(rng, y["cv"]) + m["yield_conc"] * cc, 0.85, 0.995)

        out = inp.copy()
        out.cqas["aggregates_hmw"] = inp.cqas.get("aggregates_hmw", 0.0) + (
            m["aggregate_conc"] * cc + m["aggregate_tmp"] * ct + m["aggregate_conc_tmp"] * cc * ct)
        residual_buffer = m["residual_buffer_pct_at_0dv"] * float(np.exp(-sp["diavolumes"]))
        out.product_mass_g = inp.product_mass_g * step_yield
        out.volume_l = out.product_mass_g / final_conc
        # express residual DNA as ng/dose for the drug substance
        out.cqas["residual_dna"] = inp.cqas.get("residual_dna", 0.0) * DNA_NG_PER_DOSE_PER_REL
        out.meta["ds_concentration_g_per_l"] = final_conc
        return StepResult(step=self.name, step_yield=step_yield, inp=inp, out=out, params=sp,
                          metrics={"ds_concentration_g_per_l": final_conc,
                                   "residual_dna_ng_per_dose": out.cqas["residual_dna"],
                                   "residual_buffer_pct": residual_buffer})
