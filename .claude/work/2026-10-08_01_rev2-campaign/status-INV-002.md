# Status: INV-002 final fix pass (run 3)

Author: Claude Opus 5.5 (claude-opus-5-5), 2026-10-09. Took over the draft as it stood.
Backup of the run-2 draft: `INV-002_model_adequacy.DRAFT.pre-run3.qmd` (this folder).

Inputs read, in order: data-state-2026-10-09b.md, feedback-INV-002.run2.md, content-review-INV-002.run2.md,
the draft; then the brief, section_plan, STORY_BIBLE §9b, WRITING_GUIDE, REGISTER_EXEMPLAR, rendered
PCMP-001 and INV-001 (content only).

## Facts established from the data (2026-10-09, after the data change)

- Selected models: 18 of 22 adequate. No adequate model: VI acidic variants (exact fit, no Box-Cox
  interval), VI fragments, CEX fragments, VF XMuLV.
- Full quadratic on planned runs: 14 fail the overfitting limit; 7 meet all three tests; 1 (VI acidic
  variants) is an exact fit that `model_adequacy.csv` and `adequacy.adequacy()` still mark adequate=True
  (p_lof NaN, gap 0). The document now calls it "not testable: exact fit".
- `iac_verification_full.csv` also treats that exact full quadratic as adequate, so `iac_full.csv`
  widens the bioreactor acidic-variant upper limit to 39.6 while `iac.csv` keeps 39 (a priori). So 5
  criteria differ between the two verifications: 4 wider under model selection, 1 kept at a priori.
  In force, 3 criteria are widened against a priori (`iac.csv` widened). The fix list's "now three, not
  four" matches the in-force count, not the comparison with the full-quadratic verification (still 4).
- Full quadratic + block on all runs (what the augmentations were sized for): acidic variants met
  (gap 0.116), AEX HCP met (0.108), high mannose NOT met (gap 0.247).
- VI aggregate selected model: hold_time + temperature only (no pH). NOR in force ends at 120 min and
  23 C as characterized; the one-sided 95 % bound over both grids is equal (computed).
- p_oos: 0 of 2000 for hcp and aggregates; 1 - 0.05**(1/2000) = 0.15 %.
- Repeated corners (C.7): HM p = 0.565, aggregates p = 0.054 (borderline), AV 0.631, AEX HCP 0.578.
- Binomial (effectiveness check): 16 new runs need >= 14 inside; 12 need >= 10. HM 13/16 and AGG 11/16 fail.
- `T.model_adequacy(failing_only=False)` prints "nan" for the exact fit's lack-of-fit p and has no
  verdict column, so Table 3.1 is rebuilt with T.frame/CTable (all 22 models, verdict).

## Progress

- [x] Read everything; explored data (scratchpad scripts)
- [x] Rewrite setup chunk and prose (A-F), 20:27. Setup chunk runs with every assert true.
- [x] Gate pass 1: renders OK, style OK; FAIL only on Table 8.4 repeating its step cell (merge added).
      Pending edits below now APPLIED; gate pass 2 running.
- (old note) Gate pass 1 running (20:28). Pending edits after it: typed parameter names ("culture pH",
      "hold time", "protein load", "temperature") -> pname(); LOF-power note on the model of the
      mean (8.1); name rule 2 in Section 5; Summary "against them" -> name the criteria; closure
      "4 of them" -> name; 9.1 opening: full single-batch term before first "single-batch bound".
- [x] Gate pass 2: FAIL font floor (Table 8.3 "Block p" header too wide) -> header shortened.
- [x] Gate pass 3: every hard gate OK (numeral lint advisory only). PDF 54 pages.
- [x] PDF table check: 2.1, 3.1, 6.1, 8.1-8.4, 9.1-9.3 read correctly. DONE; report sent.

## Table numbering after the rewrite

3.1 full quadratic verdicts (all 22, rebuilt, label tbl-model-adequacy); 8.1 selected-model verdicts
(new, landscape, tbl-selected); 8.2 sharpen; 8.3 aug check; 8.4 measured; 9.1 impact; 9.2 criteria
(5 rows); 9.3 sensitivity (5 rows).

## Notes for a successor

- If stopped mid-rewrite, restore from the backup above and re-apply; the plan is in this file.
