# PCP-007: final pass (review run 2)

Fix these and nothing else. The draft is `pc_package/PCP-007_cex.DRAFT.qmd`. The second judge's report is
summarised here; `feedback-plans-shared-2026-10-10.md` still applies. Every value stays computed and every
deciding word computed or asserted. Principle (as PCP-008 and PCP-009 now do): where PCMP-001 Version 2.0
replaces a Version 1.0 rule, the body states the Version 2.0 rule and the change list quotes the Version 1.0
rule it replaces; the two never stand side by side in the body.

Checked against the frozen Version 1.0 PCP-007: these flagged sentences are Version 1.0 text and stay word for
word: "do not bind" (leached Protein A), "not retained" (§4.1), "an effect smaller than that spread will not be
claimed", the execution-after-approval sentence, "Each run will be sampled at four points", "relative to the
peak maximum" (corrected in change 11, see A4), the operating region rule "declared where the fitted models
predict ..." (see A2), "held comfortably inside", the flow-rate rationale, peak broadening for the protein
load interactions, the assay-variability rule and the augmentation rule. Where Version 1.0 set no threshold,
your §7 list already says so.

## A. Errors and contradictions
1. **Prediction and the fourth criterion.** "A response-surface model is used for prediction only if it passes
   the four tests of PCMP-001 §7.2" is your Version 2.0 sentence; PCMP-001 does not say it. Delete it. State
   PCMP-001's remedy (lack of fit and the limit on overfitting) as the consequence of a failing model, and say
   once that PCMP-001 §7.5 asks only the first three criteria of the model behind a widening bound (§7.6). The
   reports examine a run flagged by the fourth. Table 1.1 note e now reads "on a model that meets the first
   three adequacy criteria of PCMP-001 §7.2" (builder, re-render).
2. **The operating region.** The Version 1.0 rule ("declared where the fitted models predict that every output
   ... meets its criterion") is replaced by PCMP-001's single-batch statistic (change 6). Quote the Version 1.0
   rule in change 6 and state only the Version 2.0 rule in §7.5. "The declared region will lie inside the
   ranges studied, and the normal operating ranges will lie inside the declared region" stays only if it is
   Version 1.0 text; then add that PCR-007 states the result.
3. **Execution and approval.** "Execution may begin once the plan is approved and the qualification runs of
   Section 5.1 have been made and the offsets estimated": keep the Version 1.0 part word for word and add one
   sentence that this Version 2.0 is the amendment INV-001 required (corrective action CA2), issued after the
   runs and approved on its effective date. Cut "which is acceptable because the derivation of its criteria
   uses no result of these runs" (a plan does not certify itself; the derivation fact can stay without
   "acceptable").
4. **Change 11, the collection thresholds.** Version 1.0 Table 6.1 set the stop collect in OD units (0.5 to
   1.5, set-point 1), so the design used absolute absorbance and only the description was wrong. Say exactly
   that in change 11 ("Version 1.0 described the thresholds as relative to the peak maximum, while its Table
   6.1 set the stop collect in OD units; the description now matches the design"). Do the same for the other
   corrections of change 11 (name what Version 1.0 said and what is corrected), and state in change 11 that the
   expected directions of §4.1 are unchanged.
5. **The qualification outputs and run counts** are a requirement of PCMP-001 §7.1 ("Each PCP-00N names the
   outputs, the number of runs at each scale and the manufacturing-scale data set"). Attribute them to it in
   the change list, not to this plan.
6. **Host cell protein and leached Protein A at the load pH** (Q5 items 3 and 4): "Host cell protein, DNA and
   leached Protein A are cleared because they carry a net negative charge at the load pH and are therefore not
   retained" is your Version 2.0 correction and overstates it: part of the host cell protein binds (the
   "weakly bound remainder", the clearance of 40 in Table 7.2), and leached Protein A travels largely in
   complex with the antibody. Say that most host cell protein flows through, a part binds weakly or with the
   bound antibody, and leached Protein A in complex with the antibody binds with it, which limits its clearance.
   Keep the Version 1.0 "do not bind" sentence as Version 1.0 wrote it if it is Version 1.0 text, and list
   this correction.
7. **The verification clearance factor** (Q5 item 10): define it as `iac.verification` computes it, the
   nominal feed of the step model over the predicted pool, not load over pool (as PCP-008 now does).
8. **The flow-rate range and fragments** (Q4): say that the flow-rate study measures no fragments, so the
   flow-rate range is not supported for fragments by its own data, and that Version 1.0 set no rule for it.
9. **Calibration recorded for one study only** (Q5 item 15): "the record names an instrumented system for the
   response-surface study only (EQ-CHR-118)".
10. **The fragments sentence of §5.3** says nrCE-SDS is the method "in every study at every step": write it as
    PCMP-001 §7.8 now does ("every study that measures fragments, at every step, measures them by
    nrCE-SDS"). `T.methods_by_study` records which method each executed design used: PCP-008 and PCP-009
    dropped it as an execution record; drop it too and point to PCMP-001 Table 7.3.
11. **Changes 2, 10 and 11 name no PCMP-001 rule**: change the sentence "Each change below names the rule of
    PCMP-001 Version 2.0 that it applies" so that it covers the corrections of description.
12. **The capability simulation** (Q5 item 22): if it is your sentence, say that the draws carry the
    coefficient and residual uncertainty as PCMP-001 §6.5 defines the integrated model, or point to it;
    if Version 1.0 text, keep it.

## B. The rest of the review
Q1: name the interaction in "Protein load and load/wash conductivity act on the same host cell protein" (at a
high load more host cell protein is held in association with the bound antibody, and a higher ionic strength
weakens that association) and in the §6.2 interaction sentence (your Version 2.0 text only). Q2: "influential
run" for "carries the fit" when you describe Version 1.0 in your own words (keep a quotation as a quotation);
"controlled room temperature"; name the register (the drug substance CQA register). Q3: cut "This is the
Version 1.0 rule for ..." (two) and "That bound is the one A-Mab value in the criteria of this step" if it
repeats §1.1. Q6 and Q7: cut the openers and restatements flagged; name INV-002's corrective actions; name the
assumption, the check and objective 6 where the review asks; name RA-001 and PCMR-001 at first use. Tables:
leave the shared builders as they are.

## C. Gate and report
Gate with `check_render.py --render` (with `.venv/bin/python`), render the pdf and the docx, read the page image
of every table you changed, refresh `PCP-007_cex.DRAFT.txt`. Report each item with where it was resolved,
anything left and why, the passes, the page count, and any `<<NEEDS:>>` left (none).
