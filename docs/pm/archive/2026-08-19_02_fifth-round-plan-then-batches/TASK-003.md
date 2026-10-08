---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-003
status: done
kind: measurement
title: "The blind reading of shipped vs new PCP-005, recorded verbatim, then the rule applied \u2014 HALT for the owner (D7)"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-005"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-003 — The blind reading of shipped vs new PCP-005, recorded verbatim, then the rule applied — HALT for the owner (D7)

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

HARD STOP. If the owner reads only one file first, record it and ask for the other.

## Acceptance criteria

- [x] A.pdf/B.pdf = the shipped pc_package/PCP-005_protein_a.pdf and the DRAFT's pdf under the letters blind-key-PCP-005.md assigns, copied by a command that prints neither key, sizes nor page counts; the owner given READING.md's pilot text
- [x] the owner's answer recorded VERBATIM, dated, before the key is opened (checksum) and before any count; the quoted sentences located per source; decisions.pass_rule applied mechanically
- [x] decisions.pilot_outcome set PASS|FAIL; D7 settled; on FAIL the batch tasks are cancelled (cancelled_by: D7) and TASK-005/TASK-007 and the ship still run

**Depends on:** [[TASK-002]]

## What was built

HALTED FOR THE OWNER, 2026-08-19. A.pdf and B.pdf in the unit under the letters blind-key-PCP-005.md assigns, copied by a command that printed neither the key, nor sizes, nor page counts (both plans are 31 pages in any case); PDF metadata title/author identical. The owner is given READING.md's pilot text. The answer is recorded verbatim before the key is opened by checksum and before any count.

RESUMED AND COMPLETED 2026-08-19. The reading arrived in one message and was recorded verbatim before the key was opened: 'A reads better. In B, following sentence clearly revealed it's origin: "Three mechanisms frame what the study expects to find.' Key: new = A, checksum-verified (A.pdf == DRAFT.pdf, B.pdf == shipped); the quoted sentence occurs once in the shipped .qmd and never in the new one. Rule applied mechanically: new judged better, 0 sentences quoted from it -> D7 = PASS. What the owner said about the new plan: 'reads better'; about the shipped: one sentence named, a paragraph-shape announcement of exactly the kind the content review's Q4 flags.

## Documents it is about

- **PCP-005** — `pc_package/PCP-005_protein_a.qmd`

## Files it touched

- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/A.pdf`
- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/B.pdf`
- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/owner-reading-PCP-005-<date>.md`
- [[D7-does-the-plan-pass]] — `docs/pm/decisions/D7-does-the-plan-pass.md`
