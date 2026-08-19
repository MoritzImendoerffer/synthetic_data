---
type: pm-board
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
generated: true
tags: [pm/board]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# Board — the active epic

**[[epic|2026-08-19_02_fifth-round-plan-then-batches]]** · **10 of 41 done** · 31 todo

[[epic|Why this epic]] · [[_Artifacts|The corpus and its gates]] · [[_Archive|Finished epics]]

## Waiting on the project owner

**This is the only section that is yours.** Each is an argument a person has to settle.
**One of them blocks a task below**, named in its own row: until it is settled that work cannot start.

| Decision | Waiting on | Blocks |
|---|---|---|
| [[D8-do-the-batches-continue|D8 — after each batch, does the sampled document pass, and do the batches continue?]] | project owner | each batch's successor (TASK-014.., [[TASK-020..]], [[TASK-028..]], [[TASK-033..) until its row reads PASS]] |

## Not finished — the assistant's work, not the owner's

Nothing in this table needs the project owner. It is what the coding assistant has still to do,
and it is here so the state is visible, not so anyone else acts on it.

| Task | Status | Waiting on | Kind | What it is |
|---|---|---|---|---|
| [[TASK-011]] | `todo` | the assistant | annex | Promote batch B1 (PCR-006, PCR-008, PCR-009, PCR-010): render, re-cut spans, re-anchor, re-ground |
| [[TASK-012]] | `todo` | the assistant | measurement | Sampled blind reading of one document from batch B1 — HALT for the owner (D8) |
| [[TASK-013]] | `todo` | the assistant | measurement | Rebuild-and-reground proof after batch B1 |
| [[TASK-014]] | `todo` | the assistant | document | Author PCR-004 (Harvest and Clarification (Step 4)) in one pass under the rebuilt apparatus, with one content-review cycle |
| [[TASK-015]] | `todo` | the assistant | document | Author PCR-003 (Production Bioreactor (Step 3)) in one pass under the rebuilt apparatus, with one content-review cycle |
| [[TASK-016]] | `todo` | the assistant | document | Author PCR-005 (Protein A Chromatography (Step 5)) in one pass under the rebuilt apparatus, with one content-review cycle |
| [[TASK-017]] | `todo` | the assistant | annex | Promote batch B2 (PCR-004, PCR-003, PCR-005): render, re-cut spans, re-anchor, re-ground |
| [[TASK-018]] | `todo` | the assistant | measurement | Sampled blind reading of one document from batch B2 — HALT for the owner (D8) |
| [[TASK-019]] | `todo` | the assistant | measurement | Rebuild-and-reground proof after batch B2 |
| [[TASK-020]] | `todo` | the assistant | document | Author PCP-004 (Harvest and Clarification (Step 4)) in one pass under the rebuilt apparatus, with one content-review cycle |
| [[TASK-021]] | `todo` | the assistant | document | Author PCP-006 (Low-pH Viral Inactivation (Step 6)) in one pass under the rebuilt apparatus, with one content-review cycle |
| [[TASK-022]] | `todo` | the assistant | document | Author PCP-008 (Anion Exchange Chromatography (Step 8)) in one pass under the rebuilt apparatus, with one content-review cycle |
| [[TASK-023]] | `todo` | the assistant | document | Author PCP-009 (Small-Virus Retentive Filtration (Step 9)) in one pass under the rebuilt apparatus, with one content-review cycle |
| [[TASK-024]] | `todo` | the assistant | document | Author PCP-010 (Ultrafiltration / Diafiltration (Step 10)) in one pass under the rebuilt apparatus, with one content-review cycle |
| [[TASK-025]] | `todo` | the assistant | annex | Promote batch B3 (PCP-004, PCP-006, PCP-008, PCP-009, PCP-010): render, re-cut spans, re-anchor, re-ground |
| [[TASK-026]] | `todo` | the assistant | measurement | Sampled blind reading of one document from batch B3 — HALT for the owner (D8) |
| [[TASK-027]] | `todo` | the assistant | measurement | Rebuild-and-reground proof after batch B3 |
| [[TASK-028]] | `todo` | the assistant | document | Author PCP-003 (Production Bioreactor (Step 3)) in one pass under the rebuilt apparatus, with one content-review cycle |
| [[TASK-029]] | `todo` | the assistant | document | Author PCP-007 (Cation Exchange Chromatography (Step 7)) in one pass under the rebuilt apparatus, with one content-review cycle |
| [[TASK-030]] | `todo` | the assistant | annex | Promote batch B4 (PCP-003, PCP-007): render, re-cut spans, re-anchor, re-ground |
| [[TASK-031]] | `todo` | the assistant | measurement | Sampled blind reading of one document from batch B4 — HALT for the owner (D8) |
| [[TASK-032]] | `todo` | the assistant | measurement | Rebuild-and-reground proof after batch B4 |
| [[TASK-033]] | `todo` | the assistant | document | Author PTP-001 (A-Mab Drug Substance) in one pass under the rebuilt apparatus, with one content-review cycle |
| [[TASK-034]] | `todo` | the assistant | document | Author PCMP-001 (A-Mab Drug Substance) in one pass under the rebuilt apparatus, with one content-review cycle |
| [[TASK-035]] | `todo` | the assistant | document | Author RA-001 (A-Mab Drug Substance) in one pass under the rebuilt apparatus, with one content-review cycle |
| [[TASK-036]] | `todo` | the assistant | document | Author PCMR-001 (A-Mab Drug Substance) in one pass under the rebuilt apparatus, with one content-review cycle |
| [[TASK-037]] | `todo` | the assistant | annex | Promote batch B5 (PTP-001, PCMP-001, RA-001, PCMR-001): render, re-cut spans, re-anchor, re-ground |
| [[TASK-038]] | `todo` | the assistant | measurement | Sampled blind reading of one document from batch B5 — HALT for the owner (D8) |
| [[TASK-039]] | `todo` | the assistant | measurement | Rebuild-and-reground proof after batch B5 |
| [[TASK-040]] | `todo` | the assistant | measurement | Write the batches' results page |
| [[TASK-041]] | `todo` | the assistant | documentation | Move the findings into docs, update the roadmap, retire or reduce the proposal, and ship |

## Done

| Task | Status | Waiting on | Kind | What it is |
|---|---|---|---|---|
| [[TASK-001]] | `done` | — | mechanism | Fix the pilot's inputs before the agent exists: PCP-005 brief, scaffold, blind key, reading protocol |
| [[TASK-002]] | `done` | — | document | Author PCP-005 (Protein A Chromatography (Step 5)) in one pass under the rebuilt apparatus, with one content-review cycle |
| [[TASK-003]] | `done` | — | measurement | The blind reading of shipped vs new PCP-005, recorded verbatim, then the rule applied — HALT for the owner (D7) |
| [[TASK-004]] | `done` | — | measurement | Count the pilot and write its results page |
| [[TASK-005]] | `done` | — | annex | Promote the new PCP-005: render, re-anchor its annex, re-ground the corpus |
| [[TASK-006]] | `done` | — | measurement | Rebuild-and-reground proof after the pilot's promotion |
| [[TASK-007]] | `done` | — | document | Author PCR-006 (Low-pH Viral Inactivation (Step 6)) in one pass under the rebuilt apparatus, with one content-review cycle |
| [[TASK-008]] | `done` | — | document | Author PCR-008 (Anion Exchange Chromatography (Step 8)) in one pass under the rebuilt apparatus, with one content-review cycle |
| [[TASK-009]] | `done` | — | document | Author PCR-009 (Small-Virus Retentive Filtration (Step 9)) in one pass under the rebuilt apparatus, with one content-review cycle |
| [[TASK-010]] | `done` | — | document | Author PCR-010 (Ultrafiltration / Diafiltration (Step 10)) in one pass under the rebuilt apparatus, with one content-review cycle |

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
