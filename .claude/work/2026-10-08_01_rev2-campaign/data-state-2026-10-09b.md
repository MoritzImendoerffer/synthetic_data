# Data state after the owner's decisions of 2026-10-09 (second session)

The data, the config and the engine changed once, together, after every author had stopped. Read this
before you render, because some assertions in your draft will now fail, as they should. Every value
below comes from the data. Pull it through the helpers; never type it from here.

## 1. An exact fit is never adequate (owner: "Not adequate; the a priori value stands")

- Acidic variants in the low-pH response-surface design have no scatter: every result at the same hold
  time is identical. The full quadratic therefore reproduces them exactly. With no residual there is no
  pure error for the lack-of-fit test and no residual mean square for the model F-test, so PCMP-001
  §7.2 cannot be applied. The Box-Cox profile is unbounded, so no scale is chosen and no interval is
  reported. The prediction interval has zero width.
- `adequacy.select_model` now returns `adequate = False` for an exact fit. `D.fit(...)["status"]` is
  "none" and `D.fit(...)["exact"]` is True. The output is judged on its measured results.
- Its bound (0.40 points) is below the platform value (1.00), but it no longer replaces it, because the
  model is not adequate. So **the bioreactor acidic-variant upper limit is back at its a priori value**
  (`D.iac_table("bioreactor")`, `iac.csv`), and it is no longer "widened". Every sentence that explains
  an acidic-variant widening must go. Aggregate is the only bioreactor criterion that the low-pH hold
  widened.
- The aggregate model at low pH has no pH term. The NOR in force ends at the same longest hold and
  highest temperature as the NOR as characterized, so the aggregate bound also covers the NOR in force.
  Compute it if you state it.
- INV-002 counts one adequate selected model fewer (`T.model_adequacy`, its brief).

## 2. The hold studies were made in the Version 2.0 re-analysis (owner: "Re-date into the Version 2.0 period")

- No Version 1.0 document planned or reported a hold study. S-HAR-HLD, S-PA-HLD and S-VI-HLD are now
  dated in September 2026, after INV-001 closed and after AMD-001 (`study_chronology.csv`).
- Fragments are measured by nrCE-SDS on every sample, and there is no SEC fragment result
  (`hold_<pool>.csv`; `T.hold_stability(pool)` has no SEC fragment column and no "retained samples"
  note). The retests S-PA-RET and S-VI-RET covered the retained response-surface samples only
  (`T.methods_by_study` note b).
- Each report records its hold study as a discrepancy from the plan: PD-004-02 (harvest), PD-005-05
  (Protein A), PD-006-05 (low pH), in `discrepancy_register(DOC)`. The computed model-selection
  discrepancies keep their numbers (PD-005-04, PD-006-04).
- **No plan describes a hold study.** Version 1.0 of the plans did not foresee one, and a Version 2.0
  amendment does not add one. Remove from a plan its hold-study design, sampling, schedule rows and any
  hold criterion stated as part of the plan.

## 3. The A-Mab concentration study at low pH (owner: "Deviation plus a confirmation study")

- PCP-006 Version 1.0 §6.4 set the concentration study across the range 5 to 35 g/L, with the other
  three parameters at their set-points, and required aggregate, acidic variants and XMuLV log
  reduction on every run. S-VI-UNI measured aggregate and acidic variants only, and PCR-006 Version 1.0
  did not notice.
- PCP-006 Version 2.0 keeps the Version 1.0 design (an amendment does not change a plan to match what
  was done). PCR-006 Version 2.0 records the omission as deviation **DEV-006-03**, found in the
  re-analysis, closed by the confirmation study **S-VI-UNI2** (discrepancy **PD-006-06**): XMuLV-spiked
  low-pH holds at both ends of the concentration range, in duplicate, the other parameters at their
  set-points as characterized (`univariate_studies.csv`, column `xmulv_lrf`).
- The step model has no concentration term in the inactivation, so the two levels differ by run-to-run
  variation only. A single run below the claim is not the claim failing: the claim is judged on the
  model at the least favourable NOR combination.

## 4. Labels (owner: "Fix all")

The parameter is now "CO2 partial pressure (pCO2)" (mmHg), and the units are mOsm/kg (osmolality),
% air saturation (dissolved oxygen), 10⁶ cells/mL (initial viable cell concentration) and
× standard (basal medium concentration). Never type a parameter name or unit: use
`CFG.unit_op(UO).param(key).name` and `.unit`. Remove any abbreviation entry for an old unit
(e.g. "e6").

## 5. What a Version 2.0 plan may add (coordinator, after the PCP-006 factual check)

A Version 2.0 plan is an amendment issued after its studies ran. It states what PCMP-001 Version 2.0
sets: the a priori criteria, the fragment method, the scale-down offset rule, the adequacy tests, the
judgement statistics, the verification rule and the execution windows. It lists each as a change. It
must not add a step-specific decision rule, such as a refit procedure, a NOR rule for one parameter or a
test chosen for one study. Such a rule is written with the data known, which is INV-001 finding 1 again.
It never says a rule was "fixed before the data". It keeps the design, sampling and spiking as Version
1.0 planned them, even where a study departed from them, and the report records the departure. Where
Version 1.0 had no rule that the report needs, the plan says it has none. The report then states its
approach and records it as a discrepancy. STORY_BIBLE §9b has this as canon.
