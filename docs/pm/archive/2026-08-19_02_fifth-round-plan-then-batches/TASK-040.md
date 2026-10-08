---
type: pm-task
epic: 2026-08-19_02_fifth-round-plan-then-batches
sprint: 2026-08-19_02_fifth-round-plan-then-batches
task: TASK-040
status: done
kind: measurement
title: "Write the batches' results page"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-007", "PTP-001"]
---

> [!warning] Generated from `.claude/work/2026-08-19_02_fifth-round-plan-then-batches/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-040 — Write the batches' results page

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

The corpus-wide before/after is the campaign's closing measurement.

## Acceptance criteria

- [x] one page for the eighteen: per document the audit result, review run-1/run-2 counts, pages, re-anchoring counts (quotes moved / total, spans re-cut), and the before/after on `measure_apparatus.py` for the whole corpus (all 20 as one column, against the Track D baseline in docs/results/2026-08-18-track-d-stopped.md §3: `, which` 9.82, trailing relatives 11.39, acts-through 1.21, governs/sets 2.07); the five sampled readings verbatim with their verdicts; every number from saved files

**Depends on:** [[TASK-039]]

## What was built

Wrote docs/results/2026-08-21-fifth-round-batches.md, 202 lines, covering the eighteen documents after the pilot plus the three re-authors. Every number in it comes from a committed script: aggregate_campaign.py was written into this work unit for the purpose and shells out to measure_apparatus.py --check-baseline over all 20 shipped .qmd, taking the corpus median of the per-document cells that command prints, so the page cites code rather than a session heredoc (the failure recorded in 2026-08-18-track-d-stopped.md §9). CORPUS-WIDE BEFORE/AFTER, 337 cells over 20 documents: passive 56.0 -> 49.8, ', and '+clause 26.8 -> 20.9, parenthetical openings 7.0 -> 1.8, copula 25.8 -> 21.7, sentences over 40 words 8.1 -> 4.0, 2+ clause coordinators 6.3 -> 3.3, median sentence length 23.0 -> 21.0, colons 0.6 -> 0.0, semicolons 0.5 -> 0.0, coined compounds 0.2 -> 0.0. THE ROUND'S OWN ARTIFACT, stated plainly on the page: `rather than` rose from 0.0 to 1.8 per 1k words across eighteen documents. Three judges named it independently and two documents cut it hard after being told (PTP-001 15->4, PCP-007 12->1), but corpus-wide it ROSE, because it is how an author trained off a filing clause writes a contrast. Not fixed. The page also records: the audit's three failure modes with the principle that should replace them; the two revisions that introduced wrong physics and the fact that WARNING THE NEXT AUTHOR STOPPED IT RECURRING; the two cases where an author correctly overruled its judge on corpus consistency; that eleven of twenty documents were promoted on the review and the gates alone with the plan side resting on one reversed reading; six machinery defects found and not fixed; and that report_sections statements were FALSE rather than stale in every B5 document, which no gate catches.

## Documents it is about

- **PCP-007** — `pc_package/PCP-007_cex.qmd`
- **PTP-001** — `pc_package/PTP-001_transfer.qmd`

## Files it touched

- [[2026-08-<dd>-fifth-round-batches]] — `docs/results/2026-08-<dd>-fifth-round-batches.md`
