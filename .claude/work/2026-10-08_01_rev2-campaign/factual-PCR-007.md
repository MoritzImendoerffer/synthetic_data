# Factual check of PCR-007 Version 2.0, draft run 1 (2026-10-11)

Checker: Claude Opus 5.5 (a6bc6c07a16683c89). Scratch scripts chk1–chk7.py (scratchpad), read-only against the engine
and CSVs; for the data questions it also read amab_process/unit_ops/cex.py, amab_process/analytics.py and
refs/text/amab.txt. Saved by the coordinator.

## Errors, most consequential first
1. §7.4 HCP: "PCMP-001 §7.5 judges the verification on the predictions of the scale-down model, without an offset."
   Neither PCMP-001 §7.5 nor PCP-007 §7.6 mentions an offset; PCMP-001 §7.1(2) applies the offset to every judgement
   against a criterion; INV-001 CA1 rule 2 "Every Version 2.0 judgement subtracts the offset". The engine
   (amab_process/iac.py::_nor_worst) divides the process-model feed (Protein A pool 9,125 ng/mg; low-pH pool 1.907 %
   HMW) by the scale-down prediction with no offset, and the criteria in force were fixed this way. "Confirmed" holds at
   the offset estimate (40.2) but not at the unfavourable end (28.1 < 40); §10 says the Protein A criterion of 17,069
   ng/mg assumes this confirmation. Fix: say the plans are silent, that the criteria were derived without the offset,
   register it as an approach; keep the sensitivity. [coordinator: owner decision pending]
2. Fragments verification, two verdicts: Table 7.4 (builder) "Confirmed", PCMP-001 §7.5 "the predicted worst case
   confirmed the platform worst case", PCP-007 §7.6 rule gives confirmed (1.449 ≥ 1.30); the executive summary, §7.4 and
   Conclusion 6 say "stands without confirmation" (PCMP-001 §6.3). [coordinator: as for PCR-006: confirmed by the plan's
   rule, on a model that does not meet PCMP-001 §7.2, stated as a limitation]
3. §7.1 and §13.2.1: the widening "decides the qualification … and no conclusion over the NOR": at the a priori 400
   ng/mg the design space is 99.85 %, not 100 % (22 of 14,641 points at load 40 g/L resin, conductivity 3 mS/cm, pH
   6.16–6.2 exceed 400, max 408); the "covers the whole region" claim (exec. summary, §6, §10, §12) rests on the
   widening; PARs and the judgement over the NOR do not change.
4. §5.3.2, §13.2.2, §11: the drift (×1.129) is added to the NOR limit only. Added to the design-space maximum 408 → 461
   ng/mg (99 grid points, 0.68 %, exceed 427); to the qualification's unfavourable end 414 → 467; PARs unaffected
   (highest NOR-propagated 97.5th percentile 291 → 328). State these, or limit "does not depend on the trend" to the NOR.
5. §5.5: the duplicate scatter "is smaller than the residual SD of the response-surface design for every response" is
   false: larger for aggregate (0.102 vs 0.065 ln) and residual DNA clearance (0.203 vs 0.153 log10); smaller only for
   HCP (0.060 vs 0.109) and yield (0.28 vs 1.74).
6. §9: elution flow rate GPP without the significant DNA result (p = 0.044 under the report's own approach; residual DNA
   "affected" under PCMP-001 §6.2): no size against the drug-substance criterion, GPP not named as a judgement.
7. §1.2 "The first five are those of Version 1.0 of the plan": objectives 2 and 3 were amended at Version 2.0 (fragments,
   PCP-007 change 2); objective 5 paraphrase drops "in-process controls and monitoring", objective 2 drops "the fitted
   models predict".
8. §3.2 "Buffers, packing and resin storage met platform specification" not in the record (DEV-007-01 expired buffer
   lot; §3.5.1 item 2 no packing records); "ran at controlled room temperature" restates the plan.
9. §11 and §12 item 7 "the study events … changed no conclusion" too broad: deleting run 14 changes the selected
   aggregate model (loses the conductivity term) and gives yield a stop-collect term (−0.76 per coded unit, p = 0.078,
   in the mechanism's direction); yield models with that term lie 1.1 and 1.8 AICc units away; full-quadratic p 0.239,
   screening 0.268. Name what is unchanged and write "no effect detected" with the tests; §5.3.6 infers "no effect" from
   the selection having removed the term (circular).
10. §5.3.2 and §9: the HCP load curvature as a finding: two of five near-equivalent models drop it; its size (−0.092 ln,
    about 14 ng/mg at set-point) is below the centre-point spread (SD 0.144 ln, 18.7 ng/mg), which PCP-007 §12 says will
    not be claimed.
11. §9 paraphrases PCMP-001 §7.7 without "practically relevant" and the too-small clause.
12. Executive summary and Table 3.2: the window "2026-02-04 and 2026-03-27" omits S-CEX-VER (2026-09-24 to 09-25) and
    S-VI-WC (2026-09-26 to 09-29), both on this scale-down model; Table 3.2 omits S-VI-WC.
13. Minor: Version 1.0 HCP load PAR printed 10–28.4 (report says 10–28.3; unrounded 28.375, now rounded inward); §3.5
    compares a log-scale selected-model residual SD with a raw-scale full quadratic (full quadratic on log 0.040 vs
    0.062); Table 1.2 lacks SOP-3015, SOP-2103, AMV-3019, AMV-3221 though §3.3 says every method is there; HCP least
    favourable combinations quote a stop-collect setting not in the HCP model (tie-break artefact); Table 7.2 footnote b,
    §6 and Conclusion 2 include fragments (no measured offset); Conclusion 3 does not say objective 3 was not met for
    fragments; §1.4 INV-002 covered "every response-surface model" (22 with a criterion, three of four criteria); leached
    Protein A 0.33 (Table 3.1, geometric) vs 0.34 (Table 5.10, arithmetic); "rose to 26.4 °C for 38 minutes" (38 min above
    set-point); centre points at run positions 10, 21, 24, 25 ("spread through" generous); no margin of the flow-rate
    range to the NOR; "before the interactions/curvature are added" misleading; §3.1 adds "at its estimate" to the
    qualification rule.

## Departures from PCP-007 Version 2.0 (none of the author's six refuted)
1. Load aggregate and HCP (§5.4, §12): confirmed. 2. DNA and leached Protein A on the screening runs (§5.4): confirmed.
3. Flow-through, wash and strip, no mass balance (§5.4): confirmed (the strip test could not be triggered: same entry).
4. Packing tests before each campaign (§5.1): confirmed (plate count and asymmetry for the three S-CEX-SDM runs only, no
   limits). Nuance for 1–4: Version 1.0 §3.4, §3.1 say load, flow-through, wash and pools were assayed and the column
   released against SOP-2008, so the entries say "no result in the record", and "Changes in this revision" says so.
5. S-CEX-FRC: confirmed, in neither version of PCP-007 nor its Table 11.1 (fractionated runs F2–F5, Table 3.4); under
   PCP-007 or AMD-001 is a coordinator call; it needs an entry.
6. The seven decisions without a threshold: confirmed; items 1, 3, 5, 7 are the report's own approaches (need entries);
   items 2, 4, 6 could not be applied because of departures 4, 3 and 1.
Additional: 7. step-level capability (PCP-007 §5.5, kept from Version 1.0: fitted models over 2,000 NOR draws, Cpk per
Table 7.1 attribute against its intermediate criterion) not given; 8. verification without the offset (error 1);
9. the fragments confirmation rule of §7.6 not applied (error 2); 10. feed lots (§6.2) not recorded.
Not verifiable: sample assignment to analytical runs (§5.4; matters for the HCP drift); retention under SOP-2010; whether
the screening analysis preceded the response-surface study (§11).

## Data questions
1. Stop-collect sign: a modelling problem, not chance. unit_ops/cex.py aggregate fold 2.5·(1 − 0.30·load − 0.15·pH −
   0.12·stop collect), +1 = 1.5 AU (an earlier stop): aggregate rises with the AU setting, opposite to the plan and to
   A-Mab ("Extended stop collect leads to minor increase in aggregate levels in pool"); no stop-collect term in yield
   (A-Mab models yield on it); the fragment model (analytics.frag_cex, −0.10) uses the opposite convention, matching the
   plan: the seeded model is internally inconsistent. Owner: fix the config sign and add a yield term, or register it.
2. Flow rate: enters no CEX output in the model, DNA clearance drawn independently of the setting, so p = 0.044 is a
   false positive by construction; yield has no flow effect. The report must classify on its data: residual DNA is
   "affected", so GPP needs a named judgement of practical relevance (0.32 log10, factor 2.1 over 100–300 cm/hr, about
   half across the NOR; drug substance 0.00017 ng/dose, Cpk 7.3, resting on the anion exchange 5 log10, a model input).
   For yield the interval (−5.19 to 2.00 points) includes the load effect (−5.18), so "changes neither" is not shown.
3. Verification with scale-down predictions and no offset: confirmed (iac._nor_worst, raw doe_cex_rsm.csv), mixing a
   manufacturing-scale feed with a scale-down pool prediction. HCP lowest factor 40.2 at the offset estimate, 28.1 / 57.6
   at the interval ends; bound 32.9 at the estimate, 23.0 / 47.1 at the ends. Aggregate lowest factor 1.40 / 1.78 at the
   interval ends (not confirmed either way); its bound moves to 1.24 / 1.58.

## Checked and correct
Screening effects and fit statistics (Tables 5.2, C.1); selected models, ANOVA, coefficients (5.3–5.7, C.2); Box-Cox λ
and intervals; 1,337 candidates; stepwise AICc; criterion 4 under "4/n flags, F decides" (aggregate met: flagged 7, 10,
15, F median 0.96; HCP not met: order p = 0.043, flagged 8, 13, F median 0.94; fragments and yield met); Tables 5.8, 5.9;
drift (−0.0045 per run, 0.121, ×1.13, 326 ng/mg); fold changes and set-point predictions; Table 3.1, 414 ng/mg, p 0.016
and 0.285, 83.3–176; Table 7.2, worst corners, 9 and 95 SDs, design space (100 %, 408, 2.20), Table 7.3; Tables 7.1 and
7.4, 427/400/107, 0.024/0.824/3.63, all-runs bound 4.27 with 12 runs, 7.02/6.46, 1.35, 158 ppm, 17,069; S-CEX-VER and
S-VI-WC folds and bounds; Table 8.1, zero OOS, 0.15 %, 30.5 ng/dose; Table 5.1; screening vs response surface (0.98,
p = 0.739, 478/265, 368, 0.59 vs 0.13); DNA and leached Protein A figures; Tables 5.10 and 5.11 except error 5; event
facts and residuals, run-14 deletion (1.39 %, 288 ng/mg), 9.44 %; dates and calibration; method precisions and LOQs;
Table 3.4; Appendices A, B, B.2; both registers; plan citations.

## Could not be checked
Figures; PCR-008 (draft); packing tests, feed lots, analytical-run order, run-14 re-assay, the cause of the HCP drift,
whether run 6's wash was at its design 7 mS/cm (re-test 5.06; Version 1.0 said in-line measurement verified it); a "Tris"
buffer at pH 5.02 (outside Tris's range); brief §4b still gives fragment PARs (engine now "n.a.").
