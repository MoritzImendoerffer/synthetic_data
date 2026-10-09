# PCMP-001 fix pass (decisions of 2026-10-09): status

Agent: Opus 5.5. Only `pc_package/PCMP-001_master_plan.qmd` was edited. Nothing committed.

## 1. What I changed

Setup chunk:
- Chronology: the plan lists the studies the Version 1.0 reports analysed plus S-PA-SDM2
  (`start < REV1 effective` or `kind == "qualification"`). The old kind filter let the new
  re-analysis univariate studies S-BRX-OSM, S-HAR-UNI2 and S-UFDF-UNI2 through, which broke
  `assert len(_post) == 1`. They are now left to the reports, like the augmentation and
  support studies before them.
- `n_eq` counts the systems the listed studies used (3). Asserted equal to
  `T.calibration_windows_data()` and to its set of studies.
- Verification: no longer requires a "better but inadequate" case (there is none now). The
  inadequate and confirmed sentences are built only when they apply. The host cell protein
  text is classified per step: the anion exchange bound (4.27) replaced 4-fold, and the cation
  exchange bound (36.7) does not exceed 40-fold, so 40 stands. The Protein A fold check now
  handles both cases.
- New computed facts, each with an assert:
  - `vb` from `D.VERIFICATION_BOUND`.
  - Every verified worst case is a quality attribute judged per batch.
  - The platform hold (180 min) is parsed from the `iac.platform` sources. The A-Mab hold is
    `nor_characterized[1]` (120 min), and the NOR in force is no longer than that.
  - The bioreactor criteria that the low-pH replacements widened.
  - The site names, derived from SENDING_SITE and RECEIVING_SITE and checked against the
    title-block rows.
  - Each planned qualification study closed before the first characterization study of its
    step.
- NOR and set-point text is computed from `Parameter.nor` against `.nor_characterized` and
  `.setpoint` against `.setpoint_characterized`, and classified as narrowed or moved.

Prose:
- "Changes in this revision", item 2: the one-sided 95 % prediction bound of a single batch at
  the least favourable NOR combination, never a confidence bound of the mean. Every change is
  argued by its risk.
- §1: the sites are pulled from the constants, and "facility" becomes "site" to match the
  title block.
- §2, §5 (paragraphs 1 and 3) and §7.1: the qualification runs and the offset estimate come
  before the first characterization run. The qualification decision is made at analysis,
  because it needs the response-surface model. The PCP states which outputs are not compared,
  and the PCR states the consequence when the model is not qualified.
- §4: computed sentence (Protein A narrowed its load NOR; low-pH viral inactivation moved its
  pH NOR and set-point, and narrowed the hold-time and temperature NORs with a new hold-time
  set-point).
- §6.3: three single-batch analyses, now including the verification.
- §7 introduction and §7.4: the host cell protein paragraph, the table paragraph ("platform or
  verified"), the summary paragraph with the shorter-hold statement, and the last paragraph.
- §7.5: what the bound is and why (per batch; the platform value was a single run; a tolerance
  interval would be purer but too conservative), the rule, the four-part risk argument, and the
  outcomes, including that the low-pH replacements reflect the shorter hold.

## 2. What is verified

- The setup chunk runs with no failing assertion.
- `check_render.py --render`:
  - docx and pdf render.
  - The style gate passes, with no gated tic and no banned phrase.
  - No missing glyphs, every cross-reference resolved, all 12 complex tables complete, no
    repeated index cell, no text below 7.9 pt.
  - The numeral lint lists 29 lines. It is advisory, and the lines it flags are document IDs in
    lines that were already there.
- The PDF has 39 pages.

## 3. What is left

- **The annex has not been rebuilt.** `build_master_plan()` raises `KeyError: 'S-BRX-OSM'`,
  because it loops over the full `study_chronology.csv`. `ground_truth/PCMP-001.json` is the old
  file, and grounding was not run. Needed in `build_master_plan()`:
  1. Skip chronology IDs that the plan's table does not list.
  2. Re-anchor the verification statements on the new text ("The prediction bound of a single
     batch was better than the platform worst case for ..."). Drop the statement built from
     `vinad_list`, which is empty now, and replace the "confidence bound" wording in the
     statement texts.
  3. Fix the NOR statements. The regex takes the first footnote marker of each row, and for
     inactivation pH and hold time that is the set-point marker, so the statements land on the
     wrong footnote. The pH NOR was moved, not narrowed. Write the NOR and set-point statements
     separately, each on its own footnote.
  4. Then rebuild, run `validate_annex`, and run `check_grounding` with
     `GROUNDING_STRICT_ANCHORS=1`.
- The complex-table pages of the PDF have not been looked at as images.
- Shared output that is now wrong (in `tables.py`, not changed by me):
  - In `T.iac_derivation`, footnotes a) and c) as PCMP-001 renders them still say
    "95 % confidence bound". The plan's prose now contradicts its own table until this is
    fixed. The same old wording is in note e) of `T.criteria_change` and notes b) to d) of
    `T.worst_case_verification`.
  - `T.parameters_by_step` says "Narrowed at Version 2.0 from pH 3.4–3.6" (c2). The pH NOR was
    moved (3.3–3.5, same width), not narrowed.
- Depends on uncommitted work in `tables.py`: `calibration_windows_data` is limited to the
  Version 1.0 studies. Against the committed `tables.py`, the `n_eq` assertion stops the
  render, as it should.
- To confirm: the plan's chronology (34 studies, ending 2026-09-11) and its equipment
  paragraph leave out S-BRX-OSM, S-HAR-UNI2, S-UFDF-UNI2 and EQ-TFF-188.
