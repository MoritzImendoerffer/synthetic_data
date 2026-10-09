# Status: PCP-006 final fix pass (2026-10-09)

- **Author:** Claude Opus 5.5 (`claude-opus-5-5`), taking over the draft as it stands.
- **Draft:** `pc_package/PCP-006_viral_inactivation.DRAFT.qmd`
- **Fix list:** `feedback-PCP-006.final.md` (A1–A4, B1–B11, C). Governing note: `data-state-2026-10-09b.md` §5.
- **Gate:** `PATH="$PWD/.venv/bin:$PATH" uv run python authoring/check_render.py pc_package/PCP-006_viral_inactivation.DRAFT.qmd --render`

## Progress

- [x] Read inputs (data-state, fix list, factual, review run 2, draft, brief, section plan, bible §9b, guide, exemplar, lessons, rendered PCMP-001 §7)
- [x] A1 hold study removed: §6.5 and §7.5 sections deleted, Table 5.3 and Table 11.1 rows gone,
      change 5 of §1.1 gone, objective 6 gone, roles/risks/methods/stats mentions gone, the
      `hold_viral_inactivation.csv` read and its assertions removed. `_plan_kinds` no longer has
      "hold", and the study set is now computed (see below).
- [x] A2 concentration study restored to the Version 1.0 design (settings across the range studied,
      the other three parameters at set-point, aggregate + acidic variants + XMuLV LRF on every
      run). §12 assumption 4 now covers fragments only. §4.3, §5.1, §5.5, §6.4 and §8 rule 5 follow.
      No change listed in §1.1.
- [x] A3 every parameter name and unit now comes from `CFG` through `PN` / `PNC` / `PU` /
      `mv_txt` / `conc_txt` / `params_txt` / `conc_range_txt`.
- [x] A4 §7 says nothing about an acidic-variant widening; Table 7.2 and the derivation are computed.
- [x] B1 §7.1 item 3 is PCMP-001 §7.2's own remedy; the refit recipe and "fixed here, before the
      data are seen" are gone; new item 4 gives what follows when no adequate model results.
- [x] B2 §7.4 "not a more stable product" replaced.
- [x] B3 §1.1 change 1 says "the criteria upstream of this step".
- [x] B5 spiking procedure of Version 1.0 in §5.1, §5.3, Table 5.1 and Table 5.3.
- [x] B6 change 4 adds the model-adequacy tests Version 1.0 lacked.
- [x] B7 Table 11.1 carries Start and End from `study_chronology.csv`; start and end defined in the
      table note; change 6 lists it.
- [x] B8 §5.5 lists the verification of the platform worst cases among the single-batch judgements.
- [x] B9 Table 4.1 prints the register's "% (CEX/icIEF)"; CEX in the Abbreviations; §4.2 says
      acidic variants are measured by icIEF under SOP-3013.
- [x] B10 §7.3 surplus computed from `iac_viral_cumulative.csv`.
- [x] B11 appendix notes say the runs are in the order the design was generated, not standard order.
- [x] C residue: "clearance fold" gone, classification words (§7.5), univariate rule 5.
- [x] Gate passes with `--render` (3 passes with `--render`, 2 dry runs before them). Every hard
      gate OK. The numeral lint is advisory and its 24 lines are list numerals, identifiers
      (Version 1.0, SOP-4001, INV-001 finding 5, PCMP-001 §6.4) and statistical conventions
      (α, 4/n, log10), no typed measurement.
- [x] Tables 4.1, 5.3, 7.1, 7.2, 11.1 inspected in the PDF at 80 dpi. Table 5.3 was rebuilt once
      after the first look, because the Study and Runs cells wrapped too hard.
- **Final page count: 40 pp.** No `<<NEEDS:>>` markers.

## Notes for a successor

- **The study set of this plan is computed, not listed.** `mine` is the chronology of this step
  filtered to the five Version 1.0 study kinds AND `end < REV1["effective"]`. A second assertion
  checks that every other study of the step started after INV-001 opened. So re-dating a study
  into the Version 1.0 period fails the render instead of silently adding it to the plan.
- Table 5.3 now has one row per sample of a designed run (the four of Version 1.0 §5.4), with
  `merge=["Study", "Runs or conditions"]`.
- `A-Mab concentration` is measured in the input pool, so SOP-3016 and AMV-3021 (Protein A
  affinity HPLC, product titre) were added to this document's reference lists from the shared
  registry. Nothing else in the reference tables changed.
- Nothing outside the draft was edited.
