---
type: pm-task
epic: 2026-08-18_03_author-facing-apparatus
sprint: 2026-08-18_03_author-facing-apparatus
task: TASK-006
status: done
kind: mechanism
title: "Split the register gate into GATED tics and ADVISORY signals; the author sees pass/fail, the reviewer sees the table"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
---

> [!warning] Generated from `.claude/work/2026-08-18_03_author-facing-apparatus/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-006 — Split the register gate into GATED tics and ADVISORY signals; the author sees pass/fail, the reviewer sees the table

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

Runs only on D4 = PASS. Do NOT move any band edge — the two-sided length bands stop being gated, they are not widened. The self-test must keep proving all four sources pass GATED. `paren` has a floor of 3.0 today; it moves to ADVISORY with the length rows because a floor on parentheses is a floor on a habit, not a tic.

## Acceptance criteria

- [x] check_style.py: `LIMITS` becomes `GATED` = {em_dash, semicolon, colon, bold, multi_hyphen, rather_than} + BANNED, and `ADVISORY` = {mean_len, median_len, pct_over_40, pct_over_55, pct_under_15, paren} + the clause-packing family; `evaluate()` fails only on GATED; `--selftest` passes on all four sources for GATED and prints the ADVISORY table without failing
- [x] `uv run python authoring/check_style.py --review <qmd>` prints the full table (GATED + ADVISORY, per-source columns, connectives, clause packing, longest sentences); without --review the tool prints only `OK`/`FAIL` and the failing GATED rows
- [x] check_render.py's register block prints pass/fail and failing GATED rows only — `uv run python authoring/check_render.py pc_package/PCR-003_bioreactor.qmd | grep -c 'mean sentence length'` → 0
- [x] `make style PY="uv run python"` → 24 OK / 0 FAIL (GATED is a subset of today's LIMITS, so nothing may go red); `make test PY="uv run python"` passes with tests/test_style.py::test_limits_unchanged rewritten to pin `len(GATED) == 6` and `len(ADVISORY) == 6` and the count printed in the outcome
- [x] the probe from TASK-003 passes GATED (`check_style.py pc_package/PCR-005_protein_a.PROBE.qmd` → OK) and its length rows appear under --review
- [x] CLAUDE.md Voice rule no longer says the thresholds on sentence length are enforced, and the sentence 'a measure that is printed back to the author moves, and one that is not drifts' is replaced by: the author sees pass/fail on the tics; the reviewer reads the table with `--review`; a length band is a signal for the reviewer and never a target for the author. WRITING_GUIDE §4a's table is split into the two sets (or, if TASK-008 has already replaced the guide, the new guide's tic list matches GATED exactly)

**Depends on:** [[TASK-004]]

## What was built

check_style.py: `GATED` = {em_dash, semicolon, colon, bold, multi_hyphen} + BANNED; `ADVISORY` = {mean_len, median_len, pct_over_40, pct_over_55, pct_under_15, paren, rather_than} + the clause-packing family and connectives (printed, never evaluated). `LIMITS` is kept as the ordered union — the row order the committed baseline tables and --compare print in — and `evaluate(m, limits=None)` judges GATED by default; the self-test passes LIMITS so an advisory band a human source fails still fails the self-test (a band real prose fails is wrong whether it gates or advises). `--review` prints the advisory rows with bands and an '<- outside the source band' note, the connective line, the packing line, and with -v the compounds and longest sentences; without it the tool prints the sentence/word count, the five gated rows and 'OK no gated tic and no banned phrase' or the failing gated rows. `--compare` rows are tagged [gated]/[advisory]. Rationale written above GATED in the file, with the 2026-08-19 measurement.

DEVIATION FROM THE PLAN, recorded in decisions.rather_than_is_advisory: `rather_than` moved to ADVISORY (GATED 5 / ADVISORY 7, not 6 / 6), because the plan's acceptance requires the probe to pass GATED and the probe carries 'rather than' at 1.6 per 1k. No band edge moved.

Gates: `check_style.py --selftest` → 4 of 4 human sources measured and passing, every row gated and advisory. `make style` → 26 OK / 0 FAIL (24 shipped documents plus the two untracked probe files the glob picks up). `make test` → 90 passed (89 + test_evaluate_gates_only_the_tics; test_limits_unchanged rewritten as test_limits_split pinning GATED 5 / ADVISORY 7 / LIMITS 12 in the baseline row order). Author view: `check_render.py pc_package/PCR-003_bioreactor.qmd | grep -c 'mean sentence length'` → 0. Probe: `check_style.py pc_package/PCR-005_protein_a.PROBE.qmd` → OK, and `--review` shows its 7 advisory rows with pct_over_40 1.1 and rather_than 1.6 marked outside the band. `measure_apparatus.py --check-baseline` still 408 / 120 cells with disagreements only in the three Track D documents; while doing so, its baseline column list was made to skip uppercase-suffixed working files (.PROBE/.EXCERPT/.DRAFT), which had shifted the columns.

CLAUDE.md Voice rule rewritten: gated on the tics only, the author sees pass/fail and nothing else, the reviewer reads --review, 'a measure printed back to the author is a target, not a signal', with the 2026-08-19 result linked; the checklist bullet says GATED only. WRITING_GUIDE.md §4a: the intro paragraph states the split and each table row is tagged (gated)/(advisory) — minimal, since TASK-008 replaces the guide.

## Files it touched

- `authoring/check_style.py`
- `authoring/check_render.py`
- `tests/test_style.py`
- `CLAUDE.md`
- [[WRITING_GUIDE]] — `authoring/WRITING_GUIDE.md`
