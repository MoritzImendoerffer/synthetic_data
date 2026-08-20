# Every value is gated; every comparison between values is not

**Status:** proposed 2026-08-20, out of work unit `2026-08-19_02_fifth-round-plan-then-batches`.
Eight defects of this class were found by hand in one day, across six documents, by five
independent readers who were not looking for them. Nothing in the build looks for them at all.

## The problem

The corpus rests on one rule: **no number is typed, every number is an inline `{python}`
expression pulled from the config through a helper** (CLAUDE.md, golden rule 1).
`check_render.py` proves every one of those expressions evaluates. `check_grounding.py` proves
every annex quote is a verbatim substring of the rendered text. Between them they establish that
the *values* in a document are the values in `outputs/`.

They establish nothing about the **relations asserted over those values**. "The highest", "the
tightest", "twice", "an order of magnitude", "follows from", "assigned from" — every one of these
is authored prose about numbers that are themselves correct. The author of `PCR-004` put it
exactly right when it caught one of its own:

> "The claim was wrong and no gate would have caught it, since Tool #1 appears in the table but
> the comparison was mine."

**The gap is structural, not accidental.** The stronger the value-level guarantee, the more a
reader trusts a sentence *about* those values — and the less anything checks it.

## The evidence

All eight were found on 2026-08-20. Every row below was verified directly against
`config/parameters.yaml` or `outputs/data/*.csv` while writing this proposal, not taken on report.

| Document | The claim | What the data says |
|---|---|---|
| `PCP-004`, `PCP-006`, `PCP-010` | criticality "is assigned from", "follows from", or rises with the Tool #1 score | `score = impact × uncertainty` for all 10 rows, but viral clearance is **VH at 20** and galactosylation **H at 48**. Viral clearance has the *highest* impact (20) and the *lowest* uncertainty (1). |
| `PCR-004` attempt 2 | "host cell protein carries the highest Tool #1 score" | aggregate **60**, host cell protein **36**, residual DNA **6** |
| `PCR-004` attempt 2 | a 25 % excursion is "an order of magnitude larger than the analytical variability" | AMV-3015 precision is **4.0 %**; 25 / 4 = **6.25** |
| `PCR-005` | the leached Protein A ELISA is "the least precise of the methods applied at this step" | AMV-3016 **6.5 %** against AMV-3012 **9.5 %** — backwards |
| `PCP-004` | the host cell protein ELISA "is the least precise method in the set" | **true** against all 8 rows of `dev_methods.csv`, but the document's own table quotes 2 of them and says the others "are not quoted here" — unsupported by what the reader can see |
| `PCR-005` | the step "removes more host cell protein and more DNA than any other step of the train" | contradicts `PCR-007`; corrected by the author, not independently re-verified here |
| `PCR-003` | pCO2 and culture pH sharing a sign on acidic variants is "what a shared intracellular mechanism predicts" | a higher pCO2 lowers cytosolic pH while a higher culture pH raises it; a shared account predicts **opposite** signs |

Two of these are not simply false. `PCP-004`'s superlative is **true of the data and unsupported
by the document**, which a reader cannot distinguish from a false one. `PCR-003`'s is a claim
about a *mechanism* implied by two signs, which no lookup settles. A useful check has to surface
all three shapes and adjudicate only the ones it can.

## What is not the problem

- **Not the values.** Every number in every claim above is correct. Re-running `make data
  figures` changes nothing about this.
- **Not the annex.** `check_grounding` would pass all eight: the quotes are verbatim.
- **Not the register.** `check_style.py` measures tics. None of these is a tic.
- **Not the content review.** Five judges read these documents against four questions and found
  most of these *incidentally*, in an "outside the four questions" postscript. None of the four
  questions asks whether a comparison is true.

## The idea

`authoring/check_comparisons.py` — a **reviewer's worksheet**, not a gate and not an author-facing
counter.

It works in three stages:

1. **Find the claims.** Scan the document's prose for comparison cues: superlatives (*highest,
   lowest, largest, smallest, tightest, most, least, best, worst, only*), ordering verbs
   (*follows from, assigned from, rises with, ranks*), and magnitude relations (*an order of
   magnitude, twice, half, a factor of N, N times*).
2. **Bind them to data.** For each claim, find the entity names in the same sentence that appear
   in the corpus's own registries — `cqa_reg`, `param_reg`, `dev_methods`, the method ids — and
   the column the claim is about. The helpers already carry the name→row mapping the documents
   render from, so this is a lookup rather than a guess.
3. **Report, and adjudicate where it can.** Print each claim with the rows it is about and their
   values. Where the claim is a superlative over one column and the entity set is unambiguous,
   assert it mechanically and mark it `TRUE` / `FALSE`. Where it is not, mark it `READ` and print
   the values beside the sentence for a human.

A fourth output matters as much as the verdicts: **claims whose entity set is larger than the set
the document renders**, which is `PCP-004`'s case. The check knows both what the register holds
and what the document's tables show, so it can say "this ranks 8 methods; your table shows 2".

## Why it must not be a gate

This project has learned twice that a number shown to an author becomes a target
([`docs/results/2026-08-19-apparatus-probe.md`](../results/2026-08-19-apparatus-probe.md); the
author-facing counter finding in CLAUDE.md's Voice rule). A comparison check that fails a build
would teach authors to stop writing comparisons, and comparisons are how a report earns its
conclusions. The output goes to a **reviewer**, beside `check_style.py --review`, and the author
never sees it.

## What it would take

- `authoring/check_comparisons.py`, one file, no new dependency. The cue lexicon is a literal in
  the file, the bindings come from `_pcpkg.py`'s existing registries.
- A `--selftest` in this repository's tradition: the eight defects above are a **labelled test
  set**. The pre-fix drafts are preserved in
  `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/*.pre-review.qmd` and
  `*.DRAFT.post-review.qmd`, so the check can be run against text that is known to contain them.
  **Acceptance: it surfaces all eight, and a reviewer can read a whole document's output in under
  a minute.**
- A line in `authoring/REVIEW_CHECKLIST.md` telling the reviewer to run it. No change to
  `RUNNER.md`, to the launch prompt, or to anything the author reads.

## Verification

Run it over all 20 shipped documents and count. The claim to test is not "it finds bugs" but
**"the number of `READ` lines per document is small enough that a reviewer reads them all"**. If a
50-page report yields 40 lines, it is a worksheet; if it yields 400, it is noise and the cue
lexicon is wrong.

Then re-run the eight-defect selftest after any lexicon change, exactly as `check_style.py
--selftest` protects its thresholds against drift.

## What this deliberately does not do

- It does not check prose against prose. `PCR-005` contradicting `PCR-007` is in scope only
  because both rest on the same CSVs; two documents disagreeing about something neither derives
  from data is out of scope.
- It does not verify mechanistic inferences. `PCR-003`'s "what a shared intracellular mechanism
  predicts" is wrong for a reason no table holds. The check can print the two signs beside the
  sentence; a human decides.
- It does not gate, score, or count for the author.

## Open questions

- **Does the cue lexicon generalise, or is it fitted to eight examples?** The honest test is to
  write it from the eight, then run it on the twelve documents that have never been reviewed this
  way and see whether it finds a ninth.
- **Where does "only" belong?** "the only response that limits the operating region" is a
  comparison; "the only step credited with MVM clearance" is a register fact. Both are checkable
  and the second is the more valuable, but they bind to different tables.
- **Should the annex carry comparative assertions?** `schema_ext.py` could add an assertion type
  whose warrant is a relation over two or more entity values, which would make the claim
  machine-checkable *and* make it visible to a consumer of the corpus. That is a larger change and
  probably a separate proposal; see the transferability note below.

## Transferability, since the question was asked

The failure generalises further than the fix does.

**The lesson is general to any pipeline that establishes values by provenance.** Wherever numbers
are pulled from a source of truth and the pulling is verified, the verification creates a blind
spot exactly where prose reasons *about* the numbers. That applies to generated regulatory
submissions, clinical study reports, financial reporting from a warehouse, and any
retrieval-grounded generation that cites values — cite-checking that a number appears in a source
does not check that the sentence's comparison of two sourced numbers is sound.

**The check itself transfers only where a dataset stands behind the prose.** Stages 2 and 3 need
a name→row binding. Without one it degrades to "highlight every superlative", which is a much
weaker tool.

**For `nlp_reports` specifically, the interesting part is the schema, not the script.** This
corpus already records `assertions` with `SourceReference`s. A *comparative* assertion — one whose
warrant is a stated relation (`max`, `ratio`, `monotonic`) over two or more named entity values —
is a thing an annotation schema could represent, and once represented it is checkable by anyone,
not just by this repository's helpers. It would also give an NLP consumer something it currently
cannot get: which sentences in a document make claims that are *derivable* from the tables, as
against claims that merely quote them. That belongs in `pc_package/schema_ext.py` first, recorded
in `schema_extensions_used`, and only ever upstream if it proves out — CLAUDE.md rule 4 keeps
`nlp_reports` read-only, and this proposal does not touch it.
