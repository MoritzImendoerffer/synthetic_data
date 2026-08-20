---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-049
status: todo
kind: document
title: "Re-author PCR-004 (attempt 2) in one pass under the same regime, with one content-review cycle"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCR-004"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-049 — Re-author PCR-004 (attempt 2) in one pass under the same regime, with one content-review cycle

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

The owner preferred the pre-campaign text for this document (TASK-018 FAIL), and ranked it last of three on the same paragraph in the cross-document reading the same day. The comparison text for the reading stays the PRE-CAMPAIGN pdf ($U/B2-old-PCR-004.pdf). May run alongside B3. The regime is unchanged, so this tests the draw.

## Acceptance criteria

- [ ] procedures/AUTHOR-A-DOCUMENT.md followed for PCR-004 / harvest / report_nondoe exactly as TASK-014: brief rebuilt fresh (2b 1, 5d 0, §5c None), DRAFT instantiated, ONE fresh agent (`opus`) with the §2 prompt verbatim; a NEW blind key drawn to blind-key-B2b-PCR-004.md BEFORE the agent is launched, with a random nonce so neither length nor checksum identifies the letter, and NO checksum printed
- [ ] transcript audit clean; check_render --render clean with glyphs; 0 <<NEEDS>>; no DoE fabricated (the step has none) and every section of section_plan.yaml report_nondoe present in order
- [ ] content review: run 1 by a fresh judge, ONE return to the same author if any question reads no, run 2 by a second fresh judge; filed with run-1/run-2 counts
- [ ] outcome records model, passes, sizes, audit, review counts, and specifically what §6 now says about the absence of a design space — the paragraph the owner read

## Documents it is about

- **PCR-004** — `pc_package/PCR-004_harvest.qmd`

## Files it touched

- `pc_package/PCR-004_harvest.DRAFT.qmd`
- `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/content-review-PCR-004-attempt2.md`
