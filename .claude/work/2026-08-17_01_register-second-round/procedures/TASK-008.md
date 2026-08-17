# TASK-008 procedure — measure three points by one method, apply the rule, record the reading

Read `state.json` → `TASK-008` first, then `decisions.stopping_rule_edges` in the same file, then
`docs/results/2026-08-17-register-pilot.md` (the page this one is written against).

## 1. The three points, on disk

| point | PCP-003 | PCR-003 |
|---|---|---|
| round zero (`b0361f1`) | `.claude/work/2026-08-16_01_register-from-four-sources/pre-rewrite/PCP-003_bioreactor.qmd` | same dir, `PCR-003_bioreactor.qmd` |
| round one (`f06f1a7`) | `.claude/work/2026-08-17_01_register-second-round/pre-rewrite/PCP-003_bioreactor.qmd` | same dir, `PCR-003_bioreactor.qmd` |
| round two | `pc_package/PCP-003_bioreactor.qmd` | `pc_package/PCR-003_bioreactor.qmd` |

If a `pre-rewrite/` file is missing: `git show b0361f1:pc_package/PCP-003_bioreactor.qmd > <path>`
(round zero) or `git show f06f1a7:…` (round one).

## 2. Run the two scripts, once each, all six files

```bash
R0=.claude/work/2026-08-16_01_register-from-four-sources/pre-rewrite
R1=.claude/work/2026-08-17_01_register-second-round/pre-rewrite
uv run python authoring/check_style.py --compare \
   $R0/PCP-003_bioreactor.qmd $R1/PCP-003_bioreactor.qmd pc_package/PCP-003_bioreactor.qmd \
   $R0/PCR-003_bioreactor.qmd $R1/PCR-003_bioreactor.qmd pc_package/PCR-003_bioreactor.qmd \
   > .claude/work/2026-08-17_01_register-second-round/measure_style.txt
uv run --extra discourse python authoring/check_discourse.py \
   $R0/PCP-003_bioreactor.qmd $R1/PCP-003_bioreactor.qmd pc_package/PCP-003_bioreactor.qmd \
   $R0/PCR-003_bioreactor.qmd $R1/PCR-003_bioreactor.qmd pc_package/PCR-003_bioreactor.qmd \
   > .claude/work/2026-08-17_01_register-second-round/measure_discourse.txt
uv run --extra discourse python authoring/check_discourse.py --cap <same six> \
   > .claude/work/2026-08-17_01_register-second-round/measure_discourse_cap.txt
```

`--compare` prints the same basename for the three revisions of one document; relabel the columns
by position (0 / 1 / 2) when you copy them. The pilot page's spaCy numbers were taken with the
caps; report the **uncapped** table as the round's numbers and the capped one in a footnote for
comparability with the pilot page.

Possessives and constructions (`its`, `their`, `it is/was/will be`, `the <noun> is`) come from
the snippet in the pilot page's *Verification* block; run it over the six files.

## 3. Write `docs/results/2026-08-XX-register-round-two.md` (use today's date)

Skeleton — every table has the four source columns and the six document columns:

```
# The second round: the author was told the number
Run date, work unit, documents, before/after paths, commit ids for rounds zero and one.
Verdict in one line: "Track 2 opens" or "stop and change the target", and the line that decided it.

## Why the run happened            (owner reading of round one; the two sentences; the count)
## What changed — the two packing measures    (', so ' %, initial connective %, 2+ coordinators %)
## The connective repertoire        (rate and distinct, from --compare)
## Topic chaining, copula, front field        (uncapped; capped in a footnote)
## Possessives and what the substitution cost (its / their / it is / the <noun> is)
## The register gate's own numbers  (mean, median, over-40, over-55, under-15 against band and sources)
## The stopping rule, line by line  (table: condition | edge | PCP-003 | PCR-003 | holds?)
## The owner's reading              (verbatim; dated; "not blind, and why that was accepted")
## The hypothesis, answered         (per document, per measure: did giving the author the number move it?)
## What was found on the way        (incl. commercial scale stated? runtime-name subjects? pct_under_15 cost?)
## Verification                     (the exact commands above)
## Files
```

Rules for the page: every number from `measure_*.txt`, never from this plan or the pilot page;
counts with denominators; if a measure moved backwards, name the substitution that paid for it and
count it (round one's model: 25 possessives → 23 copulas).

## 4. The stopping rule (do not move an edge after seeing the numbers)

| condition | edge |
|---|---|
| mid-sentence `, so ` | ≤ 1.0 % of sentences, both documents |
| opens with a connective | ≥ 3.0 % of sentences, both documents |
| topic chaining | not more than 2.0 pt below round one (uncapped round-one value from your own run) |
| copula | not more than 2.0 pt above round one |
| register gate | `check_style.py` passes both (it did in TASK-007) |

All hold → "Track 2 opens". Any fails → "stop and change the target". Within 0.5 pt of an edge →
say so and let the owner decide, but write the plan's edge down first.

## 5. The owner's reading

Ask the project owner to read the two rendered pdfs and answer: is the pair still *immediately*
recognisable as machine-written, and which sentences give it away? Record the answer verbatim,
dated, in the page. This is the human check by owner decision (`decisions.human_check`); it is
not blind — the owner has read both documents twice — and the page says so.

Also record decision D1 input: if the numbers hold and the reading says "still obvious", the
quoted sentences are the next target, and TASK-009 takes the "stop" branch of the proposal.

## 6. `docs/results/README.md`

Add a row like the pilot's, saying why the run happened and linking the page.

## 7. The notebook

Either add §14 to `authoring/register_analysis.ipynb` that shells out to the two scripts and shows
the tables, or write in the page's *Verification*: "the two scripts are the method for these
measures; the notebook's §13 is superseded for them." Say which in `outcome`.

## 8. Done when

Every acceptance line in `state.json` → `TASK-008` is true, and the `measure_*.txt` files are in
the work unit.
