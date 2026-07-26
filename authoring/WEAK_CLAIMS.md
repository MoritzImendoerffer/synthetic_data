# Weak claims — a deliberate, labeled benchmark feature

The corpus's default invariant is that **every claim is grounded** (CLAUDE.md golden rule 3,
WRITING_GUIDE §3/§6). This feature is the controlled **exception**: a few fluent,
in-register but **unsupported or overstated** claims are planted into a report and
**labeled** as such, so the benchmark carries negative examples for evidence-grounding NLP
tasks — claim verification, hallucination / overstatement detection, "does the cited
evidence actually support this sentence?".

## Why plant them

A grounded corpus teaches a model what *supported* prose looks like, but not how to catch
the failure it most needs to catch: a claim that **reads** authoritative and on-register yet
is not backed by the data or a citation. Real regulatory documents contain exactly these —
an appeal to unnamed "prior experience", a screening result over-sold as a design space, a
robustness claim with no boundary. Labeling a handful lets a benchmark score that skill.

## The three weakness types planted (PCR-003)

Registered in [`authoring/weak_claims.yaml`](weak_claims.yaml); each is a real anti-pattern
the WRITING_GUIDE warns against, so it distorts a specific grounded claim:

| id | type | what makes it weak |
|---|---|---|
| WC-003-01 | `unsupported_prior_knowledge` | attributes a factor conclusion to unnamed "prior manufacturing experience" — no citation, no data — and uses it to dismiss a parameter that is actually classified and studied |
| WC-003-02 | `overstated_outcome` | sells the **screening** model as the predictive / design-space model (the RSM's role) and generalizes to "all foreseeable conditions" |
| WC-003-03 | `unbounded_generalization` | turns a scale-down capability estimate into an indefinite commercial "guarantee" and denies the Stage-2 at-scale confirmation the lifecycle requires |

Each `weak_claims.yaml` entry carries the verbatim `quote`, a `rationale`, and the
`correct_version` it distorts (useful as a paired positive/negative example).

## How they are marked

1. **In the report** — the claim appears verbatim in the prose, phrased naturally. It is
   *not* visibly flagged in the rendered document (that would defeat the detection task).
2. **In the documentation** — this file + the machine-readable registry `weak_claims.yaml`.
3. **In the ground-truth annex** — `authoring/build_weak_claims_annex.py` reads the
   registry, verifies each quote appears verbatim in the document (the same grounding rule
   as `pc_package/check_grounding.py`), and emits
   `authoring/out/<DOC>.weak_claims.json`: labeled assertions with
   `support = "unsupported"`, the `weakness_type`, the quote and the rationale. When the
   full annex is built (`pc_package/build_ground_truth.py`), these records merge into the
   document's annex, so it both **grounds the span** (the quote exists) and **labels it
   weak** (`support = unsupported`).

## Why the gates do not catch them (the point)

The authoring gates check *executable expressions* (`check_render.py`) and *typed numerals*
(`lint_numerals.py`) — not prose overstatement. A weak claim contains no typed measurement
and renders cleanly, so it passes every gate. That gap is deliberate: the weakness is a
**content** judgment, and the label therefore lives in the **annex**, not the gate. This is
also why the feature is safe — it cannot be confused with a build defect, and it never
relaxes grounding anywhere else: a claim not registered in `weak_claims.yaml` must still be
fully supported.

## Build / verify

    uv run python authoring/build_weak_claims_annex.py --doc PCR-003 \
        --file pc_package/PCR-003_bioreactor.qmd

Exit 0 iff every planted quote is grounded in the document. Extend the registry (not the
prose alone) when planting more, so the quote and its label never drift apart.
