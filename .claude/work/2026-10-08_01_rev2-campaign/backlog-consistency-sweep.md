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
- INV-002 factual check done (`factual-INV-002.md`, 9 errors: the fourth adequacy criterion of PCMP-001
  §7.2 (residuals/influence) left out; run 23 at design pH vs recorded pH (Protein A HCP full quadratic
  fails LOF at the recorded pH: decide whether the count becomes 15); Table 9.2 footnotes swapped;
  Version 1.0 misdescribed; AICc constant; INV-001 misquoted; NOR of the worked example; SOP-1002 title;
  Table 10.1 quoting). Next: one fix pass by a fresh author, then promote and annex.

## Third session (2026-10-10, owner upgraded the usage limits: "Proceed where you left off")
Baseline at start: 174 tests pass; HEAD 61a2a75; promoted with Version 2.0 annexes: PCMP-001, INV-001,
PCP-003, PCP-005, PCP-006, PCR-005.
Coordinator changes (uncommitted until the next checkpoint):
- `campaign.revisions[1].reason_plan`: plans and corpus documents no longer print "re-analysis of the
  studies" in their revision history (`revision_history`, report-only clause). The promoted plans
  PCMP-001, PCP-003, PCP-005 and PCP-006 must be re-rendered and their annexes rebuilt (the revision
  layer reads the helper) before the next strict grounding run.
- INV-002 config record: PA1 "for a probability of success of at least 0.90"; effectiveness check "the
  sample-size calculation of preventive action PA1"; `assurance_basis` "an attribute with a criterion";
  `D.fig_assurance` y-axis "Probability of success". INV-002 must drop its display-time substitutions.
- Plan drafts instantiated for PCP-004, PCP-009, PCP-010 (PCP-007/008 were already).
Agents launched (fresh contexts; resume with SendMessage if the session survives):
- INV-002 final fix (`feedback-INV-002.final.md`): a81452ec590153bd7
- PCP-007 author: ac165794047144c20; PCP-008: a85321c9cc5db62b4; PCP-009: a8386d13c874ea937;
  PCP-004: a4f22fc16c1edba54; PCP-010: ae1369f68bedfad4e
  (each keeps `status-<DOC>.md` in this folder; if cut off, a successor resumes from it).
Coordinator default taken (owner may override): INV-002 Table 3.1 counts the full quadratic models as
Version 1.0 fitted them (Protein A run 23 at its design pH); 14 failing stays; the recorded-pH failure
of pool HCP (lack of fit p = 0.024) is stated beside it. This keeps the promoted PCR-005 sentence true.

### Third session, continued (2026-10-10, late morning)
Owner's answers Q1-Q8 (seven open questions of REPORT-LESSONS plus the harvest/UF-DF scale-down gap) and
"go ahead with the data batch": implemented in 7768d43 (stage 1) and a0feef0 (stage 2); see
`data-batch-2026-10-10.md` and the authors' note `data-state-2026-10-10.md`. Afterwards (uncommitted):
PCR-003 register entries DEV-003-03..06 and PD-003-05/06 (from pcr003-departures.md; the initial
viable cell concentration effect on acidic variants, +3.4 points p = 0.029, is the PCR-003 author's
judgement and goes into its hand-back); revision reason per document class (`_revision_reason_key`).
Owner's table request: default layout unchanged; two optional passes (a rule under every row; x/y grid),
merged cells respected. Agent a23e63d9df374f2cd building it (ctable.py, table_rules.lua,
reference_rows/grid.docx, Makefile corpus-variant, variants/ folder). Do not render in pc_package/ while
it edits ctable.py.
Plan drafts written: PCP-004 (34 pp), PCP-007 (42), PCP-008 (37), PCP-009 (35), PCP-010 (29).
Reviews in: PCP-004 and PCP-010 (factual + content); fix lists `feedback-PCP-004.run1.md`,
`feedback-PCP-010.run1.md` go to the SAME authors (resume a4f22fc16c1edba54 and ae1369f68bedfad4e).
Not yet reviewed: PCP-007 (author ac165794047144c20), PCP-008 (a85321c9cc5db62b4), PCP-009
(a8386d13c874ea937). INV-002: last fix pass done (55 pp); next a short verification, promotion,
annex builder (`procedures/ANNEX-A-DOCUMENT.md`). PCR-005 re-opened: `feedback-PCR-005.datastate-2026-10-10.md`.
Next after the table agent: re-render promoted plans; launch PCR-003 and PCR-006 authors.
Agents running (2026-10-10, after fb15f2b): PCP-004 fix (resumed a4f22fc16c1edba54), PCP-010 fix (resumed
ae1369f68bedfad4e); PCR-003 author a927024c4bf0fc18f; PCR-006 author afabf170561291d76; PCR-005 data-state fix
abadf6256c0fc7077; content reviews PCP-007 a24e2bd5c70772f54, PCP-008 a2f8329cb027d5845, PCP-009
a57a2849aacbbd8ef; factual checks PCP-007 a5c7593f2fd5bff26, PCP-008 a33bf3aff8104fd1d, PCP-009
af2012aac231135e2; INV-002 verification a028da9c3f3c42e09. Reviewers return text (the harness blocks
subagent report files): save each as content-review-/factual-<DOC>.md.
Table-agent findings for the owner: (1) every uncaptioned pipe table in the default carries an empty last
row (the longtable counter patch in _tables.tex), fixed in the variants only; (2) INV-002 Table 5.1 note
cut off (fixed: shorter note, gate now probes note ends); (3) Approvals tables of INV-001/INV-002 ran 16 pt
past the margin (fixed: relative widths; template too); (4) row padding left out of the variants.

### Third session, afternoon (2026-10-10, after the API outage at about 14:30)
Promoted today: INV-002 (ff2b01f, 54 pp), PCP-010 (dcc175c, 31 pp). PCMP-001 re-rendered three times
(§7.5 rule 2 names the three tests; §7.8 fragments sentence; parameter table fits its page; the virus filter
role names XMuLV; the moved-set-point note names the plan's set-point); 535/535 grounded.
Machinery: check_render.check_footer_clear (text into the page foot); table-fit probe reads typographic
quotes; true minus in T.num/_sgn/offsets; T.criteria_results note c; fig_par band label;
design_space_grid includes fragments; ra_content.cqa_table criteria by type and no severity for unscored
attributes; DEV-005-02 rule on the full quadratic, ratio 3.0 (oot_check); register DEV-003-07/08,
DEV-005-03, DEV-007-03, DEV-008-04, wording of DEV-003-01/03/05.
Agents (resume by ID with SendMessage):
- Annex builders: INV-002 ac6a717e02b6ae911, PCP-010 ab582c36f3bd6aae7. After each: add the document to
  REV2_READY and to ALL_DOCS in tests/test_grounding.py, build, ground, commit.
- Plans: PCP-004 final pass (a4f22fc16c1edba54, feedback-PCP-004.final.md); PCP-007 revised (author
  ac165794047144c20), review run 2 aa97020d05885f3a3; PCP-008 revised (a85321c9cc5db62b4), review run 2
  a116dad938b470292; PCP-009 final pass (a8386d13c874ea937, feedback-PCP-009.final.md).
- Re-open of the promoted PCP-003/005/006 (a9fbbfbe01c8ef961, feedback-promoted-plans-reopen-2026-10-10.md);
  then re-anchor their annexes (legacy builders in build_ground_truth.py).
- PCR-005 follow-up (abadf6256c0fc7077, feedback-PCR-005.followup-2026-10-10.md); then re-anchor its annex.
- PTP-001: factual saved (factual-PTP-001.md); content review ad3f19600c7ed6b1b running; author a84158a8f962603ae.
- RA-001: factual saved (factual-RA-001.md); content review a2065767a62f14e49 running; author affba11fac83b329f.
  RA-001 author must adapt to ra_content.cqa_table (fragments severity None) and drop Table 3.2.
- PCR-003 drafted (79 pp; author a927024c4bf0fc18f): content review a9651619b55b03f57, factual a2df8d084c9f4048e.
  Its fix pass must cite DEV-003-07/08 and the reworded DEV-003-01/03/05.
- PCR-006 drafted (74 pp; author afabf170561291d76): content review ade968d8b5ef485a7, factual
  a7e90f52e29059230. Its fix pass: font floor on pp. 41, 51, 73 (Tables 7.4, 7.12, D.1).
For the owner (report when the round closes): the DNA calibration (AEX 5 logs, 70 kg reference adult);
the empty last row of uncaptioned pipe tables in the default layout; PCR-003 at 79 pp and PCR-006 at 74 pp
against the CLAUDE.md bands (update the bands at the end); `show()` re-parses pre-formatted numeric strings
(tabulate numparse), reported by the PCR-003 author.
For later reports: PCR-008 records the AEX coded-0 runs at 175 g/L (not the 200 g/L set-point) without
reconciling D-001, examines the HCP bound for single-run dependence, states the 5-log DNA clearance as
"more than" (pools below the LOQ), DEV-008-04; PCR-007 records DEV-007-03 and the missing load
aggregate/HCP and screening DNA/leached Protein A; PCR-009 records how yield was determined on spiked runs
(the Version 1.0 "unspiked filtrate pool" cannot exist); PCR-004 records the missing harvest scale-down
qualification as a deviation (owner Q8); every report states residual DNA as controlled by clearance (A-Mab:
"None as DNA is consistently cleared"), not by a release test.

### Third session, evening (2026-10-10, after the second API outage)
Promoted and annexed today: INV-002 (1052 quotes), PCP-010 (256), PCP-009 (485). Promoted, annex pending:
PCP-008 (annex agent ab7d06daaa01eeeab). REV2_READY = INV-001, INV-002, PCMP-001, PCP-003, PCP-005, PCP-006,
PCP-009, PCP-010, PCR-005.
Register added today: DEV-003-07/08/09, DEV-005-03/04/05, DEV-006-04, DEV-007-03/04, DEV-008-04 (32 in all).
Engine: screening setting corrections (DEV-003-01, run 4 at 153.5 mmHg); design-matrix letters from
D.factor_letters; fig_par viral band label; S-VI-WC relabelled (least favourable combination, not "harshest
within the PAR"); T.criteria_change note e names the three tests; INV-001 sentence likewise.
Agents (resume by ID):
- Re-open PCP-003/005/006: a9fbbfbe01c8ef961 (second pass: deleted Version 1.0 text, THRESHOLDS). Then re-anchor
  the three annexes (legacy builders in build_ground_truth.py) and re-render the promoted PCP-003/005/006.
- PCR-005 follow-up: abadf6256c0fc7077 (items 1-6 done; queued: classify by PCMP-001 §7.7, DEV-005-05). Then
  re-anchor the PCR-005 annex (legacy build_report_protein_a).
- PCP-004 final: a4f22fc16c1edba54. PCP-007 final: ac165794047144c20. Then promote each, annex agents.
- PCR-003 revision: a927024c4bf0fc18f (feedback-PCR-003.run1.md). PCR-006 revision: afabf170561291d76
  (feedback-PCR-006.run1.md). Then review run 2 each.
- RA-001 content review a2065767a62f14e49; PTP-001 content review ad3f19600c7ed6b1b (factual checks saved). Then
  fix passes by their authors (affba11fac83b329f, a84158a8f962603ae).
Owner questions (report at the round's end): DNA calibration (AEX 5 logs, 70 kg); the empty last row of
uncaptioned pipe tables; page bands (PCR-003 79 pp, PCR-006 74 pp); show() numparse; the low-pH acidic-variant
results with no scatter (33 runs against an icIEF repeatability of 0.41 points: a data-integrity signal?); the
bioreactor classes of dissolved oxygen (KPP) and basal medium (GPP) against the stated mechanism; the integrated
model vs the fitted models (Table 8.1 means vs the RSM set-point predictions).
