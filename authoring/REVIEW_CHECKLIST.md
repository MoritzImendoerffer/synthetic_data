# Review checklist — questions a reviewer asks of a finished section

**Who reads this: a reviewer, after the draft exists. Never the author, before.** These were the
"rigor obligations" and "scaffolds" that `authoring/section_plan.yaml` assigned to each section
until 2026-08-19, and the author was told to perform them. Measured on 2026-08-18, each of the
eight sentences the project owner rejected in `PCR-005` was one of those obligations being
performed — "is put to no other use in this report" is *explicit_non_claim* discharged in a
sentence; "follow from the physical chemistry … and confirm the expectations recorded in §2.1" is
the instruction "establish the mechanistic expectation now so Results can confirm", verbatim.
On 2026-08-19 the same section written with no obligations at all was preferred blind
(`docs/results/2026-08-19-apparatus-probe.md`). So the obligations moved here, rephrased as
questions, and the answer to each is a fact about the finished text: yes or no, with the
sentence that shows it.

How to use it: read the section, then answer the questions that apply to it. A "no" is a
finding for the author, stated as what the section lacks — not as a phrase to insert. The
register gate (`check_style.py`) and the reviewer's table (`check_style.py --review`) are
separate; this file is about what the text commits to, not how it is shaped.

## The whole document

| question | shows itself as |
|---|---|
| Does the executive summary state the outcome of the whole document, so a reader who stops there knows the resolution? | the classes, the CQAs set or cleared, the capability and its margin, the deviations, all in the first page |
| Does the document open wide (product, step, basis), narrow to the studies, and widen again (control strategy, discussion, conclusions)? | the section order, and an opening paragraph in each part that says where the reader is |
| Does every number trace to the model? | no typed set-point, range, effect, p-value or Cpk anywhere in the prose (`check_render.py` numeral lint) |
| Is the same thing called the same name throughout, with explicit cross-references ("see §7") rather than restatements? | one name per attribute, parameter and study; no paraphrased repeat of a claim |

## Per section

| question | applies to | shows itself as |
|---|---|---|
| Does the section state its finding before its evidence, and does each paragraph open on its point? | every section | the first sentence of the section and of each paragraph is the claim, and the table or effect follows it |
| Where a table is introduced, does the text say which rows matter and why, and what follows from them? | any section with a table | the notable rows named in the prose, the conclusion after them; a bare `@tbl-x` with nothing said about it is the failure |
| Does the text say that the screening design identifies effects and the response-surface model is the predictive one, and does it stop short of claiming prediction from a near-saturated screening fit? | Results; Study design; the master plan's statistical approach | the framing sentence present once, and no design-space claim resting on the screening model |
| Does every design-space, PAR or capability claim say what it covers — the ranges studied, what the model does and does not cover, and the scale-down assumption? | Design space; PARs; Capability; Conclusions; Executive summary | at least two of range / model / assumption bounds beside the claim; an unbounded robustness claim is the failure |
| Does the verb match the evidence? "demonstrates" only for a strong effect with a tight interval; "is consistent with" or "suggests" for a small or non-significant one; near-limit noise attributed to the assay | Results; Discussion; Materials and methods | the strength of the verb against the p-value and interval next to it |
| Where a result was worse than expected, is the adverse magnitude stated first, then the mitigating evidence, then the residual position? | Results; Deviations; Discussion; the transfer plan's gap analysis | the number that went wrong in the first sentence, not the reassurance |
| Where an attribute is controlled by more than one step, does the text state this step's contribution and name the documents for the others? | Executive summary; Prior knowledge; Capability; Control strategy; the master report | the other documents named by ID; "the step controls X" with no other step named is the failure when X is shared |
| Does every deferral name a location? | Materials and methods; Deviations; wherever data are not shown | an appendix, a paired report, an SOP or an AMV in place of "data not shown" |
| Is a factor with no significant effect classified and kept as evidence of robustness, with the evidence stated? | Parameter classification; Results | the null factor's class and the size of the interval that bounds its effect |
| Is the capability stated as the Cpk and the margin to the limit, and is the tightest one named? | Capability; Executive summary; Conclusions | the Cpk, the margin, and the words "the tightest" beside one attribute |
| Does the section say what the step does not do or does not by itself guarantee? | Executive summary; Control strategy; Conclusions | one plain sentence of scope; a sentence written only to discharge this question ("is put to no other use in this report") is the opposite of the intent |
| Is the worst-case corner the region must still satisfy named? | Design space; PARs | the corner's settings and its predicted response against the limit |
| Is the range of each factor justified, not only its presence? | Prior knowledge; Study design | the reason for the edges — platform history, the RA-001 score, the mechanism — next to each range |
| Where the text gives a mechanism, does it name a physical cause — which species, which interaction, which property of the resin, the buffer or the culture, and in which direction it acts? | Prior knowledge; Results (mechanistic interpretation); Discussion | a cause a chemist could dispute; "acts through the capacity of the bed", "behaves as a resin property", "the physical chemistry of affinity capture" name a category and are the failure |

## Content — what a sentence commits to

Added 2026-08-19 (TASK-010). Everything above is about whether a section carries what it should.
These four are about whether a sentence says anything, and no counter can answer them. They are
answered by a reader of the finished text who has read neither the writing guide nor any measure
of the draft: a fresh-context agent given only this block and the text, or the project owner. Each
answer is yes or no per sentence, with the sentence quoted. **A "no" on any of the four blocks
promotion** until the author has addressed it.

| # | question | a "no" looks like |
|---|---|---|
| 1 | Does every `because`, `since`, `governs`, `sets`, `acts on / through` name a physical cause — a species, an interaction, a property of the resin, the buffer or the culture, and a direction — **in the clause where the verb stands**, and not only in a clause that follows a colon or in the next sentence? | "governs pool host cell protein because it sets the aggressiveness of desorption"; "acts through the capacity of the bed"; "follows from the physical chemistry of affinity capture" |
| 2 | Is every technical term a term of art in the chromatography, cell-culture or virology literature? | "aggressiveness of desorption"; "resin property" used for a process; "parameter of a single run" for "operating parameter" |
| 3 | Can each sentence in a mechanism paragraph be disagreed with on its own? | a sentence that stacks a claim, a cause, a list and an inference so that no part can be denied without the rest |
| 4 | Does any sentence tell the reader how to file the finding it has just stated? | a trailing clause that renames the finding as a category ("…, which is the curvature a two-level design cannot see"; "…, which is the interaction already seen in Table 5.8"); a causal gloss that answers an objection nobody raised |

How it is run: `procedures/REVIEW-BEFORE-PROMOTION.md` in the active work unit (the annex step
of `authoring/RUNNER.md`, step 5) — the judge is given this block and the rendered text and
nothing else, its answers are filed in the work unit beside the draft, and the draft is promoted
only when the four read yes or the author has answered each no.
