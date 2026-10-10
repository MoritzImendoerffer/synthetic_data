# Content review of PTP-001 Version 2.0, draft run 2 (2026-10-10)

Judge: Claude Opus 5.5 (abd749d8ac6dfed97), read only the draft text (`PTP-001_transfer.DRAFT.run2.txt`, 1,380
lines). Saved by the coordinator from the agent's hand-back.

**Checked and correct:** 22 documents; 37 parameters (22 multivariate, 15 univariate); 1 CPP, 20 WC-CPP, 10 KPP,
6 GPP (21 for the batch record); 11 attributes, 11 methods, 27 studies; every NOR inside its characterized range;
every step plan approved before its first study; 1 pg/mg is 0.7 ng/dose, 700 times the criterion; viral margins
0.02 log10. The rules the plan says it does not set are handled plainly ("This plan set no step criteria"; the
transfer protocols set the transfer limits; the qualification protocol sets the PPQ criteria; Table 6.1 changed
values with planned values in footnotes).

## Reissue scope: a rule, a result used as a basis, or an execution detail added after the data
- R1. Execution history known only after the studies: "Designs run before the decision measured fragments by SEC
  (Table 6.4)."; "The retained response-surface samples of Protein A and low-pH viral inactivation were re-tested by
  nrCE-SDS, and the cation exchange response-surface design measured fragments by both methods on every run.";
  "From that date, every study that measures fragments, at every step, measures them by nrCE-SDS."; "Table 6.4
  shows which method measured fragments in which designed study."; Table 6.4 footnote d) ("Retained samples of the
  response-surface design, tested 2026-04-06 to 2026-04-17."); footnote g) ("Re-executed design (DEV-008-01). The
  invalidated first execution measured fragments by SEC."). The allowed change is the reference to PCMP-001
  Version 2.0 §7.8 and nrCE-SDS added to the methods to transfer; the history belongs in the step reports.
- R2. "Where the characterization reports base a decision on fragments, they use nrCE-SDS results." A rule written
  after the data about which results serve as a basis; footnote c) ("Reported for information only (AMD-001).")
  likewise.
- R3. A study result as the basis of the method choice: "The decision followed the method comparability study
  S-CEX-FRC, in which SEC and nrCE-SDS were run on the same samples."; "SEC read fragments high wherever the sample
  still carried host cell protein, because part of the host cell protein elutes in the low molecular weight window
  of SEC (INV-001 finding 6)."; "This answers INV-001 finding 6, that size exclusion chromatography (SEC) reads
  fragments high in samples that still carry host cell protein." The plan's change needs only §7.8.
- R4. "The Protein A report PCR-005 records, as discrepancy PD-005-06 from the Protein A plan PCP-005, that the
  loaded antibody mass of the capture runs came from this titre and not from A280." (§1.1 item 5 repeats it.)
  Adding SOP-3016 and AMV-3021 to the method record is allowed; how the capture runs were loaded is an execution
  detail.
- R5 (minor). "Those steps were studied in parallel, which their independent scale-down models allowed."

## Q1: causal clauses without a physical cause or a direction
- "At a set pressure the flux depends on how the feed builds up at the membrane surface, so a feed that differs
  between the scales shows as a difference in flux and capacity." (name protein polarization in UF/DF or pore
  plugging by aggregates in the virus filter)
- "Buffer preparation is the one element in that group that still needs a study, because central preparation adds
  a hold before use that laboratory preparation does not have." (no buffer property named: pH drift from CO2
  uptake, bioburden, leachables)
- minor: "That processing changes with the nutrient supply and with the dissolved gas concentrations in the
  bioreactor." (no direction); "In cell culture, scale acts through mixing and through gas transfer." / "In the
  purification steps, scale acts through column packing and through pressure." ("pressure" is not a mechanism);
  "Inactivation by pH, removal by charge and removal by size act on different properties of the virus particle."
  (name the lipid envelope)

## Q2: terms that are not terms of art
- "AMV-3221 in Table 6.3 is the verification-qualified method for aggregate by SEC-HPLC, whose qualified
  performance the method record holds." ("verification-qualified" coined; "the method record" undefined)
- "Until the receiving site has run the process, these are batches of the development train at the sending site."
  ("development train" undefined)
- minor: "offset rule" (§1.1 item 3, Table 4.1, Table 8.1; defined only in §5); Table 2.2 header "Criticality Tool
  #1".

## Q3: sentences that file a finding or answer an objection nobody raised
- "A narrower distribution does not invalidate a range, because every NOR lies within the characterized range of
  its parameter (Table 6.1)."
- "The division between the sites is one of work, not of accountability."
- "Comparability between the two sites is demonstrated on material, not on documents."
- "It is not assumed from the platform."
- "Each needs laboratory work at a site that has not yet done it, and neither can be closed by a review of
  documents." (second clause)
- minor: "Those edges are established at small scale, and a qualification batch is not a characterization
  experiment."; "Each row therefore states what is compared and how a difference is managed, not a measured
  outcome."

## Q4: criteria without a basis, results not judged
- "The sponsor set their criterion, measured by non-reduced capillary electrophoresis with sodium dodecyl sulfate
  (nrCE-SDS), when fragments joined the register at Version 2.0 (PCMP-001 §3)." (who and when, not why; ≤ 2 % has
  no stated basis)
- "Each claimed step is held to its platform claim (PCMP-001 §7.4)." (claims per step not given, so the sums 16.72
  and 8.62 log10 cannot be checked)
- "The criterion is met through the clearance that the characterization demonstrates and is not tested at
  release." (no clearance demonstrated or log reduction required given)
- "A transfer is successful when the receiving site reproduces the qualified intermediate precision of the method
  and returns accuracy within the qualified range on a common set of samples." (Table 6.3 gives one accuracy value,
  not a range; no criterion for the difference between sites)
- minor: Table 6.3 gives qualified performance without qualification criteria or met/not met.

## Q5: statements that are wrong or contradicted
1. Development train: "Until the receiving site has run the process, the manufacturing scale of that comparison is
   the development train at the sending site (Section 5)." / "...these are batches of the development train at the
   sending site." Conflicts with Table 4.1 (the sending site has only "Scale-down models of the unit operations") and
   "The largest difference between the sites is scale." The offset has no defined reference.
2. Table 8.1 gap 1 action ("Qualify each model against the receiving site equipment train by the offset rule of
   PCMP-001 Version 2.0 §7.1, and record the comparison in the plan and the report of the step.") is impossible by
   Table 10.1 (first receiving-site batches after PCMR-001; every step plan approved before its studies).
3. "The first two gaps set the schedule." vs §10 / Table 10.1: "The characterization work sets the duration of the
   transfer." Method transfer "do[es] not wait on that chain".
4. "The remaining gaps are closed by sequencing, by training or by a bounded qualification study, and none of them
   needs a change to the process itself." vs Table 8.1 (harvest/UF-DF closed by stating a limitation; viral by
   keeping the small-scale claims), and "The gap on harvest and UF/DF will still be open when the characterization
   campaign ends, ..." vs the column "Action that closes it".
5. "Comparability is judged against these criteria and not against the means observed in development." / "A
   development mean is a property of the scale-down model and of the few batches behind it." ICH Q5E: specification
   tests alone are generally not adequate for a manufacturing change (site change included); as written a conformance
   check with no sending-site material compared; under §5 the development-train batches are the manufacturing-scale
   reference, so their mean is not a property of the scale-down model.
6. "Viral safety rests on three independent steps, not on any one of them." For MVM only two steps carry a claim
   (low pH has XMuLV credit only); margins of 0.02 log10 make every claimed step necessary. "The margin is smaller than
   the intermediate precision of the infectivity titre assays (0.3 and 0.32 log10 in Table 6.3), so a step that falls
   short of its claim cannot be made up by the other steps." (rests on an unstated premise: no step credited above its
   claim). "Both requirements are therefore met by the claims alone, with a margin of 0.02 log10 for each virus."
   (below the precision of a single titre)
7. "A model is qualified for each output by its offset from manufacturing scale, not by a test of equivalence, and
   every judgement against a criterion is stated at manufacturing scale." vs §5: fragments and viral clearance are not
   compared ("Their offset is unknown, not zero.").
8. Methods in scope: Table 6.3 / Table 8.1 "Transfer and requalify every method in Table 6.3, ..." brings the XMuLV
   and MVM infectivity assays (AMV-3017, AMV-3018) to the commercial site, while §6.3 says no batch test measures
   viral clearance and §5 leaves it out of comparability; Table 8.1 says the claims cannot be verified at commercial
   scale; nrCE-SDS is in scope but missing from Table 6.3.
9. "The remaining elements in Table 4.1 do not change the process itself, but each differs between the sites." Two
   sentences later the central buffer hold needs a study; raw-material lot variation is a known driver of culture
   performance and glycosylation.
10. (minor) "Buffer preparation is the one element in that group that still needs a study, ..." (method transfer
    also needs laboratory work: Table 8.1 row 2; §8)
11. "The CQA register therefore assigns them to harvest." ("therefore" does not follow from "Fragments form in
    culture and during the harvest hold"; Table 2.1 leaves fragments out of the bioreactor role; Table 6.4 "not in
    scope" for the bioreactor; Table 6.1 has no harvest hold time or temperature and classes every harvest parameter
    KPP or GPP, so no parameter controls the attribute assigned to harvest)
12. (minor) "Table 6.2 lists the procedures and method validations referenced in this plan, which are the documents
    that support the transfer." (AMV-3221 missing)
13. (minor) "In that lifecycle, process characterization is Stage 1 (process design) and process performance
    qualification is Stage 2." / "Process performance qualification is the Stage 2 activity that follows this
    transfer (U.S. Food and Drug Administration 2011)." (Stage 2 also includes equipment and utility qualification,
    §7 condition 3)
14. (minor) "...approves each handover listed in Section 10." (§10 lists deliverables, not handovers)
15. (minor) "Every parameter will be held at its set-point in Table 6.1, and no deliberate excursion will be run."
    (post-clarification turbidity is an outcome and cannot be set)
16. (minor) "Sampling during the campaign will follow the sampling plans of the step plans." (those plans sample
    small-scale runs; FDA 2011 expects a stronger PPQ sampling plan)
17. (minor) Title block "Approved", effective 2026-09-30, Approvals table empty (corpus convention).

## Q6: sentences that read as machine-written
- "ICH Q10 places technology transfer within that quality system (International Council for Harmonisation 2008)."
- "The reverse case matters more."
- "However, the engineering batches will confirm that expectation." (with "It is not assumed from the platform.")
- "Among the methods whose intermediate precision is a relative standard deviation, the residual DNA method by qPCR
  (AMV-3014) is the least precise, at 15 %." (restates Table 6.3, no consequence)
- "Its transfer should therefore be completed and reviewed before the engineering batches are run."
- "PCMP-001 §7.8 keeps SEC for aggregate, where no such interference applies."
- "The master plan PCMP-001 plans the characterization campaign that produces the evidence, and the master report
  PCMR-001 consolidates it."
- "It is accepted for the reason that the risk assessment RA-001 assigned the parameters of both steps to
  univariate study." (circular)
- "An interaction between two of them is therefore not expected to move a result in Table 2.2." (Table 2.2 holds
  criteria)
- minor restatements: "The campaign will not challenge the edges of the characterized ranges."; "Each can start when
  this plan is approved, and Table 10.1 gives this plan as their only dependency."; "The transfer is delivered in
  three parts."; "It states what must be in place before the campaign may start and the strategy the campaign will
  follow."; "The methods are transferred and requalified, the raw material lots come from commercial supply under
  supplier qualification, the buffers are prepared centrally, and the operators are trained on the master batch
  record."

## Q7: sentences a reader cannot follow alone
- "Version 2.0 replaces it under corrective action CA3 of the QA investigation INV-001." (say what CA3 requires)
- "Limits set in that way were the subject of INV-001 findings 1 to 3." (findings 2 and 3 never stated)
- "...when fragments joined the register at Version 2.0 (PCMP-001 §3)." (name the CQA register of PCMP-001
  Version 2.0)
- "The register assigns each viral clearance requirement to one step, and each requirement is met by the claims of
  several steps (Section 2)." / "The register assigns each to one step, but each requirement is met by the sum of the
  claims of several steps." (name the step)
- "Until the receiving site has run the process, these are batches of the development train at the sending site."
  (equipment, scale, which batches)
- "Their representativeness rests on the mechanism of the step for fragments and on the virus spiking studies for
  viral clearance (PCMP-001 §7.1)." (name the mechanism: protease clipping, hold time, temperature, lysis)
- "The reverse case matters more." (name it)
- "Two records cover SEC." (which record is transferred; which SOP AMV-3221 runs under; "the method record")
- Table 6.4 footnote g) "Re-executed design (DEV-008-01)." (code only)
- "At this revision the actions on the scale-down models, the analytical methods and the parameter classification
  were brought into line with the rest of this plan (Section 1.1)." (name the changes)
- "The first two gaps set the schedule." (name them)
- minor: "The viral clearance claims of the three claimed steps now refer to PCMP-001 Version 2.0 §7.4."; "The
  separations of duty in Section 6.2 and Section 11 are the exception and are not waived."; revision history "changes
  listed in the document (see INV-001)" (the list is in §1.1).

## Hard-to-read tables
- Table 6.1: footnote markers run into values and names ("20–39c1)", "3.4c3)", "3.3–3.5c2)", "110c5)", "Dissolved
  oxygena)"); a stray "a)" line belongs to "Number of diavolumes"; two footnote series, the c-notes hide the
  Version 1.0 values; univariate parameters shown only by footnote a) on 15 of 37 rows; "as characterizedb)" in a
  numeric column.
- Table 6.4: single entries ("SEC", "no DoE", "not in scope", "not measured") between the Screening and
  Response-surface columns; markers run into method names ("SECc) , nrCE-SDSd)"); seven footnotes for 16 rows.
- Table 2.2: "Criticality Tool #1" crams two columns into one header; viral rows VH beside a score of 20 below H rows
  at 48–60, explained only by the footnote; "M-H" and "L-M" read as ranges.
- Table 10.2: "Plan" heads both the document column and the approval-date column; rows 8–10 lose alignment.
- Tables 4.1 and 8.1: four columns of full sentences split across pages; Table 8.1 "Action that closes it" wrong for
  the harvest/UF-DF and viral rows.
- Table 6.3: the precision column mixes % RSD and log10 SD; accuracy a single number with no definition; AMV-3221
  out of sequence with a coined qualifier; nrCE-SDS missing.
- Table 6.2 (minor): "Type" labels break mid-list.

## Answers for the document as a whole
1 No; 2 No; 3 Yes; 4 No; 5 Yes; 6 No; 7 No.
