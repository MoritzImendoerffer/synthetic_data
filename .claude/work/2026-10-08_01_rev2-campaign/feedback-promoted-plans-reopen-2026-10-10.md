# Re-open of the promoted plans PCP-003, PCP-005 and PCP-006 (2026-10-10)

The three plans were promoted on 2026-10-08 and 2026-10-09, before the shared resolutions of
2026-10-10 (`feedback-plans-shared-2026-10-10.md`) and the correction of PCMP-001 §7.5 and §7.8. The plans
reviewed today (PCP-004, PCP-007 to PCP-010) state those resolutions; these three must state them the same
way. Fix these and nothing else. The documents are promoted (`pc_package/PCP-003_bioreactor.qmd`,
`PCP-005_protein_a.qmd`, `PCP-006_viral_inactivation.qmd`); edit them in place. Read the rendered
PCMP-001 (`pc_package/PCMP-001_master_plan.pdf`, §6.2, §7.1, §7.2, §7.5, §7.7, §7.8) for content, and the
frozen Version 1.0 plan of each (`pc_package/superseded/rev1/`) wherever an item restores Version 1.0 text.
Every value stays computed and every deciding word computed or asserted.

## For each of the three plans
1. **The widening rule names its three tests.** PCMP-001 §7.5 rule 2: the bound replaces the platform value
   where it is better and "the response-surface model behind it meets the first three adequacy criteria of
   Section 7.2 (a significant model, no significant lack of fit and the limit on overfitting) and is not an
   exact fit. The fourth criterion, on the residuals and on influential runs, does not decide the change.
   The report that gives the bound examines it and states whether the bound depends on a single run."
   Restate it so wherever the plan states the rule. Never "meets the adequacy criteria of PCMP-001" or "of
   Section 7.1", which reads as all four. Found: PCP-003 ("meets the adequacy criteria of PCMP-001"),
   PCP-006 rule 2 ("meets the adequacy criteria of Section 7.1"), PCP-005 ("The A-Mab model of anion exchange
   passed the adequacy tests", and the same in a table note: it meets the first three, and fails the fourth
   on Cook's distance, so the sentence is false; say it meets the first three and is not an exact fit).
2. **The operating region or design space is drawn on the single-batch limit** (PCMP-001 Version 2.0, its
   judgement statistics): a setting lies inside when every quality attribute meets its criterion at both
   ends of the 95 % prediction interval of a single run, and viral clearance on its mean prediction.
   Restate it where the plan defines its region (PCP-003 §7 item 6 now says "where the response-surface
   models predict that every modelled attribute meets its criterion"; check PCP-005 and PCP-006), and list it
   in "Changes in this revision" as a change from Version 1.0.
3. **The frozen Version 1.0 criteria** (shared resolution 2): where the change on the Version 1.0 record is
   listed, it names both INV-001 findings, the title-block date (finding 5) and the criteria added to the
   plan text when the package was compiled, without a revision of the approved plan (finding 1). Where the
   plan quotes a Version 1.0 limit, say it was written into the compiled text, not approved with the plan.
4. **Classification, remedy, NOR-propagated draw** (shared resolutions 4, 6, 7): check that each plan keeps
   the Version 1.0 classification sentence word for word and lists PCMP-001 §6.2 and §7.7 as a change; states
   PCMP-001's remedy word for word ("either refitted with a justified change of terms or transformation, or
   it is not used to set a range") with the Version 1.0 consequence it replaces; and states the draw as
   PCMP-001 §6.4 defines it, with no "±3 standard deviations" claim for a parameter whose set-point is not
   the midpoint of its NOR. Change only what does not already conform.
5. **Fragments method**: if a sentence says fragments are measured by nrCE-SDS "in every study at every
   step", write it as PCMP-001 §7.8 now does ("every study that measures fragments, at every step, measures
   them by nrCE-SDS").
6. Registered discrepancy D-001 (PCP-003 and PCP-006 carry it in their brief §5c): do not touch the
   set-point PAR sentence, and add nothing about the design centre, coded 0 or the midpoint.

## PCP-005 only
7. **§6.4, the univariate assessment, is Version 1.0 text rewritten to match the record.** Restore the
   Version 1.0 design sentences word for word (numbers as inline expressions): "Operating temperature and bed
   height will be assessed one factor at a time. Each will be run at the low edge, the centre and the high
   edge of its characterized range, with the other parameters held at their set-points and with the same
   responses measured as in the multivariate designs." and the ranges sentence. Delete the execution
   statements: "Each is run in duplicate at the low end and at the high end of its range studied", "The
   set-point runs of the scale-down model qualification serve as the reference", "Fragments are not measured
   in the univariate study, which ran before AMD-001" and the responses list that follows the record. Keep
   the judgement rule of Version 2.0 (each result a single batch, against the criterion after the offset)
   as PCMP-001's. PCR-005 records the departures (DEV-005-03: duplicates at the ends, no centre run; the
   fragment result by nrCE-SDS not measured).
8. Check the sequence paragraph of §11 for the same kind of execution statement ("The retained pools are
   tested by nrCE-SDS after AMD-001" is an execution fact; the execution windows of PA3 in Table 11.1 stay).

## Gate and report, per plan
`check_render.py --render` (with `.venv/bin/python`; venv on PATH), render pdf and docx, read the page image
of every table you changed. Report per plan: each item and where it was resolved, anything left and why, the
page count, the passes. The annexes are re-anchored afterwards by the coordinator; do not edit
`build_ground_truth.py`.
