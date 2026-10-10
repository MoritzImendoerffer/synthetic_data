# Status — PCR-006 (Low-pH Viral Inactivation) Version 2.0, authoring run

Author: Claude Opus 5.5 (claude-opus-5-5), one-pass, per authoring/RUNNER.md.
Draft: pc_package/PCR-006_viral_inactivation.DRAFT.qmd
Scratch: /tmp/claude-1000/-home-moritz-github-repos-synthetic-data/be14bf3c-e46a-46fd-b419-65482c2add0e/scratchpad/pcr006/

## Inputs read (2026-10-10)
- [x] authoring/RUNNER.md
- [x] authoring/out/PCR-006.brief.md
- [x] authoring/section_plan.yaml (report_doe)
- [x] authoring/STORY_BIBLE.md (§9b)
- [x] authoring/WRITING_GUIDE.md
- [x] authoring/REGISTER_EXEMPLAR.md
- [x] procedures/REPORT-LESSONS.md
- [x] data-state-2026-10-09b.md, data-state-2026-10-10.md
- [x] rendered PCP-006 (pdftotext, scratch PCP-006.txt)
- [x] rendered PCMP-001 (pdftotext, scratch PCMP-001.txt)
- [x] helper signatures (_pcpkg, doe_report, tables, ctable); adequacy.* signatures via inspect only

## Decisions
- Selected models: aggregate (hold time, temperature) and XMuLV (pH, hold time, temperature) meet §7.2 criteria 1-3, FAIL criterion 4 (Cook's: agg runs 3,7,8; XMuLV runs 4,5) -> influence analysis (PD-006-07) computed doc-locally with adequacy.select_model on 17 runs: no conclusion changes (incl. the aggregate verification bound 0.55 < 0.70 and XMuLV failure at characterized NOR).
- Acidic variants: exact fit -> no adequate model, judged on measured results. Fragments: fails overfitting limit (gap 0.33) -> measured results.
- Near-equivalent models (dAICc<=2) computed; no conclusion changes. Fragments: hold-time-only model within 2 AICc meets criteria 1-3 (sensitivity only; selected model decides).
- D-001: describe first PAR analysis without saying where others were held; no "around the set-point".
- No fig_rsm_contours (would show a predicted surface for acidic variants, which has no adequate model): own XMuLV contour figure from D.predict at 19 and 20 °C.
- PAR margins computed from the printed (inward-rounded) PAR edges.
- Fragments/XMuLV never stated 'at manufacturing scale' (no offset).


## Progress
- [x] setup chunk with computed scalars and assertions
- [x] body sections written (all, one pass; assembled 2026-10-10)
- [ ] check_render passes (run 1: inline KeyError; run 2: all hard checks OK except unresolved @tbl-par-margins, fixed; self-review fixes for claims beyond the record applied; run 3 pending)
- [x] pdf + docx render (explicit quarto renders OK; PDF 74 pp)
- [x] visual check of complex tables / figures (all pages with a complex table or figure viewed once; fixes applied and re-checked)

## Hand-back items (departures in neither register, NOR changes, helper issues)
- PCP-006 Table 5.3 input-pool samples (aggregate, acidic, A-Mab conc.) on every design run: record holds none (no load columns in doe_viral_inactivation_*.csv). Not in either register.
- Widening of the bioreactor aggregate criterion: made on criteria 1-3 (CLAUDE.md, PCMP-001 §7.5 as applied); PCP-006 §7.4 rule 2 refers to all of its §7.1 (four criteria); aggregate model fails criterion 4. Report states it in §verification and shows the bound holds with each flagged run deleted; not in either register (PD-006-07 Planned text names ranges and design space only).
- T.worst_case_verification labels fragments and acidic rows 'Confirmed' on models failing §7.2 (REPORT-LESSONS §1 rule 6).
- T.criteria_results note c says 'at manufacturing scale' also for fragments (no offset measured).
- D.fig_par legend '95% predictive' for the XMuLV (worst-case) band, which is the range of mean predictions over NOR combinations (to verify in render).
- model_adequacy.csv marks the exact-fit acidic full quadratic 'adequate: True'.
- D.ofat_analysis / D.vi_worst_case_summary judge scale-down results against criteria without the offset (verdict unchanged; report states mfg-scale check).


## Self-review fixes after run 2 (2026-10-10)
- Restored margins table + 2 paragraphs lost in an earlier replace; minus sign as one expression.
- Removed claims the record does not hold: cause of screening/RSM pH-effect difference; executed spiking/operation details (now the plan's procedure, present tense); input-pool sampling (record holds none -> stated in sampling plan); DEV-006-01/02 embellishments; in-process controls; jacket/control-system details; A-Mab case-study comparison for pH class; harvest in-process test in the verification risk paragraph; 'additive because no interaction entered'; icIEF-resolution explanation of the zero scatter (record gives no reason; OFAT repeatability 0.41 points).
- Counts typed as words now computed (W()) and asserted; no sentence opens on an inline number.
- Run 3: all hard checks OK except table-fit false positive on tbl-vi-ofat-effects (note "Holm's" rendered with typographic apostrophe; table complete on its landscape page, checked visually p.45).
- Visual pass over every complex table/figure of run 3: rebuilt flat tables (params, screening fit, coefficients, ANOVA, capability) as T.frame; p-values formatted; Tables 7.5/7.6 headers broken; App C limited to modelled responses; prose precision aligned with tables; residual/run-order + Cook's figure added (PCP-006 §5.5); verification wording (a failing model confirms nothing).

## Final state (2026-10-10)
- check_render: 5 runs. Run 1 inline KeyError; run 2 unresolved @tbl-par-margins; runs 3-5 every hard check OK
  (chunks, 0 <<NEEDS>>, tic gate, docx, pdf, glyphs, cross-refs) except the table-fit false positive on
  tbl-vi-ofat-effects (straight vs typographic apostrophe in "Holm's"; table complete, p.45). Exit code 1 for that reason only.
- Body: 768 sentences, 16,577 words (check_render). PDF 74 pages. No <<NEEDS:>>.
- Not committed (coordinator: do not commit). Draft only: pc_package/PCR-006_viral_inactivation.DRAFT.{qmd,pdf,docx}.
- Annex (build_ground_truth) not started: separate step per RUNNER.

## Revision pass 1 (after content review + factual check), started 2026-10-10 afternoon
Inputs read: feedback-PCR-006.run1.md, factual-PCR-006.md, content-review-PCR-006.md, REPORT-LESSONS.md (unchanged),
brief regenerated (DEV-006-04; PD-006-03 relabelled, reason fixed), rendered PCP-006 of 16:32 (§7.4 rule 2: first
three criteria, fourth does not decide, PCR-006 states whether the bound depends on a single run; new §7.6
operating-region decision criteria and objectives-met conditions).

## Revision pass 1: done (2026-10-10, late)
- Owner's Cook's decision folded in: both modelled outputs meet criterion 4 (4/n flags, F median decides);
  flagged runs examined as PCP-006 §7.1 requires (not a discrepancy); PD-006-07 withdrawn (6 discrepancies);
  widening rests on a model meeting all four criteria; run-5 dependence of the XMuLV PARs and temperature effect stated.
- DEV-006-04 recorded (§3.4 sampling, §4.3, §7.7 verification, deviations subsection); four deviations.
- NOR decisions: three stages with engine-replica margins (0.04 / 0.04 / 0.11); intermediate stage values derived
  from structured values (characterized set-point, NOR high), 105 min asserted against the S-VI-OFAT hold times.
- Factual items 1-17 + minor and content-review items resolved (see report); font floor fixed (Tables 5.10, 7.4, 7.12, D.1).
- Gate (check_render --render, venv on PATH): exit 0, all checks OK. Explicit pdf + docx renders OK. PDF 77 pp.
  849 sentences, 18,576 words. No <<NEEDS:>>. Page images of every changed table/figure read.
- Text extract refreshed: PCR-006_viral_inactivation.DRAFT.txt. Not committed.
