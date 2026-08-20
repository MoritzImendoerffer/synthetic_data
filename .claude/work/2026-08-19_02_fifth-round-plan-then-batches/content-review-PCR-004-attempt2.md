# Content review of the PCR-004 draft, attempt 2 — before promotion

**2026-08-20, TASK-049 §4.** Second attempt at `PCR-004`, ordered by the owner after the B2
reading went to the pre-campaign text. **The regime is unchanged**: attempt 1 was already written
under the amended rule 4, so this tests the draw and nothing else. Harvest has no DoE
(`report_nondoe`); §5c assigns no registered discrepancy. Two fresh judges (`opus`), one return
between them, then one further correctness return authorised by the owner.

## Counts per question, both attempts

| | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| attempt 1, run 1 | 26 | 5 | 7 | 15 |
| attempt 1, run 2 | **4** | **0** | **0** | **8** |
| attempt 2, run 1 | 26 | 5 | 7 | 25 |
| attempt 2, run 2 | 5 (+7 methodological) | **7** | 6 | ~20 |

**Two things this says, and they point opposite ways.**

The two first runs are the same document twice. Two independent authors, fresh contexts, the same
brief and the same frozen regime produced **identical counts on Q1, Q2 and Q3** and a worse Q4.
That is not a draw; it is a property of harvest — a step that governs nothing, forms nothing and
clears nothing, whose prose has to keep explaining an absence. Run 1's judge named the mechanism
exactly: "The genuinely mechanistic sentences around them are strong and falsifiable, which makes
the empty ones stand out rather than blend in. **The failures are the connective tissue between
them.**"

The two second runs are not the same at all. Attempt 1 converged to 4/0/0/8 and attempt 2 did not
converge — Q2 went **up**, 5 to 7, and Q3 barely moved. So the *revision* is the high-variance
step, not the authoring. And the document the review scored best, attempt 1, is the one the owner
read against the pre-campaign text and rejected.

## What run 2 objects to, which is worth reading before the blind reading

Attempt 2's remaining Q2 flags are not coinages of the register kind. They are **plain-English
metaphors standing where a physical statement belongs**: "an effective parameter with a saturating
benefit and no observed penalty", "a gentle harvest … a harsh one", "That fraction is the depth
filter's job, not the centrifuge's", "the signature of a filter approaching the capacity of its
media rather than of a filter passing a constant fraction of what it sees", "The mechanistic
picture that emerges is a step operated comfortably inside two saturating effects".

Whether that reads as warmth or as looseness is exactly what a human reading decides and a count
cannot.

## The correctness return, and what it found

Authorised by the owner after run 1. Three items the run-1 judge raised outside the four
questions, plus one the author found itself:

- the doubled "as well as as" typo;
- "the more critical attribute of the three" → "most";
- **a numerical error**: a 25 % excursion against a 4.0 % method precision was called "an order of
  magnitude larger than the analytical variability". It is 6.25×. It is now a grounded scalar
  (`turb_exceed_pct / turb_rsd`) rendering as 6, and the one surviving "order of magnitude" is
  5 NTU against a 0.5 NTU limit of quantitation, which is exactly ten.
- **found by the author while fixing the grammar**: "host cell protein carries the highest Tool #1
  score" is false — aggregate 60, host cell protein 36, residual DNA 6. Verified against
  `cqa_register.csv`. Its own note on this is the sharpest statement of the gap the campaign found:
  "no gate would have caught it, since Tool #1 appears in the table but the comparison was mine."
  That sentence is the reason `docs/next/comparison-claims-unchecked.md` exists.

Spelling unified to "disk" throughout, matching the SOP-2005 title.

## Gates

Audit clean over all three turns; `suspect` and `other qmd` both empty. All hard gates pass on
every turn: chunks exec, inline expressions eval, no gated tic, no banned phrase, docx renders, no
missing glyphs, 0 `<<NEEDS>>`. **33 pages** after revision, against a measured non-DoE report band
of 26–28 — attempt 1 was 31. Two attempts running above the band is a question for the band, and
belongs at ship.

**Two rendering defects the author found by looking at rendered pages rather than extracted text**:
column collision in the parameter tables (en-dashes render wider than pandoc's width calculation
assumes, fixed with `tbl-colwidths`) and mass-balance values reparsed by tabulate into `6.56e+04`.
A corpus-wide check confirmed no shipped document renders a reparsed value. The collision cannot be
grepped at all — `pdftotext` reads a collided column perfectly happily — so nothing in the
verification chain gates layout.
