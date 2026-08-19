---
type: pm-task
epic: 2026-08-19_01_fourth-round-one-document
sprint: 2026-08-19_01_fourth-round-one-document
task: TASK-008
status: todo
kind: documentation
title: "Move the findings into docs, update the roadmap and the proposal, and ship"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
---

> [!warning] Generated from `.claude/work/2026-08-19_01_fourth-round-one-document/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-008 — Move the findings into docs, update the roadmap and the proposal, and ship

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

/ship does this. Whether the campaign continues to the remaining documents is a new decision for the owner and a new /explore, not this unit's.

## Acceptance criteria

- [ ] docs/results/README.md gains the page's row; authoring/HANDOFF.md §3a gains one row: 'PCR-007 re-authored in one pass under the rebuilt apparatus, 2026-08-<dd>' with the re-anchoring counts (quotes moved / 88, spans re-cut / 33) on PASS, or 'authored, read, not promoted' on FAIL
- [ ] docs/ROADMAP.md: the register-campaign row says what is now true — on PASS, that one document is at the rebuilt-apparatus register and the remaining count (14 at round zero + the earlier-round documents), and that the rest is the owner's call; on FAIL, what the reading named and that the regime needs revising before another document
- [ ] docs/next/register-from-four-sources.md: rewritten down to what remains (the other documents, in the owner's order) or deleted if the owner decides the campaign is done — the plan does not decide this; its README.md row matches
- [ ] CLAUDE.md depth band and TASKS.md page band re-measured if PCR-007's page count moved them; TASKS.md 'Things that will catch you out' gains an item only if this round found one
- [ ] `uv run python scripts/pm_notes.py` regenerated; D5 and D6 settled; metadata.json status = shipped

**Depends on:** [[TASK-005]]

## Files it touched

- [[README]] — `docs/results/README.md`
- [[HANDOFF]] — `authoring/HANDOFF.md`
- [[ROADMAP]] — `docs/ROADMAP.md`
- [[register-from-four-sources]] — `docs/next/register-from-four-sources.md`
- [[README]] — `docs/next/README.md`
- `CLAUDE.md`
- [[TASKS]] — `pc_package/TASKS.md`
