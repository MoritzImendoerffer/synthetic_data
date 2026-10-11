# Status — PCR-010 (Ultrafiltration / Diafiltration) Version 2.0, authoring run

Author: Claude Opus 5.5 (claude-opus-5-5), one-pass, per authoring/RUNNER.md.
Draft: pc_package/PCR-010_ufdf.DRAFT.qmd
Scratch: /tmp/claude-1000/-home-moritz-github-repos-synthetic-data/be14bf3c-e46a-46fd-b419-65482c2add0e/scratchpad/pcr010/

## Inputs read (2026-10-11)
- [x] authoring/RUNNER.md
- [x] authoring/out/PCR-010.brief.md
- [x] authoring/section_plan.yaml (report_nondoe, inherits report_doe)
- [x] authoring/STORY_BIBLE.md (§9b, harvest and UF/DF univariate studies)
- [x] authoring/WRITING_GUIDE.md
- [x] authoring/REGISTER_EXEMPLAR.md
- [x] procedures/REPORT-LESSONS.md
- [x] data-state-2026-10-09b.md, data-state-2026-10-10.md
- [x] rendered PCP-010 (pdftotext)
- [x] rendered PCMP-001 (pdftotext, scratch pcmp001.txt)
- [x] helper signatures (_pcpkg, doe_report, tables, ctable)
- Note: lines of config/parameters.yaml were opened while locating the residual-buffer and skid
  records (outside the read list). No fact in the draft is taken from a config comment; values
  come through CFG / csv() / helpers only.

## Decisions
- No DoE, no model: every output judged on its individual results (REPORT-LESSONS §1 rule 1).
- Aggregate offset applied (scale-down result minus offset); acidic variants and residual buffer
  have no offset (not compared) and are judged as measured (PCMP-001 §7.1, PCP-010 §5.1).
- Qualification approach (PCP-010 §7.1 sets none): conclusion over the NOR = every individual
  result at a level inside the NOR meets the criterion at manufacturing scale; qualified when the
  same at the offset estimate and both CI ends. Stated as the report's approach.
- Buffer exchange: record has one residual-buffer result per run, no pH, no per-DV series. ln fit
  across the DV series; PCP-010 §7.2 plateau criterion not met as worded (falls measurably at every
  level to 10 DV). Reported as not met; no acceptance claimed (no owner risk decision).
- Aggregate rises with final concentration and TMP (significant, small): campaign's own finding,
  presented as a result with size against the 5 % criterion computed.
- PCMP-001 Table 7.1 assumption (no step after CEX changes aggregate): size of the UF/DF increase
  within the NOR stated; no criterion moved (no verification at a step without a model, PCP-010 §7.2).

## Progress
- [x] setup chunk with computed scalars and assertions
- [x] body sections written (all, one pass, 2026-10-11)
- [x] check_render: 8 runs. Run 1 dry (OK). Run 2 --render FAIL (font floor: Appendix A and B tables
      shrunk below 7.9 pt). Runs 3-8 --render OK, with self-review fixes between them (two-line
      headers, no constant columns, zero-count P(OOS) bound, meaning of a very large Cpk, Table 3.1
      "n.a." tied to the report's approach, glycan statement as expectation, excursion vs change in
      the design-space section, largest attribute change incl. the non-significant acidic change).
- [x] pdf + docx render (explicit, after the last edit): PDF 47 pp
- [x] visual check of every complex table and figure (pages 13, 16, 18, 19, 21, 23-26, 31, 33, 35,
      42, 45-47; Table 9.1 and both figures re-checked on the final render)
- Body per check_render: 553 sentences, 10,349 words of prose. No <<NEEDS:>>.

## Hand-back items (departures in neither register, helper issues)
Departures from PCP-010 in neither register (no identifier invented; each stated in the text):
1. S-UFDF-UNI2 ran on EQ-TFF-188; PCP-010 §5.1 plans the studies on EQ-TFF-142, where the offsets were
   estimated. No run compared the skids. PD-010-01's register text does not name the skid.
2. No pH reading and no conductivity series after each diavolume (PCP-010 Table 5.2, §5.5, §7.2). The
   exponential fit was made across the runs of the DV series instead (one result per run).
3. Buffer-exchange criterion of PCP-010 §7.2 (plateau at or below 7 DV) NOT MET as worded: the residual
   falls measurably at every step to 10 DV, and no pH. No owner risk decision exists; objective (iii)
   not met. The lower DV NOR edge (7 DV) rests on the measured residual (at most 0.091 %), not on a plateau.
4. No result for the load pool (A280, SEC, icIEF), the pre-diafiltration retentate or the permeate
   (PCP-010 Table 5.2). The change of aggregate and acidic variants across the step is not available
   (PCP-010 §4.2 says the studies measure what the step adds).
5. Order of execution of S-UFDF-UNI2 not in the record (randomization, PCP-010 §6.2).
6. Load pool(s) of S-UFDF-UNI2 not identified (single pool, PCP-010 §5.2; bridging rule §12).
7. Manufacturing-scale batches of S-UFDF-SDM not named, and no date of the offset calculation
   (PCP-010 §5.1 requires PCR-010 to give both).
8. The qualification compared the aggregate level in the final retentate, not the change across the
   step that PCP-010 §5.1 / Table 5.1 names.
9. Approaches chosen by this report where PCP-010 sets no rule: qualification decision without a
   model (§7.1: every individual aggregate result inside the NOR, offset at estimate and both CI
   ends); "small against the criterion" (§7.3: no threshold, changes and margins given, judged);
   "approaches" (§4.3: no threshold, edge margins given, judged); assay-noise rule vs slope test
   (§5.3: both applied to aggregate, they agree); plateau tolerance and pH (§7.2: none set after the
   data, plateau as §5.5 defines it).
10. Version 1.0 of PCR-010 read acidic variants against 40 % alone (PCP-010 change 1: "PCR-010 records
    the departure"); recorded in "Changes in this revision" only, no register entry.
11. The study-event records (DEV-010-01, -02) name no study and no run.
Substantive results for the owner:
12. PCMP-001 Table 7.1 assumes no step after CEX changes aggregate. UF/DF final DS concentration and
    TMP raise aggregate (significant); up to 0.06 pp above set-point at the NOR corner (sum of slopes).
    No criterion moved (no verification at a step without a model, PCP-010 §7.2); the CEX aggregate
    criterion (5.00 %) makes no allowance for it. DS aggregate Cpk 15.7, 0 of 2,000 batches outside.
13. TMP is KPP, but its only measured effect is on aggregate (a CQA, significant, 0.06 pp across the
    PAR); its performance effect (flux) was not measured across the range, so the KPP class rests on
    the mechanism plus the PCMP-001 §7.7 "too small" judgement.
Helper / record notes:
14. T.methods_by_study(["ufdf"]) prints "no DoE" for aggregate and fragments and says nothing of the
    SEC aggregate results of the univariate and qualification studies (text explains it).
15. capability.csv rounds means and SDs to 4 decimals (residual DNA prints 0.0002 ± 0 via cap_for);
    means and SDs taken from monte_carlo.csv instead.
16. The record names no method for residual_buffer_pct. Lines of config/parameters.yaml were opened
    (outside the read list) while locating the record: they call it a conductivity-based estimate and
    map the S-UFDF-UNI2 aggregate repeatability to AMV-3221 (verification-qualified SEC), whereas the
    plan and UFDF_AMV_REFS name AMV-3011. The draft uses AMV-3011 and takes no fact from config comments.

## Fix pass 1 (2026-10-11, same author, after content-review-PCR-010.md, factual-PCR-010.md, feedback-PCR-010.run1.md)
Inputs read: feedback-PCR-010.run1.md, content-review-PCR-010.md, factual-PCR-010.md, data-state-2026-10-11.md,
REPORT-LESSONS §3 rule 1, §6, §7, regenerated brief (authoring/out/PCR-010.brief.md), rendered PCMP-001 (§7.3, §7.5,
§7.7, §7.8), rendered PCP-010 (§4.1, §4.3, §5.5, §7.2, §7.3, §8), rendered Version 1.0 PCR-010, A-Mab pp. 47, 57, 114.
Backup of the pre-fix draft: scratchpad pcr010/PCR-010_ufdf.DRAFT.pre-fix1.qmd. File edited: pc_package/PCR-010_ufdf.DRAFT.qmd only.

Setup changes (assertions):
- Register: `len(PDS) == 1` replaced by PD-010-01..07 (`PD` dict, plan PCP-010, studies only on -01, -01 names both
  skids, -02 conductivity, -07 minimum). Pins the seven register mentions.
- Cation exchange: `D.acceptance_basis("cex", agg) == "drug substance"` and `_cex == DS criterion` replaced by
  "tightened on verification", `CEX_AG = 4.90`, iac.csv row tightened, `AG_HI - UF_ALLOW == CEX_AG`, UF/DF verification
  row (add_max 0, not met, difference offset = report offset, adequate, gap <= 0.2, LoF p > 0.05). Pins "tightens ... to 4.90 %".
- One-sided diavolume NOR: `ONE_SIDED == {diavolumes: low}`; `nor_s`/`nor_cell` print "≥ 7 DV"; in-NOR test one-sided
  (N_IN_NOR now counts 10 DV); MARG high of diavolumes is None (n.a.).
- Corner argument per run (SP_AGG_MFG_MAX, RATIO_RNG > 10); E5 drop-one offsets (0.010-0.026, highest 0.80, margin 4.20);
  acidic Cpk at the study mean with the simulated SD (0.63 < minimum; every result below the simulated mean); AC_MIN ties.

Items resolved (where): A1 diavolumes one-sided (§1.4 item 9, §4.1, Tables 4.1/7.1/7.2/9.1, §7.3, §10, figures);
A2 PD-010-07 (exec, §1.4 item 10, §5.5, §10 item 3, §12.3, §13.2; both plan conditions quoted, "could not be judged as
planned", no "not met", no release value claimed); A3 allowance 0.104 -> 4.90 % (exec, §1.4 item 11, §7.1 with the
verification analysis PCMR/PCMP-001 asks PCR-010 to give, §9, §10 item 2, §11, §12.2); A4 second skid accepted with
argument (exec, §3.1, §11, §12.1; §4.2 claim reduced to levels, replicates, skid as the entry now carries); A5 p.114
(§1.3, §2.1). B: PD-010-02..-07 each cited where relied on and each described in §13.2. C: E1 §6; E3 §10 item 1;
E4 §3.5/§8; E5 §13.1.2; E6 §5.5/§12.3; E7 §2.1; E8 §5.5; E9 exec/§5.4/§8/§12.5; E10 §3.1/§11/§12.1; E12 §8 (p.47 and
p.57); E13 §3.3; E14 §1.4; minors (PCMP-001 §5, §1.4 item 5 refs, §2.3 Statistics and QA, §3.5 PAR wording, §7.3 per
run, §13.1.1 two-sided CI wording, CEX/HPLC/UV/n.a. abbreviations, yield pure error 2.08). D: Q1 causes with
direction (§2.1 Donnan/volume exclusion, limiting flux, deamidation; §2.3; §4.1; §5.4; §8; §9; §11), Q2 (residual
process buffer measurand stated as not named, limiting flux defined, §6.4 analysis explained, corner runs, table
headers), Q3 filing sentences removed, Q5 1-11 (KPP definition quoted with "practically relevant" and the too-small
clause; TMP class argued as a judgement of practical relevance), Q6 machine sentences removed, Q7 codes given context,
tables (5.1 headers, 5.2 units and no Yes/No column, 7.1 ranges and no constant column, 8.1 no verbal column and DNA
to 3 significant figures, 9.1 class and p columns, A.1 manufacturing-scale aggregate column, Table 3.3 dropped as
empty), figures (5.1 at manufacturing scale, 5.2 caption explains the log scale).
Gate: check_render --render pass (exit 0) twice; pdf + docx rendered; check_render once more pass. 53 pp; 629 sentences,
11,852 words of prose. No <<NEEDS:>>. Page images read: Tables 4.1, 5.1, 5.2, 7.1, 7.2, 8.1, 9.1, 13.2, A.1, Figures 5.1, 5.2.
DRAFT.txt refreshed (pdftotext -layout). No annex work.
Left for the coordinator: see the hand-back (helper tables, the unplanned verification at UF/DF, brief wording).

## Final pass (2026-10-11, same author, after content-review-PCR-010.run2.md and feedback-PCR-010.final.md)
Inputs read: feedback-PCR-010.final.md, content-review-PCR-010.run2.md, data-state-2026-10-11.md, REPORT-LESSONS §6 and §7,
regenerated brief, register entries PD-010-01..08, rendered PCMP-001 (§7.2, §7.5, §7.7), PCP-010 §8, A-Mab pp. 47-48
(Table 2.17), amab_process/studies.py `_sample_overrides` and amab_process/iac.py `_univariate_increase` (read only).
Backup of the pre-final draft: scratchpad pcr010/PCR-010_ufdf.DRAFT.pre-final.qmd. File edited: pc_package/PCR-010_ufdf.DRAFT.qmd only.

Setup changes (assertions):
- Register now PD-010-01..08; PD-010-07 reason pinned to "lowers the residual process buffer further" (no "only lowers");
  PD-010-08 pinned (subject "Aggregate verified", planned cites §7.2, done cites §7.5).
- F-test of the verification fit (criterion 1 of PCMP-001 §7.2, not in iac_verification.csv) computed with
  amab_process.adequacy.adequacy on the same data; asserted to reproduce the csv's R²-gap and lack-of-fit p (1e-3), f_ok and adequate.
- DV_SIM_SD = (NOR high - NOR low)/6 and DV_COMBO_HI = NOR high of the diavolumes (from config), asserted SP < NOR high < range high.
- DNA_LOQ from dev_methods.csv (AMV-3014, pg/mg) and the ratio LOQ / simulated DS level (asserted > 1000).

Items resolved: Q5.1 (§4.1 once, with the diavolume slope on aggregate; removed in §1.4 item 9, §5.5, §10 item 3); Q5.7
(§3.5 simulation spread, §7.1 upper combination value); Q5.3 (§9 intro and the TMP and final concentration bullets, one
judgement naming, NOR change vs margin, bound, flux not measured; §12 item 5 gives numbers); Q5.2 (§2.1, §2.3, §4.1, §5.6
corrected wall-concentration premise; campaign's own addition stated in §2.1); Q5.4 (§3.5, §7.1 with the F-test); Q5.5 (§8);
Q5.6 (§7.1); Q4 (§8 "acceptable" removed; exec and §12 give 0.63); Q1 (§2.3 clause, Table 5.2 note, §13.1.2 hold-up
"record does not say how", §9 numbers); Q2 (residual process buffer defined in §3.3, "allowance" removed everywhere,
"concentrated further" in §13.1.2); Q3/Q6 glosses and restatements removed (§3.1, §4.2, §5.3, §5.4, §5.5, §6, §7.2, §7.3,
§13.2; PAR limitation 3 kept, the earlier duplicate sentence removed); Q7 (§2.3, §3.1, §5.3, §5.5 objective iii, §7.1 rule 1
and subject, §11, §12 item 1, §13.2 PD-010-03/-04/-05 named by content, exec summary subjects and "it"). PD-010-08 cited in
exec, §4.2, §7.1, described in §13.2. D-001 untouched.
Gate: check_render --render exit 0 (twice); pdf + docx rendered; check_render once more exit 0. The numeral lint stays
advisory (44 lines, 42 before; the two new ones are section numbers and the 95 % convention). 54 pp; 634 sentences,
12,284 words of prose. Page image read: Table 5.2 (the only table changed, its note). DRAFT.txt refreshed. No annex work.
