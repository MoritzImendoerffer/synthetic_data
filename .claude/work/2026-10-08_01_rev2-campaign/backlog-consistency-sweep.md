# Consistency sweep and open decisions (kept current; 2026-10-09, second session)

## Owner decisions taken on 2026-10-09 (implemented in 0b452c9 and after)
1. **A criterion is widened or tightened on the single-batch bound.** The bound is the one-sided 95 %
   prediction bound of a single batch at the least favourable NOR combination (`iac.BOUND_CONFIDENCE`,
   `bound="batch"`). Every change is argued by its risk: whose risk it is (producer or patient), how
   it is detected, and its impact on the downstream steps and the drug substance. INV-002 states the
   result: cation exchange host cell protein no longer widens (40 stays), and the other four criteria
   widen by 4 % to 7 %.
2. **Harvest and UF/DF.** Option c: new Version 2.0 univariate studies S-HAR-UNI2 and S-UFDF-UNI2
   (PD-004-01, PD-010-01).
3. **Low-pH hold time.** The NOR in force was revised to 100–120 min with the set-point at 110. That
   revision triggered the confirmation runs S-VI-WC at pH 3.20 / 120 min (PD-006-03). There, cation
   exchange misses the pre-set fragment-clearance rule (fold bound 1.25 < 1.30). Accepted on risk
   (decision 5a).
4. **Osmolality.** Option b: collect more data in study S-BRX-OSM (PD-003-01). The 400 set-point is
   not made the upper limit. The acidic-variant risk at the worst corner is accepted as the producer's
   risk, with mitigation, and the NOR is not narrowed (decision 6a, EMA definition of a NOR).

## Second session of 2026-10-09 (after the usage-limit stop and a restart)
Done by the coordinator:
- **Data blocker fixed.** PCP-003 Version 1.0 approval moved to 2025-08-07, before S-BRX-SDM
  (2025-08-11, re-dated in 0b452c9 to hold a full culture). New test
  `test_each_plan_approved_before_its_first_study`.
- **Shared builders.** `T.nor_change(par)` classifies a NOR change as narrowed, moved, or moved and
  narrowed; `T.parameters_by_step` now says "Moved" for the low-pH pH NOR. `check_render`'s table probe
  compares without whitespace (the PDF drops the space after a minus sign).
- **INV-001** rendered (38 pp, gate green). Tables 4.3, 6.1 and 6.2 inspected. Annex re-anchored on the
  fix-pass text: 432 quotes. New non-claim NC08 (S-BRX-OSM outside the scope); the low-pH NOR changes
  anchored on the direction-only sentence; the Protein A load NOR on PD-005-01's new paragraph.
- **PCMP-001** re-rendered (39 pp, gate green). Annex re-anchored: 534 quotes. Re-analysis studies the
  plan does not list are noted, not recorded; the NOR and set-point changes are separate statements,
  each on its own footnote, with the verb from `T.nor_change`.
- **PCP-005** still described the verification rule with "95 % confidence bound" (7 places). Corrected
  to the one-sided 95 % prediction bound of a single batch, re-rendered (gate green), annex rebuilt (186).
- STORY_BIBLE (the older verification paragraph), section_plan (`acceptance_framework`) and a
  `doe_report` comment now state the single-batch rule.
- Gates: 170 tests pass; 21/21 annexes valid; `GROUNDING_STRICT_ANCHORS=1` 3250/3250.

Running (fresh agents; the previous ones were lost with the restart):
- PCR-005 follow-up author (status note §3: the prose for the single-batch rule and the narrowed load
  NOR; length below 70 pp).
- PCP-003 author for the review-run-1 fix cycle (every prose fix still open).
- INV-002 content review run 2 (fresh judge) → `content-review-INV-002.run2.md`.
- PCP-006 factual pass (fresh agent) → `factual-PCP-006.md`.

## Next, in order
- **PCP-006:** final fix pass from review run 2 (`content-review-PCP-006.run2.md`) and the factual pass;
  then promote, rewrite `build_plan_viral_inactivation` for the Version 2.0 text, add to REV2_READY.
- **INV-002:** fix pass from review run 2, then a factual check. The author flagged two statements as its
  own reading of the specification limits and not a recorded release-test list: "detected at release"
  and "not the patient". Then promote it, write a new annex builder, add it to REV2_READY and
  test_grounding.
- **PCP-003:** review run 2 by a fresh judge, factual pass, final fix pass, promote, rewrite the annex
  builder (`T.sop_references` with the plan's `PLAN_SOPS`/`PLAN_AMVS`).
- **PCR-005:** factual pass on the follow-up text, then promote and re-anchor `build_report_protein_a`;
  update `authoring/rhetorical/PCR-005.spans.yaml` (it references DEV-005-03).
- **PCR-006 and PCR-003 briefs** carry S-VI-WC (decision 5a) and S-BRX-OSM (decision 6a) as of
  2026-10-09. Author each once its plan is final. The PCR-006 brief mentions S-BRX-OSM once, so check
  where before authoring.
- Never stage `.claude/transitions/` or the signal and wakeonlan files.

## For the owner (collected, not yet decided)
- **Units and labels in the config** (PCP-003 review; they print in every parameter table, e.g. PCMP-001
  Table 4.2): "mOsm" should be mOsm/kg, "% sat" should be % air saturation, "e6 cells/mL" should be
  10⁶ cells/mL, the basal medium unit prints as "X", "Dissolved CO2 (pCO2)" mixes a concentration with a
  partial pressure, and decimals are uneven ("1–1.4" beside 1.2, set-point "1"). An earlier unit change
  to SI was tried and reverted (ede101e) with no recorded reason, so this waits for the owner.
- Residual DNA criterion ≤ 0.001 ng/dose (unit); no ELISA coverage figure in the record; six step-yield
  results at 99.0 %; the GPP class of temperature and bed height does not cover fragments; DEV-005-02
  has no out-of-trend limit; `D.governing_factor` returns load for fragments.

## Machinery noted, not yet done
- Done 2026-10-09: named constants `D.PAR_GRID_SETPOINT`, `D.NOR_SD_DIVISOR`, `D.PI_LEVEL`,
  `D.VERIFICATION_BOUND` (= `iac.BOUND_CONFIDENCE`); PCP-003 and PCP-006 use them.
- `_pcpkg` has no `BIOREACTOR_SOP_REFS`/`BIOREACTOR_AMV_REFS`; PCP-003 filters `SOP_REFS`/`AMV_REFS`.
- **Title block (2026-10-09):** "(Step N)" no longer wraps; the sites are three rows (sponsor,
  development site, commercial drug substance site) instead of one row joined by an arrow. The site
  entities of the annexes now quote those rows. Every shipped Version 2.0 document must be re-rendered
  BEFORE its annex is rebuilt (done for PCMP-001, PCP-005 and INV-001; PCR-005 when promoted).
- Helper tables flagged by the PCP-003 review: Tables 1.1 and 7.1 use different footnote letters for the
  same ideas; "margin" used for a divisor; SOP-3016 paired with AMV-3021 against the number scheme;
  `T.iac_derivation` prints "≥ 16.7" beside "≥ 8.60".
- Design space on the mean vs per batch (PCP-003 review); KPP process-performance data;
  `revision_history` content; registry title nits.
