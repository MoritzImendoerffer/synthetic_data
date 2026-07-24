"""Step 3 — Production Bioreactor (fed-batch).

Semi-mechanistic: a logistic growth / integral-productivity model gives the
viable-cell-density (VCD), viability and titer time-course; a second-order
response-surface model (A-Mab Table 3.16, coded factors) maps the multivariate
operating point to the product-quality CQAs set in cell culture (afucosylation,
galactosylation, high mannose, aggregates, acidic charge variants) and the
harvest impurity load (HCP, DNA).
"""

from __future__ import annotations

from typing import Dict, Optional

import numpy as np
import pandas as pd

from ..core import Stream, StepResult, rsm, clip, lognormal_noise
from .base import BaseUnitOp


class Bioreactor(BaseUnitOp):
    key = "bioreactor"

    # -- kinetics --------------------------------------------------------------
    def timecourse(self, setpoints: Optional[Dict[str, float]] = None,
                   rng: Optional[np.random.Generator] = None) -> pd.DataFrame:
        """Daily VCD / viability / titer profile for the given operating point."""
        sp = self.setpoints(setpoints)
        c = self.coded(sp)
        k = self.uo.raw["kinetics"]

        duration = int(round(sp["duration"]))
        vcd0 = sp["ivcc"]
        mu = k["mu_max"] * (1 + k["mu_temp"] * c.get("temperature", 0)
                            + k["mu_pH"] * c.get("pH", 0))
        vcd_max = k["vcd_max"] * (1 + k["vcdmax_pH"] * c.get("pH", 0)
                                  + k["vcdmax_temp"] * c.get("temperature", 0)) \
            * (0.6 + 0.4 * sp["medium_conc"]) * (0.8 + 0.02 * sp["feed_vol"])
        vcd_max = max(vcd_max, vcd0 * 1.5)

        days = np.arange(0, duration + 1)
        # logistic growth
        ratio = (vcd_max - vcd0) / max(vcd0, 1e-6)
        vcd = vcd_max / (1 + ratio * np.exp(-mu * days))
        # viability: high during growth, declines in stationary/death phase
        t_peak = np.log(ratio) / mu if ratio > 1 else 1.0
        death_rate = 0.03 + 0.010 * max(0.0, c.get("temperature", 0)) \
            + 0.008 * max(0.0, c.get("duration", 0))
        via = 100.0 * np.exp(-death_rate * np.clip(days - t_peak, 0, None))
        via = np.clip(via, 20, 99.5)
        viable = vcd * via / 100.0
        ivcc = np.cumsum(viable)  # e6 cells/mL * day (trapezoid ~ cumulative sum)

        titer = k["qp"] * ivcc / 10.0
        titer = titer * (1 + k["titer_do"] * c.get("do", 0))
        if rng is not None:
            titer = titer * lognormal_noise(rng, k["titer_cv"])

        return pd.DataFrame({
            "day": days, "vcd": vcd, "viability": via,
            "viable_cell_conc": viable, "ivcc": ivcc, "titer": titer,
        })

    # -- CQA response surface --------------------------------------------------
    def _cqas(self, c: Dict[str, float], final_via: float,
              rng: Optional[np.random.Generator]) -> Dict[str, float]:
        r = self.uo.raw["rsm"]
        centre, lin, inter, quad = r["centre"], r["linear"], r["interactions"], r.get("quadratic", {})
        noise = r.get("noise_cv", {})

        def response(name: str, base: float, hard_lo=0.0, hard_hi=None) -> float:
            y = rsm(base, lin.get(name, {}), c,
                    quadratic=quad.get(name, {}),
                    interactions={tuple(kk.split("*")): vv for kk, vv in inter.get(name, {}).items()})
            if rng is not None and name in noise:
                y *= lognormal_noise(rng, noise[name])
            return clip(y, hard_lo, hard_hi)

        cqas = {
            "afucosylation": response("afucosylation", centre["afucosylation"]),
            "galactosylation": response("galactosylation", centre["galactosylation"]),
            "acidic_variants": response("acidic_variants", centre["acidic_variants"]),
            "aggregates_hmw": response("aggregates_hmw", centre["aggregates_hmw"]),
        }
        # high mannose: centre + mild pH/temperature dependence (higher pH, lower temp -> more Man5).
        # DO is deliberately excluded so it remains a true KPP (no significant CQA impact) per A-Mab.
        hm = self.uo.raw.get("high_mannose_centre", 6.0) \
            * (1 + 0.15 * c.get("pH", 0) - 0.08 * c.get("temperature", 0))
        if rng is not None:
            hm *= lognormal_noise(rng, noise.get("high_mannose", 0.08))
        cqas["high_mannose"] = clip(hm, 0.0)

        # harvest impurity load (driven by culture duration / viability)
        hc = self.uo.raw["rsm"]["harvest_centre"]
        via_factor = (100.0 - final_via) / (100.0 - 60.0)  # 0 at 100% via, 1 at 60%
        hcp = hc["hcp"] + lin["hcp"]["duration"] * c.get("duration", 0)
        hcp *= (0.7 + 0.6 * clip(via_factor, 0, 2))
        dna = hc["residual_dna_rel"] + lin["residual_dna_rel"]["duration"] * c.get("duration", 0)
        dna *= (0.7 + 0.6 * clip(via_factor, 0, 2))
        if rng is not None:
            hcp *= lognormal_noise(rng, 0.15)
            dna *= lognormal_noise(rng, 0.20)
        cqas["hcp"] = clip(hcp, 1.0)
        cqas["residual_dna"] = clip(dna, 1.0)
        return cqas

    # -- run -------------------------------------------------------------------
    def run(self, inp: Optional[Stream], rng: np.random.Generator,
            setpoints: Optional[Dict[str, float]] = None) -> StepResult:
        sp = self.setpoints(setpoints)
        c = self.coded(sp)
        tc = self.timecourse(sp, rng)
        final_via = float(tc["viability"].iloc[-1])
        titer = float(tc["titer"].iloc[-1])
        volume = float(self.cfg.meta["commercial_scale_l"])

        cqas = self._cqas(c, final_via, rng)
        out = Stream(product_mass_g=titer * volume, volume_l=volume, cqas=cqas,
                     meta={"titer_g_per_l": titer, "final_viability_pct": final_via,
                           "peak_vcd": float(tc["vcd"].max()),
                           "ivcc": float(tc["ivcc"].iloc[-1])})
        return StepResult(step=self.name, step_yield=1.0,
                          inp=inp or Stream(0.0, volume), out=out,
                          params=sp, metrics={"titer_g_per_l": titer,
                                              "final_viability_pct": final_via,
                                              "peak_vcd_e6": float(tc["vcd"].max())})
