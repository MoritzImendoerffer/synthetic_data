# The corpus states facts. It does not argue.

**Status:** proposed 2026-08-16. **In progress in work unit
`2026-08-16_01_register-from-four-sources`.** **Rewritten 2026-08-16 after exploration**: the first
version treated this as a sentence-statistics problem to be fixed by recalibrating thresholds. It
is a discourse problem, and the guide's own rules are part of the cause. The measurements behind
every number here are in that unit's `syntax-analysis.md`, `rhetoric-comparison.md` and
`mined-patterns.md`.

Raised by the project owner: "currently, the prose is written in a way no SME would write", and on
one passage, "hard to read, nearly not understandable, makes vague statements formulated not like a
scientific text is formulated".

## The problem

Every document passes all thirteen register thresholds. The prose still reads as machine-written,
and the reason is that **the gate measures ornament while the defect is in how claims connect.**

Five measurements, corpus against the two human sources:

| Measure | A-Mab | PDA TR 60 | PCR-003 |
|---|---|---|---|
| % of sentences whose subject continues the previous sentence | 57.0 | 59.6 | **35.1** |
| `However` / `For example`, whole document | 46 / 12 | 21 / 22 | **0 / 0** |
| % of sentences shaped "X is \<noun phrase\>" | 14.7 | 18.2 | **33.3** |
| `its` per 1000 words | 0.28 | — | **6.67** |
| % of clauses opening with an adjunct | 29.5 | 25.4 | **13.6** |

Zero `However` and zero `For example` across roughly 30,000 words of four documents. The entire
connective repertoire is `therefore`. Two thirds of sentences start a fresh topic. A third contain
no event, because their main verb is `be` and the meaning sits in abstract nouns on stacked
prepositions.

One sentence carries four of the five:

> "These are large and well-resolved effects of limited practical consequence, because the
> attribute is of very low criticality and its acceptance criterion is applied as an upper limit
> that lies far above the observed range."

A-Mab makes the identical argument and hands the reader the number that settles it:

> "For example, it is seen that medium concentration had a statistically significant effect on
> aFucosylation (p = 0.001). However, by reviewing Figure 3.4 it is seen that its effect was very
> shallow. In this case, changing the medium concentration from 0.8 to 1.6 X only changed the
> aFucosylation levels by 0.3 %."

## What the problem is not

Eight hypotheses were tested with a dependency parse and returned null. Each would have produced a
rule that changed nothing or made things worse:

sentence length and complexity (the corpus is **simpler** than the sources on tree depth, PP
nesting and compounding) · word order (subject-before-verb in 100 % of A-Mab clauses, 99.7 % of
PCR-003's; zero fronted objects anywhere) · nominalisation (the corpus does it **half** as often as
the sources) · formulaic repetition (fewer repeated 4-grams than A-Mab) · over-claiming (fewer
boosters than both sources) · list-like coordination (identical) · number density · punctuation
ornament.

**So no threshold of the kind `check_style.py` already has will reach this**, and adding one is the
failure mode this repository has already paid for: when a one-sided sentence-length cap was added,
the next generation came back at a 17-word mean with 41 % of sentences under 15 words. The metric
moved and the prose got worse.

## The cause, and it is in the repository

- ~~**`WRITING_GUIDE.md` §2c and §2d forbid the shapes that carry an argument.** "One paragraph, one
  point." "One sentence, one point; if a sentence carries two claims, make it two sentences." A
  concession is a claim plus its counter-consideration. An instance is a rule plus an example. Both
  are two points. **The authors complied exactly.**~~ Amended on 2026-08-16 (TASK-003). Both
  sections keep one point per unit as the default and now name one licensed exception, with four
  shapes, seven verbatim source examples and a worked correction each. The 20 documents already
  written are unaffected until they are re-authored.
- ~~**`check_style.py` caps `therefore`** at 1.2 per 1000 words — the one connective still in
  use — and says nothing about the eight the guide itself recommends.~~ Done on 2026-08-16
  (TASK-002). The cap is gone and the nine connectives are counted as a diagnostic that fails
  nothing. The measurement it now prints: the 20 documents run a median 1.5 per 1000 words using
  3 of the 9, against 2.2–2.7 and 6–9 for the four sources.
- ~~**§2d already states the topic-chaining rule** and it is met a third of the time. This one
  needs exemplifying and checking, not inventing.~~ Exemplified on 2026-08-17 (TASK-005). §2d
  carries three worked corrections from `PCR-004`, `PCMR-001` and `PCP-004`, a new §2d bis states
  the possessive rule with its measured table, and the exemplar gained section 23. Re-measured
  over all four sources and all 20 documents: sources chain 57.0 to 61.9 %, the corpus a median
  36.3 %. **Not checked** — no gate was added, per the proposal's own "diagnosis, never a target".
- ~~**`REGISTER_EXEMPLAR.md` contains no plan-genre passage**, and 10 of 20 documents are
  plans.~~ Done on 2026-08-17 (TASK-004). Part 3 of the exemplar carries a seven-pattern
  argument-moves catalogue, 32 new quotes taking the file from 88 to 120, drawn from all four
  sources. ISPE Technology Transfer supplies 9 of them, including 3 of the 5 modality passages.
- ~~**Two of the four published sources have never been extracted.**~~ Done on 2026-08-16
  (TASK-001). `scripts/extract_sources.py` carries all four, and `refs/text/` holds `ispe_tt.txt`
  and `ispe_pv.txt`. The ISPE Technology Transfer guide is the only plan-shaped source available
  and `PTP-001` is a technology transfer plan, so it is still the one that matters here.

## The idea

Give the author the shapes, taken verbatim from human prose, and remove the rules that forbid them.
Then re-author one document and look at it.

1. **Amend §2c and §2d** so a paragraph may carry a claim together with its counter-consideration,
   and name the shapes: rule → instance → counter-move → quantified resolution; concession before
   commitment; finding with its limit in the same sentence. One point per paragraph stays the
   default and the tension pair becomes the licensed exception, narrowly, because the opposite
   failure is the 34-word sprawl of the first-pass corpus.
2. **Add a moves catalogue to `REGISTER_EXEMPLAR.md`**, seven patterns with three to five verbatim
   examples each, already mined and verified against `refs/text/`. The exemplar is arranged by "the
   job each passage does"; these are jobs it does not yet cover.
3. **Exemplify the given-new rule** §2d already states, which is the cheapest item here.
4. **Drop the `therefore` ceiling** or pair it with the other eight connectives.
5. **Extract the remaining two sources** and build the plan-genre exemplar, subject to the
   licensing question below.
6. **Pilot on PCP-003 and PCR-003** — one plan, one report — then measure and read the result.
   Widened from one document to two on 2026-08-17 at the project owner's request: they proposed
   re-authoring all twenty at once, and the agreed middle is a pilot that exercises both genres
   and both registered discrepancies before the campaign is committed to.
7. **Decide the remaining eighteen on the pilot**, not in advance. The corpus is 119,453 words of
   prose and 2084 grounded annex quotes; re-authoring all of it is a campaign, and the amended
   artifacts have not yet produced a single paragraph.

## Verification

- Both pilot documents' shapes move toward the sources on all five measures, each reported with
  its denominator, before and after. A result that holds in one genre and not the other is the
  most useful thing this pilot can produce.
- **The acceptance test is discrimination, not counts**: can a reader tell the re-authored passage
  from a source passage? A connective count is a diagnosis and would be gamed as a target.
- `check_exemplar_quotes.py` passes on every added exemplar quote. One of 25 mined quotes already
  failed this because it spanned a page break, so the check is not a formality.
- `check_render.py --render` on the pilot, then rebuild the annex and re-ground. The corpus is at
  2,084 quotes across 20 annexes and a re-author invalidates those over the changed text.

## What this deliberately does not do

It does not add a syntactic gate. spaCy is not a project dependency, and the analyses were run
through `uv run --with spacy`. The findings stay diagnostic unless a later decision says otherwise.

It does not patch paragraphs, it does not change what any document claims, and it does not touch
D-001 or D-002 — see the open question below.

It does not import the sibling repository's writing standard wholesale. Two of its rules — "if a
sentence needs a semicolon, make it two sentences" and "should read like a checklist, not an essay"
— point at the floor this corpus is already stuck at. That guide governs engineers writing
repository documents; this corpus imitates an SME writing for an assessor.

## Open questions

1. **Blocking. May ISPE passages be quoted into `REGISTER_EXEMPLAR.md`?** Both guides are
   watermarked "for personal use only". Reading them to derive numbers is unencumbered; quoting
   them into a committed file is not, and `--selftest` reads `refs/text/`, which is committed. The
   plan-genre exemplar is exactly the blocked act. Fallback: build it from PDA TR 60's protocol
   sections, which are thinner.
2. ~~**Blocking. Does D-002 get a carrier, or does PCR-003 stay out of scope?**~~ **Answered by
   building the carrier**, 2026-08-17 (TASK-006). `authoring/discrepancies.yaml` is now on `main`
   with the discrepancy half only, and `build_brief.py` emits §5c for all 20 documents — eight
   with an assignment, twelve empty. The brief quotes the registered sentence verbatim, so an
   author cannot paraphrase D-002 into a qualified version that would be true. Nothing about the
   weak-claims layer came across; `weak_claims` is still empty in 20/20 annexes.
3. Which source is the reference for which document type? PDA hedges at 24.5 per 1000 words because
   it is guidance. A-Mab sits at 6.6 and is the closer genre for a report.
