# Content review of the PCP-007 draft — before promotion

**2026-08-21, TASK-029 §4.** Batch B4, authored under the amended rule 4. §5c assigns **no**
registered discrepancy, so any inconsistency this review finds is a bug rather than a benchmark
item. Reviewed here is the **second** draft: the first was set aside before any review, because
sibling prose reached it through `authoring/DISCREPANCIES.md`
(`PCP-007.DRAFT.run1-siblingleak.md`). Fresh judges (`opus`), one return between them.

## Counts per question

| run | Q1 | Q2 | Q3 | Q4 | verdicts |
|---|---|---|---|---|---|
| 1 (as authored) | 13 (12 clear, 1 marginal) | 4 (1 marginal) | 4 (1 marginal) | 8 (6 clear, 2 marginal) | No · No · No · Yes |
| 2 (after one cycle) | 12 (1 mechanistic, 11 procedural) | 0 (1 table label) | 0 (1 near-miss) | 3 | No · **Yes** · **Yes** · Yes |

**Q2 and Q3 both converged to yes**, as they did for `PCP-003` in the same batch. Q1's row needs
reading rather than counting: of the twelve, **one** is a mechanism sentence whose direction slips
into the next sentence, and **eleven** are administrative, procedural, statistical or scheduling
uses of the listed words. The judge said so itself, unprompted: "If only mechanism-bearing clauses
are counted, the answer is yes with that single exception." It also recorded that nothing in the
document defers a mechanism past a colon or into the next sentence. Not promotable on all four by
the letter of the rule; the document proceeds to the batch's annex task under
`decisions.one_review_cycle`.

## The terminology flag that is not the author's invention

The judge flagged "assurance factor" and "break even point" as coinages. Both trace to
`config/parameters.yaml`, which is the source of truth this corpus is built on: the comment on
`ipc_limits.margin` calls the quantity the **assurance factor**, and supplies the reasoning that a
limit set at the ceiling "would leave the drug substance dependent on every downstream step
delivering its nominal clearance exactly". The author wrote what the config says.

This matters beyond one sentence. `PCP-008` has already produced a disagreement between two judges
over the neighbouring term "assurance margin", which one author removed and another kept, so the
corpus is already split on it. The flag was forwarded to the author with that provenance stated and
no instruction either way, because changing the term to satisfy a literature test could deepen the
split, and keeping it fails the test. Whichever the author chose is recorded in run 2.

## Run 1 — the judge's report, verbatim

Model: Claude Opus 5 (`claude-opus-5`). Read: all 29 pages of
`pc_package/PCP-007_cex.DRAFT.pdf`, in four page ranges, and nothing else.

### Question 1 — causal verbs that name no physical cause in their own clause

1. p5 §1 — "Their purpose is to establish how the parameters of the step act on the quality attributes it controls, to define the region over which those attributes meet their criteria, and to justify the ranges and the controls that will be applied in commercial manufacture (U.S. Food and Drug Administration 2011)." — Q1: "act on" carries no species, interaction or direction; it is a bare placeholder for a relation the study will supply.
2. p6 §2 obj. 2 — "To define the multivariate region over which the fitted models predict that every quality attribute the step governs meets its criterion." — Q1: "governs" is used as a bare relational label between step and attribute, with no charge, resin or buffer property in the clause.
3. p6 §2 obj. 3 — "To establish a proven acceptable range for each parameter against each attribute it governs, both with the rest of the step at target and with the rest of the step varying within its normal operating ranges." — Q1: same bare "governs"; nothing physical stands in the clause.
4. p10 §4.2 — "The size variant and impurity attributes it governs are formed upstream, at the production bioreactor and at the capture step, and this step clears them." — Q1: "governs" asserts a relation the sentence never grounds; the chemistry that would ground it sits a page earlier.
5. p10 §4.1 bullet 1 — "Load is therefore expected to act on aggregate clearance, on host cell protein clearance and on yield through one physical quantity." — Q1: "through one physical quantity" names an abstraction, not the ligand occupancy the two preceding sentences described.
6. p11 §4.2 — "Residual DNA and leached Protein A will be measured across the step so that their clearance is confirmed, and neither is treated as a response of the designed experiments, because the mechanism predicts a clearance that does not depend on the parameters under study." — Q1: the "because" cites "the mechanism" as an authority instead of naming charge repulsion of DNA or the acidity of Protein A.
7. p11 §4.3 — "4 parameters were assigned to the multivariate design, because prior knowledge links each of them to aggregate clearance, to host cell protein clearance or to yield, and because the mechanisms above predict that they interact." — Q1: both "because" clauses point at prior knowledge and at an earlier section, not at a species or interaction in the clause.
8. p11 §4.3 — "Elution flow rate was assigned to a univariate assessment, since its expected effect is small and acts through a different physical quantity from the other four." — Q1: "a different physical quantity" is a placeholder; residence time and peak sharpness are never named where the verb stands.
9. p14 §5.5 — "The purpose of the screening analysis is to identify which factors and which interactions act on each response." — Q1: "act on" is empty of physical content in its own clause.
10. p17–18 §6.4 — "The assessment will establish whether flow rate acts on the separation over the studied range, and it will support the range within which the parameter is controlled in manufacture." — Q1: "acts on the separation" names no mechanism or direction, though the following sentence supplies one.
11. p19 §7 — "The in-process criterion is the level this step's pool must meet, and the two are not the same number, because the pool is not the drug substance." — Q1: the "because" restates the main clause as its own reason; no physical cause at all. (Also fails Q4.)
12. p20 §7 — "A parameter that acts on performance but not on a quality attribute is a key process parameter, and one that acts on neither over the range studied is a general process parameter." — Q1: two uses of "acts on" as an undefined relation inside a classification definition.
13. p17 §6.2, marginal — "A full factorial was selected rather than a fraction, because the factor count is small and because the mechanisms in §4.1 predict interactions between protein load and each of the other three factors." — Q1: the second "because" defers to §4.1, though it does at least name the interacting parties.

Not counted: p7 §3 "The controlled procedures and method validations that govern the work are listed in Table 3.2" uses "govern" in the document-control sense, not the physical one. Statistical "since"/"because" clauses in §5.5 and §8 do name their cause in the clause (missing quadratic terms, the target-versus-NOR distinction) and pass.

### Question 2 — terms that are not terms of art

1. p19–20 §7 — "The assurance factor is what makes each of them an in-process control rather than a break even point at which the batch would depend on every downstream step delivering its nominal clearance exactly." — Q2: "break even point" is an economics metaphor, and "assurance factor" is not the literature's term (it is safety factor or safety margin).
2. p19 §7 — "Both in-process criteria were carried back from the drug substance criterion through the clearance the downstream steps deliver in the nominal train, and each was then divided by an assurance factor, 5 for aggregate and 3.2 for host cell protein." — Q2: first use of the coined "assurance factor"; "nominal train" is also a coinage rather than a standard phrase.
3. p10 §4.1 bullet 4 — "It is the direct handle on the trade between aggregate clearance and yield." — Q2: "handle" and "the trade" are engineering shop-talk, not chromatography terms.
4. p13 §5.2, marginal — "Chromatography is performed under ambient temperature control and temperature is not varied, because the platform operates the step within a narrow ambient band at both sites and the transfer introduces no difference in that control." — Q2: "narrow ambient band" is coined; the standard phrasing is a controlled ambient range.

Everything else checks out as standard: bind and elute mode, sulfonate ligand, isoelectric point, charge shielding, flow through, wash displacement, stop collect threshold, ascending and descending edge, plate count, peak asymmetry, column volumes, linear velocity, size variant, HMW, leached Protein A, face centred central composite, resolution IV, aliasing, pure error, lack of fit, predicted R², one sided capability index, ALCOA+, WC-CPP/CPP/KPP/GPP, knowledge space.

### Question 3 — mechanism sentences that cannot be disagreed with alone

1. p9 §4.1 bullet 1 — "Protein load sets the fraction of the ligand in use." — Q3: an arithmetic identity (load per litre of resin over capacity), so there is nothing to contest.
2. p10 §4.1 bullet 4 — "Elution stop collect decides how much of the descending edge of the elution peak enters the pool." — Q3: true by the definition of a stop collect threshold; it states no contestable physics.
3. p10 §4.1 bullet 4 — "It is the direct handle on the trade between aggregate clearance and yield." — Q3: "direct handle" is too vague to be denied; there is no proposition to reject.
4. p9 §4.1, marginal — "The impurity clearances of the step follow from the same chemistry." — Q3: a transition whose referent ("the same chemistry") is only recoverable from the previous paragraph.

The rest of §4.1, both mechanism paragraphs and the four bullets, holds up: the charge, binding, elution, resolution and pool-cut claims can each be denied on their own, and each names a direction.

### Question 4 — sentences that file the finding for the reader

1. p19–20 §7 — "The assurance factor is what makes each of them an in-process control rather than a break even point at which the batch would depend on every downstream step delivering its nominal clearance exactly." — Q4: renames the just-stated division by 5 and 3.2 as a category, and answers an objection nobody raised.
2. p19 §7 — "The in-process criterion is the level this step's pool must meet, and the two are not the same number, because the pool is not the drug substance." — Q4: a causal gloss defending a difference no reader had challenged.
3. p12 §5.1 — "It is the only estimate of experimental error the analysis uses, which is why the centre point replicate counts in §6 cannot be reduced without weakening every model adequacy statement that depends on them." — Q4: a trailing "which is why" that rebuts a proposal to cut replicates that the plan never raises.
4. p10 §4.1 — "At the particle size of the platform resin and over the range in Table 6.1, its effect on resolution is expected to be small, which is why it is assessed one factor at a time rather than in the multivariate design." — Q4: trailing clause that files the physical statement into a study-design decision inside the mechanism bullet list.
5. p10 §4.1 bullet 4 — "It is the direct handle on the trade between aggregate clearance and yield." — Q4: a trailing sentence that renames the preceding mechanism as a category.
6. p25 §12 — "The qualification of §5.1 compares the attributes that enter and leave the step, which is the comparison the conclusions rest on, and it does not compare the internal flow distribution of the two columns." — Q4: the inserted "which is the comparison the conclusions rest on" pre-files the gap as acceptable before the gap is stated.
7. p21 §8, marginal — "The proven acceptable ranges and the operating region of §7 answer different questions and will not be conflated." — Q4: instructs the reader how to hold the two apart before the distinction has been made.
8. p17 §6.3, marginal — "A face centred design was selected for that reason." — Q4: a filing sentence between the rationale and its elaboration; it adds nothing the neighbours do not carry.

### Answers for the document as a whole

1. **No** — 12 clear failures plus 1 marginal, concentrated in the objectives, §4.2/§4.3 and the study-purpose sentences; the §4.1 mechanism paragraphs themselves are clean.
2. **No** — "assurance factor", "break even point", "nominal train", "direct handle", "the trade", "narrow ambient band".
3. **No** — three definitional or vague sentences (two bullet openers and the "direct handle" closer), plus one weak transition; the remaining roughly two dozen are contestable.
4. **Yes** — 6 clear cases and 2 marginal ones, clustered in §7 (the in-process criterion discussion) and in the trailing "which is why" clauses of §4.1 and §5.1.


## Run 2 — the judge's report, verbatim

Model: Claude Opus 5 (`claude-opus-5`). A second fresh judge, not the run-1 judge and not the
author. Read: the revised 30-page `pc_package/PCP-007_cex.DRAFT.pdf` in four page ranges, and
nothing else in the repository.

### Question 1 — causal verbs that do not name a physical cause in their own clause

One mechanism sentence, where the physics is present but the direction is deferred:

- "Elution buffer pH sets the net charge on the antibody at the moment of elution." — Q1: the clause names the buffer property, the species and the property acted on, but no direction; the direction arrives only in the next sentence ("A higher pH within the studied range weakens binding and brings monomer and aggregate off the column earlier and closer together"). The parallel bullet passes because its verb is directional in place ("sets the ionic strength that shields the charge on the ligand and on the bound species"), as does "Elution flow rate sets the residence time of the antibody in the pores of the resin during elution, and a longer residence time lets the antibody equilibrate more completely with the mobile phase and so sharpens the elution peak."

Then a group of occurrences of the listed words that are administrative, procedural, logistical or statistical rather than mechanistic. Each names a real, checkable reason in its own clause, but none names a species, an interaction or a resin/buffer property, so each fails Q1 read literally:

- "The controlled procedures and method validations that govern the work are listed in Table 3.2." — Q1: "govern" in its administrative sense; no physical cause.
- "Buffer preparation, column packing and resin storage are held to platform specification and are governed by the procedures in Table 3.2." — Q1: same administrative "governed".
- "Chromatography is performed under ambient temperature control and temperature is not varied, because the platform operates the step at controlled room temperature at both sites and the transfer introduces no difference in that control." — Q1: the "because" gives a site/control fact, not a physical cause.
- "The elution buffer pH range stops short of the pH at which the antibody would no longer bind reproducibly, because a run at such a pH would confirm the mechanism and would tell the study nothing about the operating region." — Q1: the "because" gives a study-design reason, not a physical one.
- "The table carries no classification, because classification is an outcome of the study and will be reported in PCR-007 under SOP-4001." — Q1: procedural reason.
- "A full factorial was selected rather than a fraction, because the factor count is small and because protein load is expected to interact with each of the other three factors, through the peak broadening that rising ligand occupancy produces." — Q1: the first "because" is a design-arithmetic reason; only the second carries physics, and it does so in place.
- "It is not the predictive model of the step, since a model without quadratic terms cannot describe curvature, and the response surface model is the model from which the operating region, the proven acceptable ranges and the capability estimate will all be derived." — Q1: statistical reason.
- "The coefficient of determination, its adjustment for the number of terms in the model, and the predicted coefficient of determination computed from the prediction error sum of squares should lie close to one another, because a predicted value well below the adjusted value indicates a model that describes the runs it was built on and predicts poorly." — Q1: statistical reason.
- "It will in general return the narrower of the two ranges, because a setting that is acceptable with the rest of the step at target need not be acceptable when the rest of the step sits anywhere inside its normal operating ranges." — Q1: logical reason.
- "The univariate assessment of elution flow rate may run in parallel with either designed study, since it shares no material or equipment constraint with them." — Q1: scheduling reason.
- "Response columns are absent because no run has been executed." — Q1: bookkeeping reason.

Nothing anywhere in the document defers a mechanism past a colon or into the next sentence: the eight mechanistic "because"/"since" clauses all carry their species and interaction inside the clause, e.g. "Host cell protein, DNA and leached Protein A are cleared because they carry a net negative charge at the load pH and are therefore not retained by the sulfonate ligand", and "For aggregate the in-process criterion is the tighter of the two, because no step downstream of cation exchange dissociates high molecular weight species".

### Question 2 — non-terms-of-art

No prose failures. One borderline item, in a table cell rather than a sentence:

- Table 6.1, "Elution stop collect | OD desc." — Q2: "optical density" is a term of art, but the chromatography term for a pool-collection threshold is absorbance (AU/mAU) or percentage of peak maximum, which is what the prose itself uses ("both read as ultraviolet absorbance relative to the peak maximum"). Loose label, not a coined term.

Everything else checks out as literature usage: bind and elute mode, sulfonate ligand, isoelectric point, dynamic binding capacity, ligand occupancy, peak broadening, plate count and peak asymmetry, residence time, mobile phase, strip fraction, high molecular weight species, host cell protein, leached Protein A, size variant, enveloped and small viruses, face centred central composite design, resolution IV fraction, pure error and lack of fit, proven acceptable range, and the WC-CPP/CPP/KPP/GPP set from the A-Mab case study. No coined three-part compounds.

### Question 3 — sentences in mechanism paragraphs that cannot be disagreed with

None. One near-miss, listed for completeness:

- "Four expectations follow from that experience, and the multivariate design is built to test them." — Q3 near-miss: it announces rather than asserts, but it remains checkable against the design (both the count and the claim that the design tests them can be denied).

Every other sentence in §4.1, §4.2, §6.3, §6.4 and the §7 criterion paragraph states something a reviewer could deny, down to the summary lines: "Yield is lost at the two edges of the pool", "The step therefore clears leached Protein A by a modest factor", "Rising ligand occupancy is therefore expected to move aggregate clearance, host cell protein clearance and yield in the same direction, all three falling as load rises."

### Question 4 — sentences that tell the reader how to file the finding

- "The step therefore clears leached Protein A by a modest factor that is a property of the chemistry rather than of any parameter studied here." — Q4: the trailing clause re-files the clearance just stated into a category ("chemistry, not a study parameter") in the same breath as stating it.
- "Such a statement is bounded by the range studied and by the power the design carries, and PCR-007 will state it in those terms rather than as an absence of effect in general." — Q4: a trailing gloss on the finding in the preceding sentence, answering an objection ("you are claiming no effect exists") that no one in the document has raised.
- "They are identity and quality controlled inputs to this study rather than factors of it." — Q4: renames the preceding sentence's subject as a category, and repeats a categorization §1 has already made about the feed.

Three defensible near-misses I did not flag, because each states a decision rule prospectively rather than glossing a finding: "and the range will not be narrowed to manufacture a margin the data do not require"; "and the claim is bounded by that range and no wider"; "which the model qualification and the centre point performance will confirm rather than assume".

### Answers for the document as a whole

1. **No** — strictly. Every clause that makes a *mechanistic* claim names its cause in place, and no mechanism is deferred past a colon or into the next sentence. But one sentence ("Elution buffer pH sets the net charge on the antibody at the moment of elution") leaves its direction to the next sentence, and eleven occurrences of the listed words are administrative, procedural or statistical and name no physical cause at all. If only mechanism-bearing clauses are counted, the answer is yes with that single exception.
2. **Yes.** Every technical term in the prose is a term of art; the only loose usage is the table unit "OD desc." for a collection threshold the prose describes as ultraviolet absorbance relative to the peak maximum.
3. **Yes.** Every sentence in the mechanism paragraphs makes a claim that can be denied on its own.
4. **Yes**, three times, and rarely — the leached Protein A "property of the chemistry" clause, the "rather than as an absence of effect in general" gloss, and the "inputs to this study rather than factors of it" re-categorization.

## What the return fixed, and the one term it changed

The bare "act on" and "governs" are gone from every physical claim. The DNA and leached Protein A
non-response justification now cites repulsion by the sulfonate ligand across the studied
conductivity and pH instead of citing "the mechanism". "Protein load sets the fraction of the
ligand in use", an arithmetic identity, became a claim about approaching dynamic binding capacity
with all three responses degrading as load rises. The stop-collect bullet became the claim that
the tail is progressively richer in aggregate because monomer elutes ahead of it, and "the direct
handle on the trade" went with it.

The author reported one judgement it declined to make: the mechanism source and the seeded model
agree that a later stop raises pool aggregate, so it kept "stopping later or earlier" throughout
and did not map that onto the numeric direction of the OD threshold, which neither source
supports.

**The term that changed: "assurance factor" became "safety factor".** The author's reasoning, on
the record: a divisor applied to a calculated ceiling is called a safety factor throughout
bioprocess validation, whereas "assurance factor" appears only in an internal comment glossing a
config key. The value still flows from `CFG.ipc_limits[...]['margin']` through an inline
expression, so only the noun in the prose differs from the noun in the comment. This is a
deliberate divergence between the corpus vocabulary and the config's, recorded here rather than
settled, and it is a one-word revert if the owner prefers the config's term.

## Findings recorded, not acted on

- **The judge scoped question 1 itself, unprompted**, splitting mechanistic uses of the listed
  words from administrative and statistical ones and giving a second answer under that scope. That
  is now a repeated, independent result across judges and documents, not an inference from one.
- **"OD desc."** as the unit of the elution stop collect parameter is a loose label. It comes from
  the parameter table, so it is a corpus-wide item rather than this document's, and the prose
  around it is correct.
- One mechanism sentence still defers its direction to the next sentence, and three "rather than"
  or trailing-clause glosses survive. One cycle is spent, so they stand.

## Disposition

Run 1 was returned to the same authoring agent with the flagged sentences as what each lacks and
the four questions restated. No counts and no phrase to insert were passed, and the judge's
suggested literature terms were withheld so the author had to find them. One cycle only, so run 2
ends the review. Two questions read yes and two do not, and the document proceeds to the batch B4
annex task (TASK-030). Nothing is added to the document after this point.
