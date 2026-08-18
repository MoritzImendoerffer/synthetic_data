# Project owner's reading of the pilot — 2026-08-18

Recorded VERBATIM and before any measure was taken of what it names, which is the order the
three previous rounds used and the order `decisions.human_check` fixes for this one. The counts
that follow it were produced afterwards, by `measure_trackd.py`.

## The reading, verbatim

> "The interaction of the two is significant at -1,900, reproducing the sign and roughly the
> magnitude estimated in the screening stage. The quadratic term in elution pH is significant at
> 1,944 (p = 0.0040), which is the curvature a two-level design cannot see" ...which is the
> curvature a two level design cannot see... is there a way to stop you from writing these weird
> formulations?; "because a non-significant screening estimate makes no claim about the sign" ...
> why should a screening estimate make a claim about a sign? "The contours are curved instead of
> parallel, which is the interaction and the pH curvature already seen in Table 5.8." ... again.
> Maybe just ban ", which is"? also a weird formulation "The leached Protein A model is retained
> as knowledge-space evidence and is put to no other use in this report."

## Provenance of the four quotes

All four are `PCR-005`, the re-authored Protein A report. Quote 1 is quoted from the rendered
PDF, where the inline expressions resolve to `-1,900`, `1,944` and `p = 0.0040`; the other three
are verbatim in the `.qmd` as well. No quote is from `PCP-007` or `RA-001`, the other two pilot
documents, and none is from `PCR-003`, the control.

## What the reading names

Three of the four are one syntactic move and one is not.

1. `, which is the curvature a two-level design cannot see` — a trailing relative clause that
   renames the finding just stated as an abstract noun.
2. `, which is the interaction and the pH curvature already seen in Table 5.8` — the same move,
   plus a back-reference.
3. `because a non-significant screening estimate makes no claim about the sign` — not a relative
   clause. A causal gloss that answers an objection nobody raised. The owner's question, "why
   should a screening estimate make a claim about a sign", is the point: the sentence invents a
   reader who thought it did.
4. `is put to no other use in this report` — neither. A periphrastic negation where "and is not
   used again" would do.

What unites all four is not a construction. It is the sentence explaining itself: the finding is
stated and then, inside the same sentence, the reader is told how to file it. A regex reaches the
two commonest carriers of that move. It does not reach the move.

## Second part of the reading, same day

> "The surfaces in Figure 5.2 follow from the physical chemistry of affinity capture and confirm
> the expectations recorded in §2.1." you state that the surfaces are defined by the mechanism of
> affinity capture but you provide no reason or explanation of the shapes. "Elution buffer pH
> governs pool host cell protein because it sets the aggressiveness of desorption" aggresivenes is
> not a scientifc term (you are trained in scientific literature, why are you writing in such a
> strange way?)

Both quotes are `PCR-005` again, and both are **mechanism** sentences. This is a different fault
from the first four and it is not measurable the same way.

### What it counts out to

`aggressive` / `aggressiveness`: **0 occurrences in 3,338 sentences of the four published human
sources. 2 in the corpus, both in PCR-005.**

Hollow-warrant shapes, per 100 sentences, sources then the whole 20-document corpus:

| pattern | PDA | A-Mab | ISPE TT | ISPE PV | corpus |
|---|---|---|---|---|---|
| `follows from the …` | 0 | 0 | 0 | 0 | 0.23 (12) |
| `consistent with the …` | 0 | 0.19 | 0 | 0 | 0.15 (8) |
| `physical chemistry` | 0 | 0 | 0 | 0 | 0.02 (1) |
| `confirms the expectation…` | 0 | 0 | 0 | 0 | 0.02 (1) |
| `by the mechanism …` | 0 | 0 | 0 | 0 | 0.04 (2) |

These are **rare**. Twelve instances of `follows from the` across twenty documents is not a rate a
band can govern, and a ceiling of zero on five phrases would be routed around in one draft. The
first fault class is 15× over its source band and a counter can see it. This one is not.

### Why it is there — the specific gap

`section_plan.yaml` REQUIRES mechanism in at least four places: "State the MECHANISM the study",
a whole `Mechanistic interpretation` section, "state directions + mechanism".

Nothing supplies it.

- `REGISTER_EXEMPLAR.md` has fifteen numbered reporting moves — opening a unit operation,
  reporting a model, design space, capability, classification, deviations. **None of the fifteen is
  about explaining a mechanism.** The file teaches how to report; it never shows how to say why.
- The document brief runs §1 Identity, §2 Quality attributes, §3 Parameters, §4 DoE structure,
  §4b PARs, §5 Deviations, §5c discrepancies, §5d discourse targets, §6 Cross-references,
  §7 Helper inventory. **There is no mechanism section and no domain prose in it at all.**
- `STORY_BIBLE.md` §4 gives each step's ROLE in the train, not its physical chemistry.

So the author is instructed to write a mechanistic interpretation, is given no mechanism, and is
simultaneously optimising against seventeen surface counters (twelve gated, five advisory). What
satisfies every counter at zero content cost is a sentence shaped like an explanation:
`follow from the physical chemistry of affinity capture`, `because it sets the aggressiveness of
desorption`. Both pass every gate this repository has. Neither says anything.

That is the honest answer to "why are you writing in such a strange way".

## Third quote, same class — and the owner's doubt about it is unfounded

> "Protein load acts through the capacity of the bed: ..." maybe this sounds strange to me because
> I am not a native speaker but I have no idea what that means (I can imagine what you are trying
> to say but I doubth that scientific articles would use such a phrase)

It is not a non-native-speaker effect. The frame `X acts through/on Y` occurs:

**0 times in 3,338 sentences of the four published human sources. 63 times in the corpus**, across
`PCP-004`, `PCP-005`, `PCP-007`, `PCP-010`, `PCR-005`, `PCR-007`, `PCR-008` and `RA-001`.

The related abstract frame `governs`/`sets <noun>` runs 0.00–0.19 per 100 sentences in the sources
and 2.07 in the corpus.

So the reading is right and the count agrees with it: this is a house construction of the corpus,
not of the literature. `acts through the capacity of the bed` compresses a real mechanism — as the
load approaches the dynamic binding capacity of the resin, the mass transfer zone extends further
down the bed and weakly bound impurity is carried into the eluate rather than washed out — into
four words that state a category instead of a cause. The corpus does sometimes write the full
version: the very next clause of that sentence does. The frame is what precedes it.

## Summary of the reading — three fault classes

| class | example quoted | sources | corpus | counter can see it? |
|---|---|---|---|---|
| appositive gloss | `, which is the curvature a two-level design cannot see` | 0.6–2.4 / 100 sent. | 7.9–17.4 | yes, 15× over |
| mechanism frame | `acts through the capacity of the bed` | 0.00 | 1.21 (63) | yes, and the source count is zero |
| hollow warrant / wrong register | `follow from the physical chemistry of`; `aggressiveness of desorption` | 0.00 | 0.23 (12); 2 | barely — too rare to band |

The first two are measurable. The third is not, and it is the one that matters most, because it is
where a sentence claims to explain and does not.

## Fourth quote — and it is a span the annex labels as the good example

> "Leaching of the affinity ligand behaves as a resin property over these ranges, since ligand
> release depends on the chemistry of the immobilization, on the cumulative cycle count and on the
> sanitization history, none of which is a parameter of a single run." ... none of which is a
> parameter of a single run ... Imagine you would write a scientifc article, would you write this
> way?

**No.** Faults, in order of seriousness:

1. `behaves as a resin property` — a category error. A process does not *behave as* a property.
   What is meant is that leaching is set by the state of the resin and not by the operating
   parameters of the run.
2. Four moves in one sentence: a claim, a causal clause, a three-item list, then a trailing
   inference. A paper splits these, because each is separately arguable.
3. `none of which is a parameter of a single run` — the same appositive gloss as the first four
   quotes, in a different carrier. It performs the reader's inference for them. `parameter of a
   single run` is also not the term of art; `operating parameter` is.
4. `the chemistry of the immobilization` — periphrasis for `immobilisation chemistry`.

What a paper would write, in three sentences that are shorter in total and say more:

> Ligand leaching depends on the immobilisation chemistry, the cumulative cycle number and the
> sanitisation history. None of these varied within this study. No effect of the four operating
> parameters was therefore expected, and none was resolved.

### The count the first pass understated

`,\s+which` missed `none of which`. The full trailing-relative family, per 100 sentences:

| | PDA | A-Mab | ISPE TT | ISPE PV | corpus (20 docs) |
|---|---|---|---|---|---|
| `, which` | 1.10 | 1.44 | 0.60 | 2.35 | **9.82 (513)** |
| `<quantifier> of which` | 0.12 | 0.00 | 0.00 | 0.00 | **0.38 (20)** |
| all trailing relatives | 2.44 | 2.02 | 1.20 | 2.97 | **11.39 (595)** |

Sources 1.20–2.97. Corpus 11.39. Four to nine times over, 595 instances.

### The consequence for the benchmark, which is worse than the prose

`rhetorical_spans` is a labelled benchmark layer, not decoration. Across the nine annexed
documents it carries **26 spans labelled `mechanistic_warrant`**, and **6 of the 26 carry one of
the flagged frames** — `behaves as`, `acts on/through`, `follows from`, `aggressiveness`. Both
sentences the owner quoted are among the six. The others are in `PCR-004` and `PCR-008`.

**This sentence is span `PCR-005-R17`, and I chose it.** It was selected during TASK-006 today as
the canonical `mechanistic_warrant` anchor for the re-authored report, from a shortlist of
candidates, on the judgement that it was the clearest statement of mechanism in the section. So
the fault passed the authoring agent, the register gate, and my own review of the annex.

That is the real cost. A benchmark that labels a hollow warrant as a warrant teaches whatever is
trained on it that naming a category is the same as giving a cause.
