# The corpus states facts. It does not argue. — what remains

**Status: two rounds delivered, target changed 2026-08-18.** Round one shipped in work unit
`2026-08-16_01_register-from-four-sources`; round two in `2026-08-17_01_register-second-round`.
Both are measured: [round one](../results/2026-08-17-register-pilot.md),
[round two](../results/2026-08-18-register-round-two.md). This proposal is rewritten down to what
is still open, because 18 of 20 documents have not been touched and the pair that has been touched
twice is still recognisable on its first sentence.

Raised by the project owner: "currently, the prose is written in a way no SME would write". Twice
since, on reading the re-authored pair: "hard to read, nearly not understandable"; and on
2026-08-18, **"yes, it is immediately clear. Already the first sentence gives it away."**

## Where this stands

Round two cleared every target it set and every line of a stopping rule fixed before it ran:
mid-sentence `, so ` 10.6 % and 8.0 % → **0.0 %** in both genres, sentence-initial connectives
1.8 % and 0.9 % → **4.9 % and 4.0 %**, topic chaining 34.4 % and 30.7 % → **46.0 % and 46.1 %**
although chaining was never set as a target, copula back inside the source band in both. Five of
five measures moved, against one of five in the pilot.

The owner then read the pair and named three faults, none of them measured. Counted afterwards:

| fault | sources | PCP-003 | PCR-003 |
|---|---|---|---|
| `, and ` joining a second clause | 1.1–3.4 % of sentences | 18.2 % | 22.6 % |
| `, not ` contrastive tail | 0.0–0.2 % | 0.0 % | **4.3 %** (was 0.0) |
| sentences carrying a passive | 54.3–59.8 % | 54.7 % | **34.4 %** |

**The finding that matters is not any one of those numbers.** Every measure printed back to the
author moved. The three faults the owner named are precisely the three that were **not** printed
back — and two of them are already forbidden, in words, by rules the guide states. So:

> An author executes exactly what is measured and printed back to it, and leaves everything else
> where it was, including rules it has read.

That is why this proposal is now about the measures rather than about the guide.

**Decision D1 was settled by the project owner on 2026-08-18: option B.** Track 2 — the remaining
eighteen documents — stays blocked. Committing eighteen one-pass re-authors and roughly 700
re-anchored annex spans to a register the owner still recognises on the first sentence buys
eighteen documents that need doing again.

## Track A — the three measures the reading named

Cheap: two regexes and one spaCy field. All advisory, for the reason this campaign has now proved
twice — a ceiling on `, so ` is met by writing `, and`, and a ceiling on `, and ` will be met by
writing a semicolon, so the family is printed together and nothing is gated.

1. **`, and ` joining a second clause**, beside the existing packing line in `check_style.py`. This
   is the round-two blind spot and it is a hole in the *measure*: the gate counts mid-sentence
   `, so ` and sentences carrying **two or more** coordinators, so a sentence with exactly one
   `, and ` joining two clauses falls between them. `WRITING_GUIDE.md` §2d already forbids it.
2. **`, not ` contrastive tail**, same line. `WRITING_GUIDE.md` §4b already says the sources
   "almost never build 'not X but Y'". Round two created 18 instances in `PCR-003` while that rule
   sat unenforced, which is the clearest evidence on the page that an unmeasured rule is not a rule.
3. **Passive rate**, in `check_discourse.py`, as a **band and never a floor**. `PCP-003` is inside
   the source band at 54.7 % and `PCR-003` is twenty points under it; a floor would push the plan
   the wrong way. This one needs the optional extra and stays advisory like the rest.

## Track B — the fault no measure reaches

"The 4 factors that **screening retained**" — screening is a study and retains nothing. The author
invented an agent because it was avoiding a passive, and no counter can see that. This is an
authoring rule and it belongs in `WRITING_GUIDE.md` beside the runtime-noun rule (§2d,
Correction 0): **where the sources would write a passive, write the passive.** Do not manufacture
an agent for a process, a study, a design or a model.

The measurable half is Track A item 3; this is the half that has to be taught.

## Track C — the guide's own register, now the leading hypothesis

Held back deliberately in round two (owner decision, minimum edits) and promoted here by round
two's own result. Measured 2026-08-17: `WRITING_GUIDE.md` commentary opens **0 %** of its sentences
with a connective and carries a mid-sentence `, so ` in 1.5 % of them; `REGISTER_EXEMPLAR.md`
commentary 0 % and 5.4 %; `STORY_BIBLE.md`, the briefs and `CLAUDE.md` all 0 %. An author reads
several hundred lines of that before writing a word.

Round two is the evidence that made this worth doing. It showed that an author executes what it is
shown *and measured on*; the guide is the largest single thing it is shown. Rewriting the guide's
commentary in the register the guide demands is a real task and a large one, and it is now the
first candidate rather than the last.

## Track D — the remaining eighteen (blocked)

Blocked on A, B and C by decision D1, option B. When it opens, the budget from two measured rounds:
**one one-pass re-author per document**, and **21–44 re-anchored annex quotes per document** rather
than the ~40 the pilot guessed — round two moved 21 of `PCP-003`'s 105 quotes and 23 of
`PCR-003`'s 177, from 37 edited builder strings, because every table-row quote survives a
re-author untouched. Add the curated rhetorical layer where a document has one: 33 of `PCR-003`'s
35 spans needed re-cutting. Each document needs `check_render.py --render` **and** an explicit PDF
render, because `check_render.py` glyph-checks whatever PDF is already on disk.

The corpus stays split 2-of-20 on register until this finishes, which is the argument for not
leaving A, B and C open for long.

## What this deliberately does not do

It does not gate any of the new measures. Every one of them is met by typing or avoiding a word,
and this campaign has now watched that happen twice: `, so ` driven to 0.0 %, below every source,
and possessives driven to zero in `PCP-003` — both overshoots of a rule stated as a substitution.

It does not touch what any document claims. Both registered discrepancies survived two re-authors
and were re-verified against the new text each time; `authoring/discrepancies.yaml` plus brief §5c
is what keeps them alive.

It does not reopen the discrimination test. Three rounds scored 64 of 64 and the owner has now read
the pair three times, so no blind test involving these documents can be valid. The human check
stays what it is: the owner reads and quotes what gives it away, and what they quote becomes the
next target.

## Open questions

1. **Do the three new measures go in one work unit with a third re-author of the same pair, or
   does Track C come first?** Round two's own lesson argues for measures first — the guide was
   amended in round one and the author still did only what was printed back. But a third re-author
   of `PCP-003`/`PCR-003` is the fourth measurement of two documents that no longer represent the
   corpus, and the pair's owner has read them three times.
2. **Is there a document other than the bioreactor pair to test on?** Every round so far has used
   the same two. A third round on, say, `PCR-005` would cost the same and would say whether the
   result generalises, at the price of losing the three-point comparison.
3. Which source is the reference for which document type? PDA hedges at 24.5 per 1000 words because
   it is guidance. A-Mab sits at 6.6 and is the closer genre for a report.
