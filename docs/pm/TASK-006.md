---
type: pm-task
epic: 2026-08-17_01_register-second-round
sprint: 2026-08-17_01_register-second-round
task: TASK-006
status: todo
kind: document
title: "Re-author PCR-003 in one pass from the amended artifacts, as a DRAFT"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-17_01_register-second-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-006 — Re-author PCR-003 in one pass from the amended artifacts, as a DRAFT

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-006.md in this work unit — numbered steps, code, commands and the output each must print. Follow it top to bottom.  SEPARATE FROM TASK-005 on purpose; same rules. PCR-003 is the document the owner read twice and quoted from; it is 9,631 words and carries D-002 and the curated 35-span rhetorical layer (authoring/rhetorical/PCR-003.spans.yaml), which TASK-007 re-curates — the author does not look at the spans file.  THE TWO SENTENCES THE OWNER QUOTED are in the round-one text at lines 701 and 707 (Discussion). They are ✗ examples in the guide now (TASK-002); the author will meet them there and nowhere else.  THE AUTHOR IS TOLD THE NUMBER (see TASK-005 notes) and not told to hit a chaining figure.  NEVER PATCH.  RENDER THE PDF SEPARATELY.

## Acceptance criteria

- [ ] before authoring, the round-one text is copied: cp pc_package/PCR-003_bioreactor.qmd .claude/work/2026-08-17_01_register-second-round/pre-rewrite/ (it equals `git show f06f1a7:pc_package/PCR-003_bioreactor.qmd`)
- [ ] `uv run python authoring/build_brief.py PCR-003` regenerated first, so the brief carries §5c (D-002) and §5d with the round-one numbers (8.0 % ', so ', 0.9 % initial connective, chaining 30.7 %)
- [ ] ONE agent authors the whole document in one pass from WRITING_GUIDE.md, REGISTER_EXEMPLAR.md, STORY_BIBLE.md, section_plan.yaml and the PCR-003 brief; it reads no sibling .qmd and not the PCP-003 draft
- [ ] `uv run python authoring/check_render.py pc_package/PCR-003_bioreactor.DRAFT.qmd --render` passes, including the embedded style gate; the advisory packing line it prints is copied into this task's completion note
- [ ] the D-002 absolute appears UNQUALIFIED in the draft, followed by the narrower true elaboration (brief §5c)
- [ ] the Discussion names the four response-surface factors where it counts them, and the report states the commercial scale via V["commercial_scale_l"]
- [ ] no inline expression that yields a response or parameter name is the agreeing subject of a clause (the 'acidic variants is' fault); every value is an inline {python} expression
- [ ] the committed pc_package/PCR-003_bioreactor.qmd and all 20 annexes are untouched at the end of this task

**Depends on:** [[TASK-002]], [[TASK-004]]

## Documents it is about

- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- `pc_package/PCR-003_bioreactor.DRAFT.qmd`
- [[PCR-003.brief]] — `authoring/out/PCR-003.brief.md`
- `.claude/work/2026-08-17_01_register-second-round/pre-rewrite/PCR-003_bioreactor.qmd`
