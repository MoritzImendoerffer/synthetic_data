---
type: pm-board
epic: 2026-08-18_01_register-third-round
sprint: 2026-08-18_01_register-third-round
generated: true
tags: [pm/board]
---

> [!warning] Generated from `.claude/work/2026-08-18_01_register-third-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# Board — the active epic

**[[epic|2026-08-18_01_register-third-round]]** · **4 of 7 done** · 3 todo

[[epic|Why this epic]] · [[_Artifacts|The corpus and its gates]] · [[_Archive|Finished epics]]

## Waiting on the project owner

**This is the only section that is yours.** Each is an argument a person has to settle.
None of them blocks the work below.

*None.*

## Not finished — the assistant's work, not the owner's

Nothing in this table needs the project owner. It is what the coding assistant has still to do,
and it is here so the state is visible, not so anyone else acts on it.

| Task | Status | Waiting on | Kind | What it is |
|---|---|---|---|---|
| [[TASK-005]] | `todo` | the assistant | annex | Promote the draft, render both formats, re-anchor the PCR-003 annex and spans, and re-ground the corpus |
| [[TASK-006]] | `todo` | the assistant | measurement | Measure the four-point series by one method, apply the stopping rule, and record the owner's reading |
| [[TASK-007]] | `todo` | the assistant | documentation | Move the findings into docs, and rewrite or retire the proposal on the verdict |

## Done

| Task | Status | Waiting on | Kind | What it is |
|---|---|---|---|---|
| [[TASK-001]] | `done` | — | mechanism | Make the round-two owner-reading measure a file that reproduces its table, then move the two regex counts into check_style.py |
| [[TASK-002]] | `done` | — | mechanism | Add the passive rate and the parser's ', and '+clause count to check_discourse.py, as bands with denominators |
| [[TASK-003]] | `done` | — | mechanism | Print the three new measures in brief §5d, and add the write-the-passive rule and the two search strings to the guide |
| [[TASK-004]] | `done` | — | document | Re-author PCR-003 in one pass from the amended artifacts, as a DRAFT |

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
