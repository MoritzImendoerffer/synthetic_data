# Weak claims — a retired feature, and the reason it was retired

**Status: NOT APPLIED. No document in the corpus contains a planted weak claim.**
`authoring/weak_claims.yaml` is retained as a record of the design and as the starting point
if the feature is ever revived, but nothing reads it into a shipped document. See
"If you revive this" below for the condition that has to be met first.

## What the feature was

The corpus's default invariant is that **every claim is grounded** (CLAUDE.md golden rule 3,
WRITING_GUIDE §3/§6). This feature was the controlled exception: a few fluent, in-register
but unsupported or overstated claims would be planted into a report and **labeled**, so the
benchmark carried negative examples for evidence-grounding tasks — claim verification,
overstatement detection, "does the cited evidence actually support this sentence?".

The motivation is still sound. A grounded corpus teaches a model what supported prose looks
like, but not how to catch the failure it most needs to catch: a claim that *reads*
authoritative and on-register yet is not backed by the data or a citation. Real regulatory
documents contain exactly these.

## Why it was retired

The claims were **planted after authoring**, as a maintainer step. The author is required to
ground everything (WRITING_GUIDE §7a), so a labeled negative could not come from the author
— hence the post-hoc injection. That sequencing is the flaw.

A claim written against a finished document has no way to be *merely unsupported*. It lands
in prose that has already settled every question it touches, so it does not read as an
overreach the evidence fails to justify; it reads as a sentence that fights the paragraph
next to it. Two of the three registered PCR-003 claims demonstrated this when the report was
re-authored:

| claim | what the document now says |
|---|---|
| WC-003-02 — "the screening design alone conclusively establishes the multivariate design space" | "The screening design identifies the factors. The response-surface model is the predictive model and the basis of the design space." |
| WC-003-03 — "guaranteed to produce in-specification drug substance indefinitely, and no further confirmation at commercial scale is required" | "One corner of the characterized region is excluded from the design space." / "The excluded corner is a galactosylation edge of failure, and it bounds the claim made above." |

Both become **internal contradictions** rather than unsupported claims. That silently changes
the benchmark task from *"is this claim supported by the evidence?"*, which requires
grounding, to *"does this sentence contradict another sentence?"*, which is far easier and a
different capability. A model could score well without doing any evidence grounding.

Note what caused it: the report got **more** rigorous. It now reports a genuine edge of
failure, and that honest finding is precisely what the planted claim collides with. The
better the document, the worse post-hoc injection behaves.

It is worth being clear that the problem was **not** stylistic. Measured against PCR-003's
own 409-sentence distribution the three claims sat at the 46th, 61st and 68th percentile for
length, with no em-dashes, semicolons, bold or banned phrases. They would not have been
findable by surface style. The defect was invisible to every gate, including the register
gate — which is exactly why it is written down here.

## The principle this establishes

> **A benchmark negative must be authored as part of the document's argument, not injected
> into a finished document.**

Anything that changes what a document *claims* has to be present while the argument is being
built, so the surrounding prose accommodates it coherently. This generalises beyond weak
claims: the same reasoning applies to any post-hoc content edit.

Post-hoc steps that only build artifacts *around* the text remain fine — the ground-truth
annex, the rhetorical layer, the grounding check. Those never modify what the document says.
When `check_grounding` fails, the fix direction is always to re-anchor the annex quote to the
document, never to edit the document to suit the annex.

## If you revive this

Do not reinstate the injection step. Instead, specify the intended weak claims to the author
**up front**, as part of the authoring inputs, so they are written into the narrative in one
pass:

1. Put the intended claims (id, section, weakness type, and the *fact* they distort) in the
   brief or the story bible, so the single author sees them before writing.
2. Have the author write them into the argument, positioned so that no neighbouring sentence
   directly rebuts them — unsupported, not contradicted.
3. Keep the labeling exactly as designed: the registry records the verbatim quote, the
   weakness type, the rationale and the `correct_version`; the annex carries
   `support = "unsupported"` so the span **grounds** while being **labeled weak**.
4. Verify with `authoring/build_weak_claims_annex.py`, which hard-fails on an ungrounded
   claim.

This conflicts with WRITING_GUIDE §7a, which currently forbids the author from writing
ungrounded claims. Reviving the feature means amending that rule to "you write only the
weak claims named in your brief, and nothing else ungrounded" — deliberately, not by
accident.

A separate option worth considering is to keep contradiction as its own labeled category
(a `contradicted_by_document` weakness type) rather than treating it as a defect. That is a
benchmark design decision, not a mechanical one, and it should be made explicitly.

## Current state of the machinery

- `authoring/weak_claims.yaml` — the three PCR-003 entries, retained as a record. Not applied.
- `authoring/build_weak_claims_annex.py` — still works; hard-fails because the claims are not
  in the document. That failure is correct.
- `pc_package/build_ground_truth.py` `build_weak_claims()` — skips any registered claim whose
  quote is absent from the document and prints a warning, so a document with no planted
  claims is a clean, buildable state rather than a guaranteed grounding failure.
