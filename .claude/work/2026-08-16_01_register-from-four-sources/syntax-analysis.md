# What the dependency parse says the difference is

Parsed with spaCy `en_core_web_sm` 3.8.0 on 2026-08-16, over 450 sentences per human source and
every sentence of each corpus document. Inline `{python}` expressions were replaced by a numeral
before parsing, so the corpus sentences keep the shape a reader sees.

Reproduce with `scratchpad/depparse.py` and `scratchpad/verbs.py` (spaCy is **not** a project
dependency; both were run through `uv run --with spacy`).

## The features that do not differ

| Feature | A-Mab | PDA TR 60 | PCR-003 | PCR-005 | PCR-008 | PCP-003 |
|---|---|---|---|---|---|---|
| tree depth | 7.75 | 7.37 | 6.99 | 6.91 | 6.98 | 6.62 |
| nested PP depth | 1.37 | 1.34 | 1.31 | 1.37 | 1.33 | 1.24 |
| noun-compound chain | 1.30 | 1.10 | 1.02 | 1.20 | 1.04 | 0.94 |
| finite verbs / sentence | 2.43 | 2.38 | 2.35 | 2.25 | 2.27 | 2.44 |
| relative clauses / sentence | 0.27 | 0.24 | 0.25 | 0.27 | 0.28 | 0.25 |

**The corpus is not syntactically more complex than the sources.** It is slightly simpler on every
structural measure. So "hard to read" is not caused by long or deep sentences, and no rule about
sentence length will touch it.

## The two features that do differ

| Feature | A-Mab | PDA TR 60 | PCR-003 | PCR-005 | PCP-003 |
|---|---|---|---|---|---|
| **% of sentences shaped "X is \<noun phrase\>"** | **14.7** | **18.2** | **33.3** | 26.7 | 18.3 |
| **`be` as the main verb (count / sentences)** | 66 / 408 | 82 / 421 | **144 / 420** | 100 / 367 | 37 / 195 |
| light main verb overall (`be, have, show, provide, make, …`) | 30 % | 29 % | **43 %** | 38 % | 25 % |
| **tokens before the main verb** | **9.22** | **9.36** | **5.78** | 6.93 | 6.33 |
| subject–verb gap | 3.33 | 4.47 | 1.62 | 2.00 | 2.49 |

Two independent findings:

**1. A third of PCR-003's sentences have no event in them.** The main verb is `be`, and the
content sits in abstract nouns joined by prepositions. Human regulatory prose does this half as
often.

**2. Human sentences carry more before the main verb, not less.** A-Mab and PDA both put about
nine tokens in front of the verb; the corpus puts under six.

**That figure conflates two things, and the decomposition matters** (`scratchpad/front.py`):

| | A-Mab | PDA | PCR-003 | PCR-008 | PCP-003 |
|---|---|---|---|---|---|
| adjunct tokens before the subject phrase | 3.03 | 2.64 | 1.62 | 1.31 | 1.22 |
| length of the subject phrase itself | 5.64 | 5.64 | 3.80 | 3.98 | 4.20 |
| tokens between subject and verb | 1.01 | 1.19 | 0.44 | 0.59 | 1.19 |
| **% of clauses with a real front field** | **29.5** | **25.4** | **13.6** | **9.1** | **9.1** |

Both parts differ. The actionable one is the front field: **about one human main clause in four
opens with an adjunct, against one in ten of the corpus.** The subject-phrase difference is a
separate observation and probably follows from the corpus naming things tersely.

**And the slot is used for a different job.** The most common real front fields:

| | |
|---|---|
| A-Mab | `Also,` `Thus,` `Therefore,` `However,` `In addition,` `Here,` |
| PDA TR 60 | `For example,` `However,` `In these cases,` `In some cases,` `In this case,` `For this reason,` |
| PCR-003 | `First,` `Second,` `Third,` `For galactosylation` `For high mannose` `For aggregate` |

The human front field carries a **logical connective**. The corpus front field carries an
**enumerator or a topic label**. The slot is not missing from the corpus; it is filled with list
markers instead of argument links, which is the connective finding of
[`rhetoric-comparison.md`](rhetoric-comparison.md) seen from the other side.

**3. Canonical word order is not the difference.** Audited over 1,527 human main clauses
(`scratchpad/svo.py`):

| % of main clauses | A-Mab | PDA | PCR-003 | PCP-003 |
|---|---|---|---|---|
| subject before its verb | 100.0 | 99.9 | 99.7 | 100.0 |
| object after its verb | 100.0 | 100.0 | 100.0 | 100.0 |
| subject after the verb | 0.0 | 0.1 | 0.3 | 0.0 |
| object before the verb | 0.0 | 0.0 | 0.0 | 0.0 |

Human regulatory prose does not invert. The one PDA exception is a parse artifact where an embedded
quoted question runs into the next sentence. So a rule forbidding inversion — as the sibling
repository's guide has — is correct for this genre and is **not a live constraint**, because
nothing in either corpus violates it. Fronting an adjunct is not inverting: the SVO core is intact
in 100 % of clauses on both sides.

## The two sentences, parsed

**A-Mab** — *"In this case, changing the medium concentration from 0.8 to 1.6 X only changed the
aFucosylation levels by 0.3 %."*

| | |
|---|---|
| ROOT | `changed` — a lexical event verb |
| direct object | `levels` |
| abstract nouns | `concentration` (1) |
| prepositions | `In`, `from`, `by` (3, none stacked) |

The sentence states an event: a named change of input produced a measured change of output. The
front field (`In this case,`) ties it to the argument above it.

**PCR-003 §5.2** — *"These are large and well-resolved effects of limited practical consequence,
because the attribute is of very low criticality and its acceptance criterion is applied as an
upper limit that lies far above the observed range."*

| | |
|---|---|
| ROOT | `are` — the copula |
| subjects | `These`, `attribute`, `criterion`, `that` — four clauses |
| predicate | `effects` |
| abstract nouns | `consequence`, `criticality`, `acceptance` |
| prepositions | `of`, `of`, `as`, `above` |

Nothing happens in this sentence. Its subject is a bare demonstrative whose antecedent is a table,
its predicate is a noun, and the argument is carried by three nominalisations chained on
prepositions. That is the "vague, not like a scientific text" quality precisely: the reader has to
reconstruct the events from the nouns.

## What an unsupervised pass found that reading did not

`scratchpad/divergence.py` emits dependency-triple features for both sides, compares rates and
sorts by log ratio, with no hypothesis about what matters. It rediscovered two findings above —
auxiliaries per sentence 1.00 → 0.21 (the modality gap) and sentence-initial adverbs 5.4× rarer
(the front field) — and surfaced one that reading the passages had not:

| Word | A-Mab per 1k | PCR-003 per 1k | Ratio |
|---|---|---|---|
| `its` | 0.28 | **6.67** | **24×** |
| `it` | 1.50 | 10.63 | 7× |
| `their` | 0.53 | 4.16 | 8× |

The corpus binds almost every noun to a possessive: "its acceptance criterion", "its characterized
range", "its set-point", "its limit", "its expiry", "its release specification". A-Mab writes "the
acceptance criterion" or names the thing. This is the largest single divergence found by any
method, and it is a direct readability cost: each possessive makes the reader hold an antecedent
and bind it. The failing sentence does it twice.

**Rule.** Prefer the definite article or the noun itself. A possessive is for a genuine
relationship that the reader would otherwise mistake, not for every attribute of a thing already
under discussion.

**A caveat about the method.** The top of the divergence ranking was dominated by artifacts of
replacing inline expressions with a numeral (`NUM<nmod<PROPN`, `OPEN_POS=NUM`). The ranking finds
where two corpora differ; deciding which differences are style and which are measurement is still a
person's job.

## Five further analyses, of which four returned null results

Run with `scratchpad/more.py`. A null result here is worth as much as a finding: it stops a
plausible-sounding rule from being written into the guide.

| | A-Mab | PDA TR60 | PCR-003 | PCR-008 | PCP-003 |
|---|---|---|---|---|---|
| **% of sentences chained to the previous one** | **57.0** | **59.6** | **35.1** | **32.8** | **31.0** |
| hedges per 1k | 6.6 | 24.5 | 3.3 | 3.7 | 4.4 |
| boosters per 1k | 10.2 | 10.0 | 7.0 | 7.0 | 5.7 |
| hedge : booster | 0.64 | 2.45 | 0.47 | 0.54 | 0.78 |
| nominalisation heading an `of` phrase, per 1k | 8.9 | 9.0 | 4.4 | 5.3 | 2.7 |
| repeated 4-gram tokens per 1k | 66.5 | 28.5 | 47.6 | 55.7 | 14.3 |
| longest coordination chain | 0.91 | 0.91 | 0.82 | 0.72 | 0.95 |

### The finding: topic chaining, and it is a rule the guide already has

A sentence is **chained** when its subject names something the previous sentence already mentioned,
or is a pronoun. Human sources chain **57 % and 60 %** of sentences. The corpus chains **31 to
35 %**, so about two thirds of its sentences start a fresh topic and the reader is re-oriented
each time.

`WRITING_GUIDE.md` §2d already states the rule: *"Begin with information the reader already has and
end with the new information."* It is met a third of the time. **This is not a rule to invent, it
is a rule to exemplify and check** — a different and cheaper kind of fix.

It also explains the front-field result above. `For galactosylation` / `For high mannose` /
`For aggregate` are topic *switches*. Each one tells the reader to drop the previous subject and
pick up a new one.

### Four null results

1. **Nominalisation is not the problem.** The corpus heads an `of` phrase with a nominalisation at
   4.4 per 1000 words against the sources' 8.9 and 9.0 — it does this **half as often** as human
   regulatory prose. A rule saying "avoid nominalisations" would push the corpus further from its
   sources, not closer.
2. **The corpus is not more formulaic.** Repeated 4-grams run 47.6 per 1000 words in PCR-003
   against A-Mab's 66.5, with 136 distinct repeated 4-grams against A-Mab's 405. Human regulatory
   prose repeats its terminology heavily and that is normal. No rule.
3. **Nothing over-claims.** Boosters run 5.7–7.0 per 1000 words in the corpus against 10.0–10.2 in
   both sources. Combined with the hedge deficit, the corpus is flat in **both** directions: it
   neither commits nor qualifies as much as a human author. The defect is not overconfidence.
4. **Coordination is identical.** Longest in-sentence list chain 0.72–0.95 on both sides. The
   "prose narrates the table as a list" hypothesis is not supported at the syntactic level.

### On hedging, genre matters

PDA TR 60 hedges at 24.5 per 1000 words because it is guidance: it recommends rather than reports.
A-Mab, the closer genre to a characterization report, sits at 6.6, still 1.7× the corpus. So the
target for a report is A-Mab's rate and not PDA's, and the plan should say which source is the
reference for which document type.

## Five rules that follow, each with its measured target

These are derived from the parse, not from taste. Each names the number a document can be checked
against, and each is a **diagnosis**, never a target an author should optimise directly.

1. **The main verb names the event.** `be` as the root verb in at most **20 %** of sentences
   (human 16–19 %; PCR-003 is at 34 %). Rewrite `X is a Y of Z` as `X does Z`.
2. **Front the frame, then go subject–verb–object.** Aim for roughly **9 tokens before the main
   verb**, not 6. That field holds the condition, the contrast or the case in hand — which is where
   `However` and `For example` live.
3. **An abstract noun may not be the payload.** `effects of limited practical consequence` states
   nothing a reader can check. Give the magnitude that makes it true.
4. **A demonstrative subject names its antecedent.** `These are …` becomes `These three effects
   are …`, or names them. `this`/`these`/`it` as bare subject: 5.8–10.2 % in the corpus and
   7.6–9.6 % in the sources, so the rate is fine — the failure is the missing head noun, not the
   frequency.
5. **Cap the of-chain.** Two stacked `of` phrases in one predicate is the signature of a sentence
   that should have had a verb.

## Worked rewrite

The PCR-003 sentence, rebuilt on the A-Mab shape (rule → instance → counter-move → quantified
resolution). Numbers stay inline expressions, per the numbers rule:

> Raising dissolved CO₂ across its characterized range lowers acidic variants by
> `` `{python} f"{abs(eff('acidic_variants','C')):.1f}"` `` percentage points, and the effect is
> well resolved. However, the attribute is of very low criticality, and its acceptance criterion
> applies only as an upper limit. The highest level any screening run reached was
> `` `{python} f"{acid_max:.1f}"` `` %, against a limit of
> `` `{python} f"{D.acceptance_for(UO,'acidic_variants')[1]:.0f}"` `` %.

Three sentences, three lexical main verbs (`lowers`, `applies`, `reached`), one `However`, and the
number that settles the doubt is given here rather than deferred to §8. Same facts, same grounding,
same helpers.
