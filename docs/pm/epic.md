---
type: pm-epic
sprint: 2026-08-17_01_register-second-round
status: planned
started: 2026-08-17
proposal: docs/next/register-from-four-sources.md
tags: [pm/epic]
---

# Epic — the second two-document round: give the author the number

Board: [[_Board]] · proposal:
[`docs/next/register-from-four-sources.md`](../next/register-from-four-sources.md), Track 1 ·
exploration: `.claude/work/2026-08-17_01_register-second-round/exploration.md` · plan:
`.claude/work/2026-08-17_01_register-second-round/implementation-plan.md` · round one:
[`docs/results/2026-08-17-register-pilot.md`](../results/2026-08-17-register-pilot.md)

**Why it opened.** The previous epic re-authored `PCP-003` and `PCR-003` from an amended guide and
got one clean win in five. Then the project owner read the new `PCR-003`: better than before, and
still immediately recognisable as machine-written. Two sentences were quoted. One packs a premise,
a consequence and a recommendation into a single sentence with `, so … , and …` — "a classical
case for Therefore, However, As a consequence". The other counts "the four that matter" without
naming them.

**The count agrees with the reader.** Over the same prose the gate reads, mid-sentence `, so `
occurs in **6–11 % of corpus sentences against 0.1–0.4 % in all four human sources**;
sentence-initial connectives open **0–2 % of corpus sentences against 3.7–6.1 %**. Round one made
both worse (`PCR-003` 6.5 → 8.0 %, `PCP-003` 7.9 → 10.6 %). The corpus reasons inside the
sentence; the sources reason across sentences. This construction was not on the pilot's list, it
needs no parser to count, and it is a substitution — the kind of rule the pilot found authors can
execute.

**What this epic does.** Builds the feedback loop the pilot said was missing — the packing counts
printed by `check_style.py`, `check_discourse.py` for chaining/copula/front field behind an
optional spaCy extra, the guide's rule restated as a substitution, and a brief §5d that tells the
author where the last revision stood — then re-authors the same two documents one pass each,
re-anchors, and measures rounds zero, one and two by one method. The stopping rule is fixed in
advance; the owner reads the result and quotes what still gives it away.

**Decisions the owner took on 2026-08-17.** Clause packing displaces topic chaining as the target
(chaining and copula are no-regression conditions). The guide gets minimum edits; rewriting its
own commentary is a hypothesis for later. The discrimination test is dropped — "it is immediately
obvious that the text is AI generated" — and the owner's non-blind reading is the human check.

**What it will not do.** Add a gate; re-author any of the other eighteen; move a number; touch
weak claims; fix D-001 or D-002; patch a sentence in a committed document.
