---
type: pm-epic
sprint: 2026-08-18_01_register-third-round
status: shipped
started: 2026-08-18
proposal: docs/next/register-from-four-sources.md
tags: [pm/epic]
---

# Epic — round three: measure what the reader named, on PCR-003

> **Shipped 2026-08-18.** All three newly printed measures moved and all eight lines of the
> stopping rule hold: `, and ` + clause 22.6 → **0.5 %**, `, not ` 4.3 → **0.0 %**, passive
> 35.4 → **57.4 %** and inside the source range for the first time in the series. The corpus is
> at 2084/2084 quotes grounded across 20 annexes with strict anchors and 0 weak anchors, and a
> full `make clean && make data figures corpus` reproduces every document's rendered text
> byte-identically with `outputs/` unchanged. **The owner's reading names no sentence for the
> first time** — "The document reads better. Not perfect but ok to me." — which closes Track A
> and Track B and settles D2. What did **not** ship: `PCP-003` was held at round two as the
> control, so every move above is a move *in the report*, and the both-genres check is still
> owed. Measurements:
> [`docs/results/2026-08-18-register-round-three.md`](../results/2026-08-18-register-round-three.md).
> What remains: [`docs/next/register-from-four-sources.md`](../next/register-from-four-sources.md)
> — Track C, Track D, and two count-led candidates the reading could not see.

Board: [[_Board]] · proposal:
[`docs/next/register-from-four-sources.md`](../next/register-from-four-sources.md), Track A + B ·
exploration: `.claude/work/2026-08-18_01_register-third-round/exploration.md` · plan:
`.claude/work/2026-08-18_01_register-third-round/implementation-plan.md` · round two:
[`docs/results/2026-08-18-register-round-two.md`](../results/2026-08-18-register-round-two.md)

**Why it opened.** Round two cleared every target it set and every line of a stopping rule fixed in
advance — mid-sentence `, so ` to 0.0 % in both genres, sentence-initial connectives to 4.9 % and
4.0 %, topic chaining to 46 % without being asked for — and the project owner read the pair and
recognised it on the first sentence of the report. Three faults were named, none of them measured:
the balanced `, and ` two-clause sentence, a `, not ` contrastive tail, and passive avoidance that
manufactured a false agency ("the 4 factors that screening retained"). Counted afterwards, they run
at 22.6 %, 4.3 % and 34.4 % of the report's sentences against 1.1–3.4 %, 0.0–0.2 % and 54–60 % in
the four sources — and the first of them did not move in round two at all.

**The finding the epic is built on.** Every measure printed back to the author moved; the three
faults named are exactly the three that were not printed back, and two of them are forbidden in
words by rules the guide already states. An author executes exactly what is measured and printed
back to it, and leaves everything else where it was, including rules it has read. So this epic is
about the measures.

**What the owner settled.** Measures first (Track A before the guide's own register, Track C);
`PCR-003` alone, for a fourth point on the longest series in the corpus; Track B's rule — where the
sources would write a passive, write the passive — rides along as a guide edit. `PCP-003` is not
re-authored and is reported as the control column.

**Seven tasks.** Two regex counts into `check_style.py`, reproducing round two's never-saved table
first · passive rate and the parser's and-clause into `check_discourse.py`, one denominator, band
not floor · brief §5d and the guide's write-the-passive rule · one-pass re-author of `PCR-003` ·
promote, re-curate 35 spans under both extractors, re-ground · four points by one method with a
stopping rule fixed in advance and the owner's reading · the documentation move.

**What it will not do.** Gate any of the new measures. Touch the guide's own commentary. Re-author
`PCP-003`. Open the eighteen without the owner's reading saying the pair is no longer immediately
recognisable.
