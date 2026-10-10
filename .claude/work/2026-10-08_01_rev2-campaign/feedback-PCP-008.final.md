# PCP-008: final pass (review run 2)

Fix these and nothing else. The draft is `pc_package/PCP-008_aex.DRAFT.qmd`. The second judge's flags are
summarised in `content-review-PCP-008.run2.md`; `feedback-plans-shared-2026-10-10.md` still applies.
Every value stays computed and every deciding word computed or asserted.

Checked against the frozen Version 1.0 PCP-008: these flagged sentences are Version 1.0 text and stay word
for word: the coding statement (registered discrepancy D-001 depends on it; add nothing about protein load
and the centre of its range), §13 "This plan will be executed after approval ..." and its change-control
sentence, "The normal operating ranges in the control strategy will be set from the second analysis",
"does not vary the quality of its load", the protein load range "well above the set-point", the pooling
sentence, the quadratic-terms sentence, the "release profile" of the load rule, the complexed ligand
fragments, and the flow-rate assignment reason. Where Version 1.0 set no threshold, the §7 list already
says so; add "well inside" and "high risk" of the classification rule to that list if Version 1.0 and
PCMP-001 set none.

## A. Errors and contradictions in the Version 2.0 text
1. **§13**: keep the Version 1.0 sentences. Add one sentence beside them: this Version 2.0 is the amendment
   that INV-001 required of each step plan (name the corrective action), issued after the runs and approved
   on its effective date.
2. **Prediction and condition 4**: "A response surface model is used for prediction only if it passes the
   four conditions of Section 5.5" (Version 2.0 wording) contradicts item 7, which takes a bound from a model
   that may fail condition 4. If Version 1.0 had the same rule in its own words, restore those words; then
   add once that PCMP-001 §7.5 asks only the first three conditions of the model behind a widening bound
   (item 7). Do not add any other consequence of condition 4: the reports examine a flagged run.
3. **"PCR-008 verifies them"**: only the host cell protein worst case is verified on a model; the leached
   Protein A value stands under PCMP-001 §7.5 (item 7). Say which.
4. **Capability**: the Cpk is one-sided for each attribute of this step; remove the two-sided wording
   ("names the side of the criterion that limits the Cpk") or restrict it to a two-sided criterion.
5. **"not by a test of equivalence"** (twice): Version 1.0 accepted the model where no significant
   difference was found between the scales, a test for a difference. Say so.
6. **"it had no class for a critical process parameter"**: Version 1.0 had the well-controlled critical
   class. Say precisely what it lacked (a class for a critical parameter that is not well controlled), or
   cut the clause.
7. **The objective on fragments** ("Quantify the effect of each studied parameter ... on fragments, over the
   ranges given in Section 6.1"): the flow-rate runs measure host cell protein and yield only. Restrict the
   fragments part to the parameters of the designs.
8. **The design-space objective and item 5**: a quality attribute on the single-batch limit, viral clearance
   on its mean prediction, as PCMP-001 states it. Make the objective say the same.
9. **The verification statistic** (Q5 item 20): the modelled response is pool host cell protein; the
   clearance factor is the nominal feed over the predicted pool (as `iac.verification` computes it). Say it
   in one clause.
10. **Mass transfer and residence time** (your change 10 correction, Q5 item 16): "Virus particles and DNA
    are large and diffuse slowly, so their binding is limited by mass transfer" contradicts the DNA
    sentence ("expected to be robust", monitored, not modelled) and DNA is not measured on the flow-rate
    runs. Keep the correction for the virus particles, which the viral run at the high flow rate tests, and
    drop DNA from it, or say the plan does not test it.
11. **The load pH × Equil/Wash-1 interaction** (your Version 2.0 sentence, Q5 item 22): a higher load pH
    gives an acidic host cell protein more net negative charge, and the salt of the solution in contact with
    the bed while it binds screens that charge. Say it so, without tying it to one buffer the plan does not
    give a pH for.
12. **Execution record** (shared resolution 9): keep the execution windows (PA3) in the past tense. Cut "No
    two windows overlap." and the sentence on where the spiked runs sit in the record. Phrase the equipment
    sentence as PCP-009 does ("The record names none of the instrumented scale-down systems under
    calibration and change control of PCMP-001 Table 5.1 for these studies"). Reduce Table 11.1 note a) to
    the fact that the first execution was invalidated and PCR-008 records the deviation (DEV-008-01). State
    "no verification at another step has changed them" as what Table 8.1 shows (the criteria in force equal
    their a priori values), if true; assert it.

## B. The rest of the review
Q1 and Q2: "has a significant effect on" instead of "governs" or "acts on" where the relation is
statistical, except in Version 1.0 sentences; name the species and the direction where the review asks
(yield in flow-through: the antibody carries a net positive charge at the load pH and is repelled by the
ligand; virus particles diffuse slowly to the ligand). Q6: say each fact once (the compiled criteria, the
offset timing, the residence-time sentences). Q7: name INV-002's corrective actions where the text says
"The corrective actions of INV-002 are applied in the paired report PCR-008" (the model selection and the
refits of the response-surface models below the adequacy criteria); name the two tests of condition 4; name
the 4-fold and 10-fold clearances; name the distribution of the simulation (normal, standard deviation of
the NOR width divided by `D.NOR_SD_DIVISOR`); name the old rules after "This replaces". Tables: the Table
8.1 rounding note goes if nothing in the table is recomputed (it is the builder's; leave it if it is the
builder's own note). Leave the shared builders as they are.

## C. Gate and report
Gate with `check_render.py --render` (with `.venv/bin/python`), render the pdf and the docx, read the page
image of every table you changed, refresh `PCP-008_aex.DRAFT.txt`, confirm the D-001 sentence of §5c is
verbatim. Report each item with where it was resolved, anything left and why, the passes, the page count,
and any `<<NEEDS:>>` left (none).
