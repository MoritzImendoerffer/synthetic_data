# Content review of the PCP-010 draft — before promotion

**2026-08-20, TASK-024 §4.** Batch B3, authored under the amended rule 4. UF/DF has **no DoE**, so
this is one of the two non-DoE documents in the batch and a direct test of whether the weakness the
owner found in `PCR-004`'s §6 is structural. §5c assigns no registered discrepancy. Two fresh
judges (`opus`), one return between them.

## Counts per question

| run | Q1 | Q2 | Q3 | Q4 | verdicts |
|---|---|---|---|---|---|
| 1 (as authored) | 10 | 0 | 4 | 12 | No · **Yes** · No · Yes |
| 2 (after one cycle) | 3 (1 clear, 1 judgement, 1 borderline) | 0 | 0 (1 noted) | 2 | No · **Yes** · **Yes** · Yes |

Q2 passed on the **first** run, which no report managed, and Q3 passes after one cycle. On the
review's own measures the non-DoE plan is among the cleanest documents of the campaign.

## What the return fixed

The three "acts on" mappings became directional claims; the circular "since" in §12 was split; the
administrative "the ranking set the study type" became a decision in the passive. **A physics
error was corrected**: the draft had transmembrane pressure "thickening" the polarisation layer,
which is the wrong mechanism. It now reads "Higher transmembrane pressure raises the permeate flux
until the polarisation layer limits it, and beyond that point it raises the antibody concentration
at the membrane wall", with crossflow named separately as what sweeps antibody off the wall. That
correction was passed to the author despite the no-phrase-to-insert rule, because it is a
correctness matter rather than a style preference.

## Two findings, neither acted on

**1. The revision introduced a contradiction.** Run 1 flagged a charge-variant clause for naming no
chemistry. The author fixed it well — run 2 held the result up as its model of a passing sentence:

> "They are measured because deamidation of asparagine residues continues while the antibody is
> held in the formulation buffer, and the rate of deamidation rises with pH and with the length of
> the hold."

But the document also says, twice and absolutely, "What the step can do to the product is
mechanical." and "Neither attribute is formed at this step." A reaction that continues during the
step **does** form acidic charge variants at the step. Naming the cause is what exposed the
absolute claim, which is the same mechanism that caught five factual errors earlier in this
campaign — except here the error was created by the fix.

This is an **unregistered** inconsistency, which CLAUDE.md says is a bug to fix or to register
deliberately, and it collides with `AUTHOR-A-DOCUMENT.md` §4's one-cycle rule. Put to the owner;
not acted on.

**2. The Tool #1 gloss is false, in three documents at once.** Told the column was undefined, the
authors of `PCP-004`, `PCP-006` and `PCP-010` each defined it, and each asserted that criticality
follows from the score — "The criticality level follows from the score" here. The register has
viral clearance at **VH with a score of 20** against galactosylation at **H with 48**. Verified
against `cqa_register.csv`; not listed in `docs/next/seeded-data-tensions.md`.

Three authors, given the same true observation, produced the same false inference, because each
could see only its own document's slice of the register. That is the argument for emitting the
definition from `_pcpkg.py`, where all ten rows are assembled, rather than fixing it per document.
