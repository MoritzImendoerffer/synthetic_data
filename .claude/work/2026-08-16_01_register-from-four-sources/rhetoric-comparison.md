# How the sources argue, and how the corpus argues

A passage-level comparison of DoE argumentation, taken from `refs/text/` and from the corpus on
2026-08-16. This is the evidence behind the shift of direction recorded in `exploration.md` §4:
the register problem is a **discourse** problem, not a sentence-statistics problem.

Only PDA TR 60 and A-Mab are quoted here. The ISPE guides are described but never quoted, because
whether they may be reproduced in this repository is unsettled.

---

## 1. The measurement that reframes the unit

Counts of discourse connectives, taken with `grep -ci` on the raw files:

| Connective | A-Mab | PDA TR 60 | PCR-003 | PCR-005 | PCR-008 | PCP-003 |
|---|---|---|---|---|---|---|
| However | **46** | **21** | 0 | 0 | 0 | 0 |
| For example | 12 | 22 | 0 | 0 | 0 | 0 |
| Note that / Notice that | — | — | 0 | 0 | 0 | 0 |
| By contrast | — | — | 0 | 0 | 0 | 0 |
| In addition | — | — | 0 | 0 | 0 | 0 |
| As a result | — | — | 0 | 1 | 0 | 0 |
| Consequently | — | — | 0 | 0 | 0 | 0 |
| **Therefore** | — | — | **10** | **5** | **7** | **1** |

Across roughly 30,000 words of corpus prose there is **not one "However" and not one "For
example"**. The whole connective repertoire has collapsed onto `therefore`.

`WRITING_GUIDE.md` §4b lists nine connectives as the ones the human sources use, beginning with
"However". The corpus uses one of them. And `check_style.py` puts a **ceiling** on that one
(`"therefore": (None, 1.2)`), so the gate constrains the only connective in service and says
nothing about the eight that are missing.

## 2. Why, and it is not the authors' fault

`WRITING_GUIDE.md` §2c and §2d specify the paragraph and the sentence:

> "One paragraph, one point. Open with the point, then give the evidence."
> "One sentence, one point; if a sentence carries two claims, make it two sentences."
> "Do not open a paragraph with a number or a table reference."

Those rules are good for clarity and they structurally forbid every move that needs two ideas held
in tension:

| Move | What it needs | §2c / §2d verdict |
|---|---|---|
| `However` | a claim and a counter-consideration | two points — split them |
| `For example` | a general statement and an instance | two points — split them |
| `By contrast` | two things compared | two points — split them |

An author following the guide exactly produces what the corpus contains: correct claims delivered
flat, one per unit, with nothing marking which of them is a concession, an instance or a contrast.
**The corpus is doing what it was told.**

---

## 3. Six moves the sources make, with the corpus counterpart

### Move 1 — Significance is not magnitude, shown rather than asserted

**A-Mab**, on the production bioreactor screening table:

> "For example, it is seen that medium concentration had a statistically significant effect on
> aFucosylation (p = 0.001). However, by reviewing Figure 3.4 it is seen that its effect was very
> shallow. In this case, changing the medium concentration from 0.8 to 1.6 X only changed the
> aFucosylation levels by 0.3 %."

Four moves in one paragraph: a general rule, an instance (`For example`), the counter-move
(`However`), and a quantified resolution. The point is that a p-value is not a consequence, and it
is **demonstrated on one case** rather than stated.

A-Mab also encodes the judgement in the table itself: grey arrows mark an effect "detected
statistically but too small to have an appreciable effect on the quality of the material produced".
The prose then does not need to repeat it for the other parameters.

**PCR-003 §5.2**, same argument, on acidic variants:

> "These are large and well-resolved effects of limited practical consequence, because the
> attribute is of very low criticality and its acceptance criterion is applied as an upper limit
> that lies far above the observed range. The point is quantified as a capability index (§8)."

The reasoning is right and the shape is inverted. It is one assertion with a subordinate `because`,
no instance, no counter-move, and **the quantification is deferred to another section** instead of
being given. A-Mab hands the reader "0.3 %" in the same sentence that raises the doubt. PCR-003
sends the reader to §8.

Corpus tables carry no equivalent of the grey arrow, so nothing in the table says which effects are
consequential.

### Move 2 — Limits differ in kind, and the difference is stated

**A-Mab**, defining the design space:

> "The limits for afucosylation and galactosylation represent the process targets for these quality
> attributes which are based on safety and efficacy data (CQA section). By contrast, the upper
> limit for soluble aggregates is based on the demonstrated capability of the purification process
> to clear these impurities. The limits for acidic variants are derived from acceptable changes in
> the level of deamidation based on past clinical and pre-clinical experience with A-Mab."

Three limits, three different provenances — clinical, process-capability, historical — set against
each other with `By contrast`. An assessor reading this learns which limits are negotiable and
which are not.

**The corpus states limits homogeneously.** PCR-003's design space section explains that the
in-process limit binds rather than the drug substance specification, which is the right argument,
but every attribute's limit is then presented in the same voice, and no two are contrasted by
where they came from.

### Move 3 — Anticipate the objection, answer it with premises

**A-Mab**:

> "Note, that the multivariate model was developed using afucosylation and galactosylation levels
> rather than ADCC and CDC activity results. The rationale for this approach is based on the
> following premises:"

followed by two premises, one of which reports a **negative** finding ("CDC activity was not
correlated to galactosylation levels").

The move addresses a question the reader has not asked yet: *why did you not model the thing you
actually care about?* `WRITING_GUIDE.md` §7 already names the failure — "Reviewer-blind prose. If
you cannot name the question a reviewer would ask about a passage, the passage is not doing
regulatory work" — but it gives no form for answering one, and the corpus contains no
`Note that`, no `The rationale for this approach`, and no premise list.

The nearest corpus equivalent is PCR-003's design space closing:

> "Three bounds apply to this claim. First, it holds only over the characterized ranges … Second,
> the surfaces predict mean levels, so at the boundary of the region the predicted mean sits on the
> limit and about half of the batches operated exactly there would be expected to exceed it …"

This is the strongest passage in the corpus and it is a genuinely expert argument. It is still a
**self-generated caveat list**, not an answer to a question a reader would raise. The difference is
that A-Mab names the objection first and then answers it.

### Move 4 — Tell the reader what not to worry about

**A-Mab**:

> "Notice that the limits on acidic variants and soluble aggregates are not exceeded within the
> ranges tested in the DOEs."

One sentence that disposes of two attributes and directs attention away from them. The corpus never
addresses the reader (`Notice`, `Note`, `we`: all zero) and instead gives every attribute equal
treatment, which is why its sections are uniform in length and shape — the thing
`WRITING_GUIDE.md` §7 calls out as "Uniform paragraphs … a strong signal of machine authorship".

### Move 5 — A conclusion that removes something from scope

**A-Mab**:

> "In conclusion, the cumulative process understanding gained from prior knowledge, results from
> process characterization studies and risk analysis show that the A-Mab seed expansion steps from
> vial thaw through N-1 seed bioreactor do not impact product quality and thus do not need to be
> included in the design space."

The conclusion does work: it *shrinks* the regulatory commitment, and it names the three evidence
types that license the shrinking. `In conclusion` appears zero times in the corpus.

### Move 6 — Define a method by the failure of the alternative

**PDA TR 60**:

> "This 'one-factor-at-a-time' type of experimentation cannot determine process parameter
> interactions, where the effect of one parameter on a quality attribute differs depending on the
> level of the other parameters."

The justification for DoE is given as the deficiency of OFAT. **A-Mab** makes the same move about
its own design:

> "This type of experimental design is not able to resolve all the interactions between parameters
> and it would have to be augmented on the subset of parameters shown to impact CQAs."

The corpus **does** have this move, and it is done well — PCR-003 §5.2:

> "… the main effects of culture temperature and osmolality do not, although both are of the same
> order as the significant terms. That is a consequence of the residual degrees of freedom
> available in this design and not evidence that the two factors are inactive."

So the corpus is capable of the reasoning. What it lacks is the marking that tells a reader a move
is being made.

---

## 4. What this means for the plan

**The corpus's problem is not that its arguments are weak.** Moves 3 and 6 show it reasoning at the
level the sources do. The problem is that every claim arrives in the same shape, unmarked, because
the guide's paragraph and sentence rules permit only one point per unit.

The changes that follow from this comparison, in order of expected effect:

1. **Amend `WRITING_GUIDE.md` §2c and §2d** so a paragraph may carry a claim *and* its
   counter-consideration when they belong together, and name the shapes: claim → instance →
   counter-move → resolution, as in Move 1. One point per paragraph stays the default; the tension
   pair becomes the licensed exception.
2. **Add a moves catalogue to `REGISTER_EXEMPLAR.md`**, organised by rhetorical job rather than by
   report section: how a source shows that significance is not magnitude, how it differentiates
   provenance, how it answers an objection, how it directs attention away. The exemplar is already
   "arranged by the job each passage does"; these are jobs it does not yet cover.
3. **Remove the `therefore` ceiling or pair it with the other eight connectives**, since capping
   the sole survivor is backwards.
4. **Give the tables somewhere to carry judgement**, the way A-Mab's grey arrows do, so that the
   prose does not have to qualify each effect in turn.
5. **Only then re-author**, and judge the result by whether a reader can tell the corpus passage
   from the source passage — not by a connective count. A count of "However" is a diagnosis, and it
   would be a bad target: an author told to produce contrast markers will produce them.
