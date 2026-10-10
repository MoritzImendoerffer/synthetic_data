# PCR-005: follow-up pass after the record changed (2026-10-10, afternoon)

Fix these and nothing else. The document is promoted: `pc_package/PCR-005_protein_a.qmd`, edited in place.
Every value stays computed and every deciding word computed or asserted.

1. **DEV-005-02, the out-of-trend rule, changed** (your flag). The record now reads: "outside the two-sided
   99 % prediction interval of a single result from the full quadratic model of the response-surface design,
   fitted to the other runs of the design without the result under review, at the settings of the run".
   Model selection was adopted in September 2026, while the review was made when the design ran, so the
   review fitted the model the plan specified. The ratio of the first result to the re-assay is now 3.0
   (`dev_005_02_first_over_reported`). `D.oot_check` fits the full quadratic: the interval at run 11 is about
   −1.46 to 5.38 ppm on 12 residual degrees of freedom (`df` in its result), the first result (about 6.4 ppm)
   lies above it and above every other run, and the re-assay inside. State the interval as the rule gives it
   (its lower end lies below zero, so only a high result could be out of trend at that run). Your asserts on
   `oot_terms == ["D"]` and on the selection with the first result in place no longer hold: follow the data,
   and keep every claim computed.
2. **The widening rule, §7.1** (your flag): state it as PCMP-001 §7.5 rule 2 now does: the first three
   adequacy criteria (a significant model, no significant lack of fit, the limit on overfitting) and not an
   exact fit; the fourth criterion does not decide the change. Where PCR-005 relies on the widened host cell
   protein criterion, PCMP-001 §7.5 asks the report that relies on it for "the bound, the runs behind it,
   and the reason why the performance of the downstream step for A-Mab is known well enough": the anion
   exchange model meets the first three criteria and fails the fourth on Cook's distance; INV-002 §8.4 shows
   the bound still above the platform value with each flagged run deleted (cite it, values computed through
   the helpers). Never "passed the adequacy tests".
3. **New deviation DEV-005-03** (`deviations.csv`): the univariate study ran each end of each range in
   duplicate, without the runs at the centre that PCP-005 requires; the reference is the qualification runs
   at set-point. PCP-005 is being restored to its Version 1.0 §6.4 (low edge, centre, high edge, the same
   responses as the multivariate designs), so PCR-005 records this departure in its deviations section, and
   beside the univariate results. The fragment result by nrCE-SDS of S-PA-UNI is not measured (samples not
   retained), as you already state.
4. **Builders changed under you**: true minus signs in the tables (`T.num`); the note of
   `T.criteria_results` for an output with no adequate model now reads "the range of the measured results of
   the designs, less the offset of the scale-down model where one is known"; `D.design_space_grid` includes
   fragments (no grid point excluded). Re-render and check the font floor and the table fit.
5. Leave the annex: the coordinator re-anchors it after this pass.

Gate with `check_render.py --render` (with `.venv/bin/python`), render the pdf and the docx, read the page
image of every table you changed. Report each item with where it was resolved, the passes, the page count,
and any `<<NEEDS:>>` left (none).

## Resolution (author, 2026-10-10, Claude Opus 5.5)

All items are done in `pc_package/PCR-005_protein_a.qmd`. The backup is `PCR-005_protein_a.pre-followup.qmd`.
Details are in `status-PCR-005.md` §5.

1. §13.2 states the rule as recorded: the full quadratic model, 99 %, −1.46 to 5.38 ppm on 12 df. The lower
   end lies below zero, so only a high result could be out of trend. The first result is 6.37 ppm (3.0 ×),
   above the interval and above every other result. The re-assay lies inside both. The first-result
   analysis was recomputed: log scale, end of pool collect, F-test p = 0.0495, −22 %, limit 6.60 ppm, PARs
   span. All of it is computed and asserted.
2. §7.1 states the rule as PCMP-001 §7.5 rule 2 now does. The anion exchange paragraph gives the three
   criteria, the fourth failing on Cook's distance (runs 2 and 9) and INV-002 §8.4 (4.33–4.56 against 4).
   These values are recomputed in the setup through the helpers, with the bound reproduced to the table.
   The CA3 sentence names the failing test. "Adequacy tests" no longer appears.
3. DEV-005-03 is recorded in §13.3, §4.4, §5.6, the Discussion, §1.4 item 10 and the executive summary.
4. Builders: the design-space assert includes fragments, and the table fit and font floor are checked
   (the deviation register's disposition column now wraps).
5. Annex not touched.
6. DEV-005-04 (added during the pass) is recorded in §13.4, §3.1 beside the offsets table, §1.4 item 10, the
   executive summary, the §13 introduction and Conclusion 11. p = 0.037 is computed from
   `sdm_qualification.csv` (S-PA-SDM runs), and no other compared output differs. The offset analysis is
   unchanged.
7. Classification (re-open of PCP-005): §9 is argued by PCMP-001 §6.2 and §7.7 as PCP-005 criterion 7 applies
   them, without the removed rule. For each parameter it gives the significant terms with p, the size of each
   effect across the PAR (pool HCP in ng/mg and as a share of the criterion) and the margin of the PAR to the
   NOR, all computed. Every class of the config is supported. The KPP classes of load flow rate and end of
   pool collect rest on judging small significant effects on pool HCP (6 % and 7 % of the criterion).
8. DEV-005-05 is recorded in new §13.5, in §4.1 at the chronology, in §1.4 item 10 and in the executive summary.
9. The objectives are quoted from the re-rendered PCP-005 §2 (seven, word for word), with one sentence naming
   the section that answers each.
10. Owner's decision "4/n flags, F decides": the criterion 5 definition, Table 5.13 (F median, Met), §5.5, F8,
    Conclusion 3, the Discussion and the §13.6 introduction are updated. The anion exchange model now meets the
    fourth criterion (no run above 0.81; runs 2 and 9 examined, INV-002 §8.4).
Layout: the discrepancy register is set landscape (PD-005-02's new text). Final: 73 pp, final gate green, no
`<<NEEDS:>>`.
