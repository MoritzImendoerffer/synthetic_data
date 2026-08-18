---
type: pm-task
epic: 2026-08-18_02_register-track-d
sprint: 2026-08-18_02_register-track-d
task: TASK-030
status: todo
kind: documentation
title: "Move the findings into docs and close the register campaign or say what remains"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
---

> [!warning] Generated from `.claude/work/2026-08-18_02_register-track-d/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-030 — Move the findings into docs and close the register campaign or say what remains

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-030.md. This is /ship's work. Track C is the only track that can still be open when this lands.

## Acceptance criteria

- [ ] HANDOFF.md §3a gains a row for the corpus-wide re-author and one for the rhetorical-layer unification
- [ ] the page band in CLAUDE.md and TASKS.md item 6 is RE-MEASURED from the fresh pdfs and corrected -- it moved once already this way, 41-59 -> 41-56
- [ ] docs/next/rhetorical-layer-coverage.md is rewritten to what TASK-001 left: one mechanism now exists, and eleven documents still carry no layer
- [ ] docs/ROADMAP.md's register row says what is true; the proposal is deleted if Track C is also closed, or rewritten down to Track C alone
- [ ] /ship's full reproduction check passes: make clean && make data figures corpus, outputs/ byte-identical, every annex byte-identical, and rendered text compared through docx_text rather than by file hash

**Depends on:** [[TASK-029]]

## Files it touched

- [[HANDOFF]] — `authoring/HANDOFF.md`
- [[TASKS]] — `pc_package/TASKS.md`
- `CLAUDE.md`
- [[ROADMAP]] — `docs/ROADMAP.md`
- [[register-from-four-sources]] — `docs/next/register-from-four-sources.md`
- [[rhetorical-layer-coverage]] — `docs/next/rhetorical-layer-coverage.md`
- [[README]] — `docs/next/README.md`
- [[epic]] — `docs/pm/epic.md`
- [[_Archive]] — `docs/pm/_Archive.md`
