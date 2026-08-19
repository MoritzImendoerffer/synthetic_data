---
type: pm-board
epic: 2026-08-18_03_author-facing-apparatus
sprint: 2026-08-18_03_author-facing-apparatus
generated: true
tags: [pm/board]
---

> [!warning] Generated from `.claude/work/2026-08-18_03_author-facing-apparatus/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# Board — the active epic

**[[epic|2026-08-18_03_author-facing-apparatus]]** · **5 of 12 done** · 7 todo

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
| [[TASK-006]] | `todo` | the assistant | mechanism | Split the register gate into GATED tics and ADVISORY signals; the author sees pass/fail, the reviewer sees the table |
| [[TASK-007]] | `todo` | the assistant | mechanism | Take scaffold, register and rigor off the author-facing section plan and put them in a reviewer's checklist |
| [[TASK-008]] | `todo` | the assistant | mechanism | Replace WRITING_GUIDE.md with a short positive guide and move its history out |
| [[TASK-009]] | `todo` | the assistant | mechanism | Write the per-unit-operation mechanism files, emit them as brief §2b, and halt for the owner's read |
| [[TASK-010]] | `todo` | the assistant | mechanism | Add the four content questions to the reviewer's checklist and calibrate them on the excerpt and the probe |
| [[TASK-011]] | `todo` | the assistant | measurement | Prove the corpus is unchanged: annexes, grounding, outputs, tests and style at the end of the unit |
| [[TASK-012]] | `todo` | the assistant | documentation | Move the findings into docs, update the roadmap, and delete the proposal |

## Done

| Task | Status | Waiting on | Kind | What it is |
|---|---|---|---|---|
| [[TASK-001]] | `done` | — | mechanism | Extend the measurement script with the frame counts, and prove it reproduces the results page |
| [[TASK-002]] | `done` | — | mechanism | Build the probe scaffold: the setup code, the ten-line guide, the stripped brief, the excerpt, and the blind key |
| [[TASK-003]] | `done` | — | document | Author the probe: two subsections, one agent, one pass, minimal regime, no counters |
| [[TASK-004]] | `done` | — | measurement | The blind reading, recorded verbatim, then the decision rule applied — HALT for the owner |
| [[TASK-005]] | `done` | — | measurement | Count what the reading named, run the gate on the probe, and write the results page |

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
