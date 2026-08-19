# Review before promotion — the content questions, asked of a finished draft

Runs at the annex step of `authoring/RUNNER.md` (step 5), BEFORE a draft is promoted from
`<DOC>_<uokey>.DRAFT.qmd` to the shipped file. Written 2026-08-19 (TASK-010).

## Who answers

A reader who has read neither `authoring/WRITING_GUIDE.md` nor any measure of the draft: a fresh-
context agent (any capable model; record which) given exactly two things — the **Content** block
of `authoring/REVIEW_CHECKLIST.md` and the rendered text of the draft (the PDF, so inline
expressions read as numbers) — or the project owner. Not the author, and not the session that
talked to the author. Freshness matters: on 2026-08-18 the annex reviewer, working in the
authoring session, selected a hollow warrant as the canonical `mechanistic_warrant` span
(`docs/results/2026-08-18-track-d-stopped.md` §5.6).

## The prompt, verbatim

> Read the attached document. Answer four questions about it, sentence by sentence, quoting each
> sentence you flag exactly as it appears and saying which question it fails and why in one line.
> Then answer each question yes or no for the document as a whole.
>
> 1. Does every "because", "since", "governs", "sets", "acts on" or "acts through" name a physical
>    cause — a species, an interaction, a property of the resin, the buffer or the culture, and a
>    direction — in the clause where the verb stands, and not only in a clause that follows a
>    colon or in the next sentence?
> 2. Is every technical term a term of art in the chromatography, cell-culture or virology
>    literature?
> 3. Can each sentence in a mechanism paragraph be disagreed with on its own?
> 4. Does any sentence tell the reader how to file the finding it has just stated (a trailing
>    clause that renames the finding as a category, or a causal gloss that answers an objection
>    nobody raised)?
>
> Report: which model you are; the flagged sentences grouped by question; the four yes/no answers.

## What is filed

`<unit>/content-review-<DOC>-<date>.md`: the judge's report verbatim, the model, and the
disposition — promoted, or returned to the author with the flagged sentences as what the section
lacks (never as a phrase to insert). A draft is promoted only when the four read yes, or when
each no has been answered by the author in the same context and the judge re-run reads yes.

## Calibration

`content-review-calibration.md` in work unit `2026-08-18_03_author-facing-apparatus` is the
first run, on the shipped `PCR-005` Results subsections (a known-bad text: eight owner-quoted
sentences) and on the probe the owner preferred. The shipped text must be flagged on question 4
at least on the sentences the owner quoted, or the questions are reworded and the run repeated.
