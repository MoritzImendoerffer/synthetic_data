# Factual check of PCR-009 Version 2.0, draft run 1 (2026-10-11)

Checker: Claude Opus 5.5 (a7225ec9af1776a94). The text matches the pdf rendered at 09:30, before commit 21f0a49 (09:36);
the brief predates it too. Scratch scripts vf_check1–5.py in the scratchpad. Saved by the coordinator.

## Errors, most consequential first
- E1 XMuLV given PARs it cannot have: Table 7.3 shows "50–140 | 50–140 | measured results" and "8–30 | 8–30"; §7 "Table
  7.3 shows the range studied for it where every measured result meets the criterion" and "Its rows of Table 7.3 show
  the range studied, over which every measured result met the claim"; note "Measured results, the output has no
  adequate model…"; §1.2 "every range in this report comes from it or, for an output with no adequate model, from the
  measured results". The current D.par_table gives "n.a. | n.a. | no adequate model"; the report says such an output
  "sets no range" (§3.5) and "has no PAR" (§7, §12 items 4 and 9); PCMP-001 §7.2 and REPORT-LESSONS §1 rule 10 agree;
  brief §4b is stale. Fix: re-render; reword the two §7 sentences and the note ("no PAR (n.a.); every measured result met
  the claim, Section 5.3"); drop the §1.2 clause; in §1.4 add that the Version 1.0 XMuLV PARs (50–140 L/m2, 8–30 psi)
  are withdrawn. Knock-on: INV-001 Table 6.3 counts PCR-009's two XMuLV ranges as "unchanged" (sweep).
- E2 §3.1 "The model was qualified in study S-VF-SDM, from 2026-04-15 to 2026-04-24…" vs Table 3.1 "Qualified: n.a."
  (step yield has no criterion), §12 item 1 (objective 1 not met), REPORT-LESSONS §1 rule 2. Fix: "The qualification runs
  were made in study S-VF-SDM…".
- E3 yield requirement misstated (§13.3 item 3, §3.2 cite only PCP-009 §5.4; "The record does not hold how the yield was
  calculated"). PCP-009 §5.2: "Each design point will be executed once, with both model viruses spiked… Step yield will
  be determined from the same run by protein mass balance, from the ultraviolet absorbance of the load and of the pooled
  filtrate." An unspiked filtrate pool (§5.4) cannot exist: the plan contradicts itself. Version 1.0 PCR-009 §3.3 records
  "mass balance across the filter from the protein concentration and the volume of the load and of the pool", §3.4 the
  samples from the spiked load and the filtrate pool. Fix: cite §5.2 and §5.4 and state the conflict; the departures are
  no concentrations or volumes, no named assay, no load sample before spiking.
- E4 "not measured" where the record is only silent (§3.1 "flux decay profile and the post-use integrity test were not
  measured at either scale", §11, §12 item 1, §13.3 item 1): sdm_qualification.csv holds no flux or integrity data;
  Version 1.0 PCR-009 §3.1 says "Each run was closed with a post-use filter integrity test under SOP-2012… no run of this
  study failed it." Fix: "not recorded"; in §3.2 and §11 add that Version 1.0 asserted every run passed, with no result
  recorded behind it.
- E5 §5.3 fragments: "…so the judgement over the NOR, the PARs and the design space do not change. The same holds for
  the deletion of any other run." Every single-run deletion selects a no-term model on 11 runs with gap 0.21 > 0.20, so
  fragments would have no adequate model and no PAR. Unchanged: the judgement over the NOR (all 19 results 0.54–0.77 %),
  the range carried into the control strategy (set by MVM), the design space. Fix accordingly. [coordinator: for a model
  with no term the gap is (2n−1)/(n−1)², fixed by n (0.19 at 12 runs, 0.21 at 11): say that criterion 3 then judges the
  number of runs, not the model.]
- E6 study events by single-run deletion (§13.1.2 "Whichever run used the lot, its deletion leaves the judgement…
  unchanged (Table 5.9)"; §13.1 "In both the run was retained"; §11): Version 1.0 PCR-009 §13.2 "the runs executed on it
  were retained" (plural); dev_lots.csv "verification run"; deleting one run at a time does not bound an event over
  several runs; Table 5.9 covers response-surface runs only (screening runs enter only the XMuLV measured-results
  judgement, qualification runs only the yield offset). Limit the claim and state these cases.
- E7 §1.4: Version 1.0 NOR-propagated pressure PAR "12.2–24.7 psi"; Version 1.0 printed 12.1–24.8 (same grid range
  12.125–24.775, rounded inward now, to nearest then). Quote Version 1.0's value or say it was recomputed with inward
  rounding.
- E8 §5.2 "No other response showed curvature… (p ≥ 0.49)": step yield p = 0.4857 → "p ≥ 0.48".
- E9 §5.2 and Table 5.2 "significant (p = 0.050)": unrounded 0.0497; print 0.0497 or "p < 0.05".
- E10 §3.5 "R², adjusted R² and predicted R² are reported for every model": Table 5.4 has no adjusted R² for the full
  quadratics (MVM 0.90, XMuLV 0.09, fragments −0.35); the Version 1.0 normality and residual-SE conditions get no
  verdict for the fragments model (Shapiro-Wilk p = 0.744; upper single-run limit 0.78 vs 2.00: both met).
- E11 §1.4 "to every response-surface model" → "…with a criterion" (brief).
- E12 §5.3 "Box-Cox interval, −2.00 to 1.99": −2.00 is the grid end; on −10 to 10 the interval is −5.46 to 1.99
  (conclusion unchanged).
- E13 Table 5.9 "Mean LRF…" holds medians for runs 3 and 7 (log scale; REPORT-LESSONS §7 rule 7).
- E14 builders: Table 8.1 "10.4 ± 0.4" vs "19.9 ± 0.62" (MVM SD 0.395); "≤2" in Tables 7.3 and 8.1 vs "≤ 2.00"; Table 5.4
  hyphen-minus (fixed in 21f0a49).
- E15 executive summary "judges every output against the criteria", "Each output met its intermediate acceptance
  criterion": step yield has no criterion → "every output with a criterion".
- E16 §3.5 capability against "the target and the minimum of PCMP-001 §7.9"; §8 gives only the target (1.33); give the
  minimum (1.0).
- E17 §3.5 paraphrases PCP-009 criterion 4 as "repeating the selection and the judgement over the NOR"; the plan says
  "repeating the judgement" (repeating the selection is what PD-009-02 records as done).
D-001 present as registered (Table 7.3 "PAR (set-point)" as par_table gives it, computed at the design centre 95 L/m2
and 19 psi; §7 does not say where the other parameter was held; no numeric effect at this step).

## Departures from PCP-009 Version 2.0 (none in PLAN_DISCREPANCIES beyond PD-009-01/02)
1. Confirmed: PCP-009 §5.1 and Table 5.1 require flux decay and the post-use integrity result at both scales; the record
   holds yield only (PCMP-001 §5 lists "virus filtration (step yield)" only: a departure from PCP-009).
2. Confirmed for the data (§5.2): no pre- or post-use result for any run; Version 1.0 asserted the post-use tests passed.
3. Partly refuted: yield from spiked runs is what §5.2 planned; no spike correction is required; Version 1.0 §3.3 records
   a mass balance. Confirmed: no concentrations or volumes, no named assay, no load sample before spiking.
4. Confirmed (§5.2, §5.4); Version 1.0 §3.2 and §3.4 say the filtrate was collected in one pool, with a buffer flush, and
   sampled once.
5. Confirmed (§5.3, §12); also the volume filtered in each run is not recorded.
6. Confirmed (§12); the flux comparison was impossible anyway (no flux data).
7. Confirmed: PCP-009 §7 and PCMP-001 §7.7 make pressure a GPP; no term containing pressure is significant for any output
   including step yield; WC-CPP is the config's value. [coordinator: A-Mab classed both parameters WC-CPP, "easy to
   control and ... minimal impact on LRF when operated within their acceptable ranges" (owner question pending)]
8. Confirmed, not listed in §13.3: deletion of all 12 response-surface runs (the plan asks only for runs above 4/n); the
   t-test comparing curvature of the two designs; Shapiro-Wilk and the single-run-limit rule (delegated by PCP-009 §7;
   REPORT-LESSONS §3.2 says record it); comparisons with near-equivalent and stepwise models, studentized residuals and
   leverage; the capability section (absent from PCP-009).
Further: A. PAR plots (PCP-009 §8, one figure per PAR; only Figure 7.1; MVM against pressure not shown; fragments noted
without a figure); B. matched load material, filtration temperature and hold-up volume per area between scales (§5.1)
not recorded; C. virus stock clarified and its volume kept small (§12) not recorded (Version 1.0 §3.1 says the spiked
load was clarified, not the stock); D. sample identification by run and volumetric load (§5.4) not recorded; E. effect as
change over half the range (§5.5) vs whole range (PCMP-001 §6.2), low; F. residual plots and residual SE per response
(§5.5): plots for MVM only, XMuLV residual SE 0.143 not given, low; G. step yield with the operating region and its cost
in product (§7), low; H. calibration-status statement (§9), low.

## Checked and correct
Design matrices and centre-point statistics; screening fits, effects, SE, t, p, curvature (fragments −0.08 and +0.05,
difference 0.13, p = 0.132, 5 df); full-quadratic statistics and coefficients (Tables 5.4, C.3); selected models (Tables
5.5–5.8, C.2: R², F, lack of fit, gap, residual SD, Shapiro-Wilk 0.910, Box-Cox, 13 submodels, AICc gaps 4.6, 1.0, 1.3,
stepwise same model); influence under "4/n flags, F decides" (run 5 Cook's 0.791 vs F median 0.743 fails; run 2 0.401
flagged only; fragments run 9 0.474 vs 0.486; run 5 residual 0.43, studentized 2.85, leverage 0.25); every row of Table 5.9
(slopes −0.770 and −0.934, crossing at 136.1, log scale for runs 3 and 7, the 30 L/m2 margin); predictions 5.54,
5.25–6.31, 4.71, 137.6, 4.57, 1.65, 4.65; fragments interval 0.50–0.78, mean 0.64; design space 110 of 121 (91 %); PARs
for MVM and fragments; measured ranges and 3 MVM results below the claim; criteria and derivation; sums 16.72 and 8.62;
CA3 sensitivity; offset −0.5 (−1.2 to 0.3); capability (Cpk, tails, 0.0015 bound); dates, identifiers, LOQs, event facts,
register entries, PCP-009 and PCMP-001 citations.

## Could not be checked
Figures 5.1, 5.2, 7.1; whether the screening analysis was done before the response-surface runs were committed (PCP-009
§6.2, §11; screening ended 2026-05-05, response-surface began 2026-05-06, no analysis dates); anything absent from the
record (titres, LODs, controls, integrity, fractions, load lots, matching, spike volume, runs affected by each event,
spike correction); the integrated Monte Carlo (not rerun); annex and grounding; the Version 1.0 narrative claims.
