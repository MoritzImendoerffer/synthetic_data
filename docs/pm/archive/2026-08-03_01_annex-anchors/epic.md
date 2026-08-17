---
type: pm-epic
sprint: 2026-08-03_01_annex-anchors
status: delivered
started: 2026-08-03
delivered: 2026-08-03
proposal: none — this unit predates docs/next/
tags: [pm/epic]
---

# Epic — anchor every annex record on the row that names it

Board: [[_Board]] · results:
[`docs/results/2026-08-03-annex-anchors.md`](../results/2026-08-03-annex-anchors.md) ·
exploration: `.claude/work/2026-08-03_01_annex-anchors/exploration.md` · requirements:
`.claude/work/2026-08-03_01_annex-anchors/requirements.md`

**This epic is finished, and it is on the board because nothing has replaced it yet.** It shipped
on `main` as `02a170a`. The next `/explore` archives it into `docs/pm/archive/` automatically.

**The finding.** Three properties matter for an annex quote: that it is grounded, that it is
distinctive, and that it alone justifies the label. The corpus checked the first two. Fourteen
annexes anchored their parameter and attribute records on the *caption* of the table those records
sit in — PCR-005 put six `ProcessParameter` records behind one caption, and it reported clean
because reuse of 6 was under a flat cap of 8. A caption grounds while attesting nothing.

**What shipped.** Every per-record reference now cites its own rendered table row, rebuilt from the
same DataFrame the document renders (`param_rows()` / `cqa_rows()` / `par_rows()`). Row anchors
went 285 → 653, annexes with at most one row anchor 14 → 0, and the spans `check_grounding` gates
1476 → 2084. The reuse rule became two-tier — `MAX_PROSE_REUSE = 3`, `MAX_ROW_REUSE = 8` — because
a row carries both ends of its relation by construction and a sentence does not.
`SourceReference.table_header` was added in `schema_ext.py`, never in `annex_contract/`, so a span
can be read column by column; 608 of 653 row anchors carry one.

**What it cost to find out.** Four landmines, all in the results page: `show()` and `_md_rows()`
disagreed on float format, so a rebuilt row grounded nowhere; Pydantic dropped the subclass field
silently under `model_dump(mode="json")` without `serialize_as_any=True`; the corpus renders
`log₁₀` two ways because the documents were rendered at different times; and a presence check that
skipped normalisation declared PCR-003's curated rhetorical layer dead and aborted a build partway,
which left later annexes stale on disk while the run looked fine under `2>/dev/null`.

**The gate.** `20/20 annexes valid` and `2084/2084 quotes grounded` with
`GROUNDING_STRICT_ANCHORS=1`, plus 85 tests. No `.qmd` was edited and nothing was re-rendered: the
annex is built around the finished document, and the registered discrepancies D-001 and D-002 are
untouched. Re-verified on 2026-08-16 from an unmodified checkout, with the same numbers.

**One note on shape.** This unit predates the `/explore` → `/plan` → `/next` → `/ship` loop, so it
holds a `requirements.md` instead of naming a proposal in `docs/next/`, and its tasks carry no
acceptance criteria. `scripts/pm_notes.py` reads that older shape on purpose; a board that will not
render is a board nobody looks at.
