# PCR-004 final pass: the readability review (one pass)

Input: `content-review-PCR-004.md` (in this folder), the medium-effort readability review of the draft after fix pass
1 and the data-state pass. Read it, `status-PCR-004.md`, `data-state-2026-10-11.md` and
`procedures/REPORT-LESSONS.md` §6 and §7. The file is `pc_package/PCR-004_harvest.DRAFT.qmd`. Every value stays
computed and every deciding word computed or asserted. Rewrite flagged sentences in plain words. Do not add new
claims. This is the last pass before promotion.

## Config changed under you (re-render to pick it up)
- PD-004-01 no longer says the plan did not name residual DNA. It says "it measured fragments, which the plan did not
  name as a response" (review Q5.3). Make the text agree.
- A register reason that only repeated the finding, "not entered in the study record", now reads "the record gives no
  reason" (review Q6, first item). Do not restate a reason the register does not give.

## Resolve as follows
- **Q1, causes.** Name the mechanism and its direction in the clause that has the verb. For example, settling velocity
  rises with the centrifugal field, so less turbidity reaches the depth filter. For SEC, host cell protein co-elutes in
  the low molecular weight region. Rewrite "decide" in §5.7 and §1.1 the same way.
- **Q2, terms.**
  - "Resolution" of a method: give the quantity on first use, the smallest difference the method tells apart
    (2.77 × SD, the repeatability limit), and call it "repeatability limit" from then on.
  - "The reading of the change": say "the largest change from day 0".
  - "The full set-point": say "every parameter at set-point". Avoid "set-point centrate" in your own prose.
  - "a priori value": explain once, as the value carried back through the platform worst cases.
  - "Integrated model of the train": name it once as a Monte Carlo simulation through the step models.
  - The method titles in Table 3.1 come from the config. Leave them.
- **Q3 and Q6.** Remove the filing glosses and the answers to objections nobody raised. State a repeated statement
  once, where it belongs, and refer back in plain words elsewhere. This covers the approach chosen after the results,
  the held-pool rule, "no result of that study enters this report", "rests on S-HAR-UNI2", "roll up into PCMR-001" and
  the culture of the pool. Delete §3.3's sentence about a table with no rows, or drop the table if the canonical order
  allows.
- **Q4 and Q5.1, Table 7.1.** Its p-values must come from the primary error term, the set-point replicates (Table
  5.3). Say which error term it uses.
- **Q5.2, the turbidity PAR and the clarification criterion.** These answer two questions, and the text must keep them
  apart in one clear place:
  - Criterion 2 asks whether a harvest setting delivers clarified harvest within the turbidity NOR (10 NTU). A
    depth filter load that gives more has not clarified to the NOR, and that is why the load PAR stops at 140 L/m2.
  - The PAR of post-clarification turbidity, 1–20 NTU, is the range over which the turbidity challenge showed no
    effect on the attributes measured in the harvest. It does not cover Protein A performance, because the load
    challenge was not made (PD-004-05).
  - The basis of 10 NTU is the NOR, set from production. Say so, and do not present it as derived from Protein A
    fouling.
  - §10 monitors against the NOR.
- **Q5.4, fragments.** Rest "not by the field" on the data, the slope of fragments against rcf. Name disulfide
  reduction after cell lysis as a known harvest mechanism that would depend on lysis and shear. The data did not show
  it within the range studied.
- **Q5.5.** The process model's fragment rise over a one-day cold hold (+0.02) differs from the day-1 change in Table
  5.4 (+0.23). Explain the difference from the data, or do not set the two side by side.
- **Q5.6.** Use one definition of the hold change, the largest change from day 0, in the ratio too.
- **Q5.7, the hold claim of §10.**
  - Limit the claim to the attributes measured.
  - Say that the fragment level entering the hold is not the highest expected in routine manufacture (§3.5).
  - Say that bioburden and endotoxin were not part of the hold study, so a hold time in manufacturing needs that
    support as well.
- **Q5.8, residual DNA.** The criterion of ≤ 0.001 ng/dose is A-Mab's claimed acceptable range (A-Mab Table 2.17,
  pp. 47–48), far below the WHO 10 ng/dose that A-Mab cites. It is not an error. Replace "far from binding" with the
  computed margin (about 0.8 log10 against the clearance credited).
- **Q5.9, the GPP class of turbidity.** The effect on capture was not measured (PD-004-05). Name the class as a
  judgement, give its basis, and say it is not shown by the data. Do not change the class.
- **Q5.10.** Compute 78.7 from the same values as Table 5.2, or print the table's difference.
- **Q5.11.** A turbidity test detects, it does not protect. Name the action on a failed result if the record or the
  plan gives one. If neither does, say "detects".
- **Q7.** Name what each code stands for in the same sentence:
  - the two study events, by what happened;
  - objectives 4 and 5, by what they ask;
  - the studies, by what they are;
  - the discrepancies, by what each changed;
  - the source of 9.30 %;
  - the referent in §5.5.
  Rewrite the abstract subjects of §5.6 and §11 so that the subject is what was done or found.
- **D-001 stays as registered.**

## Gate and report
- Gate with `check_render.py --render`.
- Render the pdf and the docx, and run `check_render` once more.
- Read the page image of every table you changed.
- Refresh `PCR-004_harvest.DRAFT.txt` with `pdftotext -layout`.
- Append a "Final pass" section to `status-PCR-004.md`.
- Hand back each item with where it was resolved, anything left and why, the page count, and builder issues. Do not
  commit.
