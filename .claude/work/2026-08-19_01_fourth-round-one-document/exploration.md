# Exploration — the fourth round: one whole document under the rebuilt apparatus

**Proposal:** `docs/next/register-from-four-sources.md`, what remains of it (the 2026-08-19
pointer at its top). This unit does not restate it.
**Predecessor:** `2026-08-18_03_author-facing-apparatus` (shipped 2026-08-19; results
`docs/results/2026-08-19-apparatus-probe.md`). Its `measure_apparatus.py` is the measurement tool
and its `procedures/REVIEW-BEFORE-PROMOTION.md` is the content-review step; both are committed there.
**Date:** 2026-08-19. **Written by:** `/explore`, on the owner's command.

## 1. What is true today

- **The apparatus is rebuilt and green.** `check_style.GATED` = 5 tics + `BANNED`, `--review` for the
  reviewer (`--selftest` 4 of 4); `section_plan.yaml` carries no `scaffold:`/`register:`/`rigor:`;
  `WRITING_GUIDE.md` is 122 lines and passes its own gate; `authoring/mechanism/*.yaml` × 8, all
  `reviewed_by_owner: 2026-08-19`; `build_brief.py` emits §2b and no §5d; `RUNNER.md` step 3 lists
  the author's inputs without obligations and step 4 has the reviewer line; `REVIEW_CHECKLIST.md`
  has the Content block. Corpus: 20/20 valid, 2084/2084 grounded, `make test` 95, `make style`
  24 OK (the probe files are gone).
- **The register of the corpus, by round:** `PCR-003` at round three (owner: "reads better, ok"),
  `PCP-003` at round two, `PCP-007` / `PCR-005` / `RA-001` at the Track D pilot (owner rejected
  `PCR-005`'s prose on eight sentences), **fifteen documents at round zero.** No document has yet
  been authored under the rebuilt apparatus as a whole; only two subsections of `PCR-005` were, as
  the untracked probe (content preserved in the predecessor's `A.pdf`).
- **The brief for a per-UO document now reads:** §1–§2 identity and attributes, **§2b mechanism**
  ("reviewed by owner: 2026-08-19"), §3 parameters, §4/§4b DoE and PARs, §5 deviations, §5c
  discrepancies, §6 cross-references, §7 helpers. Total author input for `PCR-007`, measured:
  brief 25,498 chars plus `WRITING_GUIDE.md` + `section_plan.yaml` + `STORY_BIBLE.md` +
  `REGISTER_EXEMPLAR.md` = **21,403 words** (the exemplar is 10,389 of them; the pilot's total was
  29,454, of which the guide alone was 7,835). Not one of those words is a counter.

## 2. The candidate document, and why: `PCR-007` (Cation Exchange, Step 7)

The proposal leaves the document unnamed. Measured facts that decide it:

| candidate | genre | quotes / spans | discrepancy carrier | owner has read it | mechanism file |
|---|---|---|---|---|---|
| **`PCR-007` cex** | DoE report | 88 / 33 | **no** | **no** (the owner read `PCP-007`, the plan, in the Track D pilot) | `cex.yaml`, reviewed |
| `PCR-006` viral inactivation | DoE report | 82 / 31 | yes (D-001 assignment) | no | reviewed |
| `PCR-009` virus filtration | DoE report | 70 / 37 | yes | no | reviewed |
| `PCR-008` aex | DoE report | 83 / 25 | yes | no | reviewed |
| `PCR-004` / `PCR-010` | non-DoE report | 76 / 36, 68 / 30 | no | no | reviewed |
| `PCR-005` protein_a | DoE report | 97 / 39 | no | yes, four times | reviewed |
| any `PCP-00N` | plan | 29–66 / 0 | four of eight | `PCP-003`, `PCP-007` yes | reviewed |

`PCR-007` is a full DoE report (screening + RSM, so the mechanistic subsection the whole campaign
turns on is exercised), carries no registered discrepancy (nothing to preserve by wording), has a
mid-sized annex, and **the owner has never read it, so the shipped and the new versions can be read
blind against each other**, which no re-read of `PCR-003` or `PCR-005` can offer (the proposal's
own "fourth reading" limit). It is the recommendation, not the decision; the decision is the owner's
and goes to `/plan` as D5.

**`PCR-007` today, measured** (`measure_baseline_PCR-007.txt`, `check_style_baseline_PCR-007.txt`,
this unit): 51 pages, 439 sentences, 10,677 words of prose; passes the five-tic gate. Register at
round zero on every axis the campaign has measured, sources in brackets: `, which` **10.5** per 100
sentences (0.6–2.4); all trailing relatives **11.9** (1.2–3.0); `acts on / through` **2.05** (0);
`governs / sets` **2.05** (0); mid-sentence `, so ` **10.3 %** (0.1–0.4); opens with a connective
**0.7 %** (3.7–6.1); `, and `+clause **21.6 %** regex / **26.5 %** parser (1–3.4); passive **48.8 %**
(57–64); topic chaining **37.2 %** (56–62); copula **31.1 %** (13–26); `its` **5.81** per 1k
(0.27–0.40). One `behaves as`. This is the "before".

## 3. Claims in the proposal, checked

| claim | result |
|---|---|
| "18 of 20 documents have not been touched" | stale: 15 at round zero after Track D's three (`PCP-007`, `PCR-005`, `RA-001`) |
| Track D budget: 21–44 re-anchored quotes per document; every table-row quote survives; the whole rhetorical layer re-cut; explicit PDF render; a read of every report-summary statement | stands, and now the **content review** (`REVIEW-BEFORE-PROMOTION.md`) is added before promotion |
| "test every span against both extractors" (`docx_text` → `R2`, `doc_text` → `R²`) | stands; `PCR-007.spans.yaml` header says so, 33 spans |
| Track C (the guide's register) as a candidate | superseded: the guide was replaced on 2026-08-19 |
| the two count-led candidates (`, which`, staccato) | `, which` is now measured by `measure_apparatus.py` and is exactly the family the probe moved (28.8 → 6.7); the staccato is in its `extra` block; neither is gated, per the proposal's own rule |
| the open scope question (Track C vs a both-genres check) | superseded by the rebuild; the open question now is *one report* first, then whether a plan behaves the same |
| "no blind test involving these documents can be valid" (of `PCR-003`) | still true of `PCR-003` and `PCR-005`; **not** true of `PCR-007`, which is why it is the candidate |

**The proposal stands, reduced to its last paragraph.**

## 4. What the work touches, by layer

| layer | files | notes |
|---|---|---|
| **document** | `pc_package/PCR-007_cex.qmd` (one-pass re-author into `PCR-007_cex.DRAFT.qmd`, promoted only after the review), its `.docx`/`.pdf` | the whole document, one agent, one pass, `RUNNER.md` as it now stands; the agent derives its own SETUP scalars from the helper inventory (no shipped chunk this time — the probe borrowed `PCR-005`'s; a whole document cannot) |
| **annex** | `pc_package/build_ground_truth.py` (the `_cx_*` region), `authoring/rhetorical/PCR-007.spans.yaml` (33 spans), `pc_package/ground_truth/PCR-007.json` | 88 quotes; table-row quotes rebuild themselves; prose quotes and every span re-anchored; report-summary statements re-read |
| machinery | none intended; `measure_apparatus.py` and `REVIEW-BEFORE-PROMOTION.md` reused from the predecessor by path | if a helper is missing (`<<NEEDS:>>`), `_pcpkg.py`/`doe_report.py` extend and `make test` runs |
| measurement | `docs/results/2026-08-<dd>-fourth-round-PCR-007.md` | the reading verbatim first, then the before/after on the same script |

## 5. Ground rules that bite

- **Prose changes** → the whole document, one agent, one pass, no sibling `.qmd`, not the shipped
  `PCR-007` either. `authoring/check_blank_repo.sh` is the proof that nothing under `pc_package/*.qmd`
  is needed.
- **A number changes?** No. Every value through helpers; a missing one is `<<NEEDS:>>` and a helper
  extension, never a typed number.
- **Registered discrepancy?** None for `PCR-007` (`discrepancies.yaml`: PCP-003/006/008/009,
  PCR-003/006/008/009). If the owner picks `PCR-006/008/009` instead, brief §5c carries the
  assignment and TASKS.md item 7 applies.
- **Annex around the text, never the reverse.** Grounding failures re-anchor the quote; the annex's
  report-summary statements are re-read, not re-quoted.
- **Weak claims** — `main` only, `weak_claims` empty in 20/20; untouched.
- **`nlp_reports` / `annex_contract`** — read-only; untouched.

## 6. What could go wrong

- **The whole-document arc.** The probe wrote two subsections; a whole report has to hold an
  executive summary that matches its conclusions, cross-references that resolve, and a SETUP chunk
  it writes itself. That is the RUNNER's normal case and it is what Track D's three authors did; the
  difference now is what they read. If the agent asks for a helper that does not exist, extend the
  helper, do not type the number.
- **The reading is 2 × ~50 pages.** Blind A/B of two whole reports is a long read. `/plan` should
  offer the owner a fixed subset — the executive summary, Results (screening + RSM + mechanistic),
  Design space, Discussion — as the read, with the whole document available; the previous readings
  all landed in Results.
- **Re-anchoring is the cost.** 88 quotes and 33 spans, of which the prose ones all move; the
  predecessor's `ANNEX-A-BATCH.md` is the tested loop, and the `R2`/`R²` extractor trap is real.
- **The content review will find things.** Calibrated on the probe, the four questions flagged
  seven sentences in 90 in the text the owner preferred. Expect a return-to-author cycle before
  promotion; that is the design, and it costs one same-agent pass.
- **Rendered pairs drift.** A re-render of one document rewrites only its own `.docx`/`.pdf`; commit
  those two and nothing else under `pc_package/` (memory: `verification-toolchain-gap`).

## 7. Open questions for `/plan`

1. **Which document.** `PCR-007` recommended (§2). Owner's call → D5.
2. **What the owner reads.** Whole documents blind, or a fixed subset of sections from each? Both
   PDFs will exist; the recommendation is the subset, with the whole document offered.
3. **What "pass" means for a whole document.** The probe's rule (probe preferred and < 3 sentences
   quoted) was for two subsections. For a 50-page report the plan needs a rule fixed in advance
   again — e.g. new preferred, and no more than N sentences quoted from it across the read subset.
4. **Promotion.** If the reading passes, does the new `PCR-007` ship (re-anchor its 88 quotes and
   33 spans, ~a day) — or is the reading itself the deliverable and the shipping a separate call?
   The proposal says "before nineteen", which reads as: ship it, then decide about the rest.
