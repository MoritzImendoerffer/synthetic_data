# Factual check of PCP-010 Version 2.0 (UF/DF, Step 10)

Checker: Claude Opus 5.5 (claude-opus-5-5), 2026-10-10. Returned as text (the harness blocks subagent
report files); saved by the coordinator. No wrong number found. Errors are claims about Version 1.0,
one citation, changes made but not listed, and one data gap.

## Errors, most consequential first

1. **Aggregate scale-down offset planned and needed, but not in the record and not in PCMP-001 §5.**
   Table 5.1 marks step yield, permeate flux, final concentration and change in aggregate as compared at
   both scales, and the aggregate offset "Subtracted before every judgement" (§5.1, §5.5, §7.2, §8).
   §1.1 item 2, §5.1 and §11 step 1 read as a record of what was done ("the qualification runs are made
   and the offsets estimated before the first characterization run"). `sdm_qualification.csv` has no
   S-UFDF-SDM rows; `analytics.SDM_RESPONSES` has no `ufdf` key; `D.sdm_offset("ufdf",
   "aggregate_out_pct")` is None, so `D.to_mfg` subtracts 0. PCMP-001 §5 lists compared outputs for six
   steps only, yet its Tables 5.1 and 9.1 list S-UFDF-SDM. Version 1.0 PCR-010 §3.1 says the comparison
   covers the attributes of its Table 2.1 (acidic variants included); this plan says acidic variants are
   not compared (as Version 1.0 PCP-010). Fix: keep the Version 1.0 design; fix the record (owner
   decision Q8 2026-10-10: seed S-UFDF-SDM results, add UF/DF outputs to PCMP-001 §5); word the three
   "offsets estimated" sentences as PCMP-001's requirement. Note: the plan subtracts the offset of the
   change across the step from aggregate in the final retentate; sound only with a common load at both
   scales, which PCR-010 should state.
2. **Classification rules from PCMP-001 Version 2.0 added but not listed as changes.** §5.5 "affected
   ... when that slope is significant", §7.4 "A significant effect that is too small to move an attribute
   appreciably within its PAR does not by itself make a parameter critical (PCMP-001 §7.7)", and WC-CPP
   judged on "its acceptable range" (Version 1.0: "outside the design space"). §1.1 item 3 says "Neither
   rule changes what this plan decides". Version 1.0 §7.4: "A parameter whose variation affects a quality
   attribute is classified as critical." S-UFDF-UNI2 gives significant aggregate slopes for TMP (0.0110 %
   HMW/psi, p = 0.0146) and final concentration (0.00677 % HMW per g/L, p = 9.0e-05); under Version 1.0
   §7.4 alone both would be CPP or WC-CPP; the added clause allows KPP (`parameter_classification.csv`).
   Fix: add a sixth change for classification under PCMP-001 §6.2 and §7.7; qualify item 3.
3. **§1.1 item 1 misstates how Version 1.0 judged acidic variants.** "Version 1.0 judged it against the
   same criteria, and no other criterion was applied to this step at analysis." Version 1.0 PCR-010 §5.3
   judged against an upper criterion of 40 % only (Table 8.1 spec "upper"; INV-001 finding 4;
   `doe_report.effective_acceptance`). Fix: Version 1.0 of the plan stated the same criteria, but at
   analysis Version 1.0 read acidic variants against 40 % only; this plan keeps the two-sided criterion;
   PCR-010 records the departure.
4. **Wrong table cited in §1.1 item 4** ("do not measure fragments (Table 5.2)"). Table 5.2 shows the same
   entry for aggregates, which are measured. Cite Table 5.3 and Section 4.2.
5. **§1.1 item 2 and §7.1 misdescribe the Version 1.0 qualification rule.** Version 1.0 §7.1: α = 0.05
   for step yield, flux and change in aggregate only; final concentration "within the reported
   variability of the A280 method"; a significant difference "assessed for its size against the
   acceptance criteria of §7.2 before the model is rejected", with Statistics and QA approval. State all
   three parts.
6. **§5.1 chooses the comparator data set after the runs** ("so the commercial batches of that record are
   the reference"). Version 1.0 named "the pilot and commercial record" without the batches; PCMP-001
   §7.1 leaves the manufacturing-scale data set to each plan. Say Version 1.0 did not state the batches
   and PCR-010 states which form the reference.
7. **§6.2 rewords a Version 1.0 sampling sentence while §1.1 says sampling is unchanged.** Version 1.0:
   "The diavolume series carries the additional in-process sampling that builds the buffer exchange
   curve." Restore it word for word.
8. **Revision history and Table 3.1 do not fit this plan.** The revision row says "a priori intermediate
   acceptance criteria", but no IAC exists for this step (generic `reason_plan`). Table 3.1 omits INV-002
   though the plan says it is reissued under it.
9. **Minor wording.** §5.1 "The model is qualified under SOP-1001" vs §7.1 "no rule for the
   qualification decision" (use "The qualification runs are made under..."); §5.3 says PCMP-001 §7.8
   covers "the designed studies" (it says "every study at every step"); §1.1 item 3 puts the slope test in
   Version 1.0 §7.3 (it is in §5.5); §1.1 item 1 "an IAC for each step output" (PCMP-001 gives 22 criteria
   at 6 steps).

## Checked and correct

Identity, scale and target (15,000 L, 75 g/L); every set-point, range, NOR and study type (Tables 6.1,
A.1, §5.2, §6.1); 9 runs = 6 edge + 3 set-point; Table 4.1 criteria, criticality and Tool #1 scores;
criteria framework (no IAC for UF/DF; no change credited downstream as stated; viral clearance credits);
chronology (approved 2026-02-23 before 2026-02-25; windows; EQ-TFF-142 calibration due 2026-04-22);
INV-001 dates, findings 1 and 5, CA1, CA2, PA3; INV-002 changes nothing here; AMD-001; SOP/AMV table,
related documents, Table 5.2; offset definition, 90 % interval, α = 0.05; adequacy and verification do
not apply; every PCMP-001 section reference; §9b otherwise compliant (design, levels, randomization,
single load pool, bridging rule, Table 5.3 sampling, the five §7.3 decision rules word for word, buffer
exchange acceptance, PAR definition and bounds, combination-of-edges rule, pilot-scale repeat rule; no
S-UFDF-UNI2, EQ-TFF-188, hold or augmentation study described); mechanism prose matches brief §2b.

## Could not be checked

UF/DF qualification results (none exist); S-UFDF-UNI results (none recorded); RA-001's ranking beyond
PCMP-001 Table 4.1; the A-Mab p.86 citation (a config comment says p.140); process-chemistry statements
(domain knowledge, agree with the brief); SOP contents (placeholders).
