# INV-001, final fix pass: what to change

The draft (`pc_package/INV-001_investigation.DRAFT.qmd`) passed its review cycle. Since then the
analysis changed (owner's decisions of 2026-10-09), and the setup chunk now stops at two assertions.
This pass brings the draft into line with the data. It is a fix pass: change what the list requires,
keep everything else, and keep the voice of the draft.

Every value and every deciding word comes from the data, through the brief
(`authoring/out/INV-001.brief.md`, regenerated today) and the helpers. Never type a number.

## A. What changed in the data, and where the draft is now wrong

1. **The setup stops at `assert pa_narrowed and vi_narrowed`.** No Protein A NOR changes at Version
   2.0: on the selected models the qualification of the Protein A scale-down model holds over the NOR
   as characterized, for pool host cell protein and leached Protein A, on the planned runs alone and
   on all runs (`T.sdm_offsets_data`, `D.offset_qualification`). The next assertion
   (`assert not bool(_qa.loc["pool_hcp_ng_mg", "qualified"])`) and `pa_narrow_phrase` go. Replace
   them with assertions of what the data now say, so that a re-run that changes it fails loudly.
2. **Low-pH viral inactivation: the NOR moved, it was not simply narrowed.** From config, through
   `Parameter.nor` / `.nor_characterized` and `.setpoint` / `.setpoint_characterized`
   (`CFG.unit_op("viral_inactivation").param(key)`): the pH NOR moves lower and keeps its width, with
   the set-point moved with it; the hold time NOR is narrowed at its low end and its set-point moved to
   the middle of the new NOR; the temperature NOR is narrowed at its low end. Classify each parameter's
   change in the setup chunk (moved, narrowed, set-point moved) and build the sentences from that.
   The reason, from the data: on the selected XMuLV model the platform claim is not met at the least
   favourable combination of the NOR as characterized (`D.nor_met` inside `D.characterized_nor()`),
   and it is met across the NOR in force (`D.nor_met` outside it). The set-point decision itself
   (large-scale control of pH) belongs to PCR-006; one clause pointing there is enough.
   Fix every sentence that says PCR-005 and PCR-006 "each narrow a NOR" (Summary, §6 near line 970)
   and "PCR-006 Version 2.0 narrows the NOR of the step for this reason" (near line 1223), and the
   comment near line 54.
3. **PD-005-01 (the six further scale-down runs, S-PA-SDM2), near line 1002.** Pool host cell
   protein is now modelled on the log scale and its offset is a ratio of geometric means, so the
   interval is a ratio interval, not a half-width in ng/mg. State the ratio and its interval on the
   planned runs and on all runs (`D.offset_qualification(..., studies=...)`: `offset`, `lo`, `hi`),
   that the conclusion against the criterion over the NOR is the same at either end on both run sets
   (so the model is qualified on the planned runs alone as well), and that the further runs narrowed
   the interval. Keep the record of why the runs were made (during the re-analysis, to narrow the
   offset interval of pool host cell protein) and that they are a discrepancy from the plan, not a
   deviation. Never say the three-run result would have failed (STORY_BIBLE §9b, PD-005-01).
   `pa_hcp_use` (how near host cell protein comes to its criterion) must still be right under the
   log model: check how it is computed.
4. **Preventive actions, near line 968.** "The preventive actions revise SOP-1002 so that ..." Only
   preventive action PA1 revises SOP-1002. Name the action that does it.
5. **Two corrective actions named CA3.** INV-001's CA3 reissues the reports. INV-002's CA3 analyses
   every response-surface output by model selection. Wherever the draft means INV-002's, it must say
   "INV-002 corrective action CA3" (or name what it does), never a bare "CA3". Check every occurrence.
6. **The criteria rest on the selected models.** INV-002 corrective action CA3 was adopted on
   `CFG.raw()["campaign"]["model_adequacy"]["selection_adopted"]`, before INV-001 closed, so the
   verification behind the criteria fixed at closure used the selected models (the draft already says
   so near line 1179). `hcp_aex_text` is a computed paragraph I wrote in a hurry: read it in the
   rendered PDF, check it against `T.worst_case_verification()` and `D.iac_table("protein_a")`, and
   rewrite it in the draft's voice if it reads badly. The numbers must stay computed.
7. **Table text below 7.9 pt.** `check_render` reported a page of the PDF with text below 7.9 pt. The
   likely cause is `T.worst_case_verification()` (its sub-header columns are `R{1.5cm}`). Find the
   table on that page; fix the builder in `pc_package/tables.py` if the builder is the cause (keep its
   other callers working: PCMP-001, PCR-005 and INV-002 carry it too), or the call if the call is.

## B. Check, do not assume

- Every sentence near the ones above whose deciding word (met, not met, narrowed, moved, qualified,
  wider) depends on the changed data. Compute it or assert it in the setup chunk.
- §6.3 counts of the proven acceptable ranges that changed: re-read them in the rendered PDF against
  the table they summarise.
- The chronology now excludes the augmentation studies of INV-002 (they started after INV-001's
  scope); keep it so, and keep the Version 1.0 figures computed on the planned runs with the full
  quadratic (`D.planned_full_models()`), as the draft does.

## C. Gate and render

`uv run python authoring/check_render.py pc_package/INV-001_investigation.DRAFT.qmd --render` until it
passes, then render pdf and docx and look at every complex table once (`pdftoppm` a page to png and
read it). Report: which model you are, each item above and where you changed it, the number of
`check_render` passes, the page count, and anything you could not resolve.
