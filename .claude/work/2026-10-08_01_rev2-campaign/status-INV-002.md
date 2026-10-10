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

## Final pass (2026-10-10)

Author: Claude Opus 5.5 (claude-opus-5-5). Fix list: `feedback-INV-002.final.md` (items 0-7).
Backup of the draft before this pass: `INV-002_model_adequacy.DRAFT.pre-final.qmd` (this folder).
Scratch: `/tmp/claude-1000/-home-moritz-github-repos-synthetic-data/be14bf3c-e46a-46fd-b419-65482c2add0e/scratchpad/inv002/`.

- [x] 09:05 read fix list, factual check, status, draft; backup made.
- [x] 09:30 facts established (scratch s1.py, s2.py):
  - config record now reads PA1 "probability of success", eff. check "the sample-size calculation of
    preventive action PA1", assurance_basis "an attribute with a criterion" -> drop the 3 substitutions.
  - PCMP-001 §7.2 (rendered): criteria 1 F-test, 2 LOF, 3 gap <= 0.20, 4 "The residuals show no pattern
    against predicted values or run order, and no single run dominates the fit." §6.4/§6.5 say "its NOR"
    (no "in force"); nothing in doe_report/tables/brief says which NOR p_oos draws from -> drop "in force".
  - Only setting correction in the campaign: Protein A RSM run 23, elution_ph 3.38 (DEV-005-01), PD-005-03.
    Full quadratic pool HCP: design pH plof 0.058 gap 0.057 (adequate); recorded pH plof 0.0240 gap 0.085
    (fails LOF only). Other Protein A verdicts unchanged. FQ (D.fit planned/full) = recorded pH;
    planned_full_models() and model_adequacy.csv = design pH. PD-005-02 = "Conclusions resting on an
    influence analysis".
  - AICc (code) = n ln(SSE/n) + n(1+ln 2pi) + 2p + 2k(k+1)/(n-k-1), k=p+1. Protein A HCP: fit -69.2/-53.4,
    pen 30/12, corr 49.5/5.6, AICc 10.3/-35.8 (= code). Differences unchanged (15.8, 61.9, 46.1).
    Chosen: define AICc as the code computes it (option A of fix item 5).
  - Table 9.2 swap cause: crit_body built by T.frame WITHOUT notes, which relabels the body markers
    (b->a, a->b); the old-lettered notes were then attached. Fix: pass notes to T.frame, take .body and
    .notes from it, assert each marker sits in its own row/column.
  - Worked corner (8.2) = NOR in force (load 39; characterized 40).
  - V1.0 (rev1 PDFs): PCMP-001 accepted a model on significant terms, no significant LOF, predicted R2
    consistent with adjusted R2, thresholds per study; PCP-003 "No numeric threshold"; PCR-003 Table 5.8 LOF.
- [x] 10:05 all edits applied (setup chunk: item 0 substitutions removed, run-23 block + asserts, AICc parts on
      the code's definition, Table 9.2 built once as crit_tbl with notes through T.frame + marker asserts,
      CAPA/eff. record verbatim, SOP title, NOR-in-force assert; notes of Tables 2.1, 3.1, 8.1, 8.2, 9.1, 9.2;
      prose: Summary, §1, §3 (four criteria listed once + "adequate" defined + PD-005-02 + recorded-pH para),
      §5, §6.1, §7.1, §8.1, §8.2, §8.3, §8.4, §8.5.1, §9, §9.1, §9.3, §10, §11, §12).
- [x] 10:20 gate pass 1: every hard gate OK (numeral lint advisory only, as before); PDF 55 pp. Read the
      rendered text of every changed passage: Table 9.2 marks now right (a = acidic variants selected,
      b = AEX HCP full quadratic). Small follow-ups applied: rule-11 antecedents ("With Protein A run 23",
      "pool host cell protein" in 8.2, "None of the 2,000 batches that the integrated process model
      simulated", "the failing full quadratic model of pool host cell protein"), Table 2.1 note "fails at
      least one of the three tests".
- [x] 10:35 gate pass 2 green; explicit pdf + docx renders; check_render (no --render) green.
- [x] page images read (final PDF): Tables 2.1 (p10), 3.1 (p14), 8.1 (p39, landscape, note fits), 8.2 (p41),
      9.1 (p46), 9.2 (p48: a) on acidic-variant selected 1.00 -> exact-fit note; b) on both AEX HCP full
      quadratic 4.00 -> overfitting note), 10.1 (p52, PA1 verbatim). DOCX twin of 9.2 checked: same marks.
- [x] 10:45 last prose edit ("in @tbl-model-adequacy" on the "7 meet all three tests" sentence); gate pass 3
      green (re-run once only to read the head of the output); explicit pdf + docx renders; check_render green;
      Table 9.2 page re-read. PDF 55 pp. No <<NEEDS:>>. DONE.

### Notes for the coordinator (shared modules, not edited)
- tables.py `sample_size()` caption: "Probability of success that the planned model meets the model-adequacy
  criteria" and `adequacy_remedy()` note "...meets PCMP-001 §7.2": the probability covers criteria 2 and 3
  only (lack of fit, overfitting). Each table's own note says so, but the caption/note text overstates.
  doe_report `fig_assurance` docstring likewise (not rendered).
- Which NOR the integrated model (p_oos) draws from is not stated in doe_report, tables or the brief; the
  text now attributes the draw to PCMP-001 §6.4/§6.5 ("its NOR"), without "in force".
