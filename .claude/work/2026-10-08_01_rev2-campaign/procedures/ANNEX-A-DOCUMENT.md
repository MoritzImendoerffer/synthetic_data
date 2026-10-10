# Procedure: write the Version 2.0 annex builder of ONE promoted document

Written 2026-10-10 (third session). Run it only after the document is promoted
(`pc_package/<DOC>_<uokey>.qmd`, rendered to `.docx` and `.pdf`), because every quote is tied to
one revision of the text (`authoring/RUNNER.md` step 5).

## What changed in the machinery (2026-10-10)

- A Version 2.0 builder now lives in its own module, `pc_package/annex_builders/<doc>.py`
  (`pcp_007.py` builds `PCP-007`), defining `build()` that returns the `GroundTruthAnnex`.
  `build_ground_truth.BUILDERS` uses the module as soon as it exists, in place of the Version 1.0
  builder in `build_ground_truth.py`. Several documents can therefore be annexed in parallel
  without editing one shared file.
- `python build_ground_truth.py <DOC> [<DOC> ...]` builds only the documents named, whether or not
  they are in `REV2_READY` yet.
- `python check_grounding.py --doc <DOC>` checks only that annex.

## The launch prompt (ONE agent, model `opus`, fresh context)

> Write the Version 2.0 annex builder of `<DOC>` (<Title>) as
> `pc_package/annex_builders/<module>.py`, per
> `.claude/work/2026-10-08_01_rev2-campaign/procedures/ANNEX-A-DOCUMENT.md` (read it first, in
> full). The document is final and promoted: `pc_package/<DOC>_<uokey>.qmd`, rendered to
> `pc_package/<DOC>_<uokey>.docx`.

## What the agent reads

- `pc_package/GROUND_TRUTH.md` (the method: verbatim span grounding, row anchors, the reuse
  ceilings, weak anchors) and `authoring/RUNNER.md` step 5.
- The document: its `.qmd` (it must, to find the objects each table prints) and its rendered text
  (`check_grounding.docx_text` on the `.docx` is exactly what the gate reads).
- The model builder for its document type, in `pc_package/build_ground_truth.py`:
  - a step plan: `build_plan_viral_inactivation` (PCP-006), `build_plan_protein_a` (PCP-005),
    `build_plan_bioreactor` (PCP-003);
  - a step report: `build_report_protein_a` (PCR-005);
  - an investigation: `build_investigation` (INV-001);
  - the master plan: `build_master_plan` (PCMP-001).
  Read the shared helpers they call (`qmd_namespace`, `qmd_ctables`, `ctable_rows`, `row_quotes`,
  `md_string_rows`, `_adders`, `ref`, `meta`, `rev2_layer`, `revision_layer`,
  `acceptance_criteria_layer`, `size_variant_refs`, `build_rhetorical_spans`, ...).
- The Version 1.0 builder of the same document, only for its concept ids and the kinds of record it
  produced. Never reuse a Version 1.0 quote: the text changed.
- `pc_package/schema_ext.py` for the record types.

## Rules

1. **The text is final.** Never edit the document. When a quote does not ground, re-anchor the
   quote on the text, never the reverse. If the document is wrong (a number that disagrees with
   its own table, a broken table), stop and report it.
2. **Do not edit `build_ground_truth.py`** or any other shared module. Import what you need
   (`import build_ground_truth as G`, or `from build_ground_truth import ref, ctable_rows, ...`).
   Put a helper you need and do not find into your module, and name it in your report if other
   builders could use it.
3. **Anchor every parameter and attribute record on its own rendered row** (`ctable_rows` for a
   `ctable`/`T.` table, `row_quotes` for a `show()` table, `md_string_rows` for a markdown helper
   table), with `table_header=rows.header`. A caption grounds while attesting nothing.
4. **Every value comes from the document's namespace or the CSVs** (`qmd_namespace(qmd)` executes
   the document's chunks and returns its variables), never typed.
5. **Prose reuse at or below the ceiling** (`check_grounding.MAX_PROSE_REUSE`; rows
   `MAX_ROW_REUSE`). Fix a weak anchor by finding the span that names the record, never by raising
   a threshold.
6. **Version and revision:** `rev2_layer(doc, file)` (version, effective date, supersedes, revision
   history anchored on the rendered rows).
7. **The discourse layer is part of the annex.** For a report (`PCR-00N`, `PCMR-001`), the
   rhetorical spans in `authoring/rhetorical/<DOC>.spans.yaml` were curated against the Version
   1.0 text. Re-curate the file against the current text in the same pass (each quote verbatim,
   each span's role still true of the sentence). A plan or an investigation has no spans file.
8. **`weak_claims` stays empty** (CLAUDE.md: on `main` every claim is grounded).
9. Cover what the model builder covers for its type: inventory, entities per section (step,
   parameters, attributes, methods, equipment, sites), concepts, studies and design spaces where
   the document has them, proven acceptable ranges, acceptance criteria (Version 1.0 superseded
   and Version 2.0 in force where the document prints `T.criteria_change`), document relationships
   and explicit non-claims, report sections with statements, assertions.

## Gate (run from `pc_package/`)

```bash
uv run python build_ground_truth.py <DOC>
uv run python validate_annex.py
GROUNDING_STRICT_ANCHORS=1 GROUNDING_VERBOSE=1 uv run python check_grounding.py --doc <DOC>
cd .. && uv run python -m pytest -q tests/test_grounding.py
```

Done when the annex is valid, every quote grounds, there is no weak anchor for this document, and
`tests/test_grounding.py` passes. The coordinator then adds `<DOC>` to `REV2_READY` and to
`ALL_DOCS` in `tests/test_grounding.py` (the agent does not).

## Report

Which model you are; the counts the builder prints (entities, studies, assertions, concepts) and
the number of quotes; any document error found (rule 1); any helper you wrote that belongs in the
shared module (rule 2).
