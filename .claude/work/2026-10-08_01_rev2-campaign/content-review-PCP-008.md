# Content review run 1: PCP-008 Version 2.0 (anion exchange plan)

Judge: Claude Opus 5.5 (claude-opus-5-5), fresh context, read only `PCP-008_aex.DRAFT.txt` (plus one
simulation of the Cook's rule on the planned design). Returned as text; saved by the coordinator
2026-10-10 (condensed; quotes kept). Answers: 1 No, 2 No, 3 three minor cases, 4 No, 5 errors found,
6 No, 7 No.

## Q1 Causes
- "The two parameters therefore act on the same binding equilibrium from opposite sides, and an
  interaction between them is expected." (opposite effects do not cause an interaction; the salt needed
  to screen a host cell protein rises with the net negative charge a higher pH gives it)
- "The conductivity of the load acts by the same shielding, but during loading, when the impurities
  compete with each other for the ligand." (no direction)
- "Protein load acts through the impurity mass that comes with the antibody." (no direction in clause)
- "Its range is bounded by the composition of the cation exchange pool that the previous step delivers."
  (name the salt concentration of the CEX eluate)
- "...because they act on the same binding equilibrium and their interaction is the route by which
  impurity breaks through." (abstract; low pH and high conductivity together weaken binding of acidic
  host cell proteins, so they flow through)
- "The spiking model is qualified separately, because a virus spike changes the load itself." (a spike
  adds medium, protein and salt, can shift concentration, pH, conductivity)
- "The step sets one critical quality attribute, the cumulative clearance of MVM, and clears four
  others (Table 4.1)." (no mechanism)
- "The governing parameter is the multivariate parameter with the largest main effect..." (a ranking,
  not a cause)
- "That changes the charge distribution of the species this step must bind, and so it can change what
  the step clears." (wrong species, no direction; see Q5.12)
- "...because the separation is by charge and the platform buffer system is unchanged." (A-Mab's pI
  against the load pH range decides transfer)

## Q2 Terms
"NOR-propagated analysis" (coined; coordinator: PCMP-001 term, define at first use); "The set-point
range is reported beside it." (coined); "governing parameter" (coined); "release profile of the cation
exchange pool" (an intermediate is not released; in-process limits); "sets a CQA"; "fine structure of
the antibody" (spectroscopy term; over-general); "step floors" (minimum step log reduction factor);
"breaks through" misused; "Its capsid is also acidic at the load pH" (net negative charge); "spiking
model", "characterization model" (coined names for the scale-down model); "integrated model" (integrated
process model); "Design spaces" (the plan defines a multivariate operating region); "characterization
range" vs "range studied"; "blur".

## Q3 Filing glosses
"This cut-off is a common convention that falls as the design grows..."; "For this reason the study is
expected to confirm and bound behaviour that is already understood."; "The register assigns it to this
step, although its cumulative requirement is met by the claims of this step and of virus filtration
together (PCMP-001 §7.4)."

## Q4 Criteria and basis
"Load material is representative where its charge variant profile ... fall within the release profile
of the cation exchange pool." (no limits, no source); the second-lot comparison (no criterion, no
consequence); "the spiked load matches the unspiked load ... and the spike volume stays below the
fraction at which these properties move" (no tolerance); "Should the assessment show an effect of flow
rate on any response..." (no criterion for an effect; three runs give no error estimate); "An apparent
effect on a log reduction factor that is small against the variability of the infectivity assay will be
attributed to the assay..." (no threshold; overrides α = 0.05); Cpk between 1.00 and 1.33 (no decision);
"The upper end of the load pH range lies below the pH at which part of the antibody would start to
bind..." (no basis: pI or yield data); "The study is complete when ..." (nothing on failure); objective
"Show that the step meets its platform claims..." (worded as the result: "Determine whether"); "Invalidated
under deviation DEV-008-01." (not tied to the criterion it failed).

## Q5 Wrong or contradicted (most serious first)
1. "Version 1.0 did not measure fragments at this step." Contradicted by Table 5.1 (both designs
   measured fragments by nrCE-SDS; the invalidated first execution by SEC; all under Version 1.0). Table
   1.1 note b ("The attribute was added at Version 2.0.") repeats it. Say the Version 1.0 plan did not
   call for fragments and the studies measured them anyway.
2. "Fragments and viral clearance have no offset and are judged as predicted." / "...carry no offset..."
   contradict §5.1 ("their offset is unknown, not zero").
3. Viral clearance runs "may run in parallel with the univariate assessment" vs "no two of them overlap"
   vs §6.2 log reduction factors in the design runs; Table 11.1 has no spiking window.
4. "attributes of high or very high criticality are called critical" vs Table 4.1 "CQA" column listing
   VL, L, L-M, M-H attributes (coordinator: the convention is not in PCMP-001 Version 2.0; delete).
5. "The step sets one critical quality attribute, the cumulative clearance of MVM..." vs Table 8.1 (MVM
   ≥ 4.00 of a cumulative 8.60; virus filtration claims the rest; XMuLV shared the same way).
6. Aggregate dropped as a response vs fragments carried "because the pool of this step carries a
   criterion": the same premise; Table 8.1 has no aggregate row.
7. "...keeps the residence time and the impurity mass per unit of ligand equal ... and the binding
   equilibrium depends on these two." (equilibrium binding does not depend on residence time; mass
   transfer does)
8. Cook's 4/n as pass/fail rejects most adequate models (simulation: about 6 runs above 0.14 per data
   set on Table B.1). Coordinator: generic test of every plan; keep; the reports carry the influence
   analysis (PD-008-03).
9. "The proven acceptable range from this analysis is the contiguous range around the set-point over
   which the mean prediction meets the criterion." vs §5.5 and §7 item 4 (coordinator: this is registered
   discrepancy D-001's territory; check brief §5c before changing anything here).
10. Flow rate assigned univariate "because binding ... is fast against the residence time" conflicts with
    the stated assignment rule (low interaction).
11. "Binding of the small, highly charged impurities is fast against the residence time ... so residence
    time is not expected to limit clearance." (virus particles and DNA are large and mass-transfer
    limited; the plan's viral run at high flow concedes it)
12. "That changes the charge distribution of the species this step must bind..." (acidic variants are
    antibody, which the step lets through; more acidic variants risk yield, not impurity clearance)
13. "Confirmation of the ranges at commercial scale belongs to Stage 2 and is made during process
    performance qualification (PPQ)." (PPQ runs within the NOR; §12 says edges are not confirmed)
14. "A change to this plan after approval is made by revising the plan, and the revision is approved by
    the same functions before the affected runs are made." (this revision came after the runs)
15. "Version 2.0 is issued after the studies, under the QA investigation INV-001..." (the revision
    history says INV-001 and INV-002; Table 3.1 omits INV-002, PCP-007, PCP-009, AMD-001)
16. Objective "Establish a proven acceptable range for each parameter and each attribute with a
    criterion..." cannot be delivered for flow rate (§6.4 measures HCP, yield and one viral run, not
    fragments)
17. "Leached Protein A is monitored and not fitted ... so its platform value is not checked on a model
    and stands." (§5.4 measures leached Protein A on every response-surface run; the 10-fold value could
    be checked directly)
18. Load representativeness vs Table 6.1 adjusting load pH and conductivity (check before adjustment)
19. "A criterion that is not met is dispositioned as a deviation and is not revised after the fact." (an
    output failing at the range edge locates the operating region; a result, not a departure)
20. "An effect smaller than the variability of the method that measures it cannot be separated from
    that variability." (resolution depends on the number of runs)
21. "The criteria that apply ... are therefore the intermediate acceptance criteria of Section 8, not the
    drug substance criteria of Table 4.1." (for HCP and fragments the intermediate criterion IS the drug
    substance criterion)
22. "The operating region, the proven acceptable ranges and the verification ... are all derived from it"
    (the flow-rate range comes from the univariate study)
23. Cpk and out-of-specification probability for viral clearance (not a per-batch specification)
24. "...whose attributes are controlled by the preceding step under the cation exchange plan PCP-007."
    (a plan controls nothing; the control strategy does)
25. Residual DNA "≤ 0.001 ng/dose" (low confidence; coordinator: A-Mab's claimed acceptable range, Table
    2.17; keep, with the dose of `meta.dose`)

## Q6 Machine-like (restatements and padding)
Finding 1 stated three times; "Fragments carry a criterion at this step for the first time." (repeat);
"Clearance of MVM is a viral safety attribute of very high criticality." (repeat); the flow-rate reason
three times (§4.1, §4.3, §6.4); "A study confined to the NOR would put the edge of the operating region
outside the data..." (repeat); the load set-point above the centre three times; fragments by nrCE-SDS
four times; the NOR-propagation draw repeated word for word and a third way; the fixed seed twice; the
HCP offset subtraction three times; "decided later, at analysis" five times; the approval date four
times; NOR narrowed, criterion not relaxed (repeat); load qualified (repeat); axial runs on the faces
(repeat). Padding: the objective-to-section map (three sentences); "This section states the rules by
which the study is judged."; "At that level about one term in 20 with no real effect is called
significant by chance."; "The qualification runs come first, because the offsets are estimated before
the first characterization run." (circular); the ALCOA+ spelling and asserted compliance; "The receiving
site reviews the ranges before they are fixed, because a range that the manufacturing equipment cannot
hold is of no use in a control strategy."

## Q7 Codes and stand-ins
Finding 2 cited without its content; "The revision history also names INV-002..." (say what it found);
"the other parameters" (other than which?); "the four conditions of PCMP-001 §7.2" (name them); "The
platform worst cases of this step..." (name 4-fold HCP, 10-fold leached Protein A, and the rule); "the
campaign thresholds of PCMP-001 §7.9" (Cpk 1.33 and 1); the objective-to-section sentences; "The
register" (name it); the offset sentence's abstract subject; "Condition 4" (name it); "the limit on
overfitting" (predicted R² within 0.20 of R²); "qualified under Section 7" (name the load criterion);
"treated as Section 5.5 states" (name the treatment); "the range studied bounds that class" (the class
holds only within the range studied); "As item 4 judges them" (name the rule); "argued by its risk in
PCR-008" (name the check); "with the assumption stated there attached to it" (no interaction of flow
rate); "every claim made from the model is bounded by that qualification"; "rests on the assumptions
stated in Section 5.1" (name them); Table 5.1 note b "Re-executed design (DEV-008-01)." (say it is a
deviation and why).

## Amendment rule: rules or execution details added after the data
- §7 item 2 (non-representative load invalidates a design, rerun in full, data retained for cause, not
  used for ranges): matches what happened (S-AEX-SUP, DEV-008-01). If Version 1.0 contained it, say so;
  the author's status note says Version 1.0 had it (coordinator: mark it as Version 1.0 text).
- "An extended hold of that pool after neutralization raises its acidic charge variants." (reads as the
  deviation's finding written into risks)
- The second-lot comparison (was it in Version 1.0?)
- Table 5.1 and its notes (execution record; belongs in PCR-008)
- EQ-CHR-118 calibration in the future tense (due 2026-05-30, in a document effective 2026-09-30)
- The leached Protein A exemption from verification (not attributed to PCMP-001 §7.5)
- The assay-variability rule for log reduction factors (unquantified; dismisses effects after the data)
- The fixed seed 20240724 (acceptable only if it is the campaign seed)

## Tables
Table 4.1 merged role cells unclear, header split, "CQA" heading; Table 5.1 constant (a sentence would
do; note b code without legend); Table 8.1 long header, constant columns, legend missing "Increase";
Table 1.1 R1 and R3 with no R2, code and value in one cell; Table 3.2 out of numerical order; Table 6.1
unit "pH" for pH; Table 11.1 study type of S-AEX-SUP is a description, note a repeats the text, no viral
clearance row; Tables A.1 and B.1 coded levels only (note that D = 0 is 175 g/L, not the 200 g/L
set-point).
