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

## Final pass (after content review run 2, owner's "no deviations" decision), 2026-10-10 evening
Inputs read: feedback-PCR-006.final.md, content-review-PCR-006.run2.md, REPORT-LESSONS.md §1, §3, §6, §7.
Brief regenerated (`authoring/build_brief.py PCR-006`): dev_register now Event/Summary/Detected during/Outcome with
DEV-006-01/02 only; PD-006-07 (clearance not measured in the concentration study) and PD-006-08 (input pool not
tested) added; `dev_006_03_*` scalars gone; PD-006-03 carries the risk grounds; PD-006-05 records that the
hold-judging approach was chosen after the results.

What changed in the draft
- The record (§13) is now "Study events and discrepancies from the plan": one opening sentence on how departures are
  recorded, study events first (DEV-006-01/02, both runs retained in the analysis), then the eight discrepancies,
  with new subsections for PD-006-07 (what S-VI-UNI2 showed and what four runs cannot exclude) and PD-006-08.
  No "deviation" in the report's own voice except the sentence that says what PCP-006 calls a departure.
  Setup assertions updated (2 events, PD-006-01..08, PD_CONC/PD_POOL); `dev4`/`n_dev_ret` removed.
- Errors (fix list C): first-order kinetics does not explain the plane (§5.4, bounded by the plan's full quadratic,
  agrees with §2.1/§2.3); the temperature effect on aggregate holds in every model after a deletion (0.204-0.226 pts,
  computed, F3/§5.3.2/§9/§11); acidic variants per hold time now include the concentration study at 90 min;
  the fragment rise is 1.6 times the method repeatability, not "small against the scatter"; S-VI-UNI2 measured no
  fragments (§3.3); Table 7.4 holds the XMuLV rows only, criterion "≥ 6.60", the rest in one sentence; decision 2
  left the pH edge at 3.54; the acidic variant rise depends on hold time alone and acid hydrolysis does not explain it;
  the cumulative XMuLV requirement (16.7) separated from the step claim (6.60) in the summary; both NOR-to-PAR margins
  per factor (0.11/16/2.8 and 0.10/60/2.0); the widening reflects the shorter NOR alone (0.84 at the platform hold).
- Criteria and judgements (D): the pH-control comparison (0.10 pH units) named as the judgement behind the CPP class
  and behind rejecting a 0.04 margin and accepting 0.11; the hold-time margin against the 4-min record difference;
  the acidic-variant difference reported as significant with its size (0.38 pts of a 22.0-pt criterion) and the
  "small" verdict named a judgement; the fragment acceptance cites PD-006-03 and gives the grounds once (§7.5.3);
  §10 item 3 now states the fragment rule that was not met.
- Terms and repeats (E, Q1-Q7): clearance factor / log reduction value for "fold"; S-VI-OFAT by its study id;
  "the process model at set-point, 1.55 % HMW" for "the nominal load of the step model"; LRF as the difference of
  log10 virus loads (§3.1, §5.1, Appendix D); filing sentences and register tags removed; the reason the claim is
  judged on the mean given once (§3.5); the mechanism of the hold given once (§2.3) and referred to afterwards.
- Tables and figures (F): Table 5.9 now reports all four adequacy criteria per near-equivalent model (doc-local
  `crit4`, asserted equal to the engine for each selected model); one aggregate and one fragment near model fail the
  fourth criterion, stated in the text; Table 7.2 keeps the builder's new single-run limits column, its group header
  wrapped doc-locally and the columns given widths so it stays above the font floor; Figure 7.1/7.2 captions describe
  both panels and name the legend labels; Appendix A tables are numbered A.1 (`appendix_numbering("A")` before the
  heading); Table 4.1 note names the table of set-points and ranges instead of "the table of the decisions".
- D-001 untouched: Table 7.4 keeps the engine's "PAR (set-point)" column and values, the fig_par left panels stand,
  and no sentence says where the other factors were held.

Gate and renders
- check_render --render: 7 runs this pass (font floor on Table 7.2 after the builder change, then clean).
  Final run exit 0: chunks exec, 775 inline expressions eval, no <<NEEDS:>>, tic gate OK, docx OK, pdf OK, no missing
  glyphs, every cross-reference resolved, 24 complex tables complete, no page-foot overrun, no repeated index cell,
  no text below 7.9 pt. Numeral lint advisory only.
- PDF 81 pages. Body 887 sentences, 19,579 words. Page images read for Tables 5.9, 7.2, 7.4, 7.5, 13.1 and Figures
  7.1/7.2. Text extract refreshed (3,374 lines). Not committed.

Hand-back for the coordinator
- `discrepancy_register` PD-006-06 reason still cites "(DEV-006-03)", a retired identifier; it should read PD-006-07.
- `T.criteria_results`: footnote b) (manufacturing scale, offset) hangs on the group header and on the limits header,
  which also cover the XMuLV row, and XMuLV has no measured offset. The long group header is one unwrapped
  \multicolumn line, which shrinks the whole table; this document wraps it doc-locally.
- `T.ofat_effects` (Table 7.8) is 11 columns with a two-level header and six footnotes, and `T.cex_verification_n`
  (Table 7.9) nests runs 1-5 inside each attribute with "Runs needed" on the first row only. Both are builders.
- `T.criteria_change` does print the Version 1.0 rule codes, but with footnotes R1 and R3 that explain them.
- Note: the criteria table is built as `_cr = T.criteria_results(...)` plus a doc-local width fix, so the builder
  call is repeated in a comment above it to keep the table-fit check covering it (25 complex tables checked).
