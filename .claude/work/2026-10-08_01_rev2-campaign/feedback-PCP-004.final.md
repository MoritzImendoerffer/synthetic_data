# PCP-004: final pass (review run 2)

Fix these and nothing else. The draft is `pc_package/PCP-004_harvest.DRAFT.qmd`. The review is
`content-review-PCP-004.run2.md` in this folder; `feedback-plans-shared-2026-10-10.md` still applies.
Every value stays computed and every deciding word computed or asserted.

Checked against the frozen Version 1.0 PCP-004: these flagged sentences are Version 1.0 text and stay
word for word (mark each as Version 1.0's where a reader could take it for new): criterion 1 ("A level
passes when no increase is detected at α = 0.05, or when a detected increase is smaller than the
resolution of the method that measured it"), "Step yield is reported but is not gated", the regressions
"reported with its coefficient of determination and its residual standard error", the culture fitted as
a block (§12 item 3), the bracket design of the depth filter load series, "held at its set-point",
"Samples will be drawn at four points", the SEC size-variant sentence, the exclusion of results below the
LOQ, and the disk-stack recirculation sentence (corrected below). Where Version 1.0 set no value or no
rule (the size of "the resolution of the method", the PAR of the turbidity series, how a PAR follows from
the two bracket series, a threshold for the regressions), say so once and leave the approach to PCR-004.
Never add a threshold.

## A. Errors

1. **Studies made after Version 1.0** (amendment scope item 1). PCMP-001 Version 2.0 §5: "Each report
   records its hold study as a discrepancy from its plan, and no plan describes one." Delete every
   sentence that names or describes S-HAR-HLD or S-HAR-UNI2, including the §1.1 sentence and its filing
   gloss ("They are not studies of this plan ..."). Keep one statement that the hold of the clarified
   harvest before capture is outside the scope of this plan (§1), and delete the other four.
2. **Unforeseen work** (§7): delete "Work that this plan does not foresee, done without a departure from
   this plan or from a procedure, is not a deviation." and the definition of the discrepancy term that
   follows. PCMP-001 states it; the plan need not.
3. **The qualification paragraph** (Q5 item 9). Say it in this order: the Version 1.0 comparison (centrate
   turbidity, solids removal, host cell protein, DNA, filter pressure and step yield, kept); PCMP-001 §7.1
   decides the qualification of an output with a criterion on the response-surface model of the step,
   which this step does not have, so this plan sets no qualification rule and PCR-004 states its
   approach; the turbidity of the clarified harvest is not in the comparison, so its offset is unknown,
   not zero.
4. **"This step has no intermediate acceptance criterion."** (Q5 item 14): PCMP-001 Table 7.1 sets none
   for the clarified harvest, because the derivation credits harvest with no change in any attribute, so
   the criteria of the production bioreactor output pass through it unchanged. Say that in one sentence.
5. **AMD-001 and INV-001 finding 6** (Q5 item 15): the decision of 2026-03-20 predates the investigation.
   Write it as PCMP-001 Version 2.0 §1.1 item 4 does: PCMP-001 sets nrCE-SDS as the method for fragments
   at every step, following the analytical method decision AMD-001, and this answers INV-001 finding 6.
   Say it once (§1.1); cut the repetition in §5.3.
6. **"kept in its words"** (Q5 item 17): "otherwise kept in its words, except the descriptions corrected
   under change 7".
7. **Presumed results** (Q4): the objective and §8 say "determine whether the normal operating range lies
   inside the proven acceptable range", not "confirm" or "will be shown"; "are to be met by the clearance
   that the purification train delivers"; the contribution to the control strategy is what the study
   "is to provide". If a presuming sentence is Version 1.0 text, keep it.
8. **Table 5.1 "Analytical variance (%)"** (Q5 item 11): the share of variance depends on the data set it
   was estimated in. Drop the column, or name the data set in its note if the record gives it.
9. **"No result of this study enters them."** (§7): "No result of the studies under this plan was used to
   set or change these criteria."

## B. Version 1.0 descriptions corrected (change 7, each correction named)

Replace "Descriptions that Version 1.0 stated wrongly, of the centrifuge, of the depth filter load, of the
sampling and of the analysis, are corrected without a change to the design" with a list that names each
correction (what Version 1.0 said, what this plan says instead), and mark the corrected sentences where
they stand. Include:
- **The disk-stack centrifuge** (Q5 item 7): a continuous disk-stack centrifuge passes the feed through
  its feed zone once. The cell damage a bench model does not reproduce comes from the acceleration in the
  feed zone and from the periodic discharge of solids.
- **Field and sigma factor** (Q5 item 6): say what the bench model holds. At each field of the series the
  bench feed rate is set so that its ratio of flow to sigma factor equals that of the commercial
  centrifuge at the same field and the commercial feed rate. For a batch laboratory centrifuge the
  matching quantity is V/(tΣ). State whichever of the two the Version 1.0 model is; do not invent a
  device.
- **Turbidity and the field** (Q5 item 5): the plan's own mechanism allows fine debris to rise with the
  field, so "It falls as the centrifugal field rises" becomes a statement with both effects.
- If you corrected other descriptions in run 1 (the depth filter load, the sampling, the analysis), name
  each one in the list too.

## C. The rest of the review
Fix the flagged sentences of Q1, Q2, Q3, Q6 and Q7 where the fix is local: name the physical cause and its
direction (lower viability at the end of culture releases more host cell protein and DNA; the interface
and the shear in the centrifuge and the filters break cells); write "the significance level set for the
campaign" and "is not an acceptance criterion" in your own sentences (keep "gated" where it is Version 1.0
text); name the impurity release criterion and the 10 NTU clarification limit beside their numbers; name
the load runs on centrate from 6,000 g and 12,000 g instead of "the bracket"; say "no response-surface
model" once; cut the restatements. Add a footnote to Table 6.1 that turbidity is measured, not set, in
the field and load series. Leave the shared builders as they are. Residual DNA (Q5 item 1) needs no
change: the criterion is A-Mab's claimed acceptable range, met through clearance.

## D. Gate and report
Gate with `check_render.py --render`, render the pdf and the docx, read the page image of every table you
changed, and refresh `PCP-004_harvest.DRAFT.txt` with `pdftotext -layout`. Report each item with where it
was resolved, anything left and why, the check_render passes, the page count, and any `<<NEEDS:>>` left
(none).
