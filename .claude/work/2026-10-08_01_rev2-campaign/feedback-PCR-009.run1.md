# PCR-009 after the factual check: what to change (one fix pass, same author)

Input: `factual-PCR-009.md` (in this folder). Read it, and `procedures/REPORT-LESSONS.md` §3 rule 1, §6 and §7. The
owner changed the pipeline on 2026-10-11: no separate content review ran on this draft. The readability review comes
once, after this pass. Write cleanly now. Every value stays computed and every deciding word computed or asserted.
Regenerate your brief (`authoring/build_brief.py PCR-009`), because the register and the helpers changed.

## A. The record
- **New register entries** (config, committed 0b43e1b): PD-009-03 to PD-009-07 record the departures your hand-back
  and the factual check confirmed:
  - PD-009-03: the qualification without flux decay and integrity results, and without a record of the matching;
  - PD-009-04: the integrity tests and virus controls of the design runs not recorded;
  - PD-009-05: step yield and filtrate fractions not recorded as planned. PCP-009 §5.2 planned yield by mass balance
    on the spiked run, and §5.4 an unspiked pool; the plan conflicts with itself;
  - PD-009-06: load material and flux of the spiked runs not compared;
  - PD-009-07: analyses the plan does not contain.
- **Text.** Describe each in the discrepancy part (§13.3 then lists registered entries) and cite it where the text
  relies on it. Use "not recorded", not "not measured", where the record is silent (error E4). Add that Version 1.0
  asserted every post-use test passed with no result recorded. Put any departure still in neither register in your
  hand-back (for example the PAR figures, sample identification and calibration status, if the entries above do not
  cover them).

## B. Builders changed under you (re-render; the draft predates them)
- **`D.par_table`** gives XMuLV "n.a. | n.a. | no adequate model" (E1). Reword the two §7 sentences and the Table 7.3
  note: XMuLV has no PAR, and every measured result met the claim. Drop the §1.2 clause about ranges from measured
  results. In §1.4 add that the Version 1.0 XMuLV PARs (50–140 L/m2, 8–30 psi) are withdrawn.
- **`T.criteria_results`**: the single-run limits column and a wrapped header. You may drop your PDF-twin wrap.
- **`T.model_reevaluation`**: true minus signs.
- **`D.anova_lof_df`**: handles a model with no term.

## C. Errors: resolve each as the file gives it
- **E2:** "The qualification runs were made in study S-VF-SDM…", not "qualified".
- **E3:** cite PCP-009 §5.2 and §5.4 and state their conflict. The departures are those of PD-009-05.
- **E5, the fragments deletions.** Every single-run deletion gives a no-term model on 11 runs with a gap of 0.21. For a
  model with no term the gap is (2n − 1)/(n − 1)², fixed by the number of runs (0.19 at 12, 0.21 at 11), so criterion 3
  then judges the number of runs, not the model. Say that, and say what does not change: the judgement over the NOR,
  the range carried into the control strategy (set by MVM) and the design space.
- **E6:** limit the study-event claim. Deleting one run at a time does not bound an event that affected several runs.
  Table 5.9 covers response-surface runs only.
- **E7 to E17:**
  - the Version 1.0 pressure PAR as printed, 12.1–24.8 psi, or say it was recomputed with inward rounding;
  - p ≥ 0.48;
  - p = 0.0497, or p < 0.05;
  - adjusted R² for the full quadratics, and the Version 1.0 conditions judged for fragments;
  - "with a criterion" (E11 and E15);
  - the Box-Cox interval on the wider grid;
  - "Median" where Table 5.9 holds medians;
  - the formatting of the builder values you print yourself;
  - the Cpk minimum (1.0) beside the target;
  - the plan's criterion 4 quoted as it is ("repeating the judgement").
- **D-001 stays as registered.**

## D. Owner question (leave the config as it is; state the facts)
Filtration pressure is a WC-CPP in the config, and no term containing pressure is significant for any output. A-Mab
classed both parameters of this step WC-CPP, because "both are easy to control and have minimal impact on LRF when
operated within their acceptable ranges". Argue the class on that basis and on the scope of the viral clearance claim.
Say that no pressure effect was detected. Do not change the class.

## E. Gate and report
- Gate with `check_render.py --render` (`.venv/bin/python`, venv on PATH).
- Render the pdf and the docx, and run `check_render` once more.
- Read the page image of every table you changed.
- Refresh `.claude/work/2026-10-08_01_rev2-campaign/PCR-009_virus_filtration.DRAFT.txt`.
- Report each item with where it was resolved, anything left and why, the passes, the page count, and any `<<NEEDS:>>`
  left (none). Do not commit.
