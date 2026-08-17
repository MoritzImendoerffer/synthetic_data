---
type: pm-board
epic: 2026-08-17_01_register-second-round
sprint: 2026-08-17_01_register-second-round
generated: true
tags: [pm/board]
---

> [!warning] Generated from `.claude/work/2026-08-17_01_register-second-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# Board — the active epic

**[[epic|2026-08-17_01_register-second-round]]** · **5 of 9 done** · 4 todo

[[epic|Why this epic]] · [[_Artifacts|The corpus and its gates]] · [[_Archive|Finished epics]]

## Waiting on the project owner

**This is the only section that is yours.** Each is an argument a person has to settle.
None of them blocks the work below.

| Decision | Waiting on | Blocks |
|---|---|---|
| [[D1-track-two-on-the-verdict|D1 — if the stopping rule holds, does Track 2 start without another decision?]] | project owner | nothing; it decides the next epic's scope |

## Not finished — the assistant's work, not the owner's

Nothing in this table needs the project owner. It is what the coding assistant has still to do,
and it is here so the state is visible, not so anyone else acts on it.

| Task | Status | Waiting on | Kind | What it is |
|---|---|---|---|---|
| [[TASK-006]] | `todo` | the assistant | document | Re-author PCR-003 in one pass from the amended artifacts, as a DRAFT |
| [[TASK-007]] | `todo` | the assistant | annex | Promote both drafts, render both formats, re-anchor the annexes and re-ground the corpus |
| [[TASK-008]] | `todo` | the assistant | measurement | Measure round two against rounds zero and one with one method, apply the stopping rule, and record the owner's reading |
| [[TASK-009]] | `todo` | the assistant | documentation | Move the findings into docs, settle the decision, and rewrite or retire the proposal on the stopping rule's verdict |

## Done

| Task | Status | Waiting on | Kind | What it is |
|---|---|---|---|---|
| [[TASK-001]] | `done` | — | mechanism | Print clause packing and sentence-initial connectives in check_style.py, gated by nothing |
| [[TASK-002]] | `done` | — | mechanism | Rewrite the guide's sentence rule as a substitution, fix the ✓ text that teaches the fault, and add the referent and Shape 4 examples |
| [[TASK-003]] | `done` | — | mechanism | Add authoring/check_discourse.py with spaCy as an optional extra that the build never needs |
| [[TASK-004]] | `done` | — | mechanism | Give the brief a §5d that prints the discourse targets and the document's own current numbers |
| [[TASK-005]] | `done` | — | document | Re-author PCP-003 in one pass from the amended artifacts, as a DRAFT |

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
