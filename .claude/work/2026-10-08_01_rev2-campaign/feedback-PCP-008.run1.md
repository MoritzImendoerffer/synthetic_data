# PCP-008 after review run 1 and the factual check: what to change (one revision, same author)

Inputs, in this folder: `feedback-plans-shared-2026-10-10.md` (ten corpus-level resolutions, read
first), `factual-PCP-008.md`, `content-review-PCP-008.md`, `data-state-2026-10-10.md`, and
`procedures/PLAN-LESSONS.md` (rules 4, 8 and 10 changed today). PCMP-001 was re-rendered today (§7.5
rule 2 and the design-space statistic): re-read its §7.2 and §7.5 from
`pc_package/PCMP-001_master_plan.pdf`. Where this note gives a resolution, write to it. Otherwise resolve
each flag yourself and say in your report what you did. Every value stays computed and every deciding
word computed or asserted.

## A. The factual check
1. Error 1 (item 7, widening): shared item 1.
2. Error 2 ("No approved plan contained these criteria"): shared item 2.
3. Error 3 (change 4): "Version 1.0 did not list fragments as a response of this step and did not judge
   them." The studies measured them. The builder note of Table 1.1 says "Version 1.0 did not report
   fragments", which agrees, so leave it.
4. **Error 4 (change 9, the coding of protein load): restore the Version 1.0 statement word for word**,
   in §5.5 ("Each parameter will be coded so that the set-point is 0 and the edges of the
   characterization range are ±1. ...") and in Appendix A ("The runs are given in coded units, where the
   set-point is 0 and the edges of the characterization range are ±1."). Delete change 9, the sentence in
   Table 1.1 or its note that says the set-point is not coded 0, and the sentence in §6.1 "so the
   set-point lies above the centre of the range". Two reasons. A plan never rewrites a Version 1.0 design
   statement (STORY_BIBLE §9b): where the centre points actually ran is PCR-008's to record. And your
   brief §5c carries registered discrepancy D-001, whose instruction is: "Do not describe the design
   centre, the range midpoint, or coded zero in a PLAN." Protein load is exactly the factor where D-001
   bites, so a plan sentence about the centre of its range erases part of a benchmark item
   (`authoring/DISCREPANCIES.md`). Keep the D-001 sentence as §5c gives it.
5. Error 5 (classification): shared item 4.
6. Error 6, low priority:
   - §5.1: state what PCMP-001 §7.1 requires (the offset of each output with a criterion; the other
     outputs recorded where both scales measure them) and keep the Version 1.0 list of compared outputs.
     Do not assert which offsets were recorded: residual DNA and leached Protein A are below the LOQ at
     both scales, and bed pressure was not measured. PCR-008 records that.
   - EQ-CHR-118: keep the Version 1.0 equipment sentence as Version 1.0 wrote it. The PA3 record of the
     anion exchange studies names no instrumented system. State the execution windows, say once that the
     record names no instrumented system for these studies, and leave the gap to Version 1.0 to PCR-008.
   - Item 5 and objective 2: the design-space statistic (shared item 5).
   - "the four conditions of PCMP-001 §7.2, which carry numerical limits": say which limits PCMP-001
     sets and which are the generic tests of this plan (`THRESHOLDS`).
   - "Aggregate is therefore not a response": give the reason PCMP-001 Table 7.1 gives (check `iac.csv`:
     which attributes carry a criterion at this step), so that it does not hold equally for fragments.
   - §1: list residual DNA and leached Protein A among the outputs as monitored outputs (Version 1.0
     §5.4 monitors them on every response-surface pool).
   - Change 8: name the move from a step capability estimate to the integrated model of the train, as
     PCMP-001 §7.9 states it.

## B. The content review (step-specific)
- **Version 1.0 text stays.** Several flagged rules are Version 1.0 text (the load qualification and the
  invalidate-and-repeat rule, "NOR narrowed rather than criterion relaxed", "attributed to the assay",
  the viral run at the high end, "may run in parallel"). Keep each word for word and mark it as a
  Version 1.0 rule where a reader could take it for new (the reviewer took the invalidate rule for one).
  Where Version 1.0 set no threshold, say so once and leave the approach to PCR-008.
- **Offsets of fragments and viral clearance**: "unknown, not zero", judged as the scale-down model
  gives them (PCMP-001 §7.1), in every place. Two places now say "no offset".
- **Viral clearance and the execution windows** (Q5 item 3): keep the Version 1.0 sentence that the
  viral runs may run in parallel. Make the windows sentence agree with the record (which studies hold
  the spiked runs) without adding a window the record does not have.
- **Delete the criticality convention** ("attributes of high or very high criticality are called
  critical"); PCMP-001 Version 2.0 does not have it.
- **"The step sets one critical quality attribute"**: the step contributes part of the cumulative MVM and
  XMuLV clearance; give its claims and the totals from the helpers (Table 8.1).
- **Science (Q1, Q5)**: equilibrium binding does not depend on residence time, mass transfer does;
  virus particles and DNA are large and their binding is limited by mass transfer; the interaction of
  pH and conductivity (a higher pH gives an acidic host cell protein more net negative charge, so more
  salt is needed to screen it); a spike adds medium, protein and salt; more acidic variants put the
  yield at risk, not the clearance of impurities (Q5 item 12); "the impurities compete with each other
  for the ligand" (give the direction); PPQ runs inside the NOR and does not confirm range edges (Q5
  item 13); a criterion not met at a range edge locates the operating region and is a result, not a
  deviation (Q5 item 19), unless that sentence is Version 1.0 text.
- **"A change to this plan after approval is made by revising the plan ... before the affected runs are
  made"**: if Version 1.0 text, keep it and add nothing; this revision is the amendment PCMP-001 Version
  2.0 issues after the runs, which change 1 says.
- **PAR from the mean prediction (Q5 item 9)**: check your brief §5c before you touch anything near the
  D-001 sentence. The set-point PAR is a Version 1.0 method; state PCMP-001 §6.4's statistic for the
  NOR-propagated range, and do not reconcile the two.
- **Leached Protein A** (Q5 item 17): it is monitored on every response-surface pool. Say what PCMP-001
  §7.5 does with its platform worst case at this step, and attribute it.
- **Execution record (shared item 9)**: drop Table 5.1 of executed designs if it records execution
  (the invalidated first execution, DEV-008-01, is PCR-008's), or reduce it to what PA3 asks. Drop "An
  extended hold of that pool after neutralization raises its acidic charge variants" from the risks
  (the deviation's finding). EQ-CHR-118 in the future tense goes (A6 above).
- **The seed 20240724 is Version 1.0 text** (Version 1.0 §8). Keep it, computed, once.
- **Terms (Q2)**: define "NOR-propagated analysis" and "platform worst case" at first use (PCMP-001
  terms); "governing parameter" is a Version 1.0 term, define it once; "spiking model" and
  "characterization model" become the scale-down model (spiked or not); "integrated process model";
  "minimum step log reduction factor" for "step floors"; "net negative charge" for "acidic"; no
  "release profile" for an intermediate.
- **Glosses (Q3), restatement and padding (Q6), codes and stand-ins (Q7)**: fix each flagged sentence,
  say each fact once (finding 1, the flow-rate reason, the load set-point, fragments by nrCE-SDS, the
  NOR-propagated draw, the seed, the offset subtraction, "decided later, at analysis", the approval
  date), and name each code at first use in a passage.
- **Tables**: fix what your setup chunk builds (Table 5.1 or its removal, Table 11.1 study type and note
  a). Leave the shared builders as they are: their findings go to the consistency sweep.

## C. Gate and report
Gate with `check_render.py --render`, render the pdf and the docx, read the page image of every table you
changed, and refresh `PCP-008_aex.DRAFT.txt` with `pdftotext -layout`. Confirm the D-001 sentence of
§5c is in the rendered text verbatim. Report each item with where it was resolved, the flags you left
and why, the check_render passes, the page count, and any `<<NEEDS:>>` left (none).
