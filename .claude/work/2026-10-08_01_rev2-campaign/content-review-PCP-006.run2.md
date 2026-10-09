# Content review — PCP-006 (Low-pH Viral Inactivation), Version 2.0 draft, run 2

Reviewer model: Claude Opus 5.5 (claude-opus-5-5).
Source read: `.claude/work/2026-10-08_01_rev2-campaign/PCP-006_viral_inactivation.DRAFT.txt` (PDF text, 38 pp). No other
repository file was read. Arithmetic was checked in Python using only values printed in the document.

---

## Question 1 — physical cause named in the clause where the cause verb stands

> "Each of them acts on the log reduction of XMuLV and on the amount of aggregate that forms."

Fails Q1: "acts on" with no species, property or direction in the clause. The mechanism is in Section 4.1, but
this clause carries the risk-prioritization argument and names only the two outputs. It should say which way each
parameter moves them (lower pH, longer hold and higher temperature raise the log reduction, and longer hold and
higher temperature raise aggregate).

> "At acid pH the antibody carries a large net positive charge, and the second constant domain of its heavy chain is
> partially unfolded, which exposes hydrophobic surface."

Fails Q1: the net positive charge is stated as a property with no direction and no consequence anywhere in the
paragraph, and it sits in the subject position of the aggregation mechanism, where a reader will take it as a cause
of association. High net charge opposes association by electrostatic repulsion; only the exposed hydrophobic
surface drives it. Either give the charge its direction or drop the clause.

Everything else in the mechanism passages passes: the envelope glycoprotein denaturation and its pH and
temperature direction (Section 4.1), the absence of an envelope on a parvovirus (Section 4.1), the concentration
dependence of the association rate (Section 4.3), the hinge-region cleavage as a reaction of each molecule with
the solvent (Section 12, assumption 4), and the matrix and volume dependence of the inactivation rate
(Section 5.1). "Because viral clearance is validated at worst-case conditions" and "because a model that fits its
own runs much better than it predicts left-out runs has more terms than the data support" are procedural and
statistical reasons and were judged under Q3 and Q5.

## Question 2 — every technical term a term of art

> "The NOR-propagated PAR is the one that supports a claim."

Fails Q2: "NOR-propagated" is a coinage of this document set. It is transparent and is defined by the analysis in
Section 8, but it is not a term in the DoE or process-validation literature, which would say the PAR is computed
with the remaining parameters varying over their normal operating ranges.

> "Clearance fold" (Table 7.1 column header; also "the cation exchange clearance fold", Section 7.2)

Fails Q2: the literature term is clearance factor, or fold reduction. "Clearance fold" inverts the standard
compound.

> "18–40 % (CEX/icIEF)" (Table 4.1)

Fails Q2: "CEX" is not in the abbreviation list and in this corpus denotes the cation exchange *step* (Step 7, the
step after this one). Used here as a method qualifier beside icIEF it is ambiguous. The method is icIEF under
SOP-3013; the step is named in full everywhere else in the document ("before cation exchange").

Accepted as terms of art: CPP, KPP, WC-CPP, GPP (A-Mab case study and ICH Q8 usage), intermediate acceptance
criterion, platform claim, modular viral clearance claim, spiking model, TCID50, log reduction factor, pure error,
lack of fit, face-centred central composite design, axial run, PRESS, predicted R², Cook's distance, hierarchical
model, knowledge space, ALCOA+, Tool #1 (defined in the table note).

## Question 3 — telling the reader how to file the finding

> "The wider criterion does not loosen an approved criterion, because the Version 1.0 limit was applied in the
> report at analysis and appeared in no approved plan."

Fails Q3: a gloss that answers an objection nobody has raised, and files the change under a category ("not a
loosening") rather than stating it. The two facts it rests on are already in Table 1.1 footnote a) and in
Section 1.1 item 1.

> "It is not a value of the low-pH step itself."

Fails Q3: a gloss defending the preceding sentence against a misreading no reader has committed. The preceding
sentence already says the column is the cumulative figure for the steps after this one.

> "That bound is the only A-Mab result in the criteria of this step, and it comes from the cation exchange studies."

Fails Q3: files the cation exchange bound as an exception to the a-priori claim of the Section 7 preamble instead
of letting the derivation stand. It is also the sentence that exposes the inconsistency flagged under Q5.

> "Acidic variants are of very low and fragments of low criticality, and their criteria still apply."

Fails Q3: the trailing clause pre-empts the objection "why set a criterion for a non-critical attribute". The
criteria are in Table 7.1 and in Section 7.2; nothing needs defending.

> "This is a limit on overfitting, because a model that fits its own runs much better than it predicts left-out
> runs has more terms than the data support."

Fails Q3: renames the criterion as a category and then justifies it, inside a numbered acceptance criterion where
the criterion alone is what will be applied. (The reason given is also only one of the causes of a large
R² to predicted R² gap — see Q5.)

## Question 4 — criteria with their basis, decision rules unambiguous

> "A critical process parameter (CPP) has an effect on a CQA that is significant and practically relevant within
> the characterized range, and a high risk of falling outside its acceptable range in operation."

Fails Q4: "practically relevant" and "a high risk" are not defined, and the WC-CPP class turns on "a low risk ...
because it is readily controlled and its PAR is wide against its NOR", with no threshold for "wide". Section 7.6
then adds that an effect "too small to move the attribute appreciably within the PAR" does not make a parameter
critical. Three undefined magnitude words carry the whole classification, so two analysts can reach different
classes from the same fitted model. Section 7.6 asks PCR-006 to state the effect size across the PAR, which is
the right input, but no rule turns that number into a class.

> "A justified change of terms is the removal of terms that are not significant at α = 0.05, with the model kept
> hierarchical."

Fails Q4: the remedial path in Section 7.1 item 3 is open-ended. It fixes no order (terms first or transformation
first), no limit on the number of attempts, and no pre-declared transformation family, and the judgement of what
the residuals "support" is made after the data are seen. In a plan whose whole purpose is to remove post hoc
freedom from the criteria (INV-001 finding 1), the model that the criteria are applied to is still chosen after
the fact. Pre-specifying the sequence, the candidate transformations and a stopping point would close it.

> "Where no adequate model exists for an attribute, the most extreme result measured in the designs on the side of
> the limit takes the place of the prediction limit."

Fails Q4: "the designs" is not resolved. The screening design has no usable fragment result (Section 5.3), so for
fragments this fallback can only mean the response-surface design, and for aggregate and acidic variants it is
unclear whether screening runs, which lie outside the NOR at both ends, are in the pool. Name the design.

Criteria that pass: every row of Table 7.1 carries a basis column and a derivation in the Section 7.2 text; the
four adequacy conditions of Section 7.1 item 2 are each operational, with the Cook's distance limit computed for
n = 18; the XMuLV rule in Section 7.3 names the statistic, the grid and the value; the hold criterion in
Section 7.5 names the statistic, the scale, the two-sided handling and the sampling days; the PAR rules in
Section 8 state what is compared with what. Minor: for acidic variants in the hold, the lower-limit arm of
Section 7.5 item 1 can never bind, because deamidation during a hold only raises the level; the rule stays
unambiguous, so this is noted, not flagged.

## Question 5 — wrong, internally inconsistent, or contradicted by a table

> "A response-surface model predicts the mean response. A quality attribute is therefore judged on a single batch,
> through a 95 % prediction interval, wherever a judgement supports a claim."

Fails Q5: the inference is inverted. That the model predicts a mean is not a reason to judge on a single batch; it
is the reason a prediction interval is needed, given that the criterion applies to a single batch. As written the
"therefore" draws the premise from the wrong sentence.

> "XMuLV clearance is judged on the mean predicted LRF at the least favourable combination of inactivation pH, hold
> time and temperature within their NORs, because viral clearance is validated at worst-case conditions."

Fails Q5 against Table 4.1: the sentence two lines above states that *a quality attribute* supporting a claim is
judged on a single batch through a 95 % prediction interval, and Table 4.1 lists viral clearance as an attribute
of very high criticality. XMuLV clearance is therefore a quality attribute that supports a claim and is judged on
a mean. The worst-case-conditions rule is stated consistently across Sections 1.1, 5.5, 7.3, 8 and 12, so the
defect is in the general sentence, which should be scoped to the attributes judged per batch (aggregate, fragments
and acidic variants).

> "The criteria below apply PCMP-001 §7 to this step. They are derived a priori from the drug substance criteria
> and the platform history, and no result of the studies in this plan enters them (PCMP-001 §7.3)."

Fails Q5 against Table 7.1: footnote a) of that table, and the Section 7.2 text, state that the aggregate criterion
contains the 95 % confidence bound of an A-Mab cation exchange result (PCR-007) in place of the platform clearance
fold, and the document itself says so: "That bound is the only A-Mab result in the criteria of this step". The
criteria are therefore not derived from the drug substance criteria and the platform history alone. The second
half of the sentence ("no result of the studies in this plan") is true, and the first half is what fails; state
the derivation as drug substance criteria plus platform history plus the verified downstream bounds.

> "It scans the parameter across 81 grid points over its range studied while the other two factors of the
> response-surface model vary within their NORs."

Fails Q5 against the sampling rule in the same section: the rule draws each of the other factors from a normal
distribution centred on the set-point with a standard deviation of one sixth of the NOR width and clips only at
the ends of the *range studied*, not at the NOR. About 0.3 % of draws per factor fall outside the NOR, so the
factors do not vary within their NORs as claimed. The practical effect is nil, because the interval keeps the
central 95 % of the simulated batches and trims those tails, but the sentence does not describe the rule it
introduces.

> "Increase, the largest increase across the step for X-Mab, Y-Mab and Z-Mab, at a hold time of 180 min, in the
> unit of the attribute." (Table 7.2 note), read against: "The verification of the platform worst cases takes the
> largest increase that the response-surface model predicts within the NOR, with its one-sided 95 % confidence
> bound on the unfavourable side."

Fails Q5: the comparison is not on a common basis. The platform worst cases are fixed at a 180 min hold, which is
the top of the range studied and 60 min above the top of the hold time NOR of 60–120 min in Table 6.1. The A-Mab
side is evaluated inside the NOR only. Since aggregate, fragments and acidic variants all rise with hold time, the
A-Mab value is taken at a milder condition than the reference it must beat. Under rule 2 of Section 7.4 this bias
runs in the direction of widening the criteria upstream of this step. Either evaluate the A-Mab prediction at
180 min for the verification, or state the platform value at the matching hold time.

> "Inactivation follows first-order kinetics. Its rate constant rises as the pH falls and as the temperature rises,
> and the log reduction is that rate integrated over the hold time."

Fails Q5, minor: for first-order kinetics the integral of the rate constant over the hold gives the natural-log
reduction, which is 2.303 times the log10 reduction used everywhere else in the document (LRF, log10 in
Tables 1.1, 7.1). As written the sentence equates the two. "Proportional to" would fix it.

> "This is a limit on overfitting, because a model that fits its own runs much better than it predicts left-out
> runs has more terms than the data support."

Fails Q5, minor: a large gap between R² and predicted R² is also produced by a single high-leverage or
influential run inflating PRESS, which is why Section 7.1 adds the Cook's distance test. The stated reason is one
cause presented as the cause.

Arithmetic and cross-table checks that pass: 2.00 × 1.30 = 2.60 (fragments IAC); 6.6 + 5.5 + 4.62 = 16.72, which
is 0.02 above 16.7, so the claim that a shortfall here cannot be absorbed elsewhere holds; screening 11 − 7 = 4
residual df, 2 pure error from 3 centre points, 2 lack of fit; response surface 18 − 10 = 8 residual df, 3 pure
error from 4 centre points, 5 lack of fit; 4/18 = 0.22; design centres 3.6 / 120 min / 20 °C are the midpoints of
the ranges in Table 6.1 and are not the set-points; each NOR half-width equals three times one sixth of the NOR
width, and each set-point is the NOR midpoint, so the "three standard deviations on either side" statement holds;
Appendix A is 8 + 3 = 11 runs and Appendix B is 8 + 6 + 4 = 18, matching Table 5.3 and Sections 6.2 and 6.3; the
appendix settings reproduce the ranges in Table 6.1. For aggregate, 5.00 × 1.52 = 7.60 against the shown 7.58; the
implied unrounded fold is 1.516, which rounds to 1.52, so the table's note on unrounded values covers it.

## Question 6 — reads as written by a machine

> "In both directions the bound replaces the platform value, and the point prediction never does."

Restates rules 1 and 2 of Section 7.4, which both say the bound replaces the platform value. The second clause
adds emphasis, not information.

> "Predictions of aggregate and acidic variants are translated to manufacturing scale before the comparison, and
> predictions of fragments and XMuLV clearance are compared as the model gives them (Section 5.1)."

A near-verbatim repeat of the same two-clause sentence in Section 5.5, in a section that already cross-references
Section 5.1.

> "The NOR-propagated PAR is the one that supports a claim."

Appears in Section 5.5 and again in Section 8, both times as a standalone sentence.

> "The SEC results for fragments are kept in the record and are not used for any decision."

Verbatim repeat of the Section 5.3 sentence, in the data management section.

> "For every attribute except viral clearance, a higher Tool #1 score gives an equal or higher level of criticality."

Stated in the Section 4.2 text and again, in the same words, in the note to Table 4.1 two paragraphs later.

> "The last column of the table names the step at which the register places each attribute."

Says nothing the column header "Formed or set at" does not already say.

> "Table 6.1 in Section 6.1 lists the four parameters with their ranges."

A pointer to a table two sections later, closing a paragraph that has already named the four parameters and their
study types. Section 1 has also already listed them.

> "The studies follow the sequence in Table 11.1, and two of them share a phase."

The second clause reports what the reader sees in the table's Phase 3 row.

> "RA-001 gives the scores and the rationale for each assignment, and they are not repeated here."

Commentary on the document's own coverage. The cross-reference carries the content.

> "Fragments were not assessed in Version 1.0."

The third statement of this fact in two pages, after Section 1.1 item 2 and footnote d) of Table 1.1.

> "They are the values against which the studies were planned and around which they were run."

Restates the preceding sentence and the caption of Table 6.1.

> "PCR-006 will report each result against its criterion, with the value, the criterion and whether the criterion
> was met."

The trailing list is the definition of reporting a result against a criterion.

## Question 7 — understandable standalone

> "Size exclusion chromatography (SEC) reads fragments high in this matrix (INV-001 finding 6)."

Fails Q7: "this matrix" has no antecedent here. Should name the Protein A eluate and the neutralized pool, as
Section 5.3 does.

> "One check has already changed a criterion of this step."

Fails Q7: the subject is an abstract stand-in. Should name the cation exchange aggregate clearance check and the
aggregate criterion.

> "This plan applies the same rule to a model that fails any of the four conditions in item 2."

Fails Q7: refers to a numbered item by label alone. Should name the conditions (model F-test, lack of fit,
overfitting limit, residual diagnostics).

> "A model whose conclusion changes between the two ends of the interval is not used for that output."

Fails Q7: "A model" is the scale-down model, but the sentence sits two lines after a rule about the
response-surface model and the "interval" is the 90 % confidence interval of the offset. Should name both.

> "The decision whether the model is qualified for an output rests on the conclusion over the NOR in rule 3 below,
> which needs the response-surface model."

Fails Q7: two models in one sentence, the first unnamed, plus a reference to "rule 3 below" by label. Should name
the scale-down model and state the conclusion rather than point to the rule.

> "That applies to the NOR-propagated PAR (Section 8) and to the conclusion over the NOR in the qualification of
> the scale-down model (Section 5.1), which uses the exact prediction interval of a single run."

Fails Q7: the subject "That" stands in for judging an attribute on a single batch. Should name it.

> "The first PAR analysis, at the set-points, judges the mean prediction, and the NOR-propagated PAR is the one
> that supports a claim (PCMP-001 §6.4)."

Fails Q7: "the first PAR analysis" is a label whose content is defined only in Section 8, eleven pages later.
Should say the analysis that holds the other parameters at their set-points.

> "The source also includes Table 4.16 of the A-Mab case study." (footnote a) to Table 7.2)

Fails Q7: "The source" names nothing, and the table it annotates has no source column. See the table observations.

> "It applies the Process Characterization Master Plan PCMP-001 to this step and adds what is specific to the step."

Fails Q7: "what is specific to the step" is an abstract stand-in for the content of the plan. Should name it (the
scale-down and spiking models, the step's designs and its intermediate acceptance criteria).

---

## Table observations

**Table 1.1 — Version 1.0 and Version 2.0 criteria.**
- Header runs three lines deep: the version spanners on one line, "Criterion / Rule / Criterion / Basis" on the
  next, with the stub "Attribute" straddling both. The two "Criterion" sub-headers are not distinguishable without
  the spanner above them.
- Footnote keys mix letters (a–d) with rule codes (R1, R3); the codes are both cell content and footnote keys, and
  R2 is missing with no explanation in this document.
- Footnote R3, "requirement - nominal of other steps", uses a hyphen where a minus sign is meant.
- The acidic variants row has "none" centred across the Criterion and Rule columns, so it is unclear whether
  "none" is the Version 1.0 criterion or the Version 1.0 rule. Footnote b) resolves it; the cell does not.
- The Version 2.0 basis cell "Carried back, tightened from ≤ 10.0" wraps over three lines and the footnote marker
  lands inside the phrase, between "tightened" and "from".
- Content agrees with the text (2.17, margin 6.0, 7.58, 10.0, 4.93, 6.60).

**Table 3.2 — procedures and method validations.**
- The "Type" column is a merged cell whose label is split across the rows it spans ("Standard / operating /
  procedure", "Analytical / method / validation"), so the label lines interleave with the SOP and AMV rows.
- "Reference" and "Title" run together in the header line with no visible gap.

**Table 4.1 — quality attributes in scope.**
- "Formed or set at" does not fit the viral clearance row: a cumulative clearance requirement is not formed or set
  at a step. Footnote c) patches it after the fact.
- The criticality codes VH, H, L and VL appear with no legend in the table. H and VH are expanded in the text; L
  and VL are only decodable from a later sentence.
- "18–40 % (CEX/icIEF)" is ambiguous: CEX is undefined in the abbreviation list and denotes the cation exchange
  step elsewhere in the corpus.
- The attribute cell "Viral clearance — XMuLV (enveloped)" wraps so that footnote marker a) sits beside
  "(cumulative)" on the second line rather than on the criterion it qualifies.
- The caption says the rows come from the drug substance CQA register, but two of the four attributes are of low
  and very low criticality and are therefore not CQAs by the document's own definition.
- The table note repeats the Tool #1 monotonicity sentence from the text verbatim.

**Table 5.2 — methods for size variants.**
- The aggregate row carries a single "SEC" centred under both study columns; the reading "both designs" comes from
  the text, not from the cell.
- Footnote b) reads "Retained response-surface samples, tested 2026-04-06 to 2026-04-17", but the re-test study it
  describes also covers the hold study samples (Sections 5.3 and 6.5, Table 11.1). The footnote is narrower than
  the study, which is defensible given the caption's scope but reads as the whole of S-VI-RET.

**Table 5.3 — sampling plan.**
- The re-test row duplicates itself across two columns: "Runs or conditions" holds "Retained samples of the
  response-surface design and of the hold study" and "Sample" holds "Retained samples".
- The univariate row says "two levels" without the levels; 5 and 35 g/L appear only in Section 6.4.
- Cells wrap so that study codes break away from their study names ("Response-surface design" on one line,
  "(S-VI-RSM)" on the next).

**Table 6.1 — parameters, set-points, ranges and NORs.**
- Footnote markers abut the values with no space ("3.5a)", "3.4–3.6b)", "60–120d)", "19–23e)", "5–35f)"), so a
  marker can be read as a digit or a unit.
- Five of the six footnotes record that PCR-006 Version 2.0 moved or narrowed the value in the cell. The caption
  states that these are the planned values, which is the right framing, but the Set-point and NOR columns carry no
  in-column indication that every one of their entries is superseded.
- The A-Mab concentration row has a NOR equal to the range studied, so no PAR for that parameter can extend beyond
  its NOR; the consequence is handled in Section 8 rule 5 but is not visible in the table.

**Table 7.1 — intermediate acceptance criteria.**
- Header is three deep ("Downstream worst case" spanning "Clearance fold / Increase", with Attribute, DS criterion,
  IAC and Basis on the outer lines) and the spanner and its sub-headers run together.
- The aggregate row's clearance fold of 1.52 is not a downstream worst case, which is what the column header and
  the text ("the downstream worst case is the cumulative clearance fold and increase of the steps after this one")
  both say it is. Footnote a) states that it is the 95 % confidence bound of an A-Mab cation exchange prediction
  that replaced the platform value. The label contradicts the cell.
- Footnote a) describes "a downstream step" without naming it; the text names cation exchange and PCR-007.
- The "Increase" column is 0.00 in all three applicable rows and "not applicable" in the fourth, so it carries no
  information for this step.
- The XMuLV row's DS criterion is a cumulative requirement while the other three are per-batch limits, in one
  column, decodable only from footnote c).
- The note on unrounded values is load-bearing: 5.00 × 1.52 = 7.60, not the 7.58 shown. The implied unrounded fold
  is 1.516.

**Table 7.2 — platform worst cases.**
- Footnote a) does not match what it marks. It is attached to the attribute label "Aggregates, HMW (%)" and reads
  "The source also includes Table 4.16 of the A-Mab case study", but the table has no source column and "The
  source" has no antecedent anywhere in the table or its notes. This is the clearest footnote mismatch in the
  document.
- The note fixes the platform increases at a 180 min hold, which is above the hold time NOR of Table 6.1. The
  verification rule in the text evaluates the A-Mab side inside the NOR, so the table's own note establishes that
  the two sides of the comparison are not on a common basis (see Q5).
- The "Increase" header carries no unit; the unit is given only in the note.
- The upstream criterion cells wrap so that "Aggregate, production bioreactor" and "output" split across lines.

**Table 10.1 — responsibilities.** No issues.

**Table 11.1 — sequence of studies.** Phase 3 holds two study codes in one cell, which matches the text statement
that two studies share a phase. The note on the qualification decision agrees with Sections 5.1 and 11. No issues.

**Tables A.1 and B.1 — planned designs.**
- Two-level header ("Coded level" over A / B / C, "Setting" over pH / Hold time (min) / Temperature (°C)) with the
  stub "Run" straddling both header lines; at the two-line limit rather than over it.
- The coded-level columns are identified by the letters A, B and C only. The factors are inferable because the
  Setting columns follow the same order, but neither appendix names them; the mapping lives in the Code column of
  Table 6.1, 16 pages earlier.
- Settings reproduce the ranges and centres of Table 6.1 exactly, and the run counts match Sections 6.2 and 6.3
  and Table 5.3 (11 runs with 3 centre points; 8 factorial, 6 axial and 4 centre points for 18).

---

## Answers

1. Physical cause named in the clause: **no** (2 sentences flagged).
2. Every technical term a term of art: **no** (3 flagged: "NOR-propagated", "clearance fold", undefined "CEX").
3. Tells the reader how to file the finding: **yes** (5 sentences flagged).
4. Criteria with their basis and unambiguous decision rules: **no** (3 flagged; the parameter classification
   thresholds and the remedial model-selection path are the substantive ones).
5. Wrong, internally inconsistent or contradicted by a table: **no** (7 flagged, of which the a-priori claim in
   the Section 7 preamble against Table 7.1 footnote a), the single-batch rule against Table 4.1, and the 180 min
   platform basis in Table 7.2 against the within-NOR verification are the material ones).
6. Every sentence reads as written by a process scientist: **no** (11 sentences flagged).
7. Every sentence understandable standalone: **no** (9 sentences flagged).
