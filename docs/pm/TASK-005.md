---
type: pm-task
epic: 2026-08-18_01_register-third-round
sprint: 2026-08-18_01_register-third-round
task: TASK-005
status: todo
kind: annex
title: "Promote the draft, render both formats, re-anchor the PCR-003 annex and spans, and re-ground the corpus"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCP-003", "PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-18_01_register-third-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-005 — Promote the draft, render both formats, re-anchor the PCR-003 annex and spans, and re-ground the corpus

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-005.md — the previous unit's TASK-007 procedure for one document. THIS IS THE BOUNDARY THAT MUST CLOSE. RE-CURATE THE SPANS FIRST or build_ground_truth writes nothing. THE TWO-EXTRACTOR TRAP is recorded in HANDOFF and cost a cycle in round two: test every span under both before the builder; a span containing 'R²' passes one and fails the other. Row quotes survive a re-author untouched (round two: every table-row quote held); only prose quotes move. Re-anchor to the sentence in the NEW text that names the record; never edit the document to fit a quote. Only PCR-003's builder strings change; the plan's (', and PCP-003 …' branches, ' if report else') stay. If git status shows PCP-003.docx/.pdf or any other annex modified, a full make corpus ran — restore each by NAME.

## Acceptance criteria

- [ ] the DRAFT replaces pc_package/PCR-003_bioreactor.qmd; docx and pdf rendered explicitly; check_render.py reports 0 missing glyphs on the FRESH pdf; page count recorded
- [ ] authoring/rhetorical/PCR-003.spans.yaml re-curated against the new text; every span tested against BOTH extractors (build_rhetorical_annex.doc_text yields 'R²', check_grounding.docx_text yields 'R2') before the builder runs; `uv run python authoring/build_rhetorical_annex.py --doc PCR-003 --file pc_package/PCR-003_bioreactor.docx` writes 35 spans (or the new count, stated) and drops none
- [ ] `cd pc_package && uv run python build_ground_truth.py && uv run python validate_annex.py` → 20/20; `GROUNDING_STRICT_ANCHORS=1 uv run python check_grounding.py` → N/N with 0 weak anchors, N reported against 2084 and the number of PCR-003 quotes re-anchored stated (round two: 23 quotes, 33 spans)
- [ ] D-002's registered_sentence re-verified verbatim against the new .qmd; DISCREPANCIES.md quotes the new wording if it moved; 'leached Protein A' does not occur in the report
- [ ] PCP-003's annex and rendered files are byte-identical to HEAD (git status does not list them); `git diff --stat outputs/` empty; `make test` and `make style` pass; both annexes' weak_claims still empty

**Depends on:** [[TASK-004]]

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- `pc_package/PCR-003_bioreactor.qmd`
- `pc_package/build_ground_truth.py`
- `authoring/rhetorical/PCR-003.spans.yaml`
- `authoring/discrepancies.yaml`
- [[DISCREPANCIES]] — `authoring/DISCREPANCIES.md`
