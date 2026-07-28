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

### 2d. A sentence

Begin with information the reader already has and end with the new information. Keep the
subject next to its verb. One sentence, one point; if a sentence carries two claims, make
it two sentences.

> ✗ A 1.4-fold increase in pool aggregate, which is consistent with the descending-edge
> mechanism described above and was also seen at bench scale, resulted from the highest
> load.
> ✓ The highest load raised pool aggregate 1.4-fold. This is consistent with the
> descending-edge mechanism described above, and it reproduces the bench-scale result.

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
prose and not literary prose. It is the register of the two published documents this
corpus is built on, both of which are in `refs/text/`:

- PDA Technical Report No. 60, *Process Validation: A Lifecycle Approach* (2013)
- *A-Mab: A Case Study in Bioprocess Development*, CMC Biotech Working Group (2009)

Read `authoring/REGISTER_EXEMPLAR.md` before writing. It is a collection of verbatim
passages from those two documents, arranged by the job each one does.

### 4a. The measurable targets

`authoring/check_style.py` measures these and **fails the build** if they are missed. The
thresholds are read off the two human documents above, and `check_style.py --selftest`
proves that both of them pass.

Several of these are **bands, not ceilings**. Writing that is too short and too choppy is
just as unlike a real regulatory document as writing that sprawls. Human technical prose sits
in the middle.

| Property | Band | PDA TR 60 | A-Mab |
|---|---|---|---|
| Mean sentence length | 20 – 28 words | 24.2 | 26.6 |
| Median sentence length | 18 – 25 words | 21.0 | 23.0 |
| Sentences over 40 words | 3 – 16 % | 9.8 | 13.4 |
| Sentences over 55 words | ≤ 7.5 % | 2.9 | 5.2 |
| Sentences under 15 words | 15 – 32 % | 20.5 | 19.5 |
| Parenthetical openings | 3 – 14 per 1000 words | 11.9 | 12.3 |
| Em-dashes | ≤ 2.5 per 1000 words | 1.2 | 0.0 |
| Semicolons | ≤ 4.5 per 1000 words | 1.9 | 1.1 |
| Colons | ≤ 5.5 per 1000 words | 2.1 | 3.3 |
| Bold spans | ≤ 1.0 per 1000 words | 0.0 | 0.0 |
| Coined 3-part hyphenated compounds | ≤ 1.5 per 1000 words | 0.5 | 0.2 |
| "rather than" | ≤ 0.8 per 1000 words | 0.3 | 0.1 |
| "therefore" | ≤ 1.2 per 1000 words | 0.3 | 1.0 |

The two human columns are what the sources actually measure. Aim for those numbers, not for
the edge of the band.

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

**Prefer plain connectives.** The human sources use: "However", "Therefore", "In
addition", "For this reason", "Since", "Once", "As a result", "By contrast", "Consequently".
They rarely use "rather than", and almost never build "not X but Y" constructions.

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

## 7a. Ground every claim, except the ones your brief assigns you

Every claim in the document is yours and every claim must be supported — with exactly one
exception, and only if your brief contains it.

**If your brief has no "Assigned weak claims" section, ground everything.** If you are
tempted to write one of the anti-patterns in §7 — an unreferenced appeal to prior
experience, a screening result sold as a design space, an unbounded robustness claim — that
is a defect in your text.

There is also no later step that adds, weakens or corrects a claim. These claims were once
planted by the maintainer *after* authoring, and that failed: a claim written against a
finished document contradicts the prose around it instead of merely lacking support for
itself. Assigning it in your brief beforehand is the only way it can be part of the argument
rather than an attack on it. The reasoning is in `authoring/WEAK_CLAIMS.md`, and it is worth
reading once: it is the clearest example in this project of a defect that every automated
gate passed.

**If your brief does assign weak claims (§5b), write those and nothing else ungrounded.**
They are labeled benchmark negatives: a grounding corpus needs known-bad examples, or it
only ever tests recognition of good prose. Your brief gives, for each one, the grounded fact
it distorts, what to assert instead, and where to put it.

Three things decide whether such a claim is worth anything:

- **Unsupported, not contradicted.** It must overreach beyond the evidence, not collide with
  a sentence three lines away. If a neighbour rebuts it, move the claim. Never weaken the
  neighbour and never delete a grounded statement to make room — that would trade a real
  finding for a fake one.
- **In register.** It must read like the rest of your document. A negative a reader spots by
  style rather than by checking the evidence tests nothing.
- **Unmarked.** Do not flag it, hedge it apologetically, or leave a comment. The label lives
  in the annex, not the text.

This is a deliberate reversal of an earlier rule, and the reason is instructive. These claims
used to be *planted after* authoring, and it failed: a claim written against a finished
document lands in prose that has already settled the question, so it reads as a
contradiction rather than an overreach, which is a much easier thing to detect. Writing them
into the argument in one pass is what keeps them honest negatives.
`authoring/WEAK_CLAIMS.md` has the full reasoning.

Otherwise the principle stands: the document you produce is the document that ships. Steps
that run after you — the ground-truth annex, the rhetorical layer, the grounding check —
build artifacts *around* your text and never change what it says. The maintainer will record
your exact wording for an assigned claim so the annex can label it; that step reads the
document, it does not edit it. If a later grounding check fails, the annex quote is
re-anchored to your document, not the other way round.

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
