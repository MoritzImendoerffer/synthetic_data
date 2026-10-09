# PCR-005 status, 2026-10-09 (follow-up pass 2 complete)

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
