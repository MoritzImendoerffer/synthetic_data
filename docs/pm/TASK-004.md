---
type: pm-task
epic: 2026-08-18_02_register-track-d
sprint: 2026-08-18_02_register-track-d
task: TASK-004
status: todo
kind: document
title: "Re-author PCR-005 in one pass, as a DRAFT"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCR-005"]
---

> [!warning] Generated from `.claude/work/2026-08-18_02_register-track-d/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-004 — Re-author PCR-005 in one pass, as a DRAFT

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/AUTHOR-A-DOCUMENT.md. Outline `report_doe`. Baseline for this document is in measure_baseline_style.txt / measure_baseline_discourse.txt and is printed to the author by brief §5d. Annex exposure at promotion: 123 quotes, 39 rhetorical spans. Currently 43 pp. THE PASSIVE IS A BAND AND NEVER A FLOOR. PILOT, and one of the three the project owner reads. The only pilot document with a rhetorical layer, so it is the one that tests TASK-001's converted YAML end to end.

## Acceptance criteria

- [ ] the current text is preserved first: `cp pc_package/PCR-005_protein_a.qmd .claude/work/2026-08-18_02_register-track-d/pre-rewrite/` and it equals `git show HEAD:pc_package/PCR-005_protein_a.qmd`
- [ ] `uv run --extra discourse python authoring/build_brief.py PCR-005` regenerated first; §5d carries all twelve rows and §5c is empty for this document
- [ ] ONE agent authors the whole document in one pass from WRITING_GUIDE.md, REGISTER_EXEMPLAR.md, STORY_BIBLE.md, section_plan.yaml -> report_doe and the PCR-005 brief; it reads no pc_package/*.qmd and no authoring/rhetorical/*.spans.yaml
- [ ] `uv run python authoring/check_render.py pc_package/PCR-005_protein_a.DRAFT.qmd --render` passes including the style gate; the pdf is rendered SEPARATELY with the venv on PATH and glyph-checked fresh; the packing line is copied verbatim into the completion note
- [ ] `grep -c '<<NEEDS' <draft>` is 0 and no typed measurement survives the numeral advisory except statistical conventions
- [ ] `grep -c 'screening retained\|screening identified\|the design carries\|the model identifies\|the study selected' <draft>` is 0
- [ ] the committed pc_package/PCR-005_protein_a.qmd and all 20 annexes are untouched; git status shows only the DRAFT and its untracked renders

**Depends on:** [[TASK-001]], [[TASK-002]]

## Documents it is about

- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`

## Files it touched

- `pc_package/PCR-005_protein_a.DRAFT.qmd`
- [[PCR-005.brief]] — `authoring/out/PCR-005.brief.md`
- `.claude/work/2026-08-18_02_register-track-d/pre-rewrite/PCR-005_protein_a.qmd`
