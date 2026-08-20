# Content review of the PCR-008 draft, attempt 2 — before promotion

**2026-08-20, TASK-042 §4.** The document is the second attempt at `PCR-008` under the same frozen
regime; attempt 1 (promoted on 2026-08-19) lost its blind reading to the round-zero text on
2026-08-20, and the owner chose re-authoring over reverting or accepting (D8).

Judge, run 1: fresh-context agent (`opus`, self-reported Claude Opus 5), given the four Content
questions of `authoring/REVIEW_CHECKLIST.md` verbatim and
`pc_package/PCR-008_aex.DRAFT.pdf` (48 pages), and told to read nothing else. The judge read all
48 pages.

## Run 1 — as authored (`PCR-008-attempt2.DRAFT.pre-review.qmd`)

**Q1 No · Q2 No · Q3 No · Q4 Yes.**

### Q1 — causal verbs whose own clause names no physical cause and direction

**Parameter-to-response mappings with the physics deferred or absent**

- "Load pH and equilibration and wash-1 conductivity set the host cell protein content of the flow-through pool." — Q1: "set" links a parameter name to a response name; the equilibrium and the two directions arrive only in the next two sentences.
- "Load pH and wash conductivity set the host cell protein content of the pool, load pH and load conductivity set both log reduction factors, and protein load and flow rate act on neither within the ranges a platform process uses." — Q1: three causal verbs in one sentence, none naming a species, an interaction or a direction in its own clause.
- "Equilibration and wash-1 conductivity sets pool host cell protein and has the second largest effect in the study." — Q1: "sets" with no ionic strength, no ligand, no sign.
- "Load conductivity governs both log reduction factors and is delivered by the preceding step and adjusted before loading." — Q1: "governs" with no shielding, no charge, no direction.

**"because" clauses that name a decision, a geometry or a design fact rather than physics**

- "Within that plane the boundary runs from low load pH and low wash conductivity to high load pH and high wash conductivity, because the two parameters trade against each other." — Q1: "trade against each other" restates the geometry; the shielding-versus-charge cause sits back in Section 5.4.
- "Flow rate was assigned to univariate assessment because the risk assessment ranked both its potential impact and its potential for interaction below the threshold for multivariate study." — Q1: the cause is a ranking, not a species or an interaction.
- "The second was selected, because one test covers both edges and because it acts on the attribute the limit protects instead of on a surrogate for it." — Q1: the agent of "acts on" is an assay and its object is an attribute; nothing physical acts on anything.
- "A wash at the equilibration buffer composition follows the load and is collected into the pool, so the wash conductivity acts on the same bed as the load." — Q1 (weaker): "acts on the same bed" names an object but no species, no interaction, no direction.

**Bookkeeping "governs" / "sets", naming scope rather than cause**

- "The step sets one critical quality attribute, which is given in Table 2.1."
- "The response-surface models for the three attributes the step governs explain between 0.898 and 0.934 of the variation in their responses and show no lack of fit against the centre-point pure error."
- "At commercial scale the one-sided capability index is 1.51 for the cumulative MVM clearance and 1.53 for the cumulative XMuLV clearance, which are the tightest of the attributes this step governs."
- "The three governed responses are described well by the quadratic model." — Q1 for all four: the verb marks ownership of a response, not a mechanism.

Everything in Section 2.1, the core of Section 5.4, and the mechanism paragraph of Section 13.1 passes cleanly — species, interaction and direction all stand in the clause ("A higher ionic strength shields the electrostatic interaction, weakens the binding of the more weakly charged host cell proteins and virus particles, and lowers clearance"; "Deamidation converts an amide side chain to a carboxylic acid, so it adds negative charge to the antibody").

### Q2 — terms that are not terms of art

- "Pool host cell protein rejects 14.4% of them and is the binding response." — Q2: "binding response" is the optimization sense of *binding constraint*, and it collides head-on with binding to the ligand in a chromatography report.
- "The design space covers 85.6% of the characterized region, and pool host cell protein is the response that binds it." — Q2: same coinage in the executive summary.
- "The shielding penalty is therefore smaller where the driving charge is larger, which is what a negative interaction term means here." — Q2: "shielding penalty" and "driving charge" are both invented; the literature has electrostatic shielding or screening, and net charge.
- "The interaction term is -6.6 ng/mg, about half the size of either main effect, and it is negative, so the penalty for high wash conductivity is smaller at high load pH than at low load pH." — Q2: "penalty" again as a quasi-technical noun.
- "The region is therefore bounded by host cell protein alone, and its principal plane is load pH against equilibration and wash-1 conductivity, which is the pair plotted in Figure 5.1." — Q2: "principal plane" belongs to optics, not to DoE or chromatography.
- "Load pH and wash conductivity carry the surface, with coded coefficients of -5.34 and 6.19 ng/mg per coded unit." — Q2: "carry the surface" is a metaphor standing where a term should; repeated on p20 as "the two viral panels carry the gradient".
- "The load pH and wash conductivity terms survive in both executions with the same signs, which is consistent with a mechanism that the deamidated load loaded further rather than changed." — Q2: "the load loaded further" is not an idiom of the field and the intended sense has to be reconstructed.
- "The two viral responses are judged against the step floors given in Section 7, which are back-calculated from the cumulative requirements." — Q2 (weak): "step floor" is a house shorthand for required log reduction.

The genuinely loaded vocabulary is correct throughout: quaternary amine ligand, polyanion, isoelectric point, asparagine deamidation, capsid, envelope, trailing edge, hold-up, plate count and peak asymmetry, edge of failure, orthogonal clearance mechanisms.

### Q3 — mechanism sentences that cannot be disagreed with on their own

- "The expected behaviour of each parameter follows from the same physical chemistry." — Q3: asserts derivability from an anaphor; there is no proposition to contradict.
- "The negative interaction between the two follows from the same picture." — Q3: same shape, opening the strongest mechanism paragraph in the report.
- "The mechanism connects the root cause to the observation." — Q3: pure scaffolding; it states that an explanation is coming, and nothing else.
- "Robustness at this step follows from the same models." — Q3: same tic outside 5.4.
- "The impact is bounded in two ways." — Q3: an announcement of structure, not a claim.

The rest of Section 5.4 and of Section 13.1 passes: each sentence there carries a definite, contradictable claim ("At a high load pH the acidic host cell proteins carry more negative charge, so a given increase in ionic strength removes a smaller fraction of the binding energy and clears less of the population back into the pool").

### Q4 — sentences that tell the reader how to file the finding

- "That value bounds the claim rather than defeating it." — Q4: renames a weak predicted R² as a bounded claim and settles the reader's reaction for him.
- "The shielding penalty is therefore smaller where the driving charge is larger, which is what a negative interaction term means here." — Q4: the trailing clause refiles a physical statement as a statistical category.
- "A lower pH in the bed during equilibration and wash weakens the binding of the acidic host cell proteins, so the affected run reports a higher pool host cell protein than the correct buffer would have given, which is the conservative direction for every conclusion drawn from it." — Q4: a clean mechanism sentence with a filing label bolted on the end.
- "Neither result is a marginal rounding." — Q4: rebuts a doubt nobody had voiced.
- "The step is robust in yield across the ranges studied, which is what flow-through operation is expected to give." — Q4: trailing clause files the result as the expected class.
- "The two log reduction factors reproduce to about 6.9 percent, which is normal for an infectivity titre read from a dilution series." — Q4: "which is normal for" pre-empts a reader who has not objected.
- "The predicted values are lower, as they must be with 28 runs and 15 coefficients, and the weakest of them is 0.394 for the MVM log reduction factor." — Q4: "as they must be" answers an objection before it exists.
- "Working at small scale is a requirement of the viral evaluation and not a convenience, because live virus cannot be introduced into the manufacturing facility (International Council for Harmonisation 2023a)." — Q4: "and not a convenience" defends against an accusation nobody made.
- "That corner is an edge of failure inside the knowledge space, and it is the reason the design space in Section 6 is smaller than the characterized region." — Q4: the prediction is restated as a category and then as a cross-reference.
- "Criticality is treated as a continuum (International Council for Harmonisation 2023b), so the attributes in Section 2 carry a level of criticality and the parameters in Section 9 carry a class, and neither is a binary label." — Q4: the final clause exists only to forestall a misreading.
- "The consequence for the rest of this section is that an effect on host cell protein of a few nanograms per milligram cannot be separated from the noise of the step, and none is claimed." — Q4 (weaker): instructs the reader how to carry the finding forward.
- "The finite capacity is real, and it appears as soon as the impurity burden of the load rises, which is what the first execution of the design showed and Section 13 reports." — Q4 (weaker): the trailing clause files the claim against another section rather than adding to it.

### Run 1 answers for the document as a whole

1. **No.** Most mechanism verbs are properly loaded, but a recurring class of "set" / "governs" maps a parameter name onto a response name with the species, the interaction and the direction deferred or missing, and three "because" clauses name a decision or a geometry instead of a cause.
2. **No.** "binding response", "shielding penalty", "driving charge", "principal plane", "carry the surface" and "step floor" are house coinages, and one of them collides with the chromatographic sense of binding.
3. **No.** Five sentences, including the opening sentences of two mechanism paragraphs, assert that something "follows from the same picture / physical chemistry / models" and carry no independently contradictable claim.
4. **Yes.** At least a dozen sentences append a category label, a normative direction or a pre-emptive rebuttal to a finding that had already been stated.

## Disposition after run 1

Returned to the same authoring agent in one message: the four questions restated and the flagged
sentences with what each lacks, in the judge's words. No count, no phrase to insert, no target.
The author revised in its own context and re-ran `check_render --render` and the pdf itself. It
reported twelve Q1 sentences rewritten (the physical ones given species, interaction and
direction in the clause; the bookkeeping "governs"/"sets" removed), the Q2 coinages replaced with
terms of art, four of the five Q3 scaffolding sentences deleted and the fifth made contradictable,
and the Q4 filing clauses deleted or converted into information. 437 sentences / 8788 words became
446 / 8981; 48 pages either way.

## Run 2 — after the one revision cycle (`pc_package/PCR-008_aex.DRAFT.qmd` as it stands)

Judge: a second fresh-context agent (`opus`, self-reported Claude Opus 5), same four questions
verbatim, the re-rendered 48-page PDF, nothing else.

**Q1 No · Q2 No · Q3 No · Q4 Yes.**

The judge's preamble: "The document is mostly good on all four questions. Most causal verbs in it
do carry a species, an interaction and a direction in their own clause — 'Yield is unchanged
across the ranges studied, because the antibody does not bind to the ligand at the load pH',
'Protein load has no effect on any response because the impurity mass a platform load carries is
far below the capacity of the bed for the bound species', 'Deamidation converts an amide side
chain to a carboxylic acid, so it adds negative charge to the antibody'. The flags below are the
exceptions."

### Q1 — causal verb without a physical cause and a direction in its own clause

- "The two parameters therefore act on one equilibrium from opposite sides." (Executive summary) — "one equilibrium" is anaphoric and "from opposite sides" is a spatial metaphor; no species, ligand or buffer property stands in the clause with the verb.
- "The two parameters therefore act on one binding equilibrium from opposite sides." (§2.1) — Same formula repeated; the physical content sits in the two preceding sentences, not in this clause.
- "Load pH and wash conductivity act on one equilibrium from opposite sides." (§5.4) — Third occurrence of the same formula; carries no species and no signed direction of its own.
- "The four multivariate parameters are the two that set the charge state of the system, load pH and load conductivity, together with the wash conductivity that acts on the same equilibrium and the protein load that determines the impurity mass presented to the ligand." (§2.3) — "acts on the same equilibrium" names neither a species nor a direction; "set the charge state of the system" gives no direction either.
- "The step sets the cumulative clearance of minute virus of mice, and it contributes to the clearance of xenotropic murine leukaemia virus, host cell protein, residual DNA and leached Protein A." (§1.1) — "sets" names no mechanism and no direction, and it contradicts Table 8.2, where the step supplies 4.71 of the 10.03 log10 cumulative MVM claim.
- "None was classified as a key process parameter or as a general process parameter either, because each of the five is linked to a critical quality attribute by a mechanism that this study either measured or bounded." (§9) — The "because" points at "a mechanism" without naming one.
- "Figure 7.1, Figure 7.2 and Figure 7.3 plot one attribute each against its governing parameter, which is the parameter with the largest main effect on it." (§7) — "governing" is defined by a regression statistic, not by a physical cause; the three figure captions then reuse "the governing parameter" with no definition at all.
- "Where the risk of falling outside the design space is low, because the parameter is easy to measure and easy to hold, it is classified as well controlled." (§9) — The "because" gives an instrumentation property.
- "Both viral indices are properties of the whole train and not of this step alone, because they are computed against cumulative requirements." (§8) — Arithmetic reason, no physical cause.
- "No effect estimate for flow rate is reported in Section 5, because flow rate was not a factor of either design." (§4.4) — Documentary reason.
- "Operating flow rate is not part of the region, because it was not a factor of the response-surface design, and it is controlled to its normal operating range." (§6) — Design bookkeeping.
- "The bias applies to every run of both designs, because the same collection rule was used throughout." (§13.2) — Procedural reason.
- "…a single perturbed run inflates the residual error of that design rather than biasing any one term, because every effect is a contrast over all runs." (§13.3) — Statistical reason.
- "The forward control already exists, because buffer release testing under SOP-2103 is what detected the error, and the batch record requires the release result before a buffer lot is used." (§13.3) — Procedural reason.
- "The robustness analysis in Section 7 is the answer to that, because it holds the ninety-five percent predictive interval inside the criterion instead of holding the mean inside it." (§11) — Statistical reason.
- "It is also the last opportunity to detect a host cell protein excursion, because no step downstream of anion exchange is credited with host cell protein clearance." (§10) — Reason is a filing credit, not a physical cause.

The judge's own qualification: "The last eight are procedural or statistical 'because's rather
than false mechanism claims; they are listed because the question is written without an exemption
for them."

### Q2 — terms that are not terms of art

- "A higher load pH moves more of the host cell protein population below its isoelectric point and into the bound fraction, and a higher ionic strength in the bed shields that interaction and lets the weakly bound part of the population through." (§5.4) — Inverts the standard relation: raising pH does not move a protein below its own pI; the pH moves above the pI.
- "The spiking model reproduces the load of the commercial step with virus added, and the spike itself raises the particle burden well above anything the process will meet." (§3.1) — "particle burden" is a coinage; the literature says viral load, virus titre or spike level, and "particle" in pharma reads as particulate matter.
- "…the in-process limit carries an assurance margin below that requirement so that the batch does not depend on the pool sitting exactly at its nominal value." (§6) — "assurance margin" is not a term of art; the field says safety margin, control margin or action limit.
- "Protein load had no significant effect on any response in this study, and on that evidence alone it would not be quality linked." (§9) — "quality linked" is a coined adjective.
- "Operating flow rate sets the residence time and is quality linked in principle, because a bound species that does not reach the ligand is not removed." (§9) — Second use of the same coinage.
- "One of them invalidated the first execution of both designs, which were re-executed in full on a requalified load, and the analysis reported here is the re-execution." (Executive summary; also §11 and §13.1) — Qualification applies to a scale-down model or a method, not to a load lot; the document's own correct word for the lot is "representative".
- "Those species are residual DNA, the acidic fraction of the host cell protein population, leached Protein A and virus particles, whose surfaces are acidic." (§1.1) — "acidic surfaces" used where the literature says an acidic isoelectric point or a net negative surface charge at the operating pH.
- "MVM behaves like XMuLV although it has no envelope and is much smaller, because the capsid is acidic at the load pH and binds by the same electrostatic mechanism." (§5.4) — Same conflation: "acidic" is a pI property, not a charge state "at the load pH".
- "The cross-step credit is given in Section 8." (§1.1) — "cross-step credit" is a local coinage; ICH Q5A(R2) speaks of cumulative clearance across orthogonal steps.

Passing: "quaternary amine ligand, flow-through mode, log reduction factor, edge of failure,
knowledge space, design space, NOR, PAR, WC-CPP, pure error, lack of fit, face-centred central
composite, TCID50, icIEF, polyanion, asparagine deamidation, modular clearance, orthogonal
mechanisms, hold-up, collection cut, plate count, peak asymmetry, linear velocity are all
standard."

### Q3 — sentences in a mechanism paragraph that cannot be disagreed with on their own

- "The two surfaces have the shapes the binding mechanism predicts." (§5.4, opening) — Names neither a shape nor a prediction; it is a verdict.
- "The two parameters therefore act on one equilibrium from opposite sides." (Executive summary; and the two variants in §2.1 and §5.4) — Restates the previous sentence in abstract terms.
- "The capacity of the bed is finite, and a load that carries more acidic species approaches it within the same protein load range." (§5.4) — The first clause is a truism.
- "Section 13 reports such a load." (§5.4) — A cross-reference sitting inside the mechanism paragraph.
- "The step is understood as one electrostatic equilibrium approached from two sides." (§11, opening) — Reports an understanding rather than a fact.
- "That understanding is consistent with the platform history described in Section 2, with the physical chemistry of ion exchange, and with the two independent designs executed here." (§11) — Specifies no prediction; unfalsifiable as stated.
- "This study therefore confirms and bounds the platform behaviour for A-Mab, and it is not an optimization." (§2.1) — A statement about the study's category, not about the step.
- "That corner is an edge of failure inside the knowledge space." (§5.4) — A relabel of the preceding sentence's prediction.
- "The mechanism given in Section 2 is the reason it was assigned this way." (§4.4) — Points at a mechanism instead of stating one.

### Q4 — sentences that tell the reader how to file the finding just stated

- "That corner is an edge of failure inside the knowledge space." (§5.4) — Renames the just-stated 31.9 ng/mg prediction as a category.
- "The two terms that made the first execution anomalous are absent from the requalified data, which confirms the root cause." (§13.1) — Trailing clause files the observation as confirmation.
- "The normal operating range in Table 4.1 lies inside the characterized region, and one corner of it lies outside the design space, which is the finding reported in Section 7." (§6) — Trailing clause renames the fact as "the finding reported in Section 7".
- "This is the result the first execution of the design did not give, and the difference between the two executions is the subject of Section 13." (§5.2) — Tells the reader where the result is to be filed.
- "This study therefore confirms and bounds the platform behaviour for A-Mab, and it is not an optimization." (§2.1) — Trailing clause assigns the study to a category.
- "It constrains the region more than a whole-train optimization would, and the constraint is accepted because the alternative makes the acceptable range of one step conditional on the operating point of two others." (§6) — Causal gloss defending a choice against an objection no reader has raised.
- "A model that fitted the design points but not the centre points would show as lack of fit, and none of the three does." (§11) — Pre-empts an objection nobody raised.
- "That is also why the low-pH step, which acts on the envelope, contributes nothing to the MVM claim." (§5.4) — Causal gloss answering a question the paragraph had not posed.
- "These are the two lowest capability indices reported in Section 8." (Executive summary) — Ranks the finding for the reader instead of stating anything new.
- "The MVM index is the tighter of the two and the lowest in Table 8.1." (§8) — Same ranking gloss repeated.
- "The host cell protein figure is the one that carries the argument above." (§7) — Instructs the reader which figure to weight.
- "The disposition therefore rests on the common offset argument, and the verification runs support it rather than carry it." (§13.2) — Renames the evidential role of the runs as a category; "the underlying caveat is honest and earned, but the sentence is a filing instruction."
- "The classification therefore rests on the bounded mechanism and on the demonstrated consequence of exceeding it, and not on an effect measured in the reported data." (§9) — Tells the reader how to weight the classification just given.
- "A significant lack of fit means the model form does not describe the data, whatever the coefficient of determination says." (§3.5) — Trailing clause answers an objection nobody has raised at that point.

### Run 2 answers for the document as a whole

1. **No.** Three repetitions of "act on one equilibrium from opposite sides", "acts on the same equilibrium", "sets the cumulative clearance", "governing parameter", and a "because … by a mechanism that this study either measured or bounded" all put a causal verb over an abstraction with no species and no direction in the clause; a further group of "because"s give procedural or statistical reasons rather than physical ones.
2. **No.** "particle burden", "assurance margin", "quality linked", "requalified load" and "cross-step credit" are coinages, and "isoelectric point" is used in an inverted sense in the §5.4 mechanism sentence.
3. **No.** The mechanism paragraphs in §2.1, §5.4 and §11 open or close on sentences that assert nothing independently contestable.
4. **Yes.** Fourteen sentences do this.

## Counts per question

| run | Q1 flagged | Q2 flagged | Q3 flagged | Q4 flagged | verdicts |
|---|---|---|---|---|---|
| 1 (as authored) | 12 | 8 | 5 | 12 | No · No · No · Yes |
| 2 (after one cycle) | 16 | 9 | 9 | 14 | No · No · No · Yes |

## Disposition

**One cycle only, per `AUTHOR-A-DOCUMENT.md` §4 and the task's acceptance.** The draft stands as
revised and goes to the blind reading (TASK-043) against the round-zero text. Nothing further is
added to it.

## Observations for the results page, not acted on here

1. **The cycle did not converge, and a second fresh judge on the revised text flagged more, not
   fewer, sentences in every question.** Part of that is a different reader; part is traceable to
   the revision itself, which introduced "act on one equilibrium from opposite sides" and repeated
   it in three sections, where run 2 flags it under Q1 and again under Q3. This is the second
   PCR-008 attempt whose review cycle was heavy, and attempt 1 lost its blind reading.
2. **Q1 has no exemption for procedural or statistical "because".** Run 2 says so itself and
   flags eight such sentences ("because every effect is a contrast over all runs") that are
   honest and correct. A question that flags correct prose trains the author toward removing it.
3. **Two substantive points, neither a register matter.** "The step sets the cumulative clearance
   of minute virus of mice" (§1.1) sits against `outputs/data/viral_clearance.csv`, where AEX
   supplies 4.71 of the 10.03 log10 cumulative MVM claim — although two sentences later the same
   paragraph says "this step does not carry the whole claim for either model virus", and §8 gives
   the split through the helper. And the §5.4 "moves more of the host cell protein population
   below its isoelectric point" phrasing is loose in the direction run 2 names; the same
   formulation was present in attempt 1, where run 1's judge cited the sentence as *passing* Q1.
   Neither is registered in `authoring/DISCREPANCIES.md`. Recorded here for the owner rather than
   patched, because nothing is added to a finished document and the cycle is one cycle only.
