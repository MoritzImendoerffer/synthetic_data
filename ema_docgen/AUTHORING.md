# Authoring contract

Stable reference. Read in full on every section task.

Defines: the rhetorical moves available, the constraints that always apply, and
the deferral and numeral rules.

---

## Part 1 — Constraints that always apply

**C1 — Numerals.** Every numeric value must be a Quarto inline expression
(`` `{python} ...` ``) or emitted by a helper call. Never write a bare number in
prose. If a value you need does not exist in the helper API, emit
`<<NEEDS: description of the value>>` inline and continue. Do not invent,
estimate, or round from memory.

Exempt from this rule, because they are identifiers rather than measurements:
document IDs (`SOP-2007`, `AMV-3104`, `PCR-005`, `RA-004`, `DEV-007-02`),
guidance names (`ICH Q8`, `PDA TR 60`), citation keys, and cross-reference
labels (`@tbl-cqa`, `@fig-contours`).

**C2 — Facts.** Use only facts present in the section's fact pack. Do not invent
incidents, dates, lot numbers, personnel, equipment IDs, or study outcomes.

**C3 — Deferral.** Never assert a result and defer with "data not shown" or
equivalent. Every deferral names a location: an appendix in this document, a
paired report, an SOP, or a method validation. A deferral without a destination
is a defect.

**C4 — Additivity.** You do not edit the document. You emit anchored insertions.
Anchors are copied verbatim from existing prose and must be long enough to be
unique. Never propose changing, rewording, or deleting existing text.

**C5 — Voice.** Third person, past tense for what was done, present for what
holds. Passive where convention favours it. No bullet lists where the document
uses prose. No headings beyond those the docspec assigns.

**C6 — Lexical independence.** Do not reproduce phrasing from source or
reference literature. The corpus must be lexically distinct from its sources;
overlap is checked mechanically.

---

## Part 2 — Register classes

Assigned per section in the docspec. Drives density and hedging, not topic.

| Register | Character | Typical length |
|---|---|---|
| `boilerplate` | Administrative, formulaic, minimal hedging | 100–300 |
| `procedural` | What was done, in order, with references to governing procedures | 300–900 |
| `analytical` | Statistical findings with mechanistic warrant | 600–2,000 |
| `argumentative` | Justifies a decision against alternatives | 800–2,500 |
| `defensive` | Anticipates and pre-empts challenge; heaviest hedging | 1,000–3,000 |

Real packages are uneven. A three-sentence section next to an eight-page one is
normal and desirable. Length comes from the docspec, never from your judgement.

---

## Part 3 — Move taxonomy

Each move: when it applies, its slot structure, the obligation it carries, and
one exemplar. Exemplars show *form*, including inline-expression style — copy
the pattern, not the content.

### Bounding and scope

```
MOVE: step_linkage
WHEN: opening of any unit-operation section
STRUCTURE: name adjacent steps -> input attribute states -> output attribute
           states -> mark unchanged attributes explicitly
OBLIGATION: every attribute in scope appears on both sides, or is explicitly
            marked unaffected
EXEMPLAR:
  The cation-exchange step receives the depth-filtered pool from low-pH viral
  inactivation and delivers the load to the anion-exchange polish. It is
  presented with material at `{python} f"{cex_in_conc:g}"` g/L and pH
  `{python} f"{cex_in_ph:.1f}"`, carrying aggregate at
  `{python} f"{cex_in_agg:.2f}"`% and HCP at `{python} cex_in_hcp` ng/mg
  (@tbl-link). Acidic variants are not modified by this step and are carried
  forward unchanged.
```

```
MOVE: explicit_non_claim
WHEN: the step plausibly has a capability for which no credit is taken
STRUCTURE: acknowledge capability -> state no claim is made -> name where the
           claim is taken instead
OBLIGATION: must name the step or document that does carry the claim
EXEMPLAR:
  Partial precipitation of host-cell protein is routinely observed during the
  low-pH hold and is removed by the subsequent depth filtration. Because the
  extent of this clearance is not predictable across the operating region, no
  clearance credit is claimed for it here; the HCP reduction attributed to this
  stage in the control strategy derives solely from the chromatographic steps
  (**PCR-005**, **PCR-007**).
```

```
MOVE: bounded_conclusion
WHEN: closing any results or design-space passage
STRUCTURE: state conclusion -> range bound -> model bound -> assumption bound
OBLIGATION: at least two of the three bounds present
EXEMPLAR:
  Over the ranges studied and under the conditions of the qualified scale-down
  model, the eluate-pool aggregate is controlled below
  `{python} f"{agg_acc_hi:g}"`% across the characterized region. This conclusion
  assumes the feed attribute states given in @tbl-link and does not extend to
  loads above `{python} f"{load.par[1]:g}"` g/L resin, which were not evaluated.
```

```
MOVE: attribute_carry_forward
WHEN: an attribute in scope is unaffected by the step
STRUCTURE: name attribute -> state it is unmodified -> state where it is
           controlled instead
OBLIGATION: must not silently omit an in-scope attribute
```

### Risk and study design

```
MOVE: conservative_default
WHEN: describing any scoring or classification rule
STRUCTURE: state rule -> state fallback when evidence absent -> note the
           fallback is the more demanding option
OBLIGATION: the fallback must be stated even if never invoked
EXEMPLAR:
  Where neither experimental data nor a documented mechanistic rationale was
  available to support a lower score, the parameter was assigned the highest
  impact ranking and carried into the multivariate study. No parameter was
  excluded from characterization on the basis of absent evidence.
```

```
MOVE: discretionary_band
WHEN: a scoring rubric has an intermediate range
STRUCTURE: name band -> state further assessment required -> state the default
           absent that assessment
OBLIGATION: must state which way the default falls
EXEMPLAR:
  Parameters scoring in the intermediate band were assessed individually against
  platform precedent to determine whether a univariate design was defensible.
  Where no such precedent could be cited, the parameter was assigned to the
  multivariate design by default.
```

```
MOVE: transferability_denial
WHEN: prior-product or platform data exists but is not relied upon
STRUCTURE: name available data -> name the property that differs -> conclude
           non-transferability -> state what was done instead
OBLIGATION: the differing property must be named specifically
EXEMPLAR:
  Resin lifetime data exist for three prior platform antibodies processed on the
  same matrix. Because carryover and fouling behaviour are governed by the
  host-cell protein profile of the feed, which is cell-line specific, these data
  were not treated as supporting the A-Mab claim. An independent cycling study
  was executed under **SOP-2011** and is reported in §7.4.
```

```
MOVE: factor_inclusion_rationale
WHEN: introducing any DoE factor table
STRUCTURE: per factor - range -> severity score -> expected interactions ->
           mechanistic rationale for the range chosen
OBLIGATION: the rationale must justify the RANGE, not merely the inclusion
EXEMPLAR:
  Protein load was studied over
  `{python} f"{load.par[0]:g}-{load.par[1]:g}"` g/L resin. The lower bound
  reflects the minimum economically viable cycle loading; the upper bound was
  set one third above the dynamic binding capacity determined at
  `{python} f"{res_time:g}"` min residence time, so that the onset of
  breakthrough falls inside the characterized region rather than beyond it.
```

```
MOVE: linking_variable
WHEN: a design incorporates a factor owned by an adjacent unit operation
STRUCTURE: name the linking variable -> justify why the link is credible ->
           describe how its levels were realised
OBLIGATION: must name the adjacent step and the document characterising it
EXEMPLAR:
  Harvest viability was included as a linking variable because the host-cell
  protein burden presented to this step varies with culture age (**PCR-004**
  §5.2). Its levels were realised using two clarified harvest pools drawn at
  `{python} harv_early` and `{python} harv_late` days of culture; centre points
  used an equal-volume blend of the two.
```

```
MOVE: permissive_inclusion_clause
WHEN: after any rubric that could read as over-restrictive
STRUCTURE: note low-scoring parameters may still be included -> state the
           benefit -> state it does not alter classification
OBLIGATION: must not weaken the rubric it follows
```

```
MOVE: scoring_rubric_definition
WHEN: a numerical risk score is first used
STRUCTURE: define the factors -> define the arithmetic -> define the bands ->
           map bands to experimental strategy
OBLIGATION: bands must be exhaustive and non-overlapping
```

### Result reporting

```
MOVE: null_result_to_classification
WHEN: a factor shows no significant effect
STRUCTURE: state finding -> state range over which it holds -> assign
           classification -> state it still informs the knowledge space
OBLIGATION: the classification must follow explicitly from the finding
EXEMPLAR:
  Load concentration produced no detectable effect on step yield, pool aggregate
  or pool HCP over
  `{python} f"{loadconc.par[0]:g}-{loadconc.par[1]:g}"` g/L (all p >
  `{python} f"{p_thresh:.2f}"`, @tbl-uni). It is accordingly classified as a
  general process parameter. The result is retained in the knowledge space as
  evidence that titre variability within this range does not propagate to the
  eluate pool.
```

```
MOVE: mechanistic_warrant
WHEN: immediately after any significant statistical effect
STRUCTURE: restate the effect qualitatively -> give the physical mechanism ->
           state what the mechanism predicts outside the tested range
OBLIGATION: must be falsifiable, not decorative
EXEMPLAR:
  Pool aggregate rises with both load and stop-collect volume, and the two act
  together. High-molecular-weight species carry greater net positive charge and
  elute later than monomer, so they concentrate in the descending edge of the
  peak; a heavier load broadens that edge and a later stop-collect samples more
  of it. The mechanism predicts the interaction will steepen further above the
  loads studied, which is why the operating region is bounded below the tested
  maximum.
```

```
MOVE: adverse_disclosure
WHEN: any result is worse than the comparator or the expectation
STRUCTURE: state the adverse finding with magnitude -> state mitigating
           evidence -> state the residual position
OBLIGATION: the adverse number must appear before the mitigation
EXEMPLAR:
  Leached Protein A in the Resin B eluate was consistently higher than for
  Resin A, by up to `{python} f"{lpa_ratio:.1f}"`-fold. The subsequent cation-
  and anion-exchange steps reduced it to `{python} f"{lpa_final:.2f}"` ng/mg,
  indistinguishable from Resin A material by the qualified assay
  (**AMV-3104**). The difference is therefore confined to the intermediate pool
  and does not reach the drug substance.
```

```
MOVE: worst_case_identification
WHEN: any multivariate response surface is described
STRUCTURE: name the corner -> name the response it maximises -> state whether
           it lies inside the operating region
OBLIGATION: must state the inside/outside position explicitly
EXEMPLAR:
  The worst case for pool aggregate is simultaneous high load, high elution pH
  and late stop-collect. This corner lies within the characterized region but
  outside the operating region defined in §8; at the NOR bounds the predicted
  aggregate remains below `{python} f"{agg_nor_max:.2f}"`%.
```

```
MOVE: table_narration
WHEN: any table is presented
STRUCTURE: introduce table -> walk the notable rows -> state why each is notable
OBLIGATION: a bare "as shown in @tbl-x" with no walkthrough is a defect
```

```
MOVE: assay_variance_attribution
WHEN: a response is close to its acceptance limit or effects are small
STRUCTURE: state total observed variance -> state assay contribution -> state
           the process-attributable remainder
OBLIGATION: must name the method validation carrying the precision estimate
```

```
MOVE: capability_margin_statement
WHEN: reporting process capability
STRUCTURE: state the index -> state the limit it is evaluated against -> state
           one-sided or two-sided -> attribute the margin across steps
OBLIGATION: must state which steps share credit for the margin
```

```
MOVE: cross_step_credit_allocation
WHEN: an attribute is controlled by more than one unit operation
STRUCTURE: state this step's contribution -> name the other contributing steps
           -> state which completes the reduction
OBLIGATION: must name the documents characterising the other steps
```

```
MOVE: deviation_disposition
WHEN: any deviation, excursion, excluded run or invalid analysis
STRUCTURE: describe -> investigate -> assess impact on the study conclusion ->
           disposition
OBLIGATION: impact on the study conclusion must be stated explicitly, even when
            nil
```

### Change and lifecycle

```
MOVE: expected_difference_concession
WHEN: a change produces a difference that could read as a problem
STRUCTURE: name the underlying property difference -> state the consequence ->
           normalise as expected -> state what was done to bound it
OBLIGATION: must not claim equivalence where difference exists
EXEMPLAR:
  Resin B is built on a different base matrix with a modified ligand sequence.
  Its design space is consequently not identical to that of Resin A, as would be
  expected for resins differing in hydraulics, dynamic binding capacity and
  sanitisation compatibility. A separate risk assessment (**RA-004**) was
  executed to bound these differences, and the multivariate study was repeated
  in full rather than bridged.
```

```
MOVE: forward_extensibility
WHEN: closing any post-launch change or alternate-source section
STRUCTURE: state the general case -> state the qualification set required ->
           state that no further claim is made now
OBLIGATION: must specify the study set, not merely gesture at one
EXEMPLAR:
  Additional Protein A resins may become suitable for the commercial process.
  Qualification of any such resin would require the study set described in
  §9.2 - triplicate mid-point comparison, a full multivariate characterization,
  a cycling study to the claimed lifetime, and pool hold stability. No claim is
  made here for any resin other than those named.
```

```
MOVE: modular_claim_reassessment
WHEN: a change touches an area covered by an existing modular claim
STRUCTURE: name the claim -> assess applicability -> state whether additional
           study was warranted -> state the outcome
OBLIGATION: applicability must be decided, not left open
```

```
MOVE: platform_robustness_warrant
WHEN: asserting a step is inherently robust
STRUCTURE: state the claim -> cite the platform history supporting it -> state
           the boundary beyond which it does not extend
OBLIGATION: must state a boundary; an unbounded robustness claim is a defect
```

```
MOVE: scale_down_qualification_warrant
WHEN: introducing a scale-down model
STRUCTURE: design basis -> matched attributes -> qualification method ->
           statistical result -> therefore-suitable conclusion
OBLIGATION: attributes that failed equivalence must be disclosed and justified
```

---

## Part 4 — PCR-008 is the reference implementation

`pc_package/PCR-008_aex.qmd` is the densest and most complete report in the
corpus and is written in the corpus's own voice. **Prefer it over the exemplars
above wherever it covers the same ground.** It carries no contamination risk,
because it is not derived from source literature.

In particular, read PCR-008 before writing:

| For | Read |
|---|---|
| `deviation_disposition` | §12 DEV-01 and DEV-02 |
| `adverse_disclosure` | DEV-01, on the invalidated first execution |
| `assay_variance_attribution` | DEV-02, on the verification-run sample size |
| `table_narration` | Screening: factor effects |
| `scale_down_qualification_warrant` | Materials and methods |
| `capability_margin_statement` | Process capability and robustness |

The exemplars in Part 3 remain useful for moves PCR-008 does not exercise —
`transferability_denial`, `expected_difference_concession`,
`forward_extensibility`, `modular_claim_reassessment`. Those cover lifecycle and
change-management topics the current corpus does not yet contain.

Moves still lacking an exemplar anywhere: `attribute_carry_forward`,
`permissive_inclusion_clause`, `scoring_rubric_definition`,
`cross_step_credit_allocation`, `platform_robustness_warrant`. Write these from
your own output once you have text you are happy with. Two exemplars per move is
the practical ceiling: one gets copied structurally, three crowds context.
