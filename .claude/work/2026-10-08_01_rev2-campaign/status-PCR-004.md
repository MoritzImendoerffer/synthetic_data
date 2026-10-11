# Status — PCR-004 (Harvest and Clarification) Version 2.0, authoring run

Author: Claude Opus 5.5 (claude-opus-5-5), one-pass, per authoring/RUNNER.md.
Draft: pc_package/PCR-004_harvest.DRAFT.qmd
Scratch: /tmp/claude-1000/-home-moritz-github-repos-synthetic-data/be14bf3c-e46a-46fd-b419-65482c2add0e/scratchpad/pcr004/

## Inputs read (2026-10-11)
- [x] authoring/RUNNER.md
- [x] authoring/out/PCR-004.brief.md
- [x] authoring/section_plan.yaml (report_nondoe, inheriting report_doe)
- [x] authoring/STORY_BIBLE.md (§9b incl. "Harvest and UF/DF univariate studies", "Hold studies")
- [x] authoring/WRITING_GUIDE.md
- [x] authoring/REGISTER_EXEMPLAR.md
- [x] procedures/REPORT-LESSONS.md
- [x] data-state-2026-10-09b.md, data-state-2026-10-10.md
- [x] rendered PCP-004 (pdftotext, scratch pcp004.txt)
- [x] rendered PCMP-001 (pdftotext, scratch pcmp001.txt)
- [x] helper signatures (_pcpkg, doe_report, tables, ctable)

## Decisions
- No DoE. S-HAR-UNI (Version 1.0) has no data; every result is from S-HAR-UNI2 (PD-004-01) and S-HAR-HLD (PD-004-02).
- Effects: linregress of each response on the setting (brief, owner's option A), alpha = THRESHOLDS effect_alpha.
  Check with the set-point replicates as the error term (PCP-004 §5.5 wording): same decisions (asserted).
- Clarification criterion (PCP-004 §7 criterion 2): post-clarification turbidity <= NOR high of turbidity, judged on
  individual results. Depth filter load fails at the top level -> PAR bounded at the last level that passed; NOR high on
  the PAR edge (stated, hand-back).
- Criteria 1 and 3 cannot be applied as written (no result for the unclarified culture): judged by the slope against the
  setting (approach stated, hand-back).
- Hold judgement: level entering (bioreactor single-batch limit over the NOR at manufacturing scale for aggregate and
  acidic variants; highest S-HAR-UNI2 result for fragments) + largest change; criteria = bioreactor criteria in force
  (pass through harvest); fragments against the drug substance criterion (no fragments criterion at harvest; strictest in
  the train, asserted). Acidic variants lower end not met at entry (PCR-003).
- Scale-down model not qualified (PD-004-03): every result at the scale of the study, offset unknown, not zero.

## Progress
- [x] setup chunk (all deciding words asserted; tables use unique row variables, the gate re-evaluates them)
- [x] body sections, report_nondoe order (exec summary .. record, references, appendices A-C)
- [x] check_render: 13 runs; runs 1-2 failed (missing scalar WARM_COLD_FRAG; two tables sharing `_rows`, which the
      gate's table-fit check re-evaluates in the final namespace); runs 3-13 passed, exit 0
- [x] final pdf + docx render (quarto render --to pdf, --to docx), then check_render once more: pass
- [x] every complex table and figure looked at (110 dpi); fixed: Table 5.2 layout, Table A.1 header collision,
      Table 7.1 row rules, column widths of Tables 5.3/4.2; hold figure on a common size-variant axis
- Result: 49 pp; gate counts 563 sentences, 10,643 words of prose; no <<NEEDS:>>
- Concurrent edits by others during the run (config risk_mitigation alarm rule, doe_report.control_par, STORY_BIBLE):
  harvest action limit 18.72 % and monitoring text unchanged; final gate ran on the current state

## Hand-back items (departures in neither register, helper issues)
1. Unclarified culture not sampled/recorded (PCP-004 §5.4 four points; §7 criteria 1 and 3 compare within a run):
   criteria 1 and 3 judged on the slope against the setting instead (report's own approach).
2. Centrate HCP/DNA and filtrate samples not recorded (§5.4).
3. Filter pressure not measured (objective 3); Protein A load challenge not run (§6.2: column pressure, cycle yield).
4. Depth filter load series not run on centrate from 6,000 g and 12,000 g (§5.5 bracket); run once at set-point field.
5. Levels differ from Appendix A: rcf 7,500/10,500 (NOR limits 8,000/10,000 not run); turbidity 3/12.5 (NOR high 10 not run).
6. Viability and cell density of the cultures not recorded/reported (§12 risk 2); run order not recorded (§6.2 randomized).
7. Fragments measured in S-HAR-UNI2 although PCP-004 says fragments are not a response (inside PD-004-01's study, not named in it).
8. Error term: slope tested with the regression residual (brief, linregress), PCP-004 §5.4/§5.5 name the set-point replicates;
   both give the same decisions (asserted, Appendix B).
9. PCP-004 §8 rules left to the report (resolution size not needed; no R2/RSE threshold; turbidity PAR by criteria 1 and 3;
   two-series DFL rule moot) - approaches stated, in no register.
10. Step yield and the per-mg HCP/DNA rest on an antibody concentration whose method the record does not name
    (REPORT-LESSONS §2 rule 8 says titre assay SOP-3016/AMV-3021).
11. Config analytics.univariate_nodoe.assay maps aggregate_out_pct to AMV-3221 (verification-qualified SEC), PCP-004 names
    AMV-3011; the report writes "SEC" for the study results.
12. DFL upper NOR limit (140) sits on the PAR edge (no margin) - data may argue for a NOR or control decision (owner).
13. GPP class of post-clarification turbidity rests without the planned Protein A load challenge (mechanism expects a
    process-performance effect on resin life).
14. PCMP-001 Table 9.1 lists no re-analysis study of harvest (S-HAR-UNI2, S-HAR-HLD); records name no equipment for them.

## Helper / gate observations
- T.methods_by_study(["harvest"]) shows only "no DoE"; it ignores method_plan.csv rows of S-HAR-UNI2/S-HAR-HLD
  (lmw_cesds True). The report adds its own responses-and-methods table.
- capability.csv rounds mean/SD to 4 decimals, so cap_for prints residual DNA as "0.0002 ± 0"; the report takes mean
  and SD from monte_carlo.csv and Cpk from cap.
- check_render table-fit check re-evaluates each builder call in the final namespace: chunks must not share row variables.
- dev_register outcome "run retained in the analysis" for S-HAR-UNI, a study with no data in the record; the report says
  Version 1.0 retained the run and no result of that study enters this report.
- brief §2b (authoring/mechanism/harvest.yaml) still says shear rises "in the feed zone and at the disc stack"; PCP-004
  Version 2.0 change 7 corrected this (laminar, low-shear flow between the discs). The report follows the plan.

## Fix pass 1 (2026-10-11, after factual-PCR-004.md and feedback-PCR-004.run1.md)
- [x] brief regenerated (register PD-004-01 to -08)
- [x] A: PD-004-04..08 described in §13.2 and cited where relied on (§1.2, §3.2, §3.4, §3.5, §4.2, §7, §9, §11);
      completeness claims removed (§1.4 item 5, §13 opening); PD-004-02 wording (E8) in exec summary, §3.5, §12, §13.2
- [x] B: E2 (§3.5, §8), E3 (§7, §13.1.2), E4 (§1.4 item 7), E5 (§3.3, Tables 3.1, 3.2, 5.1, C.1, §5.1), E6 (§11),
      E7 (§1.2), E9 (§4.3, §5.6), E10 (§3.5, §4.2, §13.2), E11 (§5.5, §8), E12 (§2.2), E13 (§3.5 item 1),
      E14 (Table B.1 note, §3.4, §7); error term: set-point replicates decide (Table 5.3, §3.5), residual as
      sensitivity (Appendix B); practical significance across the NOR (§3.5 rule, §5.2, §5.3; -24.6, -0.22, +2.84 NTU)
- [x] D: DFL NOR edge on an unqualified model + reliance on the turbidity IPC (§7, §9, §10); GPP basis (§9)
- [x] E: gate 8 runs in this pass (1st failed: setup still asserted 3 register entries; 7 passed); PDF + DOCX
      rendered, check_render once more: pass, exit 0; page images of Tables 3.1, 3.2, 5.1, 5.3, 13.1, 13.2, B.1, C.1
      read; DRAFT.txt refreshed. 55 pp; gate counts 627 sentences, 12,176 words of prose; no <<NEEDS:>>

## Fix pass 1 hand-back
- PD-004-01 "Done" says the plan did not name residual DNA as a response; PCP-004 §1, §5.3, §7 criterion 1 and
  Appendix B name it. The text cites PD-004-01 for the levels and fragments only.
- Not in a register: the analysis by culture (PCP-004 §12 item 3), impossible because the record names no culture
  per run; the investigation of the 160 L/m2 failure before the range is reported (PCP-004 §7), which has no
  record; the fragments comparison of the held pool with the drug substance criterion (PD-004-02 names only the
  entering level and the reading of the change).
- Gap, not a departure: no method in the record for the antibody concentration (step yield, per-mg HCP and DNA).
- No builder found wrong in this pass. Register tables leave white space where a long row cannot break (layout).

## Data-state pass 2026-10-11 (after commit 51fa592, data-state-2026-10-11.md)
- Setup chunk passed unchanged; first gate on the new data passed (exit 0). Every criterion value is computed, so
  the bioreactor aggregate criterion moved by itself from 6.46 to 6.30 % (§2.2, §5.5, Table 5.5, hold judgement,
  Appendix). Held harvest still meets the aggregate criterion (2.49 % expected after 7 days at 21 °C).
- Fixed §2.2 derivation sentence: it printed `downstream_added` (now 0.64 = UF/DF 0.10 + low-pH 0.54) as "the
  aggregate increase of low-pH viral inactivation". It now names the three verified worst cases (UF/DF increase,
  cation exchange fold, low-pH increase), each from `D.iac_verification()`, at manufacturing scale, and says the UF/DF
  increase replaces PCMP-001's no-change assumption. "It is stricter" -> "The aggregate criterion is stricter".
- New setup assertions: UF/DF and cation exchange aggregate rows not met, low-pH row widening supported; the cation
  exchange bound equals the row's fold; (DS - UF/DF) x fold - low-pH = criterion; UF/DF + low-pH = downstream_added
  (rtol 1e-3, the CSV keeps 4 decimals).
- Also moved in the render (no prose depends on it): drug substance HCP Cpk 6.17 -> 6.14 in Table 8.1.
- No verification statement, no count of tightened/widened criteria and no cation exchange criterion in the text.
- pdf + docx rendered; check_render pass (exit 0); page images of Table 5.5 (p. 33) and Table 8.1 (p. 39) read.
  55 pp; 630 sentences, 12,214 words of prose. DRAFT.txt refreshed (pdftotext -layout).

## Final pass (2026-10-11, after content-review-PCR-004.md and feedback-PCR-004.final.md)
- [x] Config moved under the draft: PD-004-01 (fragments only) and "the record gives no reason" (PD-004-06, -07) picked
      up in the render. PD-004-07 prose no longer gives the tautological reason. PD-004-04/-05 keep the register's own
      reason ("not scheduled in the study record").
- [x] Q1 causes: §1.1 (two ways the settings change the feed), §3.3 (HCP co-elutes with LMW in SEC), §5.7 (field and
      load change the fine material, proteases and deamidation run faster when warm), §11 (settling velocity).
- [x] Q2 terms: "repeatability limit" defined in the exec summary and §3.5 (2.77 x SD), used in §5.2, §7, §9;
      "largest change from day 0" (§3.5 rule 2, exec summary, §5.6); "every parameter at set-point" (§3.4, §5.1,
      Table 5.3 note, Table 7.1 note, App. B); 9.30 % explained in §2.2; "Monte Carlo simulation of the whole train
      through the step models" (exec summary, §3.5), §8 refers back; Table 8.1 caption.
- [x] Q3/Q6: filing glosses removed (§2.1, §1.4 last sentence, §4.2, §4.3, §5.5, §5.6, §5.7, §6, §7 x2, §8, §10);
      §1.1 padding removed; held-pool rule and the after-the-results rules stated in §3.5, referred to elsewhere;
      "no result of S-HAR-UNI enters" once in §13.1 (plus exec summary); "rests on S-HAR-UNI2" in §1.4 only; PCMR-001
      roll-up once (§10); culture of the pool once (§4.3). Table 3.3 (methods_by_study, "no DoE" only) and its
      sentence dropped; Table 3.2 gives the methods by study.
- [x] Q4/Q5.1: Table 7.1 p-values now from the set-point replicates (p_sp), note names the error term.
- [x] Q5.2: §7 criterion 2 (NOR basis, set from production; why the DFL PAR stops at 140) and the turbidity paragraph
      (PAR 1-20 NTU = no effect on attributes measured, not Protein A performance, PD-004-05); exec summary, §10.
- [x] Q5.4 §2.1 disulfide reduction + expectation 3; §5.7 rcf slope of fragments. Q5.5 model harvest value removed
      from §5.5 and §8. Q5.6 ratio on the largest change (2.3). Q5.7 §10 item 4. Q5.8 §2.2 margin (DNA_MARGIN, 0.8).
      Q5.9 §9 GPP as judgement. Q5.10 Table 5.2 centrate mean column, text means n1, fall from the rounded means.
      Q5.11 §10 "detects", release to capture (PCP-004 §5.3).
- [x] Q7: events named (exec summary, §12 item 7), objectives 1-5 named (§1.2), §11 rewritten (studies and
      discrepancies by what they are), §5.6 subject, §5.5 referent removed.
- [x] Gate: check_render --render exit 0 (3 runs this pass), quarto pdf + docx, check_render once more exit 0.
      Page images of Tables 5.2, 7.1 and 8.1 read. DRAFT.txt refreshed. 55 pp; 629 sentences, 12,302 words.
