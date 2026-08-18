---
type: pm-task
epic: 2026-08-18_01_register-third-round
sprint: 2026-08-18_01_register-third-round
task: TASK-007
status: todo
kind: documentation
title: "Move the findings into docs, and rewrite or retire the proposal on the verdict"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
---

> [!warning] Generated from `.claude/work/2026-08-18_01_register-third-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-007 — Move the findings into docs, and rewrite or retire the proposal on the verdict

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-007.md — the previous unit's TASK-009 procedure. THIS IS /ship's WORK. THE VERDICT DECIDES THE SHAPE: if the reading says 'no longer immediately obvious', Track D (the eighteen) opens and the proposal becomes Track C + Track D with the per-document budget from three measured rounds; if the reading names new faults, they become the next target and the proposal is rewritten to them, with Track C still the leading hypothesis (owner: measures first, then C). Prepare both shapes. STATUS LINES: re-check the '41-59 pp' band and any HANDOFF claim about span counts before writing them.

## Acceptance criteria

- [ ] HANDOFF.md §3a gains rows for the two new check_style counts (with the regex-is-a-floor note), the passive + parser counts in check_discourse.py, brief §5d's three rows, the guide's write-the-passive rule, and PCR-003's third re-author with its re-anchoring count
- [ ] pc_package/TASKS.md 'Things that will catch you out' gains item 10: a study, a design, a model or a process is never the AGENT of retain/carry/identify/select — the author manufactures one when avoiding a passive; verify against the sources' passive rate (54-60 %), a band
- [ ] CLAUDE.md's Voice bullet mentions the two new advisory counts in the same sentence as the packing line (one clause), and the page band is re-checked against the new PCR-003 page count
- [ ] docs/ROADMAP.md's register row says what is now true, links the round-three page, and names the next target from the owner's reading if there is one; docs/next/register-from-four-sources.md is rewritten to what remains (Track C and D, or the new target) or deleted; docs/next/README.md agrees
- [ ] docs/pm/epic.md shipped; docs/pm/_Archive.md gains the row before the notes move; `uv run python scripts/pm_notes.py` shows 7 of 7
- [ ] final gates from the checklist: make test, make style 24/0, annexes 20/20, strict grounding N/N with 0 weak anchors, check_blank_repo PASS, `git diff --stat outputs/` empty

**Depends on:** [[TASK-006]]

## Files it touched

- [[HANDOFF]] — `authoring/HANDOFF.md`
- [[TASKS]] — `pc_package/TASKS.md`
- `CLAUDE.md`
- [[ROADMAP]] — `docs/ROADMAP.md`
- [[register-from-four-sources]] — `docs/next/register-from-four-sources.md`
- [[README]] — `docs/next/README.md`
- [[epic]] — `docs/pm/epic.md`
- [[_Archive]] — `docs/pm/_Archive.md`
- [[README]] — `docs/results/README.md`
