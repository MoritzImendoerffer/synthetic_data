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
