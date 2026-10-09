# Content review — PCP-006 Version 2.0, Low-pH Viral Inactivation (Step 6)

Reviewer: Claude Opus 5.5 (claude-opus-5-5). Source reviewed:
`.claude/work/2026-10-08_01_rev2-campaign/PCP-006_viral_inactivation.DRAFT.txt` (PDF text,
1283 lines). Nothing else in the repository was read. Arithmetic was checked only against
numbers printed in the document.

Quotes are reconstructed from the PDF text with line-break hyphenation closed up
(e.g. "chem-/istry" → "chemistry"); the words are otherwise verbatim.

## Numbers that check out (no flag)

Worth recording, because most of the quantitative load of the document is sound:

- 5.00 x 1.52 = 7.60 against the printed IAC of 7.58; 7.58 / 5.00 = 1.516, so the
  rounding note under Table 7.1 covers the difference. 2.00 x 1.30 = 2.60 exactly.
- 6.6 + 5.5 + 4.62 = 16.72, and 16.72 - 16.7 = 0.02, as Section 7.3 states.
- Version 1.0 reverse-engineers cleanly: 2.17 x 6.0 = 13.02, implying a nominal cation
  exchange fold of 2.604 against the a priori platform fold of 2.0 (10.0 / 5.00) and the
  verification bound of 1.516. A nominal better than the platform worst case, which is in
  turn better than the NOR worst case, is internally coherent. Version 1.0's XMuLV
  criterion of 4.93 implies 11.77 log10 nominal for the other two steps against their
  10.12 log10 of claim, which is likewise coherent.
- Degrees of freedom: screening 11 - 7 = 4, of which 2 pure error from three centre
  points and 2 lack of fit; response surface 18 - 10 = 8, of which 3 pure error from four
  centre points and 5 lack of fit. Both correct, and the lack-of-fit decomposition
  ("curvature and the three-factor interaction") is the right one for a 2^3 with centre
  points.
- Face-centred central composite: 8 + 6 + 4 = 18 runs, axial points at +/-1, every run
  inside the range studied. Appendices A and B decode correctly at every row.
- Design centre (pH 3.6, 120 min, 20 C) is the midpoint of each range studied and is not
  any set-point, as Section 6.1 says. Every set-point is the midpoint of its NOR, which is
  what the Monte Carlo in Section 8 assumes.

## Question 1 — physical cause in the clause where the verb stands

The mechanism paragraph in Section 4.1 is mostly exemplary: the acid, the lipid envelope,
the envelope glycoproteins, the net positive charge at acid pH, the partially unfolded
second constant domain, the exposed hydrophobic surface, the bimolecular association, the
hinge cleavage and the MVM exclusion are all named with a direction. Two sentences fail.

1. "Inactivation pH is expected to govern the step, because the rate depends on it steeply
   near the operating range."
   Fails Q1: the because-clause names no species, no interaction and no direction — it
   restates the size of the effect, so the cause offered for "governs" is the effect
   itself. The direction (the rate constant rises as the pH falls) is in the previous
   sentence, not in this clause.

2. "It acts on aggregation, because association is a bimolecular event, but it has no
   effect on the inactivation chemistry."
   Fails Q1: "acts on" carries no direction, and the clause does not say that a higher
   antibody concentration raises the collision rate and therefore the aggregation rate.
   The second half asserts a negative cause with no mechanism at all (see Q5 item 3).

Considered and not flagged: "The log reduction is the product of a rate that pH and
temperature set and the time over which that rate acts." The verb "set" has no direction
here, but the sentence states a kinetic relation rather than a causal claim, and it is
consistent with "that rate integrated over the hold time" in Section 4.1.

## Question 2 — terms of art

No sentence flagged. Every substantive term is standard: first-order inactivation, log
reduction factor, TCID50, spiking study, modular viral clearance claim, CH2 described in
plain words, succinimide formation, hinge cleavage, nrCE-SDS, icIEF, pure error, lack of
fit, PRESS, predicted R-squared, face-centred central composite design, axial runs,
standard order, knowledge space, criticality as a continuum, CPP/WC-CPP/KPP/GPP (each
defined in Section 7.6), prediction interval, Tool #1.

Two labels are not literature terms but are transparent and defined in place, so they are
noted rather than flagged:

- "NOR-propagated" ("The NOR-propagated PAR is the one that supports a claim."), a local
  compound built on a defined abbreviation.
- "Clearance fold" as the column header of Table 7.1; the literature says clearance factor
  or fold reduction. See table observations.

## Question 3 — filing the finding

No sentence flagged. Three near misses, with the reason each survives:

- "This does not loosen an approved criterion, because the Version 1.0 limit was applied in
  the report at analysis and appeared in no approved plan." Defensive in shape, but the
  objection is live: the document is an amendment under a major investigation into criteria
  set after the data, and it has just widened a number. Answering it is the plan's job.
- "That bound is the only A-Mab result in the criteria of this step, and it comes from the
  cation exchange studies." Substantive disclosure, not a category label.
- "In both directions the bound replaces the platform value, and the point prediction never
  does." A restatement of rules 1 and 2, but it closes a real gap by ruling out the point
  prediction under rule 3.

The sentence that comes closest to a filing instruction is flagged under Q6 instead
("The characterization of A-Mab therefore confirms and bounds known behaviour."), because
its defect is that it adds no fact rather than that it files one.

## Question 4 — criteria with a basis, decision rules that can be applied

Every acceptance criterion carries its basis: the aggregate, fragment and acidic variant
IACs are derived in Table 7.1 and argued in Section 7.2; the XMuLV criterion is the
platform claim; the hold criterion is referred to the pool's IAC; the 0.2 limit on the
R-squared gap is explained. The failures are all in the decision rules.

1. "The residuals show no pattern against the predicted values or the run order, and no
   single run dominates the fit."
   Fails Q4: an adequacy condition with no statistic and no threshold. "No pattern" and
   "dominates" cannot be judged the same way by two analysts; no influence measure or
   cut-off is named.

2. "A model that fails the lack-of-fit test or the limit on overfitting is refitted with a
   justified change of terms or transformation, or it is not used to set a range."
   Fails Q4 on two counts: Section 7.1 item 2 sets four adequacy conditions and this rule
   covers only two of them, so no action is stated for a non-significant model F-test or
   for a residual pattern; and "a justified change of terms or transformation" names
   neither the permitted changes nor who judges them, which is the discretion that
   INV-001 exists to remove.

3. "Each parameter is drawn from a normal distribution centred on its set-point, with a
   spread set by the width of its NOR, and clipped to the range studied."
   Fails Q4: "a spread set by the width of its NOR" states no rule (half-width as one
   sigma? as three sigma?), so the PAR that supports the claim is not reproducible from
   the protocol.

4. "A significant effect that is too small to move an attribute appreciably within the PAR
   does not by itself make a parameter critical."
   Fails Q4: "appreciably" sets no threshold, and rule 1 of the same section leans on
   "practically relevant". The CPP / WC-CPP / KPP boundary therefore cannot be settled from
   a result, which is the one thing a classification rule has to do.

5. "The range of A-Mab concentration is supported by its own univariate data, judged
   against the criteria in Table 7.1."
   Fails Q4 and Q5: Table 7.1 carries four criteria, and Table 5.3 shows the univariate
   study S-VI-UNI measures only aggregate and acidic variants. The rule cannot be applied
   to fragments or to XMuLV clearance, and the document does not say that it is restricted
   to two of the four. The same defect is in Section 5.5: "The results of the univariate
   study are compared with the set-point runs of the qualification study and with the
   criteria in Table 7.1."

6. "PCR-006 will report, for each temperature, the longest hold studied at which every
   attribute meets this criterion."
   Fails Q4: Table 5.3 and Section 6.5 sample fragments by nrCE-SDS on days 0, 3 and 7
   only, while aggregate and acidic variants are sampled on days 0, 1, 3, 5 and 7. At days
   1 and 5 "every attribute" has no fragment result, so the longest qualifying hold is
   undefined at two of the five time points.

7. "The highest level that the pool is expected to carry in routine manufacture, plus the
   increase measured over the hold, must meet the intermediate acceptance criterion of the
   pool in Table 7.1."
   Fails Q4 (minor): for acidic variants the IAC is the two-sided range 18.0-40.0 %, and
   the rule builds only an upper value, so it does not say which bound is being tested.
   Defensible on mechanism, but a two-sided criterion deserves one clause.

8. "The expected level is the upper 95 % prediction limit of a single run from the
   response-surface model, at the least favourable combination of NOR low, set-point and
   NOR high, at manufacturing scale."
   Fails Q4 (minor): "at manufacturing scale" is applied to all three attributes, but
   Section 5.1 gives an offset only for aggregate and acidic variants and says the fragment
   offset is "unknown, not zero", and Section 8 correctly restricts the translation to the
   two. For fragments the instruction names a translation that does not exist.

## Question 5 — wrong, inconsistent, or contradicted by a table

1. "The model is qualified under SOP-1001 in the qualification study S-VI-SDM, before the
   first characterization run."
   Conflicts with Section 5.1 item 3 and Table 11.1. The qualification rule reads: "The
   conclusion is whether the output meets its criterion at every combination of NOR low,
   set-point and NOR high of the three factors of the response-surface design." That
   conclusion needs the fitted response-surface model, which does not exist until
   S-VI-RSM (Table 11.1, phase 3) has run and been analysed. Table 11.1 nevertheless puts
   "Qualification of the scale-down model against manufacturing scale" in phase 1, and
   Section 11 repeats that the model "is qualified before the first characterization run".
   The execution of S-VI-SDM can come first; the qualification decision cannot. Section 7.1
   item 1 inherits the same problem.

2. "From 2026-03-20, fragments are measured by nrCE-SDS in every study at every step,
   following the method decision AMD-001 (PCMP-001 §7.8)."
   Contradicted by Table 5.3, in which the qualification study and the univariate study
   test only "Aggregate and acidic variants" — no fragments by any method. As written the
   sentence also contradicts Section 6.4, which lists only aggregate and acidic variants
   for S-VI-UNI. The claim should be about which method is used where fragments are
   measured, not about every study.

3. "It acts on aggregation, because association is a bimolecular event, but it has no
   effect on the inactivation chemistry." and "XMuLV clearance is not measured in this
   study, because the antibody concentration does not act on the inactivation of the viral
   envelope."
   Both conflict with Section 5.1: "The inactivation rate depends on the pH, the
   temperature and the composition of the pool, and not on its volume." The antibody is
   the dominant component of that composition at 5 to 35 g/L, so the plan cannot both rest
   representativeness on pool composition and assert that antibody concentration has no
   effect on the inactivation. It is also the weaker of the two positions scientifically:
   protein concentration is a recognised modifier of low-pH inactivation kinetics, and the
   plan decides not to measure XMuLV clearance in the one study that varies it sevenfold.
   If the position is kept it belongs in Section 12 as an assumption, not as a cause.

4. "Criticality was assigned with Tool #1 of the A-Mab case study, as the product of impact
   and uncertainty (CMC Biotech Working Group 2009)."
   Contradicted by Table 4.1 in the same subsection. The table gives XMuLV clearance VH at
   a Tool #1 score of 20 and aggregates H at a score of 60, with fragments L at 12 and
   acidic variants VL at 4. If the band follows the score, 60 cannot sit below 20; if it
   does not, the stated rule is not the rule used, and the document gives no second rule.
   A reader cannot reconcile the two columns from anything in the document.

5. "Each quality attribute is judged on a single batch, through the 95 % prediction
   interval of a single run, because a single batch is what must meet the criterion."
   Conflicts with the first PAR analysis in Section 8: "Its PAR is the contiguous range
   around the set-point over which the mean prediction meets the criterion." Section 5.5
   states the prediction-interval rule for quality attributes with no exception, and the
   set-point scan then judges them on the mean. Partly mitigated by "The NOR-propagated PAR
   is the one that supports a claim", but the general rule in Section 5.5 should carry the
   exception rather than leaving the two methods to be reconciled by the reader.

6. "Enveloped viruses are inactivated at low pH because the acid disrupts the lipid
   envelope and denatures the envelope glycoproteins that the virus needs to enter a cell."
   Scientifically loose, and at odds with the document's own later mechanism. Low pH acts
   on the envelope glycoproteins, driving an irreversible conformational change that
   removes the ability to fuse; the lipid bilayer itself is comparatively acid stable, and
   bilayer disruption is what solvent or detergent treatment does. Section 4.1 then says "a
   warmer hold speeds the denaturation of the envelope proteins", which is the right
   mechanism and sits oddly beside the lipid claim. The same framing carries into "It makes
   no claim for the parvovirus minute virus of mice (MVM), because a parvovirus has no
   lipid envelope for low pH to disrupt." — true of the conclusion, but the operative
   reason is that a non-enveloped virus has no envelope glycoprotein to denature.

7. "Acid also catalyses reactions at labile residues, including succinimide formation and
   hydrolysis, and these reactions add acidic variants."
   Scientifically loose in the same way. Succinimide formation removes a free carboxylate
   and shifts the molecule to the basic side; the acidic variant appears on hydrolysis of
   the succinimide to aspartate or isoaspartate. Naming the pair as a route is defensible,
   but as written the acidic shift is attributed to both reactions. Related: Table 4.1
   labels the attribute "Acidic charge variants (deamidation)", and deamidation is base
   catalysed and is the route Section 6.5 names for the neutralized pool, not for the acid
   hold. The table's mechanism label and the Section 4.1 mechanism do not agree.

8. "To determine the PAR of each parameter for each attribute that has a criterion at this
   step, and to establish whether the NOR lies within it."
   Over-promises against Section 8, which computes a PAR "for each attribute that has a
   criterion at this step and for each factor of the response-surface model" and supports
   the A-Mab concentration range from univariate data instead. Objective 3 promises a PAR
   for all four parameters; the plan delivers three.

9. Presentational, not numeric: "Aggregate in the neutralized pool must not exceed 7.58 %
   HMW." The Version 2.0 basis in Table 1.1 reads "Carried back, tightened" while the only
   comparator in that table is the Version 1.0 limit of 2.17 %. The 10.0 % a priori value
   that it was tightened from appears in neither table, only in the Section 7.2 prose, so
   the word "tightened" contradicts what the table shows. See table observations.

## Question 6 — machine-written sentences

1. "The characterization of A-Mab therefore confirms and bounds known behaviour."
   Flagged: abstract subject, no fact. The two preceding sentences have already said that
   the platform history supplies the XMuLV claim and the largest increases, and that the
   IACs are built on those values. This sentence restates them as a category of activity
   and a reader loses nothing if it is cut.

2. "The notes to Table 6.1 give the set-points and NORs that PCR-006 Version 2.0 put in
   force (Section 1.1). This plan keeps the values against which its studies were
   designed."
   Flagged: both halves are already in the document. Section 1.1 says "This plan does not
   adopt those values. The notes to Table 6.1 give them and name PCR-006 as the document
   that made each change", the Table 6.1 caption says "with the set-points and NORs against
   which the studies were planned", and the clause "the values against which the studies
   were planned and around which they were run" appears verbatim in Section 1.1 and again
   in Section 6.1 before the table. This is the fourth statement of one point.

Considered and not flagged, because each is short and carries a fact: "The deliverable of
this plan is the Process Characterization Report PCR-006, paired with this plan."
(redundant tail only); "Acidic variants are of very low and fragments of low criticality,
and their criteria still apply." (makes the real point that low criticality does not
exempt an attribute); "RA-001 gives the scores and the rationale for each assignment, and
they are not repeated here." (tells the reader where to look); the Section 13 approval
sentences (procedural and required).

## Question 7 — standalone comprehensibility

1. "XMuLV clearance is judged on the mean predicted LRF at the least favourable combination
   of the other parameters within the NOR."
   Flagged: "the other parameters" has no antecedent in Section 5.5 — there is no parameter
   of interest in that section. Should name inactivation pH, hold time and temperature (as
   Section 7.3 does).

2. "It judges XMuLV clearance at the least favourable combination of the other parameters
   within the normal operating range (NOR), because viral clearance is validated at
   worst-case conditions (Section 8)."
   Flagged: same unanchored "the other parameters", and in Section 1.1 the reader has not
   yet met any parameter of the step. Should name the three multivariate factors.

3. "Each such assumption is checked in the report of that step, and Section 7.2 describes
   the one that has changed a criterion of this step."
   Flagged: "the one" is a stand-in and the section label does the work. Should name the
   cation exchange aggregate clearance, whose confidence bound replaced the platform value.

4. "The results observed at the ends of the range studied are reported beside it for
   information."
   Flagged: "it" can be read as the predicted largest increase or as the platform worst
   case, and the two are the quantities being compared. Should name the predicted largest
   increase within the NOR.

5. "The check takes the largest increase that the model predicts within the NOR, with its
   one-sided 95 % confidence bound on the unfavourable side."
   Flagged (minor): "The check" is defined two paragraphs and one full table earlier.
   Should name the verification of the platform worst cases.

6. "The design follows the hold study of the low-pH pool in the A-Mab case study (CMC
   Biotech Working Group 2009)."
   Flagged: in a subsection headed "Hold study of the neutralized pool", "the low-pH pool"
   is ambiguous between the acidified pool and the neutralized pool of the low-pH step. The
   two are different matrices with different degradation chemistry, which is the point of
   the study. Should say which pool was held in the source study.

7. "The range of A-Mab concentration is supported by its own univariate data, judged
   against the criteria in Table 7.1."
   Flagged: the criteria are reached only by table label. Should name aggregate and acidic
   variants, which are the two the univariate study measures (see Q4 item 5).

Not flagged: the INV-001 findings, corrective action CA2, AMD-001, the SOP and AMV
numbers, and each study code are introduced with the thing they name in the same sentence
(for example "the re-test study S-VI-RET", "the method decision AMD-001", "Corrective
action CA2 of INV-001 amends each step plan with the criteria and the fragment method").
That is the document's strongest habit and it holds nearly everywhere.

## Table observations

**Title block (Field / Value).** The Title value breaks inside its parenthesis, so a line
ends "...Low-pH Viral Inactivation (Step" and the next begins "6)". The "Sponsor / sites"
cell joins two sites with an arrow that nothing in the document explains.

**Table 1.1 (Version 1.0 vs 2.0 criteria).** Header is three deep: the group row "Version
1.0 a) | Version 2.0" over "Criterion Rule | Criterion Basis", with the stub label
"Attribute" vertically centred between the two header lines, so it reads as part of the
header stack rather than as the first column's name. The footnote keys mix two schemes —
a) to d) by letter and R1 / R3 by rule code — in one list. The acidic variants row prints
"none" under the Criterion/Rule pair in a position that does not clearly belong to either
column. The aggregate Rule cell wraps as "R1, margin / 6.0", which can be read as two
values. Content versus text: the Version 2.0 basis "Carried back, tightened" is true only
against the a priori 10.0 % that appears nowhere in the table, while the visible
comparator is 2.17 %; the table therefore shows a number three times larger labelled
"tightened". Either the a priori value belongs in the table or the basis cell should say
tightened from the a priori platform value.

**Table 3.1 (Related documents).** The text above it says the table lists "the documents it
depends on, its paired report and the documents it rolls up into" — three categories,
where the table has four relationship types, the fourth being INV-001 "Reason for this
revision".

**Table 3.2 (SOPs and AMVs).** The grouped "Type" labels are vertically centred, so in the
rendered text "Standard" and "operating procedure" land beside SOP-1002 and SOP-2009
rather than at the head of their group, and "Analytical method validation" splits across
the AMV rows. The grouping is hard to follow and a reader scanning for where the SOP block
ends has no rule line to go on.

**Table 4.1 (Quality attributes in scope).** Header runs to three lines and the sub-headers
collide: "Tool #1 / score" and "Formed or / set at" are stacked in adjacent narrow
columns. The Category values split mid-word ("size / variant", "charge / variant") and are
lower-cased against the title-cased CQA column. Ambiguous column: "Tool #1 score" does not
order with "Criticality" (VH at 20, H at 60, L at 12, VL at 4), which contradicts the
caption and the text above it (see Q5 item 4); the column needs either the banding rule or
a note that viral safety is scored separately. The DS criterion cell for XMuLV mixes a
cumulative process requirement into a column of per-attribute limits. The attribute label
"Acidic charge variants (deamidation)" names a mechanism that Section 4.1 does not use for
this step (see Q5 item 7). The "Formed or set at" cell assigns XMuLV clearance to this
step although the requirement is cumulative across three steps, which the text then has to
qualify.

**Table 5.1 (Analytical methods).** The headers "Method validation" and "Method" are
adjacent and run together in the rendered line, so the AMV number and the method name read
as one field.

**Table 5.2 (Methods for size variants).** The aggregates row prints a single "SEC"
centred across the "Screening" and "Response surface" columns; with no visible merge it
can be read as belonging to neither. Footnotes are correctly placed: a) marks only the SEC
fragment cells and b) only the nrCE-SDS cell, and "Reported for information only" applies
to fragments and not to aggregate, as the text requires.

**Table 5.3 (Sampling plan).** The response-surface row carries a second study code inside
it ("Fragments by nrCE-SDS on the retained samples (S-VI-RET)") while Table 11.1 lists
S-VI-RET as its own phase; one of the two should fold. The Tests cell for that row ends a
sentence with a period and continues, which reads as two cells. Contradicts the text in
two places: the qualification and univariate rows test no fragments, against Section 5.3's
"every study at every step" (Q5 item 2); and the hold row samples fragments on three of
the five days, against Section 7.5's "every attribute" at the longest hold (Q4 item 6).
The hold row also gives no study date, so a reader cannot tell whether the hold study
preceded AMD-001 and therefore why its fragments needed retained samples.

**Table 6.1 (Parameters).** Header splits into "Range / studied" and "Study / type" in
narrow columns flanking "NOR", so the three right-hand headers run together. Six footnotes
for four rows, five of them superseding the values printed in the cells they mark, which
makes the table hard to read as the planned-values table it is meant to be. Inconsistent
figures for one value: the pH range studied prints "3.2-4" here and "4.0" in Tables A.1
and B.1. The A-Mab concentration row has "-" in the Code column, which is correct (it is
not a design factor) but is not explained in the table.

**Table 7.1 (Intermediate acceptance criteria).** Caption reads "...low-pH viral
inactivation output", which is not grammatical against the plural criteria; it should be
the outputs of the step. Two-level header "Downstream worst case" over "Clearance fold |
Increase" is fine, but "Increase" is 0.00 in every row and its meaning is carried only by
the unkeyed note "Increase, in the unit of the criterion" — a reader will take it for an
increase at this step, which is what Table 7.2 holds. "Clearance fold" is the wrong term
of art (clearance factor, or fold reduction) and does not say which step it belongs to.
The table uses two conventions for the same idea: "not applicable" spanning both
sub-columns for XMuLV, and a neutral 1.00 / 0.00 for acidic variants, where the footnote
says no downstream step changes the attribute. Footnotes otherwise match what they mark
(a) on the aggregate basis, b) on the acidic basis, c) on the cumulative DS value, d) on
the platform claim).

**Table 7.2 (Platform worst cases).** Header splits into "Largest / increase" and
"Criterion that / relies on it", and the first of those collides with "Platform source".
Label and values disagree in the last column: it is headed "Criterion that relies on it"
and the cells name steps ("Production bioreactor", "Protein A"), not criteria. The
"Platform source" cell for aggregates adds an external citation, "A-Mab Table 4.16", that
the other two rows lack, so the sourcing is inconsistent down the column, and the citation
is a bare table number into another document.

**Table 10.1 (Responsibilities).** No problems. The split of the PAR analysis between
MSAT ("analyses the data") and Statistics ("runs the PAR analysis") overlaps, but the
split is stated and not contradictory.

**Table 11.1 (Sequence of studies).** The merged phase label "3" prints between its two
studies, so S-VI-RSM sits visually under phase 2 and a reader scanning the Phase column
can mis-assign it. The caption says "the studies under this plan" but the last row is
PCR-006, the report, not a study, and Section 11 then says PCR-006 "reports every study in
Table 11.1", which includes PCR-006 itself. The hold study is placed before the nrCE-SDS
re-test although Section 6.5 says the hold samples are retained and re-tested by the same
method, and no study code covers that testing.

**Tables A.1 and B.1 (planned designs).** The "Setting" sub-headers split across three
lines ("Inactivation / pH", "Hold time / (min)", "Temperature / (C)"), so the units sit a
line away from the labels. In B.1 the axial block prints its coded levels with different
spacing from the factorial block and the "Axial" group label lands on run 11 or 12 rather
than at the head of the group. Both tables decode correctly at every row and the high pH
prints as 4.0, against "4" in Table 6.1.

## Seven answers for the document as a whole

1. Physical cause in the clause where the verb stands — **No.** Two sentences fail
   ("governs ... because the rate depends on it steeply"; "acts on aggregation, because
   association is a bimolecular event"). The rest of the mechanism writing passes.
2. Every technical term a term of art — **Yes.** Two local labels noted
   ("NOR-propagated", "clearance fold") but both are defined or transparent.
3. Any sentence that tells the reader how to file the finding — **No**, no sentence does
   this. Three near misses are listed with the reason each survives.
4. Every criterion with its basis, every decision rule unambiguous — **No.** All criteria
   carry a basis, but eight decision rules cannot be applied as written: the residual
   condition, the refit rule's coverage and discretion, the Monte Carlo spread, the
   criticality threshold, the univariate judgement against four criteria when two are
   measured, the hold rule against a three-day fragment series, the two-sided acidic
   criterion, and "at manufacturing scale" for an attribute with no offset.
5. Anything wrong, inconsistent, or contradicted by a table — **Yes**, nine items. The
   material ones: the scale-down model cannot be qualified before the runs its own
   qualification rule needs (Table 11.1); "nrCE-SDS in every study at every step" against
   Table 5.3; antibody concentration asserted to have no effect on inactivation while
   representativeness rests on pool composition; Table 4.1's Tool #1 scores not ordering
   with its criticality bands; the mean prediction used in the first PAR analysis against
   Section 5.5's prediction-interval rule; and two loose mechanisms (lipid-envelope
   disruption, succinimide as the acidic species).
6. Reads as written by a process scientist throughout — **No.** Two sentences flagged
   (the "confirms and bounds known behaviour" summary, and the fourth restatement of the
   Version 1.0 values point).
7. Every sentence understandable standing alone — **No.** Seven sentences flagged, five of
   them for "the other parameters", "the one", "it", "The check" and "the criteria in
   Table 7.1" standing in for things the sentence should name, and one for "the low-pH
   pool" in a subsection about the neutralized pool.
