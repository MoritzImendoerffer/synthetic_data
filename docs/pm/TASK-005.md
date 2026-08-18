---
type: pm-task
epic: 2026-08-18_02_register-track-d
sprint: 2026-08-18_02_register-track-d
task: TASK-005
status: todo
kind: document
title: "Re-author RA-001 in one pass, as a DRAFT"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["RA-001"]
---

> [!warning] Generated from `.claude/work/2026-08-18_02_register-track-d/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-005 — Re-author RA-001 in one pass, as a DRAFT

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/AUTHOR-A-DOCUMENT.md. Outline `risk_assessment`. Baseline for this document is in measure_baseline_style.txt / measure_baseline_discourse.txt and is printed to the author by brief §5d. Annex exposure at promotion: 317 quotes, 0 rhetorical spans. Currently n/a. THE PASSIVE IS A BAND AND NEVER A FLOOR. PILOT, and one of the three the project owner reads. NEVER RE-AUTHORED, and the largest annex in the corpus at 317 quotes -- the worst case for re-anchoring, which is why it is in the pilot rather than discovered at task 25. Outline risk_assessment; content source is risk_assessment/build_fmea.py.

## Acceptance criteria

- [ ] the current text is preserved first: `cp pc_package/RA-001_risk_assessment.qmd .claude/work/2026-08-18_02_register-track-d/pre-rewrite/` and it equals `git show HEAD:pc_package/RA-001_risk_assessment.qmd`
- [ ] `uv run --extra discourse python authoring/build_brief.py RA-001` regenerated first; §5d carries all twelve rows and §5c is empty for this document
- [ ] ONE agent authors the whole document in one pass from WRITING_GUIDE.md, REGISTER_EXEMPLAR.md, STORY_BIBLE.md, section_plan.yaml -> risk_assessment and the RA-001 brief; it reads no pc_package/*.qmd and no authoring/rhetorical/*.spans.yaml
- [ ] `uv run python authoring/check_render.py pc_package/RA-001_risk_assessment.DRAFT.qmd --render` passes including the style gate; the pdf is rendered SEPARATELY with the venv on PATH and glyph-checked fresh; the packing line is copied verbatim into the completion note
- [ ] `grep -c '<<NEEDS' <draft>` is 0 and no typed measurement survives the numeral advisory except statistical conventions
- [ ] `grep -c 'screening retained\|screening identified\|the design carries\|the model identifies\|the study selected' <draft>` is 0
- [ ] the committed pc_package/RA-001_risk_assessment.qmd and all 20 annexes are untouched; git status shows only the DRAFT and its untracked renders

**Depends on:** [[TASK-001]], [[TASK-002]]

## Documents it is about

- **RA-001** — `pc_package/RA-001_risk_assessment.qmd`

## Files it touched

- `pc_package/RA-001_risk_assessment.DRAFT.qmd`
- [[RA-001.brief]] — `authoring/out/RA-001.brief.md`
- `.claude/work/2026-08-18_02_register-track-d/pre-rewrite/RA-001_risk_assessment.qmd`
