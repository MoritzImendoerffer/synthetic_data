# PCR-005 status, 2026-10-10 (record pass after the owner's decision on deviations, complete; see §6)

Draft: `pc_package/PCR-005_protein_a.DRAFT.qmd`. Nothing committed. No shared code changed in the run-3 cycle or in this follow-up.

## 1. What changed

**Run-3 cycle (feedback-PCR-005.run3.md, A, B and C): complete in the prose.**

- **A, the log scale and the search.** §3.5 is rewritten to STORY_BIBLE §9b, with this campaign's data:
  - the model on both scales, with ε as the run-to-run error;
  - the fold changes;
  - the reasons the effects are fold changes: purification removes a share, and ELISA precision is 9.5 % of the level;
  - the named least-squares assumption, with the raw and log RMS in the lower and upper half of the predictions, and Box-Cox λ;
  - the implications, including the asymmetric interval 7,150 (5,687–8,989);
  - the search in order: 1,337 candidates, stepwise searches worse for 12 of 21 outputs, and how CA2 differs.
- **B, factual check 2.** PD-005-02 wording; a column per criterion in Table 5.7; design space on medians; "an intercept and 14 terms"; the executive summary sentence; the 28-run basis of the anion exchange bound; 1.515 and 0.535; the remaining notes.
- **C, review run 3.**
  - Hold judged on criterion 7, with the lower-limit rows referred to PCR-003; one set-point eluate.
  - The CPP classes named.
  - The interaction: Table 5.10 lists the 9 models within 2 AICc units.
  - Figure 5.1 sentence; the leverage claims replaced by a Cook's distance simulation; the trends judged per test, with their sizes.
  - Fragments without an offset; the titre method SOP-3016 / AMV-3021.
  - The widened-criterion rule; the univariate claims limited to the attributes measured; DEV-005-02 with both results and the sensitivity analysis.
  - All Q1–Q7 sentences.
  - Tables: fragments row in 5.1; notes on 5.5, 5.6 and 7.2; ANOVA precision; reference runs in 5.15; Table 7.3 header; capability table with residual DNA; Tables A.2 and B.2 with run order, HMW, DNA and pH as analysed; titre row in D.1.

**Follow-up for the single-batch rule and the narrowed load NOR: only the setup chunk is done.** Every assert that encoded the old numbers is replaced, and the new facts are computed and asserted:
- the cation exchange platform value stands, and the anion exchange single-batch bound widens the criterion to 17,069;
- over the load NOR as characterized (20–40) the scale-down model is not qualified, with the ratio at its low end giving 17,143. The limit reaches the criterion at a load edge of 39.8;
- at the NOR in force (20–39) it is qualified (16,763), and on the 3 planned runs alone it is not (18,786);
- design space:
  - no excluded point lies inside both the load NOR and the pH NOR;
  - with flow and end of pool collect at their set-points, the corner beyond 42.4 g/L at pH 3.2, or below pH 3.30 at 50 g/L, is excluded;
- one NOR-propagated PAR narrows: elution buffer pH for pool HCP, 3.21–3.9 (3.25–3.9 without CA3);
- CA3 decides the qualification and that PAR. The ca3 sensitivity table records no difference in the conclusion over the NOR;
- of the 9 near-AICc models, 2 (A, B, D and A, B, D, AB) would not qualify the model at the low end of the offset (17,485 and 17,293);
- the risk values: CEX criterion 426.7, a pool at the criterion cleared at both single-batch bounds gives 109 ng/mg, HCP LOQ 1.0, no batch out of specification;
- the low-pH platform hold is 180 min against at most 120 min in the A-Mab NOR;
- the new hold criterion is ≤ 6.46 %.

## 2. What is verified

- `check_render --render`, run once at 14:06 on the current file, passed:
  - all 53 chunks execute and all 686 inline expressions evaluate;
  - style gate at 0;
  - docx and pdf render;
  - all cross-references resolved;
  - 29 complex tables complete, no missing glyphs, no text below 7.9 pt.
- **PDF: 73 pages.**
- A probe that makes every setup assert non-fatal found 0 failing asserts on the data of commit 0b452c9.
- **Not verified:** the prose was not re-read against the new numbers. Several sentences are now wrong (section 3 below).

## 2b. Follow-up pass 2 (fresh author, 2026-10-09 evening), COMPLETE

All items of the old section 3 are now written in the prose (each against the setup chunk; new asserts
appended at the end of the setup chunk, none removed or weakened):
- exec summary F1 and F7 rewritten (load NOR decision, single-batch widening and its risk, pH PAR exception);
  F2/F3/F5/F8/F9 and the closing paragraphs trimmed; the PAR paragraph dropped as a restatement;
- §1.4 criterion paragraph ("anion exchange widened it"); new change item 7 (the NOR narrowing); item 3
  prints `nor_load_c`; the "no NOR changed" sentence is gone;
- §3.1 the NOR decision (17,143 at 20–40; boundary 39.8; 16,763 at 20–39) and the four things the
  qualification rests on (criterion and CA3, the NOR, the 6 runs, the model choice);
- §4.5 single-batch bounds, 5 × 1.404 − 0.559 = 6.46, and the low-pH reason made attribute-specific per the
  coordinator's canon correction: aggregate smaller because the hold is shorter (observed_edge 0.84 > 0.70
  at the 180-min edge, asserted); acidic variants smaller even over the same 180 min (0.60 < 1.00, asserted);
- Table 4.1 note on the load NOR; Table 5.10 has a "Scale-down model qualified" column (2 No);
- §5.3.1 near-model conclusion (2 of 9 fail at the low end, named in words); §6 design space rewritten;
- §7.1 rule, three reasons, CEX stands, AEX widens (bound, runs, adequacy, why known well enough), the
  four-part risk argument, the CA3 dependence, the fragment paragraph (neither bound beats its platform value),
  the aggregate paragraph now points to §4.5;
- §7.2/§7.3 (pH PAR 3.21–3.9, 0.009 inside the range, margins 0.19 and 0.34); §9 criterion 8 identifies
  elution buffer pH, load bullet gives the NOR and its reason, the flow corner sentence dropped;
- §10 items 1 and 5; Discussion and Conclusions rewritten; PD-005-01 the opposite outcome (18,786) with
  optional stopping as a limitation; PD-005-02 to 04 trimmed;
- §5.7: the PCR-003 sentence now says producer's risk with pH, pCO2 and osmolality alarm limits (canon 6a).
- Two tables were edited so that check_render's table probe still matches them (arguments precomputed).
Gate: check_render --render pass 1 green at 72 pp (before the length cuts). Length cuts round 1 applied
(restatements in the summary, §2, §3.5.3, §4, §5.2/5.3/5.6/5.7/5.8, §8, §13); pass 2 running.

## 2c. Data-state pass (data-state-2026-10-09b.md and the revised PCP-005), COMPLETE

Eight setup asserts failed on the new data, as they should; each was corrected to the new fact (none dropped):
- `PDS` has five entries (PD-005-05, the hold study S-PA-HLD, made 2026-09-19 to 09-28, after INV-001 closed
  and after AMD-001; asserted). The characterization window now excludes both re-analysis studies.
- Bioreactor acidic-variant upper limit back at its a priori value (39.0); the low-pH acidic-variant model is
  an exact fit, status "none", not adequate, so its bound does not replace the platform value (asserted).
- Hold data: acidic variants rose by the same 0.3 points at both temperatures; fragments rose faster at 21 °C
  (0.25 against 0.08, difference above the day-0 aliquot difference); nrCE-SDS on every sample, no SEC.
Text changed: F9; objectives (hold item removed, a sentence says the hold was not a PCP-005 objective);
§1.4 items 5 and 8; §3.3 (hold study measured fragments by nrCE-SDS alone); §4.5 rewritten (study as
PD-005-05, every time point by nrCE-SDS, the report's own hold rule because no plan states one, aggregate-only
low-pH reason, acidic criterion at its a priori value with one sentence on why the bound does not replace it);
§5.7 results and Table 5.17 caption and notes; Conclusion 9; new §13 subsection PD-005-05 (`#sec-pd05`);
"criterion 7/8" plan numbers removed (the revised PCP-005 may renumber); the bioreactor parameter names are
now computed (`lc()` keeps "CO2 partial pressure (pCO2)" capitalised; `alarm_txt`). New asserts: the low-pH
aggregate model has no pH term and the hold-time and temperature NORs in force end where characterized.
Then, after PCP-005 was revised (no hold study, no hold criterion, objectives 1-6, criteria 1-7 with
classification = 7): the held eluate is judged against the criteria of the low-pH inactivation load (asserted
from `D.iac_table`: low-pH output criterion less that step's credited increase = 6.46 % aggregate, 39 % acidic
upper limit, 2.45 % fragments), and the report says the plan set no hold criterion because it foresaw no hold
study; the hold rule is the report's own and part of PD-005-05. "Criterion 7/8" for the hold or classification
removed; classification cited once as criterion 7. Every other PCP-005 reference (§2, §4.1, §5.1, §5.5, §6.2,
§6.4, §7 criteria 1-5, §8.1, §8.2) checked against the new PDF. Acidic variants changed over the hold by less
than the day-0 aliquot difference; the text now says so (asserted). Conclusion 1 no longer puts the hold study
under PCP-005. PD-005-02 to 04 are named in the discrepancy intro (the register carries their details);
PD-005-01 and PD-005-05 keep subsections.
check_render --render passes 11-15 all green (69, 68, 69, 68, 67 pages). Final: **67 pages**.

## 2d. Factual check run 3 fix pass (factual-PCR-005.run3.md), COMPLETE

- Objectives quoted as the revised PCP-005 §2 words them (objective 1 "before the first characterization
  run", objective 6 without the added clause).
- F9 and Conclusion 9: what the hold added kept the three attributes within the UPPER limits of the low-pH
  inactivation load (deciding word `hold_rule_word`, computed from `h_ok` and the acidic fall); the lower
  limit is not claimed; acidic variants can enter below it (PCR-003).
- PD-005-06 (loaded mass from the titre, not A280): `PDS` asserts six entries; named in §3.3 (`#sec-methods`)
  and in the §13 discrepancy intro with its reason.
- §2.2 leached Protein A counted unrounded with the strict comparison: 4 of 47, the lowest at 5.002 ppm.
- §8: "does not lower acidic variants" in place of "raises slightly".
- §5.7: 2-8 °C fragment change unrounded, 0.084 against 0.081, "about the same as" (computed word).
- Notes: "at most 3.1 %" (f1); the two unsourced execution statements removed ("same laboratory columns",
  "same procedures"); the brief's SOP/AMV subset omits SOP-3015, SOP-3016, AMV-3013, AMV-3019, which the
  document adds deliberately and cites (brief/helper issue, document unchanged).
- Table 7.1 note b) now renders the exact-fit wording.
- Conclusions trimmed (step-yield restatement, univariate wording, LPA sentence, fragment-offset sentence)
  to keep the chapter on one page. check_render --render passes 16-19 green; final 67 pages.

## 3. What is left

Nothing in this pass. Final check_render --render (pass 15 of this session's count): all chunks exec, 677
inline expressions, no <<NEEDS:>>; style gate 0; docx and pdf render; all cross-references resolved and no
inline source printed; 29 complex tables complete; no index-cell repeats; no text below 7.9 pt. PDF: 67 pages.

Next (coordinator): factual pass on the follow-up and data-state text, then promote and re-anchor
`build_report_protein_a`.

For the owner/coordinator:
- The coordinator's note says the held-eluate criteria are "a priori by the master plan's rule". The report
  uses the criteria IN FORCE for the low-pH inactivation load (aggregate 6.46 %, tightened and widened on
  verification; the a priori value would be 9.30 %), as for every other judgement. Confirm that is intended.
- `T.worst_case_verification` note b) says the low-pH acidic model "fails an adequacy test"; for an exact fit
  the data-state says PCMP-001 §7.2 cannot be applied. PCR-005 §7.1 words it as "cannot be judged adequate".
- No ELISA coverage figure in the record (§7.1 says so); the pool HCP qualification rests on the narrowed NOR,
  the 6 added runs (optional stopping) and the model choice (2 of 9 near-AICc models would not qualify).

## 3-old. The list the previous author left (all done in pass 2, kept for the record)


The numbers render from the data, but these sentences still state the old facts and must be rewritten.

- **§3.1:** the qualification paragraphs. Add the load NOR decision with its reason (17,143 > 17,069 at 20–40; boundary 39.8; 16,763 at 20–39). List what the qualification rests on: the widening, the narrowed NOR, the 6 supplementary runs, and the model choice.
- **§1.4:** the criterion paragraph and the change items. Add the NOR narrowing. The Version 1.0 PAR sentence must print `nor_load_c` (20–40), not the NOR in force.
- **§4.5:** the hold-criterion derivation is now 5 × 1.404 − 0.559 = 6.46. Add the sentence that the low-pH value replaced a 180-min platform hold with at most 120 min, a shorter hold, not a more stable product (`vi_plat_min`, `vi_hold_max`).
- **§5.3.1:** the near-model conclusion. Two models fail at the low end of the offset (`near_fail_txt`, `near_fail_lo_txt`).
- **§6 design space:** the "whole region meets" sentence. Rewrite with `ds2_sp`, `ds_b_load`, `ds_b_ph`, `ds_nor_load_min`, `ds_nor_ph_max`, `ds_load_min`, `ds_ph_max`.
- **§7.1:**
  - The rule, stated exactly: a single-batch bound, with the owner's three reasons.
  - Cation exchange: the platform value stands. Anion exchange: the bound of 4.27.
  - The risk argument: producer's risk, ELISA release test (LOQ `hcp_loq`; no coverage figure exists in the record), what cation exchange and anion exchange must clear (`cex_req`, `aex_req`, `crit_cex_hcp`, `ds_at_bounds`), and `hcp_n_oos` / `hcp_ppm`.
  - The dependence on CA3 (`par_ph_wo`).
  - The fragment paragraph: neither bound now beats its platform value.
  - Remove the aggregate paragraph or point it to §4.5.
- **§7.3:** "every PAR spans its range studied". The exception is `par_ph_hcp`, with margins `par_ph_margin` and `par_ph_sp_margin`. Also the corner sentence: the median now exceeds the criterion at the corner even with flow and end of pool collect at their set-points.
- **§9:** criterion 8 now identifies elution buffer pH. The protein load bullet needs the NOR in force and its reason. Drop the load flow rate corner sentence.
- **§10:** item 1 (NOR in force) and item 5 (the requirements on cation exchange and anion exchange).
- **Discussion, Conclusions 2, 5 and 7, executive summary F1, F7 and the PAR paragraph.**
- **PD-005-01:** now the opposite outcome. Not qualified on the 3 planned runs (18,786). The 6 runs made the qualification possible. Optional stopping as a limitation. The old "did not change the qualification" text must go.
- **Table 4.1:** add a note that the load NOR was narrowed from 20–40.
- **Length:** 73 pages against the target of well below 70. Cut restatements in the executive summary, §1.4, §2.1, the Results text (hold values, screening and univariate restatements), the Discussion and §13.
- **Then:** gate and render again, and inspect Tables 5.10, 7.1 and 7.3 and the design-space text.
- **For the owner (carried over):**
  - builder issues in `criteria_change`, `sdm_offsets`, `model_reevaluation`, `hold_stability`, `worst_case_verification`, `criteria_results` and `doe_results`;
  - the `_tables.tex` numbering bug;
  - registry titles; the revision history omits CA3;
  - `D.governing_factor` returns load for fragments;
  - the DEV-005-02 record has no out-of-trend limit;
  - the GPP class of temperature and bed height does not cover fragments;
  - six step-yield results at 99.0 %;
  - the residual DNA criterion of ≤ 0.001 ng/dose;
  - no ELISA coverage figure in the record;
  - new: the qualification depends on the choice among near-AICc models.

## 4. Re-opened 2026-10-10 (data state of 2026-10-10, fix list `feedback-PCR-005.datastate-2026-10-10.md`)

Author for this pass: Claude Opus 5.5 (model id claude-opus-5-5). Backup before any edit:
`PCR-005_protein_a.pre-datastate.qmd` (this folder). Nothing committed. No shared module, config or engine
file edited. Scratch work in the session scratchpad (`pcr005/`).

**Start.** The setup chunk stopped on three asserts: the design-space fraction (recomputed on the mean),
DEV-005-02 with the first result in place (the selection now gives an adequate, significant model), and the
first result "inside the range of the other runs" (it is now above it).

**Fix list, item by item** (sections as numbered in the rendered PDF):
1. Design space on the single-batch limit: §6 rewritten. The setup block "design space, on the single-batch
   limit" takes `D.design_space_grid(UO, n=41)` (basis "batch", 90.2 % of the grid) and checks it
   independently through `D.prediction_interval` at manufacturing scale for all three outputs with a
   criterion. Fragments are judged too, because the helper's response list leaves them out. They exclude no
   point, and neither does leached Protein A. The mean-based region (97.5 %) is given once, named as a
   comparison. Plane at the set-points of flow and end of pool collect: 91.7 %. At their NOR corners
   88.5–92.8 %, at their range corners 81.4–91.9 %. The corner is excluded above 31.8 g/L resin at pH 3.2
   and below pH 3.44 at 50 g/L resin. It reaches into each NOR but never into both: at the load NOR edge
   (39) it begins below pH 3.29, at the pH NOR edge (3.4) above 47.2 g/L. No grid point is excluded with
   every factor in its NOR. With flow and end of pool collect in their NORs, each excluded point lies outside
   the load NOR or the pH NOR. Inside both, a point is excluded only with flow ≤ 105 cm/hr and end of pool
   collect ≤ 2.09 CV, both below their NORs. The old mean-based asserts are replaced. The statistic is
   restated in F7, §3.5, §5.8, §7.3 (corner sentence) and Conclusion 6.
2. DEV-005-02: §13.2. The rule is quoted from `deviations.csv` `oot_rule`, and its 99 % level is asserted
   against `dev_005_02_oot_level`. `D.oot_check` gives 1.38–5.12 ppm (scale-down) from the model selected
   on the other 27 runs, which keeps end of pool collect. The first result, 5.31 ppm (2.5 × the re-assay),
   lies outside the interval and above the other runs (1.70–4.61). The re-assay, 2.12 ppm, lies inside
   both. The analysis was recomputed with the first result in place: the selection keeps end of pool
   collect, adequate and significant (F-test p 0.034, lack of fit p 0.844, gap 0.136), −0.77 ppm across the
   range. The limit over the NOR is 5.98 ppm against 5.52 ppm on the re-assay, and every PAR still spans the
   range studied. The run-order trend is not significant (p 0.174). The judgement and the class of end of
   pool collect are unchanged. The §5.3.3 sentence follows.
3. Detection of host cell protein: §7.1, risk item 2. The release test is the ELISA (AMV-3012), its LOQ
   1 ng/mg, its coverage 80 % by 2D western blot against the platform CHO antigen (`amv_3012_coverage`,
   `dev_methods.csv`), and the report states what lies outside that share. The abbreviations 2D and CHO
   were added.
4. Residual DNA: §2.2 (pg/mg measured, ng/dose judged) and §8. The dose is 10 mg/kg (A-Mab) for a 70 kg
   adult, 700 mg (`DOSE_MG`), and the body weight is stated as an assumption. The drug substance carries at
   most 0.0004 ng/dose against ≤ 0.001, a Cpk of 7.30 (`capability.csv`, recomputed by the engine), with no
   batch out of specification (asserted). The anion exchange reduction is a nominal 5 log. Every anion
   exchange pool is below the qPCR LOQ (1 pg/mg), so the data show only more than 1.2–1.5 log10, and the
   Cpk rests on an unmeasured reduction (said).
5. Univariate SEC results: §4.4 (the responses PCP-005 Version 1.0 required; nrCE-SDS not measured
   because the samples were not retained, so S-PA-RET covered the retained response-surface pools). §3.3
   (S-PA-UNI fragments by SEC only). §5.6: Table 5.15 gains HMW and LMW by SEC, with n.t. for the reference
   runs. A new paragraph gives aggregate 1.49–1.60 % (inside the designs' range, below ≤ 6.46 %) and
   fragments by SEC 1.24–1.42 % for information only, with no difference because the reference was not
   tested by SEC. No nrCE-SDS fragment result is claimed. §9: for fragments the GPP classes of temperature
   and bed height rest on the mechanism and the response-surface model. For temperature: hydrolysis is
   expected faster when warm, the pH effect is 0.11 points over the whole pH range, the margin is 1.36
   points, and the assumption is untested. For bed height: no flow effect was detected over residence
   times of 4–12 min, and the 3 min of the shortest bed is unsupported. F10 and the Discussion say
   "not measured by nrCE-SDS".
6. Near-equivalent models: §3.1 item 4, §5.3.1, F1, the Discussion and Conclusion 2. The selected model
   decides, as the selection rule states. The others are a sensitivity, and 2 of the 9 would not qualify
   the scale-down model.
7. Criterion 5 by `D.residual_influence`: the setup takes every criterion-5 result from the helper. Its
   exact agreement with the document's own computation was asserted (rtol 1e-12) and gated (dry run)
   before the own computation was removed. The thresholds come from `THRESHOLDS` (`residual_alpha`,
   `cook_factor`/n) in §3.5, Table 5.13 header and note, §5.5 and §13.1, and the Cook's distance simulation
   uses `cook_factor`. The deletion analysis (PD-005-02) is unchanged.
8. Held pools: §4.5 now says that the held eluate is judged against the criteria in force for the low-pH
   load (PCMP-001 §7.3 after the verification of §7.5), not the a priori values.

**Length.** The first render was 72 pp. Four of the five added pages were chapter ends spilling by 2–10
lines. Only my own new text was tightened (F1, F7, F10, §6, the Discussion sentence, §13.2: one merged
sentence, two redundant clauses dropped). The deviations chapter stays one page longer: §13.2 grew by the
rule and its numbers.

**Gate** (`check_render.py`, run with `.venv/bin/python` because `uv run` once tried a network sync of the
optional discourse extra; same venv):
- dry run 1: all 53 chunks exec, no `<<NEEDS:>>`, style gate 0;
- `--render` pass 1: green, 72 pp;
- explicit quarto pdf and docx;
- `--render` pass 2: green, 71 pp, colon 0.1/1k from one new sentence, fixed;
- `--render` pass 3: green, 69 pp, 29 complex tables complete, no page-foot overrun, nothing below 7.9 pt;
- final explicit `quarto render --to pdf` and `--to docx` (venv on PATH): both exit 0;
- final `check_render.py`: green (724 inline expressions, no `<<NEEDS:>>`, all PDF checks OK). **69 pages.**

Page images read: Abbreviations (p. 5), Tables 5.13, 5.14 and 5.15 (pp. 38–40). Text pages read: §6 (p. 44)
and §13.2 (pp. 59–60). No figure changed.

**For the coordinator:**
- PCMP-001 §7.5, as re-rendered today (12:25), requires the first three adequacy criteria for a widening (a
  significant model, no significant lack of fit, the limit on overfitting) and no exact fit. PCR-005 §7.1
  still paraphrases the rule as "the adequacy tests of PCMP-001 §7.2 on lack of fit and predictive power",
  and its anion exchange sentence names only the gap and the lack of fit. The data are fine: the anion
  exchange HCP model behind the widening has F-test p = 2.7e-13 on the planned runs and is not exact, so
  the criterion stands. This is wording only, and it was not changed because it is outside this fix list.
- `D.design_space_grid` loops over `D.responses(key)`, which for Protein A lacks `lmw_cesds_pct`, so the
  helper ignores fragments. PCR-005 checks them itself, and they exclude nothing here. Other steps may be
  affected.
- PCP-005 Version 2.0 §6.4 and Table 5.1 list only pool HCP, step yield and leached Protein A for S-PA-UNI
  and say "Fragments are not measured in the univariate study". The data now hold SEC aggregate and SEC
  fragments for it, as Version 1.0 required. PCR-005 cites Version 1.0 for this.
- The DEV-005-02 `oot_rule` names "the selected model of the design", yet model selection (CA3) was adopted
  on 2026-09-15 and the review was made when S-PA-RSM ran (2026-01-12 to 2026-02-06). PCR-005 states the
  rule as recorded and computes the interval with `D.oot_check`. The record's wording may need a look.
- The 30-day sample retention exists only as a config comment. PCR-005 says "not retained", with no number.
- The drug substance DNA capability rests on the nominal 5-log anion exchange reduction, which the anion
  exchange data cannot measure (pools < LOQ, more than 1.2–1.5 log10 only). PCR-005 says so. PCR-008 and
  PCMR-001 may need the same.
- The annex `ground_truth/PCR-005.json` (2026-10-09) quotes text that changed in §2.2, §3.1, §3.3, §3.5,
  §4.4, §4.5, §5.3, §5.5, §5.6, §6, §7.1, §7.3, §8, §9, §11, §12 and §13. `build_report_protein_a`
  needs re-anchoring before promotion. Not done here.

## 5. Follow-up 2026-10-10 afternoon (`feedback-PCR-005.followup-2026-10-10.md`)

Author: Claude Opus 5.5. Backup before this pass: `PCR-005_protein_a.pre-followup.qmd` (this folder).
Edited in place, nothing committed, the annex left to the coordinator. Only the five items were touched. The
setup chunk stopped on three asserts: the deviation count (DEV-005-03 is new), and the two DEV-005-02 asserts
on selected models.

1. DEV-005-02 (§13.2). The rule is now the record's: the full quadratic model fitted to the other runs. The
   setup asserts the record text and the 99 % level, checks that `D.oot_check` uses the full quadratic, and
   asserts that selection (2026-09-15) came after S-PA-RSM ended. The interval is −1.46 to 5.38 ppm on 12
   residual df. The text says its lower end lies below zero, so only a high result could be out of trend at
   run 11. The first result is 6.37 ppm (3.0 × the re-assay, 7.55 ppm at manufacturing scale), above the
   interval and above every other result of both designs (asserted against both). The re-assay, 2.12 ppm,
   lies inside the interval and the range of the other runs. With the first result in place the selection
   takes the log scale and keeps end of pool collect. The model meets criteria 2 to 4: F-test p printed as
   0.0495, because three decimals would read 0.050; lack of fit p 0.894; gap 0.137. Leached Protein A falls
   22 % across the range of end of pool collect. The limit over the NOR is 6.60 ppm, back-transformed,
   against 5.52 ppm on the re-assay, and every PAR still spans the range. The run-order trend is not
   significant (p 0.198). The judgement and the class do not change.
2. The widening rule (§7.1). It is stated as PCMP-001 §7.5 rule 2: the first three criteria, not an exact
   fit, the fourth not deciding, and the report giving the bound examines whether it depends on a single
   run. The anion exchange paragraph now gives the F-test (p < 0.001), the lack of fit (0.824), the gap
   (0.02 against 0.20) and no exact fit. It says the fourth criterion fails on Cook's distance (runs 2 and
   9, trends met) and that, with each run deleted, the model still meets the three criteria and the bound
   is 4.33–4.56 against 4 (INV-002 §8.4). These values are computed in the setup by reproducing the
   verification bound (asserted equal to the table, 4.2673) and `D.residual_influence("aex", ...,
   runs="planned")`. The CA3 sentence now names the failing test (overfitting, gap 0.27). The phrase
   "passes the adequacy tests" is gone.
3. DEV-005-03 (new §13.3). Also recorded in §4.4 (merged into the reference sentence), §5.6 (why the
   qualification runs are the reference; the step-yield sentence cross-referenced), the Discussion,
   change item 10 in §1.4, and the executive summary deviation sentence ("DEV-005-01 to DEV-005-03", "none
   changes"). The §13 introduction now defines a deviation as a departure from the approved plan,
   procedure or GMP requirement, and says "each was investigated". The setup asserts three deviations, the
   DEV-005-03 record and the absence of any centre level in `univariate_studies.csv`. §4.4 now cites
   PCP-005 §6.4 for the responses ("as PCP-005 §6.4 requires"), as restored.
4. Builders. The design-space assert now includes fragments in `per_response` (0 excluded), and the stale
   comment is gone. `T.criteria_results` has no no-model note here, because every output has an adequate
   model. The true minus signs, the font floor and the table fit were checked on the render.
5. Annex: not touched.
6. DEV-005-04 (added by the coordinator during the pass): new §13.4. It is also recorded in §3.1 beside the
   offsets table, in change item 10 of §1.4 (merged with DEV-005-03 to keep the chapter on its pages), in the executive summary deviation sentence ("DEV-005-01 to
   DEV-005-04 were assessed, and none changes the judgement"), in the §13 introduction (the runs of
   DEV-005-01 to -03 retained, DEV-005-04 judged through its offset) and in Conclusion 11. The p-value is
   computed in the setup from `sdm_qualification.csv`, S-PA-SDM runs only (3 scale-down against 5
   manufacturing), with a two-sided pooled t test: p = 0.037. The setup asserts that no other compared output
   differs at that level (pool HCP 0.43, yield 0.68, plates 0.12, asymmetry 0.96) and that leached Protein A
   is qualified through its offset on the planned runs and on all runs. The offset analysis is unchanged.
7. Classification (from the re-open of PCP-005): §9 rewritten without the removed PCP-005 rule ("practically
   relevant when the NOR-propagated PAR is narrower than its range studied"). It now applies PCMP-001 §6.2 (an
   attribute is affected when a term containing the parameter is significant at α 0.05) and §7.7 (a
   significant effect too small to move the attribute appreciably within the PAR does not by itself make a
   parameter critical; no numerical threshold), as PCP-005 §7 criterion 7 applies them. Each bullet gives:
   - its significant terms with p, computed from the selected models (`AFF`, `termp`);
   - the change of pool HCP across the NOR-propagated PAR, others at set-point, manufacturing scale, in ng/mg
     and as a share of the criterion (`CLE`): load 38 %, pH 52 %, flow 6 %, end of pool collect 7 %;
   - fragments on pH: 0.11 points, 4 % of the criterion;
   - yield: end of pool collect 7.3 points; flow 3.6 points at 50 g/L, about 0 at 10 g/L;
   - the margin of the PAR to the NOR: load 10/11 g/L, pH 0.19/0.20, flow 50/50 cm/hr, end of pool collect
     0.3/0.3 CV, temperature 3/4 °C, bed height 5/5 cm;
   - the reason for the class.
   The DEV-005-01 buffer (pH 3.38) lay below the NOR and inside the PAR (asserted). The DEV-005-02 class
   sentence now uses the size of the effect (0.74 ppm against ≤ 158 ppm), not the removed rule. Every class of
   the config is supported. The KPP classes of load flow rate and end of pool collect rest on judging their
   significant effects on pool HCP (C² p 0.025; D p 0.003) as too small, at 6 % and 7 % of the criterion
   across the PAR, which is a judgement with no threshold.
8. DEV-005-05 (univariate study before the response-surface design, against PCP-005 §11): new §13.5. It is
   also in §4.1 at the chronology (the order of PCP-005 §11 and the departure), in §1.4 item 10, in the
   executive summary ("DEV-005-01 to DEV-005-05") and in the §13 introduction (its runs retained). The dates
   come from `study_chronology.csv`, and S-PA-SCR end < S-PA-UNI < S-PA-RSM start is asserted.
9. Objectives (from the last re-open of PCP-005): §1.2 now quotes the seven objectives of the re-rendered
   PCP-005 §2 word for word. Only the plan's internal references are written as "PCP-005 §6.1" and "PCP-005
   §5.1". The plan's note is carried in one sentence: objectives 1 to 5 are Version 1.0's, 6 and 7 were added
   at Version 2.0, fragments were added to 1 and 3, and the ranges of 3 are at manufacturing scale. One
   sentence names the section that answers each objective (1: §5.3 and §5.6; 2: §6; 3: §7; 4: §9; 5: §7 and
   §10; 6: §3.1; 7: §5.3). No other part of the report numbers an objective.
10. Owner's decision "4/n flags, F decides" (data-state §5). §3.5 criterion 5: a run above 4/n is examined by
   deleting it and repeating the judgement, and the model fails only above the median of F(p, n − p), worded
   from `THRESHOLDS["cook_f_quantile"]`. The §3.5 follow-up paragraph now treats the deletion as part of the
   criterion and PD-005-02 as the use of the failing models. Table 5.13 gains "F median" and "Met" columns:
   - limits 0.47–0.92 against a largest Cook's distance of 0.26;
   - met for pool HCP and step yield, not met for leached Protein A (run-order trend) and fragments (spread
     trend);
   - all asserted from `D.residual_influence` (`over`, `over_f`, `f_limit`, `met`).
   Also updated: the §5.5 text, F8, Conclusion 3, the Discussion and the §13.6 discrepancy introduction. The
   §7.1 anion exchange sentence now says the model meets the fourth criterion (no run above 0.81), with runs
   2 and 9 above 4/n examined by deletion (INV-002 §8.4, 4.33–4.56). The PD-005-02 register entry renders
   from the record with its new wording.

Length and layout: renders ran between 69 and 77 pp as items arrived. Chapter-end spills were pulled
back by tightening only my own new text: change item 10 now points to §13; one restatement was removed from
§4.4; and F8, the Discussion sentences and Conclusions 2, 3 and 6 were shortened (the near-model sensitivity
stays in §3.1 and §5.3.1). The deviation register (PD-005-02's new text) ran into the page foot in portrait,
so it is set landscape (`landscape=True`), with columns widened to the landscape width so that it fits one
page with no empty page before it. The deviation register's disposition column wraps (font floor). **Final:
73 pp.** The growth over 69 pp is the new content: the classification argument, DEV-005-04/05, the
objectives and the landscape register.

Gate (`.venv/bin/python`, venv on PATH), the last runs:
- `check_render --render` passes 19 and 20: green;
- explicit `quarto render --to pdf` and `--to docx`: both exit 0;
- final `check_render`: exit 0, 798 inline expressions, no `<<NEEDS:>>`, 29 complex tables complete, no page-foot
  overrun, nothing below 7.9 pt.

Page images read: Table 3.1 (true minus), Table 5.13 (F median and Met), Table 13.1 (five deviations) and
Table 13.4 (landscape register).

For the coordinator:
- The DEV-005-04 disposition code renders in the register as "judged through its offset under the offset rule
  of pcmp 001 version 2 0". This is the record or the `dev_register` underscore handling, so it was not
  retyped. DEV-003-09 has the same code.
- PCP-005 §7 criterion 5 (plan PDF of 17:33) still reads "No run has a Cook's distance above 4/n". PCR-005
  §3.5 states the rule as the owner decided it ("4/n flags, F decides") and as PD-005-02 now words the plan.
  The plan needs the same wording.
- The classes all follow from the new argument. The KPP classes of load flow rate and end of pool collect
  rest on judging their significant effects on pool HCP (C² p 0.025; D p 0.003) as too small within the PAR,
  at 6 % and 7 % of the criterion. That is a judgement with no threshold, and it is stated as such.
- The aggregate criterion of the held eluate (§4.5) also rests on a widened value, the low-pH aggregate bound
  (INV-002 §8.4: 0.546–0.551 against 0.70). The fix list named only host cell protein, so §4.5 was not
  extended.
- The annex needs re-anchoring (many quoted sentences and three tables changed).

## 6. Record pass 2026-10-10 evening (`feedback-PCR-005.record-2026-10-10.md`)

Owner's decision: a process characterization study is not GMP manufacture, so it raises no deviation. Author:
Claude Opus 5.5. The backup is `PCR-005_protein_a.pre-record.qmd`. Only what the note names was changed, and
nothing is committed.
1. §13 is renamed "Study events and discrepancies from the plan" and opens with the note's sentence (PCP-005 calls
   a departure a deviation; study events under the Version 1.0 numbers; every departure a discrepancy). It then
   gives the events (Table 13.1, retitled "Study events recorded ...", from the new `dev_register`), then the
   discrepancies.
2. DEV-005-01 and DEV-005-02 stay as study events in their subsections. "The rule in the deviation record"
   now reads "the record of the event", and in §9 "The study event DEV-005-01" and "the buffer of that event".
3. The former DEV-005-03, -04 and -05 are now subsections PD-005-07, -08 and -09 of the discrepancy part
   (anchors `sec-pd07` to `sec-pd09`, all cross-references updated), with their content kept.
   - PD-005-08 states the Version 1.0 test (including "the model modified before the characterization studies"
     from the register) and the difference under it (p = 0.037, computed as before). It gives the register's
     reason (PCMP-001 Version 2.0 §7.1; the test was stricter than the use of the model needs). The sentence that
     Version 1.0 called the model qualified was removed, so nothing calls it a failure of Version 1.0.
   - PD-005-09 gives the recorded reason (`pd09_reason`).
4. Mentions updated:
   - the executive summary (two study events, investigated, runs retained, neither changes the judgement);
   - §3.1 (PD-005-08), §4.1 (PD-005-09), §4.4, §5.6 and the Discussion (PD-005-07);
   - Conclusion 11 ("Neither study event ...");
   - the introduction of the discrepancy part (two further studies and three departures described below).
   The counts are `n_dev` (asserted 2) and `n_pd` (9).
5. Change item 10 now records the events that Version 1.0 numbered as deviations as study events under their
   numbers, and the departures found in the re-analysis as discrepancies.
6. Asserts: two events (both retained); nine PD entries in order; the subjects of PD-005-07 to -09, the
   Version 1.0 test and the reason of PD-005-08, and the reason of PD-005-09. The data asserts (no centre runs,
   chronology order, p = 0.037, no other output differs) stay.
The criteria table: the sentences around it now name the new single-run limits column, and each verdict rests on
its upper end (15,349 ng/mg, 5.52 ppm, 1.09 %, which equal the values in the text).
Layout (table fit, as the note asks):
- **Table 7.2.** The criteria table, with its new single-run limits column, was scaled below the floor (7.7 pt).
  In my own chunk its attribute column is set to wrap at 1.9 cm (`cr.align`), and the builder's header, notes
  and values are untouched. Body 8.8 pt, notes 7.94 pt.
- **The discrepancy register.** With nine rows it fits no single page at the floor. The landscape setting of
  the last pass overflowed its page (row PD-005-09 cut off), and the gate did not see it on the rotated page.
  It is now set in two portrait parts from the same builder rows: Table 13.4 (PD-005-01 to -05, label
  `tbl-pd`) and Table 13.5 (PD-005-06 to -09, label `tbl-pd-b`), with the cut point computed and the text
  naming both.
- **Executive summary.** The events sentence was shortened to keep the summary on its pages.

Gate (`.venv/bin/python`, venv on PATH):
- dry run green;
- `--render` passes 21 to 23: font floor failures on Table 7.2, fixed;
- `--render` 24 and 26: green;
- explicit `quarto render --to pdf` and `--to docx`: both exit 0;
- final `check_render`: exit 0, 798 inline expressions, no `<<NEEDS:>>`, 31 complex tables complete (both
  register parts now probed), no page-foot overrun, nothing below 7.9 pt.

**75 pp**, against 73 before this pass: Table 7.2 is taller and the register takes two pages. Page images read:
Table 13.1 (events), Tables 13.4 and 13.5 (register), Table 7.2 (criteria).

For the coordinator:
- The register's own reason for PD-005-03 still reads "the deviation record shows the buffer below its target
  pH". This is register text, so it was not retyped.
- `check_render`'s page-foot check did not catch the overflow of a landscape table (rotated page). Other
  documents with landscape tables may hide the same fault.
- The annex: `tbl-pd` is now in two parts (`tbl-pd`, `tbl-pd-b`), §13 is restructured (anchors `sec-pd07` to
  `sec-pd09` replace `sec-dev03` to `sec-dev05`), and Table 7.2 has a new column. Re-anchoring is needed.
- `T.criteria_results` is too wide for PCR-005's attribute names at its default `llrrrl`, because the spanning
  header "Mean predicted by the response-surface model" sets the width. The local wrap works here, but other
  reports may hit the floor too.
