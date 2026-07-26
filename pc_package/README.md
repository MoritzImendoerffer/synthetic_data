# A-Mab Process-Characterization Document Package (synthetic NLP corpus)

A multi-document, densely cross-referenced set of Quarto documents for the *A-Mab*
drug-substance process, each paired with a **ground-truth JSON annex**. The
documents are authored here (reusing the seeded process model and the generated
`outputs/`), rendered to **DOCX + PDF**, and are intended as a test corpus for the
NLP pipeline in the sibling `nlp_reports` project (NER, entity linking,
summarization, long-document QA). Every number is generated from the seeded model
— nothing is typed by hand — and every annex entry is grounded in text that
actually appears in its document.

> All documents are **synthetic** and carry a synthetic banner on the title page.
> The sponsor (*Novacyte Biologics*), all sites and every SOP/AMV number are
> fictional. The content follows the A-Mab case study (CMC Biotech Working Group,
> 2009) and FDA / ICH guidance.

## Status

First Plan/Report pair built for review: **PCP-003 / PCR-003 (production
bioreactor, Step 3)**. Written to BLA-supporting depth — the report is ~35 pages
(full DoE analysis: effect estimates, response-surface models with ANOVA and
lack-of-fit, design space, capability, appendices with the complete design
matrices and effect tables); the plan (protocol) is ~22 pages. The remaining
documents are planned but not yet generated (see *Document set* below).

## Document set and ID scheme

IDs use a consistent scheme; per-unit-operation plans/reports are numbered by
process step (Steps 3–10) so cross-references are predictable.

| ID | Class | Subject | Built? |
|---|---|---|---|
| `PTP-001` | Process Transfer Plan | A-Mab drug substance | pending |
| `RA-001` | Pre-Characterization Process Risk Assessment | derived from PTP-001 | pending |
| `PCMP-001` | Process Characterization Master Plan | drug-substance train | pending |
| `PCP-003 … PCP-010` | Process Characterization Plan | one per unit operation | **PCP-003 done** |
| `PCR-003 … PCR-010` | Process Characterization Report | one per unit operation | **PCR-003 done** |
| `PCMR-001` | Process Characterization Master Report | roll-up | pending |

Steps: 3 bioreactor · 4 harvest · 5 Protein A · 6 viral inactivation · 7 CEX ·
8 AEX · 9 virus filtration · 10 UF/DF. Each document carries a title block
(ID, class, version, effective date, product, sites) and a *Related documents*
cross-reference table; documents also reference placeholder `SOP-####` / `AMV-####`
numbers (prefixes recognized by the `nlp_reports` document-ID matcher).

## Files

| File | Purpose |
|---|---|
| `PCP-003_bioreactor.qmd`, `PCR-003_bioreactor.qmd` | the two documents (Quarto → DOCX/PDF) |
| `PCP-003_bioreactor.{docx,pdf}`, `PCR-003_bioreactor.{docx,pdf}` | rendered deliverables |
| `ground_truth/PCP-003.json`, `ground_truth/PCR-003.json` | composite ground-truth annexes |
| `_pcpkg.py` | shared Quarto helpers, document registry, title-block / cross-ref tables (reuses `outputs/`) |
| `doe_report.py` | DoE analysis engine: effect/coefficient tables, R²/adjusted/predicted R², ANOVA with lack-of-fit, design matrices, RSM contour & diagnostic figures (statsmodels, from the seeded DoE data) |
| `schema_ext.py` | the annex schema: reuses `nlp_reports/app/models`, adds local extensions |
| `build_ground_truth.py` | builds the annexes from the same seeded CSVs the documents render |
| `validate_annex.py` | validates every `ground_truth/*.json` against the schema |

## Build / render / validate

```bash
# from pc_package/ (needs the seeded outputs/ — run `make data figures` at repo root first)
quarto render PCP-003_bioreactor.qmd --to docx   # and --to pdf
quarto render PCR-003_bioreactor.qmd --to docx   # and --to pdf
python build_ground_truth.py                     # (re)build the JSON annexes
python validate_annex.py                         # validate them against the schema
```

`schema_ext.py` imports the `nlp_reports` contract read-only via
`NLP_REPORTS_PATH` (default `/home/moritz/github_repos/nlp_reports`); set that env
var if the sibling repo lives elsewhere. **`nlp_reports` is never modified.**

## Ground-truth annex structure

Each annex validates against `schema_ext.GroundTruthAnnex` — a thin container
whose blocks each validate against a named model and together cover the four NLP
tasks:

| Block | Model | Task |
|---|---|---|
| `inventory` | `DocumentInventoryItem` | document-type classification |
| `entities[]` | `SectionEntityExtraction` (per section) | NER + entity linking |
| `concepts` | `ConceptStore` | canonical entity-linking targets |
| `studies[]`, `design_spaces[]` | `StudyDesign`, `DesignSpace` (new) | characterization objects |
| `report_sections[]` | `ReportSection` / `ReportStatement` | extractive summarization (statement-level citations) |
| `assertions` | `AssertionStore` | relations / long-document QA |
| `transfer_gaps[]` | `TransferGap` | gap / QA (used by PTP/RA later) |

Every `SourceReference.quote` is a verbatim fragment of the rendered document
(checked by a grounding test during the build). Entity **values** (parameter
NOR/PAR/set-point, CQA acceptance, classifications) come from the same
`outputs/data/*.csv` the documents render, so annex and document cannot disagree.

## Schema extensions (local — flagged for upstreaming to `nlp_reports`)

The `nlp_reports` contract does not yet cover a few concepts these documents need.
Per instruction, the missing concepts were **created here** (in `schema_ext.py`),
leaving `nlp_reports` untouched. Each is a candidate to add to
`nlp_reports/app/models` later:

1. **`ProcessParameter.parameter_type`** — widened to include `WC-CPP` and `GPP`
   (the A-Mab continuum). Upstream allows only `CPP | KPP | non_critical |
   unclassified`; every bioreactor parameter is WC-CPP / KPP / GPP.
2. **`DocumentInventoryItem.predicted_document_type`** — added
   `process_characterization_plan`, `process_characterization_master_plan`,
   `process_characterization_master_report`, `process_transfer_plan`.
3. **`QualityAttribute`** — added optional `criticality_level`, `tool1_score`,
   `tool2_severity` (A-Mab Tool #1/#2 criticality).
4. **`StudyDesign`** and **`DesignSpace`** — new models; no upstream equivalent
   for a designed experiment (DoE) or a multivariate design space.

Also flagged (not changed): the `nlp_reports` `regex_matchers.py` DOCUMENT_ID
pattern recognizes `PCR/PVR/PPQ/TT/VAL/AMV/SOP/CS` but not `PTP/PCP/PCMP/PCMR/RA`;
add those prefixes there to recognize this set's IDs deterministically.
