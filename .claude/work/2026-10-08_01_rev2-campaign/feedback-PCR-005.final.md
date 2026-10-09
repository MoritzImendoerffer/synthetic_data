# PCR-005, final pass: what to change

Three inputs drive this pass. Work through all of them, in this order.

## A. The analysis changed (owner's decisions 2026-10-09). The report must follow the data.

Every value and every deciding word comes from the engine and the brief (`authoring/out/PCR-005.brief.md`,
regenerated today). Do not reuse a number from the current draft without recomputing it.

1. **Model selection for every output (INV-002 corrective action CA3).** `D.fit("protein_a", "rsm", resp)`
   now returns the selected model of each output: the scale from the Box-Cox profile, the model with the
   lowest AICc among all hierarchical submodels of the full quadratic (exhaustive search), then judged
   against PCMP-001 §7.2. `status` "selected" or "none" (no adequate model: judged on measured results,
   no range). The brief's §4c status table gives each output's model, scale and terms. Describe the
   procedure in the statistical methods. It is a discrepancy from the plan, PD-005-04 (computed, in
   `discrepancy_register(DOC)`); PCMP-001 is not changed. Carry `T.model_reevaluation("protein_a")`.
   The draft's own reduced step-yield code is superseded by the engine; remove what duplicates it.
2. **Run 23 analysed at its recorded elution buffer pH** (DEV-005-01, 3.38): `D.setting_corrections`.
   Discrepancy PD-005-03. In the DEV-005-01 section, give the run's residual on the model used and a
   sensitivity: the conclusion with run 23 at its design pH and with it excluded.
3. **Pool host cell protein is modelled on the log scale** (Box-Cox; the interval in `D.fit(...)["boxcox"]`).
   Prediction limits are computed on the log scale and back-transformed: their coverage is exact, they
   are asymmetric in ng/mg, and a back-transformed mean prediction is the median. The scale-down offset
   is taken on the same scale, as a ratio of geometric means (`D.sdm_offset`, `T.sdm_offsets`).
   On the log scale the protein load × elution pH interaction is not significant: the two effects
   multiply, which shows as an interaction only in ng/mg. The selected model does not contain the
   term. Its p-value in the full quadratic on the log scale is
   `D.fit(UO, "rsm", "pool_hcp_ng_mg")["full_scale"]["model"].pvalues["load:elution_ph"]`, and on the
   raw scale `...["full"]["model"].pvalues[...]` (compute both, never type them). Remove every claim
   that the two parameters interact, and state the finding correctly.
   The selected model of leached Protein A has no term (intercept only). That says the output does
   not depend on the four parameters within the range studied (STORY_BIBLE §9b, item 3 of the
   analysis). Say so plainly, and judge it accordingly; do not report effects for it.
4. **Criteria in force changed** (`D.iac_table(UO)`, `D.iac_verification`). Pool host cell protein is
   widened on the bounds of both cation exchange and anion exchange: both models are adequate once
   selected. The hold criteria (the production bioreactor output criteria) moved too. Recompute every
   criterion in the text and the "wider than Version 1.0, not a loosening" sentence.
5. **No NOR narrowing.** On the selected models the qualification of the scale-down model holds over
   the protein load NOR as characterized (20–40 g/L resin). Remove every statement that PCR-005 narrows
   the load NOR. Recompute the qualification on the planned runs alone and on all runs
   (`T.sdm_offsets(["protein_a"], studies=["S-PA-SDM"], label="tbl-sdm-offsets-planned")`,
   `D.offset_qualification(UO, resp, studies=[...])`) and say what the supplementary runs (PD-005-01)
   changed under the final analysis, whatever the data show. Today the data show that the model is
   qualified for pool host cell protein on the planned runs alone as well, and that the further runs
   narrowed the interval of the ratio; assert this in the setup chunk so that a re-run that changes it
   fails loudly, and never say the three-run result would have failed (STORY_BIBLE, PD-005-01). Their
   reason stays what the record says: they were made during the re-analysis to narrow the offset
   interval of pool host cell protein.
6. **Builder changes since your last render:** `T.doe_results` (factor codes, units on a third header
   row, run types merged, LPA defined in a note), `T.sdm_offsets` (run counts merged, CI on one line,
   the NOR named, a ratio for a log-scale output), `T.criteria_results` (median and ratio notes; an
   output with no adequate model shows its measured range), `T.worst_case_verification` (centred
   sub-headers), `T.hold_stability` (SEC note on the header). Uncaptioned tables no longer use a table
   number. Before each appendix heading print `appendix_numbering("A")`, `("B")`, … in an
   `#| output: asis` chunk.

## B. The factual pass (`factual-PCR-005.md`)

Fix all five errors. Error 2 (Table 5.9 reports a step-yield model the text rejects) and error 4 (one
grid for every design-space fraction; use `D.design_space_grid(UO, n=41)` and state the grid) still
apply in substance under the new models: every model table, F-item and value must now come from the
model the engine selects. Item 6 is moot, because no NOR is narrowed.

## C. Review run 2 (`content-review-PCR-005.run2.md`)

Address every flagged sentence and table observation that A has not made moot. Where A makes an item
moot, nothing is needed. Items that remain in substance, in short:
- Q1: name the physical cause in each causal clause (the list in the review).
- Q2: define "NOR-propagated PAR" once at first use (PCMP-001 §6.4 defines it); "lower limit", not
  "floor"; drop internal labels ("hold rule", "offset rule", "widened on verification", "one-factor
  test") in favour of what they mean.
- Q3: cut the defensive glosses listed.
- Q4: state the basis of the hold criteria (from the bioreactor output criteria and the downstream
  values); judge acidic variants against both ends of 18–39.6 % in Table 5.13; give the capability of
  acidic variants against the target and the minimum, and say how leached Protein A is judged when
  its Cpk is not meaningful; say why residual DNA has no intermediate criterion (PCMP-001); give the
  probability out of specification (`D.p_oos()`), or its bound when no batch falls outside.
- Q5 (those not resolved by A): F7 and Tables 7.2/7.3 must agree on which PARs are claimed and on what
  basis (the selected model, or the measured results); "would fail every acceptable run" holds for host
  cell protein only; "No criterion of this step was tightened" must distinguish this step's criteria from
  the hold criteria; "confirmed or bettered" overclaims where a model failed the adequacy test; "no lack
  of fit" means "no significant lack of fit" with its p-value; cross-references to the influence analysis;
  PCMP-001 §7.2 compares predicted R² with R² (not adjusted); three outputs have a criterion; the
  prediction limit is the upper end of the 95 % prediction interval (say so once); Protein A binds the VH3
  framework of some Fab fragments (qualify the fragment statement); step yield needs the load titre by
  Protein A HPLC, not A280 (use only a method the brief lists; otherwise state the limitation); the
  fragment offset argument (protease in the held harvest also clips antibody: give the bound from the
  harvest hold study); leached Protein A can depend on loading time; optional stopping in PD-005-01;
  the definition of a discrepancy from the plan (S-PA-RET was done under the method decision AMD-001).
- Q6, Q7: the restatements, hedges ("is associated with") and bare codes listed.
- Tables: the header and formatting observations, unless a builder already fixed them.

Gate, render, look at every table, as before. Report what you changed under A, B and C, what you found
moot, the page count, and anything you could not resolve.
