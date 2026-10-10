# PCR-005: the record without deviations (owner's decision, 2026-10-10, evening)

PCR-005 is final, so change only what this note names. The owner decided:
- **A process characterization study is not GMP manufacture, so it raises no deviation.** Every departure from
  the plan, whether unforeseen work or a plan requirement that was not met (even one found in a later review), is
  a discrepancy from the plan.
- **The events of execution that Version 1.0 recorded keep their DEV numbers and are called study events.**
- **The Version 1.0 scale-down rule was too strict.** That rule was no significant difference between the scales
  at p < 0.05, with any difference investigated before the characterization runs. An offset can be accounted for
  where its precision is satisfactory.

## What changed in the record (config and builders)
- **DEV-005-03, -04 and -05 are now discrepancies PD-005-07, -08 and -09.** `discrepancy_register(DOC)` renders
  them:
  - PD-005-07: the univariate study without runs at the centre;
  - PD-005-08: the leached Protein A offset accounted for, not investigated, because the Version 1.0 test was
    stricter than the use of the model needs;
  - PD-005-09: the univariate study made before the response-surface design.

  `dev_facts(DOC)` now holds two study events, DEV-005-01 and DEV-005-02.
- **`dev_register(DOC)` has new column headers:** Event, Summary, Detected during, Outcome. "retained" prints as
  "run retained in the analysis".
- **`T.criteria_results` has a new column, "95 % limits of a single run over the NOR".** It holds the lowest lower
  and the highest upper single-run limit, which is the statistic that decides each verdict of a quality attribute.
  Check the table fit and any sentence that describes the table's columns.
- **The section is now "Study events and discrepancies from the plan"** (`authoring/section_plan.yaml`,
  `procedures/REPORT-LESSONS.md` §3 rule 1 and §6 rule 9).

## What to change in PCR-005
1. **Heading and opening of the record section.** Rename §13. Open it with one sentence: PCP-005 calls a departure
   from the plan a deviation, and because a process characterization study is not GMP manufacture, this report
   records the events of execution as study events, under the numbers Version 1.0 gave them, and every departure
   from the plan as a discrepancy from the plan. Then give the events, then the discrepancies.
2. **DEV-005-01 and DEV-005-02** stay as study events in their subsections. Call them events, not deviations,
   everywhere in your own text. "Run retained" and the investigation stay.
3. **The three former deviations** move into the discrepancy part as PD-005-07, PD-005-08 and PD-005-09, each in
   its own subsection, keeping their content. For PD-005-08, state that leached Protein A differed between the
   scales under the Version 1.0 test (p = 0.037, computed as before). Give the register's reason: the test was
   stricter than the use of the model needs, and the output is judged through its offset where the offset is known
   precisely enough (PCMP-001 Version 2.0 §7.1). Do not call it a failure of Version 1.0.
4. **Every mention.** Update every mention of DEV-005-03 to -05 and of "deviation(s)": the executive summary, §1.4
   (and its item 10), §3.1, §4.1, §4.4, §5.6, the Discussion, Conclusion 11, F-findings and the §13 introduction.
   Counts become two study events and the number of discrepancies `PLAN_DISCREPANCIES` gives, computed and asserted
   (`n_dev == 2`).
5. **Changes in this revision.** One item records that the events Version 1.0 numbered as deviations are recorded
   as study events under their numbers, and that the departures found in the re-analysis are discrepancies from
   the plan.
6. **Asserts.** Adapt the setup asserts to the new register: the two events, the three new PD entries, and their
   order and subjects.

## Gate and report
- Gate with `check_render.py --render` (`.venv/bin/python`, venv on PATH).
- Render the pdf and the docx, and run `check_render` once more.
- Read the page image of Table 13.1 (events), the discrepancy register and the criteria table.
- Report what you changed and where, the passes, the page count, and any `<<NEEDS:>>` left (none).
- Do not commit. The annex is re-anchored afterwards by the coordinator.
