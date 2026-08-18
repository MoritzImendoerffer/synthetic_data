# Implementation plan — round three: measure what the reader named, on PCR-003

**Unit:** `2026-08-18_01_register-third-round`. **Proposal:** `docs/next/register-from-four-sources.md`,
Track A + Track B, on `PCR-003` alone (owner, 2026-08-18). **Exploration:** `exploration.md` beside
this file. **Predecessors:** rounds one and two, both shipped and measured. **Written by:** `/plan`.

## What is being built

Round two proved a narrow and uncomfortable thing: an author executes exactly what is measured and
printed back to it, and leaves everything else where it was — including rules it has read. The
project owner then read the round-two report and named three faults on its first sentence, none of
which anything measured, two of which the guide already forbids in words. This unit measures those
three, prints them back, states each as a substitution, re-authors `PCR-003` once, and measures a
fourth point on the longest series in the corpus.

Seven tasks. Three are machinery, one is a document, one is annex, one is measurement, one is
documentation. The critical path is linear: 001 and 002 can run in parallel; 003 needs both; 004
needs 003; 005 needs 004; 006 needs 005; 007 needs 006.

## The order, and why

1. **TASK-001 — the two regex counts into `check_style.py`.** First because the round-two figures
   have no code behind them: they came from an inline heredoc that was never saved. The task's
   acceptance is that it reproduces round two's table exactly before the count becomes the gate's
   line — the discipline the previous unit's TASK-001 applied to `clause_pack.py`. The regex is a
   **floor** (it misses "…, and both were retained"), and the code comment says so.
2. **TASK-002 — passive rate and the parser's and-clause into `check_discourse.py`.** Independent
   of 001. Both counts go inside the copula/front loop so all four share one denominator; the
   consequence — passive reads 35.4 % (146/413) rather than round two's 34.4 % (145/421) — was
   measured by `/plan` and is written into the procedure so nobody "fixes" it. The passive is a
   **band**, never a floor: the plan genre is inside it.
3. **TASK-003 — the brief and the guide.** Needs both scripts' keys. §5d gains three rows and two
   rules stated as substitutions with search strings; the guide gains the write-the-passive rule
   beside Correction 0 (same failure one step out: a manufactured agent instead of a manufactured
   subject), the search strings, three §4a rows, and a ✓-block scan for the two new patterns; the
   exemplar gains three verbatim passives with a study as patient. Minimum edits, per the standing
   owner decision; the guide's own commentary is Track C and is not touched.
4. **TASK-004 — one agent re-authors `PCR-003` in one pass, as a DRAFT.** Told all eight numbers
   and the two new substitutions. `PCP-003` is not re-authored — it is the control column.
5. **TASK-005 — promote, render both formats, re-curate the 35 spans under both extractors,
   re-anchor, re-ground.** The boundary that must close. Only `PCR-003`'s builder strings move; the
   plan's annex must rebuild byte-identical.
6. **TASK-006 — measure four points by one method, apply the rule, record the reading.** Round
   zero, one, two, three and the `PCP-003` control, in one invocation each of the two scripts.
   The stopping rule is fixed now (below). The owner's reading is the human check; whatever it
   quotes is counted afterwards, in that order.
7. **TASK-007 — the documentation move**, under `/ship`, prepared for both verdicts.

## The stopping rule, fixed before the round runs

Edges are the source bands, one document, with round two's five as no-regression conditions:

| condition | edge | round two |
|---|---|---|
| `, and ` + second clause (regex) | ≤ 3.4 % of sentences | 22.6 |
| `, not ` mid-sentence | ≤ 0.2 % | 4.3 |
| passive construction | 50–62 % (band ±4 pt) | 35.4 |
| `, so ` | ≤ 1.0 % | 0.0 |
| opens with a connective | ≥ 3.0 % | 4.0 |
| topic chaining | ≥ 44.1 (not > 2 pt below round two) | 46.1 |
| copula | ≤ 27.7 (not > 2 pt above round two) | 25.7 |
| register gate | passes | OK |

All hold → the numbers half is met and the owner's reading decides the rest, exactly as round two.
Any fails → stop. Within 0.5 pt of an edge → say so, owner decides, edge written down first.

## Decisions this plan made (overrulable)

- **Both and-clause counts, not one.** Measured in exploration §6b: the regex misses bare-noun
  subjects, the small parser misses long coordinated NPs — including two of the three sentences
  the owner quoted. Neither is a superset. Print both, gate neither, report the union. Do not move
  to `en_core_web_trf` for a diagnostic that fails nothing.
- **Passive is a band.** Round two's copula regression is the precedent for a rule that overshoots
  in one genre; `PCP-003` is inside the passive band already.
- **One denominator** for copula/front/passive/and-clause, at the cost of a figure that differs
  from round two's heredoc by 1 point; the procedure and the page both say why.
- **`PCP-003` is reported as the control** though it is not re-authored. A one-genre round loses
  the both-genres check that made round two credible; the control column is the honest substitute.
- **The overshoot is predicted, not awaited.** `, so ` went to 0.0 % and possessives to zero;
  expect `, and ` + clause to go to ~0 %, below the sources' 1.1–3.4. TASK-006 names it as an
  overshoot; TASK-004 does not patch for it.

## What could go wrong

- The measures move and the reading names something new. This is now the expected shape of a
  round; the page says so in advance and the reading stays the test.
- The `, and ` substitution produces semicolons or `, which`. Both are already measured.
- Told to write the passive, the author writes it everywhere. The band's upper edge (62 %) is the
  guard, and the control column shows whether it is a report-genre effect.
- The rhetorical layer breaks on the superscript extractor mismatch again. TASK-005 tests every
  span under both extractors before the builder runs.
- The reader is not blind. Fourth read of `PCR-003`; stated everywhere.

## What will not be attempted

Track C (the guide's own commentary): owner says measures first. Track D (the eighteen): blocked
until the reading says the pair is no longer immediately recognisable. Any gate on the new
measures. Any edit to a committed `.qmd`. Any change under `config/` or `outputs/`.
