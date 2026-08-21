# Content review of the RA-001 draft — before promotion

**2026-08-21, TASK-035 §4.** Batch B5, authored under the amended rule 4. RA-001 is a corpus-level
document with no single unit operation, so its brief carries no §2b, and §5c assigns no registered
discrepancy. It is also one of the earlier-round documents being re-done so the corpus carries one
register. Fresh judges (`opus`), one return, plus one owner-precedent correctness pass.

## Counts per question

| run | Q1 | Q2 | Q3 | Q4 | verdicts |
|---|---|---|---|---|---|
| 1 (as authored) | 19 | 5 (+1 minor) | 4 (+1 weaker) | 7 (+2 borderline) | No · No · No · Yes |
| 2 (after one cycle) | 10 (+1 borderline, ~10 more ruled out of scope) | **0** | 8 | 6 (+2 borderline) | No · **Yes** · No · Yes |

Question 2 converged completely: the second judge found "no fabricated or coined technical
vocabulary" where the first had flagged five clear coinages. Question 1 roughly halved. **Question 3
went the wrong way**, from 4 to 8, because the revision added signposts and meta-comments about the
assessment's own reasoning ("Both viral clearance attributes carry the top severity for a different
reason.", "Basal medium concentration is the one that needed argument."). Those are recorded and
left; the cycle is spent and the extra passes were authorised for correctness only.

## What the author got right against its reviewers

Three judgement calls from the return held up under the second judge, and all three are worth
keeping because in each the author declined to do what it was asked.

- **It refused to invent two directions.** Filtration pressure has no coefficient anywhere in the
  model, so the document says prior knowledge places neither the size nor the direction of a
  pressure effect, and gives that as the reason pressure goes into the design rather than a
  univariate study. Basal medium concentration keeps "statistically significant but shallow" with no
  direction, because the A-Mab source gives a magnitude and the config gives none.
- **It corrected the first judge, with a source.** Run 1 called "justified univariate" a category the
  document invents. It is A-Mab's own Table 5.16 rule, verified in `refs/grounding/amab_risk.json`
  ("8-16 multivariate or justified univariate"), and `ra_content.py` emits `univariate (justified)`
  into the study-type column. The prose now uses the register's form and cites the source.
- **It kept two flagged terms for the right reason.** `Elution stop collect` and `End of pool
  collect` are parameter names in `config/parameters.yaml`, rendered verbatim in three tables, so
  changing the prose alone would have put the document at odds with its own tables. It glossed them
  in place instead. Run 2 raised no question-2 flag on either.
- **It caught an error it had introduced itself**, before reporting: its first revision said titer
  rises with dissolved oxygen and inoculation density "because both raise the integral viable cell
  concentration", which the model does not do — DO acts on cell-specific productivity at fixed iVCC.

## THE REVISION INTRODUCED A DIRECTION THAT READS BACKWARDS

This is the second document in B5 whose review cycle introduced a physical error, after PTP-001's
two. The pattern is the finding, not the individual sentence.

The revision wrote:

> "A centrifugation speed below its range leaves more cells and cell debris in the centrate, because
> the settling velocity of a particle falls with the centrifugal field applied to it, and that
> debris then loads the depth filters."

"Settling velocity falls with the centrifugal field" reads in ordinary English as velocity
decreasing as the field increases, which is the reverse of the truth. The intended reading is
recoverable only from the first clause. Checked against the pre-review draft: not present there, so
the cycle introduced it.

A second sentence claimed culture extension raises host cell protein, DNA **and aggregate** "because
lysing cells release intracellular protein and DNA into the broth" — a because-clause covering two
of the three things claimed. The aggregate claim itself is grounded, `aggregates_hmw` carrying a
duration coefficient of +0.3, so what was missing was its cause and not its warrant.

**Both were fixed under the precedent the owner set for PTP-001**: correctness only, those sentences
only, nothing from questions 3 or 4 reworked. The results:

> "A centrifugation speed below its range leaves more cells and cell debris in the centrate. A
> particle settles faster the stronger the centrifugal field acting on it, so a lower speed settles
> less of the fine debris in the time the material spends in the bowl, and what stays in the
> centrate then loads the depth filters."

> "Extending the culture, or harvesting it after viability has fallen, raises host cell protein and
> DNA in the harvest, because lysing cells release intracellular protein and DNA into the broth.
> Aggregate rises with culture duration as well. Antibody secreted early in the run stays in the
> vessel at culture temperature until harvest, and aggregate accumulates over that time."

The first cannot now be read in the wrong direction. The second gives aggregate a residence-time
cause consistent with a positive duration coefficient and asserts no chemistry the model does not
carry.

## Findings recorded, not acted on

- Eight question-3 sentences survive, up from four, all signposts or meta-comments on the
  assessment's own reasoning.
- Six question-4 sentences survive.
- "polarized layer" as a compression of the concentration polarization layer, and "moves the
  mannosidases and the galactosyltransferase away from the acidic conditions at which they work
  fastest" as loose for a shift in compartment pH relative to the enzymes' optima. The judge called
  neither a coinage and question 2 passed.
- `build_brief.py` does not surface `pc_package/ra_content.py`, although `section_plan.yaml` names it
  as the content source for this document class. The author found it anyway. Worth adding to the
  brief builder so the next author does not have to.
- A `show()` trap the author hit and worked around: `df.to_markdown` lets tabulate re-parse
  numeric-looking strings, so pre-formatting a mixed-magnitude column to strings does not help and a
  set-point column with pH 6.85 beside 9000 g rendered as `9e+03`. Fixed here with
  `show(..., floatfmt="g")`. Any future corpus-wide parameter table hits the same thing.
- No parameter in the content source is scored against leached Protein A although the CQA register
  sets it at the capture step. The document says so and attributes the control to resin life cycle
  and sanitization plus downstream clearance. Explained in the text rather than registered as a
  discrepancy.

## Disposition

Two review runs plus one correctness pass under the PTP-001 precedent. One of the four questions
passes. The document proceeds to the batch B5 annex task. Nothing is added to it after this point.
