# Content review of the PCP-006 draft — before promotion

**2026-08-20, TASK-021 §4.** Batch B3, authored under the amended rule 4. Low-pH viral
inactivation has a DoE, so this is a `plan` for a DoE step. §5c assigns **D-001**
(`protocol_method_statement`): the plan must commit the first PAR analysis to holding the other
parameters at their set-points. Two fresh judges (`opus`), the four Content questions verbatim,
the rendered PDF and nothing else, one return between them.

## Counts per question

| run | Q1 | Q2 | Q3 | Q4 | verdicts |
|---|---|---|---|---|---|
| 1 (as authored) | 7 | 2 | 3 | 7 (+3 milder) | No · No · No · Yes |
| 2 (after one cycle) | 4 (+1 borderline) | 0 | 1 (+1 borderline) | 2 (+2 secondary) | No · **Yes** · No · Yes |

## Run 1

Q1: seven mechanism-claiming verbs with the cause deferred or absent, of which the clearest is
"The same conditions act on the antibody." Q2: "assurance margin" and, borderline, "mean-level
model". Q3: three scaffolding or anaphoric sentences. Q4: seven trailing category-filings plus
three milder.

**The judge scoped Q1 itself**, unprompted: "Many are procedural or design-rationale uses where no
physical cause is available or appropriate … Those name no physical cause but make no mechanism
claim; I list them as a class rather than flagging each." It named the mechanism prose as "the
strongest writing in the document".

## Disposition after run 1

One return, the judge's scoping note passed through with the flags, replacement terms stripped.
The author rewrote each mechanism verb to carry species, rate and direction, replaced "assurance
margin" with "a safety factor", deleted the scaffolding sentences, and removed all ten filing
clauses while keeping the rules underneath them.

## Run 2

Q2 now passes outright. Q1's residue is four verbs carrying magnitude, plausibility or a design
fact instead of a direction; Q3's is one "is mechanistically plausible" sentence.

## Two findings, neither acted on

**The Tool #1 definition the author added is contradicted by its own table.** Run 1 observed that
the column was undefined; the author defined it and wrote "so a higher score is a higher
criticality". Run 2 caught the contradiction: the register has viral clearance at **VH with a
score of 20** and galactosylation at **H with 48**, so criticality does not follow from the score.
Verified against `cqa_register.csv`. The arithmetic (`impact × uncertainty`) is right; the
inference is wrong. The same false inference appears in `PCP-004` and `PCP-010`, written
independently by two other authors given the same observation — see
`content-review-PCP-010.md`.

**D-001 is intact** and unreconciled, verified in the rendered PDF after the revision.
