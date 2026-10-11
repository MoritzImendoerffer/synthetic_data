# PCR-007 final pass: the readability review (one pass)

Input: `content-review-PCR-007.md` (in this folder), the medium-effort readability review of the draft after fix pass
1. Read it, `status-PCR-007.md`, `data-state-2026-10-11.md` and `procedures/REPORT-LESSONS.md` §6 and §7. The file is
`pc_package/PCR-007_cex.DRAFT.qmd`. Every value stays computed and every deciding word computed or asserted. Rewrite
flagged sentences in plain words. Do not add new claims beyond those below. This is the last pass before promotion.

## Config changed under you (re-render)
A register reason that only repeated the finding now reads "the record gives no reason". Do not restate a reason the
register does not give. The reasons of PD-007-02 and PD-007-03 come from the register. Leave them, and do not repeat
them in your prose (Q5.10, Q6).

## Resolve as follows
- **Q5.5, verify first.** "With run 14 deleted the selection keeps a stop collect term of −0.76 … (p = 0.078)" has the
  same values as the conductivity term in Table C.2. Recompute the deletion with the helpers. Print what the
  computation gives, assert it, and correct §5.3.6, §11 and Conclusion 7 if the term or its values differ.
- **Q5.1, the buffer at pH 5.02.** The record (config) names the lot "Tris load/wash buffer", and Tris does not buffer
  at pH 5. This is a record problem for the coordinator. In your own prose, say "the load/wash buffer lot" and do not
  name the species. The event table prints the record as it is.
- **Q5.2, host cell protein and pI.** At the load pH, host cell proteins with an isoelectric point below it carry a
  net negative charge and flow through. Those above it bind with the antibody and are separated in the wash and the
  elution. Do not claim that most host cell proteins have a pI below the load pH.
- **Q5.3, §10.** Correct which steps control what. Low-pH inactivation inactivates enveloped virus. Anion exchange
  clears host cell protein, DNA, leached Protein A and virus. Virus filtration removes virus. Follow §1.1 and the
  brief.
- **Q5.4 and Q4, the objectives.** Give a verdict, met or not met, for each objective in Section 12. Objective 2 is not
  met for fragments, which have no adequate model, and objective 3 is not met for fragments either. Make Conclusions 2
  and 3 agree.
- **Q4, §13.1.2.**
  - Give the result of the run-14 aggregate verification beside its confidence interval, and say what it was judged
    against, as the record gives it.
  - Give the temperature set-point and the permitted range from the record. If the record has none, say so.
- **Q5.6.** The lot expired after it was prepared. The missing check was at the time of use. Say what the record says
  as the record's cause, and correct the logic of your own sentence.
- **Q5.7.** The PAR is the range studied, so the margin is exactly that distance. Drop "at least".
- **Q5.8.** The figure captions must give yield in % as the tables do. If the figure builder plots a fraction, fix the
  caption only. Put the builder issue in your hand-back.
- **Q5.9, residual DNA.** The criterion of ≤ 0.001 ng/dose is A-Mab's claimed acceptable range (A-Mab Table 2.17,
  pp. 47–48), set far below the WHO 10 ng/dose that A-Mab cites. State this basis once. It is not an error.
- **Q5.11.** Say which run set gives the bound in force, and give both values if they differ.
- **Q1.**
  - Name the physical cause in each flagged clause. Ionic strength at load and wash does not change the relative
    charge of aggregate and monomer at the elution pH. Load conductivity also acts on binding during loading.
  - pH changes the charge of the antibody, and so the position and width of the peak. It does not move a cut point.
  - Elution flow rate acts through residence time and mass transfer.
  - Replace "govern" and "follow the physical chemistry" with the cause and the direction.
- **Q2.** Define the corpus terms on first use in plain words, as in PCMP-001: NOR-propagated range, single-run limit,
  criterion in force, a priori criterion, limit on overfitting, study event. Then:
  - write "within 2 AICc units" for "near-equivalent";
  - write "compared with the median of F(p, n − p)" for "F median" in your prose;
  - write "will be followed up in" or name the follow-up for "managed forward".
- **Q3 and Q6.** Remove the filing glosses and the restatements listed. These include "These are sensitivities, and
  the selected model decides", "named as a judgement", "The step contributes to every attribute", "Five limitations
  remain, and each is managed forward", and the tautologies about feed lots. Name the judgement once in §9. "Roll up
  into PCMR-001" goes once, in §10. State "residual DNA has no criterion, so no conclusion depends on its offset"
  once.
- **Q7.** Name what each code stands for in the same sentence:
  - the comparison of §3.5.1 item 5, as the difference between the two ends with its 95 % CI against the smallest
    significant screening effect;
  - the rule of PCP-007 §7.6;
  - runs 6 and 14, as the expired-lot run and the temperature-excursion run;
  - the two study events;
  - S-CEX-VER and S-VI-WC, by what they tested;
  - the rule of §4.3.
  Rewrite "the trend is bounded over the NOR by its size" with the drift and its values.
- **D-001 stays as registered.**

## Gate and report
- Gate with `check_render.py --render`.
- Render the pdf and the docx, and run `check_render` once more.
- Read the page image of every table you changed.
- Refresh `PCR-007_cex.DRAFT.txt` with `pdftotext -layout`.
- Append a "Final pass" section to `status-PCR-007.md`.
- Hand back each item with where it was resolved, anything left and why, the page count, and builder issues. Do not
  commit.
