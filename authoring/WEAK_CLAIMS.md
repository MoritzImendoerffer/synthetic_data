# Weak claims — why injection failed, and where the feature lives now

**Status on `main`: NOT APPLIED.** No document on this branch contains a planted weak claim,
and none should: `main` is the fully grounded corpus. `authoring/weak_claims.yaml` is kept
here as the record of the design.

**The feature is active on `feature/weak-claims-via-brief`**, rebuilt around the fix this
document argues for: each claim is assigned in the document's brief *before* it is written,
so the author writes it into the argument in one pass, and its wording is recorded afterwards
by reading the rendered document. Four claims across three documents — two in PCR-003, one in
PCR-009, one in PCP-006. See that branch's own copy of this file for the procedure and the
review checklist.

**Integration rule: rebase that branch onto `main`; never merge it into `main`.** This is not
a style preference. The claims are fluent, in register, and indistinguishable from grounded
prose by inspection — that is the whole point of them — so a leak into `main` is silent and
no gate catches it. It has happened once: PR #6 merged the branch into `main` on 2026-07-28,
against the explicit instruction in its own commit message, and put four unsupported claims
into the fully grounded corpus, where they sat until 2026-08-02 and were then reverted. If
you are about to integrate this branch, you want `git rebase main` on the branch, not
`git merge` on `main`.

Two cheap ways to check `main` is clean, since nothing in the text will tell you:

```bash
# every annex on main must report zero
python3 -c "import json,glob; print(sum(len(json.load(open(f)).get('weak_claims') or []) for f in glob.glob('pc_package/ground_truth/*.json')))"
git log --oneline main --merges --grep=weak-claims   # should find nothing unreverted
```

**The rebase is parked as of 2026-08-03: it is now an authoring job, not a git one.** The
branch is three commits behind `main` and the two sides have re-authored the same documents
independently. Eleven `.qmd` differ on both sides; the three that carry the claims —
`PCR-003`, `PCR-009`, `PCP-006` — differ by around 3,000 lines, and no sentence of the four
registered claims appears anywhere in `main`. There is no hunk-by-hunk merge of two one-pass
authorings, so a rebase must choose one text per document: `main`'s, which drops the claims
(re-inserting them afterwards is exactly the post-hoc injection this document argues
against), or the branch's, whose prose still argues the drug-substance acceptance basis that
`083bfb1` replaced with per-step in-process limits — a contradiction between prose and
regenerated tables that no gate here detects. Integration therefore means re-authoring three
documents with their claims assigned in the brief. See the branch note in `README.md`.

**And verify the rebase itself; do not trust it.** Reverting the merge left `a0b1f66` an
ancestor of `main` whose content `main` no longer has, so replaying the branch on top
resolves hunk by hunk against reverted text. `git rebase main -X theirs` was tried on
2026-08-02 and silently produced a broken branch: pre-revert prose spliced into `PCR-003`
and `PCR-009`, and 149 lines of branch work dropped from `build_ground_truth.py`. The annex
still built and still validated. It only surfaced because the splice referenced a variable
that exists in neither version and the render crashed. After any rebase of that branch,
diff every branch-owned source file against the previous tip and expect zero drift; only
files `main` legitimately changed may differ.

The rest of this file is the failure analysis that produced that design. It is worth reading
before adding any labelled negative to a corpus, because the mistake was not obvious and no
gate caught it.

## What the feature was

The corpus's default invariant is that **every claim is grounded** (CLAUDE.md golden rule 3,
WRITING_GUIDE §3, and REVIEW_CHECKLIST.md). This feature was the controlled exception: a few fluent, in-register
but unsupported or overstated claims would be planted into a report and **labeled**, so the
benchmark carried negative examples for evidence-grounding tasks — claim verification,
overstatement detection, "does the cited evidence actually support this sentence?".

The motivation is still sound. A grounded corpus teaches a model what supported prose looks
like, but not how to catch the failure it most needs to catch: a claim that *reads*
authoritative and on-register yet is not backed by the data or a citation. Real regulatory
documents contain exactly these.

## Why it was retired

The claims were **planted after authoring**, as a maintainer step. The author is required to
ground everything (WRITING_GUIDE §3; CLAUDE.md, nothing is added after authoring), so a labeled negative could not come from the author
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

## What replaced it

The fix is the sequencing, and it lives on `feature/weak-claims-via-brief`:

1. The claim is **assigned before the document is written** — `weak_claims.yaml` records
   which fact it distorts, what to assert instead, and where to place it.
2. `build_brief.py` renders that assignment into the author's brief as §5b, so the single
   author sees it before writing and builds the surrounding argument around it.
3. The wording is **captured afterwards** by reading the rendered document. That step is
   post-hoc, but it *reads* the document; it never edits it. That distinction is the whole
   difference from the retired approach.

Two rules the branch learned the hard way. A claim must be **unsupported, not contradicted**
— if a neighbouring sentence rebuts it, move the claim. And **move the claim, never the
document**: an author asked to write an unsupported claim will feel the pull to soften
sentences elsewhere to accommodate it, which converts a local planted negative into a diffuse
weakening that nothing records.

A separate option remains open: treat contradiction as its own labelled category (a
`contradicted_by_document` weakness type) rather than as a defect to avoid. That is a
benchmark design decision, not a mechanical one, and it has not been made.

## State of the machinery on this branch

- `authoring/weak_claims.yaml` — the three retired PCR-003 entries, kept as a record. Their
  wording is not in any document, and that is correct.
- `pc_package/build_ground_truth.py` `build_weak_claims()` — skips a registered claim whose
  quote is absent and prints a note, so "no planted claims" is a clean, buildable state
  rather than a guaranteed grounding failure.
- `authoring/build_rhetorical_annex.py` — skips them for the same reason. It used to emit
  them anyway, producing a layer with three spans whose text was nowhere in the document.
- `authoring/build_weak_claims_annex.py` — the standalone strict check. It hard-fails here,
  because the claims are not in the document. That failure is correct.
