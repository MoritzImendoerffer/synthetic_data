# Exploration — where the anchors are built

## Architecture

`build_ground_truth.py` is one module per unit operation, by function prefix:

| step | doc pair | prefix | entity builders |
|---|---|---|---|
| bioreactor (3) | PCP/PCR-003 | `build_` | `build_params`, `build_cqas`, `build_proven_acceptable_ranges` |
| harvest (4) | PCP/PCR-004 | `h_` | `h_params`, `h_cqas`, `h_pars` |
| protein A (5) | PCP/PCR-005 | `pa_` | `pa_params`, `pa_cqas`, `pa_pars` |
| viral inactivation (6) | PCP/PCR-006 | `vi_` | `vi_params`, `vi_cqas`, `vi_pars` |
| CEX (7) | PCP/PCR-007 | `cx_` | `cx_params`, `cx_cqas`, `cx_pars` |
| AEX (8) | PCP/PCR-008 | `ax_` | `ax_params`, `ax_cqas`, `ax_pars` |
| virus filtration (9) | PCP/PCR-009 | `vf_` | `vf_params`, `vf_cqas`, `vf_pars` |
| UF/DF (10) | PCP/PCR-010 | `uf_` | `uf_params`, `uf_cqas`, `uf_pars` |

**The bioreactor pair is the reference implementation for R1** (`build_params` line 226,
`param_row_quotes` line 261, `build_cqas` line 282): the caption stays in `table_title`,
`row_quotes(df, keys)` supplies the per-record `quote`. Its **PAR builder does not** follow
the pattern (line 593 anchors on `PAR_CQA_QUOTE[cqa]`, shared across that CQA's parameters),
so PCR-003 is in scope for the PAR part of R1 too.

The 7 other steps anchor parameters and attributes on the caption string itself — e.g.
`pa_params` line 1725 passes `caption` as both `quote` and `table_title`.

## Which DataFrame each anchor table comes from

Every anchor table is rendered from a shared helper, so `row_quotes()` can rebuild it:

| anchor | plan (`PCP-00N`) | report (`PCR-00N`) |
|---|---|---|
| parameters | `plan_params(UO)` (PCP-004 renders `floatfmt=".0f"`) | `report_params(UO)` |
| attributes | `cqas_by_keys([...])`, PCP-008 also `cqas_for(UO)` | `cqas_for(UO)` and/or `cqas_by_keys([...])` |
| PARs | — | `D.par_table(UO)` (006, 007, 008, 009, 005, 003) |
| capability | — | `cap_for([...])` (`.4g` / `.2f` in some docs) |

Per-document key lists are in each `.qmd` (`show(cqas_by_keys([...]))`); they must be copied
exactly, because the row text depends on the row order of that call.

**Format trap:** `show()` defaults to `_pcpkg._auto_floatfmt(df)`, `_md_rows()` defaults to
`.3g`. Any table the document renders with the auto format and the annex rebuilds with `.3g`
yields an ungrounded quote. Fix `_md_rows`'s default to `_auto_floatfmt` first (T1), then
pass the explicit `floatfmt` only where the `.qmd` passes one.

## R3 — where `table_header` can live

`annex_contract/base.py:231` `SourceReference` has `table_id`, `table_title`,
`section_title`, `heading_path` — **no header field**. `annex_contract/` is vendored and
must not be edited (schema_ext.py docstring, golden rule 4), so the extension is a subclass
in `schema_ext.py`, re-exported as `SourceReference` so every builder picks it up.

Verified on pydantic 2.13.4:

```
ProcessStep(source_references=[SR(..., table_header="A | B")]).model_dump(mode="json")
  → table_header DROPPED, no warning
  → with serialize_as_any=True: preserved
```

The vendored models annotate `list[SourceReference]` (the base), so the single dump site
(`build_ground_truth.py:7340`) must pass `serialize_as_any=True`. Models defined *in*
`schema_ext.py` (StudyDesign, DesignSpace, ProvenAcceptableRange, …) annotate the subclass
and are unaffected either way.

`validate_annex.py` re-validates from disk; pydantic ignores unknown keys inside the base
model, so validation passes — which also means it would ignore a *misspelled* field name.
`check_grounding` must therefore verify `table_header` verbatim, giving the field a gate of
its own.

## R2 — what the threshold change will and will not catch

`specificity_report` counts quote reuse (`MAX_QUOTE_REUSE = 8`) and document occurrences
(`MAX_DOC_OCCURRENCES = 3`). Current worst reuse per annex, post-separator:

```
PCP-005 x7 caption   PCP-008 x6 sentence   PCR-008 x8 sentence   PCR-005 x6 caption
RA-001  x6 ROW       PCP-003 x4 sentence   PCR-003 x4 sentence   PCMR-001 x3 ROW
```

RA-001's ×6 is a *rendered row* listing five attributes, so it legitimately anchors the
entity plus five `parameter_impacts_attribute` assertions. A flat threshold of 3 would flag
it. Hence R2's two tiers: prose > 3 is a weak anchor, a row (detectable by `CELL_SEP`)
keeps the wider cap. Residual prose above 3 after re-anchoring gets fixed by re-anchoring,
never by raising the number back.

## Constraints confirmed in the tree

- No `.qmd` edit, no re-render: annex-only change (CLAUDE.md "nothing is added to a document
  after authoring"). `make corpus` re-renders anyway; the annex step alone is
  `build_ground_truth.py && validate_annex.py && check_grounding.py`.
- `authoring/DISCREPANCIES.md` D-001/D-002 live in document prose, untouched by anchoring.
- `pc_package/first_pass/ground_truth/` is frozen and outside the glob — do not rebuild it.
