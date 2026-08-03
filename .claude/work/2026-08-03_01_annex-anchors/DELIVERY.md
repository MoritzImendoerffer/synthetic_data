# Delivery — annex anchor quality

Status: **implemented, verified, not yet committed** (2026-08-03)

## What changed

**R1 — every record anchors on the row that names it.** Fourteen annexes (`PCP`/`PCR-004`…`010`)
anchored their parameter and attribute records on the *caption* of the table those records sit
in; PCR-005 had six parameters behind one caption. Bioreactor, PCMR-001, PTP-001 and RA-001 had
narrower versions of the same problem (PAR records on a per-attribute sentence, attributes on a
bare label). All of them now cite their own rendered row, rebuilt from the helper the `.qmd`
renders (`param_rows()` / `cqa_rows()` / `par_rows()`).

| | before | after |
|---|---|---|
| row-anchored spans, corpus | 285 | **653** |
| annexes with ≤1 row anchor | 14 | **0** |
| prose spans reused >3× | 14 | **0** |
| spans gated by `check_grounding` | 1476 | **2084** |

**R2 — the reuse rule is two-tier.** `MAX_PROSE_REUSE = 3` (was one flat `MAX_QUOTE_REUSE = 8`),
`MAX_ROW_REUSE = 8`. A row carries both ends of its relation by construction, so reuse is normal
— RA-001's ranking rows name five attributes each and rightly anchor five assertions. A sentence
reused four times is the caption failure. Every case that looked like a legitimate exception had
a better anchor available: a shorter contiguous slice naming one record ("released N-glycan
mapping, which reports afucosylation"), or a per-record sentence elsewhere (§9's per-parameter
classification statement instead of "no process parameter had a significant effect").

**R3 — `SourceReference.table_header`.** New local extension in `schema_ext.py` (never
`annex_contract/`), carrying the rendered header row so a span can be read column by column.
608 of 653 row anchors carry one; partial rows carry the matching partial header.

## Landmines found on the way

1. **`show()` and `_md_rows()` disagreed on float format** (`_auto_floatfmt` vs `.3g`). A row
   rebuilt in the wrong format grounds nowhere. Fixed first, before any re-anchoring.
2. **Pydantic drops subclass fields silently.** `model_dump(mode="json")` on a contract-typed
   `list[SourceReference]` discarded `table_header` with no warning and no validation error.
   Needs `serialize_as_any=True`; a test now pins it.
3. **The corpus renders `log₁₀` two ways.** PCR-008's `.docx` keeps the subscript characters,
   PCR-006's turns them into a subscript run reading `log10` — same label, two renderings,
   because the documents were rendered at different times. Folded on both sides of the
   comparison (`SCRIPT_DIGITS`), like the whitespace collapse.
4. **A presence check that skipped normalisation cost a build.** `build_rhetorical_spans`
   compared a raw quote against normalised document text and declared PCR-003's curated layer
   dead, aborting the build partway — which left later annexes stale on disk while the run
   *looked* fine under `2>/dev/null`. Now `_present()`, used by both presence checks.

## Verification (all green)

```
python build_ground_truth.py                     20 annexes written
python validate_annex.py                         20/20 valid
python check_grounding.py                        2084/2084 spans grounded
GROUNDING_STRICT_ANCHORS=1 python check_grounding.py   exit 0, zero weak anchors
uv run python -m pytest -q tests/                85 passed
```

No `.qmd` was edited and nothing was re-rendered: the annexes are built *around* the finished
documents, per CLAUDE.md. Registered discrepancies (D-001, D-002) are untouched.

## Files

- `pc_package/build_ground_truth.py` — row helpers, header threading, re-anchoring (+599/-…)
- `pc_package/check_grounding.py` — `CELL_SEP`, `SCRIPT_DIGITS`, `normalize`, two-tier rule,
  `table_header` gating
- `pc_package/schema_ext.py` — `SourceReference.table_header`
- `tests/test_grounding.py` — new; cell-boundary round trip, reuse ceilings, header survival
- Docs: `GROUND_TRUTH.md` §1, `README.md`, `CLAUDE.md`, `TASKS.md`, `authoring/RUNNER.md`
- 20 rebuilt `ground_truth/*.json`
