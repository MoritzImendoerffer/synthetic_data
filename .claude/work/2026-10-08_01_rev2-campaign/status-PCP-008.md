# Status — PCP-008 (Anion Exchange Chromatography) Version 2.0 draft

Author: Opus 5.5 (claude-opus-5-5), same author for run 1 and this revision, in
`pc_package/PCP-008_aex.DRAFT.qmd`. Run-1 draft kept at the session scratchpad
(`pcp008/PCP-008_aex.DRAFT.run1.qmd`).

## Final pass after review run 2 (2026-10-10, late afternoon) — DONE
Inputs: feedback-PCP-008.final.md (fix these and nothing else), content-review-PCP-008.run2.md.
Run-2 draft kept at the scratchpad (`pcp008/PCP-008_aex.DRAFT.run2.qmd`).
- Version 1.0 text kept or restored word for word: coding statement (D-001), §13 sentences,
  NORs set from the second analysis, "does not vary the quality of its load", protein load "well
  above the set-point", the pooling sentence ("blur", restored), the quadratic-terms sentence
  (restored, dropped from change 10), the release profile, the complexed fragments sentence
  (restored), the flow-rate assignment reason in §4.3 (restored).
- §7 intro: "well inside" and "high risk" added to the list of rules without a threshold.
- A1 §13: one added sentence (INV-001 CA2 amendment, issued after the runs, approved on 2026-09-30).
- A2 §7 item 3: "used for prediction only if ... four conditions" and the descriptive-report
  sentence removed; adequacy definition kept; added once that PCMP-001 §7.5 asks only the first three
  conditions of the model behind a widening bound.
- A3 change 6 and objective 6: only the HCP worst case is verified on a model; leached Protein A
  stands under §7.5; §11 deliverable wording to match.
- A4 capability: two-sided wording removed (one-sided Cpk; between the values PCMR-001 names the
  driving parameters).
- A5 change 3 and §7 item 1: Version 1.0 described as a test for a difference.
- A6 change 9: "no class for a critical parameter that is not well controlled".
- A7 objective 1: Version 1.0 words + fragments for the multivariate parameters only.
- A8 objective 2: quality attributes on the single-batch limit, viral clearance on the mean.
- A9 §7 item 7: model of pool HCP; clearance factor = nominal load HCP over predicted pool.
- A10 virus particles only (DNA dropped) in §4.1 and §6.4; residence-time sentences said once
  (§5.1 shortened).
- A11 §4.1 interaction: the salt of the solution in contact with the bed while the protein binds.
- A12 execution record: windows in the past tense; overlap and spiked-run sentences cut; equipment
  sentence as PCP-009; Table 11.1 note a) reduced; §8 "basis column of Table 8.1 shows each criterion
  at its a priori value" (asserted iac == a priori).
- B: yield cause named (ligand repels the positively charged antibody); compiled criteria said once
  (criteria paragraph refers to change 7); offset timing once (§5.1); INV-002 corrective actions named
  (model selection and refits); condition-4 tests named in change 5; NOR-propagated distribution
  named in the capability paragraph; old rules named after "This replaces". Table 8.1 rounding note is
  the builder's: left. No statistical "governs"/"acts on" outside Version 1.0 sentences.
Gate: check_render --render green on the first final-pass run and after the explicit renders (2 runs);
PDF 38 pp; 391 sentences / 9,187 words of prose; no <<NEEDS:>>; D-001 and the coding statement
verbatim in PDF and DOCX; Table 11.1 page inspected; PCP-008_aex.DRAFT.txt refreshed.

## Revision after review run 1 and the factual check (2026-10-10, afternoon) — DONE
Inputs: feedback-plans-shared-2026-10-10.md, feedback-PCP-008.run1.md, factual-PCP-008.md,
content-review-PCP-008.md, data-state-2026-10-10.md, PLAN-LESSONS (rules 4, 8, 10), re-rendered PCMP-001
§6–§7 (content only), frozen Version 1.0 PCP-008 (flowing text, for word-for-word restoration), brief
§5c (regenerated 10:51, D-001 unchanged).

Approach: Version 1.0 design, sampling, spiking and decision text restored word for word in §5–§13 and
the appendices (numbers as inline expressions, § and Table references as cross-references that render
the same numbers: Table 3.2, 5.1, 6.1, 6.2). Each rule in §7 is tagged "(Version 1.0)" or "(PCMP-001
Version 2.0)". Where PCMP-001 V2 replaces a V1.0 rule, the V2 rule is stated and the V1.0 consequence
is named in "Changes in this revision". Scientifically wrong descriptive sentences corrected and listed
together as change 10.

Resolved, by item:
- A4 / most important: V1.0 coding statement restored word for word in §5.5 and Appendix A; change 9
  and every sentence on the centre of the protein load range deleted (no design centre, midpoint or
  coded zero described). D-001 sentence (V1.0 §8 text) verbatim in PDF and DOCX.
- S1 widening rule names the three tests + exact fit + fourth condition examined by PCR-008 (§7 item 7).
- S2 change 7 names the title-block date and the criteria added at compilation (INV-001 root cause 1);
  criteria paragraph says the V1.0 limits were written into the compiled text, not approved.
- S3 residual tests: |residuals| on predicted, residuals on run order at THRESHOLDS residual_alpha;
  Cook's distance against THRESHOLDS cook_factor/n (§5.5, computed).
- S4 V1.0 classification text kept word for word + PCMP-001 §6.2/§7.7 rules (§7 item 6, change 9).
- S5 single-batch design-space statistic (§7 item 5, change 2, objective 2).
- S6 PCMP-001 remedy word for word (§7 item 3); V1.0 consequence named (change 5); no CA2 rule stated.
- S7 NOR-propagated draw as PCMP-001 §6.4 (§8), stated once; ±3 SD asserted (every set-point is
  its NOR midpoint).
- S8 V1.0 text restored; corrections listed as change 10; V1.0 rules marked.
- S9 executed-methods table dropped; execution record limited to the PA3 windows (past tense) and
  "the record names no instrumented system"; hold sentence dropped from risks.
- S10 INV-002 said once (what it investigated; corrective actions applied by PCR-008).
- A3 change 4 wording; A6 all six low-priority items (offset requirement without asserting which
  offsets were recorded; EQ-CHR-118 V1.0 sentence + identification table, no future-tense due date;
  which limits PCMP-001 sets; aggregate reason from PCMP-001 Table 7.1; monitored DNA/leached PA in §1;
  capability move to the integrated process model in change 8).
- B items: offsets "unknown, not zero" everywhere; spiked-run studies named (S-AEX-SUP/SCR/RSM/UNI,
  computed); criticality convention deleted; step contributes claims (5.5 of 16.7; 4 of 8.6);
  science (mass transfer vs equilibrium, large species, pH x conductivity interaction, spike adds
  medium/protein/salt, load risk = yield, load competition direction, PPQ inside NOR); §13 V1.0 text
  unchanged; leached PA attributed to PCMP-001 §7.5; seed once (computed); terms; restatements and
  padding cut; codes named; Table 4.1 headers, Table 3.2 sorted, Table 11.1 study type and note.

Flags left, with reasons:
- "release profile" of the CEX pool kept in §5.3 and §7 item 2: Version 1.0 sampling/decision text the
  fix list says to keep word for word; §7 says once that Version 1.0 set no numerical limits.
- Flow-rate assignment reason (fast binding) vs the stated rule (low interaction): V1.0 text kept; no
  RA-001 rationale added that cannot be verified.
- Load qualification before or after pH/conductivity adjustment: V1.0 text; no rule added.
- Cpk and out-of-specification probability for viral clearance: PCMP-001 §7.9 scope kept
  (capability.csv carries viral rows); for the PCMP-001 owner.
- Table 6.1 unit "pH" for pH: as config and PCMP-001 Table 4.2.
- Builder tables 1.1 and 8.1: left for the consistency sweep.
- The brief's T.methods_by_study(["aex"]) is no longer carried (execution record); the annex builder
  should not expect it.
- For PCR-008 (record vs Version 1.0 rules kept): univariate both ends in duplicate + one spiked run,
  no centre run; bed pressure not measured; DNA and leached PA below LOQ at both scales; no
  instrumented system recorded for S-AEX studies (V1.0 named EQ-CHR-118); MVM governing parameter
  (factual check).
- Environment: `uv run` tried to re-resolve en-core-web-sm over the network and failed to start
  once; the last gate runs used `.venv/bin/python` directly.

Gate: check_render --render green on the first revision run and on every run after it (5 runs);
numeral lint (advisory) flags only identifiers, version/section/list numbers and "Table 7.1 of
PCMP-001". PDF 38 pp, no missing glyphs, all cross-references resolved, 8 complex tables complete,
no text below 7.9 pt. 394 sentences / 9,088 words of prose (check_render). No <<NEEDS:>>.
`PCP-008_aex.DRAFT.txt` refreshed (pdftotext -layout). Changed tables inspected as PNG: 3.2, 4.1, 5.1,
6.1, 6.2, 11.1, A.1, B.1.

## Run 1 (2026-10-10, morning) — superseded by the revision above
Two check_render passes (matrix legend note wrapped; moved to caption), 37 pp.
