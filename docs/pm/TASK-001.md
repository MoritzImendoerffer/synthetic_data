---
type: pm-task
epic: 2026-08-18_02_register-track-d
sprint: 2026-08-18_02_register-track-d
task: TASK-001
status: done
kind: mechanism
title: "Unify the rhetorical layer onto one gated mechanism: 280 code-built spans become YAML"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCMR-001", "PCR-003", "PCR-004", "PCR-005", "PCR-008", "PCR-009", "PCR-010"]
---

> [!warning] Generated from `.claude/work/2026-08-18_02_register-track-d/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-001 — Unify the rhetorical layer onto one gated mechanism: 280 code-built spans become YAML

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-001.md. OWNER DECISION 2026-08-18: unify first. The layer is built two ways today -- PCR-003's 35 spans come from authoring/rhetorical/PCR-003.spans.yaml and are hard-gated by build_rhetorical_annex.py, while the other 280 come from eight Python functions that emit every span UNCONDITIONALLY with no presence check, so a stale one is caught only later by check_grounding as an ungrounded quote. This task is pure refactor: it must not change one byte of any annex. Do it BEFORE any document is re-authored -- afterwards there is no byte-identical baseline to prove the conversion against. It also closes half of docs/next/rhetorical-layer-coverage.md.

## Acceptance criteria

- [x] authoring/rhetorical/ gains eight files -- PCR-004 (36 spans), PCR-005 (39), PCR-006 (31), PCR-007 (33), PCR-008 (25), PCR-009 (37), PCR-010 (30), PCMR-001 (49) -- carrying the same span ids, roles, sections, quotes and supported_by/restates/bounds edges the Python builders emit today
- [x] the eight builders (h_/pa_/vi_/cx_/ax_/vf_/uf_/pcmr_ _rhetorical_spans) and their *_RHET_SPANS tables are deleted from build_ground_truth.py, which routes all nine documents through build_rhetorical_spans()
- [x] `cd pc_package && uv run python build_ground_truth.py` then `git diff --stat pc_package/ground_truth/` is EMPTY -- all 20 annexes rebuild byte-identical, which is the proof the conversion changed nothing
- [x] `uv run python authoring/build_rhetorical_annex.py --doc <DOC>` runs for all nine and reports 35/36/39/31/33/25/37/30/49 spans, dropping none
- [x] 20/20 annexes valid and GROUNDING_STRICT_ANCHORS=1 check_grounding.py reports 2084/2084 with 0 weak anchors
- [x] make test and make style unchanged (89 passed, 24 OK / 0 FAIL)

## What was built

The rhetorical layer is one mechanism. 263 curated spans moved out of Python and into eight `authoring/rhetorical/<DOC>.spans.yaml` files, and all nine documents now go through `build_rhetorical_spans()` — the hard-gated path PCR-003 already used.

Proof it changed nothing: `cd pc_package && uv run python build_ground_truth.py` then `git diff --stat pc_package/ground_truth/` is empty and `diff -r /tmp/gt-before pc_package/ground_truth` is silent. All 20 annexes rebuilt byte-identical. build_ground_truth.py is 994 lines shorter and 23 lines longer (net -971).

The spans were emitted, not retyped: a throwaway script imported build_ground_truth, read the eight tuple tables in table order, and round-tripped every file through yaml.safe_load against the source tuples before writing. The ids in the converted YAML are the FULL ids (`PCR-004-R00`, supported_by `["PCR-004-R05"]`), not the suffixes — TASK-001.md step 2 says build_rhetorical_spans prefixes with the doc id, and it does not: it takes `s["id"]` verbatim, which is why PCR-003's spans are bare `RS-P01`. Full ids are what keeps the annex byte-identical.

Two mechanism divergences had to be handled, both found by reading the code rather than the plan.

1. section_id. The Python builders bucketed a whole layer under a flat `<DOC>_sec_rhet`; the YAML path builds `<DOC>_sec_<section title>` per span. Byte-identity needs the flat form for the eight. `build_rhetorical_spans` now reads an optional document-level `section_id:` key and falls back to the per-section form, so PCR-003 is untouched and the eight carry the key. The wart is preserved deliberately and is documented in each converted file's header; normalising the nine onto one form is a separate change that WILL move bytes.

2. PCMR-001 is 49 spans, but only 32 of them are curated prose. The other 17 are rows of the campaign deviation register, built by the old builder from `outputs/deviations.csv` with a table_id and table_title. Freezing a rendered data row into a curated YAML file would hard-code a value that lives in outputs/ (golden rule 1) and break on reseed (rule 2), so they stayed in code as `pcmr_dev_spans()`, appended to the YAML layer at the call site. So the acceptance line "PCMR-001 (49 spans)" reads 32 in the spans file and 49 in the annex. This is the one place the task could not be done as written.

The gate now bites where it did not. Negative test: one span quote in PCR-008.spans.yaml replaced with text not in the document -> `FAIL PCR-008: 1 of 25 rhetorical span(s) do not appear in PCR-008_aex.docx`, build writes nothing. Before this task that span would have been emitted regardless and surfaced only later, as an ungrounded quote in check_grounding.

Gates. build_rhetorical_annex.py over all nine: 35 / 36 / 39 / 31 / 33 / 25 / 37 / 30 / 32 spans, none dropped, all OK (the ninth is 32 for the reason above; the annex holds 49). validate_annex.py: 20/20 annexes valid. GROUNDING_STRICT_ANCHORS=1 check_grounding.py: 2084/2084 quotes grounded across 20 annexes, 0 weak anchors, exit 0. make test PY="uv run python": 89 passed. make style PY="uv run python": 24 OK, 0 FAIL. `git diff outputs/` empty. weak_claims 0 in all 20 annexes. Rhetorical span total unchanged at 315 over 9 documents.

Outside view. Three live claims went false and were corrected in place. `docs/next/rhetorical-layer-coverage.md`: its build table, its "one layer is built two ways" section and steps 1-2 of "What it would take" are now marked done with the date, and the status line says half done — the eleven documents with no layer at all are untouched and are what the proposal is still for. `authoring/RHETORICAL_ANNEX.md`: the note said "Put new layers in the builder, not in a YAML file", which is now backwards; it is rewritten to say what actually closed the silent-degradation failure it was defending against, which was the hard gate and not co-location. `authoring/HANDOFF.md`: the two sentences naming ax_rhetorical_spans and "built two ways".

The per-document rationale in the deleted comment banners was not thrown away. PCR-004's negative argument, PCR-005's leached Protein A cluster, PCR-009's adverse-first spine, PCR-010's what-is-not-claimed and PCMR-001's split were transplanted into the header comments of the corresponding YAML files, where the spans they describe now live.

## Documents it is about

- **PCMR-001** — `pc_package/PCMR-001_master_report.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`
- **PCR-004** — `pc_package/PCR-004_harvest.qmd`
- **PCR-005** — `pc_package/PCR-005_protein_a.qmd`
- **PCR-008** — `pc_package/PCR-008_aex.qmd`
- **PCR-009** — `pc_package/PCR-009_virus_filtration.qmd`
- **PCR-010** — `pc_package/PCR-010_ufdf.qmd`

## Files it touched

- `pc_package/build_ground_truth.py`
- `authoring/rhetorical/`
- `authoring/build_rhetorical_annex.py`
