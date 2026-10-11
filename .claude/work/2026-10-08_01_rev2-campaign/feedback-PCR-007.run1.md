# PCR-007 after the factual check: what to change (one fix pass, same author)

Input: `factual-PCR-007.md` and `data-state-2026-10-11.md` (both in this folder). Read them, and
`procedures/REPORT-LESSONS.md` §3 rule 1, §6 and §7. The owner changed the pipeline on 2026-10-11: no separate content
review ran on this draft. The readability review comes once, after this pass. Write cleanly now. Every value stays
computed and every deciding word computed or asserted. Regenerate your brief (`authoring/build_brief.py PCR-007`),
because the register, the criteria and the helpers changed.

## A. The record
- **New register entries** (config): PD-007-05 to PD-007-11 record the departures your hand-back and the factual check
  confirmed:
  - PD-007-05: load aggregate and host cell protein not recorded;
  - PD-007-06: residual DNA and leached Protein A not measured on the screening runs;
  - PD-007-07: flow-through, wash and strip fractions and the mass balance not recorded (the strip test could not be
    triggered);
  - PD-007-08: packing tests for the three qualification runs only, with no limits;
  - PD-007-09: S-CEX-FRC, in neither version of the plan;
  - PD-007-10: the approaches where the plan sets no threshold, and capability for the drug substance, not the step;
  - PD-007-11: feed lots not recorded.
- **Text.** Describe each in the discrepancy part and cite it where the text relies on it. Use "not recorded" where the
  record is silent. Where Version 1.0 asserted that the load and fractions were assayed and the column released, say
  that it did so with no result recorded. Put any departure still in neither register in your hand-back.

## B. The criteria and the verification moved (data-state §2)
- **Offsets in the verification.** The engine now applies the offset to the verification (PCMP-001 §7.1 rule 2), so
  error 1 changes. Do not say that the verification is judged without an offset. Re-read every number from the helpers.
  These have moved:
  - the host cell protein fold within the NOR is 40.22 against the platform 40, with a bound of 32.93;
  - the aggregate fold bound is 1.398;
  - the cation exchange host cell protein criterion is 418 ng/mg;
  - the Protein A host cell protein criterion is 16,719 ng/mg;
  - the low-pH aggregate criterion is 6.84 %.
  Keep the sensitivity to the ends of the offset interval, computed: at the unfavourable end the host cell protein
  fold falls below 40.
- **Cation exchange pool aggregate is now 4.90 %**, tightened on verification. UF/DF raises aggregate within its NOR.
  The one-sided 95 % single-run bound of the rise, 0.104 points, is carried back from the drug substance limit. Say
  this wherever the pool criterion appears, and pull every value.
- **Fragments, error 2.** One verdict: confirmed by the plan's rule (PCP-007 §7.6), on a model that does not meet
  PCMP-001 §7.2, stated as a limitation. This is the same resolution as PCR-006.

## C. Owner decisions
- **Stop collect.** The data stand as observed. Aggregate rises with the AU setting, against the expected mechanism
  (PCP-007 §4.1; A-Mab). The report gives no cause. Say that yield shows no stop-collect term.
- **Elution flow rate stays GPP.** Argue the class as a judgement of practical relevance. DNA clearance is 0.32 log10
  lower at 300 cm/hr (p = 0.044), which puts residual DNA under "affected" by PCMP-001 §6.2. Give its size against the
  drug substance (residual DNA per dose, Cpk) and name the judgement as a judgement. For yield, the interval includes
  an effect as large as the load effect, so do not write "changes neither". Quote PCMP-001 §7.7 with "practically
  relevant" and the too-small clause (error 11).

## D. Errors 3 to 13: resolve each as the file gives it
- E3: the design space at the a priori criterion is not 100 %. Give the computed share, and rest "covers the whole
  region" on the widening.
- E4: add the drift to the design-space maximum and to the unfavourable end of the qualification, or limit "does not
  depend on the trend" to the NOR.
- E5: the duplicate scatter is larger than the residual SD for aggregate and DNA clearance. Say so for each response.
- E7: objectives 2 and 3 were amended at Version 2.0. Quote objective 5 in full.
- E8: drop "met platform specification" (DEV-007-01, PD-007-08).
- E9: name what the study events leave unchanged, and write "no effect detected" with the tests. Deleting run 14
  changes the selected aggregate model and gives yield a stop-collect term. Do not infer "no effect" from the
  selection having removed a term.
- E10: the curvature of host cell protein against load is below the centre-point spread. Do not claim it as a finding
  (PCP-007 §12).
- E12: the study window includes S-CEX-VER and S-VI-WC, and Table 3.2 includes S-VI-WC.
- E13: the minor items, each as listed.
- **D-001 stays as registered.**

## E. Gate and report
- Gate with `check_render.py --render` (`.venv/bin/python`, venv on PATH).
- Render the pdf and the docx, and run `check_render` once more.
- Read the page image of every table you changed.
- Refresh `.claude/work/2026-10-08_01_rev2-campaign/PCR-007_cex.DRAFT.txt`.
- Report each item with where it was resolved, anything left and why, the passes, the page count, and any `<<NEEDS:>>`
  left (none). Do not commit.
