---
type: pm-task
epic: 2026-08-18_02_register-track-d
sprint: 2026-08-18_02_register-track-d
task: TASK-027
status: cancelled
kind: document
title: "Re-author PCMR-001 in one pass, as a DRAFT"
generated: true
waiting_on: ?
tags: [pm/task, pm/cancelled]
about: ["PCMR-001"]
---

> [!warning] Generated from `.claude/work/2026-08-18_02_register-track-d/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-027 — Re-author PCMR-001 in one pass, as a DRAFT

**Epic:** [[epic]] · **Status:** `cancelled` · **Waiting on:** ? · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/AUTHOR-A-DOCUMENT.md. Outline `master_report`. Baseline for this document is in measure_baseline_style.txt / measure_baseline_discourse.txt and is printed to the author by brief §5d. Annex exposure at promotion: 273 quotes, 49 rhetorical spans. Currently n/a. THE PASSIVE IS A BAND AND NEVER A FLOOR. The master report rolls up all eight pairs and is authored LAST. It has the second-largest annex in the corpus (273 quotes) and the largest rhetorical layer (49 spans).

## Acceptance criteria

- [ ] the current text is preserved first: `cp pc_package/PCMR-001_master_report.qmd .claude/work/2026-08-18_02_register-track-d/pre-rewrite/` and it equals `git show HEAD:pc_package/PCMR-001_master_report.qmd`
- [ ] `uv run --extra discourse python authoring/build_brief.py PCMR-001` regenerated first; §5d carries all twelve rows and §5c is empty for this document
- [ ] ONE agent authors the whole document in one pass from WRITING_GUIDE.md, REGISTER_EXEMPLAR.md, STORY_BIBLE.md, section_plan.yaml -> master_report and the PCMR-001 brief; it reads no pc_package/*.qmd and no authoring/rhetorical/*.spans.yaml
- [ ] `uv run python authoring/check_render.py pc_package/PCMR-001_master_report.DRAFT.qmd --render` passes including the style gate; the pdf is rendered SEPARATELY with the venv on PATH and glyph-checked fresh; the packing line is copied verbatim into the completion note
- [ ] `grep -c '<<NEEDS' <draft>` is 0 and no typed measurement survives the numeral advisory except statistical conventions
- [ ] `grep -c 'screening retained\|screening identified\|the design carries\|the model identifies\|the study selected' <draft>` is 0
- [ ] the committed pc_package/PCMR-001_master_report.qmd and all 20 annexes are untouched; git status shows only the DRAFT and its untracked renders

**Depends on:** [[TASK-026]]

## What was built

Cancelled 2026-08-18 by decision D3, settled STOP on the owner's reading of the pilot. See docs/results/2026-08-18-track-d-stopped.md.

## Documents it is about

- **PCMR-001** — `pc_package/PCMR-001_master_report.qmd`

## Files it touched

- `pc_package/PCMR-001_master_report.DRAFT.qmd`
- [[PCMR-001.brief]] — `authoring/out/PCMR-001.brief.md`
- `.claude/work/2026-08-18_02_register-track-d/pre-rewrite/PCMR-001_master_report.qmd`
