# CLAUDE.md — conventions for this repository

Instructions for Claude (and any coding agent) working in `synthetic_data`. The goal
is that the generated documents stay **consistent across all unit operations** and
**reproduce consistently** whenever the example is re-run with different settings.
Keep this file short, factual and current.

## What this repo is

A seeded Python model of the **A-Mab** monoclonal-antibody drug-substance process
(`amab_process/`, driven by `config/parameters.yaml`) that generates a **document
corpus** for NLP development — a set of cross-referenced Quarto documents with
machine-readable ground-truth annexes (`pc_package/`). The seeded model is the single
source of truth (`amab_process/`, `scripts/`, `outputs/`). `risk_assessment/build_fmea.py`
is retained as the curated failure-mode/effect/control **content source** for the
Pre-Characterization Risk Assessment (`RA-001`); it is not a shipped deliverable.
(An earlier single consolidated PC report + rendered FMEA were removed — superseded by
the corpus; recoverable from git history if needed.) Full workflow:
[`docs/WORKFLOW.md`](docs/WORKFLOW.md); corpus package:
[`pc_package/README.md`](pc_package/README.md); DoE engine:
[`pc_package/DOE_ENGINE.md`](pc_package/DOE_ENGINE.md).

**The corpus is complete**: 20 documents, all one-pass authored, all annexed and grounded.
To change one, add a unit operation, or re-run the set, start at
**[`pc_package/TASKS.md`](pc_package/TASKS.md)** — it covers what to touch, what to rebuild
afterwards, and the traps. The bioreactor pair `PCP-003` / `PCR-003` is the reference for
structure and depth, but **never** for voice: read the register rule below before writing
anything.

## Golden rules (do not violate)

1. **Single source of truth.** Every number originates in `config/parameters.yaml` →
   the model → `outputs/`. **Never hard-code a value that lives in the config or
   `outputs/` into a `.qmd`, a helper, or an annex.** Read it through `_pcpkg.py` /
   `doe_report.py`, or from the CSV. If you catch yourself typing a set-point, range,
   effect, p-value or Cpk, stop and pull it instead.
2. **Reproducible by construction.** Changing `meta.seed` or any config value and
   running `make clean && make data figures && make corpus` must regenerate the entire
   document set **with no manual edits**. Nothing may depend on values that only a
   previous run happened to produce.
3. **Everything is grounded.** In a ground-truth annex, every `SourceReference.quote`
   must appear **verbatim** in the rendered document, and every entity value must match
   the document (both come from the same CSVs). Prose may only state what the data
   supports — never invent facts, ranges, IDs or units.
4. **Do not modify `nlp_reports`.** It is imported read-only for its Pydantic models
   (via `NLP_REPORTS_PATH`). If a concept is missing, extend it **locally** in
   `pc_package/schema_ext.py` and record it in `schema_extensions_used`.

## The shared machinery — reuse it, don't re-implement

Every corpus document is built from the same modules; per-unit-operation documents
differ only in their `UO` key and unit-specific narrative:

- `pc_package/_pcpkg.py` — data helpers (`csv`, `show`, `plan_params`, `report_params`,
  `cqas_for`, `cap_for`, …), the **document registry** (`DOC_REGISTRY`, IDs, titles),
  the title block, related-documents and SOP/AMV cross-reference tables, and the
  synthetic banner. Add new shared helpers here, not inline in a `.qmd`.
- `pc_package/doe_report.py` — the DoE statistics/figures engine (see its doc).
- `pc_package/schema_ext.py` — the annex schema (`GroundTruthAnnex` + local extensions).
- `pc_package/build_ground_truth.py` / `validate_annex.py` — build and validate annexes.

## Consistency conventions (apply to every unit operation)

- **IDs (fixed scheme):** `PTP-001`, `RA-001`, `PCMP-001`, `PCP-00N` / `PCR-00N`
  (per unit op, `N` = process step 3–10), `PCMR-001`. Filenames:
  `PCP-00N_<uokey>.qmd`, `PCR-00N_<uokey>.qmd`; annex `ground_truth/<ID>.json`.
- **Front matter (identical across documents):** `format:` docx (`reference-doc:
  reference.docx`) + pdf (`documentclass: scrreprt`); `bibliography:
  references.bib`; `toc-depth: 3`; `number-sections: true`;
  `execute: echo:false, warning:false, cache:false`; `jupyter: python3`. First code
  chunk: `sys.path.insert(0, os.path.abspath(".")); from _pcpkg import *`.
- **Every document** opens with `title_block(DOC, UO_TITLE)` + `SYN_BANNER`, an
  Approvals table and Abbreviations, and closes with `# References {.unnumbered}` +
  `::: {#refs} :::`. Use `related_docs_md(DOC)` and `sop_table(...)` for cross-refs.
- **Canonical section order — Report (`PCR-00N`):** Executive summary · Introduction
  (product/UO, objectives, regulatory basis) · Prior knowledge & quality risk basis
  (CQAs in scope, risk-based prioritization from RA-001) · Materials & methods
  (scale-down model & qualification, operation, analytical methods, sampling plan,
  statistical methods) · Study design (factors/ranges, screening, RSM, univariate) ·
  Results (center-point reproducibility, screening effects, RSM models with ANOVA &
  diagnostics, mechanistic interpretation) · Design space · Process capability ·
  Parameter classification · Contribution to the control strategy · Discussion ·
  Conclusions · Deviations · References · Appendices (A screening matrix, B RSM matrix,
  C full effect/coefficient tables, D analytical methods).
- **Canonical section order — Plan (`PCP-00N`):** Purpose & scope · Objectives ·
  Related documents · Prior knowledge & quality risk basis · Materials & methods (SDM
  qualification, operation, analytical methods, sampling, statistical methods) · Study
  design · Acceptance & decision criteria · Data management & integrity · Roles &
  responsibilities · Deliverables & schedule · Risks & assumptions · Approvals ·
  References · Appendices (planned design matrices).
- **Depth follows the design, not a page target.** As built: reports with a DoE run 41–55 pp,
  reports without one 26–28 pp, plans 23–31 pp. Achieve depth with grounded tables, analysis
  and full appendices — never with filler, and never by inventing a DoE for a step that has
  none.
- **Voice (gated):** a process scientist writing material to support a BLA: precise,
  complete, mechanistically reasoned, traceable — and written in **plain technical
  English at about C1 level**, modelled on the published human sources in `refs/text/`
  (PDA TR 60; the A-Mab case study), *never* on an existing document in `pc_package/`.
  Short sentences, almost no em-dashes or semicolons, no coined compounds
  ("host cell protein", not "host-cell-protein"), no commentary on your own rhetoric.
  Measurable targets and worked corrections: `authoring/WRITING_GUIDE.md` §4; verbatim
  exemplars: `authoring/REGISTER_EXEMPLAR.md`. Enforced by `authoring/check_style.py`,
  whose thresholds are calibrated so both human sources pass (`--selftest`).
- **Framing rule:** the screening model identifies effects; the **response-surface
  model is the predictive/design-space model**. State this; don't over-claim the
  near-saturated screening fit.
- **Registered discrepancies are real and deliberately kept.** A few documents contain
  genuine inconsistencies a review should have caught — a PAR analysis that departs from
  the method its own protocol specifies (D-001), and an absolute claim in PCR-003 that the
  corpus's own CQA register contradicts (D-002). They are listed precisely in
  [`authoring/DISCREPANCIES.md`](authoring/DISCREPANCIES.md) so they can be scored. **Do
  not "fix" one without removing its entry**; that silently deletes a benchmark item. An
  *unregistered* inconsistency is a bug — fix it, or register it deliberately.
- **Nothing is added to a document after authoring.** The document a one-pass author
  produces is the document that ships. Post-authoring steps (annex, rhetorical layer,
  grounding check) build artifacts *around* the text and never change what it claims;
  when `check_grounding` fails, the annex quote is re-anchored to the document, never the
  reverse. The planted weak-claim feature is **retired** for exactly this reason — see
  [`authoring/WEAK_CLAIMS.md`](authoring/WEAK_CLAIMS.md) for the failure it caused and the
  condition for reviving it.
- **Ground-truth annexes:** always a `GroundTruthAnnex` with `inventory` +
  per-section `entities` + `concepts` + `studies`/`design_spaces` +
  `proven_acceptable_ranges` + `report_sections` + `assertions`, plus the discourse
  layer `rhetorical_spans` (and `weak_claims`, currently empty — see above). Build them in `build_ground_truth.py`
  from the same CSVs (never hand-write JSON), with doc-specific quotes that exist in
  that document. **How the annex links to the report — the verbatim span-grounding
  method, and how it relates to schema-constrained (Pydantic→LLM) generation and other
  attribution techniques — is documented in [`pc_package/GROUND_TRUTH.md`](pc_package/GROUND_TRUTH.md).**
  The rule in one line: every `SourceReference.quote` is a verbatim substring of the
  rendered document (`check_grounding.py` gates it), numeric values are derived from the
  seeded CSVs, and the whole annex validates against the Pydantic schema
  (`validate_annex.py`).

## Which steps have DoE (affects report content)

Steps with screening + RSM data (use `doe_report.py` fully): **bioreactor (3),
protein_a (5), viral_inactivation (6), cex (7), aex (8), virus_filtration (9)**.
Steps **without** DoE: **harvest (4)** and **UF/DF (10)** — their plan/report present
univariate/qualitative characterization and are correspondingly shorter; do not
fabricate a DoE for them.

## Adding a unit-operation Plan/Report pair

**Do not copy an existing document.** An earlier version of this section said to copy the
bioreactor pair, and that is how the machine register propagated through the whole corpus:
each document inherited the previous one's voice, and the writing guide was then distilled
from the result. All 20 documents had to be re-authored to break the loop.

1. `python authoring/build_brief.py <DOC>` — the grounded facts and the helper inventory.
2. Instantiate `authoring/template.qmd`; set `DOC`, `UO`, `UO_TITLE`.
3. **One agent authors the whole document in one pass**, in `section_plan.yaml` order, from
   `WRITING_GUIDE.md`, `REGISTER_EXEMPLAR.md`, `STORY_BIBLE.md` and the brief — never from a
   sibling `.qmd`. Structure comes from `section_plan.yaml`; voice comes from
   `REGISTER_EXEMPLAR.md`, which is built only from the published human sources.
4. Add the pair's entities and assertions to `build_ground_truth.py`, anchoring each record
   on its rendered table row via `row_quotes()` rather than on a caption.
5. Run the verification checklist below. The full loop is in `authoring/RUNNER.md`.

## Re-running with different settings

1. Edit `config/parameters.yaml` (seed, ranges, CQA limits, coefficients…).
2. `make clean && make data figures` — regenerates all datasets/figures.
3. `make corpus` — re-renders every document and rebuilds + validates the annexes.
   Nothing else should need touching; if a document needs a manual number, that is a
   bug — move the value into the config/helper path.

## Verification checklist (must pass before a document is "done")

- `make data figures` current for the active seed.
- `quarto render <doc>.qmd --to docx` and `--to pdf` succeed with no errors.
- `uv run python authoring/check_style.py <doc>.qmd` passes (the register gate; see the
  Voice rule above). `check_render.py` runs it automatically as a hard gate.
- `python build_ground_truth.py && python validate_annex.py` → all annexes valid.
- `python check_grounding.py` → every annex quote verbatim in the rendered text, and no weak
  anchors. `GROUNDING_STRICT_ANCHORS=1` makes the anchor check a gate; the corpus is at zero.
- No missing glyphs in the PDF (`check_render.py` gates it — a dropped `≥` once turned a
  clearance floor into a point value).
- Section structure matches the canonical order above, at the depth the design supports.

## Environment

Python ≥ 3.11, Quarto 1.7+ with a LaTeX engine (PDF), `statsmodels`/`scipy` for the
DoE engine, `jupyter`/`nbclient` for Quarto's Python engine. Dependencies are declared
twice and must agree: `pyproject.toml` + `uv.lock` (`uv sync`, the tested path) and
`requirements.txt` (pip). The Makefile calls `python3`; if your environment is not on
`PATH`, pass it in: `make test PY="uv run python"`. YAML gotcha: scientific notation
needs a signed exponent
(`2.0e+5`, not `2.0e5`). The published source PDFs live **outside** the repo at
`$SYNTHETIC_DATA_SOURCES` (default
`/home/moritz/Nextcloud/Datasets/synthetic_data/source_documents/`); their page-marked
text extracts are in `refs/text/` (regenerate with `python scripts/extract_sources.py`).
Do not commit source PDFs or invent batch IDs; SOP/AMV numbers are explicitly placeholders.
