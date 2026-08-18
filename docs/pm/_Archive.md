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

The epic currently on the board is [[epic]] — `2026-08-18_01_register-third-round`, shipped
2026-08-18 and archived by the next `/explore`.

| Epic | Shipped | What it produced |
|---|---|---|
| [`2026-08-16_01_register-from-four-sources`](archive/2026-08-16_01_register-from-four-sources/_Board.md) — make the corpus argue | 2026-08-17 | Four sources extracted and the register band rebuilt on them, the `therefore` cap removed, `WRITING_GUIDE.md` §2c/§2d/§2d bis amended, a 120-quote moves catalogue, the discrepancy carrier (`authoring/discrepancies.yaml` + brief §5c), and `PCP-003` + `PCR-003` re-authored and measured. **One clean win in five**; the remaining 18 documents are blocked on a second two-document round. [Results](../results/2026-08-17-register-pilot.md) · [what remains](../next/register-from-four-sources.md) |
| [`2026-08-17_01_register-second-round`](archive/2026-08-17_01_register-second-round/_Board.md) — give the author the number | 2026-08-18 | Advisory clause-packing measures in `check_style.py`; `check_discourse.py` behind an optional spaCy extra the build never needs; `WRITING_GUIDE.md` §2d restated as a substitution with the ✓ blocks that taught the fault fixed; brief §5d printing each document's own numbers; and `PCP-003` + `PCR-003` re-authored a second time. **Five of five measures moved in both genres** (`, so ` → 0.0 %, sentence-initial connectives → 4.9 % / 4.0 %, chaining → 46.0 % / 46.1 % unasked) and every line of the pre-fixed stopping rule holds — **and the owner still recognised the pair on its first sentence**, naming three faults nothing measured. D1 settled on option B: the eighteen stay blocked, the three faults are the next target. [Results](../results/2026-08-18-register-round-two.md) · [what remains](../next/register-from-four-sources.md) |
| [`2026-08-18_01_register-third-round`](archive/2026-08-18_01_register-third-round/_Board.md) — measure what the reader named | 2026-08-18 | Two regex counts (`, and `+clause, a **floor**, and `, not `) added to `check_style.py`'s advisory line; the passive rate and the parser and-clause added to `check_discourse.py` on one denominator; brief §5d printing all three back to the author; the write-the-passive rule in `WRITING_GUIDE.md` §2d; and `PCR-003` re-authored a third time with `PCP-003` held at round two as the control. **All three newly printed measures moved** — `, and `+clause 22.6 → 0.5 %, `, not ` 4.3 → 0.0 %, passive 35.4 → 57.4 % and inside the source range — and all eight lines of the pre-fixed stopping rule hold. **The owner's reading names no sentence for the first time**: "The document reads better. Not perfect but ok to me." A count-led sweep then found six measures that moved away from the sources in the same re-author, the two largest being `, which` at 15.33 % and a new staccato measure at 6.86 %. D2 settled. [Results](../results/2026-08-18-register-round-three.md) · [what remains](../next/register-from-four-sources.md) |
