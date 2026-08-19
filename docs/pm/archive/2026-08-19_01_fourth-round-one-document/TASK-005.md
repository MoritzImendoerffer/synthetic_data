---
type: pm-task
epic: 2026-08-19_01_fourth-round-one-document
sprint: 2026-08-19_01_fourth-round-one-document
task: TASK-005
status: done
kind: measurement
title: "Count what the reading named, before/after against the same script, and write the results page"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCR-007"]
---

> [!warning] Generated from `.claude/work/2026-08-19_01_fourth-round-one-document/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-005 — Count what the reading named, before/after against the same script, and write the results page

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

Every number from measure_apparatus.py or check_style output saved in the unit — no session heredoc. Compare against PCR-007's own baseline (measure_baseline_PCR-007.txt) AND against the probe page, so the reader sees whether a whole document under the regime looks like the two subsections did.

## Acceptance criteria

- [x] `uv run --extra discourse python ../2026-08-18_03_author-facing-apparatus/measure_apparatus.py pc_package/PCR-007_cex.qmd pc_package/PCR-007_cex.DRAFT.qmd > measure_after_PCR-007.txt` — shipped and new side by side, sources first, all blocks; `uv run python authoring/check_style.py --review` on both saved as check_style_after_PCR-007.txt
- [x] the results page holds: the regime (inputs and word count, model, check_render passes, one content-review cycle with its per-question counts); the reading verbatim; the rule applied; a table shipped vs new vs the four sources for `, which`, all trailing relatives, `acts on / through`, `governs / sets`, `, so `, `, and `+clause (regex and parser), opens with a connective, passive, chaining, copula, `its`, mean_len, pct_under_15, pct_over_40, staccato — every number from the two saved files; the gate result on both (GATED and the advisory rows); pages and sentence counts; and the comparison with the probe's numbers (docs/results/2026-08-19-apparatus-probe.md §3) in one paragraph
- [x] a 'what was found on the way' section: <<NEEDS>> the agent hit, helpers extended if any, what the content review flagged and what one cycle changed, anything the RUNNER as rebuilt got wrong
- [x] a Verification section whose commands are exactly the ones run; the page is linked from docs/results/README.md at ship (TASK-008)
- [x] written whichever way D6 fell; on FAIL it says 'the draft is kept in the unit and nothing shipped'

**Depends on:** [[TASK-004]]

## What was built

Page: docs/results/2026-08-19-fourth-round-PCR-007.md. Numbers from measure_after_PCR-007.txt (measure_apparatus.py, shipped vs new, sources first, all blocks) and check_style_after_PCR-007.txt (--review on both); no heredoc.

Shipped -> new (sources), per 100 sentences: `, which` 10.5 -> 5.8 (0.6–2.4); all trailing relatives 11.9 -> 6.6 (1.2–3.0); acts on/through 2.05 -> 0.41 (0); governs/sets 2.05 -> 0.62 (0); behaves as 1 -> 0; copula 31.1 -> 24.6 % (13–26). The new PCR-007 lands where the probe landed (5.6 / 6.7). Unchanged or worse, and the reader did not mind: `, so ` 10.3 -> 11.0 % (0.1–0.4); `, and `+clause 21.6 -> 14.9 regex / 26.5 -> 20.3 parser (1–3.4); connective openings 0.7 -> 0.0 (3.7–6.1); passive 48.8 -> 48.9 (57–64); chaining 37.2 -> 39.5 (56–62); `its` 5.81 -> 6.26 per 1k; staccato 0 -> 3.9. Gate: both OK on the five tics; the new one outside the advisory band on parentheses (2.2, floor 3.0) and 'rather than' (1.9, ceiling 0.8), inside on every length row (mean 22.2, 3.7 % over 40, 27.2 % under 15). Pages 51 -> 50, sentences 439 -> 482.

The page also carries: the regime table, run 1's self-measurement finding with the RUNNER fix, the content review's run-1/run-2 counts, the reading verbatim with the rule, what is settled and not. Comparison with the probe in §5a.

## Documents it is about

- **PCR-007** — `pc_package/PCR-007_cex.qmd`

## Files it touched

- [[2026-08-19-fourth-round-PCR-007]] — `docs/results/2026-08-19-fourth-round-PCR-007.md`
- `.claude/work/2026-08-19_01_fourth-round-one-document/measure_after_PCR-007.txt`
- `.claude/work/2026-08-19_01_fourth-round-one-document/check_style_after_PCR-007.txt`
