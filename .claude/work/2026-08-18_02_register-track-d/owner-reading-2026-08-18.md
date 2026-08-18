# Project owner's reading of the pilot — 2026-08-18

Recorded VERBATIM and before any measure was taken of what it names, which is the order the
three previous rounds used and the order `decisions.human_check` fixes for this one. The counts
that follow it were produced afterwards, by `measure_trackd.py`.

## The reading, verbatim

> "The interaction of the two is significant at -1,900, reproducing the sign and roughly the
> magnitude estimated in the screening stage. The quadratic term in elution pH is significant at
> 1,944 (p = 0.0040), which is the curvature a two-level design cannot see" ...which is the
> curvature a two level design cannot see... is there a way to stop you from writing these weird
> formulations?; "because a non-significant screening estimate makes no claim about the sign" ...
> why should a screening estimate make a claim about a sign? "The contours are curved instead of
> parallel, which is the interaction and the pH curvature already seen in Table 5.8." ... again.
> Maybe just ban ", which is"? also a weird formulation "The leached Protein A model is retained
> as knowledge-space evidence and is put to no other use in this report."

## Provenance of the four quotes

All four are `PCR-005`, the re-authored Protein A report. Quote 1 is quoted from the rendered
PDF, where the inline expressions resolve to `-1,900`, `1,944` and `p = 0.0040`; the other three
are verbatim in the `.qmd` as well. No quote is from `PCP-007` or `RA-001`, the other two pilot
documents, and none is from `PCR-003`, the control.

## What the reading names

Three of the four are one syntactic move and one is not.

1. `, which is the curvature a two-level design cannot see` — a trailing relative clause that
   renames the finding just stated as an abstract noun.
2. `, which is the interaction and the pH curvature already seen in Table 5.8` — the same move,
   plus a back-reference.
3. `because a non-significant screening estimate makes no claim about the sign` — not a relative
   clause. A causal gloss that answers an objection nobody raised. The owner's question, "why
   should a screening estimate make a claim about a sign", is the point: the sentence invents a
   reader who thought it did.
4. `is put to no other use in this report` — neither. A periphrastic negation where "and is not
   used again" would do.

What unites all four is not a construction. It is the sentence explaining itself: the finding is
stated and then, inside the same sentence, the reader is told how to file it. A regex reaches the
two commonest carriers of that move. It does not reach the move.
