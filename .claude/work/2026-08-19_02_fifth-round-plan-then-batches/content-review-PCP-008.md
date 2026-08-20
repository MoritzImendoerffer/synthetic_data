# Content review of the PCP-008 draft — before promotion

**2026-08-20, TASK-022 §4.** Batch B3, authored under the amended rule 4. §5c assigns **D-001**.
Two fresh judges (`opus`), one return between them.

## Counts per question

| run | Q1 | Q2 | Q3 | Q4 | verdicts |
|---|---|---|---|---|---|
| 1 (as authored) | 4 real + 7 registry | 0 | 2 (+1 borderline) | 6 (+2 borderline) | No · **Yes** · No · Yes |
| 2 (after one cycle) | 3 deferrals + 5 registry | 1 | 0 (1 borderline) | 5 | No · No · **Yes** · Yes |

Q3 passes after the cycle. Q1's real failures fell from four to three deferrals.

## The two judges disagree on one term, which is worth recording

Run 1 answered **Yes** to Q2, listing "assurance margin" among four procedural coinages and
holding that "each is defined in place and none is invented pseudo-science". Run 2 answered
**No** on that single term: "'assurance margin' is not a term of art (the field says safety factor
or safety margin), and it is neither defined nor given a value anywhere in the plan."

Both read the same document. The disagreement is about whether the surrounding sentence counts as
a definition, and it is the clearest case in this campaign of the review's verdict depending on the
judge rather than on the text. `PCP-006`'s author, given the same flag, replaced the term with "a
safety factor"; `PCP-008`'s kept it, because its run-1 judge had passed it. **The batch is now
inconsistent on this term across documents**, which no single-document review can see.

## The author's refusal, which was correct

The return carried run 1's seven "registry" Q1 flags — "the step *sets* an attribute", "a parameter
that *acts on* a CQA". The author declined to change them and said why: they are this corpus's
fixed vocabulary for the step-to-attribute relation, rule 5 of `WRITING_GUIDE.md` requires one name
per thing, and the judge itself had marked them category labels rather than mechanism claims. Run 2
flagged the same construction again, which is expected — the question has no scope line — and the
refusal still stands.

## What the return fixed

The four real Q1 failures: "set by the mechanism" deleted (the four sentences after it already
named the causes); the quadratic-terms sentence now puts the physics in the because-clause (net
charge changes most steeply near the isoelectric point); the §4.1 "expected to set the clearance"
sentence replaced by two directional sentences closing on "push the same binding equilibrium in
opposite directions"; and the method-precision sentence replaced by the actual relation. Seven
filing clauses and both borderlines cut.

**A toolchain trap, caught by the author and worth recording.** Re-wrapping an edited paragraph
split an inline expression across a newline (`` `{python}\nf"{acc_hcp[1]:.3g}"` ``). Quarto's inline
regex does not cross newlines, so it would have rendered as literal source text in the PDF.
`check_render` caught it only through the expression count, 28 against 29. Repaired, and the
rendered PDF verified to contain zero `python}` literals. A corpus-wide check confirmed no shipped
PDF carries this defect.

## Findings not acted on

Run 2 raised one mechanism point outside the four questions: "The parvovirus model has no envelope
and is small, and its capsid is acidic at the load pH, so it binds by that mechanism as well." —
the absence of an envelope and the small size bear on filtration and on low-pH inactivation, not on
charge-based binding to a quaternary amine ligand. Only the acidic capsid clause does work.

**D-001 is intact**, verified in the rendered PDF after the revision, wording and strength
unchanged and nothing added that reconciles it.
