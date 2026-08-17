# The weak-claims branch: carry it forward, or let it go

**Status:** proposed 2026-08-16. Parked by the project owner on 2026-08-16 (`97f94fc`). No work
unit. **This proposal decides nothing on its own** — it separates what is settled from what is
still open, so the next person does not reach for `git` first.

## What is settled

**Labeled weak claims are a benchmark item worth having.** A corpus where every claim is grounded
cannot score a system that is supposed to find unsupported ones.

**They are assigned in the brief, before the document is authored.** The first version planted
them into a finished report afterwards, and when the reports were re-authored two of the three
PCR-003 claims stopped being unsupported and became flat contradictions of nearby sentences,
because the new report settles the questions they overreach on. That converts the benchmark task
from evidence grounding to contradiction detection, and every gate passes it — including the
register gate, since the claims sat at the 46th–68th percentile of the document's own
sentence-length distribution with no style markers at all. The general rule that came out of it is
in `CLAUDE.md`: **nothing is added to a document after authoring.** Full reasoning:
`authoring/WEAK_CLAIMS.md`.

**`main` stays fully grounded.** `weak_claims` is empty in all 20 annexes, without exception.
Nothing in a document reveals that four of its sentences are deliberately unsupported, so a leak is
silent — which is why PR #6, which merged the branch on 2026-07-28 against the instruction in its
own commit message, had to be reverted.

**The direction is fixed.** `main` is carried onto `feature/weak-claims-via-brief` by **rebasing**.
The branch is never merged back.

## What is open

The rebase is parked, and the reason is not laziness. Measured on 2026-08-16:
`feature/weak-claims-via-brief` is **1 commit ahead of `main` and 4 behind**. Both sides have
re-authored the same documents since the merge base. Eleven `.qmd` differ on both sides, the three
carrying the claims differ by around 3,000 lines, and no sentence of the four registered claims
appears anywhere in `main`.

**Two one-pass authorings of one document do not merge hunk by hunk.** A rebase has to pick a text
per document, and both picks lose something real:

| Pick | What it costs |
|---|---|
| `main`'s documents | the claims are gone, and re-inserting them afterwards is exactly the post-hoc injection the feature was rebuilt to avoid |
| the branch's documents | they still argue the drug-substance acceptance basis that `083bfb1` replaced with per-step in-process limits, so the prose would contradict its own regenerated tables, with no gate to catch it |

So the honest options are:

1. **Re-author the three documents on the branch**, with the four claims named in each brief, from
   the current `main` model. That is the only path that respects both rules at once. It costs three
   one-pass authorings plus their annexes and re-grounding.
2. **Let the branch go**, keep it as a record, and treat labeled weak claims as a thing this corpus
   does not carry until someone wants the benchmark item enough to pay for option 1.
3. **Keep it parked**, which is the state today, and accept that it drifts further behind `main`
   with every corpus change.

## Verification, whichever way it goes

- `git log --oneline main..feature/weak-claims-via-brief` and the reverse, quoted with the counts,
  in whatever result page records the decision.
- On the branch after any authoring: the full gate set, plus `weak_claims` populated in exactly the
  annexes that should carry it.
- On `main`, unchanged and forever: `weak_claims` empty in 20 of 20 annexes.

## What this deliberately does not do

It does not propose a merge, a cherry-pick or a "just take the three files". `README.md` and
`WEAK_CLAIMS.md` both carry the never-merge rule next to the rebase procedure, and this file exists
so the reasoning is found before the command.

## Open question

Is the weak-claims benchmark item still wanted? Everything above assumes yes. If the answer is no,
option 2 is a five-minute job and this proposal is deleted.
