---
type: pm-task
epic: 2026-08-18_01_register-third-round
sprint: 2026-08-18_01_register-third-round
task: TASK-002
status: done
kind: mechanism
title: "Add the passive rate and the parser's ', and '+clause count to check_discourse.py, as bands with denominators"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-003", "PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-18_01_register-third-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-002 — Add the passive rate and the parser's ', and '+clause count to check_discourse.py, as bands with denominators

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-002.md. THE PARSER LOGIC IS IN THIS UNIT'S andclause.py (parser_and_clause) — port it, do not re-derive it; the exploration §6b table is what it must reproduce. THE PASSIVE COUNT is round two's: any token nsubjpass or auxpass (measure_owner_reading was produced that way). ONE DENOMINATOR: put both counts inside copula_front()'s loop (line 76-88) so passive, front, copula and and-clause all divide by the same n; do NOT write a fourth loop with its own cap. Rename the function if you like; keep the return shape backward-compatible for build_brief (TASK-003 reads the JSON keys). WHY BOTH COUNTS OF THE AND-CLAUSE EXIST: exploration §6b — the regex misses bare-noun subjects ('and both were retained'), the small parser misses long coordinated NPs including TWO OF THE THREE sentences the owner quoted. Neither is a superset. Print both, gate neither, and let the results page report the union. Do NOT switch to en_core_web_trf. BAND NOT FLOOR: PCP-003 is INSIDE the passive band (54.7) and PCR-003 twenty points under it; a floor pushes the plan the wrong way. Say 'band' in the header text and in the JSON label. The extra is installed today (spacy 3.8.15). Prove degradation on a base `uv sync` at the end and re-install with `uv sync --extra discourse` for TASK-003.

## Acceptance criteria

- [x] measure() returns 'passive_pct' + 'passive' [count, n] and 'and_clause_pct' + 'and_clause' [count, n], computed inside the SAME loop and over the SAME sentence list as copula/front so the three share one denominator n; a sentence is passive if any token has dep_ in ('nsubjpass','auxpass'); a sentence has an and-clause if a token with dep_=='cc' and lower_=='and' has a sibling conj (conj.i > tok.i, dep_=='conj') that is VERB/AUX with a child nsubj/nsubjpass/expl AND the token before 'and' is ','
- [x] the text table prints two new rows after front field: 'passive construction % (passive/n)' and "', and '+clause, parser % (and/n)"; the header note says the passive is a BAND (sources 54-60 %) and never a floor
- [x] `uv run --extra discourse python authoring/check_discourse.py --cap pc_package/PCR-003_bioreactor.qmd pc_package/PCP-003_bioreactor.qmd` prints, for the parser and-clause row, PDA 3.2 (26/…) / A-Mab 1.2 / ISPE TT 0.9 / ISPE PV 2.8 / PCR-003 24.9 (105/…) / PCP-003 24.6 (50/…) — this unit's andclause.py figures, within ±0.5 pt on the corpus columns and exact on the counts where the cap does not bite (both corpus documents are under 450 sentences)
- [x] the passive row for PCR-003 reads 35.4 (146/413) — 146 passive sentences (measured by /plan on 2026-08-18; round two's 145 was taken on the DRAFT) over the copula loop's denominator of 413, NOT round two's 34.4 (145/421) over all sentences; the completion note records both figures and the reason (eight sentences with no root/subject are outside the copula denominator); PCP-003's value is recorded the same way
- [x] --json carries the four new keys; `uv run python authoring/check_discourse.py <qmd>` on a base sync (no extra) still prints the one degrade line and exits 0; `make test`, `make style` unchanged

## What was built

check_discourse.py measures five things instead of three, and the last four share one denominator.

copula_front() became copula_front_passive_and() and returns cop, front, passive, andc, n. Both new counts are taken inside its existing per-sentence loop, after the root/subject test that sets n, so passive, and-clause, copula and front field all divide by the same n. No fourth loop and no fourth cap. A sentence counts as passive when any token carries nsubjpass or auxpass, which is how round two's heredoc counted it. _and_clause() is ported from this unit's andclause.py without change: a "cc" token "and" preceded by a comma, whose head has a conj child later in the sentence that is VERB or AUX and carries its own nsubj, nsubjpass or expl. measure() gained passive_pct / passive / and_clause_pct / and_clause; the chaining, copula and front keys are untouched, and build_brief.py's §5d still builds against them (rerun for PCR-003: 46.1 (190/412), 25.7 (106/413), 17.4 (72/413), unchanged).

Reproduction, `--cap`, over PCR-003 and PCP-003 (PDA / A-Mab / ISPE TT / ISPE PV / PCR-003 / PCP-003):

  passive construction % (passive/n)   59.8 (251/420)  61.9 (255/412)  63.0 (267/424)  61.4 (259/422)  35.4 (146/413)  55.2 (111/201)
  ', and '+clause, parser % (and/n)      3.6 (15/420)     0.7 (3/412)     0.7 (3/424)    2.8 (12/422)  25.4 (105/413)   24.9 (50/201)

Both corpus counts are exact against andclause.py: 105 and 50. The percentages read 0.5 and 0.3 points high because the denominator is the copula loop's n (413, 201), not every sentence (421, 203); that is the shared denominator working as intended. The capped source columns are within 0.5 of andclause.py, and uncapped every source count is exact: PDA 26, A-Mab 13, ISPE TT 6, ISPE PV 23.

PASSIVE, PCR-003: 35.4 % (146/413), the figure /plan predicted. Round two's page says 34.4 % (145/421). Two differences, both understood: the round-two heredoc ran on the DRAFT before promotion and one sentence changed (145 -> 146), and it divided by all 421 sentences rather than the 413 that have a root and a subject. On the all-sentence denominator today's document is 146/421 = 34.7 %. PCP-003: 55.2 % (111/201) here against round two's 54.7 % (111/203) — same 111 sentences, same eight-sentence denominator effect.

FLAGGED FOR TASK-003, not fixed here: the plan's band for the passive, 54.3-59.8 %, is the round-two figure over all sentences. On this table's denominator the same four sources run 56.9-64.0 % uncapped and 59.8-63.0 % capped, so a note reading "sources 54-60 %" would be contradicted by the columns printed beneath it. The header note therefore states both: 54-60 % of all their sentences, 57-64 % on this table's n. TASK-003 has to decide which band goes into the brief's §5d, and the two must not disagree.

Both rows print after front field with the labels the acceptance names, and the header note says the passive is a band and never a floor, with the reason. --json carries all four keys (passive_pct 35.351…, and_clause_pct 25.423…). --cap's docstring and help now say the cap covers four measures rather than two.

Degradation proved on a base `uv sync` with no extra: `uv run python authoring/check_discourse.py pc_package/PCR-003_bioreactor.qmd` printed the single degrade line and exited 0; make test 89 passed and make style exited 0 in that environment. `uv sync --extra discourse` restored spacy 3.8.15 for TASK-003.

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- `authoring/check_discourse.py`
