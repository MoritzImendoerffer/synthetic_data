# PCP-006: final pass (review run 2, the factual check, the owner's decisions of 2026-10-09)

Fix these and nothing else. The draft is `pc_package/PCP-006_viral_inactivation.DRAFT.qmd`. Read
`data-state-2026-10-09b.md` in this folder first: the data changed, and some assertions will fail, as
they should. Section 5 of that note, on what a Version 2.0 plan may add, governs this pass.

## A. The owner's decisions of 2026-10-09

1. **Hold study.** S-VI-HLD was made in September 2026, during the Version 2.0 re-analysis. Version 1.0
   of this plan did not foresee it, and the amendment does not add it. Remove from the plan:
   - its design (§6.5);
   - its rows in the sampling plan (Table 5.3) and in the study sequence (Table 11.1);
   - any hold criterion stated as part of this plan (§7.5);
   - change 5 of §1.1, as far as it concerns the hold.
   PCR-006 records the hold study as PD-006-05.
2. **The A-Mab concentration study** keeps its Version 1.0 design. Version 1.0 §6.4 set A-Mab
   concentration one factor at a time, at settings across the range 5 to 35 g/L, with pH, hold time and
   temperature at their set-points. It measured aggregate, acidic variants and XMuLV log reduction on
   every run. State that design. Remove §12 assumption 4's statement that the study does not measure
   XMuLV clearance, and do not list a change. That S-VI-UNI measured no XMuLV is a deviation that
   PCR-006 records (DEV-006-03). The plan neither mentions it nor adapts to it.
3. **Labels.** Never type a parameter name or unit; pull them from `CFG.unit_op(UO).param(key)`.
4. The bioreactor acidic-variant upper limit is at its a priori value again: the low-pH acidic-variant
   model fits exactly and is not adequate. Check that nothing in §7 says a low-pH bound widened it.
   Table 7.2 and the derivation are computed.

## B. The factual check (`factual-PCP-006.md`): resolutions

1. **§7.1 item 3: the refit rule.** Delete "The change is fixed here, before the data are seen, and one
   refit is allowed" and the two refit bullets (log transform, hierarchical backward elimination). State
   the remedy for a failing model exactly as the rendered PCMP-001 §7.2 states it, and what follows when
   the model still fails (no range from it; the output judged on its measured results). A plan issued
   after its data may not add a refit procedure. Model selection (INV-002 CA3) is the report's
   discrepancy (PD-006-04), not the plan's method.
2. **§7.4: "not a more stable product".** Only the report can know this, and for acidic variants it is
   false. Say instead what the plan can state: a bound smaller than the platform value may reflect the
   shorter hold of the A-Mab NOR as well as the product, and PCR-006 states which, for each attribute.
3. **§1.1 change 1.** The verification of this step's platform worst cases moves the criteria
   **upstream** of this step, never this step's own. This step's criteria move only through the
   verification at cation exchange (PCR-007).
4. **The univariate study:** see A2.
5. **The spiking procedure** of Version 1.0 governed the runs that were made. An amendment cannot
   change it. State it as Version 1.0 planned it:
   - The XMuLV spike is added to the pool after acidification and before the hold begins, at the volume
     ratio fixed in SOP-2009, which is small enough not to change the pH or the antibody concentration.
   - The input titre is taken from a sample of the spiked pool at the start of the hold. The output
     titre is taken at the end of the hold. The log reduction is the difference between the two.
   - Each design point has a spiked run for XMuLV and an unspiked counterpart for product quality.
   - Version 1.0 took three samples from each spiked run and two from each unspiked run:
     - the input pool before acidification (aggregate, acidic variants, concentration), from both runs;
     - the spiked load after acidification and before the hold (XMuLV), from the spiked run;
     - the end of the hold (XMuLV), from the spiked run;
     - the neutralized pool after neutralization and filtration (aggregate, acidic variants), from the
       unspiked run.
   - Fragments by nrCE-SDS come from the neutralized pool, as AMD-001 and the retest S-VI-RET make them
     (Table 5.2).
   Make §5.1, §5.3, Table 5.1 and Table 5.3 say this. A change you cannot source from these facts or
   the brief stays out.
6. **§1.1, the list of changes.** Add the model-adequacy tests that Version 1.0 lacked:
   - predicted R² within the limit of R²;
   - the regressions of the residuals;
   - the Cook's distance cut-off.
   PCP-005 lists the same as its change 4. These are generic tests applied the same way in every plan,
   not a rule for this step. Remove the hold study (A1).
7. **Execution dates.** Give Table 11.1 Start and End columns from `csv("study_chronology.csv")` for the
   studies of this plan: S-VI-SDM, S-VI-SCR, S-VI-RSM, S-VI-UNI and the retest S-VI-RET. Define start
   and end once. List it in §1.1 as PCP-005 does ("records the execution window of every study that the
   plan governs", INV-001 finding 5).
8. **§5.5, the single-batch judgements.** Add the verification of the platform worst cases (§7.4) to
   the list. The hold criterion is gone (A1).
9. **Table 4.1, acidic variants.** Print the criterion as the register gives it (`cqas_for`), "% (CEX/icIEF)".
   Put CEX in the Abbreviations as the register uses it: cation exchange chromatography, an analytical
   method for charge variants. This campaign measured acidic variants by icIEF (SOP-3013); say so once.
10. **§7.3, "cannot be made up".** The claims exceed the requirement by a small surplus. Compute it from
    `csv("iac_viral_cumulative.csv")` and write that a shortfall larger than that surplus cannot be made
    up by the other steps.
11. **Appendix notes, "standard order".** The runs are in the order of the design file
    (`D.planned_matrix_df`), not Yates order. Say that.

## C. Review run 2 (`content-review-PCP-006.run2.md`): still open

Most of its findings were fixed in your last pass. Check each against the current text and fix any
that remain, with these resolutions:
- **Q4, classification words.** PCMP-001 and SOP-4001 set no numerical threshold for "practically
  relevant" or "wide". Do not let them decide a class. Say that PCR-006 states the effect size across
  the PAR and the margin of the PAR to the NOR, and classifies on them.
- **Q4, the remedy path:** resolved by B1.
- **Q4, "the designs"** for an output with no adequate model: name the response-surface design.
- **Q2, "NOR-propagated":** the corpus term, defined in PCMP-001. Define it at first use in words.
- **"Clearance fold"** becomes "clearance factor" everywhere in your prose. The builders already use
  "clearance factor".
- **Q7**: name each thing at first use in a section, with its code.
- **Tables 4.1, 5.3, 7.2, 11.1** are your own. Use at most two header lines, no constant column, units in
  the header, a legend for every code, and merged repeated cells (`T.frame(..., merge=[...])`). Table 7.2
  note a) must say what it marks.

## D. Gate and report

Gate with `PATH="$PWD/.venv/bin:$PATH" uv run python authoring/check_render.py pc_package/PCP-006_viral_inactivation.DRAFT.qmd --render`.
It now also fails on an inline expression printed as source: join adjacent inline expressions into one.
Look at Tables 4.1, 5.3, 7.1, 7.2 and 11.1 in the PDF. Report what you changed under A, B and C, the
gate result, and the page count.
