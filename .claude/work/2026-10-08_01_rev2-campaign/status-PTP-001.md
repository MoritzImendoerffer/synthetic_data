# Status — PTP-001 (Process Transfer Plan, Version 2.0) authoring

Author: Claude Opus 5.5 (claude-opus-5-5), one-pass, per authoring/RUNNER.md.
Draft: pc_package/PTP-001_transfer.DRAFT.qmd
Scratch: /tmp/claude-1000/-home-moritz-github-repos-synthetic-data/be14bf3c-e46a-46fd-b419-65482c2add0e/scratchpad/ptp001/

## Inputs read (2026-10-10)
- [x] authoring/RUNNER.md
- [x] authoring/out/PTP-001.brief.md
- [x] authoring/section_plan.yaml (transfer_plan)
- [x] authoring/STORY_BIBLE.md (§3, §9b)
- [x] authoring/WRITING_GUIDE.md
- [x] authoring/REGISTER_EXEMPLAR.md
- [x] procedures/PLAN-LESSONS.md
- [x] data-state-2026-10-10.md
- [x] rendered PCMP-001 Version 2.0 (content only), rendered PTP-001 Version 1.0 (content only)
- [x] helper signatures (_pcpkg, tables, ctable) + probes of the data (scratch probe1-4.py)

## Decisions
- Structure: section_plan transfer_plan order, 11 numbered sections; "Changes in this revision" as §1.1.
- Changes listed (7): approval date + execution windows (revision history says "approval and execution
  dates recorded", so §10 records plan approvals and the windows of the 30 studies of the Version 1.0
  record, end < REV1 effective); IAC references (PCMP-001 V2 §7.3/§7.4/§7.5) in §5, §6.3, §7;
  offset rule (PCMP-001 V2 §7.1) in §4, §5, §8; fragments CQA + nrCE-SDS (AMD-001, finding 6) +
  T.methods_by_study(); SOP-3016/AMV-3021 and the method record (11 rows from dev_methods.csv);
  T.parameters_by_step() in §6.1 with the Version 2.0 NOR/set-point changes (computed sentence);
  package table now lists INV-001/INV-002.
- No study after Version 1.0 described (no hold, augmentation, S-PA-SDM2, S-VI-OFAT, S-CEX-VER, S-VI-WC,
  S-BRX-OSM, *-UNI2). No new rule. V1.0 transfer elements, gap analysis, PPQ strategy kept.
- Restated, because the V1.0 sentence now contradicts the CQA register: "harvest and UF/DF form or clear no
  quality attribute" -> gap accepted on RA-001's basis as PCMP-001 V2 §4 describes it.
- V1.0 "HCP ELISA least precise" is false on the current method record (qPCR 15 %): computed rank instead.
- V1.0 "Table 10.1 gives this plan as the dependency for all four" was false (operator training not a row):
  sentence rephrased.
- Assertions in setup: PTP approval < RA-001 < PCMP-001 < first study; each PCP before its first study;
  last V1.0 study < 2026-07-24; windows overlap; NOR within characterized range; harvest/UF-DF no design;
  fragments set_by harvest; qPCR least precise; AMV-3020 absent from dev_methods.csv; HCP IAC at 3 steps;
  fragments/LRF not compared in sdm_qualification.csv; viral claims meet cumulative requirement.

## Gate log
- check_render pass 1: OK (all chunks/inline eval, tic gate OK, docx+pdf render, 33 pp).
- Table review (pdftoppm, 110 dpi): fixed chronology date wrap, methods column spacing, gap owner width;
  prose revised (glycan separation mechanism, gap basis, duplicate of table note removed).
- check_render pass 2: OK.
- Final pass: change item 5 de-duplicated, "280 nm" written as the method name (A280); quarto render --to pdf
  and --to docx; check_render passes 3 and 4: OK. PDF 33 pp. check_render prose count: 303 sentences,
  5133 words. No <<NEEDS:>>.
- Builder issue, not fixable in the document: T.parameters_by_step() is ~4 lines taller than the page; its
  last notes run into the page number (same in rendered PCMP-001).

## Done (2026-10-10)
- Draft complete and gated. Not committed. Rendered DRAFT.pdf / DRAFT.docx in pc_package/ (untracked names).
- Stale on re-authoring (annex step, not done here): build_ground_truth.py PTP-001 region (Version 1.0
  quotes), ground_truth/PTP-001.json; PTP-001 not yet in REV2_READY. No rhetorical spans file exists.

## Revision run 2 (2026-10-10, after factual-PTP-001.md and feedback-PTP-001.run1.md)
Same author, same draft. Pre-revision copy: scratch/PTP-001.pre-run2.qmd.
- Factual 1: Table 10.2, §10 and §1.1 item 1 count the 27 studies Version 1.0 reported (computed: ended before
  2026-07-24, kinds comparability/retest excluded, asserted = S-CEX-FRC, S-PA-RET, S-VI-RET). Caption
  "studies that Version 1.0 reported". PA 4, VI 4, CEX 4; same span.
- Factual 2: §1.1 item 4 written as PCMP-001 §1.1 item 4 (the addition of nrCE-SDS answers finding 6).
- Factual 3: §6.3 release testing has two exceptions (residual DNA, viral clearance, met through clearance);
  new DNA paragraph (A-Mab claimed range p.47, dose 10 mg/kg p.26 = 700 mg at an assumed 70 kg, qPCR LOQ
  1 pg/mg = 0.7 ng/dose = 700x the criterion, asserted); §5 comparability qualified likewise. §7 had no
  release-testing statement, so nothing added to the PPQ strategy.
- Factual 4: §6.2 titre paragraph cites PCR-005 PD-005-06 (asserted from PLAN_DISCREPANCIES); change 5 too.
- Factual 5: V1.0 sentence on the outputs compared restored in §5.
- Factual 6: virus filter "removes small and enveloped virus" in §6.3; role from UNIT_OP_ROLE.
- Factual 7: "where one is defined" in §6.3 and §7. Factual 8: findings 1 to 3. Factual 9: builder note.
- Factual 10: new change items 8 (corrections of V1.0) and 9 (engineering batches under the master batch
  record, Table 10.1 order; §6.3, gap 4 action and §10 now agree); §8 intro says which actions changed;
  Table 6.2 text matches its caption. Factual 11: PCMP-001 §7.8 wording; ranking among %RSD methods.
- Content review: S-CEX-FRC no longer the basis (PCMP-001 §7.8/AMD-001 are); SEC-for-aggregate attributed to
  PCMP-001; harvest gap basis kept and listed; V1.0 "Its transfer should therefore..." kept (V1.0 text);
  scale-dependent parameters corrected; filters at set pressure; CO2/O2 cause named (solubility, gas flow
  vs kLa); "remaining elements" corrected; "will confirm"; sending-site comparison said once (§5, item 3);
  AMV-3011 vs AMV-3221 named; Protein A/CEX bind the antibody; aggregate also at low pH; "commits the
  studies of its step"; transfer protocol sets the numerical limits; viral margin vs titre precision;
  afucosylation -> FcγRIIIa/ADCC and galactose -> CDC (A-Mab p.38); "virus spiking studies"; reader
  glosses cut; code subjects named. Tables: 2.2 note (criteria basis, VH by rule); 6.3 units per cell.
- Gate: check_render --render run 2 pass 1 OK; two prose fixes; pass 2 OK; explicit pdf/docx renders;
  closing check_render OK (incl. new page-foot check). PDF 35 pp. 335 sentences, 5977 words. No <<NEEDS:>>.
- Table images read: 2.1, 2.2, 6.1 (now fits its page), 6.3, 8.1 (both pages), 10.2.
- Extract refreshed: .claude/work/2026-10-08_01_rev2-campaign/PTP-001_transfer.DRAFT.txt.

## Final pass (2026-10-10, after content-review-PTP-001.run2.md and feedback-PTP-001.final.md)
Same author, same draft. Pre-pass copy: scratch/PTP-001.pre-final.qmd. Shared file touched: references.bib
(one ichq5e entry, ICH style). Coordinator's adjustment to A1 applied: one pointer to PCMP-001 V2 §7.8 as the
rule, no Table 7.3 reference.
- A1: Table 6.4 and every sentence of fragment-method history dropped (retests, re-executed design, S-CEX-FRC
  as basis, "Where the characterization reports base a decision ..."); §6.2 points once to PCMP-001 §7.8;
  the change (nrCE-SDS added, finding 6 answered) kept in §1.1 item 4. A2: PD-005-06 cut (§6.2, item 5); the
  titre is transferred because it sets the protein load of a capture run. A3: "studied in parallel" cut.
- B1: development train defined once in §5 (manufacturing-scale train at the sending site whose batches are
  the reference of each qualification); Table 4.1 row 1 and item 3 agree; V1.0 Table 4.1 row 1 correction
  listed (item 3). No batch count given. B2: gap 1 action = compare engineering batches with the
  development-train batches, recorded in the engineering batch reports (item 3). B3/B4: "set the schedule"
  replaced; closed vs managed gaps named; column "Action that closes or manages it" and caption (item 9).
  B5: ICH Q5E comparison with development-train batches + criteria; "A development mean ..." and the next
  sentence cut (item 8). B6: XMuLV three claimed steps, MVM two (computed from iac.csv), claims per step,
  premise "no step is credited above its claim", margin vs titre precision; lipid envelope named (item 9).
  B7: item 3 limits manufacturing-scale judgements to compared outputs. B8: titre assays out of Table 6.3
  (stay with the spiking studies); Table 8.1 row 2 and §6.2 agree; nrCE-SDS has no performance row,
  validation AMV-3020 in Table 6.2 (item 5). B9: other Table 4.1 elements can affect the process (CO2 uptake
  lowers buffer pH, bioburden; raw-material lots; methods); both buffer preparation and method transfer need
  laboratory work (item 8). B10: fragments assignment attributed to the CQA register of PCMP-001 V2 with the
  §3 basis; judged downstream. B11: AMV-3221 added to Table 6.2 (doc-side list, record title); Stage 2
  covers facility/equipment/utilities (§1, §7); turbidity measured, not set (PCP-004 wording); PPQ sampling
  set by the qualification protocol (FDA 2011); handovers = deliverables of Table 10.1 (items 8, 9).
- C: fragments origin as PCMP-001 §3 words it; claims per step beside the sums; DNA clearance shown in the
  step reports, capability assessed in PCMR-001 (PCMP-001 §7.3); transfer accuracy "within the limits the
  transfer protocol sets", protocol sets the allowed difference between sites.
- D: concentration polarization (UF/DF), pore plugging by aggregates (virus filter), buffer CO2 uptake/pH,
  lipid envelope; "verification-qualified" not in prose; SEC records named (AMV-3221 transferred); §3 ICH Q10
  gloss cut; qPCR ranking sentence cut; "for the reason that" circularity fixed; CA3, findings 1-3 and the
  step of each viral requirement named. V1.0 sentences kept as instructed.
- E: Table 6.4 dropped; Table 10.2 "Approved" header, unit operation column unwrapped (rows on one line);
  Table 2.2 "Criticality level" / "Tool #1 score"; Table 6.1 stray "a)" is a pdftotext artefact (the image
  shows the superscript on the "Number of diavolumes" line), not the builder.
- Gate: check_render --render final pass 1 OK; explicit pdf/docx renders; closing check_render OK.
  PDF 36 pp. 346 sentences, 6432 words. No <<NEEDS:>>. Table images read: 2.2, 4.1 (both pages), 6.1, 6.2,
  6.3, 8.1 (both pages), 10.2. Extract refreshed. Not committed.
