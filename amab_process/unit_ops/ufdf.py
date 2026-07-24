"""Step 10 — Ultrafiltration / Diafiltration (formulation).

NOT part of the A-Mab drug-substance characterization (p.140); included for mass
balance and to express the final drug substance. Concentrates to the DS target
and converts the tracked relative residual-DNA quantity to ng/dose.
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
        step_yield = clip(y["base"] * lognormal_noise(rng, y["cv"]), 0.85, 0.995)

        final_conc = sp.get("final_conc", self.cfg.meta["drug_substance_target_g_per_l"])
        out = inp.copy()
        out.product_mass_g = inp.product_mass_g * step_yield
        out.volume_l = out.product_mass_g / final_conc
        # express residual DNA as ng/dose for the drug substance
        out.cqas["residual_dna"] = inp.cqas.get("residual_dna", 0.0) * DNA_NG_PER_DOSE_PER_REL
        out.meta["ds_concentration_g_per_l"] = final_conc
        return StepResult(step=self.name, step_yield=step_yield, inp=inp, out=out, params=sp,
                          metrics={"ds_concentration_g_per_l": final_conc,
                                   "residual_dna_ng_per_dose": out.cqas["residual_dna"]})
