---
type: pm-board
epic: 2026-08-18_02_register-track-d
sprint: 2026-08-18_02_register-track-d
generated: true
tags: [pm/board]
---

> [!warning] Generated from `.claude/work/2026-08-18_02_register-track-d/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# Board — the active epic

**[[epic|2026-08-18_02_register-track-d]]** · **7 of 30 done** · 23 todo

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
| [[TASK-008]] | `cancelled` | ? | document | Re-author PCP-004 in one pass, as a DRAFT |
| [[TASK-009]] | `cancelled` | ? | document | Re-author PCR-004 in one pass, as a DRAFT |
| [[TASK-010]] | `cancelled` | ? | document | Re-author PCP-006 in one pass, as a DRAFT |
| [[TASK-011]] | `cancelled` | ? | document | Re-author PCR-006 in one pass, as a DRAFT |
| [[TASK-012]] | `cancelled` | ? | annex | Promote, render, re-anchor and re-ground batch 1 (harvest and viral inactivation) |
| [[TASK-013]] | `cancelled` | ? | document | Re-author PCP-008 in one pass, as a DRAFT |
| [[TASK-014]] | `cancelled` | ? | document | Re-author PCR-008 in one pass, as a DRAFT |
| [[TASK-015]] | `cancelled` | ? | document | Re-author PCP-009 in one pass, as a DRAFT |
| [[TASK-016]] | `cancelled` | ? | document | Re-author PCR-009 in one pass, as a DRAFT |
| [[TASK-017]] | `cancelled` | ? | annex | Promote, render, re-anchor and re-ground batch 2 (aex and virus filtration) |
| [[TASK-018]] | `cancelled` | ? | document | Re-author PCP-010 in one pass, as a DRAFT |
| [[TASK-019]] | `cancelled` | ? | document | Re-author PCR-010 in one pass, as a DRAFT |
| [[TASK-020]] | `cancelled` | ? | document | Re-author PCP-003 in one pass, as a DRAFT |
| [[TASK-021]] | `cancelled` | ? | document | Re-author PCP-005 in one pass, as a DRAFT |
| [[TASK-022]] | `cancelled` | ? | annex | Promote, render, re-anchor and re-ground batch 3 (UF/DF, and the bioreactor and Protein A plans) |
| [[TASK-023]] | `cancelled` | ? | document | Re-author PCR-007 in one pass, as a DRAFT |
| [[TASK-024]] | `cancelled` | ? | document | Re-author PTP-001 in one pass, as a DRAFT |
| [[TASK-025]] | `cancelled` | ? | document | Re-author PCMP-001 in one pass, as a DRAFT |
| [[TASK-026]] | `cancelled` | ? | annex | Promote, render, re-anchor and re-ground batch 4 (CEX report, transfer plan, master plan) |
| [[TASK-027]] | `cancelled` | ? | document | Re-author PCMR-001 in one pass, as a DRAFT |
| [[TASK-028]] | `cancelled` | ? | annex | Promote, render, re-anchor and re-ground the master report (PCMR-001) |
| [[TASK-029]] | `cancelled` | ? | measurement | Measure the whole corpus by one method, apply the stopping rule, record the reading |
| [[TASK-030]] | `cancelled` | ? | documentation | Move the findings into docs and close the register campaign or say what remains |

## Done

| Task | Status | Waiting on | Kind | What it is |
|---|---|---|---|---|
| [[TASK-001]] | `done` | — | mechanism | Unify the rhetorical layer onto one gated mechanism: 280 code-built spans become YAML |
| [[TASK-002]] | `done` | — | mechanism | Freeze the Track D measurement as a script that reproduces the baseline |
| [[TASK-003]] | `done` | — | document | Re-author PCP-007 in one pass, as a DRAFT |
| [[TASK-004]] | `done` | — | document | Re-author PCR-005 in one pass, as a DRAFT |
| [[TASK-005]] | `done` | — | document | Re-author RA-001 in one pass, as a DRAFT |
| [[TASK-006]] | `done` | — | annex | Promote, render, re-anchor and re-ground the pilot batch (PCP-007, PCR-005, RA-001) |
| [[TASK-007]] | `done` | — | measurement | Measure the pilot, take the owner's reading, and decide whether the remaining 16 run |

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
