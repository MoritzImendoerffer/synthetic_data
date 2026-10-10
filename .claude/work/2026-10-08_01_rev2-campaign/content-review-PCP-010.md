# Content review run 1: PCP-010 Version 2.0 (UF/DF plan)

Judge: Claude Opus 5.5 (claude-opus-5-5), fresh context, read only `PCP-010_ufdf.DRAFT.txt`. Returned as
text; saved by the coordinator 2026-10-10. L = line number in the .txt file. Quotes join words split by
hyphens at PDF line breaks.

## Step-specific rules or execution details added after the data

No clear case. Where Version 2.0 sets no rule the plan says so and leaves the approach to PCR-010 (the
qualification decision L727-730, the threshold for a "small" change L784-786, the classification
threshold L802-805). Four items need their origin stated:
- L479-481 "Under PCMP-001 §7.1 the offset of each output is the mean of the scale-down runs at
  set-point minus the mean of the manufacturing-scale batches, so the commercial batches of that record
  are the reference." Version 1.0 compared against "the pilot and commercial record"; dropping the
  pilot batches is a step-level reading chosen after the runs; no number of batches.
- L483-484 "The qualification runs are made, and the offsets estimated, before the first
  characterization run of the step." (also Section 11 item 1). Prospective wording in an amendment
  issued in September; Version 1.0 accepted the model by an equivalence test. State as a fact when the
  offsets were computed.
- Decision rules outside §7.3 not marked as Version 1.0 text: the extension trigger (L446-448), the
  pilot-scale repeat (L943-945), the rule that attributes noise to the assay (L952-954), and "Analytical
  Development will report the method variability over the range in which the samples fall." (L578-579,
  reads as written with the results in hand).
- The buffer-exchange criterion "at or below 7 DV" (Table 5.1, L761-763): if not from Version 1.0, a
  step-specific criterion added after the data.

## Q1 Physical cause in the causal clause
- L461-463 "The model holds the membrane loading and the crossflow at their commercial values, because
  together they decide what the antibody meets in the step." (name wall concentration, shear, residence
  time)
- L411-412 "This step adds no protease, and its mechanical route acts on aggregate." (no species or
  interaction; ignores the time-driven chemical route)
- L431-432 "The step sets no CQA of its own, and its three parameters act on the product by the
  different routes described below." (cause deferred)
- L575-576 "Aggregate in the load of this step is expected to be low, because the cation exchange step
  before it is the principal aggregate reduction step of the train." (role, not the interaction:
  aggregate binds the cation exchanger more strongly than the monomer)
- L677-678 "The range extends above the NOR because pressure above the flux limit compresses the
  polarization layer without raising throughput." (why high TMP is useless, not why it is risky)

## Q2 Terms of art
- L825 "The NOR-propagated analysis of PCMP-001 §6.4 is not performed." (coinage)
- L946-948 "...comparing the responses against the pure error band of Section 5.5." ("pure error band"
  not a term of art; also L627, L954)
- L210-212 "...through the platform worst case of every downstream step." (house jargon)
- L234-235 "The method decision AMD-001 of 2026-03-20 sets non-reduced CE-SDS (nrCE-SDS) as the method
  for fragments wherever they are measured (PCMP-001 §7.8)." ("method decision" not a document type)
- L180-181 "The step forms no quality attribute of A-Mab, and no clearance of any attribute is credited
  to it (Section 4.2)." and L431 "The step sets no CQA of its own" ("forms/sets a quality attribute" not
  standard usage)

## Q3 Filing glosses
- L215-216 "INV-001 finding 1 therefore moves no criterion of this plan."
- L230 "Neither rule changes what this plan decides."
- L236-237 "The studies of this step do not measure fragments (Table 5.2), so the decision changes no
  method of this plan."
- L246-247 "This step has no designed experiment, and INV-002 changes nothing in this plan."
- L382-383 "The criticality level is assigned separately and is not read off that score."
- L628-630 "A slope that is significant at α = 0.05, but predicts a change across the range that is small
  against the acceptance criterion, is described in those terms."
- L737-738 "The acidic charge variants must lie within 18–40 %, so both ends of that range apply."

## Q4 Criteria with basis
- L446-448 "Where a measured attribute approaches its acceptance criterion at an edge, the study should
  be extended to the combination of edges before a range is claimed." ("approaches" has no threshold)
- L761-763 "The buffer exchange is accepted when the conductivity and the pH of the retentate have
  reached the plateau of the formulation buffer, by the analysis of Section 5.5, at or below the lower
  edge of the diavolume NOR, 7 DV." (no target, no tolerance, no failure rule)
- L332-334 "...the number is set to bring them below what the formulation tolerates." (no value)
- L773-774 "A parameter passes over its range studied when every level in the range is acceptable and
  the change measured across the range is small against the criterion." (no threshold; L784-786 does not
  say PCR-010 decides)
- L952-954 "Noise near the low end of the method range will be attributed to the assay and not to the
  parameter under study, unless the change measured across the range is larger than the pure error band
  of Section 5.5." (no basis)

## Q5 Scientifically wrong or internally contradicted
- L348-350 "...a higher TMP compresses that layer without raising throughput, and it raises the
  concentration and the shear that the antibody meets at the wall." (wall shear is set by crossflow and
  channel geometry, not TMP)
- L463-465 "The membrane loading, in grams of antibody per square metre, fixes the bulk concentration
  that the step reaches and the time that the antibody spends on the skid." (Table 6.1 varies final
  concentration 65–85 g/L at fixed loading; diavolumes set the duration, L358-359; TMP sets the flux)
- L520-522 "...the membrane loading holds the time on the skid at its commercial value." (Table 6.1
  varies DV and TMP, so the time differs between runs)
- L485-487 "Only the change in aggregate bears on a criterion of this step, because aggregate in the
  final retentate is judged against the drug substance criterion (Section 7.2)." (Table 5.1: acidic
  variants 18–40 % and buffer exchange also carry criteria)
- L748 "The acidic charge variants have no offset, and each result is judged as measured." (Table 5.1
  "the offset is unknown"; L515-516 "unknown, not zero")
- L631-633 "No response-surface model is fitted for this step, because the design has no factorial
  structure and no interaction or curvature term can be estimated from it." (three levels per parameter
  with a replicated set-point allow curvature per parameter; only interactions cannot be estimated)
- L670-671 "Each range studied is wider than the corresponding NOR in the direction in which the risk
  lies." (low TMP lengthens the operation: more pump passes, more deamidation; incomplete buffer
  exchange lies below 7 DV, where the range does not extend)
- L749-750 "The derivation in PCMP-001 credits no step after cation exchange with a change in aggregate,
  and no step after low-pH viral inactivation with a change in acidic variants." (conflicts with
  Sections 4.1 and 4.2, which say this step adds both)
- L180-181 (quoted under Q2) contradicted by L337 "The step can add to aggregate and to the acidic charge
  variants"
- L410-411 "They are formed by proteolytic clipping of the antibody, in culture and during the harvest
  hold (PCMP-001 §3)." (incomplete: non-enzymatic hinge hydrolysis proceeds with time; co-purified
  proteases not excluded)
- L404-406 "The membrane separates by size, and the glycan variants of the antibody are the same size,
  so the step cannot change their distribution." (glycoforms differ slightly in mass; the reason is
  that the membrane retains every glycoform)
- L943-945 "If aggregate fails its criterion at bench scale, the condition will be repeated at pilot
  scale before an operating range is narrowed on the strength of the bench result." (contradicts §7.3
  rule 3 and rule 5)
- L952-954 contradicts L623-624 "An attribute is called affected by a parameter when that slope is
  significant at this level." (two tests for an effect)
- L801-802 "A significant effect that is too small to move an attribute appreciably within its PAR does
  not by itself make a parameter critical (PCMP-001 §7.7)." (conflicts with L623-624 plus L798-799)
- L816-818 "The PAR of a parameter is the contiguous span of levels over which every attribute measured
  on the final retentate met its criterion, with the other parameters at their set-points." (leaves out
  rule 2's "small against the criterion")
- L553-555 "These are in-process measurements read from the skid instruments." (Table 5.3 lists them as
  "Diafiltration samples")
- Weakness: three runs per series give one residual degree of freedom for a slope test.

## Q6 Machine-like
- L396 "It carries a criticality of H, and its criterion is ≤ 5 % HMW (SEC)." and L396-397 "The acidic
  charge variants carry a criticality of VL and a criterion of 18–40 %." (restate Table 4.1)
- L418-419 "Viral clearance is not measured, for the reason given in Section 1."
- L705-706 "The design gives no estimate of an interaction between parameters." (repeats L443-444)
- L805 "The classification is an outcome of the studies and is reported in PCR-010."
- L869-870 and L920-921 (second and third tellings of the approval date, L192-193)
- L980-981 "Version 2.0 is issued after the runs it governs, under INV-001, for the reasons given in
  Section 1.1."
- L747 and L815-816 (third and fourth tellings of the offset subtraction)
- L681-683 "...it has to be dispositioned as readily as an excursion above it."
- L412-418 "The derivation of PCMP-001 credits no step after virus filtration with a change in
  fragments (Table 7.1)..." (roundabout for "this step")

## Q7 Codes or abstract stand-ins
- L199-201 "This amendment is issued under corrective action CA2..." (name the action)
- L215-216 (name the finding that criteria were set after the data were seen)
- L852-853 "INV-001 preventive action PA3 requires both in every study record." (name the execution
  window and calibration status)
- L401, L535-536, L962-963 "Step 9" (name virus filtration); "(Table 7.1)" means PCMP-001's table, which
  this document does not have (also L407-409, L417)
- L395-396 "...by the mechanical route of Section 4.1." (name pump shear and wall concentration)
- L680-681 "...the aggregation risk of Section 4.1." (name viscosity and wall concentration)
- L561-562 "...for the reason given in Section 4.2." (state it)
- L657-658 "...for the reasons given in Section 4.3." (name the low RA-001 ranking and no likely
  interaction)
- L722-723 "...as Section 5.1 describes (PCMP-001 §7.1)." (say subtracted from aggregate, recorded for
  the others)
- L701-702 "...the panel of Section 5.3." (name SEC, A280 and icIEF)
- L825 (name the prediction at combined NOR edges from a fitted model)
- L461-463 "what the antibody meets" (abstract)
- L516-517 "...its representativeness rests on the mechanism." (name deamidation kinetics and buffer
  passage)
- L353-354 "...the exposure is brief..." (name the time at high wall concentration and pump passes)

## Tables
- Table 5.2: the whole body is one merged "no DoE" cell; replace with a sentence.
- Table 6.1: constant "Study type" column; Table A.1 repeats Table 6.1.
- Table 11.1: constant "Equipment" and "Next calibration due" columns.
- Table 4.1: no legend for "Tool #1"; "(CEX/icIEF)" uses CEX for an assay while the abbreviation list
  defines CEX as the step; "Category" repeats the CQA names.
- Table 3.1: omits INV-002.
- Table 5.1: the buffer-exchange criterion has no numerical value.
- Table 5.3: "Diafiltration samples" are skid readings.

## Answers
1 No. 2 No. 3 No. 4 No. 5 Yes. 6 No. 7 No.

## Coordinator note (2026-10-10)
Some Q2 flags are corpus conventions defined in PCMP-001 (platform worst case, NOR-propagated analysis,
the method decision AMD-001); a fix pass should define them at first use, not drop them. Several Q4
flags concern Version 1.0 rules the amendment must keep (STORY_BIBLE §9b); the fix is to mark them as
Version 1.0 text, not to change them.
