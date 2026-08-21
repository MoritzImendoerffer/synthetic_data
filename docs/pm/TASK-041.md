---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-041
status: done
kind: documentation
title: "Move the findings into docs, update the roadmap, retire or reduce the proposal, and ship"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCMP-001", "PTP-001"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-041 — Move the findings into docs, update the roadmap, retire or reduce the proposal, and ship

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

/ship does this.

## Acceptance criteria

- [x] results README rows for both pages; HANDOFF §3a one row per batch with re-anchoring counts and discrepancy outcomes; ROADMAP register row says the corpus is at one register (or exactly which documents are not); CLAUDE.md depth bands re-measured from the rendered PDFs; the proposal deleted if nothing remains, else reduced; D7/D8 settled; pm regenerated; metadata shipped

**Depends on:** [[TASK-040]]

## What was built

Shipped 2026-08-21. FULL rebuild run, not the annex-only path, because the unit changed a helper (_pcpkg.all_sop_table) and four .qmd: make clean && make data figures corpus, exit 0. outputs/ reproduced BYTE-FOR-BYTE. Final 2089/2089 quotes grounded across 20 annexes, 20/20 valid, 0 weak anchors, make test 95 passed, make style 24 OK. Of the 20 rendered pairs the rebuild rewrote, only PTP-001 and PCMP-001 changed TEXT (the all_sop_table fix); the other 18 were byte-different but text-identical render noise and were restored BY NAME. Diff read for typed numbers: none added — the only numeric lines in the _pcpkg diff are step numbers in a comment, and the config change is comment-only, which is why outputs/ reproduced. Findings moved: results page + README row, HANDOFF §3a (1 model row, 3 tooling rows), ROADMAP row to DELIVERED, CLAUDE.md depth bands re-measured (3 corrected, 1 added). The proposal was NOT deleted: Track C and three unprinted measures remain, so it is rewritten down from 175 lines to 68 and its docs/next row now reads as priority 1. D8 settled; epic.md and _Archive.md updated.

## Documents it is about

- **PCMP-001** — `pc_package/PCMP-001_master_plan.qmd`
- **PTP-001** — `pc_package/PTP-001_transfer.qmd`

## Files it touched

- [[README]] — `docs/results/README.md`
- [[HANDOFF]] — `authoring/HANDOFF.md`
- [[ROADMAP]] — `docs/ROADMAP.md`
- [[register-from-four-sources]] — `docs/next/register-from-four-sources.md`
- [[README]] — `docs/next/README.md`
- `CLAUDE.md`
- [[TASKS]] — `pc_package/TASKS.md`
