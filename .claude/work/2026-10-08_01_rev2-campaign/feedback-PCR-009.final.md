# PCR-009 final pass: the readability review (one pass)

Input: `content-review-PCR-009.md` (in this folder), the medium-effort readability review of the draft after fix pass
1. Read it, `status-PCR-009.md`, `data-state-2026-10-11.md` and `procedures/REPORT-LESSONS.md` §6 and §7. The file is
`pc_package/PCR-009_virus_filtration.DRAFT.qmd`. Every value stays computed and every deciding word computed or
asserted. Rewrite flagged sentences in plain words. Do not add new claims. This is the last pass before promotion.

## Config changed under you (re-render to pick it up)
A register reason that only repeated the finding, "not entered in the study record" or "… qualification record", now
reads "the record gives no reason". Do not restate a reason the register does not give.

## Resolve as follows
- **Q1, causes.** Name the mechanism and its direction in the clause that has the verb. As the volume filtered per
  square metre rises, the membrane fouls, and the flow shifts to the larger pores, so retention of the small virus
  falls. Pressure raises the flux. Give the direction where you write "sets", "governs" or "bounds". In §2.1, say what
  the platform experience gives (the expected direction of each effect) without "sets". Make the interaction
  expectation of PCP-009 §4.3 follow from what is stated, or quote the plan's expectation as the plan's.
- **Q2, terms.** The corpus terms stay, because PCMP-001 uses them: least favourable NOR combination, single-run
  limit, NOR-propagated PAR, limit on overfitting, criterion on residuals and influential runs. Define each in plain
  words on first use. Then:
  - write "intercept-only model" for "model with no term";
  - write "the LRF claimed for this step" for "the claim of this step";
  - write "the CQA register" for "the register";
  - name the Version 1.0 conditions (normal residuals, and the residual SD against the distance to the criterion);
  - write "statistic that decides the verdict" for "statistic of judgement".
- **Q3 and Q6.** Remove the filing glosses and the answers to objections nobody raised. State a repeated statement
  once, where it belongs. This covers the Version 1.0 post-use claim, which appears four times, and "step yield has no
  criterion". The PD-009 paragraphs should add to Table 13.2, not restate it. Rewrite the circular PD-009-01 sentence
  so it says what was compared and what stayed the same.
- **Q4.**
  - Give the basis of the cumulative requirements (≥ 8.6 and ≥ 16.7 log10) as the document that sets them states it.
    Pull it through the brief or the helpers. If the record gives no basis, cite the document that sets them.
  - For fragments, say that the sponsor set the 2.00 % criterion and that A-Mab gives no fragment limit (A-Mab Table
    2.2 p.30, Table 2.29 p.56). Do not invent a basis.
- **Q5.1, integrity tests.** A post-use integrity test of a parvovirus filter is designed to detect a loss of
  small-virus retention. MVM retention depends on integrity at least as much as XMuLV retention does. Correct §10,
  §11 and the PD-009-04 text.
- **Q5.2.** Pressure raises the flux although it compacts the fouling layer, which raises its resistance. Correct the
  cause.
- **Q5.3, step yield.** A fixed hold-up is a smaller share of a larger load, so yield rises with load unless the loss
  in the fouling layer grows faster. Make the expectation follow from the mechanism, and compare it with the data.
- **Q5.4.** The interaction model's fit statistics are optimistic because four parameters are fitted to five distinct
  points. Rewrite the reason.
- **Q5.5.** Table 13.1 prints "run retained in the analysis" from the shared builder. The narrative must say that
  every run made on the lot was retained, as Version 1.0 recorded. The builder wording is on the sweep list. Leave
  the table.
- **Q5.6.** Use the residual SD of the model (Table 5.5), which sets the standard errors, in the detection argument.
- **Q5.7.** Label the limit at the least favourable NOR combination exactly as the helper computes it. Check
  `D.decision_statistic` and the interval's sidedness and confidence. If it is the lower end of a two-sided 95 %
  interval, say "two-sided 95 %" or "one-sided 97.5 %". Do not change the statistic.
- **Q5.8.** Recompute the centre-point SDs of Table 5.1 from unrounded data. If the table is right, leave it.
- **Q5.9.** Judge the pressure excursion against the run's own set pressure, not the NOR.
- **Q7.** Name what each code stands for in the same sentence:
  - the adequacy criteria, as F-test, lack of fit, limit on overfitting, and residuals and influential runs;
  - run 5, as the run at 50 L/m2 and 19 psi with the highest LRF, in Conclusion 7;
  - CA3, as the model selection;
  - the analyses of PD-009-07, in the executive summary;
  - what PCP-009 §7 requires, in Conclusion 1.
  Rewrite the abstract subjects ("The conclusions on the PARs moved", "That bounds…", "The boundary rests on single
  runs") so that the subject is what was done or found, with the values.
- **D-001 stays as registered.**

## Gate and report
- Gate with `check_render.py --render`.
- Render the pdf and the docx, and run `check_render` once more.
- Read the page image of every table you changed.
- Refresh `PCR-009_virus_filtration.DRAFT.txt` with `pdftotext -layout`.
- Append a "Final pass" section to `status-PCR-009.md`.
- Hand back each item with where it was resolved, anything left and why, the page count, and builder issues. Do not
  commit.
