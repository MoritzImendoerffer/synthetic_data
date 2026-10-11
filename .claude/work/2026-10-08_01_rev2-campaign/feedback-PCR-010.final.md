# PCR-010 final pass: the readability review (one pass)

Input: `content-review-PCR-010.run2.md` (in this folder), the medium-effort readability review of the draft after fix
pass 1. Read it, `status-PCR-010.md`, `data-state-2026-10-11.md` and `procedures/REPORT-LESSONS.md` §6 and §7. The file
is `pc_package/PCR-010_ufdf.DRAFT.qmd`. Every value stays computed and every deciding word computed or asserted.
Rewrite flagged sentences in plain words. Do not add new claims beyond those below. This is the last pass before
promotion.

## Config and brief changed under you (re-render; regenerate the brief)
- **PD-010-08 (new).** Aggregate verified at UF/DF on S-UFDF-UNI2, by a main-effects fit evaluated at the least
  favourable NOR combination (PCMP-001 Version 2.0 §7.5). PCP-010 §7.2 says no verification is planned at this step.
  Cite it in §7.1 and describe it in §13.2. Your setup assertion that the register holds PD-010-01 to -07 must now
  hold -08.
- **PD-010-07 reason** now reads "each further diavolume lowers the residual process buffer further". It no longer says
  "only lowers".
- **Register reasons.** A reason that only repeated the finding now reads "the record gives no reason".
- **The brief** now names the verification as the one exception to "judge each response on its slope".

## Resolve as follows
- **Q5.1, "a further diavolume only lowers".** It conflicts with §2.1 and §4.1: more diavolumes also mean more time
  and more pump passes. Say once that more diavolumes lower the residual process buffer further. Also say that they
  add pump passes, which could raise aggregate, and give the measured diavolume slope for aggregate. Drop the
  repetitions.
- **Q5.7, the one-sided NOR in the simulation and the combinations.** Describe what the engine does
  (`amab_process/studies.py` `_sample_overrides`, `amab_process/iac.py` `_univariate_increase`, read only).
  Diavolumes are drawn around the set-point with the SD of the 7–9 DV range and never below 7 DV. In the least
  favourable combination their upper value is 9 DV. Pull both values from the config through the helpers. Say this
  in §3.5 and §7.1.
- **Q5.3, the classes of TMP and final concentration.**
  - Both have a significant effect on aggregate, a CQA.
  - Quote the PCMP-001 §7.7 rule once. A parameter with an effect on a CQA is a CPP unless the effect is too small to
    be practically relevant.
  - Give each class with its numbers: the change across the NOR against the margin to the criterion.
  - Say that the effect is carried in the 0.104-point bound behind the cation exchange criterion.
  - Say that the effect of TMP on flux was not measured across the range (Table 9.1).
  - Name the class as a judgement once. Keep the classes.
- **Q5.2, the TMP mechanism.** Above the limiting flux, the wall concentration stays at its limiting value. A higher
  TMP compacts and thickens the polarization layer, with no gain in flux. Correct the premise. Say that the aggregate
  effect of high concentration and TMP is this campaign's own addition to the process model, as the brief states.
- **Q5.4, §7.2.** Say that the §7.2 criteria apply to response-surface models, not to the univariate slopes. Then say
  that the main-effects fit used for the verification is judged on the first three §7.2 criteria. PCMP-001 §7.5
  requires this of a model whose bound replaces a platform value.
- **Q5.5, residual DNA.** The criterion of ≤ 0.001 ng/dose is A-Mab's claimed acceptable range (A-Mab Table 2.17,
  pp. 47–48). It is not an error. Say that the drug substance level is a computation from the clearance credited to
  the steps, not a measured result, and that it lies far below what a residual DNA assay can quantify.
- **Q5.6, acidic variants.** The PCMP-001 §7.3 assumption that no step after low-pH inactivation changes acidic
  variants ignores deamidation on the skid, which raises them. Say so plainly. The rise moves acidic variants away
  from the lower 18 % limit, which is the limiting side, so the assumption errs on the safe side for that limit.
- **Q4, last item.** Report the acidic-variant Cpk as the integrated model gives it, and the 0.63 at the study mean,
  without the word "acceptable".
- **Q1.**
  - Give how TMP and concentration act on the polarization layer, in the clause itself.
  - The aggregate offset was measured at the set-point only. Say that it is assumed constant across settings.
  - Say how the hold-up lowered the final concentration, if the record says. If it does not, say that.
  - In §9, give the numbers in place of the restated rule.
- **Q2.**
  - "Residual process buffer": define it once and say what the record does and does not name.
  - "Allowance": say "the prediction bound of the aggregate rise across the step" on first use, then "the bound".
  - The event register's "topped up" comes from the record. In your prose, say "concentrated further".
- **Q3 and Q6.** Remove the "that is a judgement" glosses except one naming in §9. Remove the pre-emptive defences and
  the restatements listed.
- **Q7.** Name what each code or rule stands for in the same sentence:
  - the PCMP-001 §7.5 rule 1;
  - the PCP-010 §4.3 and §5.3 rules;
  - "the register", as the discrepancy entry named by what it accepts;
  - PD-010-03 and PD-010-04, by what is missing;
  - objective (iii), by what it asks;
  - "it" in the executive summary, the Cpk.
  Rewrite the abstract subjects so that the subject is what was done or found, with the value.
- **D-001 stays as registered.**

## Gate and report
- Gate with `check_render.py --render`.
- Render the pdf and the docx, and run `check_render` once more.
- Read the page image of every table you changed.
- Refresh `PCR-010_ufdf.DRAFT.txt` with `pdftotext -layout`.
- Append a "Final pass" section to `status-PCR-010.md`.
- Hand back each item with where it was resolved, anything left and why, the page count, and builder issues. Do not
  commit.
