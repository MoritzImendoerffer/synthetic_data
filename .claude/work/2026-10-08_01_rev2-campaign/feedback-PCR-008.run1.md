# PCR-008 after the factual check: what to change (one fix pass, same author)

Input: `factual-PCR-008.md` and `data-state-2026-10-11.md` (both in this folder). Read them, and
`procedures/REPORT-LESSONS.md` §3 rule 1, §6 and §7. The owner changed the pipeline on 2026-10-11: no separate content
review ran on this draft. The readability review comes once, after this pass. Write cleanly now. Every value stays
computed and every deciding word computed or asserted. Regenerate your brief (`authoring/build_brief.py PCR-008`),
because the register, the criteria and the helpers changed.

## A. The record
- **New register entries** (config): PD-008-04 to PD-008-10 record the eleven departures you handed back, all confirmed
  by the factual check, and its additional ones:
  - PD-008-04: bed pressure and the spiking-model qualification;
  - PD-008-05: virus assay controls and detection limits;
  - PD-008-06: load qualified on acidic variants only, and its lots not recorded;
  - PD-008-07: records of execution not kept (system, calibration, lots, analyst, review, retained samples, the run of
    DEV-008-03, approval of the designs);
  - PD-008-08: measurements and analyses of the plan not made (DNA and leached Protein A on the augmentation runs,
    ANOVA for yield and fragments, the PAR figures, the completion rule);
  - PD-008-09: protein load coded about 175 g/L, which is not its set-point. Describe the coding as it is, and never
    connect it to the "PAR (set-point)" column. D-001 stays as registered;
  - PD-008-10: the approaches where the plan sets no threshold, and the analyses the plan does not contain.
- **Text.** Describe each in the discrepancy part and cite it where the text relies on it. Remove any claim that the
  record is complete. §3.2 must not assert platform control (DEV-008-03 shows a buffer lot out of range). Put any
  departure still in neither register in your hand-back.

## B. The criteria and the verification moved (data-state §2)
The engine now applies the offset to the verification. Re-read every number from the helpers. These have moved:
- the anion exchange host cell protein fold bound is 4.18, still above the platform 4, so the widening holds. Drop
  your offset-sensitivity bound if it duplicates this, and keep the unfavourable end of the offset interval, computed;
- the cation exchange host cell protein criterion is 418 ng/mg;
- the Protein A host cell protein criterion is 16,719 ng/mg.
Do not say that the verification is judged without an offset.

## C. Owner decision
Flow rate stays WC-CPP. Argue the class as a judgement on the scope of the viral clearance claim, and say that no flow
effect was detected. Quote PCMP-001 §7.7 with "practically relevant" and the too-small clause (error 12).

## D. Errors: resolve each as the file gives it
- E1: use PCMP-001's statement that all 11 register attributes are CQAs, and follow its consequence for the WC-CPP rule.
- E2: each model meets every criterion that applies. Present the carve-out as the report's reading.
- E3: scope "no effect" to the response-surface model, and give the screening term for fragments.
- E4: write "at manufacturing scale where an offset is known (pool host cell protein)".
- E5: limit the DEV-008-02 claim to the two executions.
- E6: name the load results that exist.
- E7: compare like with like.
- E8: give the INV-002 success definition with its two criteria.
- E9: say "of the 28 planned runs".
- E10: the step-yield model on the planned runs also fails the F-test.
- E11: the edges and the margin, unrounded as the file gives.
- E13: the isoelectric point sentence is backwards. Binding needs a pH above the pI; PCP-008 §4.1 words it correctly.
- E14: report the yield at the high-load, high-conductivity runs beside the bound-antibody explanation.
- E15: the minor items. Step yield needs a method in Table 3.2 or D.1.

## E. Gate and report
- Gate with `check_render.py --render` (`.venv/bin/python`, venv on PATH).
- Render the pdf and the docx, and run `check_render` once more.
- Read the page image of every table you changed.
- Refresh `.claude/work/2026-10-08_01_rev2-campaign/PCR-008_aex.DRAFT.txt`.
- Report each item with where it was resolved, anything left and why, the passes, the page count, and any `<<NEEDS:>>`
  left (none). Do not commit.
