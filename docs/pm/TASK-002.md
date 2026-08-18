---
type: pm-task
epic: 2026-08-18_01_register-third-round
sprint: 2026-08-18_01_register-third-round
task: TASK-002
status: todo
kind: mechanism
title: "Add the passive rate and the parser's ', and '+clause count to check_discourse.py, as bands with denominators"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCP-003", "PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-18_01_register-third-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-002 — Add the passive rate and the parser's ', and '+clause count to check_discourse.py, as bands with denominators

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-002.md. THE PARSER LOGIC IS IN THIS UNIT'S andclause.py (parser_and_clause) — port it, do not re-derive it; the exploration §6b table is what it must reproduce. THE PASSIVE COUNT is round two's: any token nsubjpass or auxpass (measure_owner_reading was produced that way). ONE DENOMINATOR: put both counts inside copula_front()'s loop (line 76-88) so passive, front, copula and and-clause all divide by the same n; do NOT write a fourth loop with its own cap. Rename the function if you like; keep the return shape backward-compatible for build_brief (TASK-003 reads the JSON keys). WHY BOTH COUNTS OF THE AND-CLAUSE EXIST: exploration §6b — the regex misses bare-noun subjects ('and both were retained'), the small parser misses long coordinated NPs including TWO OF THE THREE sentences the owner quoted. Neither is a superset. Print both, gate neither, and let the results page report the union. Do NOT switch to en_core_web_trf. BAND NOT FLOOR: PCP-003 is INSIDE the passive band (54.7) and PCR-003 twenty points under it; a floor pushes the plan the wrong way. Say 'band' in the header text and in the JSON label. The extra is installed today (spacy 3.8.15). Prove degradation on a base `uv sync` at the end and re-install with `uv sync --extra discourse` for TASK-003.

## Acceptance criteria

- [ ] measure() returns 'passive_pct' + 'passive' [count, n] and 'and_clause_pct' + 'and_clause' [count, n], computed inside the SAME loop and over the SAME sentence list as copula/front so the three share one denominator n; a sentence is passive if any token has dep_ in ('nsubjpass','auxpass'); a sentence has an and-clause if a token with dep_=='cc' and lower_=='and' has a sibling conj (conj.i > tok.i, dep_=='conj') that is VERB/AUX with a child nsubj/nsubjpass/expl AND the token before 'and' is ','
- [ ] the text table prints two new rows after front field: 'passive construction % (passive/n)' and "', and '+clause, parser % (and/n)"; the header note says the passive is a BAND (sources 54-60 %) and never a floor
- [ ] `uv run --extra discourse python authoring/check_discourse.py --cap pc_package/PCR-003_bioreactor.qmd pc_package/PCP-003_bioreactor.qmd` prints, for the parser and-clause row, PDA 3.2 (26/…) / A-Mab 1.2 / ISPE TT 0.9 / ISPE PV 2.8 / PCR-003 24.9 (105/…) / PCP-003 24.6 (50/…) — this unit's andclause.py figures, within ±0.5 pt on the corpus columns and exact on the counts where the cap does not bite (both corpus documents are under 450 sentences)
- [ ] the passive row for PCR-003 reads 35.4 (146/413) — 146 passive sentences (measured by /plan on 2026-08-18; round two's 145 was taken on the DRAFT) over the copula loop's denominator of 413, NOT round two's 34.4 (145/421) over all sentences; the completion note records both figures and the reason (eight sentences with no root/subject are outside the copula denominator); PCP-003's value is recorded the same way
- [ ] --json carries the four new keys; `uv run python authoring/check_discourse.py <qmd>` on a base sync (no extra) still prints the one degrade line and exits 0; `make test`, `make style` unchanged

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- `authoring/check_discourse.py`
