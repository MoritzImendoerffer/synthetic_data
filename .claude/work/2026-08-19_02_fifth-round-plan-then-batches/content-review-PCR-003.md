# Content review of the PCR-003 draft — before promotion

**2026-08-20, TASK-015 §4.** Batch B2, authored under the amended rule 4 of `WRITING_GUIDE.md`.
The production bioreactor has a DoE (`report_doe`), and §5c of the brief assigns **D-002**, the
`unsupported_absolute` registered discrepancy. Two fresh judges (`opus`, self-reported Claude Opus 5
both times), the four Content questions verbatim, the rendered PDF and nothing else, one return in
between.

## Run 1 — as authored (`PCR-003.DRAFT.pre-review.qmd`, 55 pp)

**Q1 No · Q2 No · Q3 No · Q4 Yes.** Flags: Q1 20, Q2 8, Q3 11, Q4 30 — the heaviest run-1 load of
the campaign.

Q1: bare "sets"/"governs" for register relations ("The step sets 7 of the drug substance quality
attributes"), placeholders standing where a cause belongs ("they are governed here through the
culture conditions that release them"), mediators named without a direction ("Culture pH acts on all
three through intracellular pH"), anaphora ("Both parameters act on the same machinery."), and two
tautologies ("because the cells are the same cells").

Q2: "machinery" and "sialylation machinery", "post-translational state", "intermolecular
attraction", "integral of viable cells", "cofactor conditions", "assurance margin".

Q3: eleven — self-sealing openers, promises about later numbers, and two glosses that use a result
as its own confirmation ("which is what a shared intracellular mechanism predicts", "Both are
additive, which is what independent mechanisms give").

Q4: thirty, in three groups — trailing renames, causal glosses answering unraised objections, and
six the judge called "pre-emptive disclaimers that instruct the reader what not to conclude".

## Disposition after run 1, and a conflict recorded before the return was sent

Returned to the same authoring agent in one message: the four questions restated, the flagged
sentences with what each lacks in the judge's words, the judge's replacement terms stripped. No
count and no verdict was sent.

**The six "pre-emptive disclaimers" are content this project requires.** "A factor with no
significant term in any response is reported as having no demonstrated effect over the range
studied, which is a statement about that range and not about the parameter in general" is rule 6 of
`WRITING_GUIDE.md` ("Say where a claim stops"). "The screening models are therefore read for the
size, the direction and the significance of effects, and nothing in this report predicts from them"
is CLAUDE.md's framing rule ("the screening model identifies effects; the response-surface model is
the predictive/design-space model. State this"). The return was sent unfiltered anyway, because
filtering it would be the session overruling the reviewer, and the author holds the guide.

**The author converted them to fact instead of deleting the content**, which is the better answer
than either compliance or refusal. The framing rule now reads: "A 19-run screening design identified
the active factors and their interactions, and a 28-run face-centred central composite design in the
four factors carrying the largest effects produced the predictive models used for the design space
and the proven acceptable ranges." Scope limits survive as "over the range studied" in six places
and as the raw-materials sentence in §3. Verified in the rendered text after the revision.

**The revision found two substantive errors, not register defects.**

1. "The two parameters have the same sign … which is what a shared intracellular mechanism
   predicts" was **false**. A higher pCO2 lowers cytosolic pH while a higher culture pH raises it,
   so a shared intracellular-pH account predicts *opposite* signs. The paragraph now says
   base-catalysed deamidation alone would give culture pH the opposite sign, names the sialylated
   and glycated species the fraction also carries, and states that the three contributions were not
   measured separately.
2. "Both are additive, which is what independent mechanisms give" is now the testable fact: no
   culture pH × culture duration interaction on aggregate reaches significance, with the coefficient
   table cited.

The author also reports checking **every new direction against the fitted coefficients before
asserting it**, and dropping one it would otherwise have written — a rise in culture pH speeding the
sialyltransferase, which predicts the wrong sign against the fitted −2.01. And it revised eight
sentences the judge had not flagged that carried the identical defect, so the fix is consistent
rather than spot-applied.

467 sentences / 10,269 words became 453 / 10,005. The mechanism paragraphs got longer and the
document got shorter, because the filing sentences went. 55 pages both times.

## Run 2 — after the one revision cycle

**Q1 No · Q2 Yes · Q3 No · Q4 Yes.** Flags: Q1 6 mechanism-claiming (+ a bookkeeping family of
about five), Q2 0, Q3 6, Q4 7.

### Q1 — six, all of one shape: the direction withheld to the next sentence

- "The pH, the temperature, the dissolved gases and the osmolality of the medium set the rate at which the cells grow, the antibody each cell secretes and the post-translational modifications that antibody carries."
- "The activity of those enzymes, the supply of the donors and the residence time of the glycan in the Golgi therefore set the fraction of antibody that leaves the cell without core fucose and the fraction that leaves galactosylated."
- "Culture duration acts on the harvested pool rather than on the cell."
- "Culture pH sets how fast the galactosyltransferase works and culture duration sets how much of the pool that enzyme made while its donor was still plentiful…" — "sets how fast" names the enzyme but withholds whether rising pH speeds it or slows it.
- "Culture pH sets how fast the galactosyltransferase and the fucosyltransferase work, through the pH of the Golgi lumen in which both enzymes sit."
- "Culture duration sets how much of the harvested pool those enzymes made after their UDP-galactose and GDP-fucose donors had been drawn down."

Plus a bookkeeping family with no physical cause available at all — the design-space and PAR
definitions, and "Table 2.1 lists the quality attributes this step sets".

The judge's counter-examples, where the sign travels with the verb: "High mannose is governed by
culture pH (+1.09, p < 0.001) with a smaller contribution from culture temperature." and "High
mannose carries the highest Tool #1 score of the group at 80, because high mannose species clear
faster from the circulation and the exposure relationship carries the larger uncertainty."

### Q2 — clean

"Nothing flagged. Every technical term is standard in the cell-culture, glycobiology, chromatography
or DoE literature." The judge lists biantennary glycan, fucosyltransferase, galactosyltransferase,
mannosidases, GlcNAc transferase, UDP-galactose, GDP-fucose, manganese cofactor, Golgi lumen,
cytosolic and intracellular pH, asparagine deamidation, sialylated glycans, glycated lysines,
isoelectric point, effector function, volumetric oxygen mass transfer coefficient, specific
productivity, integral of viable cell concentration, resolution V, aliased, saturated model, PRESS,
predicted R², pure error, lack of fit, one-sided Cpk. It notes that the only near-coinages,
"propagated range" and "the propagated analysis", are defined where introduced in §7.

### Q3 — six

"A parameter that raises deamidation may lower the sialylated fraction at the same time…" (the modal
makes it a bare possibility) · "One result was not predicted." (a signpost) · "The mechanisms by
which the culture parameters act on the glycan attributes are established for the platform." (a
provenance claim) · "The interaction between culture pH and culture duration on the two glycan
attributes is the central result of the study." (a ranking) · and the two trailing "so neither
parameter can be set without reference to the other" clauses.

### Q4 — seven

Trailing clauses converting a result into a control rule ("…so neither parameter can be set without
reference to the other", "…and the two parameters are controlled together rather than
independently"), a gloss true by arithmetic ("A model with a predicted R² of 0.60 describes a new
observation less well than one at 0.92."), two glosses on numbers already reported, "The univariate
ranges in Table 7.1 and the multivariate region in §6 are two views of the same models…", and the
Tool #1 "rather than in a binary class" defence, which the judge notes is the second time the
document makes it.

## Counts per question

| run | Q1 | Q2 | Q3 | Q4 | verdicts |
|---|---|---|---|---|---|
| 1 (as authored) | 20 | 8 | 11 | 30 | No · No · No · Yes |
| 2 (after one cycle) | 6 (+ a bookkeeping family) | 0 | 6 | 7 | No · **Yes** · No · Yes |

## Disposition

One cycle only. The draft stands as revised and goes to the batch annex step with B2.

**D-002 is carried untouched** through both runs: the absolute claim stands verbatim and unqualified
in §1.1, its authorized elaboration follows, nothing later reconciles it, and leached Protein A is
never mentioned in the document (grep-verified at zero). Neither judge flagged it, which is what a
registered discrepancy is supposed to do — it is a benchmark item for a *content* review of the
corpus, not a register defect.
