# PCP-010 after review run 1 and the factual check: what to change (one revision, same author)

Inputs, in this folder: `factual-PCP-010.md` (9 errors, each with its source and fix),
`content-review-PCP-010.md` (the fresh judge's flagged sentences, by question), and
`data-state-2026-10-10.md` (the data changed on 2026-10-10). Read all three. Where this note gives a
resolution, write to it; otherwise resolve each flag yourself, stating in your report what you did with
it. Every value stays computed and every deciding word computed or asserted.

## A. What changed under the draft (2026-10-10)
1. **S-UFDF-SDM now has results** (owner's decision Q8): 3 scale-down and 5 manufacturing runs of step
   yield, aggregate, final concentration and permeate flux. The plan still describes only the planned
   qualification (Version 1.0 design). It states as PCMP-001's requirement, not as a record of what was
   done, that the qualification runs and the offsets come before the first characterization run
   (factual error 1). For aggregate, the plan applies the offset PCMP-001 §7.1 applies to an output with
   a criterion; how the change across the step and the level in the final retentate relate (a load
   common to both scales) is PCR-010's to state.
2. **The revision history now reads "Reissued under INV-001: the rules of PCMP-001 Version 2.0 applied,
   execution dates recorded"** (no INV-002, no intermediate criterion). Remove every sentence that says
   this plan is reissued under INV-002 or names INV-002 as a reason (factual error 8; Table 3.1 then
   agrees).
3. **Criterion 4 thresholds are in the config** (`THRESHOLDS["residual_alpha"]`, `["cook_factor"]`). They
   apply to response-surface models, which this step does not have; do not add them.

## B. The factual check
Resolve errors 1 to 9 as `factual-PCP-010.md` gives them (error 1 as in A1, error 8 as in A2). Error 2:
add the classification rules of PCMP-001 §6.2 and §7.7 to "Changes in this revision" and qualify the
item that says neither rule changes what the plan decides. Error 7: restore the Version 1.0 sentence word
for word.

## C. The content review: coordinator's resolutions
- **Version 1.0 rules stay as Version 1.0 wrote them** (STORY_BIBLE §9b), even where the judge found
  them vague or in tension (the extension trigger, the pilot-scale repeat, the rule that attributes noise
  to the assay, "small against the criterion", the buffer-exchange plateau). Where you paraphrased a
  Version 1.0 rule, restore its wording; where Version 1.0 set no threshold, say so and leave the
  approach to PCR-010. Never add a threshold. Mark them as Version 1.0 rules where a reader could take
  them for new ones.
- **Science (Q5) is corrected where a sentence describes the process wrongly**, without changing the
  design: wall shear is set by crossflow and channel geometry, not by TMP; the final concentration is a
  parameter of the design and the time on the skid differs between runs, so membrane loading does not
  fix either; acidic variants and the buffer exchange also carry criteria at this step; the acidic
  variant offset is unknown, not zero, and the two sentences must agree; three levels with a replicated
  set-point allow a curvature per parameter, only interactions cannot be estimated; the PCMP-001
  derivation assumes no change in aggregate or acidic variants after the steps it names, while this step
  can add both (say the derivation assumes it and the study measures it); the membrane retains every
  glycoform; fragments also form by non-enzymatic hinge hydrolysis with time. Fix the "skid instruments"
  sentence against Table 5.3, whichever Version 1.0 says.
- **Terms (Q2):** "NOR-propagated analysis" and "platform worst case" are PCMP-001 terms: define each at
  first use. Write "pure error", not "pure error band". Give AMD-001 its name at first use ("the
  analytical method decision AMD-001"). Replace "forms" or "sets" a quality attribute with what the step
  does to it.
- **Causes (Q1), glosses (Q3), restatement (Q6), codes and stand-ins (Q7):** fix each flagged sentence:
  name the physical cause in the clause, cut the filing glosses, say each fact once, name the virus
  filtration step instead of "Step 9", and name PCMP-001 when citing its Table 7.1.
- **Tables:** drop `T.methods_by_study` if it only says "no DoE" (say it in one sentence instead); no
  constant column (Table 6.1 study type, Table 11.1 equipment and calibration date: say them once in the
  text or the note); a legend for "Tool #1"; do not use CEX for an assay; Appendix A shows the level
  schedule without repeating Table 6.1.

## D. Gate and report
Gate with `check_render.py --render`, render the pdf and the docx, read the page image of every table
you changed. Report: each item above with where it was resolved, the flags you left and why, the
check_render passes, the page count, and any `<<NEEDS:>>` left (none).
