---
type: pm-task
epic: 2026-08-17_01_register-second-round
sprint: 2026-08-17_01_register-second-round
task: TASK-009
status: todo
kind: documentation
title: "Move the findings into docs, settle the decision, and rewrite or retire the proposal on the stopping rule's verdict"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
---

> [!warning] Generated from `.claude/work/2026-08-17_01_register-second-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-009 — Move the findings into docs, settle the decision, and rewrite or retire the proposal on the stopping rule's verdict

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-009.md in this work unit — numbered steps, code, commands and the output each must print. Follow it top to bottom.  THIS IS /ship's WORK and the plan leaves room for it; do not do it early.  THE VERDICT DECIDES THE SHAPE OF THE PROPOSAL. Two branches, both prepared here so /ship does not improvise: (a) stopping rule holds → the proposal becomes 'Track 2 — the remaining eighteen', with the budget from the pilot page and the round-two per-document re-anchoring counts, and D1 asks the owner whether Track 2 starts without another decision; (b) it does not → the proposal is rewritten to the target the owner's reading names, and the guide's-own-register hypothesis (decisions.guide_scope) is written up as its first candidate, with the numbers from exploration.md §4 (guide commentary 0 % initial connectives, ', so ' 1.5–11.5 %).  HANDOFF §3a is two tables ('Model / world-canon changes', 'Tooling changes'); everything here is tooling.  TASKS.md's list was six, then seven after round one (the discrepancy trap); these are eight and nine.  pm_notes.py archives the previous epic when ACTIVE_WORK changes; the _Archive.md row is /ship's, written before the notes move.

## Acceptance criteria

- [ ] authoring/HANDOFF.md §3a 'Tooling changes' gains rows for: the advisory packing measures in check_style.py, check_discourse.py + the optional extra, brief §5d, and the guide's rule-as-substitution rewrite — each saying what it did
- [ ] pc_package/TASKS.md 'Things that will catch you out' gains two: (a) an inline expression that yields a NAME must not be an agreeing subject; (b) the guide's own commentary is written in the register it forbids — verify against the sources, not against the guide's prose
- [ ] CLAUDE.md's Voice bullet says the packing measures exist and are advisory, in one sentence, if TASK-003 has not already covered it
- [ ] docs/ROADMAP.md's register row says what is now true; if Track 2 opens it names the eighteen and the per-document budget (~40 spans, explicit pdf render); if not, it names the next target from the owner's reading
- [ ] docs/next/register-from-four-sources.md is rewritten to Track 2 alone (if the verdict is 'open') or to the new target (if 'stop'), or deleted if nothing remains; docs/next/README.md's row agrees
- [ ] docs/pm/decisions/D1-track-two-on-the-verdict.md is settled with the owner's answer and status: settled
- [ ] docs/pm/epic.md carries the shipped summary and docs/pm/_Archive.md gains this epic's row before the notes move
- [ ] `docs/results/` page is linked from ROADMAP, README and the proposal or its successor

**Depends on:** [[TASK-008]]

## Files it touched

- [[README]] — `docs/results/README.md`
- [[HANDOFF]] — `authoring/HANDOFF.md`
- [[TASKS]] — `pc_package/TASKS.md`
- [[ROADMAP]] — `docs/ROADMAP.md`
- [[register-from-four-sources]] — `docs/next/register-from-four-sources.md`
- [[README]] — `docs/next/README.md`
- [[D1-track-two-on-the-verdict]] — `docs/pm/decisions/D1-track-two-on-the-verdict.md`
- [[epic]] — `docs/pm/epic.md`
- [[_Archive]] — `docs/pm/_Archive.md`
- `CLAUDE.md`
