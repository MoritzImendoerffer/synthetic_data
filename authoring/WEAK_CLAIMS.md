# Weak claims — labeled benchmark negatives, written in one pass

**Status: ACTIVE.** Four claims across three documents:

| id | document | type |
|---|---|---|
| WC-003-01 | PCR-003 (report) | `unsupported_prior_knowledge` |
| WC-003-02 | PCR-003 (report) | `overstated_outcome` |
| WC-009-01 | PCR-009 (report) | `unbounded_generalization` |
| WC-006-01 | PCP-006 (**plan**) | `missing_citation` |

The registry is `authoring/weak_claims.yaml`. Each claim is **assigned before the document is
written** and its wording **captured after**. Everything below explains why that order is the
whole design, because the obvious alternative was tried first and failed.

## This feature does not belong on `main`

> **Integration rule: `git rebase main` here. Never merge this branch into `main`.**
> This was violated once. PR #6 merged the branch into `main` on 2026-07-28, against the
> instruction in the merged commit's own message, and the four claims sat in the grounded
> corpus until the merge was reverted on 2026-08-02. Nothing in a rendered document reveals
> them, so no gate caught it. Check `main` is clean with:
>
> ```bash
> python3 -c "import json,glob; print(sum(len(json.load(open(f)).get('weak_claims') or []) for f in glob.glob('pc_package/ground_truth/*.json')))"
> ```

**Verify the rebase; do not trust it.** Because that merge was reverted, `a0b1f66` is an
ancestor of `main` whose content `main` no longer has, so replaying this branch on top
resolves hunk by hunk against reverted text. `git rebase main -X theirs` was tried on
2026-08-02 and silently produced a broken branch: it spliced pre-revert prose into
`PCR-003` and `PCR-009`, and dropped 149 lines of this branch's own work from
`build_ground_truth.py`, including the fix that anchors each PAR record on its own table
row. Nothing failed loudly — the annex still built and still validated. After any rebase,
diff every branch-owned source file against the previous branch tip and expect zero drift:

```bash
git diff --stat <previous-tip> HEAD -- 'pc_package/*.qmd' pc_package/_pcpkg.py \
    pc_package/doe_report.py pc_package/ra_content.py authoring/ scripts/ config/
```

Only files that `main` legitimately changed may differ. Everything else must be identical.

It lives on its own branch (`feature/weak-claims-via-brief`) and is **not merged into
`main`**. `main` stays a corpus in which every claim is grounded — that invariant is what
makes it usable as a positive-example set, and a reader or a downstream tool has no way to
know that four sentences in it are deliberately unsupported unless they read the annex.
Keeping the two apart makes the distinction a property of which branch you check out, rather
than a footnote someone has to notice.

So the branch is the deliverable. Rebase it onto `main` when `main` moves; do not merge it
back.

## What the feature is for

The corpus's default invariant is that **every claim is grounded** (CLAUDE.md golden rule 3,
WRITING_GUIDE §3/§6). This is the controlled exception: a few fluent, in-register but
unsupported or overstated claims, **labeled** in the annex, so the benchmark carries negative
examples for evidence-grounding tasks — claim verification, overstatement detection, "does
the cited evidence actually support this sentence?".

A grounded corpus teaches a model what supported prose looks like, but not how to catch the
failure it most needs to catch: a claim that *reads* authoritative and on-register yet is not
backed by the data or a citation. Real regulatory documents contain exactly these.

## The first attempt failed, and why

The claims were originally **planted after authoring**, as a maintainer step. The author is
required to ground everything, so a labeled negative could not come from the author — hence
the post-hoc injection. That sequencing is the flaw.

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

## Watch for the author smoothing the document around the claim

Observed on the first run of the revived design. The PCP-006 author placed WC-006-01
correctly, then also changed a sentence in a **different section** from "These samples
establish the shape of the inactivation curve" to "…confirm the shape…", and reported that
it did so to remove a sentence that "could have read as a rebuttal".

The wording was left as "confirm", because it is independently the better word — the story
bible has characterization *confirming and bounding* known platform mechanisms rather than
discovering them, so "establish" was the outlier. But the reasoning was wrong, and the edit
was not even necessary: the claim sits in §4.1 and the sentence it touched is in §5.4.

The lesson generalises. An author told to write an unsupported claim will feel the pull to
make the whole document hospitable to it, and will reach across sections to do so. That
converts a local planted negative into a diffuse weakening of the report, which is worse
than the original injection problem because it is invisible — nothing in the registry
records it and no gate sees it.

So the instruction to authors is specific, and both halves matter: **move the claim, never
the document.** If a neighbour rebuts the claim, relocate the claim. Do not soften the
neighbour, do not delete a grounded statement, do not remove a citation elsewhere to make
the uncited one blend. When reviewing an authored document, read the author's report for
any edit it made *in service of* the claim, and check that edit on its own merits.

## How to add a claim

1. **Assign it** in `authoring/weak_claims.yaml` under the target document, with an
   `assignment:` block giving the grounded fact it distorts, what to assert instead, and
   where to place it. Leave `captured.quote` as `null`.
2. **Regenerate the brief** (`build_brief.py <DOC>`). The assignment appears as §5b, so the
   author sees it before writing.
3. **Author the document in one pass**, as normal. `WRITING_GUIDE.md` §7a tells the author
   these are the only ungrounded claims permitted, and that a document whose brief has no
   §5b grounds everything.
4. **Capture the wording.** Read the rendered `.docx`, copy the author's sentence verbatim
   into `captured.quote`, and write the `rationale` and `correct_version`. This is the one
   post-hoc step and it **reads** the document — it never edits it.
5. **Rebuild.** `build_ground_truth.py` emits a `WeakClaim` with `support = "unsupported"`,
   so the span grounds while being labeled weak. `build_weak_claims_annex.py` is the
   standalone strict check.

The build distinguishes three states, so nothing degrades quietly. Assigned-but-uncaptured
prints a note (expected until the document is authored). A captured quote that no longer
appears **hard-fails** with instructions to re-read the document and re-record the wording —
never to edit the document to match. A document with no assignment simply has none.

## Review checklist

Read these against the rendered document, not the author's report:

- Does the quote ground verbatim?
- Read its neighbours. Is it **unsupported**, or does an adjacent sentence rebut it? If a
  neighbour rebuts it, the placement is wrong.
- Is it in register? Compare its length against the document's own distribution. A negative
  a reader spots by style tests nothing.
- Did the author change anything *in service of* the claim? Its report should say so. Check
  that edit on its own merits — see the section above.
- Does any *normal* grounded assertion or `claim` span anchor on the same sentence? It must
  not; the sentence belongs to the `weak_claims` layer alone.

## An option not taken

Contradiction could be its own labeled category (a `contradicted_by_document` weakness type)
rather than a defect to avoid. That would make the retired approach useful again instead of
wrong. It is a benchmark design decision, not a mechanical one, and it has not been made —
`authoring/DISCREPANCIES.md` covers cross-document inconsistency separately and to different
ends.

## The machinery

- `authoring/weak_claims.yaml` — the registry, `assignment:` then `captured:` per claim.
- `authoring/build_brief.py` — `_weak_claim_assignments()` renders §5b into the brief.
- `pc_package/build_ground_truth.py` — `build_weak_claims()`, wired into **every** annex
  constructor. It was wired into only one for a long time, which meant assigning a claim to
  any other document would silently produce no annex record.
- `authoring/build_rhetorical_annex.py` — merges each captured claim as a `weak_claim` span.
  It reads the wording under either registry shape and skips a claim whose text is not in the
  document, so `main` (where the claims are retired) and this branch both build cleanly.
- `authoring/build_weak_claims_annex.py` — standalone strict verification.
