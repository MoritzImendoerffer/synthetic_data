---
type: pm-board
epic: 2026-08-16_01_register-from-four-sources
sprint: 2026-08-16_01_register-from-four-sources
generated: true
tags: [pm/board]
---

> [!warning] Generated from `.claude/work/2026-08-16_01_register-from-four-sources/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# Board — the active epic

**[[epic|2026-08-16_01_register-from-four-sources]]** · **10 of 10 done**

[[epic|Why this epic]] · [[_Artifacts|The corpus and its gates]] · [[_Archive|Finished epics]]

## Waiting on the project owner

**This is the only section that is yours.** Each is an argument a person has to settle.
None of them blocks the work below.

*None.*

## Not finished — the assistant's work, not the owner's

Nothing in this table needs the project owner. It is what the coding assistant has still to do,
and it is here so the state is visible, not so anyone else acts on it.

*None.*

## Done

| Task | Status | Waiting on | Kind | What it is |
|---|---|---|---|---|
| [[TASK-001]] | `done` | — | mechanism | Extract all four sources, each with its own boilerplate filter |
| [[TASK-002]] | `done` | — | mechanism | Widen the self-test to four sources and stop capping the only connective in use |
| [[TASK-003]] | `done` | — | mechanism | Amend WRITING_GUIDE 2c and 2d to license a claim beside its counter-consideration |
| [[TASK-004]] | `done` | — | mechanism | Add the moves catalogue to REGISTER_EXEMPLAR.md |
| [[TASK-005]] | `done` | — | mechanism | Exemplify the given-new rule WRITING_GUIDE 2d already states |
| [[TASK-006]] | `done` | — | mechanism | Give the brief a discrepancies section, so a re-authored document keeps its registered defects |
| [[TASK-007]] | `done` | — | document | Re-author PCP-003 and PCR-003, one pass each, from the amended artifacts |
| [[TASK-008]] | `done` | — | annex | Promote both pilot documents, re-anchor their annexes, and fix what the rewrite falsified |
| [[TASK-009]] | `done` | — | measurement | Measure both pilot documents and put them in front of a reader |
| [[TASK-010]] | `done` | — | documentation | Move the findings into docs and retire what is finished |

---

## The same, as live queries

These need the Dataview plugin in Obsidian. **They query by tag, not by folder**, so they work
wherever the vault is rooted. A folder source such as `FROM "docs/pm"` only resolves when the
vault is opened at the repository root, which is the usual reason a table comes back empty.

Without the plugin these render as code blocks, and the tables above are the board.

```dataview
TABLE status, kind, title
FROM #pm/task
WHERE status != "done"
SORT status ASC
```

```dataview
TABLE waiting_on AS "waiting on"
FROM #pm/decision
WHERE status = "open"
```
