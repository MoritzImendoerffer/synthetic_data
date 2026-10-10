"""Step 10 — Ultrafiltration / Diafiltration (formulation).

NOT part of the A-Mab drug-substance characterization (p.140); included for mass
balance and to express the final drug substance. Concentrates to the DS target
and converts residual DNA from pg per mg of antibody to ng per dose (``meta.dose``).

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



def dna_ng_per_dose(cfg, pg_per_mg):
    """Residual DNA per dose: pg DNA per mg antibody times the mg of antibody in one dose
    (``meta.dose``: mg/kg times body weight), in ng (owner's decision Q4, 2026-10-10)."""
    d = cfg.meta["dose"]
    return pg_per_mg * float(d["mg_per_kg"]) * float(d["body_weight_kg"]) / 1000.0


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
        # express residual DNA as ng/dose for the drug substance (pg/mg upstream of this step)
        out.cqas["residual_dna"] = dna_ng_per_dose(self.cfg, inp.cqas.get("residual_dna", 0.0))
        out.meta["ds_concentration_g_per_l"] = final_conc
        # permeate flux at the end of the final concentration, deterministic (no draw from rng)
        fx = m.get("flux_lmh", {"setpoint": 0.0, "tmp": 0.0, "conc": 0.0})
        flux = float(fx["setpoint"]) + float(fx["tmp"]) * ct + float(fx["conc"]) * cc
        return StepResult(step=self.name, step_yield=step_yield, inp=inp, out=out, params=sp,
                          metrics={"ds_concentration_g_per_l": final_conc,
                                   "residual_dna_ng_per_dose": out.cqas["residual_dna"],
                                   "residual_buffer_pct": residual_buffer,
                                   "flux_lmh": flux})
