# Rhetorical / linguistic-pattern annex layer

The ground-truth annexes label the corpus's **entities and values** (parameters, CQAs,
studies, capability, deviations). This layer adds the corpus's **rhetorical structure** —
which spans of prose are a *problem statement*, a *claim*, a *justification*, and so on, and
which justification supports which claim. It turns each report into labeled data for
discourse / argument-mining NLP: claim–evidence linking, argument-structure parsing, and
hedge and boundary detection.

> **Note.** This layer is *annotation over existing prose*. It never changes what a document
> says, which is why it survived the retirement of the planted weak-claim feature
> (`authoring/WEAK_CLAIMS.md`) untouched. The `weak_claim` role below is unused on `main`:
> no document here contains a planted claim, so the builder merges none. It carries spans
> only on `feature/weak-claims-via-brief`.
>
> **Coverage is complete**: all eight `PCR-00N` reports plus `PCMR-001` carry a layer,
> 315 spans in total. **One mechanism, since 2026-08-18**: every curated span lives in
> `authoring/rhetorical/<DOC>.spans.yaml` and is read by `build_rhetorical_spans()`. The eight
> Python span tables were converted to YAML in that unification, and the annexes rebuilt with no
> diff, which is what proved the conversion changed nothing.
>
> The one exception is not curated prose. `PCMR-001` also carries 17 `deviation_disposition`
> spans, one per row of the campaign deviation register, and `pcmr_dev_spans()` builds them from
> `outputs/deviations.csv`. A rendered data row belongs in code, not in a curated file: freezing
> it would hard-code a value that a reseed changes. So `PCMR-001.spans.yaml` holds 32 spans and
> the annex holds 49.
>
> **Put new layers in a YAML file, not in the builder.** The earlier rule here said the opposite,
> for a real reason: the external YAML once went stale and shipped an *empty* layer, because the
> agents re-grounding the annexes fixed every quote they could see in the file they were editing
> and never opened a registry that sat outside it. What fixed that was not co-location but the
> hard gate — `build_rhetorical_spans()` now fails the build when any span stops matching its
> document, so a stale layer cannot ship quietly whichever file it lives in. With the failure
> mode closed, the Python tables were 994 lines of quoted prose in a 7,000 line builder, editable
> only by someone reading Python.
>
> The spans are tied to a specific revision of a document, so **re-authoring a report
> invalidates them wholesale** — after the 2026-07 register correction, 34 of PCR-003's 37
> spans no longer matched. Re-curate as part of the annex step, not as a later task.

The layer is **grounded** exactly like every other annex quote: each span's `quote` must
appear verbatim (whitespace-collapsed) in the rendered document (`build_rhetorical_annex.py`
enforces this). It is **build-then-annex**: authored from the final text, so the spans and
the document cannot disagree. **The roles are annotated on finished text and are never authoring
instructions.** Until 2026-08-19 this paragraph said the opposite — that the roles were "the
concrete text-span realizations of the scaffolds and rigor obligations `section_plan.yaml`
assigns each section" — and the section plan told the author to perform those obligations. Each
of the eight sentences the owner rejected in `PCR-005` on 2026-08-18 was one of them being
performed, and the annex then labelled one of those sentences (`PCR-005-R17`) as its canonical
`mechanistic_warrant`. The obligations now live in `authoring/REVIEW_CHECKLIST.md` as questions
a reviewer asks afterwards; nothing an author reads names a role.

## Roles (the taxonomy)

Each span carries exactly one `role`:

| role | what it marks | typical cue / origin |
|---|---|---|
| `problem_statement` | the situation and complication a section opener sets — the uncertainty, risk or gap that motivates a section or the study | "whose interaction was not quantified", "at risk here" |
| `claim` | an Answer / finding asserted up front (the point of a section or paragraph) | topic sentence; "stated first"; "the step is well understood" |
| `justification` | evidence or reasoning offered for a claim: an effect, a table row, a diagnostic, a statistic | "@tbl-…", "effect … (p < …)", "because …" |
| `mechanistic_warrant` | a physical/chemical mechanism explaining a result (a justification that reasons from mechanism). **It must name a physical cause** — which species, which interaction, which property, in which direction. A category label standing where the cause belongs ("acts through the capacity of the bed", "behaves as a resin property", "follows from the physical chemistry of affinity capture") is **not** a warrant and is not labelled as one; 6 of the 26 spans so labelled on 2026-08-18 carried such a frame (`docs/results/2026-08-18-track-d-stopped.md` §5.6) | "at the operating pH the antibody carries …"; "lowering the pH protonates the histidine residues at the Fc–ligand interface and reduces affinity" |
| `hedge` | a calibrated qualification signalling limited certainty | "is consistent with", "suggests", "more modest", "attributable to the assay" |
| `bounded_conclusion` | a claim explicitly bounded by range / model / assumption / scale-down | "across the characterized ranges", "on the qualified scale-down model" |
| `cross_step_credit` | attributes control of a shared attribute across *named* steps / documents | "cleared to release levels by … PCR-005, PCR-007, PCR-008" |
| `deviation_disposition` | the adverse-finding → investigation → disposition move | "was investigated, bounded … and retained" |
| `deferral` | points to an appendix / paired doc / SOP / AMV instead of "data not shown" | "Appendix C", "given in the deviations section" |
| `restatement` | a claim restated elsewhere in different words (coreference) — links to the original claim | high mannose restated across subsections |
| `weak_claim` | *(unused — feature retired)* an unsupported / overstated claim merged from `weak_claims.yaml` | see `WEAK_CLAIMS.md` |

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
        --file pc_package/PCR-003_bioreactor.qmd

Exit 0 iff every span grounds and every relation target resolves.

## Why it is worth labeling

A model can be fluent yet fail the reader's real test: *is this sentence a claim, and does
the cited evidence support it?* Labeling the rhetorical roles — and, via the weak-claims
layer, which claims are unsupported — makes that test scorable, and the argument links make
claim–evidence retrieval a first-class benchmark task.
