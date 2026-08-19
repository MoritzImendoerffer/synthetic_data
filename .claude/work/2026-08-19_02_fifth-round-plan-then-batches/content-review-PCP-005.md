# Content review of the PCP-005 draft — before the reading

**2026-08-19, TASK-002 §4.** Judge: fresh-context `general-purpose` agent, model override `opus`
(self-reported Claude Opus 5), given the four questions of `REVIEW-BEFORE-PROMOTION.md` and
`pc_package/PCP-005_protein_a.DRAFT.pdf` (31 pages) and nothing else.

## Run 1 — on the draft as authored (`PCP-005.DRAFT.pre-review.qmd`)

Document answers: **Q1 No (8) · Q2 No, narrowly (4) · Q3 No (3) · Q4 Yes (9).**

**Q1** (§4.1 unless stated): "The 4 parameters carried into the multivariate design act through
these mechanisms."; "Protein load … acts on host cell protein and on yield through the same
physical quantity, which is the fraction of the bed capacity in use."; "Elution buffer pH sets how
completely and how fast the interaction between the Fc and the ligand is disrupted." (no
direction); "…elution pH is expected to be the parameter that most directly sets pool host cell
protein." (a ranking, not a cause); "Operating temperature acts on the diffusion coefficient of the
antibody and on the strength of the hydrophobic contacts … both effects are small" (no direction,
and not recoverable); "The 2 parameters assessed one at a time act more weakly."; §4.2 "…because
the level handed to the cation exchange step sets what the remaining polishing steps must achieve";
§5.1 "The model preserves the quantities that govern the chromatography." Passing, for
calibration: "because binding at the ligand is limited by diffusion into the pores of the bead";
"a lower pH acts by driving the residual affinity of the complex down further and by protonating
the carboxylate contacts that remain". Documentary uses of *governs* ("is governed by SOP-2008")
counted out of scope.

**Q2**: *assurance factor* and *the undivided ceiling* (§7); *governed attribute* / *governing
parameter* (§§2, 7, 8); *carboxylate contacts* (§4.1 — weakest; **this phrase is in
`authoring/mechanism/protein_a.yaml`, `elution_ph`, and reached the author through brief §2b**);
*cycle history window* (§5.1, minor).

**Q3** (§4.1): "DNA behaves differently."; "The 4 parameters carried into the multivariate design
act through these mechanisms."; "The 2 parameters assessed one at a time act more weakly."

**Q4**: §4.1 "…which is why the study is designed around the ranges the parameters may take at
commercial scale rather than around the identification of new effects."; "…so an interaction
between protein load and elution pH is expected on mechanistic grounds and not merely as a
possibility the design must cover."; "Within the range of 10 to 30 cm it is a property of the
packing rather than of the chemistry."; §4.2 "The outcome is a continuum of criticality rather
than a binary split (…), and an attribute of low or moderate criticality is still measured, still
controlled and still reported." + "Leached Protein A is such an attribute."; §5.4 "Distributing
them is what makes a drift in the system separable from the pure error of the system, since a
drift then appears as a trend across centre points in run order."; §5.5 "Coding puts the factors
on a common scale, which is what makes the estimated effects comparable between parameters
measured in different units."; §7 "The assurance factor is what makes the limit an in-process
control rather than a break-even point, since a limit set at the undivided ceiling would leave
the drug substance dependent on every downstream step delivering its nominal clearance exactly.";
§7 "…and the balance between them belongs in the report rather than in a limit."; §8 "…which is
exactly what an interaction means."

## The return to the author (once)

The lists above, minus counts and verdicts, sent to the run's author in its own context as what
each sentence lacks. Run 2 below.

## The author's revision (same context, 1 check_render pass, 31 pages, 259 → 262 sentences, 5,750 → 5,785 words)

Every named sentence changed and nothing else except three neighbours the replacements forced (the
DNA sentence rewrap, the §5.1 list after the deletion, "the multivariate region governs" → "takes
precedence"). §4.1 parameter paragraphs now carry species and direction in the verb's own clause
("Raising it fills a larger fraction of the binding capacity of the bed, which extends the mass
transfer zone toward the column outlet…"; "Lowering the elution buffer pH weakens the interaction
between the Fc and the ligand further and releases the antibody sooner"); *assurance factor* →
safety factor; *governed attribute / governing parameter* gone throughout; *carboxylate contacts*
→ "the acidic side chains that form the remaining hydrogen bonds and salt bridges"; the nine Q4
tails removed. `grep -c 'assurance factor\|governed attribute\|carboxylate contacts\|undivided
ceiling'` → 0.

## Run 2 — on the revised draft (fresh judge, self-reported Claude Opus 5, quotes re-extracted with pdftotext)

Document answers: **Q1 Yes · Q2 Yes · Q3 Yes · Q4 Yes — the fault present, 5 sentences.**

| question | run 1 | run 2 |
|---|---|---|
| Q1 | 8 | **0** mechanism failures ("every causal claim about the process passes"); listed but not counted: an anaphoric "The two effects act on yield in opposite directions" (the cause sits in the sentence before, not after), "The precision of an assay sets a floor on the effect a study can resolve" (an assay, not the process), administrative *governs* with an SOP as agent |
| Q2 | 4 | **0** — "Every technical term is standard"; closest to a coinage *characterized space*, built transparently from "characterized range" |
| Q3 | 3 | **0** — "All 46 sentences of §4.1 make a checkable claim" |
| Q4 | 9 | **5** — §4.1 "Characterization confirms and bounds them for this molecule rather than discovering them."; §4.2 "The outcome is a continuum of criticality rather than a binary split (…)."; §7 "It states no outcome, and every criterion below is fixed before the data are generated."; §12 "…and that assumption is tested by the qualification of §5.1 rather than taken on trust."; §12 "…which the case for prior knowledge in that section justifies by mechanism." |

**Disposition: not promotable on content by the checklist's letter** (Q4 reads "the fault is
present"), **and the reading proceeds** on the one-cycle output as the plan says. Three of four
questions clean after one cycle, against `PCR-007` where none of the four was.

Finding for the results page: the phrase *carboxylate contacts* reached the author from
`authoring/mechanism/protein_a.yaml` (`elution_ph`), which says "protonating the carboxylate
contacts that remain". The regime is frozen in this unit; the file is corrected at ship, recorded.
