# Content review run 2: PCP-007 Version 2.0 (cation exchange plan)

Judge: Claude Opus 5.5 (claude-opus-5-5), fresh context, read only `PCP-007_cex.DRAFT.run2.txt` (101 quotes
checked word for word; one simulation of the Cook's cut-off). Returned as text; saved by the coordinator
(condensed). Answers: 1 No, 2 No, 3 Yes, 4 No, 5 Yes, 6 No, 7 No. Resolutions: `feedback-PCP-007.final.md`.

## Amendment rule
1. Qualification details added after the qualification runs ("This plan also names the outputs compared and the
   number of runs at each scale"; the five outputs; "3 scale-down runs at set-point against 5 A-Mab batches")
   [coordinator: a PCMP-001 §7.1 requirement; attribute it].
2. A studied factor redefined after the runs (thresholds "read as absorbance (OD280), not relative to the peak
   maximum"; equal load and wash conductivity a design choice) [coordinator: Version 1.0 Table 6.1 set OD units;
   say the description now matches the design].
3. Expectations rewritten with the data known (§4.1 host cell protein and leached Protein A pI; host cell
   protein held by association with the bound antibody; monomer lost at both edges; §12 first assumption).
4. The elution pH range rationale rewritten (lower severity).
5. Equipment and calibration record (borderline; PA3).
6. "which is acceptable because the derivation of its criteria uses no result" (twice; self-certification).

## Q1
"Protein load and load/wash conductivity act on the same host cell protein"; "protein load acts with the
load/wash conductivity to set how much weakly bound host cell protein survives the wash"; "the weakly bound
remainder is displaced during the wash" (the wash is at the load conductivity); "all three falling as load
rises" (yield needs breakthrough); "leached Protein A stays unbound" (circular); "since its expected effect on the
separation is small" (flow-rate assignment).

## Q2
"carries the fit" (influential run); "single-batch limit"; "operating region", "declared region"; "NOR-propagated
analysis", "set-point PAR"; "a discrepancy from the plan and not a deviation"; "ambient temperature control"
(controlled room temperature); "identity and quality controlled inputs"; "residence time of the antibody in the
pores"; "The register" (unnamed); "analytical method decision".

## Q3
"This is the Version 1.0 rule for a factor left out of the response-surface design." / "... for an effect of the
flow rate."; "That bound is the one A-Mab value in the criteria of this step."; "which Version 1.0 also calls the
declared region"; the two "acceptable because" sentences.

## Q4
The flow-rate range has no rule against the criteria and the plan does not say it sets none; the flow-rate study
measures no fragments; "The declared region will lie inside the ranges studied ..." (an outcome stated as given);
"the campaign" as the only basis of the residual tests.

## Q5, major
1. "A response-surface model is used for prediction only if it passes the four tests of PCMP-001 §7.2" vs §7.6
   (the fourth does not decide a widening) and Table 1.1 note b "on an adequate model".
2. Cook's 4/n as a pass mark rejects almost every model (99.4 % of correct fits flag a run; leverage 0.50–0.66
   away from the centre); a cut-off near F(0.5; 15, 13) = 1.0 is usual.
3. Leached Protein A "do not bind under load conditions" vs the platform worst-case clearance of 3.16 (Table 7.2);
   Protein A–IgG complexes bind with the antibody.
4. Host cell protein "not retained by the sulfonate ligand" vs the "weakly bound remainder" and the clearance of 40.
5. The flow-rate rationale (no interaction with the collection window) vs an absolute OD threshold.
6. Peak broadening as the route for load × conductivity vs §4.1.
7. "an effect smaller than that spread will not be claimed" vs significance at p < 0.05.
8. The assay-variability rule (anti-conservative; Version 1.0 wording).
9. An absolute absorbance threshold is not scale-independent (flow-cell path length).
10. Fragments not tested in the load although Table 7.2 needs a fragment clearance factor.
11. The sequence vs Table 11.1 (weekend gaps between qualification, screening and response surface).
12. Two bases for the control strategy (PAR intersection vs the region).
13. Two rules for the operating region (the Version 1.0 mean rule beside the single-batch rule).
14. The PAR margin does not measure the distance to the region.
15. Calibration recorded for one study only.
16. INV-002, PCR-008 and AMD-001 missing from Table 3.1.
17. "Execution may begin once the plan is approved ..." vs approval after the runs.
Minor (18–32): four sample points vs five fractions; the parameter count; load and wash "cannot be varied
independently"; changes 2, 10, 11 name no PCMP-001 rule; the capability simulation without run-to-run variance;
"held at defined settings" vs the NOR-propagated PAR; the narrower-range reason; the set-point PAR on the mean;
fragments judged at scale-down scale; Table 1.1 note c "did not report fragments"; "establishes the mechanisms"
vs assumption; ranges resting on offsets from batches not made under this plan; elution by raising pH (low
confidence); higher conductivity lowers dynamic binding capacity; the criticality continuum citation.

## Q6
"Assay variability enters the analysis at two points and is handled at both."; "It answers what one parameter can
do ..."; "The reported proven acceptable range is the contiguous interval ..."; "In both directions the bound
replaces the platform value ..."; the augmentation rule that cannot be triggered (Version 1.0 text: say so);
"This section states the criteria that will be applied."; "decided at analysis" three times; "The risk
assessment RA-001 set the scope of this study."; the late-approval sentence repeated.

## Q7
"One criterion of this step uses a verified A-Mab value ..." (name host cell protein and the 4.27 bound); "Its
corrective actions are applied by the report PCR-007" (name them); "Version 1.0 of this plan reported a response
..." (a plan reports nothing); "single-batch limit"; "not one buffer"; "The register assigns no quality attribute
..."; "A prediction interval of a single run is exact."; the quoted fragments of the §7 no-threshold list (name
each decision); "An assumption is confirmed when ..." (name it); "The scale-down model is qualified by its offset."
(name the test); "A check changes a criterion upstream ..." (name the check); "Objective 6 ..."; RA-001, PCMR-001
and PCR-007 used as subjects without being named.

## Tables
1.1 (rule codes; the Basis cell crammed; "not assessed" in a criterion column); 7.1 (header; platform value and a
priori criterion missing; "1.00 / 0.00"); 5.1 (samples and timing); 4.1 ("Tool #1"); B.1 (axial rows alignment).
