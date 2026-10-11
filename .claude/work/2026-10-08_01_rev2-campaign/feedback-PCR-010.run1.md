# PCR-010 after the content review and the factual check: what to change (one fix pass, same author)

Inputs: `content-review-PCR-010.md`, `factual-PCR-010.md` and `data-state-2026-10-11.md` (all in this folder). Read
them, and `procedures/REPORT-LESSONS.md` §3 rule 1, §6 and §7. This draft had its content review before the owner
changed the pipeline. One readability review comes after this pass. Write cleanly now. Every value stays computed and
every deciding word computed or asserted. Regenerate your brief (`authoring/build_brief.py PCR-010`), because the
register, the config and the citation changed.

## A. Owner decisions (2026-10-11)
- **Diavolumes are one-sided.** Their NOR is a minimum, "≥ 7" DV (`nor_one_sided: low`; builders print it). A further
  diavolume only lowers the residual process buffer. Rewrite every passage that treats 9 DV as an upper NOR limit.
- **The buffer-exchange criterion (PD-010-07, new).** The plateau criterion of PCP-010 §5.5 has two conditions. Quote
  both. It could not be judged as planned, because the record holds no conductivity reading (PD-010-02). Do not write
  "not met" (error E2). The buffer exchange is controlled by its minimum number of diavolumes, with the formulation
  buffer of the drug substance confirmed against its release limits. Keep the residual process buffer values as the
  result. Make no claim of a release value, because the record holds none.
- **The cation exchange allowance.** UF/DF raises aggregate within its NOR. The one-sided 95 % single-run bound of the
  rise is 0.104 points. It now tightens the cation exchange pool criterion to 4.90 % (`iac_verification.csv`, the
  UF/DF row; `iac.csv`). Replace "the cation exchange criterion makes no allowance for that increase" and the 5.00 %
  statements with this, computed.
- **The second skid (PD-010-01, amended).** S-UFDF-UNI2 ran on EQ-TFF-188, which the qualification did not compare with
  EQ-TFF-142. The offsets of EQ-TFF-142 are applied to its results. This is accepted with argument: the skids share
  their design and membrane, and the offsets are small against the criteria. Say so, and drop the departure claim of
  §4.2 that the entry did not carry.
- **The A-Mab citation is p.114**, not p.86 (E11). The brief is corrected.

## B. The record
PD-010-02 to PD-010-07 are registered. Describe each in the discrepancy part and cite it where the text relies on it.
The factual-check departures marked "text only" (items 2, 4 to 9) are now covered by PD-010-02 to -06. Check that each
is cited. Put any departure still in neither register in your hand-back, for example run order, load pools, the batch
names and offset date, and the final-retentate comparison.

## C. Errors (factual check): resolve each as the file gives it
- E1: the data do not support two parameters moving together. §7.3 gives only the size an interaction would need.
- E3: drop "and in the formulation buffer", or refer to the residual.
- E4: describe the simulation as §3.5 does, each parameter drawn from N(set-point, NOR width/6), clipped to the range
  studied.
- E5: add the aggregate path of DEV-010-02, with the computed range of the offset when any one run is dropped.
- E6: objective (iii) is not met. Give one verdict.
- E7: quote "roughly exponentially".
- E8: name the runs behind 0.034 %.
- E9: rest acidic variants on deamidation, which raises them away from the limiting 18 % side, and on the integrated
  model, which has no UF/DF effect on them.
- E10: restore the qualifier "under the approach of Section 3.1".
- E12: cite A-Mab p.47 and p.57, or drop "and not by a release test".
- E13: S-UFDF-UNI2 is the third study. Name the two meant.
- E14: state the two reversals of Version 1.0.
- The minor items, each as listed.

## D. The content review
Resolve the content review's items as it gives them, unless section A or C overrides them:
- Q1, a physical cause with a direction;
- Q2, terms of art;
- Q3, filing sentences;
- Q5 items 1 to 11;
- Q6, machine-written passages;
- Q7, passages that cannot stand alone;
- the table and figure notes.
Q5 item 3 needs the PCMP-001 §7.7 KPP definition quoted, with "practically relevant" and the too-small clause. TMP
stays KPP. Its only measured effect is on aggregate, so argue the class as a judgement of practical relevance and name
it as one.

## E. Gate and report
- Gate with `check_render.py --render` (`.venv/bin/python`, venv on PATH).
- Render the pdf and the docx, and run `check_render` once more.
- Read the page image of every table you changed.
- Refresh `.claude/work/2026-10-08_01_rev2-campaign/PCR-010_ufdf.DRAFT.txt`.
- Report each item with where it was resolved, anything left and why, the passes, the page count, and any `<<NEEDS:>>`
  left (none). Do not commit.
