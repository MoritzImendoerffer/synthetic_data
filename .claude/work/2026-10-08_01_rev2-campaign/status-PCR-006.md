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
- [ ] check_render passes
- [ ] pdf + docx render
- [ ] visual check of complex tables / figures

## Hand-back items (departures in neither register, NOR changes, helper issues)
- PCP-006 Table 5.3 input-pool samples (aggregate, acidic, A-Mab conc.) on every design run: record holds none (no load columns in doe_viral_inactivation_*.csv). Not in either register.
- Widening of the bioreactor aggregate criterion: made on criteria 1-3 (CLAUDE.md, PCMP-001 §7.5 as applied); PCP-006 §7.4 rule 2 refers to all of its §7.1 (four criteria); aggregate model fails criterion 4. Report states it in §verification and shows the bound holds with each flagged run deleted; not in either register (PD-006-07 Planned text names ranges and design space only).
- T.worst_case_verification labels fragments and acidic rows 'Confirmed' on models failing §7.2 (REPORT-LESSONS §1 rule 6).
- T.criteria_results note c says 'at manufacturing scale' also for fragments (no offset measured).
- D.fig_par legend '95% predictive' for the XMuLV (worst-case) band, which is the range of mean predictions over NOR combinations (to verify in render).
- model_adequacy.csv marks the exact-fit acidic full quadratic 'adequate: True'.
- D.ofat_analysis / D.vi_worst_case_summary judge scale-down results against criteria without the offset (verdict unchanged; report states mfg-scale check).

