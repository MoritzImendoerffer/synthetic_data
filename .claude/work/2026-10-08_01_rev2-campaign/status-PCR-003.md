# Status — PCR-003 Version 2.0 authoring (one-pass, RUNNER.md)

Author: Claude Opus 5.5 (claude-opus-5-5), started 2026-10-10.
Target file: `pc_package/PCR-003_bioreactor.DRAFT.qmd` (template already instantiated).
Scratch: `/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/be14bf3c-e46a-46fd-b419-65482c2add0e/scratchpad/pcr003/`

## Inputs read (step 1)
- [x] authoring/RUNNER.md
- [x] authoring/out/PCR-003.brief.md — REGENERATED at start (old brief lacked DEV-003-03..06, PD-003-05/06; numbers unchanged). Old copy in scratch `brief.old.md`.
- [x] authoring/section_plan.yaml (report_doe)
- [x] authoring/STORY_BIBLE.md (§9b)
- [x] authoring/WRITING_GUIDE.md
- [x] authoring/REGISTER_EXEMPLAR.md
- [x] procedures/REPORT-LESSONS.md (§6 owner decisions 2026-10-10)
- [x] data-state-2026-10-09b.md, data-state-2026-10-10.md
- [x] pcr003-departures.md
- [x] rendered PCP-003 (scratch PCP-003.txt) and PCMP-001 (scratch PCMP-001.txt), content only

## Key facts / decisions so far
- Registers: DEV-003-01..06, PD-003-01..06 (render `dev_register(DOC)`, `discrepancy_register(DOC)`).
- D-002 (brief §5c): absolute "only step at which product quality attributes are formed" in Introduction, product/unit-op paragraph, followed by the narrower true elaboration. Leave alone.
- Plan PCP-003 adequacy criteria list a–e (e = normal quantile plot), PCMP-001 §7.2 lists 4.
- Plan §6.4: univariate effect the mechanism does not explain -> multivariate study + plan amendment. iVCC on acidic variants: judgement pending (look at data).
- Plan §7 crit 6: NOR narrowed if not inside region -> DEV-003-04 (not narrowed, owner 6a).
- Plan §11: univariate after RSM -> DEV-003-06.

## Data findings (scratch explore1-6.py)
- Selected models (all runs n=44, block): afuc raw 9 terms; gal raw 7; HM log 3 (pH, T, pH:T); acidic log 9; agg log 4 (pH, dur, pH:dur, pH^2). All pass F, LOF, gap. ALL FAIL criterion 4 (Cook 4/n; gal & acidic also spread trend). Influence analysis (delete each flagged run, reselect, judge NOR): no conclusion changes. Near-equivalent (<=2 AICc): afuc 3, gal 1, HM 3, acidic 11, agg 2; same conclusions, all qualified. Acidic: only pH, T, co2, pH:T common.
- Residual SD halves: acidic lower half 0.033 vs upper 0.063 (log); worst-corner PI low end with half SD 17.0 <18 -> still not met. Gal halves equal; met.
- nor_met: acidic False (worst corner pH 6.95, T 34.5, dur 18, co2 130: median 18.39, PI 16.25-20.82). Others True.
- PARs (NOR) all contain NOR; acidic pH to 7.025 (margin 0.075), co2 to 131.5 (margin 1.5).
- Design space (single-batch): 73.7 % of 11^4 grid; binding acidic. Mean basis 91.7 %.
- SDM: all five qualified (acidic: not met at lo/point/hi -> same conclusion). HM, acidic, agg ratio offsets.
- Cpk (DS): acidic 1.05 (between 1.0 and 1.33), others >1.33. P(OOS) acidic 1/2000, 821 ppm.
- Screening: osmolality significant on galactosylation (main + BD, CD, DE) AND acidic variants. DEV-003-03 summary names acidic only -> hand-back note.
- DEV-003-01 (screening run 4 pCO2 probe drift 6.5 mmHg, sign not in record): recoding +/-6.5 leaves every significant screening effect unchanged; excluding run 4 leaves 2 residual df.
- Univariate (duplicates, pooled SD 8 df): iVCC raises acidic variants +3.42 (p=0.009). Nothing else significant. JUDGEMENT: mechanism (2b) does not account for it (culture duration, the direct time-at-temperature lever, has no detectable main effect on acidic variants; 2b says iVCC changes IVC/titre, not attributes) -> plan 6.4 rule sends iVCC to a multivariate study: NOT DONE, NOT REGISTERED -> hand-back. Also NOR-low iVCC lowers acidic variants at the worst corner (no owner risk decision covers it) -> hand-back.
- S-BRX-OSM and S-BRX-AUG: chronology records no equipment/probe calibration status (PCP-003 §9, PA3) -> hand-back.
- HCP/DNA (clarified harvest) on screening, RSM, univariate runs; not on augmentation, OSM, qualification -> hand-back (sampling rule vs augmentation runs).
- Class conflicts with plan prior knowledge: basal medium GPP though 2b/plan say it changes growth/titre; DO KPP though plan says growth not expected to move. Process performance not recorded (DEV-003-05). -> hand-back.
- Offsets (Version 2.0 rule) necessarily computed in the re-analysis, after the characterization runs (PCMP-001 requires before) -> hand-back.
- governing_factor agrees with the largest main effect of every selected model (checked).

## Progress
- [x] helper signatures read
- [x] data explored (scratch script)
- [x] setup code written and tested standalone: scratch setup_code.py + setup_extra.py (all asserts pass, ~34 s)
- [x] body part 1 written: scratch body1.md (front matter blocks, exec summary, intro, prior knowledge, methods)
- [x] body part 2 (study design, results) -> scratch body2.md
- [x] body part 3 (design space .. appendices) -> scratch body3.md
- [x] assembled into pc_package/PCR-003_bioreactor.DRAFT.qmd; from here the DRAFT is the master copy (scratch parts are stale)
- check_render passes: 1 dry (ok), 2 (leak of 2 inline exprs in captions), 3 (font 7.7 pt univariate table),
  4 (same), 5 (all green), 6 (all green after content fixes). PDF 79 pp.
- [x] visual check of every complex table and figure (fixed: univariate table width, pipe-table number
  re-parsing, two headers, capability formats, PAR margins as routine SDs, narrowing claim, aggregate precision)
- [x] manual pdf + docx renders; final check_render (pass 7) all green. PDF 79 pp; prose 784 sentences / 14,989 words.
- DONE 2026-10-10 ~15:50. Not committed.

## Hand-back (unregistered departures, NOR, helpers)
1. iVCC raises acidic variants (+3.42 pts, p=0.009); mechanism does not account for it -> PCP-003 §6.4 multivariate
   study not made (unregistered). At iVCC NOR low acidic variants ~0.68 pts lower: not covered by decision 6a.
2. S-BRX-OSM / S-BRX-AUG records: no equipment, no pCO2 probe calibration status (PCP-003 §9, PA3); ran after the
   EQ-BRX-205 due date 2026-06-14.
3. HCP/DNA not measured on the 16 augmentation runs or in S-BRX-OSM (PCP-003 §5.4 "every run").
4. Version 2.0 offsets computed in the re-analysis, after the characterization runs (PCMP-001 requires before).
5. DEV-003-05 scope names characterization runs; qualification runs lack VCD/viability/titre too.
6. DEV-003-03 scope names acidic variants; screening also shows osmolality on galactosylation (p=0.008, + 3 interactions).
7. DEV-003-01 record lacks the sign of the drift (no setting correction possible); run 4 analysed at both settings.
8. Classes vs prior knowledge: basal medium GPP though plan/2b expect growth/titre effect (-> KPP); DO KPP though
   plan expects no growth change. No process-performance data (DEV-003-05).
9. pCO2 direction contradicts mechanism file / PCP-003 §4.1 (acts like higher pH, not lower).
10. NOR: 9/81 NOR combinations fail, all pCO2 NOR high, some with pH at set-point -> narrowing pH alone would not
    restore (STORY_BIBLE says pH or pCO2). If revisited, the pCO2 upper NOR is the lever.
11. Helpers: show() re-parses numeric strings (decimals lost); governing_factor ranks by screening effects (agrees here);
    HM full quadratic still fails overfitting limit on all runs (gap 0.247) after the INV-002 augmentation.
- Note 2026-10-10 15:10: run was cut once; upstream changed wording only (PCMP-001 §7.5 widening = first three
  adequacy criteria; §6.2 design space on single-batch statistic). outputs/ unchanged (11:08).
- Extra finding: acidic variants fail at 9 of 81 NOR combinations (all pCO2 NOR high), not only the 4-way corner.
- [ ] draft written
- [ ] check_render passes: 0
- [ ] pdf + docx rendered, tables/figures inspected
- [ ] hand-back written


---

# Revision run (2026-10-10, 17:00 onward): content review + factual check + owner's Cook decision

Author: Claude Opus 5.5 (claude-opus-5-5). Same draft `pc_package/PCR-003_bioreactor.DRAFT.qmd`, rebuilt from scratch
parts in `scratchpad/pcr003/rev/` (setup.py, b1.md, b2.md, b3.md, assemble.py; run-1 draft kept as rev/draft.run1.qmd).
Not committed.

## Inputs (read)
- feedback-PCR-003.run1.md (fix list), factual-PCR-003.md, content-review-PCR-003.md, procedures/REPORT-LESSONS.md
- brief regenerated twice: at the start (nine deviations) and at 17:50 after the owner's decision "4/n flags, F decides"
  (data-state-2026-10-10.md §5; PD-003-04 reworded)
- rendered PCP-003 (17:26) and PCMP-001 (17:23), content only (§6.4, §7 items 3-7, PCMP-001 §7.2, §7.5)

## Owner's decision folded in (criterion d, residuals and influential runs)
- Setup: RI_FAIL == SPREAD == [galactosylation, acidic variants]; no run above the F(p, n-p) median (0.886-0.959);
  17 flags at 4/n on 13 runs, each examined by deletion (planned work). The low-pH aggregate model behind the widened
  bound meets criterion d too (asserted).
- Text: exec summary, §1.4 item 4, §3.5 criterion d and the deletion paragraph, §5.3.2 (+ Table 5.5 with the F median
  and a verdict column), §7.1 (low-pH model), Discussion item 2, PD-003-04 subsection.

## Gates
- check_render dry runs: all chunks exec, all inline eval, style gate green, no NEEDS (several passes).
- A pdf render failed once at 17:5x on an assert of the old criterion d (the engine changed mid-render); fixed.
- Words of prose 15,808 (run 1: 14,989); restatements cut before adding (Discussion opening, PD subsections reduced
  to what each changed, DEV-003-04/07 shortened, Stage 2 sentence, osmolality-rise repeats, §2.1 sentence).

## Final state (20:36)
- check_render --render (venv on PATH): pass 4 of the revision; gate exit 0. All chunks exec, all inline expressions
  evaluate, no NEEDS, style gate green, docx and pdf render, glyphs ok, references resolved, 19 complex tables complete,
  page foot clear, no repeated index cells, no text below 7.9 pt. The earlier failures were Table 5.6 at 7.0 pt
  (narrowed), plus one pdf render killed by the old criterion d assert. The numeral lint is advisory: 92 lines,
  all of them conventions (95 %, objective and version numbers, run 4, coded levels).
- PDF 82 pp (run 1: 79). Prose 774 sentences / 15,817 words (run 1: 784 / 14,989). Restatements were cut first.
  The growth comes from new required content: DEV-003-07/08/09, the planned-runs analysis, Table 5.6 (effect against
  criterion width), criterion d with the F limit, and the longer register tables, which come from the builders.
- Text extract refreshed: .claude/work/2026-10-08_01_rev2-campaign/PCR-003_bioreactor.DRAFT.txt.
- Page images viewed: Tables 4.3, 5.2, 5.3, 5.5, 5.6, 5.9, 5.10, 5.11, 5.12, 7.3, 8.1, 13.1, 13.2, A.1, B.1, B.2
  and Figure 6.1 (hatched).

## Hand-back (revision)
1. Ground 2 of DEV-003-04 does not support the decision on its own. The containment rests on the 16 augmentation runs
   (added after the planned results, pCO2 calibration not recorded, DEV-003-08) and on model selection. On the planned
   runs alone the acidic-variant PARs are pH 6.6-6.93, 34.6-36 °C and 40-116 mmHg, so none contains the NOR; the worst
   corner is 18.01 % with a lower limit of 15.48 %; the design space is 59.6 % (73.7 % on all runs).
2. Integrated model (engine question): no scale-down offset, no fitted model, no ivcc term for acidic variants.
   Drug substance means compared with the manufacturing-scale qualification batches and with the set-point
   prediction at manufacturing scale: afucosylation 7.98 / 7.93 / 8.67, galactosylation 25.98 / 26.37 / 26.23,
   high mannose 5.99 / 6.45 / 6.40. For high mannose the integrated mean equals the scale-down mean (5.99).
3. Register text: Table 13.1 "S BRX OSM", "producers risk", "nor", "pcmp 001 version 2 0"; the DEV-003-04 summary
   says the attribute falls below its limit, but the predicted median is 18.39 % (only the single-batch interval falls
   below); DEV-003-06 cites "PCP-003 Table 11.1"; the PD-003-04 reason contains a function name; Table 13.2 has very
   long cells.
4. Builders: T.doe_results "Man5" for total high mannose; the Appendix A note "cO2 partial pressure" has no unit for
   153.5; T.criteria_results has no prediction limits; T.sdm_offsets puts differences and ratios in one column;
   T.model_reevaluation does not state the scale.
5. Error 6(e): PCP-003 §1, §5.4 and Table 5.3 say host cell protein and DNA are measured on the clarified harvest of
   "every"/"each" run, which read literally covers the qualification runs. §5.1 lists the qualification outputs
   without them. The record has no host cell protein or DNA on the qualification runs, the 16 augmentation runs or
   S-BRX-OSM. Not in either register.
6. The rendered PCP-003 (17:26) still states criterion d as "No run has a Cook's distance above 4/n ... 0.14 for the
   28 runs" (§7 item 3d and the changes list). It needs the owner's restatement.
7. Owner questions: the low-pH acidic-variant exact fit (one result per hold time); the DO class (KPP) against
   §2.1 (no oxygen limitation, which points to GPP); the basal medium class (GPP) against PCP-003 §4.1 (growth and
   titre effect, which points to KPP); osmolality as a WC-CPP without a PAR; the alarm limit values are not in the
   record; no action limit for acidic variants at harvest; the ivcc effect at its NOR low is not covered by the risk
   decision (the median at the worst corner would be about 17.69 %).


---

# Final pass (2026-10-11): review run 2 + owner's decisions of 2026-10-10 (record) and 2026-10-11 (bioreactor)

Inputs read: feedback-PCR-003.final.md, content-review-PCR-003.run2.md, REPORT-LESSONS §3 rule 1, §6 rule 9, §7;
data-state-2026-10-10 §3 and §5; rendered PCP-003 (08:25) and PCMP-001 (08:21), content only; A-Mab text (galactose and
CDC, p.38; DNA claimed range, p.47). Brief regenerated 08:25 (two study events, PD-003-01..13, new classes).
Backups of the run-2 parts: rev/*.pre-final.*, rev/draft.run2.qmd.

## Done (scratch parts rewritten: b1 fully, b2 by paragraph, b3 fully; setup asserts and new values)
- Record: §13 is now "Study events and discrepancies from the plan". Its opening sentence is in the record rule's
  terms. Events (DEV-003-01/02) come first, then the register and PD-003-01..13; the former DEV subsections are now
  PD-003-07..13, and every mention was updated. "Deviation" survives only in Changes item 9 and the §13 opening (the
  plan's term). PD-003-13 follows the register reason (the Version 1.0 test was stricter than the model's use needs).
- Owner's decisions 2026-10-11:
  - pH held by base addition and pCO2 by the CO2 fraction of the sparge gas (§3.2, Changes item 8, §9, §10).
  - Classes argued by the PCMP-001 §7.7 rule (osmolality CPP, DO GPP, basal medium KPP), with the conflict
    sentences deleted.
  - The ivcc corner: one significant result in 28 tests, about 1.4 expected by chance, no correction set
    afterwards. The acceptance is extended and production trending recommended (§5.4, §7.2, PD-003-11, §10).
  - Alarms at pH 6.9, 115 mmHg pCO2 and 412.5 mOsm/kg, and an action limit of 18.72 %, from D.acidic_mitigation()
    (§7.2, §10).
- Errors (Q5): D-002 elaboration corrected, the sentence itself kept. Q5.2, Q5.4, Q5.6, Q5.8 ("single run" + what
  the interval excludes, §3.5), Q5.10, Q5.11, Q5.12, Q5.15 (fitted means, slope n.s.), Q5.16 (bias 22.23/21.50,
  22.83/21.85; biased worst-corner median about 17.79 %), Q5.17, Q5.18, Q5.19 and Q5.20 (half the time at 3.1 points,
  4.3 points at 80 %) are all done.
- Q4: the bands are stated as a judgement on which no class rests; normality in the criterion's words; aggregate 11
  of 16 runs inside, stated as a limitation; the narrowing decision given its basis; "confirmed" removed.
- Tables: 5.5 "F median"; 5.12 "Fitted mean"; the Table 7.1 rounding note (6.44 rounded against 6.46) and "the
  increase applies to the upper limit only" in the text; 8.1 DNA as × 10⁻ⁿ, tails "< 0.01", dose in the note; the
  Figure 6.1 caption names the grid over the NOR; Man5 dropped and CDC added in the abbreviations; the Appendix A
  text says that Run is standard order and that run 4 is shown at its design setting.
- HCP/DNA: what was measured where is stated in §4.6, as data-state §3 gives it.

- Coordinator additions folded in:
  - temperature as a fourth alarm (dd965f8);
  - then the HOLD on alarm limits: no alarm value or rule is cited. The action limit (18.72 %, lower criterion + 2
    icIEF intermediate-precision SDs), the trending against ivcc and the release test are kept. One alarm sentence
    fits in §7.2 (last paragraph) and as a new item in §10 without restructuring. The register text PD-003-08 in
    Table 13.2 still names the alarm limits.
  - No fragments criterion is attributed to A-Mab.
- Builder change under the draft (21f0a49, criteria-table header wraps): my chunk keeps only the column widths.

## Final state (2026-10-11 09:5x)
- check_render --render passes every gate (last two runs), and a separate check_render afterwards also passes.
  Numeral lint advisory: 97 lines, all conventions.
- PDF 85 pp (82 before the pass): Table 13.2 now carries 13 discrepancies with long builder cells, and the single-run
  limits column and the required additions (action limit, tests and power, bias, ivcc acceptance, record intro)
  outweigh the cuts. Prose 770 sentences / 16,070 words (15,817 before).
- Page images read: Tables 4.3, 5.5, 5.12, 7.1, 7.2, 8.1, 13.1, 13.2, A.1 and Figure 6.1; §10.
- .txt extract refreshed. Not committed. NEEDS: none.

- 2026-10-11 ~10:10: the alarm decision was added (owner, option 1, dae4b7e), in §7.2 and §10 only.
  - The combined alert fires when culture pH is above 6.79, pCO2 above 101 mmHg and culture temperature below
    35.39 °C at the same time. The limits come from the helper, and `covers_nor` is asserted.
  - §10 item 2 carries the rule, the coverage of the NOR, osmolality under the harvest action limit, and the NOR
    read as about ±3 SD (PCMP-001 §6.4).
  - check_render --render passes; 86 pp; 777 sentences / 16,241 words; .txt refreshed; not committed.
