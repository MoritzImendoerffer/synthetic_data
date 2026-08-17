---
type: pm-task
epic: 2026-08-17_01_register-second-round
sprint: 2026-08-17_01_register-second-round
task: TASK-004
status: todo
kind: mechanism
title: "Give the brief a \u00a75d that prints the discourse targets and the document's own current numbers"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCP-003"]
---

> [!warning] Generated from `.claude/work/2026-08-17_01_register-second-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-004 — Give the brief a §5d that prints the discourse targets and the document's own current numbers

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-004.md in this work unit — numbered steps, code, commands and the output each must print. Follow it top to bottom.  WHERE. authoring/build_brief.py:build() writes sections with w(); §5c is emitted at line ~415 by w(_discrepancy_assignments(doc_id)) and §6 starts at line 417. Insert §5d between them, always emitted (the same rule as 5c: a section that disappears is indistinguishable from one that stopped being generated).  HOW TO GET THE NUMBERS. sys.path already reaches authoring/ — import check_style and call measure(prose_from_qmd(path)) on pc_package/<DOC>_<uokey>.qmd; the uokey→filename map is in _pcpkg's DOC_REGISTRY. For spaCy rows: subprocess `python authoring/check_discourse.py --json --cap <qmd>` and read stdout; if it prints the one degrade line, print 'not measured'. Do not import spacy in build_brief.py itself.  THE DECISION (plan, overrulable): §5d prints numbers and rules and never generates prose. The proposal said the brief 'can generate worked chains from the document's own grounded facts'; a template-generated chain is machine prose handed to the author, which is the loop this repository has already paid for once. Worked corrections stay in the guide (TASK-002).  THIS IS THE PILOT'S HYPOTHESIS MADE CONCRETE: 'an author can execute and self-verify a substitution and cannot self-verify a rate' — so the brief gives the author the substitution AND the number, and check_style prints the number back on every render.  THE SCALE LINE. V is report_values (outputs/report_values.json); PCP-003 line 91 already does scale_l = V["commercial_scale_l"]. Point the author at it; do not type 15,000.

## Acceptance criteria

- [ ] `uv run python authoring/build_brief.py PCR-003` emits '## 5d. Discourse targets' between §5c and §6, with a table: measure | PDA TR 60 | A-Mab | ISPE TT | ISPE PV | this document as it stands — for the three TASK-001 measures (from check_style.measure on pc_package/PCR-003_bioreactor.qmd: 8.0 / 0.9 / 5.4) and, when spaCy is importable, chaining / copula / front field from check_discourse (30.7 / 32.5 / 9.2 with --cap semantics stated); when spaCy is absent those rows read 'not measured — uv sync --extra discourse' and the brief still builds
- [ ] `uv run python authoring/build_brief.py PCP-003` emits the same section with 10.6 / 1.8 / 9.3
- [ ] §5d restates, verbatim from the guide, the four rules as substitutions with their search strings: one step per sentence → connective opens the next; article or noun, never 'it is'; name the set you count; runtime nouns never as agreeing subjects — and the round's targets (', so ' ≤ 1.0 %, initial connective ≥ 3.0 %, chaining and copula not regressing) with the sentence 'these are printed by check_style.py on every run of check_render.py'
- [ ] §5d contains NO generated example sentence — no template prose; grep for a '> ✓' or '✗' block in the emitted §5d returns nothing
- [ ] §1 Identity gains one line: the report must state the commercial scale, pulled as V["commercial_scale_l"] (config/parameters.yaml line 24, 15000), because the round-one PCR-003 never states it
- [ ] a document with no .qmd on disk gets §5d with 'no previous revision' in the document column rather than a crash
- [ ] `make test PY="uv run python"` passes; `cd pc_package && uv run python build_ground_truth.py && uv run python validate_annex.py` still 20/20 (the brief touches no annex)

**Depends on:** [[TASK-001]], [[TASK-003]]

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`

## Files it touched

- `authoring/build_brief.py`
