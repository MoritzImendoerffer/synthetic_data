---
type: pm-task
epic: 2026-08-18_02_register-track-d
sprint: 2026-08-18_02_register-track-d
task: TASK-002
status: done
kind: mechanism
title: "Freeze the Track D measurement as a script that reproduces the baseline"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-003", "PCP-005", "PCP-008", "PCR-003", "PCR-004", "RA-001"]
---

> [!warning] Generated from `.claude/work/2026-08-18_02_register-track-d/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-002 — Freeze the Track D measurement as a script that reproduces the baseline

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-002.md. THIS IS THE MEMORY-MEMO TASK. Twice now a number quoted in a planning document came from an unsaved heredoc and could not be reproduced -- round two's owner-reading counts, and the proposal's 1.5 % guide figure that re-measured at 3.77 %. No number produced by this round may come from anywhere but this script. It wraps check_style.py and check_discourse.py rather than re-implementing them.

## Acceptance criteria

- [x] measure_trackd.py takes a list of .qmd and prints one row per document for every measure the stopping rule names, each with its denominator, plus the four human-source columns
- [x] run over all 20 committed .qmd it reproduces measure_baseline_style.txt and measure_baseline_discourse.txt EXACTLY -- same numbers to one decimal, including PCP-005 passive 66.7, PCP-008 67.7 and RA-001 64.2, the three already above the source band
- [x] it also emits the staccato and ', which' measures round three added by hand, so they are on one denominator with the rest
- [x] the script is committed inside the work unit and the results page cites it by path

## What was built

Every number Track D publishes now comes from `.claude/work/2026-08-18_02_register-track-d/measure_trackd.py`, and it reproduces both committed baselines cell for cell.

```
uv run --extra discourse python .claude/work/2026-08-18_02_register-track-d/measure_trackd.py --check-baseline $(ls pc_package/*.qmd)
  style:     408 cells compared, 0 disagreement(s)
  discourse: 120 cells compared, 0 disagreement(s)
  the six fixture cells: 6 OK
```

The six the procedure names as the fixture all read the same in the baseline and from the script: PCP-005 passive 66.7, PCP-008 passive 67.7, RA-001 passive 64.2, RA-001 ', so ' 14.6, PCR-004 ', and '+clause 29.3, PCR-003 ', and '+clause 0.5. They are asserted by name inside --check-baseline so a reader does not have to trust a total.

Four blocks. `style` calls check_style.compare, which is what measure_baseline_style.txt is. `discourse` calls check_discourse.measure per column and prints check_discourse's own table, which is what measure_baseline_discourse.txt is. `extra` is the block round three had to compute in a session. `rule` is one row per document with every stopping-rule measure, its denominator, and a verdict. The gates are wrapped, not re-implemented: check_style.measure and check_discourse.measure are the authority for blocks one and two.

The rule block passes its own sanity check. Run over the 20 committed .qmd, PCR-003 is the ONLY PASS -- it is the control, already at round three -- and PCP-003 fails on exactly one line, ', and '+clause at 18.2 %, which is what decisions.scope_19_documents says about it. The other 18 fail on ', so ' and opens-with-a-connective as well. Chaining and copula are compared against each document's own baseline row and read +0.0 across all 20, which is the third proof the script reproduces the baseline.

Two definitions were recovered rather than invented, by re-deriving round three's published figures and keeping only the pattern that reproduces all four sources. The four subordination rows count OCCURRENCES over the whole prose divided by the sentence count -- a rate per 100 sentences, not the share of sentences that carry one. PCR-003 has 67 ', which' in 66 sentences and the published 15.33 % is 67/437; its 6 semicolons include only 1 inside a sentence the splitter kept, so a share-of-sentences reading gives 0.23 against the published 1.37. The possessive rates divide by len(text.split()), up to 19 % larger than the word count check_style divides by (ISPE TT: 22,216 against 18,731). Both are documented in the script where the patterns are defined.

WHAT REPRODUCES, AND THE ONE THING THAT DOES NOT. Exact on all four sources and on both documents round three's files cover: the staccato (runs, longest run, share), ', which', ', where', the semicolon, ', because', 'its', 'their', 'the <noun> is'. `it is/was` does not. Round three published 22 / 28 / 41 / 50 on the sources and 4 on PCP-003; the pattern here gives 18 / 28 / 40 / 50 and 3, and agrees on A-Mab, ISPE PV and PCR-003. Every candidate that lifts PDA TR 60 to 22 overshoots the other three, so the pattern cannot be recovered from its output and its method was never saved. That figure is not stale, it is uncheckable -- which is the exact failure this task exists to end. It is flagged in the printed row and named in the script.

Two bugs found and fixed while proving it. Reading the baseline header with a whitespace tokeniser split "PDA TR 60" into three columns and shifted every comparison one document sideways -- it reported 120 disagreements against a file it in fact matched. The header is now sliced at the table's own field width and each slice is checked against the name expected there, so a shift is reported instead of compared. And the chaining/copula comparison had no rounding tolerance: the baselines carry one decimal, so an unchanged document read "chaining -0.0, FAIL". ROUND_TOL is half a printed digit.

Also written: measure_trackd_baseline_run.txt, the full four-block table over the 20 committed .qmd as of this task, so the next session has the "before" without re-running the parser.

The round-three results page cites the script by path, as the acceptance requires, and states plainly that its `it is/was` row cannot be checked and that the script's figure is the one to read.

Gates at the boundary: make test 89 passed, make style 24 OK / 0 FAIL, 20/20 annexes valid, 2084/2084 quotes grounded with strict anchors and 0 weak anchors, `git diff outputs/ pc_package/ground_truth/` empty.

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCP-005** — `pc_package/PCP-005_protein_a.qmd`
- **PCP-008** — `pc_package/PCP-008_aex.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`
- **PCR-004** — `pc_package/PCR-004_harvest.qmd`
- **RA-001** — `pc_package/RA-001_risk_assessment.qmd`

## Files it touched

- `.claude/work/2026-08-18_02_register-track-d/measure_trackd.py`
- `.claude/work/2026-08-18_02_register-track-d/measure_baseline_style.txt`
- `.claude/work/2026-08-18_02_register-track-d/measure_baseline_discourse.txt`
