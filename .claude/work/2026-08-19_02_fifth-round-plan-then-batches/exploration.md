# Exploration — the fifth round: one plan first, then the batches

**Proposal:** `docs/next/register-from-four-sources.md`, its 2026-08-19 pointer ("what remains").
This unit does not restate it. **Owner's decision (2026-08-19, in the conversation that opened this
unit):** `PCP-005` first; then, if it passes, the rest in batches with the regime frozen and one
sampled reading per batch. **Predecessors:** `2026-08-18_03_author-facing-apparatus` (the rebuild),
`2026-08-19_01_fourth-round-one-document` (PCR-007 passed; its procedures are the tested loop).
**Date:** 2026-08-19. **Written by:** `/explore`.

## 1. What is true today

- **One report is at the rebuilt register.** `PCR-007`, preferred blind, promoted, 2084/2084
  grounded, 20/20 valid. `PCR-003` at round three, `PCP-003` at round two, `PCP-007` / `PCR-005` /
  `RA-001` at the Track D pilot, fourteen at round zero.
- **The loop is tested end to end** (`2026-08-19_01_…/procedures/`): `TASK-002.md` (the launch
  prompt = the RUNNER's invocation line), `READING.md`, the content-review prompt in
  `2026-08-18_03_…/procedures/REVIEW-BEFORE-PROMOTION.md`, the annex loop in
  `2026-08-18_02_…/procedures/ANNEX-A-BATCH.md`, and the transcript audit by tool-input grep.
  `RUNNER.md` step 3 now says the author runs `check_render` and nothing else on its draft.
- **No plan has been authored under the rebuilt apparatus.** Plans are half the corpus, have no
  rhetorical layer and no mechanistic subsection, and fell into different traps in rounds one and
  two (the copula/expletive trade in `PCP-003`). The brief for a plan now carries §2b (the step's
  mechanism) and no §5d; `build_brief.py PCP-005` → `## 2b` 1, `## 5d` 0, §5c "None".

## 2. `PCP-005` today, measured

`measure_baseline_PCP-005.txt`, `check_style_baseline_PCP-005.txt` (this unit): **31 pages, 192
sentences, 4,605 words**; passes the five-tic gate. Round zero on the campaign's axes, sources in
brackets: `, so ` **11.5 %** (0.1–0.4); opens with a connective **0.0 %** (3.7–6.1); `, and `+clause
**26.6 %** regex / **35.4 %** parser (1–3.4); topic chaining **30.9 %** (56–62); copula 13.2 %
(inside); **passive 66.7 %** (57–64 — above the band, the plan genre already sits high); `, which`
5.7 per 100 sentences (0.6–2.4); all trailing relatives 5.7; `acts on / through` 1.56 (3);
`governs / sets` 2.08 (4); `its` 8.25 per 1k (0.27–0.40).

Why this plan: no registered discrepancy (`discrepancies.yaml` carriers among plans are `PCP-003`,
`PCP-006`, `PCP-008`, `PCP-009`), never read by the owner, 48 annex quotes and no spans (the
cheapest possible re-anchor), its mechanism file (`protein_a.yaml`) reviewed. Its author reads
**21,415 words** (brief 24,991 chars + guide + plan + bible + exemplar).

## 3. The remaining eighteen, sized

| batch (plan, overrulable) | documents | quotes / spans | discrepancy carrier | notes |
|---|---|---|---|---|
| this unit's pilot | `PCP-005` | 48 / 0 | no | the plan-genre test, read blind |
| B1 reports | `PCR-006`, `PCR-008`, `PCR-009`, `PCR-010` | 82/31, 83/25, 70/37, 68/30 | `PCR-006`, `PCR-008`, `PCR-009` (D-001) | three carry D-001: brief §5c must survive, TASKS.md item 7 |
| B2 reports | `PCR-004`, `PCR-003`, `PCR-005` | 76/36, 118/35, 97/39 | `PCR-003` (D-002) | `PCR-003` round three and `PCR-005` Track D re-done for one register; `PCR-004` non-DoE |
| B3 plans | `PCP-004`, `PCP-006`, `PCP-008`, `PCP-009`, `PCP-010` | 36/0, 44/0, 51/0, 29/0, 31/0 | `PCP-006`, `PCP-008`, `PCP-009` (D-001) | |
| B4 plans | `PCP-003`, `PCP-007` | 66/0, 49/0 | `PCP-003` (D-001) | round two and Track D re-done |
| B5 corpus-level | `PTP-001`, `PCMP-001`, `RA-001`, then `PCMR-001` **last** | 58/0, 43/0, 169/0, 170/49 | none | no §2b (no single step); `PCMR-001` rolls up every PCR and is written last (`section_plan.yaml` note); `RA-001` the largest non-roll-up annex |

Eighteen re-authors, roughly 1,400 quotes of which the table rows rebuild themselves and the prose
moves, 282 spans re-cut. Per document in the fourth round: ~30–45 min authoring, ~10 min review +
one return, ~15–25 min re-anchoring (reports), serial annex step.

## 4. Claims checked

| claim | result |
|---|---|
| proposal: "the other documents, under the same regime, in the owner's order … and whether a plan behaves the way a report did" | stands; the owner's order is given (PCP-005 first) |
| Track D budget list (21–44 quotes per document; every table-row quote survives; whole rhetorical layer re-cut; explicit PDF render; report-summary statements read) | stands; PCR-007 cost 31 of 110 and all 33 spans, three statements rewritten |
| "the regime frozen" | `RUNNER.md` step 3 as of `f2de811`, `WRITING_GUIDE.md` 122 lines, `check_style.GATED` 5, `REVIEW_CHECKLIST.md` with the Content block — none changes in this unit |
| mechanism files reviewed for every step | all eight `reviewed_by_owner: 2026-08-19` |
| `PCMR-001` written last | `section_plan.yaml` line 43 and 406 |

**The proposal stands.**

## 5. What the work touches, by layer

document (nineteen one-pass re-authors, each into a `.DRAFT.qmd`, promoted only after the review
and, where sampled, the reading), annex (`build_ground_truth.py` per-step regions, the span YAMLs
of the eight reports with a layer, `ground_truth/*.json`), measurement (one results page per
batch; `measure_apparatus.py` before/after), machinery: none intended.

## 6. Ground rules that bite

- Prose changes → one agent, one pass, no sibling `.qmd`; the author runs `check_render` only;
  the transcript is audited for `--review` / `check_discourse` / `measure_` / sentence listing
  **before** the draft is read by anyone.
- **Registered discrepancies**: D-001 in `PCP-003/006/008/009`, `PCR-006/008/009`; D-002 in
  `PCR-003`. Brief §5c carries the assignment; the promoted text must carry it in substance;
  `discrepancies.yaml` and `DISCREPANCIES.md` updated together if the wording moves (ANNEX-A-BATCH
  §5). Nothing in `PCP-005`.
- No number changes; no `make data figures`; `outputs/` identical.
- Weak claims `main` only; `nlp_reports`/`annex_contract` untouched.
- **Rendered pairs:** commit only the document's own `.docx`/`.pdf`; `check_render --render`
  rewrites a docx, restore by name.

## 7. What could go wrong

- **A plan is a different genre and the author may not know what a plan is for.** The section
  plan's `plan` class says prospective, `plan_params` not `report_params`, no findings. The
  reading is the test.
- **Passive already above the band in plans** (66.7 % here; `PCP-008` 67.7 %). Advisory only; but
  guide rule 9 ("people decide → passive") could push a plan higher. Not a gate; the owner's
  reading decides.
- **Parallel authors, serial annex.** Two documents at once is fine; `build_ground_truth.py` is
  one file and the annex step is serial per batch.
- **The first `PCR-005` and `PCR-003` re-authors** had 39 and 35 spans; both carry a registered
  discrepancy or the largest annex — schedule them in a batch of their own (B2).
- **`PCMR-001` last**, and its 49 spans include 17 data-row `deviation_disposition` spans built
  from `outputs/deviations.csv` — those rebuild themselves.
- **The owner's sampled readings are the only human check.** One per batch, chosen by the owner
  after the batch is promoted; a failed sample stops the next batch.

## 8. Open questions for `/plan`

1. The pass rule for the plan reading — the same as `PCR-007`'s (new preferred, fewer than five
   sentences quoted)? Recommended yes, unchanged.
2. Batch composition and order as in §3 — overrulable.
3. Whether the sampled reading per batch is blind A/B of one document (recommended: yes, same
   protocol) or a read of the new document alone.
4. Whether the five earlier-round documents are re-done (the owner said "all of it, including the
   five" when recommending; recorded as the assumption).
