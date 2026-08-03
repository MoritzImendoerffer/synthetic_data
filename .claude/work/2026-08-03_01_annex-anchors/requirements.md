# Requirements — annex anchor quality

Source: conversation of 2026-08-03, following the `" | "` cell-separator change
(row quotes now carry their column boundaries).

## Problem

Three properties matter for an annex quote, and the corpus checks only the first two:

1. **Grounded** — the span exists in the rendered document (`check_grounding.py`, hard gate).
2. **Distinctive** — the span identifies one place (`specificity_report`, advisory).
3. **Self-sufficient** — the span alone justifies the label (nothing checks this).

Measured state on 2026-08-03 (after the separator change, 1476/1476 grounded):

| annexes | per-record anchor | piped (row) quotes |
|---|---|---|
| PCMP-001, PCMR-001, PCP-003, PCR-003, PTP-001, RA-001 | rendered table rows | 17–149 each |
| PCP-004…010, PCR-004…010 (14) | **table captions and shared prose** | 1 each (title block only) |

`PCR-005` anchors six `ProcessParameter` records on one caption; `PCP-008` anchors six on
one sentence. Both report clean because reuse of 6 is under `MAX_QUOTE_REUSE = 8`.

The column header is carried nowhere in the annex: from
`"Culture pH | pH | 6.85 | 6.75–6.95 | 6.6–7.1 | WC-CPP | multivariate"` a span-first
consumer cannot tell which range is the NOR. The caption is not lost — it is already
`SourceReference.table_title`.

## Functional requirements

- **R1** Every per-record `SourceReference` in the 14 caption-anchored annexes anchors on
  its own rendered table row, built from the same DataFrame the document renders
  (`row_quotes()`), with the caption left in `table_title`. Applies to parameters, quality
  attributes, proven acceptable ranges and the assertions over them.
- **R2** `specificity_report` flags prose spans reused by more than 3 records (down from 8).
  A rendered table row carries both ends of its relation by construction, so the row case
  keeps the wider cap — a row that names five attributes legitimately anchors five
  assertions (RA-001 does exactly this).
- **R3** A table-anchored `SourceReference` carries its column header as
  `table_header`, a local `schema_ext` extension recorded in `schema_extensions_used`.
  The header is a rendered span, so `check_grounding` verifies it verbatim like a quote.

## Non-functional / constraints

- **C1** No `.qmd` is edited and nothing is re-rendered: annexes are built *around* the
  finished documents (CLAUDE.md, "nothing is added to a document after authoring").
- **C2** No value is hard-coded. Row text and header come from the same
  `outputs/data/*.csv` → helper path the document renders (golden rule 1).
- **C3** `annex_contract/` is vendored and must not be edited; extensions live in
  `schema_ext.py` only (golden rule 4).
- **C4** Registered discrepancies (`authoring/DISCREPANCIES.md`) stay intact.

## Acceptance criteria

- `python build_ground_truth.py && python validate_annex.py` → 20/20 valid.
- `python check_grounding.py` → every quote **and every `table_header`** grounded.
- `GROUNDING_STRICT_ANCHORS=1 python check_grounding.py` → exit 0 with
  `MAX_QUOTE_REUSE = 3` in force (corpus stays at zero weak anchors).
- Every one of the 14 annexes carries row-shaped (piped) quotes for its parameter,
  attribute and PAR records — not 1 piped quote each.
- `uv run python -m pytest -q tests/` passes, with a test that pins R2 and R3.
- Docs updated: `GROUND_TRUTH.md` §1, `README.md`, `CLAUDE.md`, `TASKS.md`, `RUNNER.md`.

## Risks

- **Row text must match the render exactly.** `show()` defaults to `_auto_floatfmt(df)`
  while `_md_rows()` defaults to `.3g`; a table rendered with the auto format and rebuilt
  with `.3g` produces a quote that does not ground. Align the default before re-anchoring.
- **Pydantic drops subclass fields silently.** `model_dump(mode="json")` on a vendored model
  whose field is typed as the base `SourceReference` drops `table_header` with **no
  warning** (verified, pydantic 2.13.4). `serialize_as_any=True` is required at the dump site.
- **Threshold 3 could flag good anchors.** Legitimate multi-relation rows (RA-001 ×6) must
  stay clean, which is why R2 splits the rule by span shape rather than lowering one number.
