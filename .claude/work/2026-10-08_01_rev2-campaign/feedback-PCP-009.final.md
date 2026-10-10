# PCP-009: final pass (review run 2)

Fix these and nothing else. The draft is `pc_package/PCP-009_virus_filtration.DRAFT.qmd`. The second
judge's report is summarised here; `feedback-plans-shared-2026-10-10.md` still applies. Every value
stays computed and every deciding word computed or asserted. Checked against the frozen Version 1.0
PCP-009: the step-yield expectation and its hold-up sentence (V1.0 §4.1), "It is retained completely
while the membrane is intact", the integrity-test sentence, the univariate confirmation run (V1.0 §6.4)
and the protein sampling of "the unspiked load and the unspiked filtrate pool" are all Version 1.0 text.

## A. Errors and contradictions

1. **The qualification gate.** Change 3 says PCMP-001 §7.1 replaces the Version 1.0 rule that the
   screening runs would not begin until the qualification test had been met, and the decision is made at
   analysis. Two sentences of the same Version 1.0 gating rule still stand in the body and contradict
   change 3: §11 "Each phase begins when the preceding phase has met its criterion in Section 7." and §12
   "If the qualification in Section 5.1 fails, the study cannot proceed." Treat them as the screening
   gate is treated: quote each in change 3 as a Version 1.0 rule that PCMP-001 §7.1 replaces, and remove
   it from the body (in §12, keep the mitigation sentence that follows it, re-scaling and repeating the
   qualification, as Version 1.0 text if it still reads correctly; otherwise quote it in change 3 too).
   The sentence that no output with a criterion is compared at both scales stays once, in §5.1.
2. **The success criterion** (§7) is Version 1.0 text and stays. Add one sentence after it: under PCMP-001
   Version 2.0 fragments are judged in the same way (change 1), and PCR-009 states how it reads "the
   scale-down model is qualified" at a step where no output with a criterion is compared at both scales.
3. **The integrity test** (Version 1.0 text, scientifically overstated): an integrity test bounds the
   defects it can detect; it does not show that no pore of retrovirus size exists. Correct the sentence
   ("a membrane that passes that test has no defect large enough for the test to detect") and list it
   with the other corrections (change 10). "It is retained completely while the membrane is intact"
   stays (Version 1.0 expectation), and PCR-009 compares it with the censored results.
4. **Step yield** (Q1 and Q5 item 1): the Version 1.0 expectation stays ("to fall slowly as the
   volumetric load rises"). Its mechanism sentence reads as a fixed hold-up per unit area, which would
   make yield rise with load. If you can state the mechanism Version 1.0 meant (product held in a fouling
   layer that grows with the volume filtered), correct the description and list it in change 10;
   otherwise leave both sentences and add nothing.
5. **The count of outputs** (§1 "4 outputs") vs Table 5.1 (five, with flux decay): compute it from the
   table, or name the outputs.
6. **"No calendar dates are fixed in this plan."** vs Table 11.1: Version 1.0 fixed no calendar dates in
   advance, and Table 11.1 records the execution windows (PA3). Say so in one sentence.
7. **"The record names no instrumented system for these studies."**: name what is meant, the
   instrumented scale-down systems under calibration and change control of PCMP-001 Table 5.1.
8. **"no criterion of this step was tightened or widened by the verification of platform worst cases at
   the other steps"** reads as a result in a plan. State it as what Table 7.1 shows: the criteria in force
   equal their a priori values.
9. Leave the unspiked filtrate pool sentence as Version 1.0 wrote it (factual error 6 of run 1). PCR-009
   records how step yield was determined on the spiked runs. Add nothing.

## B. The rest of the review
Q6: cut the restatements of Tables 3.1 and 3.2 and the fourth and fifth statements that both parameters
are studied multivariately. Q7: name INV-002's corrective actions where the text says "Its corrective
actions are applied by PCR-009" (the model selection and the refits of the response-surface models below
the adequacy criteria); name step yield and flux decay in "The outputs that Version 1.0 compares at both
scales are kept"; name the classification rule in change 9; name the quantity a platform worst case is
("the lowest clearance fold or largest increase seen on the platform for this step, from which an
upstream criterion was derived"). Tables: Table 5.1 so that each output has its criterion on its own row
(no criterion shared across rows by a merged cell), and the run counts in a note tied to the comparison;
"log10" and "L/m2" one way across the tables. Leave the shared builders as they are.

## C. Gate and report
Gate with `check_render.py --render` (use `.venv/bin/python`), render the pdf and the docx, read the page
image of every table you changed, refresh `PCP-009_virus_filtration.DRAFT.txt`, confirm the D-001 sentence
of §5c is verbatim in the rendered text. Report each item with where it was resolved, anything left and
why, the passes, the page count, and any `<<NEEDS:>>` left (none).
