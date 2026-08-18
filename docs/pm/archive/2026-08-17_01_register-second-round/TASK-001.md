---
type: pm-task
epic: 2026-08-17_01_register-second-round
sprint: 2026-08-17_01_register-second-round
task: TASK-001
status: done
kind: mechanism
title: "Print clause packing and sentence-initial connectives in check_style.py, gated by nothing"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-003", "PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-17_01_register-second-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-001 — Print clause packing and sentence-initial connectives in check_style.py, gated by nothing

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-001.md in this work unit — numbered steps, code, commands and the output each must print. Follow it top to bottom.  WHERE. authoring/check_style.py: measure() at line 263 builds the dict m; connective_line() at 325 is the model for the new advisory line; render() at 338 prints it at line 352; compare() at 422 prints the connective rows at 447-452. Add the counts inside measure() next to '_connectives'.  THE PATTERNS, fixed so the numbers reproduce (they are what clause_pack.py in this unit runs): mid-sentence so = r',\s+so\s+' (case-insensitive) on the sentence; clause coordinators = r',\s+(so|and|but|since|because|which|while|whereas|yet)\s+' counted per sentence, '2+' means len(findall) >= 2; sentence-initial connective = the sentence matches r'^(However|Therefore|Consequently|As a result|In addition|For this reason|By contrast|In contrast|For example|Thus|Hence|Nevertheless|Nonetheless|Moreover|Furthermore|Instead|Rather|First|Second|Third|Finally|Overall)\b,?' (case-insensitive). Run over sentences(text) — the same list the length statistics use — so denominators agree with '_n_sent'.  WHY ADVISORY. The proposal and the pilot both say a floor on a discourse feature is met by typing the word; a ceiling on ', so ' is met by writing ', and' or ';'. So print the family together and gate nothing. Do NOT add to LIMITS; do not touch BANNED.  THE TRAP. sentences() replaces xrefs with 'Ref' and inline expressions are already 'NUM' from prose_from_qmd; a sentence beginning 'NUM' or 'Ref' is not a connective-led one, and the regex above already handles that. Keep the count on the sentence list, not on the raw text, or the denominator drifts from _n_sent.

## Acceptance criteria

- [x] measure() returns three new fields: '_pct_so_mid' (% of sentences containing mid-sentence ', so '), '_pct_initial_conn' (% of sentences whose first word is a connective from a fixed list), '_pct_coord2' (% of sentences with two or more clause coordinators), each with its count and denominator kept
- [x] render() prints them as ONE advisory line beside the connective line, marked '(diagnostic, never gated)'; LIMITS is unchanged at 12 entries and evaluate() ignores the new fields
- [x] compare() prints three new rows; `uv run python authoring/check_style.py --compare pc_package/PCR-003_bioreactor.qmd pc_package/PCP-003_bioreactor.qmd` shows, to one decimal: ', so ' PDA 0.1 / A-Mab 0.3 / ISPE TT 0.4 / ISPE PV 0.4 / PCR-003 8.0 / PCP-003 10.6; sentence-initial connective 4.8 / 6.1 / 4.2 / 3.7 / 0.9 / 1.8; 2+ coordinators 2.3 / 1.2 / 1.5 / 3.1 / 5.4 / 9.3
- [x] `uv run python authoring/check_style.py --selftest` still reports 4 of 4 human sources measured and passing
- [x] `make style PY="uv run python"` still passes 20/20 — no document newly fails, because nothing new is gated
- [x] tests/test_style.py exists: it feeds sentences() a fixture with two known packed sentences and one connective-led sentence and asserts the three counts; `make test PY="uv run python"` reports more than 85 passed

## What was built

check_style.py measures clause packing beside CONNECTIVES and gates nothing. Three regexes at module level, copied from clause_pack.py in this work unit so the numbers reproduce: CLAUSE_COORD (comma + one of so/and/but/since/because/which/while/whereas/yet), SO_MID, INITIAL_CONNECTIVE (21 openers, matched at the head of the sentence). measure() counts them over sentences(text), the same list _n_sent counts, and adds six underscore keys: _pct_so_mid, _pct_initial_conn, _pct_coord2 and their three numerators. evaluate() iterates LIMITS, not m, so nothing new is gated; len(LIMITS) stays 12 and tests/test_style.py asserts it.

render() prints one advisory line via packing_line(), directly under the connective line, carrying the source band [0.1-0.4 / 3.7-6.1 / 1.2-3.1] so the author reads the gap without opening the exploration. compare() gained three rows, placed before the (sentences of prose) row.

`uv run python authoring/check_style.py --compare pc_package/PCR-003_bioreactor.qmd pc_package/PCP-003_bioreactor.qmd` prints, in the planned columns (PDA TR 60 / A-Mab / ISPE TT / ISPE PV / PCR-003 / PCP-003):

% sentences with mid-sentence ', so ' (not gated)     0.1   0.3   0.4   0.4   8.0  10.6
% sentences opening with a connective (not gated)     4.8   6.1   4.2   3.7   0.9   1.8
% sentences with 2+ clause coordinators (not gated)   2.3   1.2   1.5   3.1   5.4   9.3

Every value matches the procedure to the decimal, so the gate now reads what clause_pack.py read.

Gates. --selftest: 4 of 4 human sources measured and passing. `make style PY="uv run python"`: exit 0, 24 OK lines (20 documents + the 4 sources), 0 FAIL -- no document newly fails. check_style.py on PCR-003 prints the packing line (', so ' 8.0 %, 34/423; opens with a connective 0.9 %, 4/423; 2+ coordinators 5.4 %) and still ends OK. tests/test_style.py is new and is the first direct test of sentences()/measure(); `make test PY="uv run python"` reports 88 passed, up from 85.

The corpus-wide picture the line now exposes: the worst document on the make style run packs ', so ' into 14.6 % of its sentences (24/164) and opens 0.0 % of them with a connective, which is the defect this round targets, printed on every run from here on.

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- `authoring/check_style.py`
- `tests/test_style.py`
