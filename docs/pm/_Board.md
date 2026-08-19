---
type: pm-board
epic: 2026-08-19_01_fourth-round-one-document
sprint: 2026-08-19_01_fourth-round-one-document
generated: true
tags: [pm/board]
---

> [!warning] Generated from `.claude/work/2026-08-19_01_fourth-round-one-document/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# Board — the active epic

**[[epic|2026-08-19_01_fourth-round-one-document]]** · **1 of 8 done** · 1 doing · 6 todo

[[epic|Why this epic]] · [[_Artifacts|The corpus and its gates]] · [[_Archive|Finished epics]]

## Waiting on the project owner

**This is the only section that is yours.** Each is an argument a person has to settle.
**One of them blocks a task below**, named in its own row: until it is settled that work cannot start.

| Decision | Waiting on | Blocks |
|---|---|---|
| [[D5-which-document|D5 — which document is the one whole document under the rebuilt apparatus?]] | project owner | nothing — the plan assumes PCR-007 and proceeds; overrule before TASK-002 runs |
| [[D6-does-the-whole-document-pass|D6 — does the whole document written under the rebuilt apparatus read as a paper?]] | project owner | [[TASK-006]], [[TASK-007]] |

## Not finished — the assistant's work, not the owner's

Nothing in this table needs the project owner. It is what the coding assistant has still to do,
and it is here so the state is visible, not so anyone else acts on it.

| Task | Status | Waiting on | Kind | What it is |
|---|---|---|---|---|
| [[TASK-002]] | `doing` | the assistant | document | Author PCR-007 in one pass under the rebuilt apparatus: one agent, the RUNNER's inputs, nothing else |
| [[TASK-003]] | `todo` | the assistant | measurement | Content review before the reading: the four questions on the draft, at most one return to the author |
| [[TASK-004]] | `todo` | the assistant | measurement | The blind reading of shipped vs new PCR-007, recorded verbatim, then the rule applied — HALT for the owner |
| [[TASK-005]] | `todo` | the assistant | measurement | Count what the reading named, before/after against the same script, and write the results page |
| [[TASK-006]] | `todo` | the assistant | annex | Promote the new PCR-007: render, re-cut its 33 spans, re-anchor its annex, re-ground the corpus |
| [[TASK-007]] | `todo` | the assistant | measurement | Rebuild-and-reground proof after promotion: the corpus is whole |
| [[TASK-008]] | `todo` | the assistant | documentation | Move the findings into docs, update the roadmap and the proposal, and ship |

## Done

| Task | Status | Waiting on | Kind | What it is |
|---|---|---|---|---|
| [[TASK-001]] | `done` | — | mechanism | Fix the launch prompt, the blind key and the reading protocol before anything is written |

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
