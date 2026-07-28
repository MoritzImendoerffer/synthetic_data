# A-Mab Process-Characterization Document Package (synthetic NLP corpus)

Twenty cross-referenced Quarto documents describing the characterization of the *A-Mab*
drug-substance process, each paired with a **ground-truth JSON annex**. The documents are
authored here from the seeded process model and the generated `outputs/`, rendered to **DOCX
and PDF**, and intended as a test corpus for the NLP pipeline in the sibling `nlp_reports`
project: NER, entity linking, summarization, relation extraction and long-document QA.

Two properties hold across the whole set. Every number is generated from the seeded model, so
nothing is typed by hand. And every annex entry quotes text that appears verbatim in its own
document, so the labels cannot drift away from the prose.

> All documents are **synthetic** and carry a synthetic banner on the title page. The sponsor
> (*Novacyte Biologics*), all sites and every SOP/AMV number are fictional. The content
> follows the A-Mab case study (CMC Biotech Working Group, 2009) and FDA / ICH guidance.

## Two things to know before using the corpus

**Two documents contain deliberate defects.** They are genuine inconsistencies that a review
should have caught, kept rather than fixed so a benchmark has something to find:
`authoring/DISCREPANCIES.md` lists each one precisely — which documents, which spans, and
what the correct statement would be. Do not treat the corpus as uniformly correct, and do not
fix a registered entry without removing it.

**Every other claim is grounded.** Outside those registered entries, no document states
anything the seeded data does not support. Labelled unsupported claims exist only on the
branch `feature/weak-claims-via-brief`, never here.

## Document set

IDs follow a fixed scheme. Per-unit-operation plans and reports are numbered by process step,
so cross-references are predictable.

| ID | Class | Subject | Pages |
|---|---|---|---|
| `PTP-001` | Process Transfer Plan | A-Mab drug substance | 24 |
| `RA-001` | Pre-Characterization Process Risk Assessment | drug-substance train | 24 |
| `PCMP-001` | Process Characterization Master Plan | drug-substance train | 24 |
| `PCP-003` / `PCR-003` | Plan / Report | Production Bioreactor (Step 3) | 31 / 55 |
| `PCP-004` / `PCR-004` | Plan / Report | Harvest and Clarification (Step 4) | 24 / 28 |
| `PCP-005` / `PCR-005` | Plan / Report | Protein A Chromatography (Step 5) | 30 / 43 |
| `PCP-006` / `PCR-006` | Plan / Report | Low-pH Viral Inactivation (Step 6) | 27 / 43 |
| `PCP-007` / `PCR-007` | Plan / Report | Cation Exchange Chromatography (Step 7) | 27 / 50 |
| `PCP-008` / `PCR-008` | Plan / Report | Anion Exchange Chromatography (Step 8) | 28 / 50 |
| `PCP-009` / `PCR-009` | Plan / Report | Small-Virus Retentive Filtration (Step 9) | 25 / 41 |
| `PCP-010` / `PCR-010` | Plan / Report | Ultrafiltration / Diafiltration (Step 10) | 23 / 26 |
| `PCMR-001` | Process Characterization Master Report | roll-up of all eight steps | 34 |

**Six steps carry a designed experiment** — bioreactor, Protein A, viral inactivation, CEX,
AEX and virus filtration — with a screening design and a response surface, and their reports
are correspondingly longer. **Harvest (4) and UF/DF (10) have no DoE**; they present
univariate and qualitative characterization instead. That asymmetry is deliberate, and no DoE
is invented for them.

`PCP-003` / `PCR-003` is the reference pair. Read it first if you want to see the intended
structure and depth.

Each document carries a title block (ID, class, version, effective date, product, sites) and a
*Related documents* cross-reference table, and cites placeholder `SOP-####` / `AMV-####`
numbers whose prefixes the `nlp_reports` document-ID matcher recognizes.

## Register

The documents are written in **plain technical English at about C1 level**, modelled on the
two published human sources in `refs/text/`: the A-Mab case study and PDA Technical Report
No. 60. Verbatim exemplar passages are in
[`authoring/REGISTER_EXEMPLAR.md`](../authoring/REGISTER_EXEMPLAR.md); the measurable targets
are in [`authoring/WRITING_GUIDE.md`](../authoring/WRITING_GUIDE.md) §4.

This is enforced rather than aspirational. `authoring/check_style.py` — run by `make style`
and by the authoring gate — measures the sentence-length distribution, the density of
em-dashes, semicolons and coined compounds, and a list of banned tics. Its thresholds are
calibrated so that **both human sources pass** (`check_style.py --selftest`). If a threshold
ever fails the self-test, the threshold is wrong, not the source.

No document in this directory is a voice reference for writing a new one. The exemplar is
built only from the published sources, so the corpus cannot drift by imitating itself — which
it did once, before that rule existed.

## Files

| File | Purpose |
|---|---|
| `PCP-00N_*.qmd`, `PCR-00N_*.qmd`, `PTP-001_*.qmd`, `RA-001_*.qmd`, `PCMP-001_*.qmd`, `PCMR-001_*.qmd` | the twenty documents (Quarto → DOCX/PDF) |
| `*.docx`, `*.pdf` | rendered deliverables |
| `ground_truth/*.json` | one ground-truth annex per document |
| `_pcpkg.py` | shared helpers, document registry, title block, cross-reference tables |
| `doe_report.py` | the DoE analysis engine — see [`DOE_ENGINE.md`](DOE_ENGINE.md) |
| `ra_content.py` | the risk content RA-001 renders, and the tables its annex anchors on |
| `schema_ext.py` | the annex schema: reuses `nlp_reports/app/models`, adds local extensions |
| `build_ground_truth.py` | builds every annex from the same seeded CSVs the documents render |
| `validate_annex.py` | validates every `ground_truth/*.json` against the schema |
| `check_grounding.py` | asserts every annex quote appears verbatim in its rendered document |

## Build, render, validate

```bash
# from the repo root: regenerate the model outputs the documents read
make data figures

# render everything and rebuild + validate + ground-check the annexes
make corpus
```

For one document:

```bash
cd pc_package
quarto render PCR-003_bioreactor.qmd --to docx    # and --to pdf
python build_ground_truth.py                      # rebuild the annexes
python validate_annex.py                          # schema
python check_grounding.py                         # every quote is verbatim in the document
```

`schema_ext.py` imports the `nlp_reports` contract read-only through `NLP_REPORTS_PATH`
(default `/home/moritz/github_repos/nlp_reports`); set that variable if the sibling repo
lives elsewhere. **`nlp_reports` is never modified.**

## The ground-truth annex

Each annex validates against `schema_ext.GroundTruthAnnex`, a container whose blocks each
validate against a named model:

| Block | Model | What it supports |
|---|---|---|
| `inventory` | `DocumentInventoryItem` | document-type classification |
| `entities[]` | `SectionEntityExtraction` (per section) | NER and entity linking |
| `concepts` | `ConceptStore` | canonical entity-linking targets |
| `studies[]`, `design_spaces[]` | `StudyDesign`, `DesignSpace` | designed experiments, design space |
| `proven_acceptable_ranges[]` | `ProvenAcceptableRange` | per-parameter PAR with its basis |
| `report_sections[]` | `ReportSection` / `ReportStatement` | extractive summarization with statement-level citations |
| `assertions` | `AssertionStore` | relation extraction and long-document QA |
| `transfer_gaps[]` | `TransferGap` | transfer-gap QA (PTP-001 only) |
| `rhetorical_spans[]` | `RhetoricalSpan` | discourse roles and claim → evidence edges |
| `weak_claims[]` | `WeakClaim` | labelled unsupported claims — **empty here**, see above |

Two invariants hold for all 1470 quotes in the corpus:

- Every `SourceReference.quote` appears **verbatim** in the rendered document
  (`check_grounding.py` gates it).
- Entity **values** — set-points, NOR/PAR, acceptance criteria, classifications — come from
  the same `outputs/data/*.csv` the documents render from, so annex and document cannot
  disagree on a number.

A quote also has to *identify* its evidence, not merely exist. Per-record quotes anchor on the
rendered **table row** carrying both ends of the relation, and `check_grounding` reports
quotes that are too generic to attest anything. The mechanism, and why it is not a
length rule, is in [`GROUND_TRUTH.md`](GROUND_TRUTH.md) §1.

## Schema extensions (local, and candidates for upstreaming)

The `nlp_reports` contract does not yet cover everything these documents need, so the missing
pieces were added here in `schema_ext.py`, leaving `nlp_reports` untouched. Each annex lists
what it used in `schema_extensions_used`.

1. **`ProcessParameter.parameter_type`** — widened to include `WC-CPP` and `GPP`, the A-Mab
   criticality continuum. Upstream allows only `CPP | KPP | non_critical | unclassified`.
2. **`DocumentInventoryItem.predicted_document_type`** — added
   `process_characterization_plan`, `process_characterization_master_plan`,
   `process_characterization_master_report`, `process_transfer_plan`, `risk_assessment`.
3. **`QualityAttribute`** — added optional `criticality_level`, `tool1_score`,
   `tool2_severity` (A-Mab Tool #1 and Tool #2 criticality).
4. **`StudyDesign`** and **`DesignSpace`** — new. Upstream has no model for a designed
   experiment or a multivariate design space.
5. **`ProvenAcceptableRange`** — new. A PAR is not simply a range: it carries the analysis
   that produced it and the conditions the other parameters were held at.
6. **`RhetoricalSpan`** — new. The discourse layer: role labels plus `supported_by`,
   `restates` and `bounds` edges. See [`../authoring/RHETORICAL_ANNEX.md`](../authoring/RHETORICAL_ANNEX.md).
7. **`WeakClaim`** — new. A labelled unsupported claim, with its weakness type, the reason it
   is unsupported and the correct version. Unused on this branch.

Also flagged, not changed: the `nlp_reports` `regex_matchers.py` DOCUMENT_ID pattern
recognizes `PCR/PVR/PPQ/TT/VAL/AMV/SOP/CS` but not `PTP/PCP/PCMP/PCMR/RA`. Adding those
prefixes there would let it recognize this set's IDs deterministically.

## Further reading

| Topic | Document |
|---|---|
| How the annex attaches to the text, and how that compares with other attribution methods | [`GROUND_TRUTH.md`](GROUND_TRUTH.md) |
| The DoE statistics: designs, models, ANOVA, design space, PAR | [`DOE_ENGINE.md`](DOE_ENGINE.md) |
| The discourse layer and its role taxonomy | [`../authoring/RHETORICAL_ANNEX.md`](../authoring/RHETORICAL_ANNEX.md) |
| Registered defects | [`../authoring/DISCREPANCIES.md`](../authoring/DISCREPANCIES.md) |
| Writing or regenerating a document | [`../authoring/RUNNER.md`](../authoring/RUNNER.md) |
