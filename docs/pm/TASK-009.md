---
type: pm-task
epic: 2026-08-18_03_author-facing-apparatus
sprint: 2026-08-18_03_author-facing-apparatus
task: TASK-009
status: done
kind: mechanism
title: "Write the per-unit-operation mechanism files, emit them as brief \u00a72b, and halt for the owner's read"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-003", "PCR-005", "PTP-001"]
---

> [!warning] Generated from `.claude/work/2026-08-18_03_author-facing-apparatus/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-009 — Write the per-unit-operation mechanism files, emit them as brief §2b, and halt for the owner's read

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

Runs only on D4 = PASS. Written from domain knowledge, NOT from refs/text/ — exploration §2 checked that A-Mab's Protein A section is 'Expect higher HCP at low pH' and carries no mass-transfer explanation. This is the one place in the repository where prose is authored without a source to ground it against, which is why the owner reads every file once and the file says so. Keep it mechanism only: no claim about the seeded data's effect sizes, no set-point, no range, no direction claim that the CSV could contradict — 'lowering the pH protonates … and reduces affinity' is mechanism; 'HCP rises 1.4-fold at pH 3.2' is a number and forbidden.

## Acceptance criteria

- [x] eight files, one per unit-operation key in config; each maps every CQA the step sets or clears (cqas_for / the CQA register) and every studied parameter (report_params) to two to four sentences of physical chemistry using the terms of art (for protein_a at least: dynamic binding capacity, mass transfer zone, histidine protonation at the Fc–ligand interface, immobilisation chemistry, cumulative cycle number, sanitisation history)
- [x] `grep -cE '[0-9]' authoring/mechanism/*.yaml` on the prose values → 0 for every file (no numbers, so a reseed cannot stale it and golden rule 1 is untouched); a `key:` for the UO and `source: domain knowledge; reviewed by owner <date>` at the top of each
- [x] build_brief.py emits the file as `## 2b. Mechanism — how the step works` for every per-UO document (PCP-003..010, PCR-003..010, sixteen briefs) and omits it for PTP/RA/PCMP/PCMR; `uv run --extra discourse python authoring/build_brief.py PCR-005 && grep -c '## 2b' authoring/out/PCR-005.brief.md` → 1; the same for PTP-001 → 0
- [x] HALT: the eight files are put in front of the owner and each one's `reviewed by owner` line is filled with the date the owner read it; the task is not completed until all eight carry it — a file the owner corrected records the correction in the outcome
- [x] authoring/RUNNER.md preconditions list authoring/mechanism/ as an input the brief carries; `make test` unchanged

**Depends on:** [[TASK-004]]

## What was built

WRITTEN, AND HALTED FOR THE OWNER'S READ (2026-08-19). Eight files in authoring/mechanism/ (bioreactor, harvest, protein_a, viral_inactivation, cex, aex, virus_filtration, ufdf), each with key, step_title, source, reviewed_by_owner (null until read), an overview, a `cqas` map (every CQA the step sets per the register, plus the responses it clears or measures — 7/3/4/3/5/6/3/1 entries) and a `parameters` map covering every parameter key in config (9/3/6/4/5/5/2/3). Written from domain knowledge in the terms of art (dynamic binding capacity, mass transfer zone, histidine protonation at the Fc–ligand interface, immobilisation chemistry, cumulative cycle number, sanitisation history, polarisation layer, isoelectric point, nucleotide sugar donor, …). Directions are committed only where the physical chemistry is unambiguous AND agrees with the sign the seeded model encodes (checked against config/parameters.yaml: e.g. HCP up with load and down with elution pH at Protein A; LRV up as pH falls at low-pH hold; aggregate clearance down with load and later stop-collect at CEX; HCP clearance up with load pH and down with conductivity at AEX; MVM LRV down with filtered volume). Where the model's sign is empirical against the textbook (pCO2 and pH on acidic variants at the bioreactor) the file names the pathway and says the net direction is what the fitted model reads.

No number in any prose value: tests/test_mechanism.py (5 tests) asserts one file per UO, the shape, no digit in overview/cqas/parameters, every config parameter present, every CQA the step sets present — 95 passed. Two digit slips caught by the test and reworded ('CH2–CH3 interface', 'CH2 domain' -> 'the second and third constant domains of the heavy chain'). One word the owner objected to on 2026-08-18 ('aggressively') was in the first draft of protein_a.yaml and is gone.

build_brief.py emits `## 2b. Mechanism — how the step works` for every per-UO document (key is not None) with the file's provenance line ('reviewed by owner: not yet' until the field is set), the overview, and one bullet per attribute and per parameter with the register's / config's display names; corpus-level documents get no §2b (`build_brief.py PTP-001 && grep -c '## 2b'` -> 0; PCR-005 -> 1). authoring/mechanism/README.md says what the files are, why, and the no-number rule; RUNNER.md preconditions name the file and require the owner's read before authoring.

HALT: the eight files are in front of the owner. The task completes when each carries `reviewed_by_owner: <date>`; a correction the owner makes is recorded here.

RESUMED AND COMPLETED 2026-08-19. The owner read the eight files: "for the parameters like dissolved oxygen the abbrviation is DO not do and CO2 not co2 same for ivcc. Other than that the texts read fine". The `do` / `co2` / `ivcc` seen are the config identifiers the YAML must key on (tests/test_mechanism.py maps them to config/parameters.yaml); the fault was the brief printing the key beside the display name. Fixed in build_brief.py §2b: bullets carry the display name only ("Dissolved CO2 (pCO2)", "Dissolved oxygen", "Initial viable cell conc.") and never the key; authoring/mechanism/README.md says keys are identifiers, not abbreviations. Verified on PCP-003's brief (grep for the bracketed keys -> 0). All eight files now carry `reviewed_by_owner: 2026-08-19`. No content correction. Between the write and the read, one content correction of my own from TASK-010's judge (histidine already protonated across the elution range) went into protein_a.yaml before the owner read it. make test 95 passed.

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`
- **PTP-001** — `pc_package/PTP-001_transfer.qmd`

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
- [[README]] — `authoring/mechanism/README.md`
- `tests/test_mechanism.py`
- [[RUNNER]] — `authoring/RUNNER.md`
