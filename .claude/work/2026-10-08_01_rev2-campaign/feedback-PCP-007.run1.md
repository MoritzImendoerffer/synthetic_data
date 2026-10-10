# PCP-007 after review run 1 and the factual check: what to change (one revision, same author)

Inputs, in this folder: `feedback-plans-shared-2026-10-10.md` (ten corpus-level resolutions, read
first), `factual-PCP-007.md` (11 errors), `content-review-PCP-007.md` (the fresh judge's flags, by
question), `data-state-2026-10-10.md`, and `procedures/PLAN-LESSONS.md` (rules 4, 8 and 10 changed
today). PCMP-001 was re-rendered today (§7.5 rule 2 and the design-space statistic): re-read its §7.2
and §7.5 from `pc_package/PCMP-001_master_plan.pdf`. Where this note gives a resolution, write to it.
Otherwise resolve each flag yourself and say in your report what you did. Every value stays computed and
every deciding word computed or asserted.

## A. The factual check
1. Error 1 (widening rule): shared item 1.
2. Error 2 (§6.4): restore the Version 1.0 univariate sentence and make its scope explicit, because
   Version 2.0 §5.3 now also lists fragments, which S-CEX-UNI did not measure: "Runs will be executed at
   the low edge, the set-point and the high edge of the range given in Table 6.1, with every other
   parameter held at its set-point, and the responses that Version 1.0 listed in §5.3 (pool aggregate,
   pool host cell protein, residual DNA, leached Protein A and step yield) will be measured on each."
   Pull the names from the helpers where they exist.
3. Errors 3 and 4: shared items 3 and 5.
4. Error 5 (change 5): say what is new against Version 1.0 as PCMP-001 Version 2.0 §1.1 states it
   (coefficient uncertainty in each draw, the defined distribution, the 97.5th percentile rule). Version
   1.0 already judged on a single batch.
5. Error 6: delete the two sentences (shared item 6). The report applies INV-002 CA2.
6. Errors 7 and 8: change 4 says Version 1.0 examined the residuals and influential runs with no test
   and no cut-off. Name the tests INV-002 judged (the model F-test, lack of fit, the limit on
   overfitting), or drop the clause.
7. Error 9: restore each rewritten or deleted Version 1.0 sentence. Where a Version 2.0 change makes a
   Version 1.0 sentence wrong (§8 "Each of the two attributes will be reported with a plot" now that
   fragments carry a criterion), keep the sentence's rule and list the change under the change that
   causes it (fragments).
8. Error 10: shared item 2. Error 11 (aliasing in a 2^(4−1) fraction): a descriptive correction, listed
   with the other corrections as one change (shared item 8).

## B. The content review (step-specific)
- **Version 1.0 text stays.** Several flagged sentences are Version 1.0 text, including expectations
  (protein load interacting with each other factor through peak broadening, the augmentation rule,
  "within assay variability of its criterion", "comparable in size with the effects estimated in the
  screening study", "follows the screening analysis"). Keep each word for word and mark it as a Version
  1.0 rule where a reader could take it for new. Where Version 1.0 set no threshold, say so once and
  leave the approach to PCR-007. Correct a Version 1.0 sentence only where it describes the process
  wrongly, and list that correction with the others.
- **Science (Q1, Q5), in your own Version 2.0 sentences or as listed corrections:** host cell protein at
  high load (fewer free sites leave more host cell protein in the flow-through; if the mechanism you mean
  is host cell protein bound to the antibody and eluting with it, say that); the direction of each named
  effect (elution flow rate, load x conductivity, the stop-collect point as an absorbance threshold,
  start and stop and fragments); elution pH controls release, so the failure modes at the ends of its
  range are incomplete elution and co-elution of aggregate, not binding; the platform sets the load to
  the wash conductivity, which is a design choice; the complexed Protein A sentence (name the interaction
  or cut it); "Most host cell proteins are acidic at the operating pH" (their isoelectric point lies
  below the load pH, so they carry a net negative charge); "a dimer carries twice the charged surface"
  (contact hides part of each surface); "The excess can never exceed the host cell protein present"
  (cut: an absorbance area and an ELISA mass are not comparable).
- **Delete the criticality convention** ("Attributes of high (H) and very high criticality are called
  critical"): PCMP-001 Version 2.0 does not have it, and Table 4.1 lists attributes of every criticality.
- **"The studies are run on a qualified scale-down model"**: the qualification is decided at analysis
  (PLAN-LESSONS rule 1). Say the qualification runs come first and the decision is made at analysis.
- **Verification (Table 7.2, §7.3)**: state the statistic PCMP-001 §7.5 uses, as PCMP-001 states it,
  not "the predicted worst case".
- **The PAR of the flow rate** comes from the univariate study. Make the PAR sentence and the
  classification sentence agree with that.
- **S-CEX-FRC and the SEC/nrCE-SDS comparison**: a plan does not report results. Name the analytical
  method decision AMD-001 and its outcome (fragments by nrCE-SDS from this step on) in one sentence, and
  leave the comparison results to PCR-007. That also removes the contradiction between "SEC read
  fragments high wherever the sample still carried host cell protein" and "From the cation exchange pool
  onward the two methods agreed".
- **Fragments without an offset**: state PCMP-001 §7.1 (an output not compared at both scales has an
  unknown offset, not zero, and is judged as the scale-down model gives it). The mechanism that makes
  that judgement reasonable is an assumption: state it once, in Risks and assumptions.
- **The widened host cell protein criterion**: the report that gave the bound, the anion exchange report
  PCR-008, examines it (PCMP-001 §7.5). Do not give PCR-007 that duty.
- **Execution record (shared item 9)**: the execution window of each study and the calibration status of
  EQ-CHR-118 as recorded facts, once. Rephrase "No other study under this plan ran on one of the
  instrumented systems" so that it does not read as measurements without control. Drop the S-CEX-UNI
  retention facts and the account of the response-surface study across the decision date (PCR-007's).
- **The seed 20240724 is Version 1.0 text** (Version 1.0 §8). Keep it, computed.
- **Terms (Q2)**: define "NOR-propagated analysis", "set-point PAR", "platform worst case" and
  "execution window" at first use (they are PCMP-001 terms); keep the Version 1.0 term for the operating
  region and define it once; "discrepancy from the plan" once; "Clearance factor" or "fold", one of them.
- **Do not describe the design centre** ("At this step the set-points are also the centre of the
  design"). The plans state the set-point PAR as their method and say nothing about coded 0 or the
  midpoint (registered discrepancy D-001, `authoring/discrepancies.yaml`). Cut the sentence.
- **Glosses (Q3), restatement and padding (Q6), codes and stand-ins (Q7)**: fix each flagged sentence.
  Say each fact once: finding 1, the AMD-001 sentence, the flow-rate residence time, "decided at
  analysis", "The centre points are run at the set-point of every factor." (Version 1.0 says it once:
  keep that one), the approval date, the seed.
- **Tables**: fix what your setup chunk builds (Table 10.1 role names, Table 11.1 parenthesis). Leave the
  shared builders (`T.criteria_change`, `T.iac_derivation`, `T.cqa_table`, the approvals and revision
  tables) as they are: their findings go to the consistency sweep. If Table 7.2 lists a fragment fold that
  rests on a load result no plan required, tell me rather than add a sample.

## C. Gate and report
Gate with `check_render.py --render`, render the pdf and the docx, read the page image of every table you
changed, and refresh `PCP-007_cex.DRAFT.txt` with `pdftotext -layout`. Report each item with where it
was resolved, the flags you left and why, the check_render passes, the page count, and any `<<NEEDS:>>`
left (none).
