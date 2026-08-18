# Exploration — Track D: bring the whole corpus to one register

**Proposal:** `docs/next/register-from-four-sources.md`, Track D. This unit does not restate it.
**Predecessors:** three shipped rounds — `2026-08-16_01_register-from-four-sources` (pilot),
`2026-08-17_01_register-second-round`, `2026-08-18_01_register-third-round`.
**Date:** 2026-08-18. **Written by:** `/explore`.
**Opened on the project owner's instruction**, not off the ROADMAP order: "all documents should
be re-authored".

## 1. What is actually true today, measured rather than assumed

Every number below is from one invocation each of `check_style.py --compare` and
`check_discourse.py` over all 20 `.qmd`, saved as `measure_baseline_style.txt` and
`measure_baseline_discourse.txt` in this unit.

**Eighteen of twenty documents are still at round-zero register.** Only `PCP-003` (round two) and
`PCR-003` (round three) have been re-authored.

| | sources | the 18 untouched | PCP-003 | PCR-003 |
|---|---|---|---|---|
| mid-sentence `, so ` | 0.1–0.4 % | **6.3–14.6 %** | 0.0 | 0.0 |
| opens with a connective | 3.7–6.1 % | **0.0–2.4 %** | 4.9 | 3.7 |
| `, and ` + second clause | 1.1–3.4 % | **16.3–29.3 %** | 18.2 | 0.5 |
| `, not ` | 0.0–0.2 % | 0.0–1.0 % | 0.0 | 0.0 |
| topic chaining | 56–62 % | **28.9–39.5 %** | 46.0 | 47.6 |
| adjunct front field | 28–37 % | **6.0–12.5 %** | 22.4 | 30.2 |
| copula main verb | 13–26 % | 13.2–33.6 % | 21.9 | 16.5 |
| passive construction | 57–64 % | **44.2–67.7 %** | 55.2 | 57.4 |

**Two of those rows change how the round must be instructed.**

- **The passive is not a floor for this corpus, and for several documents it is a ceiling.**
  `PCP-005` sits at 66.7 %, `PCP-008` at 67.7 %, `RA-001` at 64.2 % — all above the source band.
  An instruction that says "write more passives", which is how round three's rule reads if it is
  copied without its band, would push those three the wrong way. The brief already states it as a
  band; the per-document task must not restate it as a floor.
- **Chaining and front field are the two large, universal gaps** — every one of the eighteen is
  20 to 30 points below the sources on both. Neither has ever been set as a target, and both moved
  a long way in `PCR-003` anyway, purely from being printed as context.

## 2. Every claim in the proposal, checked

The proposal was rewritten one hour before this unit opened, so most of it is current. Three
things it says are incomplete, and one number in it is now the wrong scope.

- **"21–44 re-anchored annex quotes per document"** — true as a per-document figure, but the
  proposal quotes it from rounds that touched documents with 105 and 177 quotes. The corpus
  ranges from **35 quotes (`PCP-009`) to 317 (`RA-001`)**, and the re-anchoring cost scales with
  the quote count. Measured today, per document: PCMP-001 69, PCMR-001 273, PCP-003 105,
  PCP-004 42, PCP-005 66, PCP-006 55, PCP-007 67, PCP-008 74, PCP-009 35, PCP-010 37,
  PCR-003 177, PCR-004 85, PCR-005 123, PCR-006 102, PCR-007 110, PCR-008 114, PCR-009 80,
  PCR-010 77, PTP-001 76, RA-001 317. Total **2084**. At round three's rate — 22 of 177, or
  12 % — the whole corpus is roughly **250 quotes to re-anchor**, and `RA-001` and `PCMR-001`
  alone are a fifth of it.
- **"the full curated rhetorical layer where a document has one"** — the proposal implies one
  mechanism. There are **two**, and only one of them is gated. `PCR-003` has 35 spans in
  `authoring/rhetorical/PCR-003.spans.yaml`, checked by `build_rhetorical_annex.py`, which
  **fails hard** on a stale quote. The other **eight** documents carry **280 spans hard-coded in
  eight Python functions inside `build_ground_truth.py`** — `h_` (PCR-004, 36), `pa_` (PCR-005,
  39), `vi_` (PCR-006, 31), `cx_` (PCR-007, 33), `ax_` (PCR-008, 25), `vf_` (PCR-009, 37), `uf_`
  (PCR-010, 30), `pcmr_` (PCMR-001, 49). Those functions emit **every** span unconditionally,
  with no presence check, so a stale one is caught only later, by `check_grounding.py`, as an
  ungrounded quote. **315 spans across 9 documents** have to be re-cut, and 280 of them by hand
  inside a 7600-line Python file.
- **"eleven documents carry no rhetorical layer"** — verified true: `PTP-001`, `RA-001`,
  `PCMP-001` and the eight `PCP-00N`.
- **Registered discrepancies: the proposal says "both survived every re-author" and leaves it
  there. There are eight documents carrying one, not two.** `D-001` lives in `PCP-003`,
  `PCP-006`, `PCP-008`, `PCP-009`, `PCR-006`, `PCR-008` and `PCR-009`; `D-002` in `PCR-003`.
  `TASKS.md` item 7 is explicit that a re-authored document silently loses its discrepancy unless
  the brief carries it, and that losing the prose half while the generated half survives leaves
  the annex asserting something the document no longer says. **Seven documents in this round are
  exposed to that**, against one in round three.

Everything else holds. Verified by running:

- `build_brief.py` produces a brief for **all** document types, including the four that have never
  been re-authored (`PTP-001`, `RA-001`, `PCMP-001`, `PCMR-001`), and each brief carries §5c, §5d
  with all twelve rows, and the helper inventory.
- `section_plan.yaml` carries **seven** doc-type outlines — `report_doe`, `report_nondoe`, `plan`,
  `transfer_plan`, `risk_assessment`, `master_plan`, `master_report` — which covers all 20.
- The corpus is at 2084/2084 quotes grounded with strict anchors, 20/20 annexes valid,
  `make test` 89 passed, `make style` 24 OK / 0 FAIL.

## 3. What this round cannot learn from the previous three

Rounds one to three each re-authored one or two documents and measured them against four human
sources. Track D is a different shape and two of the campaign's habits do not transfer.

- **There is no control column left.** Every previous round held something fixed. If all 19 move,
  a measure that moves is a measure that moved everywhere, and nothing distinguishes "the
  instruction works" from "the corpus drifted together". The only remaining control is the
  four human sources themselves, which do not change.
- **The owner's reading cannot cover 19 documents.** Three rounds were decided by a person reading
  one or two rendered PDFs and quoting what gave them away. That does not scale, and the round-three
  reading already showed the limit of a fourth read by the same reader. This round has to decide in
  advance what the human check is: a sample of documents chosen before the numbers are seen, or a
  reading of the two genres that have never been read (`RA-001`, `PTP-001`), or none.

## 4. What the work touches, by layer

| Layer | Files | Cost |
|---|---|---|
| document | 19 of the 20 `pc_package/*.qmd` | one one-pass re-author each; `PCR-003` is already at the newest rules and is the one to leave alone |
| annex | `build_ground_truth.py` (7600 lines, per-step prefixed regions), 19 of 20 `ground_truth/*.json` | ~250 quotes re-anchored, 315 rhetorical spans re-cut across 9 documents |
| machinery | none required | the gates, the guide and the brief already carry everything round three added |
| model | none | `outputs/` must be unchanged at ship |

**`build_ground_truth.py` is one file, and that is the parallelism constraint.** Its builders are
prefixed per unit operation (`h_`, `pa_`, `vi_`, `cx_`, `ax_`, `vf_`, `uf_`, plus the PTP/RA/PCMP/
PCMR blocks), so the *regions* two documents touch are disjoint — but two agents editing one file
concurrently lose each other's writes. Authoring is the opposite: each document is its own new
file and nothing is shared.

## 5. Ground rules that bite here

- **Prose changes → one-pass re-author, never a patch**, and never from a sibling `.qmd`. With 19
  documents in flight the sibling-copying loop is the single largest risk in this unit, and it is
  the one that already cost the project a full corpus re-author once.
- **Seven documents must carry `D-001` through the re-author**, one must carry `D-002`. Brief §5c
  is the carrier; re-verify `registered_sentence` against the new text afterwards and update
  `discrepancies.yaml` and `DISCREPANCIES.md` together when the wording moves.
- **The passive is a band, never a floor.** Three documents are already above it.
- **No number changes.** Nothing in `config` moves; `git diff outputs/` empty at ship.
- **Nothing is added to a document after authoring.** Grounding failures are fixed by re-anchoring.
- **`weak_claims` stays empty in all 20 annexes**; that feature lives only on
  `feature/weak-claims-via-brief` and is never merged.
- **The two-extractor trap**: `check_grounding.docx_text` yields `R2`, `build_rhetorical_annex.doc_text`
  yields `R²`. Test every span under both before any builder runs.
- **`check_render.py --render` renders docx only** and glyph-checks whatever PDF is on disk. Every
  document needs an explicit PDF render, or the glyph gate passes on a stale file.

## 6. What could go wrong

- **The guide is rewritten later and all 19 need doing again.** This is the sharpest risk and it is
  not hypothetical: Track C is the proposal's own leading hypothesis, and `WRITING_GUIDE.md`
  commentary measures at 3.77 % `, so ` and 10.38 % `, and ` + clause against sources at 0.1–0.4 and
  1.1–3.4. Authoring 19 documents from an artifact that is itself the suspected cause, and then
  fixing the artifact, is the most expensive possible order. **This is a decision for the project
  owner and it belongs in the plan as one, not in a task.**
- **Doing 280 code-built spans by hand.** `docs/next/rhetorical-layer-coverage.md` already proposes
  unifying the two mechanisms. Doing that first would turn 280 hand edits inside a 7600-line Python
  file into YAML with a hard gate — and the same proposal wants the layer extended to eleven more
  documents, which is work this round will otherwise make harder.
- **A silent discrepancy loss in one of seven documents.** No gate catches it.
- **Concurrency in `quarto`.** Round two ran two authoring agents at once and both gated with
  `check_render`, which renders into `pc_package/`. Two is proven; more is not, and Quarto keeps a
  `.quarto` cache directory per project.
- **Cost.** One data point: round three's `PCR-003` author took about 62 minutes and 577k tokens for
  a 56-page report. Reports are 26–56 pp and plans 23–31 pp, so 19 documents is a large multiple of
  that however it is sequenced.

## 7. Questions this exploration cannot answer

1. **Track C first, or Track D first?** See §6. The owner's call, and the plan is written both ways.
2. **Is `PCP-003` in scope?** It is at round two and never saw the three measures round three added
   — its `, and ` + clause is still 18.2 %. Re-authoring it makes the corpus one register; leaving it
   makes the corpus three. This exploration assumes **19 documents: all except `PCR-003`**.
3. **What is the human check, given a reading cannot cover 19 documents?** Must be fixed before the
   numbers are seen, as every previous round's stopping rule was.
