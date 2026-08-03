# Ground truth — how the annexes link to the reports

Each document in the corpus has a **ground-truth annex** (`ground_truth/<ID>.json`) that
validates against `schema_ext.GroundTruthAnnex`. The report is the **input** an NLP system
sees; the annex is the **answer key** — the gold labels for the target tasks (entity
recognition and linking, study/design-space extraction, claim–evidence pairing,
unsupported-claim detection, extractive summarization). This note explains the mechanism
that ties the two together, why it is built the way it is, and how it relates to techniques
you may have met under other names.

---

## 1. The link is a *verbatim quote*, not an offset or an embedding

Every label in an annex — an entity, a study, a design space, a PAR row, an assertion, a
report-section statement, a weak claim, a rhetorical span — carries one or more
`SourceReference` objects, and each `SourceReference` has a **`quote`**: a short string that
must appear **verbatim** in the rendered document. `check_grounding.py` extracts the plain
text of the `.docx`, collapses whitespace, and asserts that every `quote` is a substring of
it. Any quote that isn't present fails the gate.

Exactly one piece of document structure survives that extraction: a **table cell boundary
reads as `" | "`** (`check_grounding.CELL_SEP`). Everything else — tags, line wraps, runs of
spaces — collapses to a single space, and sub/superscript digits fold to plain digits
(`SCRIPT_DIGITS`: the same `log₁₀` label renders both ways across the corpus, so it is a
rendering artifact, not content). Prose quotes are unaffected by the separator, because a
sentence lives inside one paragraph and never crosses a cell boundary; row quotes carry it, so
a consumer can split the row back into the cells the document actually has.

A row still does not say what its columns *mean*, so a table-anchored reference also carries
`table_header` — the rendered header row, gated verbatim like the quote itself. Between the
two, `"Culture pH | pH | 6.85 | 6.75–6.95 | 6.6–7.1 | WC-CPP | multivariate"` becomes readable
from the span alone: the fourth cell is the NOR because the header says so. The caption is
already `table_title`, and the section is `section_title` / `heading_path`, so neither belongs
in the quote — concatenating them would produce a string that appears nowhere in the document
and forfeit the substring test.

We call this **verbatim span grounding**. The idea is simple but load-bearing: *a label is
only allowed to exist if it can point at the exact span of source text it describes, by
quoting it.* The quote is the alignment between the gold label and the report. Nothing in
the annex is allowed to "float free" of the document.

**Why a quote rather than the more usual alternatives?**

| Locator | How it points at a span | Trade-off |
|---|---|---|
| **Character offsets** (start/end indices) — CoNLL/BIO, BRAT `.ann`, spaCy/Prodigy spans | "characters 4120–4145" | Precise, but brittle: any re-render, whitespace reflow, or docx→pdf change shifts every offset. Needs the exact same serialization forever. |
| **Embedding / fuzzy match** | "the span most similar to X" | Robust to paraphrase, but *not checkable* — there is no crisp pass/fail, so it can't gate a build. |
| **Verbatim quote** (what we use) | "the span reading *…*" | Survives reflow (we match under whitespace-collapse), is self-describing (you can read the label and see what it refers to), and gives a **crisp, automatable pass/fail** — exactly what a CI gate needs. |

The cost of the quote approach is that a quote must be chosen to be unique-enough and must
be updated if the prose changes — which is why re-authoring a report forces its annex to be
rebuilt (a stale quote simply stops grounding, and the gate catches it).

### Grounding is necessary but not sufficient: the quote must also *attest*

A quote can ground perfectly and still be useless. A table caption exists in the document, so
it passes the gate — but if fourteen records all quote the same caption, the reference says
"somewhere in this document" rather than naming the evidence. The same is true of a bare
label: `"Production Bioreactor"` appears fourteen times in the master plan as a heading and a
table cell, so quoting it identifies nothing.

`check_grounding.specificity_report` therefore applies a second, weaker test for
**non-distinctiveness**, and reports what it finds as *weak anchors*:

| Signal | Threshold | What it means |
|---|---|---|
| one **prose** span reused across records | more than 3 | the caption failure: the span stands in for records it names none of |
| one **rendered row** reused across records | more than 8 | a row may state several relations at once, but not many |
| the quote occurs many times in the document | more than 3 | the reference is ambiguous |

The reuse ceiling is two-tier because the two shapes fail differently. A row carries both ends
of its relation by construction, so reuse is normal — RA-001's ranking rows name five
attributes each and rightly anchor five assertions. A sentence reused four times is almost
always the caption failure instead. Every case in this corpus that looked like a legitimate
exception turned out not to be one: where a sentence genuinely stated three relations, the
shortest contiguous slice naming each record was available inside it ("released N-glycan
mapping, which reports afucosylation"), and where a claim quantified over parameters without
naming any ("no process parameter had a significant effect"), the per-parameter classification
sentence in §9 stated the same result for one named parameter. Fix a weak anchor by finding
the span that names the record — not by raising the number.

It is deliberately **not** a length rule. The corpus convention is to anchor a per-record
assertion on the **rendered table row** carrying the relation, and those rows are short.
`"Culture pH | pH | 6.85 | 6.75–6.95 | 6.6–7.1 | WC-CPP | multivariate"` names both ends of
what it asserts, which makes it a far better anchor than a long sentence that merely
discusses the topic. An earlier word-count version of this check flagged 135 false positives,
nearly all of them good rows.

`build_ground_truth.row_quotes` rebuilds those rows from the same DataFrame the document
renders — joining the cells with `CELL_SEP` through `_join_cells`, which is how the row reads
in the extracted text — so the anchor stays verbatim and stays correct when the seed changes.
Keep the separator when you hand-build a partial row (RA-001 anchors on the leading cells of
its ranking rows): a space-joined row still grounded before the separator existed, but it
handed the consumer `"Culture pH pH 6.85 …"`, in which nothing marks where the parameter name
stops and its unit begins. The corpus is at **zero** weak anchors; `GROUNDING_VERBOSE=1`
lists any that appear, and `GROUNDING_STRICT_ANCHORS=1` turns the advisory into a gate.

---

## 2. Build-then-annex: the answer key is written *from* the finished report

The annex is produced **after** the report exists, from that report's final text. The
benchmark never runs a model to derive the annex at scoring time — the annex *is* the gold.
Three kinds of content are produced three different ways:

- **Deterministic (no model).** Numeric and entity values (parameters, CQAs, acceptance
  criteria, run counts, PAR ranges) are read from the **same seeded CSVs the report renders
  from** (`build_ground_truth.py` pulls `outputs/data/*.csv` via `_pcpkg`). Because both the
  document and the annex derive every number from the one source of truth, they *cannot*
  disagree on a value by construction. The `quote` strings are curated fragments chosen to
  exist in the prose.
- **Model-annotated, then verified.** The discourse layer — `rhetorical_spans` (roles such
  as `claim`, `justification`, `mechanistic_warrant`, with `supported_by` claim→evidence and
  `restates` coreference links) — is labelled by an annotation agent reading the finished
  report. So an LLM *does* label claims and their support, but only as a one-time
  **gold-creation** step, and every span it emits is then (a) grounded (quote verified
  verbatim) and (b) schema-validated. It is authoring under constraints, not an inference the
  benchmark measures.
- **Maintainer-planted.** The `weak_claims` (deliberately unsupported/overstated sentences)
  are hand-written in `authoring/weak_claims.yaml`, placed verbatim into the report, and
  labelled `support: "unsupported"`. They ground (the quote is in the document) but are
  marked as *not* supported by evidence — negative examples for unsupported-claim detection.

So: **report = input · annex = gold · quote = the alignment.** An LLM helps *create* the
gold (it writes the report and annotates argument structure), but it is fenced in by
verbatim grounding and schema validation, and the numeric truth is derived deterministically.

---

## 3. The other half: a schema constrains the *shape* (the "pass a Pydantic model" idea)

Verbatim grounding checks that a label is *anchored to the source*. A separate mechanism
checks that a label is *well-formed*: the whole annex must validate against the Pydantic
model `GroundTruthAnnex` (in `schema_ext.py`), enforced by `validate_annex.py`. Fields,
types, and enum values (parameter classifications, CQA criticality, rhetorical roles,
weakness types) are all checked.

This is the same discipline as **schema-constrained generation** — the technique you were
thinking of when you said "passing a Pydantic object to them." There, you hand a model a
schema and require it to emit conforming JSON. It shows up as:

- **Provider-native structured output**: OpenAI "Structured Outputs" (a JSON Schema),
  Anthropic tool use (`input_schema`), Google function calling — the model is steered to
  return schema-valid JSON.
- **Libraries around it**: *Instructor* (give it a Pydantic model, it validates + retries),
  *Outlines* / *Guidance* / *LMQL* / *jsonformer* (grammar- or FSM-constrained decoding, so
  malformed tokens are impossible to sample).

The key thing to internalise: **schema constraint guarantees *shape*, not *truth* and not
*source-attribution*.** A model can emit a perfectly schema-valid object that is entirely
made up. That is exactly why this corpus layers three independent guarantees:

| Guarantee | Mechanism here | What it does *not* cover |
|---|---|---|
| **Shape** — valid fields/types/enums | Pydantic `GroundTruthAnnex` + `validate_annex.py` | whether the content is true or in the document |
| **Attribution** — every label points to a real span of the source | verbatim `quote` + `check_grounding.py` | whether the *label* (e.g. the role) is the right one |
| **Value correctness** — numbers match reality | derive from the seeded CSVs (single source of truth) | prose phrasing (handled by grounding) |

Structured output gives you the first row only. Grounding adds the second; deterministic
derivation adds the third.

---

## 4. Related techniques, briefly (so the landscape is clear)

Verbatim span grounding sits in the family of **attribution / grounded-generation** methods.
If you want to read around it:

- **Attributed QA / citation.** Systems that must *cite* their sources so a claim can be
  checked against them — the *AIS* framework ("Attributable to Identified Sources",
  Rashkin et al.), *RARR* (attribute-then-revise), "According-to" prompting, and the inline
  citations of retrieval-augmented generation (RAG). Our quote is the same idea used in
  reverse: instead of a system citing at answer time, the *gold* cites at authoring time.
- **Faithfulness / entailment verification.** Rather than requiring a verbatim quote, these
  check that a generated sentence is *entailed* by a source passage using an NLI model —
  *SummaC*, *QAFactEval*, *FactCC*, *AlignScore*. This is softer (handles paraphrase) but
  probabilistic, so it measures faithfulness rather than gating a build; verbatim matching is
  the strict, checkable end of the same spectrum.
- **Span-annotation formats.** Classic annotation tools (BRAT, Prodigy, CoNLL) locate spans
  by **character offsets**; we locate them by **quote** for the robustness/checkability
  reasons in §1.
- **Constrained decoding** (Outlines/Guidance/etc.) — as in §3, for shape.

Our contribution is just to **compose** them into a single answer-key format: an LLM authors
and annotates, a Pydantic schema fixes the shape, verbatim quotes fix the attribution, and
the seeded model fixes the numbers.

---

## 5. Using the annexes as a benchmark

At evaluation time you give a system **only the report** and ask it to reproduce the annex's
annotations — recognise and link the entities, extract the studies and design space, pair
each claim with its supporting evidence, flag the unsupported claims — and score its output
against the gold annex. Because every gold label is grounded and schema-valid, the target is
unambiguous and machine-checkable.

**Rebuild discipline.** Whenever a report's prose changes, rebuild its annex:
`python build_ground_truth.py` (regenerates from the CSVs + the curated quotes) →
`python validate_annex.py` (schema) → `python check_grounding.py` (grounding vs the rendered
`.docx`). A quote that no longer appears in the document fails grounding; fix it to a verbatim
fragment of the new text. This is why the annex and the document can never silently drift.
