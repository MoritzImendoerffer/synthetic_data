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
- [ ] body part 2 (study design, results) -> scratch body2.md
- [ ] body part 3 (design space .. appendices) -> scratch body3.md
- [ ] assemble into pc_package/PCR-003_bioreactor.DRAFT.qmd (cat frontmatter + setup chunk + body1-3 + references)
- Note 2026-10-10 15:10: run was cut once; upstream changed wording only (PCMP-001 §7.5 widening = first three
  adequacy criteria; §6.2 design space on single-batch statistic). outputs/ unchanged (11:08).
- Extra finding: acidic variants fail at 9 of 81 NOR combinations (all pCO2 NOR high), not only the 4-way corner.
- [ ] draft written
- [ ] check_render passes: 0
- [ ] pdf + docx rendered, tables/figures inspected
- [ ] hand-back written
