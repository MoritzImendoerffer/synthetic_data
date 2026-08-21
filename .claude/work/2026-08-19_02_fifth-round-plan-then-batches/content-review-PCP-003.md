# Content review of the PCP-003 draft — before promotion

**2026-08-21, TASK-028 §4.** Batch B4, authored under the amended rule 4. The production
bioreactor is the step with the most mechanism to carry, and this is the plan side of the pair
whose report was re-authored in B2. §5c assigns **D-001** (`protocol_method_statement`). Fresh
judges (`opus`), one return between them.

## Counts per question

| run | Q1 | Q2 | Q3 | Q4 | verdicts |
|---|---|---|---|---|---|
| 1 (as authored) | 21 | 8 | 9 | 15 | No · No · No · Yes |
| 2 (after one cycle) | 1 (2 borderline, not counted) | 0 | 0 (1 close call, not flagged) | 3 | No · **Yes** · **Yes** · Yes |

**Q2 and Q3 both converged to yes**, which only `PCP-010` had managed before, and it needed the
same one cycle. Q1 is down to a single sentence and Q4 to three instances of one construction.
Not promotable on all four by the letter of the rule; the document proceeds to the batch's annex
task, which is what `decisions.one_review_cycle` says happens either way.

## Run 1 — the judge's report, verbatim

Model: Claude Opus 5 (`claude-opus-5`). Read: all 31 pages of
`pc_package/PCP-003_bioreactor.DRAFT.pdf` and nothing else.

### Question 1 — causal verbs that name no physical cause in their own clause

**p.5** "Harvest and clarification, which recover the culture fluid and set the load presented to capture, are covered by PCP-004." — "set" asserts the load without naming what produces it or in which direction.

**p.6** "To define the multivariate region of the well controlled parameters over which every attribute this step governs is predicted to meet its acceptance criterion." — "governs" is a bare relation between a step and an attribute: no species, no interaction, no direction.

**p.6** "To establish a proven acceptable range for each parameter against each attribute it governs, and to confirm that the normal operating range in Table 6.1 lies inside it." — same hollow "governs"; the pattern repeats verbatim on p.20, p.21 (twice), p.23 ("every governed attribute") and p.27.

**p.9** "The culture environment sets cell growth, specific productivity and the post-translational state of the secreted antibody." — the agent is an abstraction ("the culture environment") and no direction is given for any of the three objects.

**p.9** "Culture pH, temperature, dissolved gases and osmolality act on the cell throughout the run, and the age of the culture at harvest decides how much of the harvested pool was made under late-culture conditions." — "act on the cell" names no target species, no interaction and no direction.

**p.9** "The mechanisms by which the culture environment acts on product quality are therefore known before this study begins, and the study confirms and bounds them rather than discovering them." — a sentence that asserts mechanisms are known while "acts on product quality" names none.

**p.9** "Because pH, temperature, dissolved carbon dioxide and osmolality all act on the same enzymes and the same donor pools, their effects on the glycans are expected to interact." — the because-clause names shared targets but not what any one parameter does to them, and no direction.

**p.9–10** "Culture pH and temperature set the rate of the chemical reactions, dissolved carbon dioxide and osmolality act on intracellular pH and on the sialylation machinery, and the culture duration sets the time at temperature." — three hollow verbs in one sentence: the reactions are unnamed, "act on" carries no direction, and "sets the time at temperature" restates the parameter.

**p.10** "The bioreactor sets that load and the downstream train clears it, principally at Protein A capture and at the two polishing steps." — "sets" assigns the load to a step instead of naming the species and the direction that produce it.

**p.10** "Culture pH sets intracellular pH and the ionic environment of the Golgi, and through them the activity of the glycosyltransferases and the rate of deamidation." — "sets" plus "through them" carries four causal links and gives a direction for none.

**p.10** "It also sets the net charge of the antibody in the culture fluid and hence its colloidal stability." — "sets" without direction; raising and lowering pH are not distinguished.

**p.10** "Culture duration decides how much late-culture antibody the pool contains and how far viability has fallen at harvest, so it is expected to act on the age-dependent glycans and on the impurity load more directly than any other parameter." — "act on … more directly than any other parameter" is a ranking, not a cause, and has no direction.

**p.10** "Dissolved oxygen acts weakly within the range studied, through energy metabolism and through the rate of transit in the Golgi." — "acts through" names two conduits and no species, interaction or direction; "weakly" is a magnitude, not a direction.

**p.10** "Initial viable cell concentration, basal medium concentration and nutrient feed volume act on growth and on titer, and are expected to act on product quality only through the supply of glycosylation precursors, which the feed strategy replenishes." — two "act on" clauses, neither with a direction.

**p.11** "Afucosylation and galactosylation are scored high because the mechanism of action of A-Mab is primarily antibody dependent cellular cytotoxicity, and core fucose governs binding to the Fc gamma receptor that mediates it." — "governs" names species and interaction but omits the direction; whether core fucose raises or lowers Fc gamma binding is left unsaid.

**p.12** "Each of them acts principally on growth and on titer, and each is expected to reach product quality only indirectly, so a study that varies one at a time supports the range it needs." — "acts principally on" with no direction, and "reach product quality only indirectly" names no route.

**p.18** "That limitation is accepted here because interactions of three culture parameters are not expected from the mechanisms in §4.1, and because the subset carried into the response surface design is re-estimated there in a design that has no such alias." — the physical reason is a cross-reference to another section, not present in the clause.

**p.19** "The condition is accepted for these 4 parameters because RA-001 ranked their potential for interaction below the threshold for multivariate study, and because the mechanisms in §4.1 place them on growth and titer rather than on the glycosylation machinery." — the first "because" names a scoring decision, the second again defers to §4.1.

**p.20** "No numeric threshold for the coefficient of determination is set in this plan, because the value that constitutes adequacy depends on the noise of the response, and the lack of fit test measures adequacy against that noise directly." — a statistical justification, not a physical cause (defensible in context, listed for completeness).

**p.22** "An interval that is met at the set-point but broken elsewhere in the characterization range will be reported as the contiguous interval and the break described, because a range with a gap in it is not a range a batch record can carry." — the "because" names a documentation constraint, not a physical cause.

**p.26** "The phases run in the order shown, because each one depends on the output of the one before." — the because-clause restates the ordering rather than causing it.

*For contrast, these pass cleanly and show the document can do it:* "Terminal galactose is added by a galactosyltransferase from UDP-galactose, and both that donor and the manganese cofactor of the enzyme are depleted late in a fed-batch culture." (p.9); "High mannose species are those on which trimming and the later additions never proceeded, so their level is expected to rise when transit through the Golgi is fast relative to the processing enzymes or when those enzymes are inhibited." (p.9); "Carbon dioxide accumulates in a large vessel because the path length for stripping is longer…" (p.13); "Viability falls late in a fed-batch culture, so a longer culture carries a larger burden of both into harvest." (p.10).

### Question 2 — terms that are not terms of art

**p.9** "the post-translational state of the secreted antibody" — the literature term is post-translational modification; "state" is a coinage.

**p.10** "act on intracellular pH and on the sialylation machinery" — sialylation is described in the literature by sialyltransferase activity, CMP-sialic acid supply and sialidase release, not by a "machinery".

**p.10** "Culture pH sets intracellular pH and the ionic environment of the Golgi" — "ionic environment of the Golgi" is a vague paraphrase for Golgi luminal pH and Mn²⁺ availability.

**p.10** "it is expected to act on the age-dependent glycans and on the impurity load more directly than any other parameter" — "age-dependent glycans" is not a glycan class in the literature; it is invented shorthand.

**p.13** "Carbon dioxide accumulates in a large vessel because the path length for stripping is longer" — CO₂ stripping is described by kLa, gas residence time and hydrostatic head; "path length for stripping" is coined.

**p.20** "A study whose design is invalidated by a deviation will be re-executed in full on requalified material, and the invalidated dataset will be retained and referenced in PCR-003 rather than analysed." — material is released or re-tested; qualification applies to the scale-down model, not to material.

**p.24** "Run records will be captured in the validated execution system, and analytical results will be reported from the validated methods of Table 5.1 with their audit trail intact." — the term of art is a manufacturing execution system or an electronic batch record.

*Minor:* "the chromatographic steps of the platform train" (p.5) — the standard term is platform process.

Everything else checks out: core fucose, GDP-fucose, UDP-galactose, manganese cofactor, fucosyltransferase, galactosyltransferase, high mannose, asparagine deamidation, glycated lysines, colloidal stability, antibody dependent cellular cytotoxicity, Fc gamma receptor, knowledge space, design space, proven acceptable range, WC-CPP, resolution V, face centred central composite, pure error, lack of fit, ALCOA+ wording — all standard.

### Question 3 — mechanism sentences that cannot be disagreed with on their own

**p.9** "The culture environment sets cell growth, specific productivity and the post-translational state of the secreted antibody." — no magnitude and no direction, so there is nothing an opponent could contradict.

**p.9** "…and the age of the culture at harvest decides how much of the harvested pool was made under late-culture conditions." — true by definition of "late-culture".

**p.9** "These are the variables the step controls, and they are the variables this study varies." — a restatement of the preceding list; no claim is made.

**p.9–10** "Culture pH and temperature set the rate of the chemical reactions, dissolved carbon dioxide and osmolality act on intracellular pH and on the sialylation machinery, and the culture duration sets the time at temperature." — the third clause is a tautology and the first two carry no direction to dispute.

**p.10** "Culture pH sets intracellular pH and the ionic environment of the Golgi, and through them the activity of the glycosyltransferases and the rate of deamidation." — "sets" without a direction cannot be shown wrong by any result.

**p.10** "Osmolality stresses the cell, slows growth and shifts the balance of the nucleotide sugar pool." — "shifts the balance" names no direction, so that third clause survives any outcome.

**p.10** "Culture duration decides how much late-culture antibody the pool contains and how far viability has fallen at harvest, so it is expected to act on the age-dependent glycans and on the impurity load more directly than any other parameter." — the first half is definitional.

**p.10** "Initial viable cell concentration, basal medium concentration and nutrient feed volume act on growth and on titer, and are expected to act on product quality only through the supply of glycosylation precursors, which the feed strategy replenishes." — "act on growth and on titer" is unfalsifiable as stated.

**p.10** "The mechanisms above give the following expectations for the individual parameters." — a signpost inside a mechanism paragraph; nothing to contest.

### Question 4 — sentences that tell the reader how to file the finding

**p.9** "These are the variables the step controls, and they are the variables this study varies." — renames the preceding list as a category instead of adding a claim.

**p.9** "The mechanisms by which the culture environment acts on product quality are therefore known before this study begins, and the study confirms and bounds them rather than discovering them." — the trailing clause files the whole study as confirmatory.

**p.9** "Where prior knowledge is used in place of a study, it is used to justify a range rather than to claim a value." — a defensive rule answering an objection nobody raised.

**p.10** "The net direction in which any one parameter moves the acidic variants is not predictable from the chemistry alone, and the fitted model is what the report will read it from." — the trailing clause tells the reader where to look rather than stating anything.

**p.10** "The scale is a continuum rather than a binary split, so an attribute of moderate criticality is still controlled and still reported." — a causal gloss pre-empting a misreading nobody proposed.

**p.11** "Reporting them here as measurements of the load, without a model, is what the data will support." — renames the reporting choice as a category and justifies it in advance.

**p.11** "No parameter of this step was left unstudied, which reflects the position of the bioreactor in the train rather than any doubt about the platform." — the clearest instance: a causal gloss rebutting a doubt nobody voiced.

**p.13** "A model qualified on mean performance and a design that measures its own reproducibility are two different claims, and this plan makes both." — files the two preceding statements into categories and closes the paragraph on the filing.

**p.15–16** "That statement is bounded twice." — a meta-instruction telling the reader how to read the claim just made.

**p.16** "The simulation inherits the bounds of the models it uses, so it is an estimate at scale-down and not a measurement at commercial scale." — the trailing clause renames the result as a category.

**p.18** "The axial runs sit on the faces of the cube, at the edges of the characterization ranges rather than beyond them, so no run is executed outside the region this plan claims to cover." — the "so" clause answers an objection nobody raised.

**p.21** "The classification is an outcome of the study and is not anticipated in this plan." — a pure filing statement.

**p.21** "The report will state the Cpk for each attribute with its margin to the limit and will name the attribute whose capability is tightest, which is the quantity a reader needs in order to judge the step." — the trailing clause instructs the reader how to use the number.

**p.22** "The second answers what it does while the rest of the process moves as it will move in routine operation, and it is the analysis that carries the interactions." — trailing category assignment.

**p.23** "The plot shows where the boundary of acceptability sits relative to the range in which the process runs, which a tabulated interval does not." — defends the plot against an objection nobody raised.

### Answers for the document as a whole

1. **No.** Roughly twenty causal verbs — concentrated in §4.1, and every "governs" in §2, §7, §8 and §12 — name a target but no direction, or defer the physical reason to §4.1 or to RA-001. The document proves it can do better in the glycan paragraph on p.9 and the CO₂ paragraph on p.13.
2. **No.** Seven or eight coined phrases sit among otherwise correct terminology: "post-translational state", "the sialylation machinery", "the ionic environment of the Golgi", "age-dependent glycans", "path length for stripping", "requalified material", "validated execution system".
3. **No.** Nine sentences in the mechanism paragraphs of §4.1 are definitional or directionless, most sharply "the culture duration sets the time at temperature" and "the age of the culture at harvest decides how much of the harvested pool was made under late-culture conditions".
4. **Yes.** Fifteen sentences do this, and the "X rather than Y" trailing gloss is a recurring tic; the worst is "which reflects the position of the bioreactor in the train rather than any doubt about the platform" (p.11).

## Run 2 — the judge's report, verbatim

Model: Claude Opus 5 (`claude-opus-5`). A second fresh judge, not the run-1 judge and not the
author. Read: all 31 pages of the revised `pc_package/PCP-003_bioreactor.DRAFT.pdf` and nothing
else.

### Question 1 — causal verbs that do not carry the cause in their own clause

- p. 11, §4.2: "Afucosylation and galactosylation are scored high because the mechanism of action of A-Mab is primarily antibody dependent cellular cytotoxicity." — fails Q1: the because-clause names a mode of action but no species-level link and no direction; the physical chain (core fucose → FcγRIIIa affinity → cytotoxicity) arrives only in the next sentence.

Borderline, not counted as a failure:

- p. 10, §4.1: "Sialic acid is transferred by the sialyltransferases from CMP-sialic acid, and glycation adds glucose to lysine residues without an enzyme at a rate set by the residual glucose in the medium." — "set by" names the species (residual glucose) and the site (lysine residues) in place, but leaves the direction implicit in the word "rate".
- p. 20, §7: "No numeric threshold for the coefficient of determination is set in this plan, because the value that constitutes adequacy depends on the noise of the response, and the lack of fit test measures adequacy against that noise directly." — a statistical, not physical, cause; named in place, and the sentence makes no mechanistic claim.

Every other instance carries cause and direction in the clause itself (e.g. p. 13 "Carbon dioxide accumulates in a large vessel because the liquid height raises the hydrostatic head and lowers the volumetric mass transfer coefficient for carbon dioxide stripping."; p. 19 "because the nutrient feed holds the nucleotide sugar precursors in excess across the ranges studied"; p. 22 "because the level leaving the bioreactor is the level presented at release."). There are no colon-deferred causes anywhere in the document, no "since", no "governs", and no "acts on"/"acts through".

### Question 2 — non-standard terminology

No sentences flagged. Every technical term is attested: GDP-fucose, UDP-galactose, the manganese cofactor, Golgi luminal pH, core fucose, high mannose, asparagine deamidation, CMP-sialic acid, glycation of lysine residues, isoelectric point, FcγRIIIa, ADCC, volumetric mass transfer coefficient, hydrostatic head, terminal electron acceptor, icIEF, 2-AB HILIC-UPLC, SEC-HPLC, resolution V, face centred central composite, PRESS-based predicted R², one-sided Cpk. The QbD-specific labels ("knowledge space", "well controlled critical process parameter", "Tool #1 score") are A-Mab / ICH Q8 terms and are used with their cited sources. No coined compounds.

### Question 3 — sentences in mechanism paragraphs that cannot be disagreed with

No sentences flagged. Each sentence in §4.1, §4.3 and the CO2 paragraph of §5.1 states something a reviewer could contradict on its own, including the interaction claims ("The amount by which raising one parameter moves a glycan attribute is therefore expected to depend on the levels of the others.") and the negative claims ("The culture is not oxygen limited at either edge of the range in Table 6.1, so neither the specific growth rate nor the glycan distribution is expected to move measurably across it.").

Closest call, not flagged: p. 9, "The harvested pool is the integral of everything the culture secreted during the run, so a longer culture weights the pool toward antibody made after the nucleotide sugar donors have been drawn down and after viability has begun to fall." — the first clause is true by construction, but the sentence as a whole asserts a contestable weighting.

### Question 4 — sentences that file the finding they have just stated

- p. 18, §6.2: "The screening design also cannot separate a two factor interaction from an interaction of three factors, which is the price of running a half fraction." — fails Q4: the trailing clause renames the limitation just stated as a category ("the price of a half fraction") and adds nothing testable.
- p. 29, §14.2: "The axial runs are set at −1 and +1, which is what makes the design face centred." — fails Q4: the trailing clause re-labels the setting just given with the term that defines it.
- p. 12, §4.3: "They bound the response of each attribute outside the region the process should occupy, which is what allows the severity of an excursion to be assessed." — weakest of the three: same "which is what …" shape, glossing the just-stated fact with its use, though the paragraph did announce that it was giving reasons.

All three are the same construction, and it appears nowhere else in the document.

### Answers for the document as a whole

1. **No** — one sentence (p. 11, the ADCC scoring rationale) puts the physical link and its direction in the following sentence rather than in the because-clause. Every other instance passes, and nothing is deferred behind a colon.
2. **Yes.**
3. **Yes.**
4. **Yes** — three trailing "which is …" glosses, on pp. 12, 18 and 29.

## What the return fixed

The eight-sentence block of hollow "sets / acts on" expectations became seven paragraphs each
carrying a direction: higher culture pH raises intracellular and Golgi luminal pH and lowers the
antibody's net positive charge; dissolved carbon dioxide lowers cytosolic pH and drives base
addition that raises osmolality; a longer culture lowers viability and lowers galactosylation
while raising the host cell protein and DNA burden. The bare "governs" relation is gone from the
objectives, the acceptance criteria, the proven acceptable range section and the design space
discussion, replaced by what the fitted model actually contains. Of the run-1 terminology flags,
the author found every literature term without being given one: "path length for stripping" became
hydrostatic head and the volumetric mass transfer coefficient, and run 2 quotes that same sentence
as an example of Q1 passing cleanly. "Rather than" fell from 12 occurrences to 1, the substantive
CPP versus WC-CPP contrast.

The author reported one self-caught regression: it first wrote CMP-N-acetylneuraminic acid, which
pushed the coined-compound tic off zero, and switched to the standard CMP-sialic acid.

## Disposition

Run 1 was returned to the same authoring agent, in its own context, with the flagged sentences as
what each lacks and the four questions restated. No counts and no phrase to insert were passed;
for question 2 the flagged coinages were named but the literature terms the judge supplied were
**withheld**, so the author had to find them. One cycle only, so run 2 is the end of the review.

Two questions read yes and two do not. The document proceeds to the batch B4 annex task
(TASK-030) under `decisions.one_review_cycle`, which sends a document on either way because the
blind reading, not the review, is the test. The residual items are recorded here rather than
fixed: one because-clause whose physical chain sits in the next sentence, and three "which is …"
trailing glosses. Nothing is added to the document after this point.
