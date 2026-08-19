---
type: pm-task
epic: 2026-08-19_01_fourth-round-one-document
sprint: 2026-08-19_01_fourth-round-one-document
task: TASK-007
status: todo
kind: measurement
title: "Rebuild-and-reground proof after promotion: the corpus is whole"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
---

> [!warning] Generated from `.claude/work/2026-08-19_01_fourth-round-one-document/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-007 — Rebuild-and-reground proof after promotion: the corpus is whole

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

This is the rebuild-and-reground task the workflow requires, sized to one document: nothing upstream of a render changed except that document, so a `make data figures` is not needed and must not be run (outputs/ must stay identical). Nothing else under pc_package/ may have moved.

## Acceptance criteria

- [ ] runs ONLY if TASK-006 ran: `uv run python authoring/check_render.py pc_package/PCR-007_cex.qmd --render` -> chunks exec, no <<NEEDS>>, docx renders, tic gate OK, no missing glyph on the fresh pdf
- [ ] `cd pc_package && uv run python build_ground_truth.py && uv run python validate_annex.py && GROUNDING_STRICT_ANCHORS=1 uv run python check_grounding.py` -> 20/20 valid, N/N grounded (N as TASK-006 printed), exit 0
- [ ] `git diff --stat outputs/` empty; `make test PY="uv run python"` passes; `make style` 24 OK / 0 FAIL
- [ ] the depth band: PCR-007's new page count against CLAUDE.md's 'reports with a DoE run 41–56 pp' — inside, or the band re-measured and the sentence updated at ship (TASK-008)

**Depends on:** [[TASK-006]]

## Files it touched

- not recorded
