---
type: pm-board
epic: 2026-08-03_01_annex-anchors
sprint: 2026-08-03_01_annex-anchors
generated: true
tags: [pm/board]
---

> [!warning] Generated from `.claude/work/2026-08-03_01_annex-anchors/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# Board — the active epic

**[[epic|2026-08-03_01_annex-anchors]]** · **11 of 11 done**

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
| [[T1]] | `done` | — |  | Align _md_rows default float format with show() |
| [[T2]] | `done` | — |  | Carry the column header: schema_ext.SourceReference.table_header |
| [[T3]] | `done` | — |  | Re-anchor PCP/PCR-004 (harvest) and PCR-003 PARs |
| [[T4]] | `done` | — |  | Re-anchor PCP/PCR-005 (protein A) |
| [[T5]] | `done` | — |  | Re-anchor PCP/PCR-006 (viral inactivation) |
| [[T6]] | `done` | — |  | Re-anchor PCP/PCR-007 (CEX) |
| [[T7]] | `done` | — |  | Re-anchor PCP/PCR-008 (AEX) |
| [[T8]] | `done` | — |  | Re-anchor PCP/PCR-009 (virus filtration) and PCP/PCR-010 (UF/DF) |
| [[T9]] | `done` | — |  | Tighten the reuse rule to 3 for prose spans |
| [[T10]] | `done` | — |  | Tests and docs |
| [[T11]] | `done` | — |  | Full verification sweep |

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
