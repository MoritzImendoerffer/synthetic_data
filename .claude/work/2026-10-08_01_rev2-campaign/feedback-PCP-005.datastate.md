# PCP-005 (shipped Version 2.0): one pass for the owner's decisions of 2026-10-09

The document is `pc_package/PCP-005_protein_a.qmd`, already promoted. Edit it in place: these changes
are required by the decisions the owner took after it was shipped. Read `data-state-2026-10-09b.md` in
this folder first. Change what this list requires and nothing else.

1. **The hold study is not part of this plan.** No Version 1.0 document planned or reported a hold study.
   S-PA-HLD was made in September 2026, during the Version 2.0 re-analysis, and PCR-005 records it as
   PD-005-05, a discrepancy from the plan. Version 1.0 of this plan did not foresee a hold study, and
   the amendment does not add one. Remove from the plan:
   - objective 6 (the hold of the eluate);
   - the hold-study section ("Hold study of the Protein A eluate", @sec-hold);
   - the hold rows of the sampling and methods table and the hold sentences of the sampling plan;
   - the hold study from the study sequence (Table 11.1) and from the roles table;
   - the risk or assumption about retained hold samples (item 5 of Section 12);
   - every setup assertion about S-PA-HLD.
   The retest S-PA-RET covered the retained response-surface pools only (`T.methods_by_study` note b).
   Keep the eluate criteria that this step's output must meet (Section 7), because they are not a hold
   study. If a sentence there says how long or at which temperature the eluate may be held, remove it:
   that is the report's result.
2. **The acidic-variant upper limit of the bioreactor output** is back at its a priori value. The
   low-pH acidic-variant model fits exactly and is not adequate, so its bound no longer replaces the
   platform value. The sentence "It is … %, because low-pH viral inactivation adds fewer acidic variants
   than its platform worst case …" is now false, and its setup assertion `acid_bx[1] > acid_hi_apriori`
   fails. Write the limit as it stands, computed, with an assert that it equals the a priori value.
   Remove the widening reason.
3. **Section 8.1, what PCR-005 must give for the widened host cell protein criterion.** The criterion is
   widened by the anion exchange bound, under the single-batch rule. Cation exchange keeps its platform
   value. Item 2 ("The runs of the cation exchange design behind the bound") and any other cation
   exchange item there must name the step that widened it. Compute the step from
   `D.iac_verification()`, not by typing it.
4. **"{python} inad_text" printed as source.** Two inline expressions stand next to each other around
   the sentence on the widened criterion. Join them into one expression, or drop `inad_text` if it is
   empty.
5. **Changes in this revision.** Keep the list true after items 1 to 3. Do not mention the hold study.

Gate with `PATH="$PWD/.venv/bin:$PATH" uv run python authoring/check_render.py pc_package/PCP-005_protein_a.qmd --render`.
It now fails on an inline expression printed as source. Then report what you changed, the gate result
and the page count. The coordinator rebuilds the annex afterwards. Do not edit
`build_ground_truth.py` or any other shared file.
