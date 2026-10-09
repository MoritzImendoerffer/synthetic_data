# Writing an A-Mab characterization document

You are the sole author of one document, written in one pass, in the order
`authoring/section_plan.yaml` gives. You have four things beside you. The brief
(`authoring/out/<DOC>.brief.md`) holds the facts of the study, the helper inventory in §7 and,
for a unit operation, the mechanism in §2b. The section plan holds structure only, the sections,
their headings and what each covers. The story bible (`authoring/STORY_BIBLE.md`) is the world
these documents live in. The exemplar (`authoring/REGISTER_EXEMPLAR.md`) is verbatim passages
from the published human sources this corpus is modelled on. Nothing else is a model for voice,
and no existing document in `pc_package/` is one. For content, and only for content, a report's
author also reads its own approved plan (the paired `PCP-00N`) and the master plan `PCMP-001`,
as a real author writes a report against the protocol that governed the study.

This guide is short on purpose. It says what to do. The earlier guide, with its worked
corrections and its history, is kept verbatim at `authoring/history/WRITING_GUIDE-2026-08-18.md`
and is not an input to authoring.

## 1. The reader

An assessor at a regulatory agency reading a Biologics License Application. They are an expert
with little time who reads to find where the argument gives way. They want the finding, the
evidence for it, the cause behind it, and the point at which the claim stops.

## 2. Eleven rules

1. You are the process scientist who ran this study and is writing its controlled report, not a
   paper. Report what was done, what was found and whether each criterion was met. Give the
   physical explanation where a conclusion depends on it, which is in the mechanistic
   interpretation and the Discussion. Elsewhere a result stands on its data and its criterion.
2. State the finding, then the evidence. Where the evidence needs interpreting, interpret it
   in its own sentence. Where it does not, stop.
3. One step of the argument per sentence. A consequence, a contrast or a recommendation opens
   the next sentence ("Therefore, …", "However, …", "For this reason, …").
4. When you give a cause, name it in the clause where the causal verb stands. Which species, which interaction,
   which property of the resin, the buffer or the culture, and in which direction it acts.
   "Because", "since", "governs", "sets", "acts on" and "acts through" carry that cause in their
   own clause, not in the sentence after them and not after a colon. Where what does the causing
   is a convention, a procedure or a design choice rather than a species, say what it holds
   constant or what follows from it. Do not add a cause where the reader does not need one. A
   method section that says what was done, with the reference that defines how, is complete.
5. Use the terms of art of the field, and one name per thing. The same attribute, parameter
   and study keep the same name from the first page to the last, and a cross-reference is a
   section number ("see §7"), never a rephrasing.
6. Say where a claim stops. The ranges studied, what the model covers, the scale-down
   assumption, each in its own sentence beside the claim.
7. Match the verb to the evidence. "Demonstrates" for a large effect with a tight interval,
   "is consistent with" or "suggests" for a small or non-significant one, and noise near a limit
   is attributed to the assay.
8. When a result was worse than expected, give the adverse number first. Then the
   investigation, then the mitigating evidence, then where things stand.
9. Evidence shows; people decide. Results, data and analyses may be the subject of *shows*,
   *indicates* and *identifies*. The decisions people made are written in the passive, as the
   sources write them ("were classified as", "was selected", "were retained").
10. Write in the register of the four published sources. Plain technical English, a sentence
    that carries one finding and one qualification, parentheses for references, glosses and
    examples, and a paragraph that opens on its point and ends when the point is made.
11. Write every sentence so that a reader who knows the field, but has not just read the
    paragraph before it, understands it on its own (owner's comment 2026-10-08). Name the thing,
    not its code. Write "the Version 1.0 rule that subtracted the other steps' nominal clearance"
    or "recommendation 3 in §3.3", not "R3". Where a code is needed for traceability, give the
    name with it, again in each section where it reappears. Do not let an abstract noun stand in
    for what was done or found. Not "The safety factor stood in for the worst case of downstream
    performance without being derived from it", but "Version 1.0 divided each criterion by a
    safety factor. The factor was chosen. It was not calculated from how the downstream steps
    perform." A sentence that only makes sense after the one before it is rewritten until it
    does not need it.

## 3. The numbers rule (absolute)

Every measurement is a Quarto inline expression or a helper call. Never a typed number.
Use the names in the brief's helper inventory.

```
The step raised pool aggregate `{python} f"{agg_ratio:.1f}"`-fold ...
`{python} show(top_effects("cex", "aggregate_out_pct"))`
```

Identifiers are not measurements, and are written plainly. Document IDs (`SOP-2003`,
`AMV-3010`, `RA-001`), guidance names (`ICH Q8`, `FDA 2011`), citation keys,
cross-reference labels (`@tbl-cqa`, `@fig-contours`) and coded factor levels (−1/0/+1).

A sentence whose truth the data decide (every study closed before X, all outputs met their
criterion, no range narrowed) is a measurement too. Compute its deciding word in the setup chunk,
or `assert` the condition there, so a change in the data stops the render instead of leaving a
false sentence. Found on 2026-10-08: a study added to the chronology after INV-001 was written
made two of its sentences false while every number around them updated correctly.

Never open a sentence with an inline number ("6 steps have…"). Write the sentence so the number
falls inside it ("Six steps…" is not available, because the count is an expression, so write
"The campaign has `{python} n` steps with…"). A sentence that opens on a digit reads as a
filled template.

If a number you need has no helper, write `<<NEEDS: description>>` inline and continue.
Never invent, estimate or recall a value. A `<<NEEDS:>>` marker tells the maintainer to
extend the generator; it is information, not a failure.

## 4. What fails the build

`authoring/check_style.py` gates five tics that sit at or near zero in all four human sources,
and a short list of phrases that occur in none of them. An author sees pass or fail on these and
nothing else.

| tic | the sources | write instead |
|---|---|---|
| an em-dash | at most one or two per thousand words, most often none | a full stop, or a pair of parentheses |
| a semicolon | at most a few per thousand words | a full stop |
| a colon inside a sentence | rare, except to introduce a list | a full stop, or "such as". A sentence that introduces a numbered list may end in a colon |
| bold inside a sentence | never | plain text; bold belongs to headings and table labels |
| a coined three-part hyphenated compound | never | the phrase in full ("host cell protein") |

The banned phrases are the machine's commentary on its own rhetoric, the asides in which a
sentence announces that it is stating something first or that a point deserves comment, and a
handful of generic words the sources never use. The list is `BANNED` in `check_style.py`. The
rule is simpler than the list. Say the thing.

Everything else about the shape of a sentence (its length, its parentheses, its connectives) is
read by a reviewer under `check_style.py --review` and by the questions in
`authoring/REVIEW_CHECKLIST.md`. None of it is shown to you while you write, and none of it is a
target.

## 5. Voice, and what to read before you write

The exemplar holds verbatim human passages arranged by the job each does. Read these before the
section they belong to, and read them for the shape of the paragraph and the weight of the verb,
never to lift a sentence.

- `REGISTER_EXEMPLAR.md` §1, opening a unit operation, what it is and what it does.
- §8 and §9, reporting results and reporting a model, and how much is claimed for it.
- §12, parameter classification, with the reason for the class.
- §15, deviations, limitations and things that went wrong.
- "The study is the patient, not the agent" and "Concede first, then commit", for rules 8 and 9.

## 6. Tables and figures

Introduce a table before it appears, say which rows matter and why, and state what follows from
them. A figure is described in the text that precedes it, what is plotted and what the reader
should see. Every table and figure carries a caption and a label, and every number in the prose
around it comes from the same helper that built it.

Real report tables are not flat. `pc_package/tables.py` builds the ones this corpus needs, with
merged group cells, two-level headers, "n.t." for a test that was not run, and footnotes that say
where a value came from. Use them where the brief lists them, and let the footnote carry a caveat
that belongs to one cell. The prose then says what the table shows, not what each footnote says.

Set every table the way a report sets it (owner's comment 2026-10-08). Where an index column
repeats down the rows (a step, an attribute, a study), merge its cells: build the table with
`T.frame(df, caption, label, merge=["Step", ...])` instead of a pipe table, and the render gate
fails a table that repeats an index cell instead. A grouping variable is always a column of its
own with merged cells, never a heading row inside the body (owner, 2026-10-09: "Do not mix
grouping variables in tables as rows"): a design matrix has a "Run type" column, not rows that say
"Factorial runs" between the runs. Keep headers narrow. Break a long header over two
lines (`header={"col": "Drug-substance\ncriterion"}`), or use an abbreviation that the table's
note and the Abbreviations table both define. A table may be set smaller than the text, but no
smaller than 8 pt (the owner's limit, 2026-10-08), and the render gate fails any text below it. A
table that does not fit at 8 pt gets abbreviated or broken headers, narrower columns, or a landscape
page of its own (`CTable(..., landscape=True)`). A table letters its notes in the order it first
uses them, so prose that cites a note computes the letter (`T.<builder>(...).marker_for("text of
the note")`) and never types it.

## 7. Conventions of a controlled report

These are what make a document read as a controlled record rather than an essay.

- The revision history sits in the front matter. A Version 2.0 document says once, in "Changes
  in this revision", what changed and why, and names the investigation. The rest of the document
  is the current approved text. It does not narrate its own edits.
- An acceptance criterion is stated with its basis, and a result is reported against it: the
  value, the criterion, and "met" or "not met". A table with the columns Criterion, Result and
  Met is the normal form.
- Objectives, acceptance criteria, conclusions and actions are numbered lists. Findings that
  readers will cite later carry a number of their own (F1, F2, …).
- A cross-reference names the document and the section ("PCP-005 §7", "INV-001 §5"). A deviation,
  a lot, a study and a method decision are cited by their identifier.
- Dates are written as the record has them (2026-03-20). A value below the limit of quantitation
  is written "< LOQ" and a test that was not run "n.t.", with a footnote saying why.

## 8. Depth

Depth follows the design. A step with a screening design and a response-surface model has a long
Results section because it has many things to report. A step without a DoE has a short one, and
that is correct. Achieve depth with grounded tables, analysis and full appendices, and end a
paragraph when its point is made.

## 9. Before you submit a section

Read it once as the assessor. Ask of each paragraph what it claims and what it shows, of each
sentence that gives a reason whether the reason stands in the clause with its verb, and of each
claim where it stops. Then run
`authoring/check_render.py`, fix any code error yourself in the same context, and hand the
document on. What comes after is a reviewer's work, not yours.
