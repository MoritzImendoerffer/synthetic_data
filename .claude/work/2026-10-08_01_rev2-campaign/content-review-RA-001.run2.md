# Content review of RA-001 Version 2.0, draft run 2 (2026-10-10)

Judge: Claude Opus 5.5 (a8941b311f4658f0a), read only the draft text (`RA-001_risk_assessment.DRAFT.run2.txt`).
Saved by the coordinator from the agent's hand-back.

## Reissue check: what the reissue adds after the data were known
1. "It marks each set-point and NOR that the report of its unit operation changed at Version 2.0, and PCMP-001
   Version 2.0 Table 4.2 gives the value in force." With Table 5.2 footnotes b) and c) ("Superseded at Version 2.0 by
   the Protein A report PCR-005" and "... by the low-pH viral inactivation report PCR-006"). A study outcome entering
   the assessment (the Protein A load NOR, the inactivation pH set-point and NOR, the hold time set-point and NOR, the
   inactivation temperature NOR); not among the four changes in §1.1; contradicts "No study result enters this
   assessment, and it gives no final classification of any parameter." The clear breach.
2. "The capture study measures leached Protein A in the pool across the designed experiment, and the pool is judged
   against the criterion that PCMP-001 Version 2.0 §7.3 sets for it." Execution detail plus a judging rule; not
   listed.
3. "Fragments are measured by nrCE-SDS under AMD-001, and PCMP-001 Version 2.0 §7.8 and Table 7.3 give the method
   used in each study." "The method used in each study" is an execution detail decided 2026-03-20.
4. "PCMP-001 Version 2.0 §5 states that the spiking model of each step follows the scaling principles of its
   characterization model." An execution rule for the spiking studies; not listed.
5. "If the anion exchange study finds that residence time acts together with the load chemistry, the univariate
   result for flow rate would not bound the step, and the design would have to be augmented." A decision rule naming
   the remedy used after the data; not listed; also illogical (Q5.6). Confirm Version 1.0 had it or remove it.
6. "No data are planned beyond those ends of the NOR, and a proven acceptable range (PAR) is never claimed beyond the
   range studied (PCMP-001 §7.6)." A PAR-claiming rule (the subject of INV-001), PCMP-001 cited without a version, not
   listed. Confirm Version 1.0 had it or remove it.
7. "A hold longer than its range raises aggregate at any pH in the range." Stated as fact, reads as a result.
8. "The step plans were amended under INV-001 corrective action CA2 with the criteria and the fragment method of
   PCMP-001 Version 2.0." Records later events; harmless; not listed.
Permitted changes in order: the §1.1 dates; fragments added to the register with nothing set for them; references
to PCMP-001 Version 2.0 §7.1 and §7.3; Table 1.3 corrections (agree with Tables 4.1 and 5.2; the reversed
acidic-variant direction rests on base-catalysed deamidation and moves no score), except the section label "4.2 to
4.9" (Q5.1).

## Q1: causal clauses without a physical cause
- "Because most attributes are formed there, the bioreactor carries more parameters into multivariate study than any
  other unit operation (Table 5.1)." (the cause is a count, not the interaction judgement of §5; Protein A carries 4
  parameters with 1 attribute at risk)
- "Temperature is expected to act together with pH on the glycan attributes, because both act on the activity of the
  same glycosyltransferases." (no direction; acting on the same enzyme does not make effects interact)
- "A protein load above its range is expected to raise host cell protein per milligram of antibody in the pool,
  because the wash removes a smaller share of the host cell protein retained on a more heavily loaded column." (nearly
  circular; host cell protein bound to the captured antibody)
- "Load and elution pH are expected to act together, since the resolution between monomer and aggregate depends on
  both." (an outcome, no mechanism or direction)
- "A higher elution flow rate broadens the elution peak, because the antibody has less time to diffuse out of the
  resin pores, and a broader peak dilutes the pool." (scored against yield: product lost in the tail after the OD280
  stop)
- "The log reduction is expected to fall as the volume filtered per unit area rises, because the retentive layer
  accumulates material and the chance of a parvovirus passing rises with it." (name the species and the mechanism:
  the smallest pores plug and flow moves to larger ones)
- "Filtration pressure is scored against both model viruses, because it sets the driving force across that layer."
  (no direction; none for XMuLV)
- minor: "Inactivation pH and temperature set the rate constant, and the hold time sets how long that rate acts."

## Q2: terms that are not terms of art
- "The consumers of the assessment are the characterization plans PCP-003 to PCP-010, one for each unit operation.";
  "Per unit operation, the consumer is the characterization plan named in Table 5.1."; "PCMP-001 consumes the
  assessment at campaign level." (software vocabulary: "applies", "uses as its risk basis")
- "It judges each step output on which a drug substance criterion depends against an intermediate acceptance
  criterion (PCMP-001 §7.3)." (again in §7; "step output")
- "The parameter acts on the step through residence time alone, and prior knowledge places no interaction between
  residence time and the load chemistry." ("load pH and conductivity")
- "Beyond that point the polarized layer at the membrane surface thickens and flux stops rising, so a transmembrane
  pressure outside its range is expected to change the processing time." ("concentration polarization layer")
- "under the analytical method decision AMD-001 of 2026-03-20"
- Table 4.2 cell "Slight effect on galactosylation; critical for titre" ("critical" for process performance)
- Table 1.1 cell "Formulation / mass balance"

## Q3: sentences that file a finding
- "The risk that remains once the studies have reported is a separate assessment, and nothing in this document
  anticipates it."
- "It does not divide them into a critical and a non-critical group, and it is not a control strategy."
- "Severity for these two attributes is therefore assigned on the consequence of a shortfall and not on the
  probability of detecting one."
- "A low severity lowers the priority of a parameter and does not remove it from study."
- "The polishing steps clear what reaches them."
- "The assessment marks 1 parameter “univariate (justified)”, the substitution that the A-Mab risk ranking and
  filtering approach permits where the study can be justified (CMC Biotech Working Group 2009)."

## Q4: criteria with their basis
- "The sponsor set their criterion, ≤ 2 % (nrCE-SDS), when fragments joined the register." and "The A-Mab case
  study lists fragmentation among the typical quality attributes of an antibody but gives it no limit, and the
  sponsor set the criterion for fragments, ≤ 2 % (nrCE-SDS), when they joined the register (PCMP-001 §3)." (no basis
  for 2 %; whether fragment data existed when it was set)
- "The capture study measures leached Protein A in the pool ... against the criterion that PCMP-001 Version 2.0 §7.3
  sets for it." (value and basis not given)
- Table 3.1 "≤ 0.001 ng/dose" (no dose given)

## Q5: wrong or contradicted
1. Table 1.3 Section cell "4.2 to 4.9": there is no §4.9 (4.1 to 4.8); the relabelled bioreactor failure modes are in
   §4.1 and Table 4.2.
2. The viral clearance paragraph in §3 ("Both viral clearance attributes carry the highest severity for a different
   reason." ... "A shortfall at one of these steps changes no property of the drug substance that a release test
   measures" ... "Severity for these two attributes is therefore assigned on the consequence of a shortfall and not on
   the probability of detecting one.") gives undetectability as the reason for severity 10; Table 2.1 uses it for
   detection 10 and §6 says severity excludes detectability; the real basis is the very-high-criticality rule of §3.
3. "A severity in Table 3.1 therefore combines the impact of a failure on the patient with the uncertainty of that
   impact." Residual DNA (VL, Tool #1 score 6) has severity 2 and acidic variants (VL, score 4) severity 4: the mapping
   is not monotonic and never stated.
4. "The lowest ranked parameters change step yield and process consistency, not a quality attribute." / "They are
   studied one factor at a time, so that the ranges entered in the batch record rest on data and not on platform
   precedent alone." Protein A load flow rate and end of pool collect are RPN 96 and Low, yet in the multivariate DoE.
5. "The judgement was made from platform and prior product experience and is recorded per parameter in Section 4."
   and "Each gives the potential failure mode and effect behind each score, together with the judgement on
   interactions that decides the study type." §4 records no interaction judgement for pCO2, osmolality, culture
   duration (Table 4.2), CEX elution stop collect (Table 4.6), AEX equilibration/wash-1 conductivity and AEX protein
   load (Table 4.7); "The 5 parameters scored against a glycan, charge variant or aggregate attribute are therefore
   carried into one designed experiment." rests on temperature × pH alone.
6. The AEX augmentation sentence (reissue item 5) contradicts the sentence before it and §2; flow rate is univariate.
7. Table 4.8 "Filtration volume (load) above 105 L/m2": 105 is the NOR limit; the range studied is 50–140.
8. "It forms and clears no quality attribute." (UF/DF) vs "The final concentration is the drug substance
   concentration itself, which is measured and released against a specification."; diavolumes set excipient
   composition and pH, yet Table 4.9 scores both on process performance.
9. "CQA(s) at risk" in Tables 4.2, 4.4, 4.6, 4.7 lists host cell protein, acidic variants and DNA, which §3's
   definition does not call critical ("Attributes of high and very high criticality are called critical, and 6 of the
   11 attributes are critical on that definition.").
10. "Prior knowledge gives neither the size nor the direction of a pressure effect on the log reduction." (parvovirus
    filters show lower retention at low pressure or flux and after pressure interruptions)
11. "This assessment attributed the amount released to the resin and its history of use, which are controlled under
    the resin life cycle procedure SOP-2008, and not to a parameter in Table 5.2." (ligand leaching is driven by host
    cell proteases in the load, contact time, temperature and elution pH)
12. "Dissolved oxygen raises titre through the productivity of each cell." vs Table 4.2 "Impacts peak VCD, titre and
    process consistency".
13. "...because both act on the activity of the same glycosyltransferases." (the pH mechanism named earlier includes
    mannosidases, which are glycosidases)
14. "The parameter list is assumed complete." (§3 and Table 1.1 name the harvest hold, not assessed)
15. Table 4.7 "Reduced HCP removal capacity (viral clearance robust)" vs §4.6 on exceeding binding capacity.
16. minor: "The study assignment is the output of this assessment." vs §7 "This assessment produces three outputs."
17. Version 1.0 method, not a reissue defect: uncertainty counted twice (severity includes Tool #1 uncertainty;
    occurrence 7 because the effect size is unknown).

## Q6: machine-written sentences
"The scores in this document are initial scores in the same sense."; "Basal medium concentration needed an
argument."; "Culture duration reaches as many attributes by a different route."; "Volumetric load is the parameter
on which the step turns."; "Material does carry properties from one step to the next."; "The polishing steps clear
what reaches them."; "Both viral clearance attributes carry the highest severity for a different reason."; "The
range of each parameter over which acidic variants stay within their criterion is one of the things the bioreactor
study must establish." Restatements: "An effect of that kind is estimated only by moving the two parameters
together."; "Detection scores 10 for each of these parameters." with "Neither an in-process control nor a release
test of the drug substance measures the log reduction that the hold achieves."; "The capture step carries 2
parameters into its design although they are scored against process performance alone, so that the same design
bounds step yield." (third time); "A parameter that does not act together with the load chemistry can be bounded by
moving it one factor at a time, and the anion exchange plan PCP-008 carries that justification with its design.";
"Within a class the RPN differs only through severity." (third time); "An interaction between a parameter in the
design and one left out of it cannot be found by that design."; "Under those rules a scale-down model is qualified by
its offset from manufacturing scale (PCMP-001 §7.1)." and "Each step output on which a drug substance criterion
depends is judged against an intermediate acceptance criterion (PCMP-001 §7.3)." (repeat §1.1 item 3); "It states
once what the plans would otherwise each restate, including the number of parameters assigned to multivariate and to
univariate study across the train (PCMP-001 Table 4.1)."

## Q7: sentences that cannot stand alone
Revision history ("Reissued under INV-001: approval and execution dates recorded; changes listed in the document
(see INV-001)"); "The scores in this document are initial scores in the same sense."; "In this framework risk
assessment is a lifecycle activity, not a single exercise" (name ICH Q9(R1)); "Both viral clearance attributes carry
the highest severity for a different reason."; "Culture duration reaches as many attributes by a different route.";
"An effect of that kind is estimated only by moving the two parameters together."; "Basal medium concentration
needed an argument."; "Fragments are measured by nrCE-SDS under AMD-001, ..."; "...the pool is judged against the
criterion that PCMP-001 Version 2.0 §7.3 sets for it."; "The exposure is largest at high volumetric load, where the
layer is thickest."; "The clearest exposure is the operating flow rate of the anion exchange step, ..."; "Material
does carry properties from one step to the next."; "The step plans were amended under INV-001 corrective action CA2
with the criteria and the fragment method of PCMP-001 Version 2.0."; Table 8.1 "Approval, and closure of INV-001
corrective action CA3 for this document".

## Hard-to-read tables
- Revision history: the Version 2.0 entry names only the dates.
- Table 1.3: "4.2 to 4.9" wrong; section numbers in the 4.1 and 6 rows sit between two corrections; some Version 2.0
  cells need the Version 1.0 cell ("DNA, virus and most host cell proteins do.", "Withdrawn."); no column says why each
  Version 1.0 text was wrong.
- Table 3.1: category labels float; header cut off ("Acceptance"); the score-to-severity mapping not stated; criteria
  formatted inconsistently ("≤2%"); footnote letters glued to values; "Formed or set at" assigns MVM to anion exchange
  though §4.7 calls virus filtration the principal MVM step.
- Table 4.1: no columns for the attribute at risk, occurrence or detection, so an RPN cannot be checked from its row;
  "multivariate DoE" vs Table 5.2 "multivariate"; step names split across rows.
- Tables 4.2–4.9: "CQA(s) at risk" holds non-critical attributes and lower-case "process performance"; telegraphic
  cells; Table 4.8 gives no pressure limit and uses the NOR limit for volume; the failure-mode column repeats the
  parameter name.
- Table 5.2: footnote letters read as values ("20–40b)", "3.5c)", "90c)", "univariated)"); step labels split;
  superseded values printed without the values in force.

## Answers for the document as a whole
1 No; 2 No; 3 Yes; 4 No; 5 Yes; 6 No; 7 No.
