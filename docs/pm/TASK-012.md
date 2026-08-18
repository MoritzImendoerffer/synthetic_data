---
type: pm-task
epic: 2026-08-18_03_author-facing-apparatus
sprint: 2026-08-18_03_author-facing-apparatus
task: TASK-012
status: todo
kind: documentation
title: "Move the findings into docs, update the roadmap, and delete the proposal"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
---

> [!warning] Generated from `.claude/work/2026-08-18_03_author-facing-apparatus/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-012 — Move the findings into docs, update the roadmap, and delete the proposal

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

/ship does this. On FAIL the documentation move is small: the results page, the roadmap row, the proposal deletion, and one HANDOFF row saying the hypothesis was tested and how, so a later session does not re-run the same probe.

## Acceptance criteria

- [ ] docs/ROADMAP.md row 0 says what D4 settled, what shipped (which of TASK-006..010) and links the results page; the register-campaign row says whether a fourth round is now unblocked (PASS) or still waits on results §8 (FAIL)
- [ ] docs/next/author-facing-apparatus.md is deleted and its README row removed; docs/next/register-from-four-sources.md's pointer paragraph is updated to the results page
- [ ] authoring/HANDOFF.md §3a gains one row per instrument that changed (gate split, section plan, guide, mechanism files, review checklist) or one row saying the probe failed and nothing changed
- [ ] CLAUDE.md: the Voice rule and the 'Adding a unit-operation Plan/Report pair' step 3 name the current input list and the reviewer-side checklist (PASS), or are untouched (FAIL); pc_package/TASKS.md item on re-authoring names REVIEW_CHECKLIST.md before promotion (PASS)
- [ ] `uv run python scripts/pm_notes.py` regenerated; metadata.json status = shipped

**Depends on:** [[TASK-011]]

## Files it touched

- [[2026-08-18-apparatus-probe]] — `docs/results/2026-08-18-apparatus-probe.md`
- [[ROADMAP]] — `docs/ROADMAP.md`
- [[README]] — `docs/next/README.md`
- [[author-facing-apparatus]] — `docs/next/author-facing-apparatus.md`
- [[register-from-four-sources]] — `docs/next/register-from-four-sources.md`
- [[HANDOFF]] — `authoring/HANDOFF.md`
- [[TASKS]] — `pc_package/TASKS.md`
- `CLAUDE.md`
