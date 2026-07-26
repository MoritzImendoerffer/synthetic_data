# Register exemplar — the corpus voice, distilled

Short "gold" excerpts in the corpus's own voice, each annotated with the rhetorical
**move** it teaches. Together they let you write in-register **without any report open in
front of you** — they replace "read PCR-008 as the exemplar."

The excerpts are drawn from the densest report (the anion-exchange report, Step 8). They
are **AEX-specific**: study them for the *shape of the move*, the *sentence rhythm*, and
the *way a number appears as an inline expression* — then write your step's own
sentences. **Do not paste these sentences or reuse AEX's facts.** Every number you see in
backticks (`` `{python} ...` ``) is pulled from the model; that mechanic is the point,
the specific expression is not.

How to read each entry: **Move** = the rhetorical job · **Excerpt** = the gold ·
**Imitate / Avoid** = how to carry it to your step.

---

## 1. Answer-first executive summary (SCQA at document scale)

**Move.** Open the whole document with its resolution: what the step is, its role, the
study basis — then the outcomes, stated as findings, each bounded, with the capability
and its margin. The assessor learns your conclusion in the first paragraph.

> This report documents the Stage 1 (Process Design) characterization of the A-Mab
> anion-exchange (AEX) polishing chromatography step (Step 8), the **flow-through**
> polishing operation that follows cation-exchange polishing and is the **final
> chromatographic step** of the purification train. […] anion exchange is the step at
> which the process **establishes the minute-virus-of-mice (MVM, parvovirus)
> viral-clearance claim** — the CQA it sets — and it provides orthogonal enveloped-virus
> (XMuLV) clearance and a major further reduction of host-cell protein (HCP) […]

**Imitate:** name the step, its position in the train, and the one thing it *sets*, up
front. **Avoid:** starting with methods or history; burying the outcome.

---

## 2. Bounded outcome bullets in the summary (findings, not promises)

**Move.** The key-outcomes list states each result as a bounded finding with its number
inline and its limit named — never an unbounded "the step is robust."

> Anion exchange sets the cumulative **MVM (parvovirus) clearance** claim, contributing
> approximately **`{python} f"{AEX_MVM:.1f}"` log₁₀** at the nominal condition — the first
> and principal MVM-clearance step — so that the drug substance meets its ≥
> `{python} f"{mvm_acc_lo:g}"` log₁₀ cumulative MVM requirement (achieved cumulative
> **`{python} f"{MVM_TOTAL:.1f}"` log₁₀**, Cpk = `{python} f"{mvm_cpk:.2f}"`).

**Imitate:** claim → contribution (inline) → requirement (inline) → achieved + Cpk
(inline). **Avoid:** a bullet with no bound, or a typed number.

---

## 3. Screening identifies; the response surface predicts

**Move.** State the division of labour explicitly, so the near-saturated screening fit is
never over-claimed as predictive.

> A `{python} n_scr`-run two-level full factorial screening design identified the
> significant factors and two-factor interactions […]; a `{python} n_rsm`-run
> face-centred central-composite response-surface design then quantified main effects,
> interactions and curvature and defined the multivariate operating region in the
> well-controlled CPPs.

**Imitate:** "screening identified … the response-surface design then quantified … and
defined the operating region." **Avoid:** calling the screening model predictive.

---

## 4. SCQA section opener (situation → complication → answer-as-finding)

**Move.** A section opens with agreed context, then the tension, then the claim first.

> Flow-through anion-exchange polishing is a platform operation whose behaviour is well
> established from related humanized IgG1 antibodies (X-Mab, Y-Mab and Z-Mab) and from
> A-Mab clinical and engineering experience [@amab2009]. Prior knowledge established that,
> in flow-through mode, impurity and virus binding is governed by the electrostatic
> environment: a higher load pH increases the net negative charge of the impurities and
> virus, strengthening their retention […]

**Imitate:** ground the section in platform prior knowledge, then state the mechanistic
expectation the study will confirm. **Avoid:** opening a section with a result or a table.

---

## 5. Table narration (walk the notable rows, then conclude)

**Move.** A table is introduced, its notable rows are walked with *why each matters*, and
a conclusion is drawn. A bare "@tbl-x" is a defect.

> The flow-through-pool HCP is governed by the load pH and the equilibration/wash-1
> conductivity, which act in opposite directions — a higher load pH lowers the pool HCP
> (better clearance) and a higher wash-1 conductivity raises it (poorer clearance) — with
> a significant load-pH × conductivity interaction (effect `{python} f"{AB_EFF:.1f}"` ng/mg,
> p < 0.001) that means the conductivity matters most at low load pH. Notably, the protein
> load […] have **no** significant effect on the pool HCP in this representative-load DoE
> […]. The step yield shows no significant dependence on any factor […].

**Imitate:** name the governing factors and directions, cite the key effect inline, then
the null result and what it means. **Avoid:** printing a table and moving on.

---

## 6. Null results are informative

**Move.** A non-significant factor is classified and *kept in the knowledge space* as
robustness evidence — not silently dropped.

> The step yield shows no significant dependence on any factor, consistent with a
> high-recovery flow-through operation. […] the protein load has no significant effect on
> clearance or recovery over the range studied when the load is of representative
> charge-variant quality — a finding that both widens the acceptable load range and […]
> localizes the load-related risk to the charge-variant quality of the feed rather than
> to a load set-point.

**Imitate:** turn "no effect" into a positive claim (robustness, wider range). **Avoid:**
"no significant effect was observed" with no consequence stated.

---

## 7. Calibrated hedging (verb matched to the evidence)

**Move.** Strong, tight-CI effects are stated plainly; a weaker model is called *adequate*
(not predictive), the reason given, and the variance attributed to the assay.

> The pool-HCP and XMuLV models are additionally predictive (predicted R² ≥
> `{python} f"{PRED_HCP_XMULV_MIN:.2f}"`); the MVM model is adequate (R² =
> `{python} f"{MVM_R2:.2f}"`, adjusted R² = `{python} f"{MVM_ADJ:.2f}"`, no significant
> lack of fit) with a more modest predicted R² (`{python} f"{PRED_MVM:.2f}"`) that reflects
> the narrower log-reduction range of the parvovirus response relative to the spiking-assay
> reproducibility, and is corroborated by its strong, highly significant load-pH and
> load-conductivity main effects.

**Imitate:** "predictive" vs "adequate" is a deliberate distinction; explain a modest
statistic, don't hide it. **Avoid:** claiming every model is predictive.

---

## 8. Bounded design-space claim (NOR inside characterized inside knowledge space)

**Move.** The region is stated, its planes named, and the NOR located *inside* the
characterized region *inside* the PAR knowledge space — with the worst case identified.

> The NOR of each parameter (@tbl-param) — load pH `{python} f"{load_ph.nor[0]:g}–{load_ph.nor[1]:g}"`
> […] — lies well inside the characterized region, which in turn lies within the broader
> knowledge space bounded by the proven acceptable ranges. […] Movement within the
> operating region is not a change, whereas movement outside it would require assessment
> under the quality system [@amab2009; @ichq8].

**Imitate:** the nested-region statement + the change-control sentence. **Avoid:** "the
step is robust" with no boundary.

---

## 9. Cross-step credit

**Move.** For a shared attribute, state *this* step's contribution and name the documents
for the others; never imply one step does it all.

> The cumulative XMuLV clearance meets its ≥ `{python} f"{xmulv_acc_lo:g}"` log₁₀
> requirement with Cpk = `{python} f"{xmulv_cpk:.2f}"` […], to which anion exchange
> contributes orthogonally alongside low-pH inactivation and virus filtration.

**Imitate:** "this step contributes X alongside [the other steps]." **Avoid:** claiming the
whole cumulative outcome for one step.

---

## 10. Parameter-classification rationale (the one idiomatic bullet list)

**Move.** In the classification section, one bullet per parameter: class + the evidence
that earns it. This is the corpus's one idiomatic use of prose bullets.

> - **Protein load — WC-CPP.** Carries a credible risk to the impurity and viral load and
>   is therefore controlled as a well-controlled CPP; in representative load material it
>   showed no significant effect on clearance or recovery, so its acceptable range is wide.
>   The characterization localized the load-related risk to the **charge-variant quality of
>   the load material** (§12), which is controlled as a feed-input attribute rather than by
>   a load set-point.

**Imitate:** class in bold, then the demonstrated-effect justification, then any residual
risk and where it is controlled. **Avoid:** a class with no data-supported reason.

---

## 11. Adverse before mitigation (the deviation opening)

**Move.** State the adverse magnitude and what went wrong **first**; the mitigation and
the residual position come after. Never lead with reassurance.

> During the first execution of the screening and response-surface designs, the
> anion-exchange load (the cation-exchange eluate) was subsequently found to carry an
> **elevated acidic charge-variant (deamidation) burden** […]. In that first execution, at
> the **high-protein-load / high-equilibration-wash-1-conductivity corner** of the design,
> the flow-through-pool HCP rose sharply above the in-process action limit and the pool
> purity became unacceptable, through an anomalous **protein-load × conductivity
> interaction** […]. Because an acceptable operating region could not be defined on a
> non-representative load, the affected […] designs were **invalidated** […] and
> **re-executed in full** […].

**Imitate:** what went wrong → why it matters → the disposition. **Avoid:** "a minor
deviation was noted and resolved" as an opener.

**Note — superseded studies are real.** When a deviation forced re-execution, the first
study actually exists as seeded data (STORY_BIBLE §9). Confirm root cause *from the
requalified data* and reference the superseded set; do not analyse it:

> In the requalified-load DoE reported here, the protein-load × equilibration/wash-1-
> conductivity interaction is **statistically absent** (effect `{python} f"{BD_EFF:.2f}"`
> ng/mg, p = `{python} f"{BD_P:.2f}"`) […]. The anomalous interaction seen in the first
> execution was therefore an **artifact of the degraded (deamidated) load**, not an
> intrinsic property of the step.

---

## 12. Defensive impact argument (the sophisticated move)

**Move.** When a flaw could look damaging, make the *mechanistic* argument that bounds its
impact — here, that a common-mode offset shifts an intercept but not the coefficients, so
classifications and geometry are untouched — then still state the residual correction.

> Because the identical UV set-point was applied to every run, its effect is a
> **common-mode offset**: it shifts the absolute flow-through-pool HCP level […] by an
> approximately constant amount but does not change the factor effects, the two-factor
> interactions or the geometry of the operating region — adding a constant to every
> response changes only the model intercept, not the coefficients. The parameter
> classifications and the design-space geometry reported here are therefore **unaffected**
> […]; only the absolute in-process pool-HCP set-point […] required correction.

**Imitate:** name the mechanism that limits the impact, reason from it, then concede the
real (bounded) correction. **Avoid:** hand-waving that a problem "had no impact."

---

## 13. Mechanistic interpretation (why the surfaces look as they do)

**Move.** Explain the results from the physical chemistry, tie to prior knowledge, and use
it to justify a multivariate region over independent 1-D ranges.

> At the operating pH the antibody carries a slight net positive charge and transmits,
> while the more acidic host-cell protein, DNA and model viruses bind the positively
> charged resin; the strength of that binding — and therefore the clearance — is set by
> the electrostatic environment. A higher load pH increases the net negative charge […]
> so the flow-through-pool HCP falls and the XMuLV and MVM log-reductions rise […]. This is
> the reason a multivariate operating region — rather than independent one-dimensional
> ranges — is used to assure the impurity and viral load […].

**Imitate:** mechanism → direction of each effect → why the factors must be treated
jointly. **Avoid:** restating the effect table in words without the *why*.

---

## 14. The inline-number mechanic (what grounding looks like in prose)

Every measurement is a Quarto inline expression; identifiers are written plainly. Two
concrete forms to internalise:

> The step raised pool HCP `{python} f"{HCP_FOLD:.1f}"`-fold to about
> `{python} f"{HCP_OUT:.0f}"` ng/mg, below the ≤ `{python} hcp_acc_hi` ng/mg limit.

> A Monte-Carlo simulation of `{python} f"{V['n_monte_carlo']:,}"` commercial-scale
> batches […] was used to estimate the […] process capability […].

Identifiers (`SOP-2011`, `AMV-3018`, `RA-001`, `ICH Q5A`, `@tbl-cap`, coded levels −1/0/+1)
are names — write them plainly. If a number you need has no helper, write
`<<NEEDS: description>>` and continue; never type a value from memory.
