---
type: pm-archive
tags: [pm]
---

# Finished epics

One row per epic that has left the board. The notes themselves are under
`docs/pm/archive/<epic>/` — board, epic note, task notes and decisions, moved whole and never
deleted.

**A row is added by `/ship`, before the notes move.** `scripts/pm_notes.py` archives the previous
epic when a new one starts, so the last thing `/ship` owes this file is the row; writing it later
means writing it from memory.

| Epic | Ran | What it shipped | Results |
|---|---|---|---|
| [2026-08-03_01_annex-anchors](archive/2026-08-03_01_annex-anchors/_Board.md) | 2026-08-03 | Every annex record anchored on its own rendered table row. Row anchors 285 → 653, annexes with at most one row anchor 14 → 0, gated spans 1476 → 2084, and `SourceReference.table_header` added in `schema_ext.py` | [2026-08-03-annex-anchors.md](../results/2026-08-03-annex-anchors.md) |

The epic currently on the board is [[epic]] — `2026-08-16_01_register-from-four-sources`, which
replaced the row above on 2026-08-16.

| Epic | Shipped | What it produced |
|---|---|---|
| `2026-08-16_01_register-from-four-sources` — make the corpus argue | 2026-08-17 | Four sources extracted and the register band rebuilt on them, the `therefore` cap removed, `WRITING_GUIDE.md` §2c/§2d/§2d bis amended, a 120-quote moves catalogue, the discrepancy carrier (`authoring/discrepancies.yaml` + brief §5c), and `PCP-003` + `PCR-003` re-authored and measured. **One clean win in five**; the remaining 18 documents are blocked on a second two-document round. [Results](../results/2026-08-17-register-pilot.md) · [what remains](../next/register-from-four-sources.md) |
