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

## Owner's answers of 2026-10-09 (second session), implemented in 26e5356
1. Exact fit: not adequate, a priori value stands (bioreactor acidic upper limit back to 39.0).
2. Hold studies: re-dated into September 2026, discrepancies from the plan (PD-004-02, PD-005-05,
   PD-006-05), nrCE-SDS at every time point; no plan describes one.
3. Low-pH concentration study: deviation DEV-006-03 plus the confirmation study S-VI-UNI2 (PD-006-06).
4. Labels: all fixed (pCO2 partial pressure, mOsm/kg, % air saturation, 10⁶ cells/mL, × standard).
Coordinator, same session: what a Version 2.0 plan may add (STORY_BIBLE §9b; PLAN-LESSONS rule 9);
INV-002 CAPA statuses and effectiveness check (config); sample-size table wording; the gate for an inline
expression printed as source. Data-state note for authors: `data-state-2026-10-09b.md`.

## In flight (second session, after 26e5356)
- PCP-003 author (resumed): data-state note + amendment scope (remove the osmolality NOR rule and other
  post-data rules; generic residual tests). Then review run 2 + factual pass + final fix.
- PCR-005 author (resumed): hold study as PD-005-05, nrCE-SDS throughout; acidic widening gone. Then a
  factual pass, promote, re-anchor `build_report_protein_a`, rhetorical spans.
- PCP-006 final fix pass (fresh author, `feedback-PCP-006.final.md`). Then promote and rewrite
  `build_plan_viral_inactivation`.
- INV-002 final fix pass (fresh author, `feedback-INV-002.run2.md`). Then a factual check, promote, write
  its annex builder, add to REV2_READY and test_grounding.
- PCP-005 (shipped) data-state pass (fresh author, `feedback-PCP-005.datastate.md`): hold study out of
  the plan, acidic sentence, §8.1 anion exchange, the "{python} inad_text" leak. Then rebuild its annex.

## Next, in order (older list; still valid where not superseded above)
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

## State at the usage limit (2026-10-09, about 20:40)
- Committed: 26e5356 (decision batch), 62fd2f5 (PCP-005, PCMP-001 hold decision), 6c7dd35 (PCR-005 at 67 pp).
- Uncommitted, safe:
  - CLAUDE.md (exact fit, amendment scope, UNI2 studies);
  - tables.py note d) of `T.worst_case_verification` (exact-fit wording). INV-001 and PCMP-001 were
    being re-rendered for it (`render6_*` logs in the scratchpad). Re-render both, then rebuild their
    annexes with `gt_one.py`;
  - PCP-006 draft after its final pass (40 pp, rendered, gate green). One open fix: Table 5.1 names
    AMV-3021, the titre HPLC, for the load concentration. It should be A280 (AMV-3019). My attempt
    failed a setup assertion and was reverted; find which assertion (probably the `_amv` lookup:
    AMV-3019 may not be in AMV_REFS or VIRAL_INACT_AMV_REFS). Then promote PCP-006 and write its annex
    builder (pattern: `build_plan_protein_a`).
- Agents running at the limit; their outputs land here:
  - INV-002 final fix: draft and `status-INV-002.md`;
  - PCP-003 review run 2: `content-review-PCP-003.run2.md`;
  - PCP-003 factual pass: `factual-PCP-003.md`;
  - PCR-005 factual run 3: `factual-PCR-005.run3.md`.
  If a file is missing, that agent was cut off: rerun it.
- Next:
  - PCP-003 final fix pass from the run-2 review and the factual pass, then promote and annex;
  - PCR-005 final fixes from factual run 3, then promote, re-anchor `build_report_protein_a`, and
    update the rhetorical spans;
  - INV-002: factual check, promote, new annex builder, REV2_READY, test_grounding;
  - then the plans PCP-004 and PCP-007 to PCP-010 (briefs ready; give authors PLAN-LESSONS.md and the
    data-state note), then the reports, PTP-001, RA-001 and PCMR-001.

## State after the reset (2026-10-09, late; owner: only 4 % of the weekly limit left)
- Promoted with Version 2.0 annexes: PCMP-001, INV-001, PCP-005, PCP-006 (1ca165e). PCP-003 promoted
  (41 pp), its annex builder running; until it lands, strict grounding fails on PCP-003 only.
- PCR-005: final fixes from `factual-PCR-005.run3.md` running (resumed author); new config discrepancy
  PD-005-06 (load mass from the titre assay). After it: promote, re-anchor `build_report_protein_a`
  (fitted to the 2026-10-08 text; large job), rhetorical spans.
- INV-002: final pass done (54 pp); factual check running (`factual-INV-002.md`). Then a short fix pass,
  promote, new annex builder, REV2_READY, test_grounding ALL_DOCS.
- PCP-007, PCP-008: authors STOPPED at the start to save budget; the instantiated template drafts
  `pc_package/PCP-007_cex.DRAFT.qmd` and `PCP-008_aex.DRAFT.qmd` are empty templates; re-launch with the
  same prompt (it is in this session's history: brief, RUNNER, section_plan, STORY_BIBLE, WRITING_GUIDE,
  REGISTER_EXEMPLAR, PLAN-LESSONS, data-state note; may read rendered PCMP-001 and the frozen V1.0 plan
  for content only).
- Not started: PCP-004, PCP-009, PCP-010; all reports except PCR-005; PTP-001, RA-001, PCMR-001.
- PCR-003 must record the departures in `pcr003-departures.md`.
- Small open items: config revision reason "re-analysis of the studies" is wrong for plans (shared, affects
  every revision history); `D.fig_assurance` y-axis says "Assurance"; INV-002 config wording ("assurance",
  "design-size check", "criterion attribute"): INV-002 substitutes at display time with asserts.
