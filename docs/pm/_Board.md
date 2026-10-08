---
type: pm-board
epic: 2026-10-08_01_rev2-campaign
sprint: 2026-10-08_01_rev2-campaign
generated: true
tags: [pm/board]
---

> [!warning] Generated from `.claude/work/2026-10-08_01_rev2-campaign/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# Board — the active epic

**[[epic|2026-10-08_01_rev2-campaign]]** · **15 of 35 done** · 1 doing · 19 todo

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
| [[TASK-015]] | `doing` | the assistant | measurement | HALT: owner reads the pilot |
| [[TASK-017]] | `todo` | the assistant | document | Author PCP-003 Rev 2.0 and re-anchor its annex |
| [[TASK-018]] | `todo` | the assistant | document | Author PCR-003 Rev 2.0 and re-anchor its annex |
| [[TASK-019]] | `todo` | the assistant | document | Author PCP-004 Rev 2.0 and re-anchor its annex |
| [[TASK-020]] | `todo` | the assistant | document | Author PCR-004 Rev 2.0 and re-anchor its annex |
| [[TASK-021]] | `todo` | the assistant | document | Author PCP-006 Rev 2.0 and re-anchor its annex |
| [[TASK-022]] | `todo` | the assistant | document | Author PCR-006 Rev 2.0 and re-anchor its annex |
| [[TASK-023]] | `todo` | the assistant | document | Author PCP-007 Rev 2.0 and re-anchor its annex |
| [[TASK-024]] | `todo` | the assistant | document | Author PCR-007 Rev 2.0 and re-anchor its annex |
| [[TASK-025]] | `todo` | the assistant | document | Author PCP-008 Rev 2.0 and re-anchor its annex |
| [[TASK-026]] | `todo` | the assistant | document | Author PCR-008 Rev 2.0 and re-anchor its annex |
| [[TASK-027]] | `todo` | the assistant | document | Author PCP-009 Rev 2.0 and re-anchor its annex |
| [[TASK-028]] | `todo` | the assistant | document | Author PCR-009 Rev 2.0 and re-anchor its annex |
| [[TASK-029]] | `todo` | the assistant | document | Author PCP-010 Rev 2.0 and re-anchor its annex |
| [[TASK-030]] | `todo` | the assistant | document | Author PCR-010 Rev 2.0 and re-anchor its annex |
| [[TASK-031]] | `todo` | the assistant | document | Author PTP-001 Rev 2.0 and re-anchor its annex |
| [[TASK-032]] | `todo` | the assistant | document | Author RA-001 Rev 2.0 and re-anchor its annex |
| [[TASK-033]] | `todo` | the assistant | document | Author PCMR-001 Rev 2.0 and re-anchor its annex |
| [[TASK-034]] | `todo` | the assistant | measurement | Full rebuild from clean; 21 annexes valid and grounded; Rev 1.0 set still grounds |
| [[TASK-035]] | `todo` | the assistant | documentation | Ship: results page, HANDOFF/TASKS/CLAUDE.md, ROADMAP row, delete both proposals |

## Done

| Task | Status | Waiting on | Kind | What it is |
|---|---|---|---|---|
| [[TASK-001]] | `done` | — | mechanism | Freeze Rev 1.0: tag corpus-rev1.0, copy the 20 DOCX/PDF and annexes to pc_package/superseded/rev1/ |
| [[TASK-002]] | `done` | — | model | Record execution chronology and resolve the calibration-date tension |
| [[TASK-003]] | `done` | — | model | Analytical model: fragments (LMW), per-study method assignment, SEC matrix bias, all on independent RNG streams |
| [[TASK-004]] | `done` | — | model | Hold-time stability and CEX fraction comparability datasets |
| [[TASK-005]] | `done` | — | model | Two-sided capability for acidic variants |
| [[TASK-006]] | `done` | — | model | Specification-driven IACs replace ipc_limits; Rev 1.0 criteria kept as data; integrated-model P(OOS) |
| [[TASK-007]] | `done` | — | mechanism | ctable(): one spec -> HTML table (DOCX merged cells) + raw LaTeX twin (PDF), crossref, footnotes; grounding reads it |
| [[TASK-008]] | `done` | — | mechanism | Registry: INV-001, revision metadata, revision_history(), superseded references, Makefile, schema_ext |
| [[TASK-009]] | `done` | — | mechanism | Authoring artifacts per the owner's rule decisions; brief carries the new facts and table menu |
| [[TASK-010]] | `done` | — | measurement | Rebuild data and figures; old documents still ground |
| [[TASK-011]] | `done` | — | document | Author INV-001 (investigation report) |
| [[TASK-012]] | `done` | — | document | Author PCP-005 Rev 2.0 |
| [[TASK-013]] | `done` | — | document | Author PCR-005 Rev 2.0 |
| [[TASK-014]] | `done` | — | annex | Annex the pilot: INV-001, PCMP-001, PCP-005, PCR-005 |
| [[TASK-016]] | `done` | — | document | Author PCMP-001 Rev 2.0 and re-anchor its annex |

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
