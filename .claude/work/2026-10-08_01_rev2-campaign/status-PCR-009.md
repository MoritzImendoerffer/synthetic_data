# Status — PCR-009 (Small-Virus Retentive Filtration) Version 2.0, authoring run

Author: Claude Opus 5.5 (claude-opus-5-5), one-pass, per authoring/RUNNER.md.
Draft: pc_package/PCR-009_virus_filtration.DRAFT.qmd
Scratch: /tmp/claude-1000/-home-moritz-github-repos-synthetic-data/be14bf3c-e46a-46fd-b419-65482c2add0e/scratchpad/pcr009/

## Inputs read (2026-10-11)
- [x] authoring/RUNNER.md
- [x] authoring/out/PCR-009.brief.md
- [x] authoring/section_plan.yaml (report_doe)
- [x] authoring/STORY_BIBLE.md (§9, §9b)
- [x] authoring/WRITING_GUIDE.md
- [x] authoring/REGISTER_EXEMPLAR.md
- [x] procedures/REPORT-LESSONS.md
- [x] data-state-2026-10-09b.md, data-state-2026-10-10.md
- [x] rendered PCP-009 (pdftotext, scratch PCP-009.txt)
- [x] rendered PCMP-001 (pdftotext, scratch PCMP-001.txt)
- [x] helper signatures (_pcpkg, doe_report, tables, ctable); adequacy.* via inspect only

## Decisions
- Selected models (CA3): MVM = straight line in filtration volume (raw scale), meets criteria 1-3, FAILS criterion 4 (run 5 Cook 0.79 > F median 0.74; run 2 flagged above 4/n). XMuLV = pressure only, no adequate model (F p 0.053, gap 0.245) -> measured results, all >= 4.62. Fragments and step yield = no term.
- Deletion analysis: run 5 and run 2 (flagged) plus every other run deleted in turn (covers the two study events whose runs the record does not name). Judgement over the NOR never changes; run 5 (and run 7, via log scale) carry the volume PAR edge and the design space to the end of the range. Model of all runs kept (narrower range).
- Fragments run 9: deletion leaves a no-term model that fails the overfitting limit only because gap = (2n-1)/(n-1)^2 exceeds 0.20 at n = 11; judged on measured results, no conclusion changes.
- D-001: PAR analyses described without saying where the other parameter is held; par_table printed as it comes (T.frame, merged cells, inward-rounding note).
- No fig_rsm_contours (would draw a predicted XMuLV surface); own figure of measured results with the MVM lines (all runs / run 5 deleted).
- Step yield: record holds the value only, from spiked runs; method not in record -> stated, hand-back.
- Departures not in either register listed in the record section without identifiers (7 items) and handed back.
- Pressure classed WC-CPP in config although no significant term: class argued on claim scope + mechanism, flagged as not following the PCP-009 rule; hand-back.
- criteria_results builder: PDF twin header wrapped doc-locally (layout only) to stay above the 8 pt floor.

## Progress
- [x] setup chunk with computed scalars and assertions
- [x] body sections written (one pass)
- [x] check_render: 7 runs. Run 1 FAIL (3 table calls not evaluable, a shared _rows variable), run 2 FAIL (font floor p.33 criteria_results 5.9 pt, p.51 appendix D 7.8 pt), runs 3-7 OK
- [x] pdf + docx render (53 pp; check_render: 551 sentences, 10,763 words of prose)
- [x] visual check of every complex table and figure (pdftoppm -r 110); figure 5.2 fonts enlarged and re-checked

## Hand-back items (departures in neither register, NOR changes, helper issues)

Departures from PCP-009 in neither register (stated in §13.3 of the report without identifiers):
1. S-VF-SDM measured step yield only; flux decay profile and post-use integrity test not measured (PCP-009 §5.1). Objective 1 not met as stated.
2. No pre-use/post-use integrity test result for any design run (PCP-009 §5.2); no run excluded.
3. Step yield reported from spiked design runs; PCP-009 §5.4 names an unspiked load and unspiked filtrate pool. The record holds only the yield value (no protein concentrations, no method, no spike correction).
4. No filtrate fraction results (PCP-009 §5.4); one LRF per run.
5. No spike titres, limit of detection, lower-bound flags, cytotoxicity/interference/spike recovery controls (PCP-009 §5.3), no achieved titre per run (§12).
6. Load material per run not identified (§12); flux decay of spiked runs vs qualification runs not compared (§12).
7. Filtration pressure: config class WC-CPP, but no term containing pressure is significant for any output, so by the PCP-009 §7 / PCMP-001 §7.7 rule it has no effect on a CQA (GPP by the rule). Owner decision needed.
8. Analyses the plan does not contain: deletion of every RSM run in turn (to bound the two events whose runs the record does not name); t-test of the screening vs RSM fragment curvature (REPORT-LESSONS §2 rule 5); Shapiro-Wilk and the single-run-limit reading of the Version 1.0 kept conditions (PCP-009 §7 delegates these to the report).
NOR changes: none argued by the data.
Helper issues: D.anova_lof_df ZeroDivisionError for a no-term model; T.criteria_results spanning header unwrapped (5.9 pt when an output has no model; wrapped doc-locally, PDF only); D.governing_factor docstring says RSM, code reads screening; D.center_cv_df omits fragments; fig_rsm_contours would draw a predicted XMuLV surface; attribute labels differ across builders (ATTR_NAME / RESP_LABEL / register); D.par_table gives the no-model XMuLV rows ranges (REPORT-LESSONS §1 rule 10); model_reevaluation prints hyphen minus; gap of a no-term model = (2n-1)/(n-1)^2 depends only on n.

## Fix pass after the factual check (2026-10-11, same author, Claude Opus 5.5)
Inputs: feedback-PCR-009.run1.md, factual-PCR-009.md, REPORT-LESSONS §3 rule 1, §6, §7; brief regenerated (par_table n.a. for XMuLV, PD-009-03 to -07).
- A register: PD-009-03..07 described in §13.2 and cited where relied on (§3.1, §3.2, §3.5); §13.3 "other departures" removed; "not recorded" for the record's silence; Version 1.0's post-use claim stated (§3.1, §11, PD-009-03).
- B builders: par_table n.a. (XMuLV sentences, Table 7.3 note, §1.2 clause dropped, §1.4 Version 1.0 XMuLV PARs withdrawn); criteria_results re-rendered (attribute column wrapped on the instance, layout only: notes were 7.8 pt); model_reevaluation minus signs; anova unchanged in use.
- C errors: E2 qualification runs made; E3 §5.2 vs §5.4 conflict (PD-009-05); E4; E5 fragments deletions (gap fixed by n, criterion 3 judges n; what does not change); E6 event claims limited (single RSM run only; screening and qualification runs; lot over several runs); E7 recomputed with inward rounding; E8 p ≥ 0.48; E9 p = 0.0497 (alpha-aware p format); E10 adjusted R² of the full quadratics, fragments' Version 1.0 conditions; E11; E12 Box-Cox on −10..10 (−5.46 to 1.99); E13 medians marked in Table 5.9; E14 Table 7.3 and 8.1 formats; E15; E16 Cpk minimum 1.0; E17 "repeating the judgement".
- D pressure class argued on A-Mab p. 157 ("easy to control and minimal impact on LRF...") and the claim scope; no effect detected; class unchanged.
- Also: residual SD for every model (Table 5.5), residual plots of XMuLV, fragments, step yield (Figures C.1-C.3, PCP-009 §5.5), step yield over the design space (PCP-009 §7), no instrumented system named (calibration, PCP-009 §9), PCP-009 §5.5 half-range effects vs PCMP-001 §6.2 stated.
- Gate: fix-pass runs 1 FAIL (font floor p.25 adequacy table 7.8 pt, p.33 criteria table notes 7.8 pt), runs 2-6 OK; explicit pdf+docx renders; final check_render OK. 57 pp; 592 sentences, 11,814 words of prose. No <<NEEDS:>>.
- Hand-back (neither register): PCP-009 §5.5 effects over half the range (report gives both); studentized residuals and leverage not named in PD-009-07; calibration statement (no system named; PCP-009 §11 says the same); order of analysis (screening analysed before RSM committed) not checkable. Builders: criteria_results still 13 % too wide here (fixed on the instance); discrepancy_register rows one per page in the PDF; dev_register "run retained" singular where Version 1.0 recorded several runs (DEV-009-02); anova_lof_df Model SS −6.9e-18 for a no-term model; cap_for Mean ± SD mixed decimals; par_table "≤ 2" format.

## Data-state pass 2026-10-11 (after commit 51fa592, data-state-2026-10-11.md)
- Setup chunk passed; gate on the new data passed (exit 0). The rendered text is identical to that of the fix pass:
  no value in PCR-009 depends on a moved criterion (its criteria, MVM and XMuLV 4.62 log10 and fragments 2.00 %, are
  unchanged; no verification row for this step; cumulative claims unchanged).
- Searched for verification statements, tightened/widened counts, the cation exchange aggregate criterion, NOR
  narrowing: none in the text. "No criterion of an earlier step rests on a platform worst case of this step" still
  holds (the new UF/DF row concerns aggregate, not measured here). No edit.
- check_render once more: pass (exit 0). 57 pp; 592 sentences, 11,814 words of prose. DRAFT.txt refreshed (unchanged).

## Final pass (readability review, 2026-10-11, same author, Claude Opus 5.5)
Inputs: feedback-PCR-009.final.md, content-review-PCR-009.md, data-state-2026-10-11.md, REPORT-LESSONS §5-§7.
- Q1 causes: §2.1 (platform "gives the expected direction"; claim most at risk at the maximum load; pressure raises
  flux although compaction raises the layer's resistance; PCP-009 §4.3 interaction quoted as the plan's reasoning),
  §2.3 (fouling shifts flow to the larger pores), §5.4 (LRF lowest at the highest volume), §11 (mechanism and
  direction in the first sentence).
- Q2 terms: least favourable NOR combination, NOR-propagated PAR, limit on overfitting, criterion on residuals and
  influential runs defined at first use (executive summary); "intercept-only model" throughout (text, table notes,
  figure captions); "the LRF claimed for this step"; "the CQA register"; Version 1.0 conditions named; "Statistic that
  decides the verdict"; near-equivalent models given as "within 2 AICc units"; "Spread" column renamed "Absolute
  residuals".
- Q3/Q6: filing glosses removed (§1.4, §5.3 x3, §6, §9, §11, §7 lower-edge sentence); Version 1.0 post-use claim now
  once in the body (§3.1, plus the register table); "step yield has no criterion" removed from §2.2, §5.3, §10, PD-009-03,
  PD-009-05; PD-009 paragraphs rewritten to give the effect of each entry, not its plan/done; PD-009-01 now says what
  was compared (criteria from the verification with the full quadratics vs the criteria in force) and what stayed the same.
- Q4: cumulative requirements cited to PCMP-001 §3 and A-Mab Table 4.38 p. 165 (platform totals), XMuLV check p. 166;
  fragments, A-Mab pp. 30 and 56 give no limit, sponsor set 2.00 %.
- Q5: integrity tests (§10, §11, PD-009-04); pressure cause; step yield expectation from mechanism and compared with
  the data (§5.4); screening fit statistics (4 parameters, 5 points); Table 13.1 narrative (every run retained, as
  Version 1.0 recorded); detection argument on the residual SD of the model (0.23) and the standard errors of the
  expected terms; MVM limit labelled "lower end of the two-sided 95 % interval, a one-sided 97.5 % limit"; Table 5.1
  SDs recomputed from unrounded data, correct (0.18, 0.77, 0.84), unchanged; DEV-009-01 judged against the run's set
  pressure (8 or 19 psi, or 13 psi in qualification), heading shortened.
- Q7: criteria named in the executive summary, §5.3, Tables 5.5 and 5.6 (headers and captions), Conclusion 3;
  run 5 described (executive summary, §6, Conclusions 3 and 7); run 7 described (§6); PD-009-07 analyses named in the
  executive summary; Conclusion 1 states what PCP-009 §7 requires; abstract subjects rewritten (§1.4, §5.3, §6, §11, §13.1).
- New setup assertions: pressure levels and the overshoot reasoning, the expected terms not significant, run 7, the
  screening design points and model size, the worst-corner side, the step yield next model by AICc.
- Gate: check_render --render, 3 runs, all exit 0 (advisory numeral lint only). 57 pp; 596 sentences, 11,845 words.
  Tables 5.5 and 5.6 checked on the page image. DRAFT.txt refreshed.
- Left: Table 13.1 "run retained" (builder, sweep list); the PD-009-03 reason in the config still reads "the results
  were not entered in the qualification record" (not "the record gives no reason"); not restated in the text.
