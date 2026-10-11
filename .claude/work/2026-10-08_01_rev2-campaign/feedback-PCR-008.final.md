# PCR-008 final pass: the readability review (one pass)

Input: `content-review-PCR-008.md` (in this folder), the medium-effort readability review of the draft after fix pass
1. Read it, `status-PCR-008.md`, `data-state-2026-10-11.md` and `procedures/REPORT-LESSONS.md` §6 and §7. The file is
`pc_package/PCR-008_aex.DRAFT.qmd`. Every value stays computed and every deciding word computed or asserted. Rewrite
flagged sentences in plain words. Do not add new claims beyond those below. This is the last pass before promotion.

## Config changed under you (re-render)
A register reason that only repeated the finding now reads "the record gives no reason". Do not restate a reason the
register does not give.

## Resolve as follows
- **Q5.2 and Q5.3, DEV-008-02.**
  - The record gives 180 mAU against a corrected 120 mAU, and calls the set-point "permissive". On a falling trailing
    edge, a higher stop value ends collection earlier, so less of the trailing tail was pooled. State the direction
    plainly from the values. Use "permissive" only as the record's own word, in quotes.
  - Replace "cannot have created or hidden an effect" with what the data show. A fixed UV cut can remove a different
    share of the tail at different pH and conductivity. The block term (p = 0.526) detected no shift between the
    executions. Say that, and no more.
- **Q5.1, the edge in Table 7.3.** If the builder rounds edges inward (a lower edge rounds up), say so in the table
    note and use the unrounded edge in the text. Change §5.3.4 to match.
- **Q5.5, protein load WC-CPP.** Keep the class. Make the reasoning consistent with §5.3.2 and §3.5.2:
  - the selected model carries the protein load interaction;
  - models within 2 AICc units drop it, so it is not established as an effect;
  - the class is a conservative judgement on that term, and is named as one.
- **Q4, the completion rule.** State what PCP-008 §7 item 8 requires, and report against it, met or not met, from the
    record. If the record cannot show it, say so. PD-008-08 covers it.
- **Q4, the margin between each NOR and its PAR.** State it for every parameter you call well controlled, protein
  load and flow rate included, computed.
- **Q5.4.** For viral clearance, the flow-rate claim rests on one spiked run at 450 cm/hr. Limit §5.4 as §7.4 does.
- **Q5.6.** Say which model gives 5.40 and 0.824 beside the table values from the other model, so the reader sees two
  models.
- **Q5.7.** Name each upper limit exactly as its helper computes it. The 29.4 ng/mg is the upper end of a two-sided
  95 % interval, a one-sided 97.5 % limit. The 4.18 is a one-sided 95 % bound.
- **Q5.9, residual DNA.** The criterion of ≤ 0.001 ng/dose is A-Mab's claimed acceptable range (A-Mab Table 2.17,
  pp. 47–48), set far below the WHO 10 ng/dose that A-Mab cites. State that basis once. It is not an error.
- **Q5.10, the ELISA coverage.** Say that the 20 % of host cell protein species the ELISA does not detect are not seen
  by release testing either. Say how the clearance argument covers them, from what the record and the brief give. If
  nothing covers them, say so.
- **Q5.11.** The executive summary must name the protein load term in the XMuLV model.
- **Q5.8 and Q5.12.** Leave Table 2.1 (builder, footnote explains). Recompute 0.03 from unrounded values. If it holds,
  leave it.
- **Q1.**
  - Name the physical reason the plan expected an interaction, or quote it as the plan's expectation.
  - Fragments flow through because they carry the antibody's positive charge at the load pH.
  - Correct "small, highly charged impurities", and say that virus is the species §2.1 expects to respond to flow rate.
  - Name slow diffusion of virus particles to the ligand in §9.
  - Describe the set-point cause by its direction.
- **Q2.** Define the corpus terms on first use in plain words, as in PCMP-001: NOR-propagated range, platform worst
  case, single-run limit, study event. Then:
  - write "within 2 AICc units" for "near-equivalent";
  - write "absolute-residual regression" or similar for "spread p/regression" in your prose (Table 5.4 is a builder);
  - write "decision statistic" for "deciding statistic";
  - drop "governed quality attribute".
- **Q3 and Q6.** Remove the filing glosses ("which decides", "None of them decides an acceptance", "serve no other
  purpose") and the restatements listed. The PD-008 paragraphs after Table 13.2 should add to the table, not repeat
  it. Fix the garbled spiking sentence of §3.1. Say whether the centre-point SDs are larger or smaller than the assay
  repeatability.
- **Q7.** Name what each code stands for in the same sentence:
  - INV-001 and INV-002, by what each found;
  - the augmentation decided by the model adequacy investigation;
  - the DEV-008-03 run, as the screening run with the buffer below its pH range;
  - AMD-001, as the method decision for fragments by nrCE-SDS;
  - the F-test criterion;
  - the widening rule of the master plan.
  Rewrite "What it changed was computed" and the unclear §7.5 phrase about the runs on which the criteria were fixed.
- **D-001 stays as registered.** The coding paragraph never mentions the "PAR (set-point)" column.

## Gate and report
- Gate with `check_render.py --render`.
- Render the pdf and the docx, and run `check_render` once more.
- Read the page image of every table you changed.
- Refresh `PCR-008_aex.DRAFT.txt` with `pdftotext -layout`.
- Append a "Final pass" section to `status-PCR-008.md`.
- Hand back each item with where it was resolved, anything left and why, the page count, and builder issues. Do not
  commit.
