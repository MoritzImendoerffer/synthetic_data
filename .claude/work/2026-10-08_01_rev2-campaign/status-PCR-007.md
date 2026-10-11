# Status — PCR-007 (Cation Exchange Chromatography) Version 2.0, authoring run

Author: Claude Opus 5.5 (claude-opus-5-5), one-pass, per authoring/RUNNER.md.
Draft: pc_package/PCR-007_cex.DRAFT.qmd
Scratch: /tmp/claude-1000/-home-moritz-github-repos-synthetic-data/be14bf3c-e46a-46fd-b419-65482c2add0e/scratchpad/pcr007/

## Inputs read (2026-10-11)
- [x] authoring/RUNNER.md
- [x] authoring/out/PCR-007.brief.md
- [x] authoring/section_plan.yaml (report_doe)
- [x] authoring/STORY_BIBLE.md (§9, §9b)
- [x] authoring/WRITING_GUIDE.md
- [x] authoring/REGISTER_EXEMPLAR.md
- [x] procedures/REPORT-LESSONS.md
- [x] data-state-2026-10-09b.md, data-state-2026-10-10.md
- [x] rendered PCP-007 (pdftotext, scratch PCP-007.txt)
- [x] rendered PCMP-001 (pdftotext, scratch PCMP-001.txt)
- [x] helper signatures (_pcpkg, doe_report, tables, ctable); adequacy.*/iac.verification via inspect (signatures, docstrings) only

## Decisions
- Selected models: aggregate (log, 8 terms) and HCP (log, 6 terms) meet criteria 1-3. Aggregate meets criterion 4 (flags 7, 10, 15 below F median). HCP FAILS criterion 4 on the run-order trend (p 0.043): size stated against the criterion (PD-007-02). Fragments (nrCE-SDS): no adequate model (gap 0.211), judged on measured results; no PAR, no predicted level. Yield: selected raw model, no criterion, information only.
- Deletions (flagged runs, selection repeated, doc-local with adequacy.select_model): no NOR judgement changes; HCP runs 8/13 flip the scale to raw (terms change); aggregate run 7 flips to raw. Fragment runs 4/8 would make the fragment model adequate (sensitivity only).
- Near-equivalent models (dAICc <= 2): aggregate 2, HCP 6. NOR judgement same in all. HCP: 4 of 5 alternatives exclude a small corner of the cube (design-space fraction < 1) and one (dAICc 1.82) fails the SDM qualification at the low offset end: sensitivities, selected model decides (owner decision 5).
- Screening run 9 HCP (corner 40/3/5.8/0.5) exceeds 427 at mfg scale; RSM run at same settings far lower; no systematic screening-vs-RSM difference over 16 corners. Reported as a result, design-space claim bounded.
- Stop collect raises aggregate (higher AU = earlier stop): OPPOSITE to the plan's mechanism. Reported as observed, mechanism does not explain it. Fragments direction agrees.
- Raw-scale residual SD barely grows with level (5-6 %); log choice rests on the Box-Cox profile. Stated as the data show.
- Verification uses scale-down predictions (reproduced exactly). Aggregate tightening argued by risk (PCMP-001 §7.5, four parts). HCP widening at this step (400 -> 427, AEX bound) argued by risk; it decides the SDM qualification (not qualified at 400).
- Fragments verification: model inadequate, so nothing confirmed; T.worst_case_verification prints "Confirmed" (builder issue -> hand-back), PCMP-001 §7.5 also says confirmed.
- Flow-rate study: judged with the run-to-run SD of the response-surface design (corpus precedent); alternative (duplicates' SD) stated. DNA clearance difference p 0.044 under the chosen approach.
- PAR table shown for aggregate and HCP only (fragments have no adequate model); PAR plots: aggregate vs load; HCP vs load AND conductivity (equal within SE; D.governing_factor names conductivity from the screening -> hand-back).

## Progress
- [x] setup chunk and data checks (all deciding words asserted)
- [x] body written (one pass, report_doe order)
- [x] check_render: 8 runs. Pass 1 failed (unresolved @tbl-resid), pass 2 failed (font floor, 4 tables), pass 3 failed (font floor, adjacent superscript markers in T.criteria_results), passes 4 to 8 exit 0 (the last after the final explicit renders)
- [x] pdf + docx rendered (quarto, venv on PATH): 70 pp
- [x] every complex table and figure inspected (pdftoppm, 110 dpi); no table called wrongly
- Body as check_render counts it: 759 sentences, 15,008 words of prose. No <<NEEDS:>>.
- Not run: check_style --review, check_discourse, measure_*, any sentence counter. The advisory numeral lint was also read directly (ema_docgen/scripts/lint_numerals.py): every flagged numeral is an identifier or a convention.

## Hand-back items
Departures from PCP-007 in neither register:
- Load aggregate and load host cell protein not measured on any designed run (PCP-007 §5.4 and §12). The clearance factors rest on the nominal load of the process model.
- Residual DNA and leached Protein A not measured on the screening runs (§5.4, §4.2).
- No flow-through, wash or strip result, so no host cell protein mass balance and no strip test (§5.4).
- Packing tests before each campaign (§5.1) not in the record. Plate count and asymmetry exist for the qualification runs only.
- S-CEX-FRC is work PCP-007 did not foresee.
- The approaches stated in §3.5.1 for the seven decisions without a threshold (PCP-007 §7 intro and §8). REPORT-LESSONS §3 rule 2 would record them as discrepancies.
NOR: no change argued; every output meets its criterion over the NOR with margin, and every PAR is the range studied.
Class question: elution flow rate GPP. DNA clearance is 0.32 log10 lower at 300 cm/hr (p 0.044 with the design SD). Yield is 1.6 points lower (p 0.030 with the duplicates' SD only, 0.369 with the design SD).
Helpers and data:
- D.governing_factor reads the screening model: for HCP it names conductivity, while the selected RSM model has load largest (equal within SE). Both are plotted.
- T.worst_case_verification prints "Confirmed" for fragments on a model that fails §7.2, and PCMP-001 §7.5 says the same.
- D.design_space_grid returns a binding response when nothing binds.
- D.par_table gives fragments a PAR from measured results (rows excluded in the report).
- T.method_comparability and T.model_reevaluation print hyphen minus signs.
- T.criteria_results is too wide in portrait, and its adjacent header markers trip the font floor; landscape and normalsize set on the object.
- capability.csv rounds the residual DNA SD to 0. Mean and SD taken from monte_carlo.csv.
- iac.verification uses scale-down predictions without the offset. HCP at the low end of its offset CI gives 28.1 < 40.
- The stop collect raises aggregate with the AU setting, opposite to the mechanism and PCP-007 §4.1, and has no yield effect: check the sign convention.
- DEV-007-02 record has no units for tmax and duration; °C and min were written.
- Builder labels: "load/Wash", "Pool HCP".

## Fix pass 1 (2026-10-11, same author)
Inputs: feedback-PCR-007.run1.md, factual-PCR-007.md, data-state-2026-10-11.md, REPORT-LESSONS §3, §6, §7, brief regenerated
(authoring/build_brief.py PCR-007), rendered PCMP-001 and PCP-007 re-extracted (pdftotext). Backup of the run-1 draft:
scratchpad pcr007/PCR-007_cex.DRAFT.pre-fix1.qmd. Config, helpers and annex untouched.

- A. Record: PD-007-05 to -11 described in new §13.2.5 to §13.2.11 and cited where the text relies on them (§3.2 operation,
  §3.3 analytical, §3.4 sampling, §3.5 statistics and §3.5.1 items 2, 4, 6, §8, Discussion, exec summary). "Not recorded"
  used; Version 1.0's claims (load, flow-through, wash assayed; column released) stated "with no result recorded"
  (Changes item 7, §3.4, PD-007-05, -07, -08).
- B. Verification with the offset at its estimate (evaluate() now applies it; reproduces iac_verification to 1e-3).
  Sensitivity to the offset ends computed (HCP 28.1 / 57.6, bounds 23.0 / 47.1; aggregate 1.40 / 1.78). Pool aggregate
  criterion 4.90 % with the UF/DF allowance 0.104 (asserted = DS − allowance), stated in §1.1, §7.1, the risk argument,
  §8, §10, exec summary, Changes item 1. Fragments: one verdict, confirmed by PCP-007 §7.6 with the §7.2 limitation.
- C. Stop collect: data as observed, no cause; yield "has no stop-collect term". Elution flow rate GPP argued as a named
  judgement (0.32 log10, p 0.044, factor 2.1 / 1.45 over the NOR; DS 0.00017 → 0.00036 ng/dose, Cpk 7.30 → 2.67);
  yield interval includes the load effect; PCMP-001 §7.7 quoted with "practically relevant" and the too-small clause.
- D. E3 (99.85 % at the a priori criterion, 22 points), E4 (drift: region max 408 → 461, 1.13 % of grid; qualification
  414 → 467 > 418; "does not depend on the trend" limited to the NOR), E5 (per response), E7 (objectives quoted, 2 and 3
  amended), E8, E9 (run 6 / run 14 effects named; yield stop collect tested in full quadratic p 0.239 and screening
  p 0.268; run 14 deleted gives −0.76 points/coded unit, p 0.078), E10 (curvature −0.092 < centre SD 0.144, not
  claimed), E12 (window and Table 3.2), E13 all items.
- New sensitivity found while re-reading the data: with the offset now in the verification, 3 of the 5 near-equivalent
  HCP models give a lowest fold below 40 (38.8 to 39.5) and 3 fail the qualification at 418 (up to 432 ng/mg); stated
  in §5.3.4, §7.4, Discussion, exec summary. Selected model decides.
- Gates: check_render --render x4 (pass 1 failed on the font floor in tbl-near, fixed by dropping its Terms column;
  passes 2 to 4 exit 0), explicit quarto render pdf and docx exit 0, check_render once more exit 0. 80 pp.
  Tables inspected as page images: 1.2, 3.2, 5.9, 5.10, 7.2. No <<NEEDS:>>. DRAFT.txt refreshed.
