---
type: pm-task
epic: 2026-08-16_01_register-from-four-sources
sprint: 2026-08-16_01_register-from-four-sources
task: TASK-009
status: todo
kind: measurement
title: "Measure both pilot documents and put them in front of a reader"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCP-003", "PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-16_01_register-from-four-sources/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-009 — Measure both pilot documents and put them in front of a reader

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

TWO DOCUMENTS NOW, one plan and one report, so the results page can say whether the amendment works in both genres. A result that holds for the report and not the plan, or the reverse, is the most useful thing this pilot can produce and the current plan would not have found it.

THE FIVE MEASURES, with the before-values measured on 2026-08-16/17 and the human reference now spanning four sources:
  1. topic chaining: PCP-003 30.0 %, PCR-003 37.2 % -> sources 57.0 to 61.9 (PDA 59.4, A-Mab 59.0, ISPE TT 61.9, ISPE PV 57.0). Notebook section 8.
  2. connectives: corpus median 1.5 per 1000 words using 3 of the 9 -> sources 2.2 to 2.7 using 6 to 9. 'However' twice in the whole corpus against 59 in the sources. This is now printed by check_style.py on every run, so it needs no notebook.
  3. copula rate, 'X is <noun phrase>': PCR-003 33.3 % -> reference 14.7 and 18.2. Notebook section 4.
  4. possessives per 1000 words: PCP-003 its 5.72 their 3.18 it 7.42; PCR-003 its 6.66 their 4.15 it 10.62 -> sources its 0.27-0.40, their 0.50-0.96, it 1.75-3.33.
  5. adjunct front field: 9.1 to 13.6 % of clauses -> sources 29.5 and 25.4. scratchpad/front.py, or notebook section 4.

RUN THE NOTEBOOK, do not quote this plan. It runs clean under: uv run --with spacy --with 'https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl' --with jupyter jupyter lab. Note the double --with: 'uv run --with spacy' alone builds a fresh environment each call and a separately downloaded model is not in it. Add four before/after target columns.

ALSO REPORT THE GATE'S OWN NUMBERS. TASK-002 raised mean_len to 30.5, pct_over_40 to 21.5 and pct_over_55 to 9.5 to accommodate ISPE PV, whose extraction fuses list items into pseudo-sentences. If either re-authored document lands near those ceilings rather than near the per-source columns, the band is doing harm and the results page must say so. That is a finding about the gate, not about the author.

THE ACCEPTANCE TEST IS DISCRIMINATION, NOT COUNTS. Show a reader passages from the two re-authored documents and from the human sources, unlabelled, and ask which is which. Report correct identifications over total passages. A connective count is a diagnosis and would be gamed as a target.

A NULL RESULT IS A RESULT. If the shape moves and the prose still does not read as SME prose, say so. That would mean the discourse hypothesis is wrong or TASK-003's amendment was too timid, and it stops the campaign before eighteen more documents are re-authored. Every rate carries its denominator; never quote a bare percentage.

## Acceptance criteria

- [ ] the five shape measures are reported before and after for BOTH PCP-003 and PCR-003, each with its denominator
- [ ] the figures are produced by re-running register_analysis.ipynb rather than quoted from this plan
- [ ] the four human sources are the reference columns, not two
- [ ] a discrimination test is run and reported: unlabelled corpus and source passages, with the count of correct identifications over the number of passages
- [ ] the register gate's own numbers are reported for both documents, and the report says whether either drifted into the headroom TASK-002 opened
- [ ] the results page states plainly whether the change is worth extending to the remaining EIGHTEEN documents
- [ ] a row is added to docs/results/README.md saying why the run happened

**Depends on:** [[TASK-008]]

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- [[2026-08-XX-register-pilot]] — `docs/results/2026-08-XX-register-pilot.md`
