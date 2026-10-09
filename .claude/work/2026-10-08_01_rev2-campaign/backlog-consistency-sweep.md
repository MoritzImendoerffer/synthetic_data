# Consistency sweep and open decisions (kept current; 2026-10-09)

## Owner decisions pending
1. **Widening bound.** The rule widens a criterion on the one-sided 95 % confidence bound of the MEAN
   clearance at the least favourable NOR combination; outputs are judged per batch. A single-batch
   prediction bound would: CEX HCP 36.7 (< 40, would tighten), AEX HCP 4.27 (> 4, still widens), CEX
   aggregate 1.40 (tighter than 1.52). The Protein A and CEX scale-down qualifications for HCP depend on
   the widening (`D.ca3_criteria_sensitivity()`). Changing the rule re-issues PCMP-001 §7.5.
2. **Harvest and UF/DF univariate design.** Version 1.0 recorded three levels (edges and set-point;
   intermediate settings for depth filter load; 9 runs for UF/DF with 3 set-point replicates) and
   post-clarification turbidity not set at chosen levels. The option-A data have five levels in
   duplicate and turbidity as a challenge. Recommendation: align the generator to Version 1.0's design.
3. **Low-pH NOR edge.** The upper pH NOR edge (3.5) is 0.04 from the XMuLV PAR edge (3.54) at the least
   favourable NOR combination of hold time and temperature (`D.par_margins`).
4. **Osmolality (PCR-003).** Screening: osmolality main effect on acidic variants −2.55 points
   (p = 0.013), temperature × osmolality on galactosylation (p = 0.002); not in the response-surface
   design. Recommendation: PCR-003 states it, classifies osmolality on the screening, and includes it
   in the acidic-variant mitigation.

## Shipped documents to touch in the sweep (re-render, rebuild annex, ground)
- **PCP-005:** "The model is qualified … in study S-PA-SDM … before the first run of the screening
  design": the runs and the offset estimate come first, the qualification decision needs the
  response-surface model and is made at analysis. Also re-render for `T.criteria_change` ("from"
  a priori value) and `T.sop_references` (titre method, no duplicates).
- **INV-001:** re-render for `T.criteria_change`; rebuild the annex (the criteria rows change).
- **PCMP-001:** check the same qualification-sequencing wording in §5 and §7.1.

## Machinery noted, not yet done
- Done 2026-10-09: named constants `D.PAR_GRID_SETPOINT`, `D.NOR_SD_DIVISOR`, `D.PI_LEVEL`,
  `D.VERIFICATION_BOUND` (= `iac.BOUND_CONFIDENCE`); PCP-003 and PCP-006 use them.
- `_pcpkg` has no `BIOREACTOR_SOP_REFS`/`BIOREACTOR_AMV_REFS`; PCP-003 filters `SOP_REFS`/`AMV_REFS`.
- **Title block (2026-10-09):** "(Step N)" no longer wraps; the sites are three rows (sponsor,
  development site, commercial drug substance site) instead of one row joined by an arrow. The site
  entities of the annexes now quote those rows. Every shipped Version 2.0 document (PCMP-001, PCP-005,
  INV-001, and PCR-005 when promoted) must be re-rendered BEFORE its annex is rebuilt.
