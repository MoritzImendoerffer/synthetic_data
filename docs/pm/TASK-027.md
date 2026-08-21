---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-027
status: done
kind: measurement
title: "Rebuild-and-reground proof after batch B3"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-004", "PCP-006", "PCP-008", "PCP-009", "PCP-010", "PCR-004", "PCR-010"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-027 — Rebuild-and-reground proof after batch B3

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

No make data figures.

## Acceptance criteria

- [x] `check_render.py --render` clean on every promoted document of the batch (glyphs on fresh pdfs; docx restored by name afterwards); 20/20 valid; N/N grounded strict, exit 0; `git diff --stat outputs/` empty; make test; make style 24 OK; page counts against CLAUDE.md's bands, re-measured at ship if moved

**Depends on:** [[TASK-025]]

## What was built

Rebuild-and-reground proof after B3, no `make data figures`. The six promoted documents (PCP-004, PCP-006, PCP-008, PCP-009, PCP-010, PCR-004) were re-rendered from source with the venv on PATH — fresh pdf first, then `check_render.py --render` so the glyph check reads a fresh pdf and not a stale one. All six exit 0: every chunk execs, every inline expression evals, no `<<NEEDS:>>`, all five gated tic rows ok, docx renders, no missing glyph on any fresh pdf. The only FAIL lines are the ADVISORY numeral lint on five of the six (PCP-004 4 lines, PCP-006 8, PCP-008 3, PCP-009 4, PCP-010 6; PCR-004 clean under 21 exemptions), and every listed line is a statistical convention (α = 0.05, p < 0.05, the 95 % interval), a coded design level (−1/+1/0) or the method name A280 — no typed measurement. Strict grounding was run FIRST against the freshly rendered docx: 2088/2088 quotes grounded across 20 annexes, exit 0, 0 weak anchors, which is the reproducibility statement — re-rendering from the same qmd yields text carrying every annex quote. The twelve rendered files were then restored BY NAME and verified bit-for-bit against md5s taken before the run; `git status --short` showed those twelve and nothing else had changed, so no sibling drifted. Everything re-verified against the committed renders: `build_ground_truth.py` rewrote all 20 annexes byte-identically (tree clean after it), 20/20 valid, 2088/2088 grounded strict, exit 0, 0 weak anchors, weak_claims 0 in all 20; `git diff --stat outputs/` empty; make test 95 passed; make style exit 0 with 24 blocks OK / 0 FAIL, including the 4-of-4 human-source selftest and check_exemplar_quotes; tree clean. PAGE COUNTS, fresh and committed pdfs identical page for page: the five plans 27 / 29 / 29 / 28 / 25 pp, all inside CLAUDE.md's 23–31 plan band. PCR-004 is 33 pp against the measured non-DoE report band of 26–28. It was 31 pp as attempt 1 at the B2 proof and attempt 2 is 2 pp longer, so that band is now missed by the same document twice and by PCR-010 (30 pp) at B1; flagged at authoring rather than padded down, and re-measured at ship.

## Documents it is about

- **PCP-004** — `pc_package/PCP-004_harvest.qmd`
- **PCP-006** — `pc_package/PCP-006_viral_inactivation.qmd`
- **PCP-008** — `pc_package/PCP-008_aex.qmd`
- **PCP-009** — `pc_package/PCP-009_virus_filtration.qmd`
- **PCP-010** — `pc_package/PCP-010_ufdf.qmd`
- **PCR-004** — `pc_package/PCR-004_harvest.qmd`
- **PCR-010** — `pc_package/PCR-010_ufdf.qmd`

## Files it touched

- not recorded
