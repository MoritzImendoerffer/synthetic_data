---
type: pm-task
epic: 2026-08-18_03_author-facing-apparatus
sprint: 2026-08-18_03_author-facing-apparatus
task: TASK-006
status: todo
kind: mechanism
title: "Split the register gate into GATED tics and ADVISORY signals; the author sees pass/fail, the reviewer sees the table"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
---

> [!warning] Generated from `.claude/work/2026-08-18_03_author-facing-apparatus/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-006 — Split the register gate into GATED tics and ADVISORY signals; the author sees pass/fail, the reviewer sees the table

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

Runs only on D4 = PASS. Do NOT move any band edge — the two-sided length bands stop being gated, they are not widened. The self-test must keep proving all four sources pass GATED. `paren` has a floor of 3.0 today; it moves to ADVISORY with the length rows because a floor on parentheses is a floor on a habit, not a tic.

## Acceptance criteria

- [ ] check_style.py: `LIMITS` becomes `GATED` = {em_dash, semicolon, colon, bold, multi_hyphen, rather_than} + BANNED, and `ADVISORY` = {mean_len, median_len, pct_over_40, pct_over_55, pct_under_15, paren} + the clause-packing family; `evaluate()` fails only on GATED; `--selftest` passes on all four sources for GATED and prints the ADVISORY table without failing
- [ ] `uv run python authoring/check_style.py --review <qmd>` prints the full table (GATED + ADVISORY, per-source columns, connectives, clause packing, longest sentences); without --review the tool prints only `OK`/`FAIL` and the failing GATED rows
- [ ] check_render.py's register block prints pass/fail and failing GATED rows only — `uv run python authoring/check_render.py pc_package/PCR-003_bioreactor.qmd | grep -c 'mean sentence length'` → 0
- [ ] `make style PY="uv run python"` → 24 OK / 0 FAIL (GATED is a subset of today's LIMITS, so nothing may go red); `make test PY="uv run python"` passes with tests/test_style.py::test_limits_unchanged rewritten to pin `len(GATED) == 6` and `len(ADVISORY) == 6` and the count printed in the outcome
- [ ] the probe from TASK-003 passes GATED (`check_style.py pc_package/PCR-005_protein_a.PROBE.qmd` → OK) and its length rows appear under --review
- [ ] CLAUDE.md Voice rule no longer says the thresholds on sentence length are enforced, and the sentence 'a measure that is printed back to the author moves, and one that is not drifts' is replaced by: the author sees pass/fail on the tics; the reviewer reads the table with `--review`; a length band is a signal for the reviewer and never a target for the author. WRITING_GUIDE §4a's table is split into the two sets (or, if TASK-008 has already replaced the guide, the new guide's tic list matches GATED exactly)

**Depends on:** [[TASK-004]]

## Files it touched

- `authoring/check_style.py`
- `authoring/check_render.py`
- `tests/test_style.py`
- `CLAUDE.md`
- [[WRITING_GUIDE]] — `authoring/WRITING_GUIDE.md`
