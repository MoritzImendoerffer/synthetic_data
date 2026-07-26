# Writing a process-characterization report — the standard

This is the standard for authoring an A-Mab characterization **report** (`PCR-00N`)
in one pass, at full depth. Read it in full before writing any section. It is
written the way you would brief a strong graduate student: it tells you *who you
are writing for*, *how to structure an argument at every scale*, and *what rigor
a regulator expects* — and it expects you to internalise the reasoning, not
pattern-match a template.

You are the **sole author** of this document — hold the whole report in mind as
you write, so the arc, cross-references and restatement described below actually
cohere. Two grounded inputs support you:

- the **report brief** (`authoring/out/<DOC>.brief.md`) — the grounded facts for
  *this* unit operation (its role, CQAs, parameters, DoE structure, results
  helpers, seeded deviations) and the **helper inventory**: the exact inline
  expressions you may call. Every number you write comes from there.
- the **section plan** — the ordered sections, each with its rhetorical scaffold,
  the rigor obligations that apply, and a target length band. Write them in order.

---

## 1. Who you are writing for

An assessor at a regulatory agency reading a Biologics License Application. They
are a skeptical expert, short on time, reading to find the weak point. They will
skim topic sentences first and read closely only where they smell a problem.
Three consequences govern everything below:

1. **Answer first.** They should be able to read the first sentence of any
   section and the first sentence of any paragraph and already know your claim.
   Support follows the claim; it never precedes it.
2. **Anticipate the challenge.** Length in a real report is not padding — it is
   *defensive*. Every strong claim is followed by the bound, the alternative
   considered, or the residual risk acknowledged. If you can imagine the reviewer
   asking "but what about…", answer it before they ask.
3. **Never make them take your word for a number.** Every quantitative statement
   is traceable to the model. You do not type numbers (§6).

---

## 2. Structure at four scales

Good scientific prose is structured identically at every scale: **context first,
then the new thing, then what it means.** Four named tools, one per scale.

### 2a. The whole report — the arc (Schimel, *Writing Science*; the hourglass)

A 30-page report must read as one argument, not fifteen filing cabinets. Use the
**OCAR** arc / hourglass:

- **Opening (wide):** the product, the unit operation's role in the train, the
  regulatory basis. Start broad.
- **Challenge (narrowing):** which CQAs this step governs and why they are at
  risk here — the quality problem this characterization exists to bound.
- **Action (narrow):** prior knowledge and risk basis → scale-down model →
  study design → results → design space → capability → parameter classification.
  This is the body, at full technical depth.
- **Resolution (widening):** the contribution to the control strategy, the
  discussion, the conclusions. Widen back out to what the step now guarantees for
  the process.

The canonical section order (see the section spec) *is* this arc. Honour it: the
executive summary states the resolution up front (answer-first at document
scale); the body narrows to the studies; the control-strategy and discussion
sections widen again.

### 2b. A section — the argument (Minto **SCQA** / Pyramid Principle)

Open every section with **S-C-Q-A**, then deliver the answer's support:

- **Situation** — the stable, agreed context. What is known / currently
  controlled. (No tension yet.)
- **Complication** — what changed or what is uncertain: the risk, the gap, the
  reason this section exists.
- **Question** — the implicit question the Complication raises.
- **Answer** — your claim, stated **first**, then supported beneath it.

This is exactly the plan-side "current state → problem → planned measure", but in
a report the **Answer is a finding**, given up front and then evidenced.
Example skeleton for a results section:

> *(S)* The cation-exchange step is the principal aggregate polish in the train.
> *(C)* Its clearance depends on load and elution conditions whose interaction
> was not quantified at commercial scale. *(Q)* [implicit: does a robust operating
> region exist?] *(A)* A response-surface model over four factors defines a region
> in which pool aggregate remains below its limit across the characterized ranges;
> the evidence follows.

Support beneath the Answer is **MECE** — grouped, non-overlapping arguments, each
its own paragraph, ordered strongest first.

### 2c. A paragraph — **CCC** (Context, Content, Conclusion)

One paragraph = one point. Shape it:

- **Context** (topic sentence): what this paragraph is about, tying back to the
  section's Answer. A reader skimming only topic sentences must still get the
  argument.
- **Content:** the evidence — the effect, the table row, the diagnostic.
- **Conclusion:** what it means for the claim. Do not leave the reader to infer
  it.

Never open a paragraph with a number or a table reference. Open with the point.

### 2d. A sentence — reader-expectation (Gopen & Swan, *The Science of
Scientific Writing*)

- **Old before new.** Begin a sentence with information the reader already has
  (the *topic position*); put the new, important information at the end (the
  *stress position*). This is what makes prose feel like it flows.
- **Subject next to verb.** Do not bury a long qualifier between them.
- **One unit of discourse, one point.** If a sentence carries two claims, split
  it.

Worked before/after:

> ✗ "A 1.4-fold increase in pool aggregate, which is consistent with the
> descending-edge mechanism described above and was also seen at bench scale,
> resulted from the highest load."
> ✓ "The highest load raised pool aggregate 1.4-fold. This is consistent with the
> descending-edge mechanism described above and reproduces the bench-scale
> result."

(Old info — the load — leads; the new info — the effect — lands in the stress
position; subject and verb are adjacent; one point per sentence.)

---

## 3. The rigor overlay

Structure gives flow. Rigor is the domain layer on top — the obligations that
make the prose defensible to a BLA assessor. Apply the ones the section spec
lists; several apply everywhere.

- **Grounding.** Every number is an inline expression from the model (§6). Prose
  may state only what the data support.
- **Screening identifies; the response surface predicts.** State this. The
  screening design finds which factors matter; the **response-surface model is the
  predictive / design-space model.** Do not over-claim the near-saturated
  screening fit as predictive.
- **Bounded conclusions.** Close any results or design-space claim with at least
  two of: the *range* bound (the region studied), the *model* bound (what the
  model does/doesn't cover), the *assumption* bound (feed states, scale-down
  validity). An unbounded claim is a defect.
- **Hedging calibrated to evidence.** Strong effects with tight CIs: state them
  plainly. Small or non-significant effects near a limit: hedge, and attribute
  variance to the assay where relevant. Calibrate the verb to the evidence
  ("demonstrates" vs "is consistent with" vs "suggests").
- **Adverse before mitigation.** When a result is worse than the comparator or
  expectation, state the adverse magnitude **first**, then the mitigating
  evidence, then the residual position. Never lead with the reassurance.
- **Cross-step credit.** When an attribute is controlled by more than one step,
  state this step's contribution and name the documents for the others; never
  imply this step does it all.
- **Deferral names a location.** Never "data not shown". Every deferral points to
  an appendix, a paired report, an SOP, or a method validation.
- **Null results are informative.** A factor with no significant effect gets
  classified (general process parameter) and *kept in the knowledge space* as
  evidence of robustness — state that, don't just drop it.

---

## 4. Voice and register

- Third person; past tense for what was done, present for what holds. Passive
  where convention favours the object of study over the actor.
- Register varies **by section, deliberately** — an administrative sub-section is
  three flat sentences; a design-space justification is dense and defensive. The
  section plan assigns the register; do not flatten everything to one texture.
  Uniform paragraph rhythm across a document is the tell of synthetic prose — and
  because one author writes the whole document, guarding against it is **your**
  deliberate job, not the tooling's. Vary sentence length, paragraph size and
  section-opening moves as you go.
- No bullet lists where the document uses prose. Tables are narrated (see §5),
  never dropped in bare.
- Cite only from `references.bib` using existing keys.

---

## 5. Tables and figures

A table is evidence, not decoration. Introduce it, then **walk the notable
rows** and say why each is notable, then state the conclusion. A bare "as shown
in @tbl-x" with no walkthrough is a defect. Emit tables through the helpers
(`show(...)`, the `doe_report` table builders) so the numbers are the model's;
never hand-type a table body.

---

## 6. The numbers rule (absolute)

Every measurement is a Quarto inline expression or a helper call — never a typed
number. Use the names in the brief's helper inventory:

```
The step raised pool aggregate `{python} f"{agg_ratio:.1f}"`-fold ...
`{python} show(top_effects("cex", "aggregate_out_pct"))`
```

Identifiers are **not** measurements and are written plainly: document IDs
(`SOP-2003`, `AMV-3010`, `RA-001`), guidance names (`ICH Q8`, `PDA TR 60`),
citation keys, cross-reference labels (`@tbl-cqa`, `@fig-contours`), and coded
factor levels (−1/0/+1).

If a number you need has no helper, write `<<NEEDS: description>>` inline and
continue. **Never** invent, estimate, or round a value from memory. A `<<NEEDS:>>`
is information — it tells the maintainer to extend the generator — not a failure.

---

## 7. Anti-patterns (do not do these)

- **Padding to length.** Length is emergent from defensive completeness, not from
  inflating clauses. If a section is short because its facts are few, it is
  *correct* that it is short — do not stretch it.
- **Uniform paragraphs.** Varying paragraph and section length is realistic and
  required; do not make every paragraph the same size.
- **Buried claims.** A paragraph whose point arrives in the last sentence has the
  shape backwards.
- **Unbounded robustness.** "The step is robust" with no boundary is a defect;
  state the boundary beyond which robustness is not claimed.
- **Reviewer-blind prose.** If you cannot name the question a reviewer would ask
  about a passage, the passage is not doing regulatory work.
- **Number theatre.** Do not cite a precision you do not have; match significant
  figures to the helper's formatting.

---

## 8. Before you submit a section

Check, in order:

1. Does the first sentence state the section's Answer? Does each paragraph's
   first sentence state its point? (SCQA / CCC.)
2. Is every number an inline expression from the inventory? Any bare numeral?
   Any `<<NEEDS:>>` you should flag?
3. Does every table get narrated?
4. Are the section spec's rigor obligations each visibly satisfied?
5. Is at least one claim from elsewhere in the report restated here in different
   words, without contradiction? (Coreference is what makes the benchmark hard;
   it is also what makes a report read as one argument.)
6. Would the assessor's most obvious objection to this section already be
   answered in it?
