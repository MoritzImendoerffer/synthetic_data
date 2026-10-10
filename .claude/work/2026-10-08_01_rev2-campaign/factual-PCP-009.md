# Factual check of PCP-009 Version 2.0 (draft rendered 2026-10-10 11:40)

Checker: Claude Opus 5.5 (claude-opus-5-5). Returned as text; saved by the coordinator (condensed, every
error kept). Sources: the draft's own tables, brief, data-state note of 2026-10-10, CSVs, config,
rendered PCMP-001, frozen Version 1.0 PCP-009, PCMP-001 and PCR-009. D-001 (§8 item 1) is worded at the
strength §5c directs and is not an error.

## Errors, most consequential first

1. **"No approved Version 1.0 plan contained these criteria" against the frozen Version 1.0 PCP-009,
   which contains them** (Table 1.1 note a, from `T.criteria_change`; §1.1 "set after the data were seen
   and were in no approved protocol"). The frozen Version 1.0 PCP-009 has Table 7.1 (MVM LRF ≥ 4.97,
   XMuLV LRF ≥ 5.47), its §5.3 ("the acceptance criteria in §7 allow 0.35 log10") and §7 floors 3.89 and
   3.65. The draft's own change 7 says only the title-block date was wrong. On the Version 1.0 criteria
   the MVM NOR-propagated PAR (50 to 97.2 L/m², 12.2 to 24.7 psi) excludes the NOR edges (105 L/m²,
   10 psi); Version 2.0 (≥ 4.62, worst-case mean) gives 50 to 136 and 8 to 30. Applies to every frozen
   Version 1.0 plan with a design (PCP-005 to PCP-009 carry a Table 7.1 of step criteria).
   **Coordinator's resolution (canon, INV-001 §5 root cause 1):** "Criteria set after execution could
   therefore be added to the plan text when the package was compiled, without a revision of the approved
   plan (finding F1)." The frozen Version 1.0 plan text is the July 2026 compilation, with the
   analysis-time criteria written into it; the plan approved on 2026-04-13 did not contain them. The
   note stands. The plan says so once where its criteria are given, and its change on the Version 1.0
   record names both what INV-001 found: the title-block date AND the criteria added to the plan text at
   compilation without a revision of the approved plan.
2. **Criterion 4 tests the wrong quantity** (change 4, §5.5, §7 condition 4: "the residuals ... regressed
   on the predicted value"). The rule in force regresses the ABSOLUTE residuals on the predicted values
   (config comment, `D.residual_influence`, data-state §2); raw least-squares residuals have zero slope
   against the fitted values by construction (slope about 1e-15, p = 1.000; the absolute-residual test
   gives p = 0.68, 0.08, 0.09, 0.73 for MVM, XMuLV, fragments, yield). Fix: "the absolute residuals are
   regressed on the predicted value, and the residuals on run order".
3. **The classification rule was rewritten without being listed** (§7). Version 1.0: "A parameter whose
   variability affects a CQA will be classified as a CPP, or as a WC-CPP where the risk of operating
   outside the design space is low given the control capability of the commercial equipment." The draft
   requires a "significant and practically relevant effect" and moves the WC-CPP test to PAR width
   against NOR. Fix: keep the Version 1.0 sentence and list PCMP-001 Version 2.0 §6.2 and §7.7 as a change
   (as PCP-010 does), with the Version 1.0 wording.
4. **The refit route is added but not listed** (§7: "A model that fails the lack-of-fit test or the limit
   on overfitting may first be refitted with a justified change of terms or transformation (PCMP-001
   §7.2)"). Version 1.0 §7: "Where a model fails these checks, the affected response will be reported
   descriptively and no range will be claimed from it." Fix: list it in change 4 with the Version 1.0
   consequence.
5. **The success criterion has no defined test at this step**, and §12 deletes the Version 1.0 rule "If
   the qualification in §5.1 fails, the study cannot proceed." Fix: restore the deleted rule; add a
   sentence that no output with a criterion is compared at both scales, so the qualification decision of
   PCMP-001 §7.1 applies to none, and PCR-009 states its approach.
6. **The sampling plan was rewritten** (Table 5.4, §5.2): Version 1.0 assayed "the unspiked load and the
   unspiked filtrate pool" for protein. Fix: restore the Version 1.0 protein wording; name the fragment
   sample under change 2 or leave it unstated.
7. **Version 1.0 expectations softened where the data did not bear them out** (§6.3 curvature at the top
   of the load range; §4.3 MVM fall steeper at the top of the pressure range; §6.1 MVM retention expected
   to fall at high pressure; §4.1 yield falling slowly with load). Fix: restore the Version 1.0
   expectations; PCR-009 compares them with the data.
8. **§5.5 "At this step no output with a criterion has an offset"** reads as zero. Fix (coordinator):
   "has no measured offset; the offset is unknown, not zero", as §5.1 and PCMP-001 §7.1 say.

## Checked and correct
Identity and dates (Version 2.0 effective 2026-09-30, supersedes 2026-04-13; first study 2026-04-15;
windows; no S-VF-AUG); INV-001 and AMD-001 facts; revision history; 15,000 L; Table 6.1 (no nor_v2 or
setpoint_v2 at this step); Table 4.1; Table 1.1 values and Table 7.1 against `iac.csv` and
`criteria_rev1.csv` (4.97 and 5.47 = nominal 5.32 and 5.82 less 0.35; floors 3.89 and 3.65); claims 16.72
against 16.7 and 8.62 against 8.6; AEX MVM 4.00; nothing tightened or widened; no platform worst case to
verify; the designs (7-run factorial with 3 centre points; 12-run face-centred, 4 + 4 + 4) and lack-of-fit
degrees of freedom; Appendices A and B; nrCE-SDS fragments on every run, no SEC; AMV and SOP assignments;
3 scale-down and 5 manufacturing runs of step yield; every threshold; the §8 engine description; PCMP-001
citations; the Version 1.0 design, spiking, LOD handling, controls, integrity exclusion, continuous
filtration, univariate confirmation, data management, roles and change control; §9b compliance.

## Observations (not errors)
The design-space sentence names no statistic (PCMP-001 sets none, so naming one would add a rule unless
every plan does); "effects ... over half the range studied" is Version 1.0 wording (PCR-009 records the
departure from PCMP-001 §6.2); flux decay and the integrity test stay as Version 1.0 design though the
record holds step yield only; INV-002 appears only in the revision history; AMD-001 (2026-03-20)
predates the Version 1.0 approval (2026-04-13), yet Version 1.0 omitted fragments (canon point).

## Could not be checked
SOP-4001 content (placeholder); platform history, mechanism statements, ICH content; prospective
commitments with no record (flux decay, integrity results, titres, sample identity, filtrate fractions).
