# Writing a process-characterization report — the standard

This is the standard for authoring an A-Mab characterization **report** (`PCR-00N`) in one
pass, at full depth. Read all of it before writing any section.

You are the sole author of the document. Two grounded inputs support you:

- the **report brief** (`authoring/out/<DOC>.brief.md`). This holds the facts for your
  unit operation: its role, CQAs, parameters, DoE structure, results helpers and seeded
  deviations. It also holds the **helper inventory**, which is the list of inline
  expressions you are allowed to call. Every number you write comes from there.
- the **section plan** (`authoring/section_plan.yaml`). This gives the ordered sections,
  the obligations that apply to each, and a target length band. Write them in order.

Two further artifacts set the voice: `authoring/REGISTER_EXEMPLAR.md` holds verbatim
passages from the published human documents this corpus is modelled on, and
`authoring/STORY_BIBLE.md` holds the world canon.

---

## 1. Who you are writing for

An assessor at a regulatory agency reading a Biologics License Application. They are a
skeptical expert with limited time. They read to find the weak point in the argument.

Three things follow from this.

**State the finding early.** The reader should learn the conclusion of a section from its
first sentence, and the point of a paragraph from its first sentence. Support comes after
the claim.

**Bound your claims.** A claim that does not say where it stops is a defect. Say which
ranges were studied, what the model covers, and what the scale-down model assumes. Put the
bound in its own sentence. Do not grow the claim sentence to hold it.

**Never ask the reader to take a number on trust.** Every quantitative statement traces
back to the model. You do not type numbers (§6).

---

## 2. Structure

Good technical prose has the same shape at every scale: context, then the new thing, then
what it means.

### 2a. The whole report

A 30-page report is one argument, not fifteen filing cabinets. It opens wide, narrows to
the studies, and widens again:

- **Opening.** The product, the step's role in the train, the regulatory basis.
- **Challenge.** Which CQAs this step governs, and why they are at risk here.
- **Action.** Prior knowledge and risk basis, scale-down model, study design, results,
  design space, capability, parameter classification. This is the body, at full depth.
- **Resolution.** The contribution to the control strategy, the discussion, the
  conclusions. Widen back out to what the step now assures.

The canonical section order is this arc. The executive summary states the resolution up
front. The body narrows to the studies. The control-strategy and discussion sections widen
again.

### 2b. A section

Open a section by establishing the agreed context, then the uncertainty or risk that made
the work necessary, then your finding. State the finding before the evidence for it.
Group the support so that each paragraph carries one argument, and put the strongest
first.

An opener for a results section, in the register you should be writing in:

> Cation exchange is the principal aggregate polishing step in the purification train.
> Prior work had not quantified how load and elution conditions interact at commercial
> scale. A response-surface model over four factors defines a region in which the pool
> aggregate remains below its limit across the ranges studied. The supporting data are
> given below.

Four sentences, four jobs. Note that each one is short, and that none of them announces
what it is doing.

### 2c. A paragraph

One paragraph, one point. Open with the point, then give the evidence.

Where the meaning of the evidence is not obvious, say what it means. Where it is obvious,
stop. A closing significance clause on every paragraph is the clearest signature of
machine-written text, and it reads as padding to an assessor who already understood the
point two sentences ago. Some paragraphs correctly end on a fact.

Do not open a paragraph with a number or a table reference.

**The one licensed exception: a point may be held together with its counter-consideration.**
One point per paragraph remains the default, and it governs almost every paragraph you write.
But a claim that has a real counter-consideration keeps it in the same paragraph, marked. The
rule was read for a while as forbidding that, and the corpus complied: across roughly 30,000
words of it there was not one "However". A document that never concedes reads as a sequence of
unrelated assertions, which is the thing an assessor notices first.

**On the ✗ examples in this section and in §2d bis.** Four worked corrections quote `PCP-003` and
`PCR-003` **as they stood before 2026-08-17**. Both documents were re-authored from this guide
on that date and neither contains the ✗ prose any more, and in two of the four the ✓ version is
close to what the re-authored text now says. The examples stay, because they are real
machine-register prose produced by a careful author following the unamended rules, which is
exactly what makes them worth studying. Each carries the date so the guide does not assert
something false about the corpus as it now stands.

**Shape 1: rule → instance → counter-move → quantified resolution.** State the effect, give the
case, mark the turn, then settle it with the number that settles it.

> "For example, it is seen that medium concentration had a statistically significant effect on
> aFucosylation (p = 0.001). However, by reviewing Figure 3.4 it is seen that its effect was
> very shallow. In this case, changing the medium concentration from 0.8 to 1.6 X only changed
> the aFucosylation levels by 0.3 %."
> — A-Mab

Worked correction, from `PCR-003` §5.2 as it stood before 2026-08-17:

> ✗ These are large and well-resolved effects of limited practical consequence, because the
> attribute is of very low criticality and its acceptance criterion is applied as an upper
> limit that lies far above the observed range. The point is quantified as a capability index
> (§8).

The turn is there, but it is carried by "because" inside a single copula sentence whose subject
is a bare demonstrative pointing at a table, and the number that would settle the doubt is
deferred to another section. The reader has to take "far above" on trust for five more pages.

> ✓ Raising dissolved CO₂ across its characterized range lowers acidic variants by
> `` `{python} f"{abs(eff('acidic_variants','C')):.1f}"` `` percentage points, a well resolved
> effect. However, the attribute is of very low criticality, with an acceptance criterion that
> applies only as an upper limit. The highest level any screening run reached was
> `` `{python} f"{acid_max:.1f}"` `` %, against a limit of
> `` `{python} f"{D.acceptance_for(UO,'acidic_variants')[1]:.0f}"` `` %.

Three sentences, three lexical main verbs, one "However", and the resolving number given in
place instead of promised for later.

`acid_max` is not an existing helper. Derive it in the setup chunk, the way that report already
derives `cv_scr_max` before quoting it in the results:

```python
acid_max = csv(f"doe_{UO}_screening.csv")["acidic_variants"].max()
```

Typing the number itself is what §6 forbids, and the exception in this section relaxes
nothing about that.

**What this exception must not become.** It licenses a tension pair. It does not license a long
sentence, and it is not permission to reach for an em-dash. The failure it must not cause is
the first-pass corpus, which ran to a 34-word mean sentence against a human 24 to 30, 10 to 13
em-dashes per 1000 words against A-Mab's zero, and a semicolon splice in every fourth sentence.
The correction to that overshot in the other direction, into 17-word averages with 40 % of
sentences under 15 words, which is why §4a bands are two-sided. Both failures are visible from
across the room. If a tension pair is making your sentences longer, you are writing the wrong
shape: the human examples in this section and the next run 14 to 24 words, with one at 40.

### 2d. A sentence

Begin with information the reader already has and end with the new information. Keep the
subject next to its verb. **One argument step per sentence.** When the next step is a
consequence, a contrast or a recommendation, end the sentence and open the next one with the
connective: "Therefore, …", "However, …", "As a result, …", "For this reason, …". Do not join
the steps inside one sentence with ", so …" or with ", and …" carrying a second claim, and do
not carry a new claim in a ", which …" clause.

**This is a substitution. Check it in your draft.** Search for `, so `, for `, and ` that
introduces a second clause (`, and the`, `, and this`, `, and both`, `, and it`), and for
`, not `. Each one is a place where the sources would have written a full stop and a connective.
Measured over the pages the self-test reads (2026-08-17): the four sources carry a mid-sentence
", so " in 0.1 to 0.4 % of their sentences and open 3.7 to 6.1 % of their sentences with a
connective. The corpus carries ", so " in 6 to 11 % of sentences and opens 0 to 2 % with a
connective.

The other two were measured a round later, on 2026-08-18, after the project owner read a report
that had cleared every target above and still read as machine prose. `, and ` joining a second
clause runs at 18 to 23 % of corpus sentences against 1.1 to 3.4 % in the sources, and it did
not move at all in the round that drove ", so " to zero. A mid-sentence `, not ` reached 4.3 %
in that report against 0.0 to 0.2 % in the sources, and the round before it was at zero:
correcting one habit had produced another. `check_style.py` prints all four figures on every
run, and none of them is gated.

**Correction 0 — three steps in one sentence.** From `PCR-003`, *Discussion*, as it stood on
2026-08-17. The project owner quoted it as "hard to understand, too many arguments in one
sentence, including a recommendation in the last part":

> ✗ The lack-of-fit tests rest on `` `{python} f"{cp_rsm}"` `` centre-point replicates, so a
> non-significant result bounds the evidence for the model form without establishing it, and
> `` `{python} lof_p_lo_resp.lower()` `` is the case to watch (p = `` `{python} f"{lof_p_lo:.2f}"` ``).

A premise, a consequence and a recommendation, joined by ", so … , and …". The reader has to hold
all three to the end.

> ✓ The lack-of-fit tests rest on `` `{python} f"{cp_rsm}"` `` centre-point replicates.
> Therefore, a non-significant result bounds the evidence for the model form without
> establishing it. For this reason the weakest case to watch at scale is
> `` `{python} lof_p_lo_resp.lower()` `` (p = `` `{python} f"{lof_p_lo:.2f}"` ``).

Three sentences, one step each, and the second and third open on the connective that carries
the step. Note the third: the response name is a runtime value. It can therefore never be the
subject of a verb that has to agree with it, and "acidic variants is the case to watch" came
from exactly that. Put a runtime name after "is" or after a preposition, never before the verb.

> ✗ A 1.4-fold increase in pool aggregate, which is consistent with the descending-edge
> mechanism described above and was also seen at bench scale, resulted from the highest
> load.
> ✓ The highest load raised pool aggregate 1.4-fold. This is consistent with the
> descending-edge mechanism described above and reproduces the bench-scale result.

**Where the sources would write a passive, write the passive.** This is the same failure one
step further out. Correction 0 is an author supplying a *subject* the fact does not have; this
is an author supplying an *agent*. A study, a design or a screening does not retain, carry
forward or select anything. The people who ran it did, and the sources report that decision in
the passive: "were classified as", "were selected", "were identified as". The four sources put a
passive construction in 57 to 64 % of their sentences (§4a, §4b); the round-two `PCR-003` was at
35 %, having fallen at every revision, and the project owner's reading of it named the cost.
From `PCR-003`, *Executive summary*, as it stood on 2026-08-18:

> ✗ The 4 factors that screening retained then entered a face centred response surface design of
> 28 runs, and the remaining 4 parameters were assessed one at a time.

Screening is a study. It retained nothing. The sentence also carries the balanced `, and `
second clause that is its own fault, above.

> ✓ The 4 factors retained from screening then entered a face centred response surface design of
> 28 runs. The remaining 4 parameters were assessed one at a time.

Every fact survives, the agent is gone, and the two steps are two sentences. Search a draft for
`screening retained`, `the design carries`, `the study selected`, `the model identifies`.

**Reporting evidence is not the same thing, and it is not a fault.** The rule is about
decisions, not about observations. Counted in the four sources on 2026-08-18: "Results showed",
"studies showed", "the data shows" and "The analysis shows" occur about twenty times between
them, and "the assessment identified" or "studies identified" seven times. Not one of the four
ever writes a study as the agent of *retain*, *carry* or *select*. So evidence may be the
subject of a verb that reports what it shows; a study may not be the subject of a verb that
reports what a person decided.

**This first rule is the one the corpus misses most, and it is not close.** A sentence carries
the topic forward when its subject names something the sentence before it mentioned, or is a
pronoun. Measured across the pages the self-test reads, the four sources chain **57.0 to 61.9 %**
of their sentences. The 20 corpus documents chain a median of **36.3 %**, in a range of 29.2 to
42.2 %. So two sentences in three open a fresh topic and the reader is re-oriented on almost
every one. Three worked corrections, all from documents in this corpus.

**Correction 1 — a parallel block, one fresh subject per sentence.** From `PCR-004`, *Quality
attributes in scope*:

> ✗ Host cell protein is the most consequential of the three, at moderate to high criticality,
> because it is the impurity present in the largest amount in the clarified harvest. Aggregate
> is of high criticality and is the one attribute with a plausible mechanism at this step, since
> shear at the centrifuge feed zone could in principle raise it. Residual DNA is of very low
> criticality on its own, and is cleared by a large margin downstream.

Three sentences, three brand-new subjects, three copulas. The reader is handed a list and has to
work out for themselves that it is a ranking. Nothing in sentence two says it follows from
sentence one.

> ✓ Host cell protein is the most consequential of the three, at moderate to high criticality,
> because it is the impurity present in the largest amount in the clarified harvest. The second
> of the three, aggregate, is of high criticality for a different reason: shear at the centrifuge
> feed zone could in principle raise it. The third, residual DNA, is of very low criticality here
> and clears by a large margin downstream.

Each subject now opens on something the previous sentence established — "the three" — and the new
information lands at the end where it belongs. The ranking is on the page instead of in the
reader's head. Nothing was added and nothing was dropped except one possessive.

**Correction 2 — a fresh subject where the chain was already there.** From `PCMR-001`, *Process
capability*:

> ✗ The remaining attributes sit far from their limits, and their indices should be read as
> showing that the attribute does not constrain the process, and not as meaningful precision.
> Leached Protein A is the extreme case, at `` `{python} f"{lpa_ratio:,.0f}"` ``-fold below its
> limit, and its index is reported in @tbl-cap for completeness only.

The second sentence has a perfectly good given to start from and starts somewhere else instead.
It also stacks three possessives on referents the reader has to bind.

> ✓ The remaining attributes sit far from their limits. Their capability indices therefore show
> only that none of them constrains the process. The furthest is leached Protein A, at
> `` `{python} f"{lpa_ratio:,.0f}"` ``-fold below the limit, and @tbl-cap reports its index for
> completeness.

**Correction 3 — the referent hidden four times over.** From `PCP-004`, *Factors, ranges and
study type*:

> ✗ Each settable parameter will be studied at its low characterization edge, at its set-point
> and at its high characterization edge, with the other settable parameter held at its set-point,
> which gives `` `{python} n_conditions` `` clarification conditions in all, listed in @tbl-cond.

One sentence, four possessives, and by the fourth the reader has to decide which parameter "its"
belongs to. The answer is the other one, which is exactly the binding a possessive should never
be asked to carry.

> ✓ Each settable parameter will be studied at three levels: the low edge of its characterization
> range, the set-point and the high edge. While one parameter moves, the other is held at the
> set-point. That gives `` `{python} n_conditions` `` clarification conditions in all, listed in
> @tbl-cond.

One possessive survives, and it is the one that marks a real relationship: the range belongs to
the parameter. The rest became "the".

**Name the set you count.** "The four that matter", "both", "the three" ask the reader to bind a
number to things named somewhere else. If the paragraph has not named them, the sentence does.
From `PCR-003`, *Discussion*, as it stood on 2026-08-17 (the four factors were last named 270
lines earlier):

> ✗ … a screening design that ranked the factors and a response-surface design that models the
> four that matter.

> ✓ … a screening design that ranked the five factors and a response-surface design in the four
> that screening retained: culture pH, temperature, culture duration and dissolved CO2.

### 2d bis. Prefer the definite article or the noun itself

The same defect at word level. A possessive makes the reader bind a referent; an article or the
noun just says what is meant. Measured per 1000 words of prose:

| | corpus, 20 documents | PDA TR 60 | A-Mab | ISPE TT | ISPE PV |
|---|---|---|---|---|---|
| *its* | **5.73** | 0.40 | 0.32 | 0.27 | 0.36 |
| *their* | **2.29** | 0.96 | 0.50 | 0.63 | 0.69 |
| *it* | **9.59** | 3.12 | 1.75 | 3.33 | 3.19 |

*its* runs at **fourteen times** the highest of the four sources, and `PCR-003` reaches 6.66. The
corpus writes "its acceptance criterion", "its characterized range", "its set-point", "its
limit". The sources write "the acceptance criterion", or name the thing.

**Rule.** Use the definite article or the noun. Keep a possessive for a genuine relationship the
reader would otherwise mistake — "its characterization range" when two parameters are in play and
the range belongs to one of them. Do not use one for every attribute of a thing already under
discussion. This was the largest single divergence any method found between the corpus and the
sources, and it was found by ranking word frequencies, not by reading.

**The substitution is the definite article or the noun, and never "it is".** Round one of the
register pilot applied this rule two ways. `PCR-003` replaced possessives with articles and
nouns and its copula rate barely moved. `PCP-003` replaced 25 possessives with 23 expletive
subjects ("it is", "it was", "it will be" went from 7 to 21) and its copula rate rose from
18.4 % to 27.6 %, outside all four sources. Same rule, opposite cost.

**The target is a band, not a minimum.** The sources sit at 0.27 to 0.40 *its* and 0.50 to 0.96
*their* per 1000 words. Aim inside those bands; a document at 0.02 has driven out the licensed
exception too, and paid for it somewhere else.

**The same licensed exception applies here**, and for the same reason as in §2c. One point per
sentence stays the default. A claim and its qualification are one sentence when the
qualification is what bounds the claim, because splitting them lets a reader carry the claim
away without the bound. Three shapes do this, and none of them is long.

**Shape 2: concede first, then commit.** The concession goes in the front field, subordinated.
The commitment is the main clause, so it is the part that survives being skimmed.

> "Although key process parameters and key process attributes have been shown not to impact
> product quality, they are included in the control strategy because their monitoring and
> control ensures that the process is operated in a consistent and predictable manner."
> — A-Mab

> "Although the extent of the effects may differ slightly, viral clearance decreases as pH
> decreases and conductivity increases."
> — A-Mab

The second is 18 words and carries a concession, a hedge and two lexical verbs at once.
The first runs to 40, which is the upper end of what this shape should ever need.

Worked correction, from `PCP-003` §6 as it stood before 2026-08-17:

> ✗ The response-surface design assumes that screening identifies the factors that matter, and
> if screening identifies a different set the matrix in Appendix B will be re-issued before
> execution. That is an amendment to this plan and not a deviation from it.

The commitment is buried in a conditional clause at the end of a 28-word sentence, and the
qualification that matters is stranded in a separate copula sentence whose subject is "That".

> ✓ Although the matrix in Appendix B is written on the assumption that screening identifies
> the factors that matter, screening may identify a different set. The matrix is then re-issued
> before execution, which is an amendment to this plan and not a deviation from it.

**Shape 3: a finding and its limit in one sentence, with the limit in consequence terms.**
A limit stated only in statistical terms is not a limit a reviewer can act on.

> "Grey arrows indicate the effect was detected statistically but is too small to have an
> appreciable effect on the quality of the material produced."
> — A-Mab

Worked correction, from `PCR-003` §5.2 as it stood before 2026-08-17:

> ✗ `` `{python} n_sig_scr('afucosylation')` `` terms reach significance at α =
> `` `{python} alpha` ``, and the main effects of culture temperature and osmolality do not,
> although both are of the same order as the significant terms. That is a consequence of the
> residual degrees of freedom available in this design and not evidence that the two factors
> are inactive.

The finding is reported, and its limit is real, but the limit is entirely statistical: degrees
of freedom, order of magnitude, significance. Nothing tells the reader what it means for the
material. Say the consequence and attach the statistics to it.

> ✓ Culture temperature and osmolality do not reach significance at α =
> `` `{python} alpha` ``, but their effects are of the same order as the terms that do. Neither
> can therefore be called inactive on this design. Temperature is carried into the
> response-surface stage on that basis. Osmolality is not. Its range rests on the screening
> result and on the classification rationale in §9.

Check a rewrite against the data before you keep it. An earlier draft of this example ended
"and both are carried into the response-surface stage", which is false: the response-surface
design for this step carries pH, temperature, duration and dissolved CO₂, and drops osmolality.
A shape is not a licence to write a tidier sentence than the study supports.

**Shape 4: the frame comes before the subject.** A real front field opens 29.5 % of A-Mab's
clauses and 25.4 % of PDA TR 60's, against 9.1 to 13.6 % of the corpus documents measured. The
difference is not the slot, it is what fills it: the sources put a connective or a condition
there, the corpus puts a counter.

> "In this case, changing the medium concentration from 0.8 to 1.6 X only changed the
> aFucosylation levels by 0.3 %."
> — A-Mab

> "Based on process understanding, no further process development studies were deemed necessary
> for A-Mab seed culture expansion up to the N-2 step."
> — A-Mab

> "Since screening designs do not always clearly identify interactions, the reduced number of
> parameters identified by the screening experiment will be included in further experiments."
> — PDA TR 60

Worked correction, from `PCR-003` §2.1 as it stood before 2026-08-17:

> ✗ Four mechanistic expectations were carried into the study. First, galactosylation tracks
> the activity of the Golgi galactosyltransferase … Second, high mannose reflects the
> completeness of mannosidase trimming … Third, afucosylation reflects the competition …
> Fourth, aggregate formed in culture reflects the residence of secreted antibody …

Every front field holds a number. "First" tells the reader that three more are coming and
nothing else. A list of four expectations does not need to be announced or counted, and an
enumerated run is the surest way to make four related mechanisms read as four unrelated ones.

> ✓ Galactosylation tracks the activity of the Golgi galactosyltransferase and the availability
> of its nucleotide sugar donor, both of which decline as a culture ages. High mannose is
> enzymatic in the same way, and reflects how completely mannosidase trimming has run, which
> makes it sensitive to lumenal pH and to temperature. Afucosylation is set by a competition
> instead, between core fucosyltransferase activity and the rate of antibody transit. It was
> therefore expected to fall as the culture progresses. Aggregate is the one expectation that is
> not enzymatic: antibody that sits longer in an ageing broth aggregates more.

The counters are gone and each sentence now says how it relates to the one before it: in the
same way, instead, the one that is not. The reader learns why these four expectations belong in
one paragraph, which "First, Second, Third, Fourth" never told them.

**Second correction — write the frame instead of deleting one.** From `PCR-003`,
*Response-surface design*, as it stood on 2026-08-17:

> ✗ The response-surface model does not carry osmolality, so the interaction between temperature
> and osmolality that screening resolved on galactosylation (@tbl-eff-gal) is represented in
> this report by the screening estimate alone.

> ✓ Because the response-surface model does not carry osmolality, the interaction between
> temperature and osmolality that screening resolved on galactosylation (@tbl-eff-gal) is
> represented in this report by the screening estimate alone.

The condition moves into the front field and the main clause is the claim. One word changed and
the sentence now has the shape 29.5 % of A-Mab's clauses have.

---

## 3. The rigor overlay

Apply the obligations the section plan lists for each section. Several apply everywhere.

- **Grounding.** Every number is an inline expression from the model (§6). Prose may state
  only what the data support.
- **Screening identifies; the response surface predicts.** Say so. The screening design
  finds which factors matter. The response-surface model is the predictive model and the
  basis of the design space. Do not present the near-saturated screening fit as
  predictive.
- **Bounded conclusions.** Close a results or design-space claim with at least two of: the
  range studied, what the model does and does not cover, and the assumptions behind it
  (feed states, scale-down validity).
- **Hedging matched to evidence.** State strong effects with tight confidence intervals
  plainly. Hedge small or non-significant effects near a limit, and attribute variance to
  the assay where that is the cause. Match the verb to the evidence: "demonstrates",
  "is consistent with", "suggests".
- **Adverse findings come first.** When a result is worse than expected, give the adverse
  magnitude first, then the mitigating evidence, then where that leaves the study. Do not
  open with the reassurance.
- **Cross-step credit.** When several steps control an attribute, give this step's
  contribution and name the documents that cover the others.
- **Deferral names a location.** Never "data not shown". Point to an appendix, a paired
  report, an SOP or a method validation.
- **Null results are informative.** A factor with no significant effect is still
  classified, and it stays in the knowledge space as evidence of robustness. Say so.

---

## 4. Register: plain technical English (hard requirement)

This is the section that most often goes wrong, so it is specified in measurable terms.

Write **simple technical English at roughly C1 level**. The reference is not academic
prose and not literary prose. It is the register of the four published documents this
corpus is built on, all of which are in `refs/text/`:

- PDA Technical Report No. 60, *Process Validation: A Lifecycle Approach* (2013)
- *A-Mab: A Case Study in Bioprocess Development*, CMC Biotech Working Group (2009)
- ISPE Good Practice Guide: *Technology Transfer*, third edition (2023)
- ISPE Good Practice Guide: *Practical Implementation of the Lifecycle Approach to Process
  Validation* (2023)

Read `authoring/REGISTER_EXEMPLAR.md` before writing. It is a collection of verbatim
passages from those documents, arranged by the job each one does.

### 4a. The measurable targets

`authoring/check_style.py` measures these and **fails the build** if they are missed. The
thresholds are read off the four human documents above, and `check_style.py --selftest`
proves that all four pass.

Several of these are **bands, not ceilings**. Writing that is too short and too choppy is
just as unlike a real regulatory document as writing that sprawls. Human technical prose sits
in the middle.

| Property | Band | PDA TR 60 | A-Mab | ISPE TT | ISPE PV |
|---|---|---|---|---|---|
| Mean sentence length | 20 – 30.5 words | 24.2 | 26.6 | 28.0 | 30.2 |
| Median sentence length | 18 – 26.5 words | 21.0 | 23.0 | 24.0 | 26.0 |
| Sentences over 40 words | 3 – 21.5 % | 9.8 | 13.4 | 14.8 | 20.8 |
| Sentences over 55 words | ≤ 9.5 % | 2.9 | 5.2 | 5.8 | 9.0 |
| Sentences under 15 words | 15 – 32 % | 20.5 | 19.5 | 16.3 | 16.2 |
| Parenthetical openings | 3 – 14.5 per 1000 words | 11.9 | 12.3 | 14.2 | 10.7 |
| Em-dashes | ≤ 2.5 per 1000 words | 1.2 | 0.0 | 0.0 | 0.0 |
| Semicolons | ≤ 4.5 per 1000 words | 1.9 | 1.1 | 1.8 | 0.9 |
| Colons | ≤ 5.5 per 1000 words | 2.1 | 3.3 | 4.3 | 2.9 |
| Bold spans | ≤ 1.0 per 1000 words | 0.0 | 0.0 | 0.0 | 0.0 |
| Coined 3-part hyphenated compounds | ≤ 1.5 per 1000 words | 0.5 | 0.2 | 0.4 | 0.0 |
| "rather than" | ≤ 0.8 per 1000 words | 0.3 | 0.1 | 0.1 | 0.0 |
| *Connectives, per 1000 words — not gated* | *diagnostic* | *2.7* | *2.7* | *2.2* | *2.6* |
| *…of the nine in §4b, how many are used* | *diagnostic* | *9* | *7* | *7* | *6* |
| *Sentences with a mid-sentence ", so " — not gated* | *diagnostic* | *0.1 %* | *0.3 %* | *0.4 %* | *0.4 %* |
| *Sentences opening with a connective — not gated* | *diagnostic* | *4.8 %* | *6.1 %* | *4.2 %* | *3.7 %* |
| *Sentences with `, and ` + a second clause (regex, a floor) — not gated* | *diagnostic* | *3.4 %* | *1.1 %* | *1.3 %* | *3.1 %* |
| *Sentences with a mid-sentence `, not ` — not gated* | *diagnostic* | *0.2 %* | *0.0 %* | *0.1 %* | *0.0 %* |
| *Sentences with a passive construction — a BAND, not gated* | *diagnostic* | *56.9 %* | *64.0 %* | *62.9 %* | *60.1 %* |

The four human columns are what the sources actually measure. **Aim for those numbers, not
for the edge of the band.** The band is now the union of four house styles and no single
source writes at its edge: PDA TR 60 averages 24 words a sentence and ISPE PV averages 30,
so a document sitting at 30.5 is not "within the envelope" in any useful sense — it is
writing longer than the longest-winded of the four.

There was a `"therefore" ≤ 1.2 per 1000 words` row here until 2026-08-16. It was removed
because "therefore" had become the only connective the corpus still used, so the one rule the
gate had about connectives pushed down on the last one left. The last two rows replace it and
**fail nothing**: they are printed so the gap is visible. Across the 20 corpus documents the
median is 1.5 per 1000 words and 3 of the 9 connectives; the four sources sit at 2.2 to 2.7
and use 6 to 9. "However" occurs twice in the whole corpus and 59 times in the four sources.

The two clause-packing rows were added on 2026-08-17; the corpus measured 6–11 % and 0–2 % on
them, and round one of the register pilot made both worse. They fail nothing.

The three rows added on 2026-08-18 are what the project owner's reading of round two named, after
a round that had cleared every target above. None of them fails anything either. The passive row
is a **band**: the plans already sit inside it and a floor would push a genre that is already
right the wrong way. The first two come from `check_style.py`, which prints them on every run.
The passive comes from `uv run --extra discourse python authoring/check_discourse.py`, which
needs the optional parser; its denominator is the sentences that have a root and a subject, so
the same four sources read 54.3, 59.8, 59.6 and 58.4 % when every sentence is counted instead.
Compare your own document against the row above using the same command, not against those four
numbers.

The gate also rejects a short list of phrases that appear nowhere in either human source:
"stated first", "it is worth noting", "this warrants comment", "the distinction that matters
is", coined compound superlatives, and a handful of generic filler words. Run
`check_style.py -v` to see your own longest sentences and coined compounds.

For comparison, the A-Mab case study uses **no em-dashes at all** across 278 pages, and
about one semicolon per thousand words.

### 4b. The rules behind the numbers

**Use full stops.** The default way to add a qualification, an example or a contrast is a
new sentence. Not an em-dash, not a semicolon, not a subordinate clause. If you have
written a 45-word sentence, it is almost always two sentences.

**Do not overshoot into staccato.** This is the opposite failure, and it is just as
detectable. A document whose sentences are all 12 to 18 words reads like a checklist, not
like a scientist explaining a study. A normal technical sentence carries a subject, a
finding and one qualifying clause, and lands around 24 words. Roughly one sentence in ten
should run past 40 words, because some ideas genuinely need that.

**Vary sentence length deliberately.** A short sentence after two long ones is how
emphasis works in this register. If every sentence is 30 words, nothing stands out. If every
sentence is 15 words, nothing stands out either.

**Use parentheses.** Both sources average about 12 parenthetical openings per 1000 words:
`(Table 4.2)`, `(HCP)`, `(e.g. mixing, aeration, mass transfer)`, `(data are given in
Appendix C)`. A parenthesis is the natural way to attach a reference, a gloss or a list of
examples without breaking the sentence. Avoiding them entirely is its own tell.

**Do not coin compound modifiers.** Write "the step that sets the most quality
attributes", not "the quality-attribute-richest step". Write "host cell protein", not
"host-cell-protein". Hyphenate only where the term is already standard.

**Do not use bold for emphasis inside a sentence.** Neither source document does it. Bold
belongs to headings and to table labels.

**Say things once.** Do not restate a claim in fresh words for the sake of variety.
Repeating the same noun is normal in a technical document, and it is clearer than elegant
variation. Cross-references between sections should be explicit ("see §7"), not implied by
a rephrasing.

**Do not comment on your own rhetoric.** Never write "stated first", "it is worth noting",
"this warrants comment", "the distinction that matters is", "that is worth stating as a
finding rather than an omission". Just state the thing. `check_style.py` bans these
outright.

**Prefer plain connectives.** The human sources use these nine: "However", "Therefore", "In
addition", "For this reason", "Since", "Once", "As a result", "By contrast", "Consequently".
They rarely use "rather than", and almost never build "not X but Y" constructions.

This is the rule the corpus breaks hardest. "However" appears twice in twenty documents and
59 times in the four sources. Most documents run on "therefore" and "since" alone, which is
what makes a paragraph sound assembled rather than argued. The remedy is not to sprinkle the
other seven in: a connective typed to satisfy a count is a worse tell than a missing one.
It is to write the sentence that needs one — a concession, a contrast, a consequence — which
is what §2c licenses and what the moves catalogue in `REGISTER_EXEMPLAR.md` shows.

And say where the connective goes: at the head of the sentence, after the full stop that ends
the previous step. The sources open 3.7 to 6.1 % of their sentences that way; the corpus opens
0 to 2 %, and puts the same step after a comma instead (", so …" in 6 to 11 % of sentences).

**Prefer the shorter word.** "used" over "utilised", "about" over "approximately" when
approximating loosely, "shows" over "demonstrates" unless the evidence is strong enough to
earn "demonstrates".

**Tense and person.** Third person. Past tense for what was done, present for what holds.
Passive is fine where the object of study matters more than who did it — the sources use
it heavily.

**Register still varies by section.** An administrative subsection is three flat sentences.
A design-space justification is careful and complete. The section plan assigns the register.
Varying it is your job.

### 4c. Worked corrections

These are real sentences from the superseded first-pass reports, with the reason each
fails and a corrected version.

> ✗ It is the **design-space step** of the drug-substance process and the
> quality-attribute-richest characterization in the campaign.

Two coined compounds and a superlative that no human would write. Also bold mid-sentence.

> ✓ The bioreactor is the step at which the design space for the drug substance is
> defined. It forms more quality attributes than any other step in the process.

---

> ✗ Its conclusion, stated first: the step is well understood, and a response-surface model
> over the well-controlled culture parameters defines an operating region in which the
> glycan, charge-variant and aggregate CQAs remain within their acceptance limits across
> the characterized ranges.

Announces its own rhetoric, then runs to 45 words.

> ✓ The step is well understood. A response-surface model over the well-controlled culture
> parameters defines an operating region for the glycan, charge-variant and aggregate CQAs.
> Within the ranges characterized, all of these attributes remain inside their acceptance
> limits.

---

> ✗ That null result is worth stating as a finding rather than an omission: it both
> simplifies the control strategy — only pH and temperature need be held closely to govern
> high mannose — and keeps the three inactive factors in the knowledge space as evidence
> that the attribute is robust to them.

Self-commentary, an em-dash aside, a colon splice, and 46 words.

> ✓ The three inactive factors were retained in the knowledge space. Only pH and temperature
> need to be controlled closely to govern high mannose, which simplifies the control
> strategy. The absence of an effect from pCO₂, osmolality and duration is evidence that
> the attribute is robust to them over the ranges screened.

---

> ✗ High mannose — the very-high-criticality attribute that also carries the tightest
> commercial-scale capability — is the most sharply localized response of the five.

Appositive stacking between em-dashes, plus a coined superlative.

> ✓ High mannose is of very high criticality and carries the tightest commercial-scale
> capability of the five responses. It also depends on the fewest factors.

---

> ✗ That the step's own tightest capability nonetheless clears its limit with this margin is
> the quantitative form of the design-space claim.

An abstract restatement of something already said, with the subject buried in a clause.

> ✓ Even the tightest of these capabilities clears its limit with the margin given above.

---

## 5. Tables and figures

A table is evidence. Introduce it, then say what it shows.

The human sources do this plainly, and you should copy them. They write "The results are
summarized in Table 4.5" and then pick out the one or two rows that carry the argument.
They do not walk every row, and they do not append a significance clause to each one.

> The design space for this unit operation is fairly complex due to the interactions and
> non-linear behavior found in the DOE studies. First, a graphical depiction of the
> intersection between the response surface models in Table 3.16 and the limits in Table
> 3.17 is given in Figure 3.5. The shaded regions in these plots indicate the regions where
> the mean levels of the CQAs will exceed the acceptable limits or specifications. Notice
> that the limits on acidic variants and soluble aggregates are not exceeded within the
> ranges tested in the DOEs.
> — A-Mab case study

Emit tables through the helpers (`show(...)`, the `doe_report` table builders) so the
numbers are the model's. Never hand-type a table body.

Give every table a caption and label so `@tbl-id` cross-references resolve. The convention
is a caption line immediately after the code chunk:

```
: Caption sentence describing the table. {#tbl-id}
```

Equivalently, `print(": … {#tbl-id}")` as the last line of an `output: asis` chunk.
Figures carry their caption in the chunk's `#| fig-cap:` option.

---

## 6. The numbers rule (absolute)

Every measurement is a Quarto inline expression or a helper call. Never a typed number.
Use the names in the brief's helper inventory:

```
The step raised pool aggregate `{python} f"{agg_ratio:.1f}"`-fold ...
`{python} show(top_effects("cex", "aggregate_out_pct"))`
```

Identifiers are not measurements, and are written plainly: document IDs (`SOP-2003`,
`AMV-3010`, `RA-001`), guidance names (`ICH Q8`, `FDA 2011`), citation keys,
cross-reference labels (`@tbl-cqa`, `@fig-contours`) and coded factor levels (−1/0/+1).

If a number you need has no helper, write `<<NEEDS: description>>` inline and continue.
Never invent, estimate or recall a value. A `<<NEEDS:>>` marker tells the maintainer to
extend the generator; it is information, not a failure.

---

## 7. Anti-patterns

- **Padding to length.** Length comes from covering the material, not from inflating
  clauses. A section with few facts is correctly short.
- **Uniform paragraphs.** Paragraphs of near-identical length and shape are a strong signal
  of machine authorship. Vary them.
- **The mandatory significance coda.** Not every paragraph needs a closing sentence
  explaining why it mattered. See §2c.
- **Buried claims.** A paragraph whose point arrives last has the shape backwards.
- **Unbounded robustness.** "The step is robust" with no boundary is a defect.
- **Reviewer-blind prose.** If you cannot name the question a reviewer would ask about a
  passage, the passage is not doing regulatory work.
- **False precision.** Match significant figures to the helper's formatting.
- **Elegant variation.** Three different phrasings of the same attribute across one section
  makes the document harder to read, not richer.

---

## 7a. Ground every claim. Nothing is added to your document afterwards.

Every claim in the document is yours and every claim must be supported. If you are tempted to
write one of the anti-patterns in §7 — an unreferenced appeal to prior experience, a screening
result sold as a design space, an unbounded robustness claim — that is a defect in your text.

There is no later step that adds, weakens or corrects a claim. The corpus once carried a few
deliberately unsupported claims as labelled benchmark negatives, planted by the maintainer
after authoring. That failed: a claim written against a finished document contradicts the
prose around it instead of merely lacking support for itself. On a separate branch the idea
was rebuilt so that such a claim is **assigned in the author's brief before writing**, which
is the only way it can be part of the argument rather than an attack on it. Either way,
nothing is added to your document afterwards.

If your brief has no §5b, every claim you write must be grounded. The reasoning is in
`authoring/WEAK_CLAIMS.md`, and it is worth reading once: it is the clearest example in this
project of a defect that every automated gate passed.

What follows for you is simple. The document you produce is the document that ships. Steps
that run after you — the ground-truth annex, the rhetorical layer, the grounding check — only
build artifacts *around* your text and never change what it says. If a later grounding check
fails, the annex quote is re-anchored to your document, not the other way round.

---

## 8. Before you submit a section

1. Does the first sentence give the section's finding? Does each paragraph open with its
   point?
2. Is every number an inline expression from the inventory? Any bare numeral? Any
   `<<NEEDS:>>` you should flag?
3. Is each table introduced and interpreted?
4. Are the section plan's rigor obligations satisfied?
5. Read your longest sentence aloud. If you run out of breath, split it. Then read the
   section as a whole: if it reads like a list of short declarations, some of those
   sentences want joining back together with a connective or a parenthesis.
6. Count the em-dashes and semicolons in the section. If there is more than about one of
   each per page, rewrite them as full stops.
7. Would the assessor's most obvious objection to this section already be answered in it?

When the document is complete, run:

```
uv run python authoring/check_render.py pc_package/<DOC>_<uokey>.qmd --render
```

This gates on execution, on the absence of `<<NEEDS:>>` markers, on a real Quarto render,
and on the register targets in §4a.
