---
type: pm-task
epic: 2026-08-18_03_author-facing-apparatus
sprint: 2026-08-18_03_author-facing-apparatus
task: TASK-009
status: todo
kind: mechanism
title: "Write the per-unit-operation mechanism files, emit them as brief \u00a72b, and halt for the owner's read"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
---

> [!warning] Generated from `.claude/work/2026-08-18_03_author-facing-apparatus/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-009 — Write the per-unit-operation mechanism files, emit them as brief §2b, and halt for the owner's read

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

Runs only on D4 = PASS. Written from domain knowledge, NOT from refs/text/ — exploration §2 checked that A-Mab's Protein A section is 'Expect higher HCP at low pH' and carries no mass-transfer explanation. This is the one place in the repository where prose is authored without a source to ground it against, which is why the owner reads every file once and the file says so. Keep it mechanism only: no claim about the seeded data's effect sizes, no set-point, no range, no direction claim that the CSV could contradict — 'lowering the pH protonates … and reduces affinity' is mechanism; 'HCP rises 1.4-fold at pH 3.2' is a number and forbidden.

## Acceptance criteria

- [ ] eight files, one per unit-operation key in config; each maps every CQA the step sets or clears (cqas_for / the CQA register) and every studied parameter (report_params) to two to four sentences of physical chemistry using the terms of art (for protein_a at least: dynamic binding capacity, mass transfer zone, histidine protonation at the Fc–ligand interface, immobilisation chemistry, cumulative cycle number, sanitisation history)
- [ ] `grep -cE '[0-9]' authoring/mechanism/*.yaml` on the prose values → 0 for every file (no numbers, so a reseed cannot stale it and golden rule 1 is untouched); a `key:` for the UO and `source: domain knowledge; reviewed by owner <date>` at the top of each
- [ ] build_brief.py emits the file as `## 2b. Mechanism — how the step works` for every per-UO document (PCP-003..010, PCR-003..010, sixteen briefs) and omits it for PTP/RA/PCMP/PCMR; `uv run --extra discourse python authoring/build_brief.py PCR-005 && grep -c '## 2b' authoring/out/PCR-005.brief.md` → 1; the same for PTP-001 → 0
- [ ] HALT: the eight files are put in front of the owner and each one's `reviewed by owner` line is filled with the date the owner read it; the task is not completed until all eight carry it — a file the owner corrected records the correction in the outcome
- [ ] authoring/RUNNER.md preconditions list authoring/mechanism/ as an input the brief carries; `make test` unchanged

**Depends on:** [[TASK-004]]

## Files it touched

- `authoring/mechanism/bioreactor.yaml`
- `authoring/mechanism/harvest.yaml`
- `authoring/mechanism/protein_a.yaml`
- `authoring/mechanism/viral_inactivation.yaml`
- `authoring/mechanism/cex.yaml`
- `authoring/mechanism/aex.yaml`
- `authoring/mechanism/virus_filtration.yaml`
- `authoring/mechanism/ufdf.yaml`
- `authoring/build_brief.py`
