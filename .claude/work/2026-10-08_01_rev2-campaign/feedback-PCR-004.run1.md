# PCR-004 after the factual check: what to change (one fix pass, same author)

Input: `factual-PCR-004.md` (in this folder). Read it, and `procedures/REPORT-LESSONS.md` §3 rule 1, §2 rules 9 and 10
(rule 10 is corrected: PCMP-001 Version 2.0 §5 sets the held-pool criterion), §6 and §7. The owner changed the pipeline
on 2026-10-11: no separate content review ran on this draft. The readability review comes once, after this pass. Write
cleanly now. Every value stays computed and every deciding word computed or asserted. Regenerate your brief
(`authoring/build_brief.py PCR-004`), because the register changed.

## A. The record
- **New register entries** (config, committed 7df7995): PD-004-04 to PD-004-08 record the departures your hand-back and
  the factual check confirmed:
  - PD-004-04: samples before and after the step not taken, with the slope rule in place of criteria 1 and 3;
  - PD-004-05: filter-train pressure and the Protein A load challenge;
  - PD-004-06: the depth filter load series on set-point centrate only;
  - PD-004-07: records of execution not kept;
  - PD-004-08: the rules the report states.
- **PD-004-01** now names the levels that leave out three NOR limits and the added fragment and DNA responses.
- **Text.** Describe each entry in the discrepancy part, cite it where the text relies on it, and remove the claim of
  completeness if anything remains unregistered (error E1). Put any departure still in neither register in your
  hand-back.
- **PD-004-02** now says that PCMP-001 Version 2.0 §5 judges a held pool against the criteria it must meet on entering
  the next step. Only the expected entering level and the reading of the change are the report's approach. Correct
  "No plan sets how a held pool is judged" in the two places it appears (E8).

## B. Errors (factual check): resolve each as the file gives it
- E2: describe the simulation as PCMP-001 does, each parameter drawn from N(set-point, NOR width/6) clipped to the range
  studied, in §3.5 and §8.
- E3: rest the §7 capacity argument on the duplicate runs and the steep rise, not on DEV-004-02.
- E4: in "Changes in this revision", state what moved: the depth filter load PAR from 80–160 to 80–140 L/m2, with the
  upper NOR limit now on its edge; and the Version 1.0 claim of a qualified laboratory disk-stack model with no
  difference between scales, against no qualification now. Also state that the classes are unchanged.
- E5, the aggregate method. Follow the corpus convention, as PTP-001 states it: the SEC aggregate method is validated
  under AMV-3011 (SOP-3011), and AMV-3221 is the record of its qualified performance. Give its precision (3.8 % RSD)
  and the nrCE-SDS repeatability (0.06 points, config `analytics.methods.cesds`), and say that aggregate and fragments
  scatter at about method precision.
- E6: three NOR limits were not run.
- E7: objective 2 was met in part.
- E9: state the day-0 aggregate of the held pool beside the set-point runs (1.12–1.14 against 1.59 %). Say that the
  record does not name the culture of the hold pool, and that the hold verdict rests on the changes over the hold.
- E10: PCP-004 lists fragments in scope. They are not a response of its study and not named in its criteria.
- E11: 1.12 %, with the one-day cold hold the univariate runs did not have.
- E12: "called critical": PCMP-001 calls all 11 register attributes CQAs. Use the register's terms, and drop the A-Mab
  attribution unless you find it in the source.
- E13: the fragments entering level comes from a set-point culture; say this as a limit.
- E14: the minor items.
- **Departure 10, the error term.** The plan's error term decides (REPORT-LESSONS §1 rule 9). Use the set-point
  replicates for the slope tests and the intervals, and give the regression-residual version as a sensitivity (the
  decisions are the same; the precisions move, as the file lists).
- **Practical significance as the plan defines it (§5.5).** Give each significant slope's change across the NOR against
  method precision, computed:
  - centrate turbidity against rcf, −24.6 NTU;
  - post-clarification turbidity against rcf, −0.22 NTU;
  - post-clarification turbidity against depth filter load, +2.84 NTU.

## C. Builders changed under you (re-render to pick them up)
- `T.criteria_results`: the single-run limits column and a wrapped header.
- `D.par_table`: "n.a." for an output with no adequate model.
- `dev_register`: Event / Summary / Detected during / Outcome.

## D. Owner questions (leave the config as it is; state the facts)
- The upper NOR limit of depth filter load sits on its PAR edge, on an unqualified model. State it, and the reliance on
  the turbidity in-process control.
- The GPP class of turbidity rests without the Protein A load challenge. State the basis the class has.

## E. Gate and report
- Gate with `check_render.py --render` (`.venv/bin/python`, venv on PATH).
- Render the pdf and the docx, and run `check_render` once more.
- Read the page image of every table you changed.
- Refresh `.claude/work/2026-10-08_01_rev2-campaign/PCR-004_harvest.DRAFT.txt`.
- Report each item with where it was resolved, anything left and why, the passes, the page count, and any `<<NEEDS:>>`
  left (none). Do not commit.
