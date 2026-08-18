---
type: pm-task
epic: 2026-08-18_02_register-track-d
sprint: 2026-08-18_02_register-track-d
task: TASK-011
status: todo
kind: document
title: "Re-author PCR-006 in one pass, as a DRAFT"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCR-006"]
---

> [!warning] Generated from `.claude/work/2026-08-18_02_register-track-d/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-011 — Re-author PCR-006 in one pass, as a DRAFT

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/AUTHOR-A-DOCUMENT.md. Outline `report_doe`. Baseline for this document is in measure_baseline_style.txt / measure_baseline_discourse.txt and is printed to the author by brief §5d. Annex exposure at promotion: 102 quotes, 31 rhetorical spans. Currently 44 pp. CARRIES D-001: brief §5c assigns it, and TASKS.md item 7 is the failure mode -- a re-authored document loses it silently. THE PASSIVE IS A BAND AND NEVER A FLOOR.

## Acceptance criteria

- [ ] the current text is preserved first: `cp pc_package/PCR-006_viral_inactivation.qmd .claude/work/2026-08-18_02_register-track-d/pre-rewrite/` and it equals `git show HEAD:pc_package/PCR-006_viral_inactivation.qmd`
- [ ] `uv run --extra discourse python authoring/build_brief.py PCR-006` regenerated first; §5d carries all twelve rows and §5c carries D-001
- [ ] ONE agent authors the whole document in one pass from WRITING_GUIDE.md, REGISTER_EXEMPLAR.md, STORY_BIBLE.md, section_plan.yaml -> report_doe and the PCR-006 brief; it reads no pc_package/*.qmd and no authoring/rhetorical/*.spans.yaml
- [ ] `uv run python authoring/check_render.py pc_package/PCR-006_viral_inactivation.DRAFT.qmd --render` passes including the style gate; the pdf is rendered SEPARATELY with the venv on PATH and glyph-checked fresh; the packing line is copied verbatim into the completion note
- [ ] `grep -c '<<NEEDS' <draft>` is 0 and no typed measurement survives the numeral advisory except statistical conventions
- [ ] `grep -c 'screening retained\|screening identified\|the design carries\|the model identifies\|the study selected' <draft>` is 0
- [ ] the committed pc_package/PCR-006_viral_inactivation.qmd and all 20 annexes are untouched; git status shows only the DRAFT and its untracked renders

**Depends on:** [[TASK-007]]

## Documents it is about

- **PCR-006** — `pc_package/PCR-006_viral_inactivation.qmd`

## Files it touched

- `pc_package/PCR-006_viral_inactivation.DRAFT.qmd`
- [[PCR-006.brief]] — `authoring/out/PCR-006.brief.md`
- `.claude/work/2026-08-18_02_register-track-d/pre-rewrite/PCR-006_viral_inactivation.qmd`
