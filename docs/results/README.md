# docs/results — what a run measured, dated

One file per measurement, named `YYYY-MM-DD-<slug>.md`. A number that matters lives here with the
command that produced it, never in a commit message and never only in a chat.

**A results page survives the work unit.** `.claude/work/<id>/` is scratch space for one
implementation attempt and `docs/next/<name>.md` is deleted when the work lands. What the run
measured is the part that has to outlive both, because the next person's question is almost always
"what was it before?".

## What a page contains

| Section | Why |
|---|---|
| **Why the run happened** | the defect or the question, with the state before it |
| **What changed** | the before/after table, with denominators on every rate |
| **What was found on the way** | the landmines. This is usually the most reused part of the page |
| **Verification** | the exact commands and their output, so anyone can re-run them |
| **Files** | what the work touched |

**Every rate carries its denominator.** "2084/2084 quotes grounded across 20 annexes", never
"grounding passes". A bare percentage hides which run produced it, and this repository's gates all
print counts for that reason.

**Re-verify before you quote an old page.** A figure here was true when the run happened. The
annex-anchor page below was re-checked on 2026-08-16 and its figures still hold; say so, with the
date, whenever you lean on one.

## The pages

| Page | What it measured |
|---|---|
| [2026-08-03-annex-anchors.md](2026-08-03-annex-anchors.md) | row anchors 285 → 653, annexes with ≤1 row anchor 14 → 0, gated spans 1476 → 2084, and the two-tier reuse rule |
| [2026-08-17-register-pilot.md](2026-08-17-register-pilot.md) | whether the amended writing guide changes what an author writes. `PCP-003` and `PCR-003` re-authored and measured on five shapes against four human sources: **one clean win** (connective repertoire 3/9 → 6/9 distinct in both genres), one result withdrawn on a reader's judgement (possessives — a ratio artefact that cost 23 added copulas in the plan), and three that did not move, two of them backwards. Run because the owner said the prose "is written in a way no SME would write" and six tasks had changed the guide, the exemplar, the gate and the brief without a single paragraph having been written from them |
