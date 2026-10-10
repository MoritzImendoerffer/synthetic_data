# Factual check of PTP-001 Version 2.0 (draft text of 2026-10-10)

Checker: Claude Opus 5.5 (claude-opus-5-5). Returned as text; saved by the coordinator (condensed, every
error kept). Scratch: `scratchpad/chron.py` (recomputes Table 10.2).

## Errors, most consequential first
1. **Table 10.2, §10 and §1.1 item 1 count 30 studies "recorded in the Version 1.0 reports"; Version 1.0
   reported 27** (INV-001 §1: "Version 1.0 reported 27 studies, executed between 2025-08-11 and
   2026-05-15"; S-CEX-FRC, S-PA-RET and S-VI-RET "produced only fragment results, which Version 1.0 did
   not report"). The 30 are the studies that ended before the package date. Without the three: Protein A
   4 studies (2025-11-05 to 2026-02-06), low-pH 4 (2026-01-07 to 2026-02-13), CEX 4 (2026-02-04 to
   2026-03-27); total 27; same span; every plan still approved before its first study. Fix: use the 27,
   or relabel as "studies executed before the Version 1.0 reports were approved" and add that three gave
   fragment results only. (PCMP-001 §5 avoids a count.)
2. **§1.1 item 4 "The decision answers INV-001 finding 6"** has the order wrong (AMD-001 2026-03-20;
   INV-001 opened 2026-08-03). Finding 6 records the SEC bias behind the decision and that the decision
   had not reached the Version 1.0 documents; CA2 carries it into the plans. Fix: write it as PCMP-001
   §1.1 item 4 does (PCMP-001 sets nrCE-SDS, following AMD-001; this answers finding 6).
3. **Residual DNA cannot be release-tested against its criterion** (AMV-3014 LOQ 1 pg/mg = 0.7 ng/dose
   at 700 mg, 700 times the 0.001 ng/dose criterion; the modelled drug substance is about 0.00017
   ng/dose). §6.3 "Release testing confirms the attributes of the drug substance against Table 2.2" cannot
   hold for DNA. Coordinator: A-Mab's control strategy for DNA is "None as DNA is consistently cleared from
   the process" (A-Mab p.47); the corpus judges DNA through the clearance and the integrated model
   (PCMP-001 §7.3, §7.9). Say that DNA is controlled by demonstrated clearance, not by a release test.
4. **A rule added after the data, with no source** (§6.2: "The protein load of the Protein A step is set
   from that result. Protein concentration by A280 ... cannot set the load."): it is PCR-005's discrepancy
   PD-005-06 (2026-10-09); PCMP-001 does not state it; PCP-005 Version 1.0 planned load and pool mass by
   A280. Fix: cite PCR-005 (PD-005-06) in §6.2 and change 5, or cut to the transfer need.
5. **A Version 1.0 statement deleted and not listed**: Version 1.0 §5 "The comparison is then made on the
   outputs the step controls ... step yield, pool volume and the impurity levels in the pool ... viable
   cell concentration, titre and the product quality attributes". Fix: restore it (the reports record
   the departure) or list the deletion under change 3.
6. **The virus filter's XMuLV credit is missing from the text**: the XMuLV sum of 16.72 includes its 4.62
   claim (iac.csv; PCMP-001 Table 7.2), but Table 2.1 gives XMuLV credit only to steps 6 and 8 and §6.3
   says "the virus filter removes small virus by size". Coordinator: the step role in `UNIT_OP_ROLE` is
   corrected centrally.
7. **Two statements too general**: §6.3 "each step output on which a drug substance criterion depends is
   judged against an intermediate acceptance criterion" (DNA has none, fragments none at harvest,
   bioreactor harvest HCP none); §7 "Each intermediate is then tested against the same intermediate
   acceptance criterion" (harvest and UF/DF have none). Fix: "where one is defined".
8. **§1.1 item 2 cites findings 1 and 2**; finding 3 (bioreactor glycan and acidic-variant limits from
   capability data) also concerns those limits: "findings 1 to 3".
9. **Footnotes c3 and c5: "the set-point the studies were run around"** for pH 3.5 and 90 min; the
   low-pH designs were centred at pH 3.6, 120 min and 20 °C. From the shared builder (PCMP-001 Table 4.2
   too). Coordinator: the builder note now says the set-point of the characterization plan.
10. **Changes not listed** although §1.1 ends "otherwise as Version 1.0 stated them": §4 reason for the
    NORs ("characterized ranges are wider than the control capability of either site" became "every NOR
    lies within the characterized range"); Table 2.1 rows for steps 5, 6 and 8 rewritten (Version 1.0:
    step 6 "sets the cumulative XMuLV", step 8 "sets the cumulative MVM"); §2 "belong to no single step"
    reversed to "The register assigns each to one step"; §8 says the gaps "were identified at the approval
    of Version 1.0" but the table now carries nrCE-SDS, the offset rule and "the plan and the report";
    §10 dependency sentence dropped (correctly) but not recorded; Table 6.2 caption "referenced in this
    document" vs the text "in scope for the transfer".
11. Nits: "qPCR is the least precise" leaves out the infectivity titres (0.3 log10); "fragments are
    measured by nrCE-SDS in every study at every step" (S-AEX-UNI, S-UFDF-UNI, S-VF-SDM measured none;
    coordinator: corrected in PCMP-001 §7.8).

## Checked and correct
Title block, revision history; 22 documents (Table 1.1); approval dates of PTP-001, RA-001, PCMP-001 and
every plan; S-BRX-SDM start; plans before studies; span 2025-08-11 to 2026-05-15; 2026-07-24 (finding 5);
INV-001 dates and class; CA3; S-CEX-FRC before AMD-001; retests 2026-04-06 to 2026-04-17; process facts
(15,000 L, 75 g/L, 8 steps, 5 PPQ batches); Tables 2.2, 5.1, 6.1 (37 rows; class counts 1/20/10/6), 6.2,
6.3 (AMV-3020 not in the record), 6.4; PCMP-001 rules restated (§7.1, §7.3, §7.4, §7.5, §7.7, §7.8, §4).

## Could not check / older inconsistencies
RA-001, PCR-005/006 and PCMR-001 Version 2.0 (drafts not opened). Table 6.2 lists AMV-3011 for SEC while
Table 6.3 and the gap action point to AMV-3221 (Version 1.0 too). Version 1.0 PCR-004 claims a qualified
harvest scale-down model, but the record holds no harvest qualification study (owner Q8: PCR-004 records
it as a deviation).
