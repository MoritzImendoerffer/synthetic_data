# Content review of the PCP-004 draft — before promotion

**2026-08-20, TASK-020 §4.** Batch B3, authored under the amended rule 4. Harvest has **no DoE**,
so this is one of the two non-DoE documents in the batch and a direct test of whether the weakness
the owner found in `PCR-004`'s §6 is structural. §5c assigns no registered discrepancy. Two fresh
judges (`opus`), one return between them.

## Counts per question

| run | Q1 | Q2 | Q3 | Q4 | verdicts |
|---|---|---|---|---|---|
| 1 (as authored) | 7 | 3 (+1 borderline) | 6 | 10 | No · No · No · Yes |
| 2 (after one cycle) | 2 (+1 borderline) | 1 (+1 borderline) | 0 | 2 (+2 borderline) | No · No · **Yes** · Yes |

Q3 passes after one cycle. Run 2 stress-tested the two weakest mechanism sentences and let both
stand: "I stress-tested the two weakest … Every sentence in §4.1, §4.2 ¶3, §4.3 ¶2, §5.1 ¶¶2 and 4,
and §5.2 ¶2 asserts something a reviewer could contradict with a fact."

**Run 2's judge scoped Q1 itself, and said why**: "Non-physical `because`/`since` clauses that
explain a *study-design* decision I treated as passing, since nothing is deferred — I note this
because a literal reading of Q1 would fail them all." That is the fifth judge of this batch to
supply the scope line the question lacks.

## What the return fixed

All seven Q1 verbs rewritten to carry the species and the direction where they stand — the
centrifuge sentence now gives sedimentation velocity proportional to field and density difference,
and residence time inversely proportional to feed rate. "lysis background", "parameter register"
and "the nephelometric value" removed. The six Q3 announcements and maxims deleted. All ten filing
sentences converted to the statement they were deferring.

It also fixed all three items the run-1 judge raised outside the questions:

- **The unsupported superlative is corrected.** §12 had said the host cell protein ELISA "is the
  least precise method in the set" while the table quotes only two of four methods. It now says
  "the less precise of the two methods quoted in the table", which is what the table shows. This is
  the same defect class as `PCR-005`'s, where the superlative was not merely unsupported but
  backwards.
- **"Tool #1" is defined** — but see the finding below.
- **Spelling unified** to the SOP registry's "disk-stack", from four body uses of "disc-stack".

## Two findings, neither acted on

**1. The Tool #1 gloss is false.** The author wrote "the criticality grade beside it is assigned
from that score". The register has viral clearance at **VH with a score of 20** against
galactosylation at **H with 48**, so the grade does not follow from the score. `PCP-006` and
`PCP-010` were given the same run-1 observation and wrote the same false inference independently.
Verified against `cqa_register.csv`; not listed in `docs/next/seeded-data-tensions.md`. See
`content-review-PCP-010.md` for why this argues for a helper-emitted definition.

**2. A document-internal factual conflict**, raised by run 2 outside the four questions: §5.4 says
the unclarified-culture reference sample "will be drawn from the harvest vessel immediately before
the feed to the centrifuge starts", but §4.1 defines the harvest vessel as what receives the
sterile-filtered filtrate, and §5.2 takes the culture from the bioreactor scale-down model.
Appendix B states it correctly, naming no vessel. Unregistered.

## The non-DoE question

`PCP-004` and `PCP-010` are the two non-DoE documents of B3, and neither behaves like `PCR-004`
did. Both converged, both now pass Q3, `PCP-010` passed Q2 on its first run, and `PCP-004`'s run-2
Q1 residue is two clauses. On the review's measures the non-DoE **plans** are among the cleanest
documents of the campaign. That does not settle the owner's `PCR-004` finding — a plan does not
have to explain the absence of a design space in the way a report does — but it does mean the
weakness is not simply "non-DoE steps write badly".
