---
type: pm-task
epic: 2026-08-18_02_register-track-d
sprint: 2026-08-18_02_register-track-d
task: TASK-024
status: cancelled
kind: document
title: "Re-author PTP-001 in one pass, as a DRAFT"
generated: true
waiting_on: ?
tags: [pm/task, pm/cancelled]
about: ["PTP-001"]
---

> [!warning] Generated from `.claude/work/2026-08-18_02_register-track-d/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-024 — Re-author PTP-001 in one pass, as a DRAFT

**Epic:** [[epic]] · **Status:** `cancelled` · **Waiting on:** ? · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/AUTHOR-A-DOCUMENT.md. Outline `transfer_plan`. Baseline for this document is in measure_baseline_style.txt / measure_baseline_discourse.txt and is printed to the author by brief §5d. Annex exposure at promotion: 76 quotes, 0 rhetorical spans. Currently n/a. THE PASSIVE IS A BAND AND NEVER A FLOOR.

## Acceptance criteria

- [ ] the current text is preserved first: `cp pc_package/PTP-001_transfer.qmd .claude/work/2026-08-18_02_register-track-d/pre-rewrite/` and it equals `git show HEAD:pc_package/PTP-001_transfer.qmd`
- [ ] `uv run --extra discourse python authoring/build_brief.py PTP-001` regenerated first; §5d carries all twelve rows and §5c is empty for this document
- [ ] ONE agent authors the whole document in one pass from WRITING_GUIDE.md, REGISTER_EXEMPLAR.md, STORY_BIBLE.md, section_plan.yaml -> transfer_plan and the PTP-001 brief; it reads no pc_package/*.qmd and no authoring/rhetorical/*.spans.yaml
- [ ] `uv run python authoring/check_render.py pc_package/PTP-001_transfer.DRAFT.qmd --render` passes including the style gate; the pdf is rendered SEPARATELY with the venv on PATH and glyph-checked fresh; the packing line is copied verbatim into the completion note
- [ ] `grep -c '<<NEEDS' <draft>` is 0 and no typed measurement survives the numeral advisory except statistical conventions
- [ ] `grep -c 'screening retained\|screening identified\|the design carries\|the model identifies\|the study selected' <draft>` is 0
- [ ] the committed pc_package/PTP-001_transfer.qmd and all 20 annexes are untouched; git status shows only the DRAFT and its untracked renders

**Depends on:** [[TASK-022]]

## What was built

Cancelled 2026-08-18 by decision D3, settled STOP on the owner's reading of the pilot. See docs/results/2026-08-18-track-d-stopped.md.

## Documents it is about

- **PTP-001** — `pc_package/PTP-001_transfer.qmd`

## Files it touched

- `pc_package/PTP-001_transfer.DRAFT.qmd`
- [[PTP-001.brief]] — `authoring/out/PTP-001.brief.md`
- `.claude/work/2026-08-18_02_register-track-d/pre-rewrite/PTP-001_transfer.qmd`
