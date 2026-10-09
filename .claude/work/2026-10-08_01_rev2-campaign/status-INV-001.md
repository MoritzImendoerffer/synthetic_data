# INV-001 fix pass for the owner's decisions of 2026-10-09: status at wrap-up

Agent: Opus 5.5 (claude-opus-5-5). File edited: `pc_package/INV-001_investigation.qmd` only.
Not touched: `tables.py`, `build_ground_truth.py`, config, `doe_report.py`, `_pcpkg.py`,
`amab_process/`. Nothing committed.

## 1. What I changed

Each item below is computed or asserted in the setup chunk. Nothing is typed.

- **Item 1, single-batch bound.**
  - `VB` comes from `D.VERIFICATION_BOUND`.
  - The setup asserts the new verification state:
    - Cation exchange host cell protein is confirmed: within the NOR the model predicts 44.9-fold against a platform value of 40.0. Its single-batch bound, 36.7, is below the platform value, so the platform value stands.
    - The anion exchange bound, 4.27 against 4.00 on an adequate model, is widened.
    - New count `n_ver_kept` (3), and `n_ver_better_inadequate` is asserted to be 0.
  - The derivation checks now use a relative tolerance, because `iac_verification.csv` rounds to 4 decimals.
  - Prose:
    - The Summary CA1 sentence is rewritten.
    - §6.1 rule 1 now says: a worse A-Mab prediction is replaced by the single-batch bound (tighten); a better single-batch bound on an adequate model replaces the platform value (widen); otherwise the platform value stands. No criterion comes from a point prediction or from a confidence bound of the mean.
    - The §6.1 closing paragraph is rewritten.
    - The §6.2 counts paragraph is rewritten.
    - The host cell protein paragraph: `hcp_aex_text` is removed and replaced by inline sentences. Cation exchange criterion 400 → 427 ng/mg, Protein A criterion 16,000 → 17,069 ng/mg, Version 1.0 limit 10,724 ng/mg.
    - The cation exchange aggregate paragraph now gives the single-batch bound of 1.40.
    - New canon sentence: both bioreactor widenings (aggregate 0.56 against 0.70, acidic variants 0.40 against 1.00) come from the shorter A-Mab hold, at most 120 min against a 180-min platform hold, not from greater stability. The 180 min is parsed from the config `iac.platform` source strings, and the 120 min is the characterized NOR.
- **Item 2, Protein A load NOR.**
  - Asserted: over the NOR as characterized, pool host cell protein is not qualified on either run set. With the ratio at the low end of its interval, the upper limit is 17,143 ng/mg against a criterion of 17,069.
  - The load NOR narrowing (20–40 → 20–39 g/L resin) is classified from the config.
  - Over the narrowed NOR, the model is qualified on all runs (16,763 ng/mg) and not on the planned runs alone (18,786 ng/mg).
  - Leached Protein A is qualified everywhere.
  - §2 PD-005-01 is rewritten as two paragraphs:
    - the ratios, the discrepancy, and "not a deviation";
    - the qualification failure over the characterized NOR, the narrowing, and that the six further runs made the qualification possible. The decision to add them was taken after the planned-run result was known; this is stated as a limitation.
  - The Summary adds the PCR-005 narrowing.
- **Item 3, low pH.**
  - No hold-time value is stated.
  - The Summary and §6.3 say PCR-006 Version 2.0 moves the NOR and the set-point of inactivation pH lower and narrows the hold-time and temperature NORs, and that "PCR-006 gives the values and the reasons".
  - The reason stays computed: the XMuLV claim is not met at the least favourable combination of the characterized NOR, on the Version 1.0 model and on the selected model.
  - Removed: "met across the NOR in force" and the per-parameter value sentences.
- **Item 4, S-BRX-OSM.**
  - It is found as the one other study that started after Version 1.0. Its discrepancy (PD-003-01, PCR-003) is looked up in `PLAN_DISCREPANCIES`.
  - It is excluded from the Version 1.0 count, the same way S-PA-SDM2 is.
  - §1 now reads: the count covers every study that started before closure, except the 2 INV-002 augmentation studies and 5 others. One computed sentence says S-BRX-OSM started on 2026-09-01, during the investigation, is outside its scope, and is recorded by PCR-003 as PD-003-01. No results are described.
- **Item 5, calibration.**
  - `eq` is restricted to the systems the Version 1.0 studies used (EQ-TFF-188 is dropped).
  - `cw` is asserted to equal the Version 1.0 studies that used an instrumented system.
  - The margin text still holds: 7 studies on 3 systems, smallest margin S-UFDF-UNI at 26 days.
- **Item 6, shared changes.** The prose around the changed tables needed no change. The §6.6 process sentence is now computed (NORs at Protein A and low-pH viral inactivation, set-points at low-pH viral inactivation), and an assertion checks that no other step changes.

## 2. What is verified

- A scratch dry-run of every chunk and inline expression passes: 272 segments, 0 errors. Only the plan-date assertion below was skipped, in a temporary copy that has been deleted.
- One real `check_render` run (dry): the style gate passes (no gated tic, no banned phrase). The setup fails at qmd line 309, `assert all(r[2] < r[3] for r in _pl)`.
- Not rendered: the pdf and docx are stale (from before this pass). The annex has not been rebuilt or grounded.

## 3. What is left

1. **Data blocker (config; not mine to change).** S-BRX-SDM was re-dated in 0b452c9 to start on 2025-08-11. PCP-003 was approved on 2025-08-25, so a study now starts before its plan was approved. That contradicts INV-001 F1/F5 and the STORY_BIBLE chronology. Fix one of:
   - set `campaign.plan_approval.PCP-003` to a date between 2025-08-04 (PCMP-001 approval) and 2025-08-11; or
   - start S-BRX-SDM after 2025-08-25.
   Check that the PCP-003 draft agrees.
2. After the fix, run `PATH="$PWD/.venv/bin:$PATH" uv run python authoring/check_render.py pc_package/INV-001_investigation.qmd --render`, then look at Tables 4.3, 6.1 and 6.2.
3. **Shared builder notes still say "95 % confidence bound".** They render in this document and contradict the single-batch rule:
   - `T.iac_derivation` notes b) and e);
   - `T.criteria_change` note e);
   - `T.worst_case_verification` notes b), c) and d).
4. **The annex builder needs re-anchoring before the build.** `build_investigation()` in `pc_package/build_ground_truth.py` reads the removed names `_vs` and `vi_nor_count`. It also quotes sentences that changed:
   - the PD-005-01 qualification sentences;
   - "The model is therefore qualified on the planned runs alone as well." and "The further runs narrowed the interval and did not change the conclusion.";
   - the Summary PCR-006 sentence, which now follows a new PCR-005 sentence;
   - §6.1 rule 1;
   - the §6.2 count sentences;
   - "On that model it is met across the NOR in force at Version 2.0.";
   - "PCR-006 gives the reason for the new set-points …";
   - the §6.6 process sentence;
   - the per-row verification statements ("at the 95 % confidence bound").
   The new statements to anchor are: the PCR-005 narrowing, the qualification over each NOR, the optional-stopping limitation, S-BRX-OSM / PD-003-01, and the low-pH hold reason.
   Then run, in `pc_package`: `python build_ground_truth.py`, `python validate_annex.py`, `GROUNDING_STRICT_ANCHORS=1 python check_grounding.py`.
5. Minor: the §4.6 sentence could say "the 7 Version 1.0 studies". It is still true as it stands.
