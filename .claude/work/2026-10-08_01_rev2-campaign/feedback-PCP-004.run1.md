# PCP-004 after review run 1 and the factual check: what to change (one revision, same author)

Inputs, in this folder: `factual-PCP-004.md` (12 errors, each with its source and fix),
`content-review-PCP-004.md` (the fresh judge's flagged sentences, by question), and
`data-state-2026-10-10.md` (the data changed on 2026-10-10). Read all three. Where this note gives a
resolution, write to it; otherwise resolve each flag yourself, stating in your report what you did with
it. Every value stays computed and every deciding word computed or asserted.

## A. What changed under the draft (2026-10-10)
1. **Harvest has no scale-down qualification in the record, and none could be made as Version 1.0
   planned it** (owner's decision Q8): no laboratory-scale disk-stack centrifuge exists, only pilot
   scale. PCR-004 records the qualification that was not performed as a deviation. The plan keeps the
   Version 1.0 qualification design and procedure as Version 1.0 stated them and claims nothing about
   their execution: no present-tense sentence says that the runs are made or the offsets estimated
   before the first characterization run (content review Q4b, factual error 5). The plan does not
   mention the deviation, which is the report's.
2. **The revision history now reads "Reissued under INV-001: the rules of PCMP-001 Version 2.0 applied,
   execution dates recorded"** (no INV-002, no intermediate criterion). Remove the sentence that the
   revision history also names INV-002, and every other statement that this plan is reissued under it.
3. **The shared step role now agrees with the CQA register**: "Primary recovery and clarification, where
   fragments form during the harvest hold" (factual error 2).
4. S-HAR-UNI2 now measured fragments and DNA. The plan still does not describe that study.

## B. The factual check
Resolve errors 1 to 12 as `factual-PCP-004.md` gives them. Error 1 in particular: step yield, centrate
turbidity, solids removal and filter pressure have no criterion, so their offsets would only be
recorded; host cell protein and DNA (criterion 1) and clarified-harvest turbidity (criterion 2, an
absolute limit) are judged against criteria, and PCMP-001 §7.1 decides qualification on a
response-surface model, which this step does not have, so this plan sets no rule for them and PCR-004
states its approach. Error 3: restore objective 4 word for word. Error 7a: restore "resolution".

## C. The content review: coordinator's resolutions
- **The Version 1.0 design stays** (STORY_BIBLE §9b): the bench model, the shear device, the criteria,
  the comparison of clarified harvest with unclarified culture, SEC on the size variants, the blending
  of the turbidity series. Many of the judge's science flags are criticisms of that design, and the
  report is where they are found and discussed. Do not redesign, and add no rule. Where you paraphrased
  a Version 1.0 rule, restore its wording; mark Version 1.0 rules where a reader could take them for new
  ones.
- **A descriptive sentence that is scientifically wrong is corrected** without changing the design: in a
  disk-stack centrifuge particles are captured on the discs, and the flow between the discs is laminar
  and low in shear; the centrifugal field varies with radius, so a setting in g does not mean the same at
  both scales without the flow to sigma factor; the depth filter media adsorb part of the DNA (error 4);
  L/m2 is a volume per area; the centrate point would locate a change in the size-variant profile; a
  non-significant difference is not evidence of no change (state the Version 1.0 rule, and do not defend
  it); "smaller than the precision of the method" and the §5.5 reporting rule must agree.
- **Terms (Q2):** a step changes or adds to an attribute, it does not "form" one; write that SEC
  overestimates low molecular weight species where host cell protein co-elutes; "Protein A load
  challenge at set-point conditions" for the fixed test; give AMD-001 its name at first use; the
  discrepancy from the plan is the corpus term, define it once.
- **Causes (Q1), glosses (Q3), restatement (Q6), codes and stand-ins (Q7):** fix each flagged sentence:
  name the mechanism and its direction in the clause; cut the filing glosses; say "no intermediate
  acceptance criterion" once; name the production bioreactor plan, the centrifugation and filtration
  procedures, the two PAR analyses, and what each investigation was about.
- **Tables:** merge the repeated Type cells of Table 3.2; widen Table 4.1's criterion column and give the
  drug substance criterion its source; Table 5.1: a two-line header, precision and LOQ in separate
  columns with the precision type, and a row for the DNA method if criterion 1 depends on it (from
  `dev_methods.csv`, AMV-3014, now in the record); drop `T.methods_by_study` if it only says "no DoE";
  one number format in Table 6.1; Table A.1 does not repeat Table 6.1; Table B.1 gives the method names
  or a legend.

## D. Gate and report
Gate with `check_render.py --render`, render the pdf and the docx, read the page image of every table
you changed. Report: each item above with where it was resolved, the flags you left and why, the
check_render passes, the page count, and any `<<NEEDS:>>` left (none).
