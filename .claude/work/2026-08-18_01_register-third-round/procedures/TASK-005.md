# TASK-005 procedure — promote, render, re-anchor, re-ground (one document)

**Follow `../../2026-08-17_01_register-second-round/procedures/TASK-007.md` top to bottom, for
`PCR-003` only.** Substitutions:

| there | here |
|---|---|
| "both drafts" / "both documents" | `PCR-003` only; `PCP-003_bioreactor.qmd`, its renders and its annex are **not touched** and must be byte-identical to HEAD at the end (`git status` must not list them) |
| step 3, spans | same, and **before running the builder** run the both-extractor test — `build_rhetorical_annex.doc_text` (reads `word/document.xml`, yields `R²`) and `check_grounding.docx_text` (yields `R2`) — over every span; round two lost a cycle at RS-J02 to exactly this. The scratch script is described in HANDOFF §3a and in `docs/results/2026-08-18-register-round-two.md` "What was found on the way" |
| step 4, misses | only the `if report` branches and report-only strings in `build_ground_truth.py` change; every `else` (plan) branch stays; the plan's annex must rebuild byte-identical |
| step 5 | D-002 only (`PCR-003`); D-001 is the plan's and is untouched |
| step 8, what may be modified | `PCR-003_bioreactor.qmd/.docx/.pdf`, `build_ground_truth.py`, `ground_truth/PCR-003.json`, `authoring/rhetorical/PCR-003.spans.yaml`, `authoring/out/PCR-003.rhetorical.json`, `discrepancies.yaml`, `DISCREPANCIES.md`, the brief. **Nothing else.** |

Round two's numbers for this document, to compare against: 23 quotes re-anchored, 33 of 35 spans
re-cut, 59 pages, N stayed at 2084/2084.
