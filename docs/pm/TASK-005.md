---
type: pm-task
epic: 2026-08-17_01_register-second-round
sprint: 2026-08-17_01_register-second-round
task: TASK-005
status: todo
kind: document
title: "Re-author PCP-003 in one pass from the amended artifacts, as a DRAFT"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCP-003"]
---

> [!warning] Generated from `.claude/work/2026-08-17_01_register-second-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-005 — Re-author PCP-003 in one pass from the amended artifacts, as a DRAFT

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-005.md in this work unit — numbered steps, code, commands and the output each must print. Follow it top to bottom.  SEPARATE FROM TASK-006 on purpose: two documents in one task is a new instance of the self-reference loop. Two agents, one document each, neither reading the other's draft — the pilot's TASK-007 rule.  THE AUTHOR IS TOLD THE NUMBER THIS TIME. That is the round's hypothesis (decisions.same_method / proposal §'Why two moved and three did not'): round one withheld the measurement and only the substitution rules landed. §5d gives the author its own round-one packing figure and the target, and check_style prints the figure back on every check_render run. The author is NOT told to raise chaining or produce connectives to a count — the guide says a produced connective is a worse tell than a missing one.  NEVER PATCH. If the first draft comes back at 8 % ', so ', that is a result for TASK-008, not a reason to edit sentences. A second one-pass author is allowed; post-editing is not.  THE PLAN GENRE TRAP from round one: PCP-003 removed 25 possessives and added 23 copulas ('it is' 7→21), and went from inside the copula band (18.4 %) to outside all four sources (27.6 %). §2d bis now names the substitution; the author should see 'it is' as the thing not to write.  pct_under_15 has a 32 % ceiling and PCP-003 round one sits at 20.4 %; splitting one sentence in ten adds roughly 5–8 points, so there is room, and the author should know the ceiling exists.  RENDER THE PDF SEPARATELY (cd pc_package && quarto render PCP-003_bioreactor.DRAFT.qmd --to pdf) — check_render glyph-checks whatever pdf is on disk.

## Acceptance criteria

- [ ] before authoring, the round-one text is copied: cp pc_package/PCP-003_bioreactor.qmd .claude/work/2026-08-17_01_register-second-round/pre-rewrite/ (it equals `git show f06f1a7:pc_package/PCP-003_bioreactor.qmd`)
- [ ] `uv run python authoring/build_brief.py PCP-003` regenerated first, so the brief carries §5c (D-001) and §5d with the round-one numbers (10.6 % ', so ', 1.8 % initial connective)
- [ ] ONE agent authors the whole document in one pass from WRITING_GUIDE.md, REGISTER_EXEMPLAR.md, STORY_BIBLE.md, section_plan.yaml and the PCP-003 brief; it reads no sibling .qmd and not the PCR-003 draft
- [ ] `uv run python authoring/check_render.py pc_package/PCP-003_bioreactor.DRAFT.qmd --render` passes, including the embedded style gate; the advisory packing line it prints is copied into this task's completion note
- [ ] the D-001 at-set-point commitment appears in the draft (brief §5c says which sentence)
- [ ] no number is typed: every value is an inline {python} expression; the commercial scale is stated via V["commercial_scale_l"]
- [ ] the committed pc_package/PCP-003_bioreactor.qmd and all 20 annexes are untouched at the end of this task; git status shows only the DRAFT, its untracked render, the brief and the pre-rewrite copy

**Depends on:** [[TASK-002]], [[TASK-004]]

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`

## Files it touched

- `pc_package/PCP-003_bioreactor.DRAFT.qmd`
- [[PCP-003.brief]] — `authoring/out/PCP-003.brief.md`
- `.claude/work/2026-08-17_01_register-second-round/pre-rewrite/PCP-003_bioreactor.qmd`
