# PCP-003: final pass (review run 2 + factual check)

Two inputs: `factual-PCP-003.md` (15 errors) and `content-review-PCP-003.run2.md`. The factual check
found the deeper problem, so it comes first.

## The correction to the amendment rule (coordinator, 2026-10-09)

My note asked you not to ADD a rule after the data. You also deleted or rewrote Version 1.0 rules the
data then broke, and that hides the departure, which is as wrong as adding a rule. STORY_BIBLE §9b and
`data-state-2026-10-09b.md` §5 now say: the amendment keeps the design, sampling, procedures and EVERY
decision rule of Version 1.0 as Version 1.0 stated them; the report records each departure.

For this pass you may read the frozen Version 1.0 plan for its content (rules, design, sampling,
procedures, prior expectations), never for voice:
`pdftotext -layout pc_package/superseded/rev1/PCP-003_bioreactor.pdf -`.

## A. Factual errors (fix each as the report says; resolutions where they differ)

1. §6.3: restore the Version 1.0 rule for choosing the response-surface factors (the factors the
   screening finds active; the design amended before execution if they differ). Do not say the plan has
   no rule. The departure (osmolality active and left out) is PCR-003's to record.
2. Residual tests: keep the Cook's distance and residual-regression tests, worded exactly as PCP-005
   words them (n = the number of runs in the fit), and keep them listed as a change. The fact that they
   flag many correct models is a weakness PCR-003 will handle as PCR-005 does; it is not yours to fix.
   Add PCMP-001 §7.2's own residual wording beside them.
3. §7 items 4 and 6: restore the Version 1.0 rule that the NOR must lie inside the acceptable region
   (narrowed until it does). The acidic-variant worst corner and the owner's decision not to narrow
   are PCR-003's to record.
4. §7 item 5: restore the Version 1.0 decision rule for the univariate study.
5. Restore HCP, DNA and the qualification comparison to the sampling plan as Version 1.0 had them.
6. Restore the Version 1.0 calibration check before and after execution.
7. §11: the study sequence as Version 1.0 planned it; the execution windows of Table 11.1 stay.
8. §4.1: the Version 1.0 prior expectation for basal medium and feed (the brief and RA-001 agree).
9. §6.2 and assumption 5: do not assume pCO2 and osmolality effects add; the screening estimates their
   interaction. State what the design estimates.
10. §5.1: no PCMP-001 §5 citation that the next paragraph contradicts. State what Version 1.0 planned.
11. §7 item 2: restore "or the design augmented" and the normality check.
12. The other dropped Version 1.0 rules (the report lists them): restore each.
13. Remove execution and analysis details taken from the data.
14. The set-point PAR grid: state the grid the engine uses (`D.PAR_GRID_SETPOINT`) and list the change
    from Version 1.0's 81 points.
15. List every record correction in §1.1.
Every change from Version 1.0 that remains must be listed in §1.1.

## B. Review run 2 (fix what is not already resolved by A)

- Classification (§7 item 7): say plainly that SOP-4001 and PCMP-001 give no threshold for its terms and
  that PCR-003 states effect sizes and margins and argues each class.
- pCO2 and osmolality: do not claim the design separates them; state the Version 1.0 design and what it
  estimates. No PAR claim "at manufacturing scale" for pCO2 that rests on osmolality being held.
- Assumption 4 (no interaction of the univariate parameters) against §4.1: state it as an assumption
  with its basis, or remove the contradiction.
- Q1, Q2, Q3, Q6, Q7 sentences and the table observations: fix as the review says.

Gate, render, look at the tables you changed. Report what you changed under A and B, and the page count.
