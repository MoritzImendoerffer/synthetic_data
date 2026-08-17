---
type: pm-task
epic: 2026-08-16_01_register-from-four-sources
sprint: 2026-08-16_01_register-from-four-sources
task: TASK-010
status: todo
kind: documentation
title: "Move the findings into docs and retire what is finished"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
---

> [!warning] Generated from `.claude/work/2026-08-16_01_register-from-four-sources/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-010 — Move the findings into docs and retire what is finished

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

THIS IS /ship's WORK and the plan leaves room for it; do not do it early.

HANDOFF.md 3a is the record of every perturbation applied to the corpus, in two tables: 'Model / world-canon changes' and 'Tooling changes'. The guide amendment and the four-source extraction both belong in the second, because both change how documents are checked. Say what each did.

TASKS.md 'Things that will catch you out' is a numbered list of six; add the discrepancy trap as the seventh, because it is a thing somebody could get wrong twice and it cost a benchmark item once already.

THE PROPOSAL IS NOT DELETED. Two documents of twenty were re-authored, so what remains is real: rewrite docs/next/register-from-four-sources.md down to the remaining eighteen and whatever TASK-009 concluded about them. Deleting it would claim work that was not done.

THE NOTEBOOK MOVES to authoring/register_analysis.ipynb, beside the guide it explains. Its ROOT-finding cell walks up to CLAUDE.md, so it works from the new location, but re-run it to confirm. A reader who does not know why 2c changed is the person most likely to revert it.

## Acceptance criteria

- [ ] the results page has a row in docs/results/README.md saying why the run happened
- [ ] authoring/HANDOFF.md 3a gains perturbation rows for the guide amendment, the source extraction and the discrepancy carrier
- [ ] pc_package/TASKS.md gains the trap: a re-authored document loses a registered discrepancy unless the brief carries it
- [ ] the notebook moves to authoring/ and still runs from its new location
- [ ] docs/ROADMAP.md says what is now true
- [ ] the proposal is rewritten down to the remaining EIGHTEEN documents rather than deleted

**Depends on:** [[TASK-009]]

## Files it touched

- [[README]] — `docs/results/README.md`
- [[HANDOFF]] — `authoring/HANDOFF.md`
- [[TASKS]] — `pc_package/TASKS.md`
- [[ROADMAP]] — `docs/ROADMAP.md`
- [[register-from-four-sources]] — `docs/next/register-from-four-sources.md`
- `authoring/register_analysis.ipynb`
