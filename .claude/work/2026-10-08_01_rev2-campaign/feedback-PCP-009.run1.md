# PCP-009 after review run 1 and the factual check: what to change (one revision, same author)

Inputs, in this folder: `feedback-plans-shared-2026-10-10.md` (ten corpus-level resolutions, read
first), `factual-PCP-009.md` (8 errors, each with its fix), `content-review-PCP-009.md`,
`data-state-2026-10-10.md`, and `procedures/PLAN-LESSONS.md` (rules 4, 8 and 10 changed today). PCMP-001
was re-rendered today (§7.5 rule 2 and the design-space statistic): re-read its §7.2 and §7.5 from
`pc_package/PCMP-001_master_plan.pdf`. Where this note gives a resolution, write to it. Otherwise resolve
each flag yourself and say in your report what you did. Every value stays computed and every deciding
word computed or asserted.

## A. The factual check
Resolve errors 1 to 8 as `factual-PCP-009.md` gives them:
1. Error 1: shared item 2 (the resolution in the factual file is the same).
2. Error 2: shared item 3.
3. Error 3: shared item 4.
4. Error 4: shared item 6. Change 4 names the Version 1.0 consequence it replaces: "Where a model fails
   these checks, the affected response will be reported descriptively and no range will be claimed from
   it."
5. Error 5: restore "If the qualification in §5.1 fails, the study cannot proceed." Then add one sentence:
   no output with a criterion at this step is compared at both scales, so the qualification decision of
   PCMP-001 §7.1 applies to none, and PCR-009 states how it reads the Version 1.0 success criterion.
6. Error 6: restore the Version 1.0 protein sampling wording ("the unspiked load and the unspiked
   filtrate pool"). Name the fragment sample under change 2, or leave it unstated.
7. Error 7: restore the four Version 1.0 expectations word for word. PCR-009 compares them with the data.
8. Error 8: "has no measured offset; the offset is unknown, not zero", as §5.1 and PCMP-001 §7.1 say.

## B. The content review (step-specific)
- **Q5 item 1, the NOR-propagated draw**: shared item 7. Neither set-point is the midpoint of its NOR
  (Table 6.1), so do not write that the draw spans the NOR as ±3 standard deviations. State the draw as
  PCMP-001 §6.4 defines it and stop there.
- **Q5 item 2, INV-002**: shared item 10.
- **Q5 item 3, the success criterion**: Version 1.0 text, keep; A5 above adds the sentence on how it reads.
- **Q5 item 4, XMuLV retained completely**: Version 1.0 text. A censored result has no scatter, so the
  report meets the tension. The plan adds no rule.
- **Q5 item 5, the integrity test**: Version 1.0 compares flux decay, step yield and the post-use
  integrity test result. Keep the sentence. If Table 5.1 is built from the record and so omits the
  integrity test, either build it from the planned list or say in its caption that it lists the outputs
  carried to manufacturing scale under PCMP-001 §7.1; it must not contradict the sentence.
- **Execution record (shared item 9)**: say once, in the past tense, which studies ran when and that the
  record names no instrumented system for them. Drop "Every run of both designs has an nrCE-SDS result
  for fragments, and aggregate was not ..." from Materials and methods and from the Table 5.3 footnote
  (PCR-009's).
- **Q4, conditions 5 and 6**: say that they are Version 1.0 rules kept, and name them (the normal
  quantile plot of the residuals; the residual standard error against the distance to the criterion).
  Version 1.0 set no threshold for either: say so once and leave the approach to PCR-009.
- **Terms (Q2)**: keep the parameter name "Filtration volume (load)" (config and A-Mab), and say once that
  it is the volume filtered per square metre of membrane. Define "NOR-propagated analysis" at first use.
  "Flux decay at the maximum volumetric load" in Table 5.1.
- **The coded levels in Appendix A** ("the low edge, the midpoint and the high end") are Version 1.0 text:
  keep them as Version 1.0 wrote them, and add nothing about the design centre or coded 0 anywhere else
  (registered discrepancy D-001, your brief §5c). Keep the D-001 sentence as §5c gives it.
- **Glosses (Q3), restatement and padding (Q6), codes and stand-ins (Q7)**: fix each flagged sentence.
  Say each fact once (the qualification timing, fragments ≤ the criterion, "Fragments are judged on
  nrCE-SDS results only", the fragment mechanism, the screening and response-surface roles), name the
  verification of platform worst cases at the other steps, and give "It was assigned by rule" a subject.
- **Tables**: fix what your setup chunk builds (Tables 5.1, 5.3, 6.1 and 6.2 constant columns, A.1 and B.1
  run-type labels). Leave the shared builders as they are: their findings go to the consistency sweep.

## C. Gate and report
Gate with `check_render.py --render`, render the pdf and the docx, read the page image of every table you
changed, and refresh `PCP-009_virus_filtration.DRAFT.txt` with `pdftotext -layout`. Confirm the D-001
sentence of §5c is in the rendered text verbatim. Report each item with where it was resolved, the flags
you left and why, the check_render passes, the page count, and any `<<NEEDS:>>` left (none).
