---
type: pm-task
epic: 2026-08-18_01_register-third-round
sprint: 2026-08-18_01_register-third-round
task: TASK-001
status: done
kind: mechanism
title: "Make the round-two owner-reading measure a file that reproduces its table, then move the two regex counts into check_style.py"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-003", "PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-18_01_register-third-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-001 — Make the round-two owner-reading measure a file that reproduces its table, then move the two regex counts into check_style.py

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-001.md. WHY FIRST: the round-two counts came from an inline heredoc that was never saved (exploration §3); measure_owner_reading.txt holds numbers with no code behind them. This task is the code, and its acceptance is that it reproduces that table exactly before it becomes the gate's line — the discipline TASK-001 of the previous unit applied to clause_pack.py. WHERE: check_style.py line 121-125 has CLAUSE_COORD / SO_MID / INITIAL_CONNECTIVE; add AND_CLAUSE and NOT_TAIL beside them with a comment saying the regex is a FLOOR (exploration §6b: it misses a second clause opening on a bare noun, 'and both were retained', and undercounts the corpus by 2-6 points while matching the sources within 0.5). measure() at 276, n_coord at 293, the _pct_ keys at 312-317, packing_line() at 358, compare() rows at 485-488. THE ORDER MATTERS: put ', and '+clause and ', not ' on the packing line AFTER the 2+ coordinator figure so the family reads left to right: so / opens-with-connective / 2+ / and-clause / not-tail. DO NOT add to LIMITS; do not touch BANNED. A ceiling on ', and ' is met by a semicolon and the semicolon ceiling already exists. THE CONTROL SENTENCE in the test must be an Oxford comma before a NOUN ('Galactosylation, high mannose, and afucosylation were measured.') and must NOT count — that is what separates the clause count from a comma count.

## Acceptance criteria

- [x] measure() returns two new fields, '_pct_and_clause' (% of sentences with a mid-sentence ', and ' followed by a clause opener) and '_pct_not_tail' (% with mid-sentence ', not '), each with its count; the patterns are exactly the ones in this unit's andclause.py / the TASK-008 heredoc: r",\s+and\s+(?:the|this|that|these|those|it|they|he|she|we|its|their|a|an|[a-z]+ing)\b" and r",\s+not\s+", both case-insensitive, run over sentences(text)
- [x] packing_line() prints them on the SAME advisory line, marked '(diagnostic, never gated)'; LIMITS is unchanged at 12 entries and evaluate() ignores the new fields
- [x] compare() prints two new rows before '(sentences of prose)'; `uv run python authoring/check_style.py --compare .claude/work/2026-08-16_01_register-from-four-sources/pre-rewrite/PCR-003_bioreactor.qmd .claude/work/2026-08-17_01_register-second-round/pre-rewrite/PCR-003_bioreactor.qmd pc_package/PCR-003_bioreactor.qmd pc_package/PCP-003_bioreactor.qmd` shows, to one decimal: ', and '+clause PDA 3.4 / A-Mab 1.1 / ISPE TT 1.3 / ISPE PV 3.1 / PCR-003 r0 24.9 / r1 21.0 / r2 22.6 / PCP-003 18.2; ', not ' 0.2 / 0.0 / 0.1 / 0.0 / 0.0 / 0.0 / 4.3 / 0.0 — the round-two figures in .claude/work/2026-08-17_01_register-second-round/measure_owner_reading.txt, reproduced exactly
- [x] `uv run python authoring/check_style.py --selftest` still reports 4 of 4; `make style PY="uv run python"` still 24 OK / 0 FAIL
- [x] tests/test_style.py gains a fixture with one ', and '+clause sentence, one ', not ' sentence, one Oxford-comma-before-a-noun sentence that must NOT count, and asserts the two counts; `make test PY="uv run python"` reports more than 88 passed

## What was built

The two regex counts the round-two owner reading produced from an unsaved heredoc now live in check_style.py, and they reproduce that table exactly.

AND_CLAUSE and NOT_TAIL sit beside CLAUSE_COORD / SO_MID / INITIAL_CONNECTIVE, with the patterns copied verbatim from this unit's andclause.py: r",\\s+and\\s+(?:the|this|that|these|those|it|they|he|she|we|its|their|a|an|[a-z]+ing)\\b" and r",\\s+not\\s+", both re.I. The comment above them says what the round-two reading was and states that AND_CLAUSE is a FLOOR: it misses a second clause opening on a bare noun, undercounts the corpus by 2-6 points and matches the four sources within 0.5, and the parser count in check_discourse.py is the other half. measure() counts both over sentences(text), the same list _n_sent counts, and adds four underscore keys: _pct_and_clause, _pct_not_tail, _n_and_clause, _n_not_tail. evaluate() iterates LIMITS, not m, so neither is gated; len(LIMITS) stays 12 and tests/test_style.py asserts it.

packing_line() prints them after the 2+ coordinator figure, so the family reads so / opens-with-connective / 2+ / and-clause / not-tail on one line marked "(diagnostic, never gated)", with the band extended to [sources: 0.1-0.4 / 3.7-6.1 / 1.2-3.1 / 1.1-3.4 / 0.0-0.2]. On PCR-003 it reads: ', so ' mid-sentence 0.0 % (0/421), opens with a connective 4.0 % (17/421), 2+ clause coordinators 1.7 %, ', and '+clause 22.6 % (95/421), ', not ' 4.3 % (18/421).

compare() gained two rows before (sentences of prose). The planned command over r0 / r1 / r2 / PCP-003 prints, in the columns PDA / A-Mab / ISPE TT / ISPE PV / PCR-003 r0 / r1 / r2 / PCP-003:

% sentences with ', and ' + a second clause (floor; not gated)   3.4  1.1  1.3  3.1  24.9  21.0  22.6  18.2
% sentences with mid-sentence ', not ' (not gated)               0.2  0.0  0.1  0.0   0.0   0.0   4.3   0.0

Every value matches measure_owner_reading.txt to the decimal, so the never-saved measure now has code behind it.

One thing beyond the procedure, reported rather than done silently: the ', and ' label is 62 characters against compare()'s 50-character label field, so that row's numbers printed two columns out of line with their headers. The label column in compare() is now 62 throughout, and the (sentences of prose) row's band column went from 9 to 11 to match the rest. Numbers unchanged; only the alignment.

Gates. --selftest: 4 of 4 human sources measured and passing. make style PY="uv run python": 24 OK lines, 0 FAIL, and check_style.py on PCR-003 still ends OK. tests/test_style.py gained test_and_clause_and_not_tail over a four-sentence fixture holding one ', and '+clause sentence, one ', not ' sentence, and the control Oxford comma before a noun ("Galactosylation, high mannose, and afucosylation were measured on one separation.") which must not count; it asserts 1 and 1. make test PY="uv run python": 89 passed, up from 88. No .qmd, guide or exemplar was touched.

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- `authoring/check_style.py`
- `tests/test_style.py`
