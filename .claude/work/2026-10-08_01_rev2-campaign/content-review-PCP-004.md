# Content review run 1: PCP-004 Version 2.0 (harvest and clarification plan)

Judge: Claude Opus 5.5 (claude-opus-5-5), fresh context, read only `PCP-004_harvest.DRAFT.txt`. Returned as
text; saved by the coordinator 2026-10-10 (condensed; every flagged sentence kept). Answers: 1 No, 2 No,
3 fail, 4 No, 5 fail, 6 No, 7 No.

## The problems that matter most
1. The plan says no conclusion depends on the scale-down offset, yet judges clarified-harvest turbidity
   against an absolute 10 NTU limit on an output whose offset it calls "unknown, not zero".
2. Criterion 1 compares clarified harvest with unclarified culture, putting the charged depth filter
   (which adsorbs DNA, per the document) between release and measurement; the plan also says the step
   "does not clear" host cell protein and DNA.
3. HMW by SEC-HPLC on crude culture and harvest, although the document records that SEC misreads samples
   that still carry host cell protein.
4. The model cannot show the lysis side of the rcf series: shear comes from a separate device at one
   dissipation rate.
5. The turbidity series has no working criterion; its 20 NTU level fails criterion 2 by construction.
6. Several statements added after the data were known (Q4b).

## Q1 Causes without a physical cause
- "The culture conditions that set the impurity burden entering harvest."
- "Two mechanisms limit the centrifuge, and they act in opposite directions." (also Q7)
- "For this reason the parameter is expressed as load per unit area, in L/m2." (solids mass per area
  does not give a volume unit; also Q5)
- "It is a property of the clarified harvest, which the centrifugal field and the filter load produce
  together." (no direction)
- "It is monitored on every batch as an in-process control, and it is listed among the parameters of the
  step because its value bounds what capture receives." (name the particulate and colloid load that
  fouls the Protein A bed)
- "Both mechanisms act in one direction only, and neither can lower an attribute that the step does not
  form." (also Q2, Q3, Q5)

## Q2 Terms
- "The step forms no quality attribute of the antibody." and "The step forms no quality attribute, so a
  parameter of the step can reach an attribute in only two ways." (attributes are measured; species are
  formed; "reach an attribute")
- "It can also unfold the antibody at a shear or air-liquid interface, which raises the HMW content."
  ("shear interface" is not a term; hydrodynamic shear alone is not an established cause of IgG
  unfolding; interfaces are)
- "...that size exclusion chromatography (SEC) reads fragments high in samples that still carry host cell
  protein." (SEC overestimates LMW species where host cell protein co-elutes)
- "Capture is used in this study only as a fixed test of the material that harvest delivers (Section
  6.2)." (Protein A load challenge at set-point conditions)
- "PCR-004 records it as a discrepancy from the plan." (coordinator: corpus convention, owner's decision;
  keep, define once)
- "AMD (analytical method decision)"; Table 5.1 header "Method share of variance" (analytical variance
  component as a percentage of total variance)

## Q3 Filing glosses
- "This agrees with PCMP-001 §7.6, under which a PAR that reaches the edge of the characterized range is
  reported as reaching it."
- "Its precision still matters, because the turbidity criterion is an absolute limit and not a comparison
  with a reference sample."
- "A null result is required here, not a bounded one." (also Q5)
- "The host cell protein ELISA is the less precise of the two methods in Table 5.1, and criterion 1 of
  Section 7 is written against its precision, not against a fixed percentage." (also Q5, Q7)
- "Both mechanisms act in one direction only, ..."

## Q4 Criteria and their basis
(a) Without an adequate basis:
- "The turbidity of the clarified harvest will be compared with the upper NOR limit of post-clarification
  turbidity, 10 NTU." (circular: the NOR is what the study justifies; no link to Protein A fouling)
- "A level passes when no increase is detected at α = 0.05, or when a detected increase is smaller than
  the precision of the method that measured it (Section 5.3)." (DNA method precision not given;
  relative or absolute; no link to the zero change the derivation credits)
- "Table 5.1 gives the validated performance of the turbidity and host cell protein methods, on which
  criteria 1 and 2 of Section 7 depend." (criterion 1 also depends on AMV-3014)
- "The responses are the pressure developed across the column over the load and the yield of the cycle."
  (no criterion judges them, and the plan does not say it sets none); "A parameter meets the criteria
  over a range when every level in that range passes criteria 1 to 3." (the turbidity PAR does not come
  from its own data)
- "The HMW content will be compared before and after the step, and a level passes when no increase is
  detected at α = 0.05." (non-significance does not show no increase)
- "The set-point condition will be run in replicate, spread across the execution of the study, and those
  replicates estimate the variation between runs against which every effect is tested." (number of
  replicates never stated)
- "Where the relationship is not linear over the range, a quadratic term may be fitted, and the fit will
  be reported with the terms that were needed." (no test for non-linearity; not left to the report)
- Table 4.1 gives drug substance criteria with no source.
(b) Added after the data were known (amendment rule):
- "The qualification runs are made, and the offsets estimated, before the first characterization run."
  and Table 11.1 Phase 1 "The offset of each output compared is estimated before the first
  characterization run." (present-tense execution claim in a plan issued ten months later)
- "It also replaces the Version 1.0 requirement that the qualification be reviewed and accepted before
  the first characterization run." (deletes a Version 1.0 gate after the fact)
- "The turbidity of the clarified harvest is judged against an absolute criterion as the model gives it."
  (a step-only rule exempting the one absolute criterion from the offset rule)
- "The record lists no instrumented scale-down system under calibration and change control for this study
  (PCMP-001 Table 5.1)." (execution detail; also Q5, Q7)
- "Work that this plan does not foresee, made without a departure from a procedure, is not a deviation."
  (not listed as a change; contradicts Section 13)
- "...the verification of platform worst cases (PCMP-001 §7.5) has nothing to check at this step."
  (exempts this step)

## Q5 Wrong or contradicted
Major:
- "The step does not clear them and is not credited with clearing them." (Table B.1, Sections 4.1, 5.3,
  5.5, 12(5): the media adsorb DNA)
- "None of the four is formed by the centrifuge or the filters." (Sections 4.1, 12(6) "aggregate formed by
  shear", 4.3 unfolding raises HMW; 4.2 clipping continues in the clarified harvest); same for "The step
  forms no quality attribute of the antibody."
- "The step forms no quality attribute, so a parameter of the step can reach an attribute in only two
  ways." (leaves out DNA adsorption depending on filter load, and clipping during the operation)
- "For an output with no criterion at the step, PCMP-001 §7.1 requires only that the offset be recorded,
  and no conclusion depends on it." (criterion 2's 10 NTU limit applies to an output whose offset is
  unknown; Table 11.1 note a repeats it)
- "Cell damage in the feed zone is reproduced in a bench shear device run at the energy dissipation rate
  calculated for the commercial feed zone." and "A setting in g therefore means the same thing at both
  scales." (one dissipation rate; a batch laboratory centrifuge has no feed zone; g varies with radius in
  a disk-stack bowl)
- "The qualification compares the model with the commercial train at the set-point condition, on the same
  culture, with replicate runs at each scale." (the step runs once per batch on one 15,000 L bioreactor;
  §5.1 "the mean of the commercial batches"; also Table 11.1 Phase 1)
- "Size variants by SEC-HPLC (AMV-3011) measure the HMW content of the antibody before and after the
  step." (SEC misreads samples carrying host cell protein; crude culture and harvest normally need
  Protein A purification first)
- "Host cell protein and residual DNA in the clarified harvest will be compared with the same
  measurements on the unclarified culture that produced it." (nets release against depth-filter
  adsorption; release shows at the centrate; cell removal step needed)
- "The criteria of the production bioreactor are therefore carried through harvest unchanged, and the
  verification of platform worst cases (PCMP-001 §7.5) has nothing to check at this step." (Section
  12(6): the criteria rest on the no-impact assumption, criteria 1 and 3 test it; criterion 1 accepts an
  increase up to 9.5 % the derivation does not credit)
- "A null result is required here, not a bounded one." (non-significance is not evidence of no change)
- "The model is qualified by its offset from the commercial train, as PCMP-001 §7.1 sets out, and not by a
  test of equivalence (Section 5.1)." (the Version 1.0 test was of difference, not equivalence)
- "Clarified harvest at a target turbidity will be prepared by blending clarified harvest with retained
  centrate to the turbidity of the level." (the blend bypasses the sterilizing-grade filter before
  capture)
- "The set-point column gives the condition at which every parameter not being varied is held, and at
  which the replicate runs of Section 5.4 are made." (turbidity "is not a set parameter")
- "All 3 parameters of the step were assigned univariate study, as the study type column of Table 6.1
  records." (feed rate or flow to sigma factor, flux, temperature, hold time neither studied nor excluded
  with a reason); "Every parameter not varied in a run will be held at its set-point (Table 6.1)."
- "For this reason the parameter is expressed as load per unit area, in L/m2." (volume per area)
- "A change in host cell protein across a parameter range that is smaller than this precision will
  therefore not be reported as an effect (Section 5.5)." (§5.5: "reported as detected and not material")
- "The step is not expected to change the size-variant profile, and the intermediate points would not
  locate a change if one were found." (the centrate point would)
- "The time from the end of culture to the end of clarification will be the same in every run, since a
  longer hold of unclarified culture allows further lysis and would confound the comparison." (later
  series use retained centrate)
- "Equipment used to set or to measure a parameter will be within its calibration at the time of use, and
  its calibration status will be recorded with the run." (Section 11: no instrumented system listed)
- "Work that this plan does not foresee, made without a departure from a procedure, is not a deviation."
  (Section 13)
- "Four of the validated methods in Table 3.2 report the responses of the study." (step yield needs an
  antibody concentration assay; none listed)
- "The filter is then challenged with both extremes of the solids load it can receive." (higher field
  makes fine debris; response need not be monotone; viability also changes the load)
Minor: "The decisions of Section 7 rest on the size of an effect against the precision of its method..."
(only criterion 1); "An effect smaller than the method can resolve will be reported as detected and not
material" (contradiction in terms); "<LOQ" excluded from the regression (biases the slope); "Residual DNA
is the response most likely to be affected, because the depth filter media adsorb DNA and the assay then
reports a small quantity." (DNA in clarified CHO harvest is far above a qPCR LOQ); "...not against a fixed
percentage" (9.5 % is fixed); "...a particle that has not reached the wall..." (in a disk stack particles
are captured on the discs); "Shear in the feed zone and at the disc stack rises with the speed of the
bowl." (flow between discs is laminar, low shear); representativeness also rests on the model centrate;
turbidity range lower edge equals the NOR low; objective 4 circular; Tool #1 sentence vs Table 4.1 "CQA"
heading; "it is the attribute that rises most when cells break" (unsupported); "The NOR will be shown
inside the PAR." (presupposes the result); "well beyond the upper NOR limit of 140 L/m2" (160 is 14 %
above); ICH Q10 does not require the wider ranges; the responses list omits filter pressure and the
Protein A responses; Table 3.1 omits INV-002, PCP-003, PCP-005, PCR-005; revision history lists "a priori
intermediate acceptance criteria" though the step has none.

## Q6 Machine-like
"What it decides is the condition of the feed to Protein A capture."; "The rows of Table 6.1 carry the
design in different ways."; "Host cell protein and aggregate carry most of the weight."; "The set-point is
a compromise between the two, and the centrifugation (rcf) series of Section 6.2 is designed to show where
each side of that compromise begins to matter."; "Aggregate carries the highest score of the four and
residual DNA the lowest."; three sentences restating Table 5.1; "Table 5.2 gives the method for size
variants in the designed studies of the step, as PCMP-001 Table 7.3 records it, and harvest has no
designed study."; the textbook definition of an interaction; no IAC stated six times; "Fragments are not
a response of this study." three times; the response-surface exclusions restated; Section 8 repeats
Section 5.5; the approval date restated; "The drug substance criteria of Table 4.1 are not in-process
limits for the clarified harvest (Section 4.2)."

## Q7 Not standing alone
The revision-history cell (name what each investigation was about); "Version 2.0 is issued after that
study ran, under the QA investigation INV-001." (name its subject); "The revision history also names the
second investigation INV-002." (name its subject); "...the hold study S-HAR-HLD and the univariate study
S-HAR-UNI2 were made at this step." (say what was held and varied); "...SOP-2005 and SOP-2006 govern the
two stages of the operation..." (name centrifugation and depth/sterile filtration); "...characterized
under PCP-003." (the production bioreactor plan); "The study tests the assumption at the two points where
the mechanisms above could make it untrue." (name lysis release and shear aggregation); "...so that both
sides of the compromise are reached." (name better clarification and more lysis); "The model reproduces
each stage of the commercial operation on the quantity that drives its mechanism..." (name energy
dissipation rate, rcf with flow to sigma factor, flux with L/m2); "AMV-3020 is listed in Table 3.2 because
the register assigns fragments to this step." (the drug substance CQA register); "...the quantity that
the bracketing arrangement of Section 5.5 varies." (name the filter load series on 6,000 g and 12,000 g
centrate); "One interaction is expected from the mechanism." (rcf × filter load via solids carried over);
"Criteria 1 and 3 compare results within a run, and criterion 2 is absolute." (name them); "The two PAR
analyses of the master plan PCMP-001 §6.4 evaluate a response-surface model..." (name them); "...for the
reason given in Section 5.1, and the model is expected to understate cumulative shear." (name
intermittent discharge and repeated passes through the feed zone); the execution-window and scale-down
system sentences (name the record; say what the missing system means); "It will give the reason for each
class from them." (ambiguous "them").

## Tables
Table 3.2 Type cells break across rows (merge); Table 4.1 split category cells, narrow criterion column
("≤ 5 % HMW (SEC) H" runs together), "CQA" heading for non-critical attributes, DNA per dose with no dose
stated; Table 5.1 three-line header with fused marker ("variancea)"), precision and LOQ run together, no
precision type, no rows for AMV-3014 or AMV-3011; Table 5.2 every cell "no DoE"; Table 6.1 constant Study
type column, mixed number formats ("9,000" vs "6000–12000"), a set-point for a parameter that is not set;
Table A.1 repeats Table 6.1, "1 | 1" turbidity cells, omits the doubled filter load series and replicate
numbers; Table B.1 methods as AMV codes with no legend.

## Coordinator note (2026-10-10)
Several Q4/Q5 flags concern the Version 1.0 design, which the amendment must keep (STORY_BIBLE §9b): the
fix is to state them accurately (and mark Version 1.0 text), not to redesign the study. The harvest
scale-down question is now an owner decision (Q8, 2026-10-10: a disk-stack centrifuge has no laboratory
scale model, only pilot scale; PCR-004 records the missing qualification as a deviation).
