# The corpus states facts. It does not argue. — what remains

**Status: three rounds delivered; Track A and Track B are closed on the reading of 2026-08-18. Track D is being worked on since 2026-08-18 in work unit `2026-08-18_02_register-track-d`, on the project owner's instruction that all documents be re-authored.**
Round one shipped in work unit `2026-08-16_01_register-from-four-sources`, round two in
`2026-08-17_01_register-second-round`, round three in `2026-08-18_01_register-third-round`. All
three are measured: [round one](../results/2026-08-17-register-pilot.md),
[round two](../results/2026-08-18-register-round-two.md),
[round three](../results/2026-08-18-register-round-three.md). This proposal is rewritten down to
what is still open, because **18 of 20 documents have not been touched**.

Raised by the project owner: "currently, the prose is written in a way no SME would write". Then,
on reading the re-authored pair: "hard to read, nearly not understandable"; then on 2026-08-18,
"yes, it is immediately clear. Already the first sentence gives it away." And then, after round
three:

> The document reads better. Not perfect but ok to me.

## Where this stands

Round three printed the three measures the round-two reading had named, and all three moved, on
`PCR-003` with `PCP-003` held at round two as the control.

| measure | sources | r2 | **r3** |
|---|---|---|---|
| `, and ` joining a second clause (regex) | 1.1–3.4 % | 22.6 | **0.5** |
| `, and ` joining a second clause (parser) | 1.0–3.4 % | 25.4 | **0.7** |
| `, not ` contrastive tail | 0.0–0.2 % | 4.3 | **0.0** |
| sentences carrying a passive | 56.9–64.0 % | 35.4 | **57.4** |

Every line of a stopping rule fixed before the round ran holds, and the reading that follows names
no sentence for the first time in the series. **That closes Track A and Track B.**

Three rounds now say the same thing, and it is the finding this whole campaign has produced:

> An author executes exactly what is measured and printed back to it, and leaves everything else
> where it was, including rules it has read.

Round three is the third confirmation from both sides at once. The three measures newly printed all
moved. The two measures nobody printed — `, which` and `its` — both drifted away from the sources
in the same re-author. And copula and front field, which are printed as context without ever being
set as goals, both moved a long way in the right direction. Printing the number appears to be
enough; setting it as a target is not required; and stating it as a *substitution* is what produces
an overshoot, which has now happened three times out of three.

## Track C — the guide's own register, and it is worse than recorded

Still the leading hypothesis, and now the only one with a mechanism behind it. An author reads
several hundred lines of `WRITING_GUIDE.md`, `REGISTER_EXEMPLAR.md`, `STORY_BIBLE.md` and
`CLAUDE.md` before writing a word, and every one of them is written in the register the guide
forbids. Re-measured 2026-08-18, over commentary only, with blockquotes, code blocks, tables and
headings stripped:

| artifact | sentences | `, so ` | opens with a connective | `, and ` + clause |
|---|---|---|---|---|
| the four human sources | — | 0.1–0.4 % | 3.7–6.1 % | 1.1–3.4 % |
| `WRITING_GUIDE.md` | 318 | **3.77 %** | 0.31 % | **10.38 %** |
| `REGISTER_EXEMPLAR.md` | 147 | **6.80 %** | 0.00 % | **10.88 %** |
| `STORY_BIBLE.md` | 83 | 2.41 % | 0.00 % | 8.43 % |
| `CLAUDE.md` | 75 | **4.00 %** | 1.33 % | 9.33 % |

**Carry this measurement, not the earlier one.** An earlier version of this proposal quoted 1.5 %
`, so ` for the guide "measured 2026-08-17", by a method that was never saved to a file. The two
figures are not comparable and the older one cannot be reproduced. That is the same failure
TASK-001 of round three had to repair for the owner-reading counts, and the fix is the same: **the
first task of a Track C round writes the measurement as a script** before anything is rewritten.

Rewriting the commentary of four artifacts in the register they demand is a large task. It is worth
its size only because of the finding above: the guide is the largest single thing an author is
shown, and this campaign has three rounds of evidence that what an author is shown and measured on
is what it writes.

## Track D — the remaining eighteen

The corpus is split 2-of-20 on register, now at two different rounds: `PCR-003` at round three,
`PCP-003` at round two, and eighteen documents untouched.

The budget, from three measured rounds rather than a guess:

- **one one-pass re-author per document**, one agent, one context, no sibling `.qmd`;
- **21–44 re-anchored annex quotes per document** — round one moved 80 across the pair, round two
  44, round three 22 of `PCR-003`'s 177 alone. Every table-row quote survives a re-author
  untouched, because the row builders rebuild the row from the DataFrame the document renders;
  only prose moves;
- **the full curated rhetorical layer where a document has one.** Round two re-cut 33 of 35 spans,
  round three all 35. Assume all of them, and **test every span against both extractors before the
  builder runs** — `check_grounding.docx_text` yields `R2` and `build_rhetorical_annex.doc_text`
  yields `R²` from the same extraction, and that trap cost round two a cycle;
- **an explicit PDF render per document**, because `check_render.py` glyph-checks whatever PDF is
  already on disk;
- **a read of every annex report-summary statement**, not a substring hunt. Round three found two
  that asserted something the re-authored report no longer says. No gate catches that.

## The two count-led candidates

Round three's reading named nothing, so these came from asking what paid for its wins. They are
**weaker evidence than anything the campaign has acted on so far**, and the results page says so.

1. **`, which` — coordination became subordination.** 9.50 → **15.33 %** of sentences, against
   0.60–2.35 % in the sources, and 40 → 65 sentences carrying one. Visible inside the guide's own
   worked correction: the ✗ example it fixes for a false agent and a balanced `, and ` came back
   carrying a trailing `, which`.
2. **The staccato — a new measure.** Sentences inside a run of three or more consecutive sentences
   under fifteen words: **0.00 % at rounds one and two, 6.86 % at round three**, against 0.37–3.94 %
   in the sources. The sources all have such runs, so the shape is not the fault and the frequency
   is. "One argument step per sentence" executed to exhaustion.

Both are unprinted measures, which is exactly what the pattern predicts will drift. Neither was
visible to a reader.

## The open scope question

**Which comes next is the project owner's to set**, and the two options are not compatible in one
round:

- **Track C**, on the argument above — the guide is the largest thing an author reads and the
  mechanism is now measured; or
- **the both-genres check round three gave up.** `PCP-003` was held at round two deliberately, so
  every round-three move is a move *in the report*. Whether the three measures move a plan the way
  they moved a report is unknown. Round two could tell a property of the instruction from a
  property of one draft precisely because it ran both genres, and the plan-genre traps — the
  copula/expletive trade `PCP-003` fell into twice — are invisible in a report.

Track D follows whichever lands, and the count-led candidates ride along in the same re-author as
guide edits, since neither is worth a round of its own.

## What this deliberately does not do

It does not gate any of the new measures. Every one is met by typing or avoiding a word, and this
campaign has watched that happen three times out of three: `, so ` driven to 0.0 %, possessives
driven to zero in `PCP-003`, and now the and-clause driven below all four sources.

It does not touch what any document claims. Both registered discrepancies have survived every
re-author and were re-verified against the new text each time; D-002 came through round three
verbatim, so neither `discrepancies.yaml` nor `DISCREPANCIES.md` needed an edit.

It does not reopen the discrimination test. Four rounds scored 64 of 64 and the owner has now read
`PCR-003` four times, so no blind test involving these documents can be valid. The human check
stays what it is, and its limit is now on the record: the reading that stopped finding things is
the fourth reading by a reader who has watched the document improve three times.

## Open questions

1. Which source is the reference for which document type? PDA hedges at 24.5 per 1000 words because
   it is guidance. A-Mab sits at 6.6 and is the closer genre for a report.
2. Is "reads better, ok to me" a stopping point or a plateau? The count-led sweep says the document
   moved toward the sources on the three measures it was given and away from them on six others.
   A reading cannot see a rate, and a rate cannot see whether a document is worth reading.
