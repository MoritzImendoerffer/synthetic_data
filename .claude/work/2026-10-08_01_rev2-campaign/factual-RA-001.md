# Factual check of RA-001 Version 2.0 (draft PDF text, 2026-10-10)

Checker: Claude Opus 5.5 (claude-opus-5-5). Returned as text; saved by the coordinator (condensed, every
error kept). Scratch: `scratchpad/ra001check/`. Every number is correct; §4 and §5 are numerically
identical to Version 1.0 (all 37 severities, RPNs, study types, priorities). The errors are in what
Version 2.0 added.

## Errors, most consequential first
1. **Execution details and a result enter a document that says it reports none** (§1 "reports no study
   result"; §1.1 "No study result enters this assessment"): Table 3.2 reproduces PCMP-001 Table 7.3 (the
   method each executed design used); note c (the SEC/host cell protein interference, the S-CEX-FRC
   result); note d ("tested 2026-04-06 to 2026-04-17"); note f ("Aggregate was not measured in the designs
   at this step"); note g ("Re-executed design (DEV-008-01) ..."); §1.1 item 2 (the S-CEX-FRC reason, INV-001
   finding 6); §3 ("From the date of AMD-001, fragments are measured ... in every study at every step").
   Fix: drop Table 3.2 and the S-CEX-FRC reason; keep the register change (fragments, ≤ 2 % by nrCE-SDS
   under AMD-001 of 2026-03-20); one pointer: "PCMP-001 Version 2.0 §7.8 and Table 7.3 give the method used
   in each study." The brief lists `T.methods_by_study()` for RA-001: change the brief too.
2. **§2, certified unchanged, changed the basis of detection 6** ("since it shows in the performance of
   the next unit operation before the batch is released"; Table 2.1 "Seen in the performance of the next
   step"). Version 1.0: "shows up in the performance of a downstream unit operation before the batch is
   released". A-Mab Table 5.24 (p.214): rank 6 "detection is delayed several downstream unit operations,
   but prior to CofA testing"; rank 4 "would definitely be detected in the next downstream operation".
   Fix: restore the Version 1.0 wording in the prose and in Table 2.1.
3. **Fragments carry a severity no assessment gave** (Table 3.1 shows 4: the code fallback of
   `ra_content.cqa_table()`; config `tool2_severity: 3` is another scale). Fix: print "—" (not scored);
   "No severity is assigned to fragments."; annex to match. (Coordinator: the helper now returns no
   severity for an attribute the assessment never scored.)
4. **§1.1 item 1 claims a record the document does not carry** ("records beside it the date on which the
   first characterization study started": neither the title block nor the revision history carries it;
   2025-08-11 appears only in §1.1). Fix: "and this section records the date on which the first
   characterization study started."
5. **§6 hands the capture-to-hold pH link to the intermediate acceptance criteria**, which cover no pH
   (PCMP-001 Table 7.1, 22 criteria). The link is handled by titration to the hold set-point
   (inactivation pH, a Step 6 parameter); Version 1.0 said "handled by the in-process limits of the
   receiving step". Fix: say so; keep the criteria sentence for attributes only.
6. **"In every study at every step"** (§3) is contradicted by the data: seven studies that started after
   2026-03-20 have no fragment result (S-AEX-UNI, S-VF-SDM, S-PA-SDM2, S-BRX-OSM, S-BRX-AUG, S-UFDF-UNI2,
   S-VI-UNI2), and by Table 3.2's own bioreactor row. PCMP-001 §7.8 carries the same sentence verbatim
   (coordinator: corrected in PCMP-001). Fix: "From the date of AMD-001, every fragment result is by
   nrCE-SDS", or delete under item 1.
7. **The basal-medium rationale moved onto an A-Mab DoE result** (§4.1 "The A-Mab case study reports a
   statistically significant but shallow effect of medium concentration on afucosylation"; Version 1.0
   "Platform experience shows"). A-Mab p.77–78 (Table 3.15) does report it, but from A-Mab's own
   production-bioreactor experiment, which conflicts with §1 ("prior knowledge alone, because no A-Mab
   characterization data existed"). Fix: restore the Version 1.0 attribution.
8. **"judges each step output against an intermediate acceptance criterion"** (§1.1 item 3, §7): PCMP-001
   sets criteria only for outputs on which a drug substance criterion depends (22 at 6 steps; none at
   harvest or UF/DF; none for residual DNA). Fix: "each step output on which a drug substance criterion
   depends".
9. **The harvest citation drops the source's caveat** (§4.2 "also treats harvest as a step with no impact
   on product quality"; A-Mab p.85 "for simplicity, it has been assumed ... This might not be true in a
   real life scenario"). Fix: "assumes, for simplicity, that harvest has no impact on product quality".
10. **Table 1.2 calls PCMP-001 "Parent — master plan"** although RA-001 precedes it and PCMP-001 consumes
    it (Version 1.0 too; from `related_docs_md`). Fix in the registry.
11. Minor: "≤2% (nrCE-SDS)" in Table 3.1 vs "≤ 2 % (nrCE-SDS)"; build_fmea labels in Table 4.2 ("360-440
    mOsm" vs "mOsm/kg", "Dissolved CO2" vs "CO2 partial pressure (pCO2)", "34-36 C" without a degree
    sign); "AEX" defined but never used; §4.4 "PCMP-001 Version 2.0 §5 sets out the spiking models" (§5
    states only the scaling principle); §4.1 "highest severities of the train" (shared with the viral
    steps; Version 1.0 too); §2 "A parameter that affects process performance alone is studied one factor
    at a time" (two Protein A ones are in the design; Version 1.0 too); the continuum citation now ICH Q8(R2)
    where Version 1.0 cited Q9(R1), not listed.

## Checked and correct
All counts (8 unit operations, 37 parameters, 21/16, priorities 16/5/16, 22/15, DoE at 6 of 8, one
"univariate (justified)", 8 parameters at RPN 700, 5 distinct RPNs 96–700, per-step numbers, Table 5.1);
all severities and RPNs (identical to Version 1.0); Tables 4.2–4.9 identical to Version 1.0 and build_fmea;
Table 5.2 (values, overlap counts 31/5/1, the values changed later match PCMP-001 Table 4.2 footnotes); the
register against PCMP-001 Table 3.1 (11 criteria, criticality, Tool #1, formed-at steps); chronology
(PTP-001 2025-06-16, RA-001 2025-07-14, PCMP-001 2025-08-04, S-BRX-SDM 2025-08-11; 2026-07-24 the
compilation date and the approval date of the Version 1.0 reports; INV-001 2026-08-03 to 2026-09-18; CA3
covers RA-001; AMD-001 2026-03-20); A-Mab outcomes cited in §2 (p.119–120, Table 4.6); UF/DF outside the case
study; references.

## Could not be checked
ICH Q8(R2) as the source of "criticality as a continuum"; the origin of the 2–10 severities (build_fmea's
`CQA_SEVERITY`, A-Mab Table 5.22 scale; Version 1.0 wording); occurrence 7 is not an A-Mab rank (unchanged
from Version 1.0, do not change).
