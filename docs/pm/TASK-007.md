---
type: pm-task
epic: 2026-08-19_01_fourth-round-one-document
sprint: 2026-08-19_01_fourth-round-one-document
task: TASK-007
status: done
kind: measurement
title: "Rebuild-and-reground proof after promotion: the corpus is whole"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCR-007"]
---

> [!warning] Generated from `.claude/work/2026-08-19_01_fourth-round-one-document/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-007 — Rebuild-and-reground proof after promotion: the corpus is whole

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

This is the rebuild-and-reground task the workflow requires, sized to one document: nothing upstream of a render changed except that document, so a `make data figures` is not needed and must not be run (outputs/ must stay identical). Nothing else under pc_package/ may have moved.

## Acceptance criteria

- [x] runs ONLY if TASK-006 ran: `uv run python authoring/check_render.py pc_package/PCR-007_cex.qmd --render` -> chunks exec, no <<NEEDS>>, docx renders, tic gate OK, no missing glyph on the fresh pdf
- [x] `cd pc_package && uv run python build_ground_truth.py && uv run python validate_annex.py && GROUNDING_STRICT_ANCHORS=1 uv run python check_grounding.py` -> 20/20 valid, N/N grounded (N as TASK-006 printed), exit 0
- [x] `git diff --stat outputs/` empty; `make test PY="uv run python"` passes; `make style` 24 OK / 0 FAIL
- [x] the depth band: PCR-007's new page count against CLAUDE.md's 'reports with a DoE run 41–56 pp' — inside, or the band re-measured and the sentence updated at ship (TASK-008)

**Depends on:** [[TASK-006]]

## What was built

Run 2026-08-19 after TASK-006. `check_render.py pc_package/PCR-007_cex.qmd --render` -> all chunks exec, all inline expressions eval, no <<NEEDS>>, no gated tic and no banned phrase, quarto docx render OK, no missing glyph (the numeral lint's three hits are α = 0.05 and two 95 % interval levels, permitted). `build_ground_truth.py && validate_annex.py` -> 20/20 annexes valid; `GROUNDING_STRICT_ANCHORS=1 check_grounding.py` -> 2084/2084 quotes grounded across 20 annexes, exit 0 — also re-run against the COMMITTED docx after the --render rewrote it (the re-render changes bytes, not text; the docx was restored by name, never by directory, and grounding reads 2084/2084 against the committed file). `git diff --stat outputs/` empty; make test 95 passed; make style 24 OK / 0 FAIL; `git status --short` clean. Depth band: the promoted PCR-007 is 50 pp, inside CLAUDE.md's 'reports with a DoE run 41–56 pp' (it was 51); no band sentence to re-measure.

## Documents it is about

- **PCR-007** — `pc_package/PCR-007_cex.qmd`

## Files it touched

- not recorded
