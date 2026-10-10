# Content review run 2: PCP-010 Version 2.0 (UF/DF plan)

Judge: Claude Opus 5.5 (claude-opus-5-5), fresh context, read only `PCP-010_ufdf.DRAFT.run2.txt`.
Returned as text; saved by the coordinator (condensed; quotes kept where a fix depends on them).
Answers: 1 No, 2 No, 3 Yes (glosses present), 4 No, 5 Yes (errors present), 6 No, 7 No.

## Most serious (judge's ranking)
1. "Quality Assurance approves this plan before any run is executed." (§10) is false for Version 2.0
   (effective 2026-09-30, runs ended 2026-03-27). Coordinator: Version 1.0 text (V1.0 §10).
2. "PCMP-001 requires the qualification runs, and the estimate of each offset, before the first
   characterization run" (three times, and step 1 of §11) is never reported as met or not met, and the
   reference batches are chosen only in PCR-010.
3. §1.1 item 6 ("A parameter with a significant but small effect can therefore be classified as a key
   process parameter under Version 2.0") contradicts §7.4 (a KPP "affects no quality attribute", and
   "affects" means a significant slope).
4. Buffer exchange: the criterion needs conductivity and pH "by the analysis of Section 5.5", which
   analyses conductivity only; §5.4 and §6.2 contradict Tables 5.1 and 5.2 on where the criterion and
   the sampling apply.
5. Mechanism: TMP raises the wall concentration "without raising throughput" and, two sentences later,
   "by driving more permeate" (film theory: the wall concentration cannot rise while the flux stays
   flat; beyond the limit extra pressure compacts the layer). The bench model gives "more pump passes"
   although crossflow and loading are matched per unit area (then the passes are equal).
6. §1.1 says Version 1.0 descriptions in §4.1, §5.1 and §5.5 were corrected but not which; some
   expectations read as written with the results known ("The effect on aggregate is therefore expected
   to be small."; "The bench model is therefore expected to be conservative for aggregate formation by
   shear."; the §5.5 curvature sentence).

## Amendment scope
Mostly compliant (each open point left to PCR-010; "If one pool is not sufficient" kept; no step-specific
decision rule). Flags: the unnamed corrections (item 6); the offset argument for acidic variants and the
buffer exchange (admissible as argument; it assumes equal duration and temperature at both scales); no
rule and no statement that none is set for the pH half of the buffer-exchange criterion and for what
follows if this step adds aggregate or acidic variants.

## Q1 Causes
"The three parameters act on the product by different routes." (V1.0; two routes are shared); "All three
are studied one at a time, because RA-001 ranked none of them high" (administrative cause; TMP and
concentration both raise the wall concentration); "The TMP drives the permeate flux." (no direction);
"The shear at the wall is set by the crossflow and by the geometry of the feed channel." (no direction);
"The final concentration sets the viscosity ... and the concentration in the polarization layer." (no
direction; under the gel model the wall concentration is capped and the bulk concentration sets the
flux); "The crossflow per unit membrane area sets the shear ... so it also sets the antibody
concentration in the polarization layer." (higher crossflow, higher shear, lower wall concentration);
"The membrane loading ... sets the volume that each square metre of membrane processes." (arithmetic);
"The number of diavolumes and the TMP set how long the operation lasts" (no direction for TMP); "How
readily an antibody aggregates does depend on the antibody" (name colloidal stability or
self-association). Borderline: two "For this reason" sentences whose cause is in the previous sentence.

## Q2 Terms
"a test of equivalence in three parts" (§7.1 describes a test for a difference at α = 0.05);
"NOR-propagated analysis" (PCMP-001 term; define); "Three bounds apply to a PAR" (limitations; "bound" is
also a confidence bound); "pump displacement to system hold-up volume" (passes are set by pump flow over
retentate volume); "design space" applied to a univariate step (V1.0 text) and "well controlled
critical" spelled two ways; minor coined labels ("analytical method decision", "execution window",
"platform worst case", "Tool #1 score", "which is a single batch" for a bench run).

## Q3 Glosses
"(INV-001 finding 4, a two-sided range assessed against its upper end)"; "which is a single batch" (twice);
"so the two studies did not run in parallel"; "and the skid was in calibration at execution"; "and not to
release a run"; "Their offsets are therefore unknown, not zero" (the next sentence judges as measured);
"PCMP-001 §5 lists the same outputs for this step."

## Q4 Criteria
The pH half of the buffer-exchange criterion has no analysis and the plan does not leave it to PCR-010;
the offset-timing requirement is never reported as met or not met; the QA approval sentence is "reported
as met"; "This step can add to both, and the studies of this plan measure what it adds." (no consequence
and no owner if it does); "An excursion below the target leaves the drug substance below the
concentration that the drug product program expects." (a requirement with no criterion); minor: the
range-studied pass rule vs the §8 PAR definition; the pilot-scale repeat (before or after the offset;
relation to decision rule 3).

## Q5 Wrong or contradicted
1. QA approval (revision history, Table 11.1).
2. "The acceptance criteria of Section 7.2 apply to the final retentate." vs Tables 5.1 and 5.2 (the
   buffer-exchange criterion is read on the diafiltration series; Table 5.2's purpose cell repeats it).
3. "The diavolume series carries the additional in-process sampling" vs Table 5.2 titled "Sampling plan
   for each characterization run".
4. §1.1 item 6 vs §7.4 (above).
5. "a test of equivalence in three parts" vs §7.1.
6. The qualification runs "together with the estimate of each offset" before the first characterization
   run vs the revision history and Table 11.1.
7. "The three parameters act on the product by different routes." vs §4.3 and §4.1 (shared routes).
8. TMP "without raising throughput" (§4.1 twice) vs §4.3 "by driving more permeate".
9. Pump passes (also §12) vs matched crossflow and loading per unit area (§5.1).
10. "They arise in the production bioreactor, and aggregate is reduced at the cation exchange step." vs
    §4.1 (deamidation continues in solution) and §7.2 (low-pH inactivation may change acidic variants);
    aggregate also forms at the low-pH elution and hold.
11. Objective (iv) PAR "against the criteria of Section 7.2" vs §8 and Table 4.1 (no buffer exchange).
12. "The scale-down model is qualified by its offset from manufacturing scale, as PCMP-001 §7.1 requires"
    vs §7.1 ("cannot be made as PCMP-001 states it").
13. In-process readings "not validated assays ... not to release a run" vs Table 5.1 and §7.2 (the sole
    basis of a criterion and of the lower diavolume edge).
14. The load pool assayed once for the whole study vs a 19-day window and continuing deamidation (no
    hold condition stated).
15. "The revision history now gives the approval date." vs its "Effective date" header.
16. LIMS "sample identifiers of Table 5.2" vs sample types.
17. The receiving site reviews the plan, with no row in the Approvals table.
18. "with the other parameters at the values the commercial step will hold" vs Table A.1 (set-points).
19. The lower-TMP side named as a worst case and left unstudied without a reason.
20. "passes through the pump a limited number of times" vs §4.1 "many times".
Science: 21 shear treated as an established cause of aggregation (shear alone causes little; interfaces,
cavitation and shed particles dominate), and the pump is not where the antibody is most concentrated;
22 "Where and why aggregate forms in the step does not depend on the antibody" (overstated); 23 viscosity
"rises steeply as the concentration approaches the DS target" (the steep rise is usually above about
100 g/L); 24 Donnan and volume exclusion leave the retentate pH and excipients off the buffer values;
25 conductivity approaches the buffer value from above or below; 26 the duration also depends on the final
concentration; 27 a common pool does not constrain the run order; 28 a formulation change affects all
three series; 29 minor (one lack-of-fit degree of freedom; residual protease concentrated with the
antibody).

## Q6 Machine-like
Restatements: the UF/DF role (§1); TMP raising flux (§4.1); the offset-timing sentence (three times); no
IAC at this step (three times); the qualification decision, model adequacy and verification not applying
(each repeats §1.1); "Each run is judged on its own measured result"; yield, flux and concentration
offsets recorded (restates Table 5.1); the aggregate offset subtraction (three times); the acidic-variant
offset (repeats §5.1); "a run lasts as long as the commercial step" (repeats §5.1); "This step has no
designed experiment." (out of place); the fragments scope (three times); SEC noise (twice); the pump passes
(repeats §5.1); "expected to be conservative" (repeats, "expected" twice); the single load pool (repeats
§5.2); INV-001 as the reason (repeats); unforeseen work recorded as a discrepancy (repeats); PA3 (repeats
the previous sentence). Padding: two signposting sentences on PCMP-001 §7; the NOR-propagated detail for
an analysis not performed; "and it does not challenge the step with material that is already outside
those criteria". Hedged: "spends little time at the highest wall concentration" (no numbers); "The effect
on aggregate is therefore expected to be small."; "will be described in those terms". Template: "Version
1.0 set the following rule for this case, and it is unchanged." (seven variants) and "Version 1.0 set no
..., and PCR-010 states ..." (four).

## Q7 Codes and stand-ins
"Descriptions of the process that Version 1.0 stated wrongly are corrected" (name each); "The statistics
on which each output is judged are stated." (name them); "The acceptance criteria are stated on the basis
of PCMP-001 Version 2.0." (name the drug substance limits); "At analysis, however, Version 1.0 read ..."
(the Version 1.0 report); "One quantity cannot be matched." (name it); "Version 1.0 set a rule for this
case, and this plan keeps it." (name the case); "Each is judged as the scale-down model measures it."
(name them); "This step has none, so this plan sets no rule for that decision." (name both); "The other
attributes of the register" (the drug substance CQA register); "which batches of that record" (the pilot
and commercial batch record); "Three bounds apply"; "the amendment of PCP-010 under action CA2" (name the
corrective action); "INV-001, which QA opened ... after its review of PCMR-001" (name the master report
and what the investigation concerned); "The classification follows PCMP-001 §6.2 and §7.7" (name the
rules); "Section 4.2 gives the reason" (give it); "RA-001 ranked" (the pre-characterization risk
assessment); "PCR-010" alone 27 times and "PCMP-001" 61 times (name each at first use in a passage).

## Tables
Approvals all "—"; revision history (INV-001 twice; "Effective date" vs "approval date" in §1.1); Table
3.1 "Rolls up into" without object, nested parentheses; Table 3.2 AMV rows out of order; Table 4.1 "Tool #1
score", "(deamidation)"; Table 5.1 the change-in-aggregate row carries a criterion on the level, "Plateau
of the formulation buffer"; Table 5.2 title vs §6.2, "Fixes the input", footnote marker fused ("pHa)");
Table A.1 header split, set-point row repeated without saying it is the three shared replicates, no run
number or order; abbreviations CE-SDS, HPLC, UV missing.
