---
type: pm-task
epic: 2026-08-18_03_author-facing-apparatus
sprint: 2026-08-18_03_author-facing-apparatus
task: TASK-012
status: done
kind: documentation
title: "Move the findings into docs, update the roadmap, and delete the proposal"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
---

> [!warning] Generated from `.claude/work/2026-08-18_03_author-facing-apparatus/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-012 — Move the findings into docs, update the roadmap, and delete the proposal

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

/ship does this. On FAIL the documentation move is small: the results page, the roadmap row, the proposal deletion, and one HANDOFF row saying the hypothesis was tested and how, so a later session does not re-run the same probe.

## Acceptance criteria

- [x] docs/ROADMAP.md row 0 says what D4 settled, what shipped (which of TASK-006..010) and links the results page; the register-campaign row says whether a fourth round is now unblocked (PASS) or still waits on results §8 (FAIL)
- [x] docs/next/author-facing-apparatus.md is deleted and its README row removed; docs/next/register-from-four-sources.md's pointer paragraph is updated to the results page
- [x] authoring/HANDOFF.md §3a gains one row per instrument that changed (gate split, section plan, guide, mechanism files, review checklist) or one row saying the probe failed and nothing changed
- [x] CLAUDE.md: the Voice rule and the 'Adding a unit-operation Plan/Report pair' step 3 name the current input list and the reviewer-side checklist (PASS), or are untouched (FAIL); pc_package/TASKS.md item on re-authoring names REVIEW_CHECKLIST.md before promotion (PASS)
- [x] `uv run python scripts/pm_notes.py` regenerated; metadata.json status = shipped

**Depends on:** [[TASK-011]]

## What was built

Shipped 2026-08-19. Gates at ship: make test 95 passed; make style 26 OK / 0 FAIL; 20/20 annexes valid; 2084/2084 quotes grounded with strict anchors, exit 0; git diff outputs/ empty. Reproduction check: the annexes-and-gates path, stated as such — no .qmd, config, model, script or annex builder changed in this unit and the only helper edit is a docstring, so a full make corpus would rewrite twenty tracked renders with float noise and prove nothing this unit claims. Moves: docs/results/README.md rows for the Track D stopped page (which had none) and the probe page; five HANDOFF §3a rows; TASKS.md traps 12 (a counter printed to an author is a target) and 13 (a multi-edit script that asserts mid-way); ROADMAP row 0 -> Recently closed and the register row unblocked with 'one whole document under the rebuilt apparatus' as the owner's next call; docs/next/author-facing-apparatus.md deleted, its README row dropped, the pointer in register-from-four-sources.md rewritten to what remains; docs/pm/epic.md first paragraph, _Archive.md row, board regenerated; D4 already settled. The four untracked probe files removed from pc_package/ (A.pdf/B.pdf and build_probe_scaffold.py hold their content).

## Files it touched

- [[2026-08-18-apparatus-probe]] — `docs/results/2026-08-18-apparatus-probe.md`
- [[ROADMAP]] — `docs/ROADMAP.md`
- [[README]] — `docs/next/README.md`
- [[author-facing-apparatus]] — `docs/next/author-facing-apparatus.md`
- [[register-from-four-sources]] — `docs/next/register-from-four-sources.md`
- [[HANDOFF]] — `authoring/HANDOFF.md`
- [[TASKS]] — `pc_package/TASKS.md`
- `CLAUDE.md`
