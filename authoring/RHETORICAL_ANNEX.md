# Rhetorical / linguistic-pattern annex layer

The ground-truth annexes label the corpus's **entities and values** (parameters, CQAs,
studies, capability, deviations). This layer adds the corpus's **rhetorical structure** —
which spans of prose are a *problem statement*, a *claim*, a *justification*, and so on, and
which justification supports which claim. It turns each report into labeled data for
discourse / argument-mining NLP: claim–evidence linking, argument-structure parsing,
hedge and boundary detection, and (with the weak-claims layer) supported-vs-unsupported
claim classification.

The layer is **grounded** exactly like every other annex quote: each span's `quote` must
appear verbatim (whitespace-collapsed) in the rendered document (`build_rhetorical_annex.py`
enforces this). It is **build-then-annex**: authored from the final text, so the spans and
the document cannot disagree. It composes with the section plan — the roles below are the
concrete text-span realizations of the scaffolds (SCQA/CCC) and rigor obligations that
`section_plan.yaml` assigns each section.

## Roles (the taxonomy)

Each span carries exactly one `role`:

| role | what it marks | typical cue / origin |
|---|---|---|
| `problem_statement` | the Situation+Complication an SCQA opener sets — the uncertainty, risk or gap that motivates a section or the study | "whose interaction was not quantified", "at risk here" |
| `claim` | an Answer / finding asserted up front (the point of a section or paragraph) | topic sentence; "stated first"; "the step is well understood" |
| `justification` | evidence or reasoning offered for a claim: an effect, a table row, a diagnostic, a statistic | "@tbl-…", "effect … (p < …)", "because …" |
| `mechanistic_warrant` | a physical/chemical mechanism explaining a result (a justification that reasons from mechanism) | "at the operating pH the antibody carries …" |
| `hedge` | a calibrated qualification signalling limited certainty | "is consistent with", "suggests", "more modest", "attributable to the assay" |
| `bounded_conclusion` | a claim explicitly bounded by range / model / assumption / scale-down | "across the characterized ranges", "on the qualified scale-down model" |
| `cross_step_credit` | attributes control of a shared attribute across *named* steps / documents | "cleared to release levels by … PCR-005, PCR-007, PCR-008" |
| `deviation_disposition` | the adverse-finding → investigation → disposition move | "was investigated, bounded … and retained" |
| `deferral` | points to an appendix / paired doc / SOP / AMV instead of "data not shown" | "Appendix C", "given in the deviations section" |
| `restatement` | a claim restated elsewhere in different words (coreference) — links to the original claim | high mannose restated across subsections |
| `weak_claim` | an unsupported / overstated claim (merged from `weak_claims.yaml`; `support = unsupported`) | see `WEAK_CLAIMS.md` |

## Relations

Spans link into an argument graph:

- `supported_by: [id, …]` on a **claim** — the justification / mechanistic_warrant spans
  that back it. This is the claim–evidence edge argument mining scores.
- `restates: id` on a **restatement** — the original claim it restates (coreference edge).
- `bounds: id` on a **bounded_conclusion** — the claim it bounds (optional).

## Annotation notes (precedence, from labeling the reports)

- **`problem_statement` in a report is thin and local.** A finished characterization
  report states findings up front, so it rarely opens a section with an explicit
  Situation+Complication (a *protocol* does). In a report the role typically realizes as a
  mid-paragraph caution — "that high R² must not be read as predictive power", "one
  screening run warrants explicit comment before the effects are accepted" — not as a
  section opener. Annotate those.
- **`justification` outranks `hedge` when a cue and an evidence-statement co-occur.** A
  clause like "the residual variation is consistent with measurement reproducibility" both
  hedges ("consistent with") and offers evidence; label it `justification` (its primary
  function). Reserve `hedge` for standalone calibration clauses — "attributable to the
  assay", "read as reliable descriptions … rather than tight point-predictors".

## Representation

Curated per document in `authoring/rhetorical/<DOC>.spans.yaml` (a list of spans with
`id`, `section`, `role`, `quote`, and any relation fields). The nuanced role/relation
judgments are made by an annotator reading the final text (an agent, reviewed) — the same
build-then-annex division as authoring the prose: the model produces the nuanced content,
deterministic tooling grounds and validates it.

`authoring/build_rhetorical_annex.py` then:

1. grounds every `quote` verbatim in the document,
2. merges the `weak_claims.yaml` claims as `role: weak_claim` (`support: unsupported`),
3. validates that every relation target id exists,
4. emits `authoring/out/<DOC>.rhetorical.json` — the annex layer (spans + an
   `argument_links` edge list), ready to merge into the document's GroundTruthAnnex
   (`assertions` / a `rhetorical_spans` extension) when `pc_package/build_ground_truth.py`
   is extended.

Run:

    uv run python authoring/build_rhetorical_annex.py --doc PCR-003 \
        --file pc_package/PCR-003_bioreactor.DRAFT.qmd

Exit 0 iff every span grounds and every relation target resolves.

## Why it is worth labeling

A model can be fluent yet fail the reader's real test: *is this sentence a claim, and does
the cited evidence support it?* Labeling the rhetorical roles — and, via the weak-claims
layer, which claims are unsupported — makes that test scorable, and the argument links make
claim–evidence retrieval a first-class benchmark task.
