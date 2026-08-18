---
type: pm-task
epic: 2026-08-18_02_register-track-d
sprint: 2026-08-18_02_register-track-d
task: TASK-001
status: todo
kind: mechanism
title: "Unify the rhetorical layer onto one gated mechanism: 280 code-built spans become YAML"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
about: ["PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-18_02_register-track-d/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-001 — Unify the rhetorical layer onto one gated mechanism: 280 code-built spans become YAML

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-001.md. OWNER DECISION 2026-08-18: unify first. The layer is built two ways today -- PCR-003's 35 spans come from authoring/rhetorical/PCR-003.spans.yaml and are hard-gated by build_rhetorical_annex.py, while the other 280 come from eight Python functions that emit every span UNCONDITIONALLY with no presence check, so a stale one is caught only later by check_grounding as an ungrounded quote. This task is pure refactor: it must not change one byte of any annex. Do it BEFORE any document is re-authored -- afterwards there is no byte-identical baseline to prove the conversion against. It also closes half of docs/next/rhetorical-layer-coverage.md.

## Acceptance criteria

- [ ] authoring/rhetorical/ gains eight files -- PCR-004 (36 spans), PCR-005 (39), PCR-006 (31), PCR-007 (33), PCR-008 (25), PCR-009 (37), PCR-010 (30), PCMR-001 (49) -- carrying the same span ids, roles, sections, quotes and supported_by/restates/bounds edges the Python builders emit today
- [ ] the eight builders (h_/pa_/vi_/cx_/ax_/vf_/uf_/pcmr_ _rhetorical_spans) and their *_RHET_SPANS tables are deleted from build_ground_truth.py, which routes all nine documents through build_rhetorical_spans()
- [ ] `cd pc_package && uv run python build_ground_truth.py` then `git diff --stat pc_package/ground_truth/` is EMPTY -- all 20 annexes rebuild byte-identical, which is the proof the conversion changed nothing
- [ ] `uv run python authoring/build_rhetorical_annex.py --doc <DOC>` runs for all nine and reports 35/36/39/31/33/25/37/30/49 spans, dropping none
- [ ] 20/20 annexes valid and GROUNDING_STRICT_ANCHORS=1 check_grounding.py reports 2084/2084 with 0 weak anchors
- [ ] make test and make style unchanged (89 passed, 24 OK / 0 FAIL)

## Documents it is about

- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- `pc_package/build_ground_truth.py`
- `authoring/rhetorical/`
- `authoring/build_rhetorical_annex.py`
