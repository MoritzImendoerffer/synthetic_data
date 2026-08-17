---
type: pm-task
epic: 2026-08-16_01_register-from-four-sources
sprint: 2026-08-16_01_register-from-four-sources
task: TASK-006
status: done
kind: mechanism
title: "Give the brief a discrepancies section, so a re-authored document keeps its registered defects"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-003", "PCP-006", "PCP-008", "PCP-009", "PCR-003", "PCR-006", "PCR-008", "PCR-009"]
---

> [!warning] Generated from `.claude/work/2026-08-16_01_register-from-four-sources/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-006 — Give the brief a discrepancies section, so a re-authored document keeps its registered defects

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

THE DEFECT THIS CLOSES. Nothing writes D-002 into a re-authored document. build_brief.py emits seven sections - Identity, Quality attributes, Parameters, DoE structure, PARs, Deviations, Cross-references, Helper inventory - written by w() calls at about lines 219, 237, 255, 265, 277, 296, 345 and 362. None is discrepancies. authoring/discrepancies.yaml does NOT exist on main; the mechanism lives on feature/weak-claims-via-brief. So re-authoring PCR-003 would delete a registered benchmark item and no gate would notice, because check_grounding.py inspects SourceReference.quote and never a description field.

WHY IT IS WORSE THAN IT SOUNDS. D-002's annex half lives in build_ground_truth.py:242 as a ProcessStep description string and is GENERATED, so it survives a re-author. Losing only the prose half leaves the annex asserting a claim the document no longer makes - worse than losing both.

WHAT TO PORT. Look at the feature branch without merging it: `git show feature/weak-claims-via-brief:authoring/discrepancies.yaml` and the matching build_brief.py section. Take the discrepancy half ONLY. Do not bring weak_claims across in any form; main keeps weak_claims empty in all 20 annexes without exception, and that branch is rebased forward and never merged back.

WHAT GOES IN THE YAML. Source of truth is authoring/DISCREPANCIES.md. D-001 is at line 35: the PAR analysis holds other factors at the design centre while four plans (PCP-003, PCP-006, PCP-008, PCP-009) commit in prose to holding them at set-points. D-002 is at line 128: PCR-003 5.1 claims 'This is the only step of the drug substance process at which product quality attributes are formed', which outputs/data/cqa_register.csv contradicts through its set_by column - protein_a sets leached Protein A, viral_inactivation and aex set viral clearance. Carry the exact sentence each document must contain, so the author writes it rather than paraphrasing it.

D-001 IS ALREADY SAFE and this task does not change that: section_plan.yaml lines 315 and 535 instruct the author to write the at-set-point commitment. That is why the PCP-003 pilot is safe today. This task turns that from luck into a guarantee and extends it to D-002.

## Acceptance criteria

- [x] uv run python authoring/build_brief.py PCR-003 emits a discrepancies section naming D-002 and quoting the sentence the document must carry
- [x] uv run python authoring/build_brief.py PCP-003 emits D-001 with its at-set-point commitment
- [x] a document with no registered discrepancy emits the section empty rather than omitting it
- [x] authoring/weak_claims.yaml and build_weak_claims_annex.py are untouched, and weak_claims stays empty in all 20 annexes
- [x] cd pc_package && uv run python build_ground_truth.py && uv run python validate_annex.py reports 20/20 valid, unchanged
- [x] uv run python -m pytest -q tests/ passes

## What was built

authoring/discrepancies.yaml now exists on main, ported from feature/weak-claims-via-brief with the discrepancy half ONLY, and build_brief.py emits it as brief section 5c through _discrepancy_assignments().

ASSIGNMENTS: D-001 to PCP-003, PCP-006, PCP-008 and PCP-009 as protocol_method_statement, and to PCR-006, PCR-008 and PCR-009 as do_not_reconcile. D-002 to PCR-003 as unsupported_absolute. Eight documents carry an assignment, twelve carry an empty section.

TWO DELIBERATE DEPARTURES FROM THE BRANCH:
  - The branch returns '' when a document has no items, so the section vanishes. The acceptance criterion asks for an empty section instead, and it is right: an absent section cannot be told apart from a mechanism that has silently stopped working, which is exactly what an author saw while this was broken. All 20 briefs now carry a 5c heading; 12 say 'None' and restate that everything must be consistent.
  - Each assignment carries a `registered_sentence` field, quoted verbatim in the brief above the instructions. The acceptance criterion says 'quoting the sentence the document must carry' and the branch only described it. Describing is the riskier option here: a paraphrase of a registered discrepancy is very easily a QUALIFIED version, and a qualified D-002 is true and stops being a benchmark item. The brief prints the sentence and says 'your wording may differ; its strength may not.' All 5 registered sentences were checked and are verbatim in their documents.

NUMBERS WERE LEFT OUT OF THE YAML ON PURPOSE. The branch's `why` fields repeat the set-points and design centres (pH 3.5 vs 3.6, protein load 200 vs 175, and so on). Those live in config/parameters.yaml and are tabulated in DISCREPANCIES.md, so a third copy would go stale quietly. The YAML points at the table instead. I did verify the four I could read directly against the config: viral_inactivation hold time 90 vs centre 120 and temperature 21 vs 20, virus_filtration volume 90 vs 95 and pressure 13 vs 19. All match DISCREPANCIES.md.

SECTION NUMBER is 5c, matching the branch and the yaml's own meta.surfaced_as, so a later rebase does not conflict. 5b is already taken: WRITING_GUIDE.md line 651 says 'If your brief has no §5b, every claim you write must be grounded', which is the weak-claims section that never appears on main.

Acceptance, all six: PCR-003's brief names D-002 and quotes its sentence, and that sentence is still live in the document; PCP-003's brief carries D-001 with the at-set-point commitment; 20/20 briefs have a 5c section with 12 empty; weak_claims.yaml and build_weak_claims_annex.py are untouched by git status and no weak_claims code path was added; weak_claims is empty in 20/20 annexes; build_ground_truth + validate_annex give 20/20 valid with git status on ground_truth/ empty; pytest 85 passed. make style exit 0, 24 OK.

FOR TASK-007: PCP-003's brief has been regenerated and its 5c carries D-001. The pilot must write the at-set-point commitment. It was previously safe only because section_plan.yaml lines 315 and 535 happen to say the same thing.

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCP-006** — `pc_package/PCP-006_viral_inactivation.qmd`
- **PCP-008** — `pc_package/PCP-008_aex.qmd`
- **PCP-009** — `pc_package/PCP-009_virus_filtration.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`
- **PCR-006** — `pc_package/PCR-006_viral_inactivation.qmd`
- **PCR-008** — `pc_package/PCR-008_aex.qmd`
- **PCR-009** — `pc_package/PCR-009_virus_filtration.qmd`

## Files it touched

- `authoring/build_brief.py`
- `authoring/discrepancies.yaml`
