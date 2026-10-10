# PCR-003 after the content review and the factual check: what to change (one revision, same author)

Inputs, in this folder: `factual-PCR-003.md` (9 errors and minor items, each with its fix) and
`content-review-PCR-003.md` (the fresh judge's flags). Read both, and `procedures/REPORT-LESSONS.md`. Where this
note gives a resolution, write to it; otherwise resolve each flag yourself and say in your report what you did.
Every value stays computed and every deciding word computed or asserted. Regenerate your brief
(`authoring/build_brief.py PCR-003`): the register changed.

## A. What changed under the draft (2026-10-10, afternoon)
1. **Register** (deviations.csv): DEV-003-07 (initial viable cell concentration, active on acidic variants in the
   univariate study, not carried into a multivariate study as PCP-003 requires); DEV-003-08 (equipment and its
   calibration status not recorded for the osmolality and augmentation studies); DEV-003-09 (aggregate differed
   between the scales in the qualification, p < 0.05 under the Version 1.0 rule, and the investigation PCP-003
   required before the characterization runs was not made; aggregate is judged through its offset under
   PCMP-001 Version 2.0); DEV-003-01 now gives the direction (the pCO2 probe read high); DEV-003-03 names
   galactosylation too; DEV-003-05 covers the qualification runs. Nine deviations, each in §13 with its own
   subsection and cited where the text relies on it (factual error 2 lists the places).
2. **Screening run 4 is now analysed at its recorded setting** (`D.setting_corrections("bioreactor",
   "screening")`: 160 less the probe offset). The significant effects are unchanged; re-read every screening
   value from the helpers, and rewrite §13.1 and §5.2 ("either possible setting").
3. **The design-matrix tables use the report's factor letters** (A pH, B temperature, C pCO2, E duration):
   factual error 5 is fixed in the builder; check Appendix B after re-rendering.
4. **Builders**: true minus signs; `T.criteria_results` note c; `T.criteria_change` note e ("a model that meets
   the first three adequacy criteria"). Re-render.

## B. The factual check: resolutions
- **Error 1, the headline**: state in §5.3.4, §13.8 and §13.9 what the planned runs alone and the plan's full
  quadratic give (the factual file lists the values; compute them through the helpers: `D.fit` with
  `runs="planned"`, `D.planned_full_models()`), replace "no conclusion would change", and say in §7.2 ground 2 and
  §1.4 that containment of the NOR rests on the augmentation runs added after the planned results were known and
  on the model selection (PD-003-03). Reconcile with INV-001, which prints the Version 1.0 analysis (full
  quadratic on the planned runs, pCO2 PAR to 115 mmHg). State plainly whether ground 2 still supports the risk
  decision behind DEV-003-04, and tell me in your report.
- **Error 2(c), DEV-003-07 sized**: give the effect at manufacturing scale and what it does at the worst NOR
  corner (median and lower prediction limit), computed; qualify the executive summary.
- **Error 2(d), DEV-003-08 impact**: say what the missing calibration record means for the pCO2 settings of the
  augmentation runs and the osmolality study, and that every selected model is fitted to the augmentation runs.
- **Error 3, the classes**: correct the references to §2.1, state the conflict between the expectation and the
  class for dissolved oxygen and basal medium, and leave the classes as the config gives them; I take them to the
  owner.
- **Error 6(b), offset timing**: the Version 1.0 test for a difference compared the scales before the first
  characterization run, so the difference of means was known then; the confidence interval and the decision were
  computed at analysis, as PCMP-001 §7.1 allows. Say so; no departure.
- **Error 6(a), (c), (d), (f)**: state each effect against the width of its criterion with a judgement of
  practical importance (plan §7 item 4); report adjusted R²; state the ranges carried into the control strategy
  (the intersection of the PARs, plan §7 item 7); call the univariate t-test the report's approach. Error 6(e):
  check PCP-003 Version 2.0 (rendered) and tell me whether "every run" covers the qualification runs; do not
  write a register entry yourself.
- **Error 8, next to D-002**: keep the registered sentence exactly; fix only the elaboration after it.

## C. The content review: coordinator's resolutions
- **D-002 stays** (§1.1, your brief §5c).
- **Q5**: afucosylation and culture duration (the stated mechanism gives the opposite sign: say what the data
  show and that the mechanism does not explain it, or correct the mechanism); "The augmentation repeats no
  setting" (runs 29, 33, 35, 41, 44 repeat runs 2, 5, 7, 11, 16: fix, and say what that means for pure error);
  the augmentation decision date against S-BRX-OSM; DEV-003-01 and the response-surface design (the same probe,
  no recalibration recorded: state it); DEV-003-02 (what the record says about the affected run; SOP-3010 for the
  test, AMV-3010 for the validation); the pH margin (2.25 SD) vs "almost no margin"; the integrated model and the
  offset (Table 8.1 means below the set-point values: check with `D.capability`/the Monte Carlo helpers whether the
  drug-substance distribution carries the offset, and state which; if it does not, tell me, it is an engine
  question); "Without it the criteria ... would differ ... and no conclusion would change" (high mannose has no
  adequate full model); the PAR definition of ICH Q8(R2) vs the NOR-propagated PAR (name the difference); PARs
  only where the model has a significant term (objective 3); the low-pH exact fit (state the fact; owner
  question); the influence analysis re-judged only the conclusion over the NOR (say which conclusions it covers;
  the factual check found every PAR survives each deletion: compute and say so); DNA judged at the drug
  substance only (§2.2); PPQ runs at target and does not confirm range edges; the wrong cross-reference; the
  purification steps and charge variants (cation exchange separates by charge); osmolality a WC-CPP without a
  PAR; "differ in single terms"; the log-scale factor statement only without interactions; "never holds longer";
  "The simulation varies osmolality" (no model term); high mannose precision; 17 cases on 13 runs; Table 7.3
  rounding; the DEV-003-04 cell vs the predicted median (register text, tell me); afucosylation model bias at the
  centre (state it).
- **Q3 glosses and self-certification**: cut them ("a departure from PCMP-001 §5", "It is not the model used",
  "reported as observed", "producer's risk" as a label, "standard practice", "answers the question for which it
  was made", the WC-CPP re-filing).
- **Q1, Q2, Q6, Q7**: fix each flagged sentence (name the physical cause and its direction; "the 95 % prediction
  interval of a single batch" for "single-batch limit" at first use; criteria named, not lettered; deviation codes
  with their subject; no code as the actor; the garbled Version 1.0 PAR sentence).
- **Length**: the report is 79 pp. Cut restatements (the risk acceptance is said four times, "821 per million"
  three times, fragments out of scope four times) before adding anything.
- **Tables and figures**: fix your own (3.1, 4.3, 5.2 "PCO2", 5.4 scale, 5.8 units, 5.9/5.10 scale labels, 5.11,
  7.3 informative rows, 13.1 typos are register text: tell me); Figure 6.1 not colour alone. Leave the shared
  builders as they are.

## D. Gate and report
Gate with `check_render.py --render` (with `.venv/bin/python`), render the pdf and the docx, read the page image
of every table and figure you changed, refresh `.claude/work/2026-10-08_01_rev2-campaign/PCR-003_bioreactor.DRAFT.txt`.
Report each item with where it was resolved, the flags you left and why, the hand-backs above, the passes, the
page count, and any `<<NEEDS:>>` left (none).
