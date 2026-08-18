---
type: pm-task
epic: 2026-08-18_01_register-third-round
sprint: 2026-08-18_01_register-third-round
task: TASK-004
status: todo
kind: document
title: "Re-author PCR-003 in one pass from the amended artifacts, as a DRAFT"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCP-003", "PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-18_01_register-third-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-004 — Re-author PCR-003 in one pass from the amended artifacts, as a DRAFT

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-004.md — the previous unit's TASK-006 procedure with the round-three brief. ONE GENRE ONLY, by owner decision (proposal, 'shape of the next round'): PCP-003 is NOT re-authored. Its §5d row is generated anyway (it costs nothing) and it is the CONTROL — if a measure moves in PCR-003 the page says 'moved in the report'. THE AUTHOR IS TOLD THE NUMBER for all eight measures now (three new + five from round two) and the two new substitutions. It is NOT told to write more passives to hit a count; the rule is 'where the sources would write a passive, write the passive', and the passive figure is a band the report is under. PREDICTED OVERSHOOT (exploration §3): expect ', and '+clause to go to ~0 %, below the sources' 1.1-3.4, the way ', so ' did. That is a result for TASK-006, not a reason to edit a sentence. NEVER PATCH. Second one-pass author allowed; post-editing is not. pct_under_15 has a 32 % ceiling and round two sits at 19.5 %; splitting the ', and ' clauses adds short sentences — the author should know the ceiling. RENDER THE PDF SEPARATELY with PATH="$PWD/.venv/bin:$PATH"; check_render glyph-checks whatever pdf is on disk.

## Acceptance criteria

- [ ] before authoring, the round-two text is copied: `cp pc_package/PCR-003_bioreactor.qmd .claude/work/2026-08-18_01_register-third-round/pre-rewrite/` and it equals `git show e7a4768:pc_package/PCR-003_bioreactor.qmd`
- [ ] `uv run --extra discourse python authoring/build_brief.py PCR-003` regenerated first; §5c carries D-002 and §5d carries the round-two numbers (', and '+clause 22.6, ', not ' 4.3, passive 34.4, plus the five round-two measures)
- [ ] ONE agent authors the whole document in one pass from WRITING_GUIDE.md, REGISTER_EXEMPLAR.md, STORY_BIBLE.md, section_plan.yaml and the PCR-003 brief; it reads no pc_package/*.qmd and not authoring/rhetorical/PCR-003.spans.yaml
- [ ] `uv run python authoring/check_render.py pc_package/PCR-003_bioreactor.DRAFT.qmd --render` passes including the style gate; the pdf is rendered SEPARATELY with the venv on PATH and glyph-checked fresh; the packing line (now five figures) is copied verbatim into the completion note
- [ ] the D-002 absolute appears UNQUALIFIED in the introduction with the true elaboration following; the commercial scale is stated via V["commercial_scale_l"]; the Discussion names the four factors it counts
- [ ] no inline expression yielding a name is an agreeing subject (grep from the previous unit's TASK-006 §4 returns nothing); `grep -c 'screening retained\|screening identified\|the design carries\|the model identifies' pc_package/PCR-003_bioreactor.DRAFT.qmd` is 0
- [ ] the committed pc_package/PCR-003_bioreactor.qmd, pc_package/PCP-003_bioreactor.qmd and all 20 annexes are untouched; git status shows only the DRAFT and its untracked renders

**Depends on:** [[TASK-003]]

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- `pc_package/PCR-003_bioreactor.DRAFT.qmd`
- [[PCR-003.brief]] — `authoring/out/PCR-003.brief.md`
- `.claude/work/2026-08-18_01_register-third-round/pre-rewrite/PCR-003_bioreactor.qmd`
