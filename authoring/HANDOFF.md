# One-pass authoring — handoff

Pick-up notes for a fresh Claude Code session. Assume no prior conversation context;
everything needed is here or linked.

**Status: the corpus is finished.** All 20 documents are authored, rendered, annexed and
grounded, on `main`. This file explains how it was built and what to respect when changing
it. It is not a build list — do not follow it top to bottom and re-author a document that
already exists.

---

## 1. The decision this implements

We are replacing the two-pass **additive densification** harness (`ema_docgen/`)
with **one-pass, full-depth authoring, report by report**. No backward
compatibility with the minimal documents is required.

Why the pivot (so you don't re-litigate it):

- `ema_docgen`'s densify-a-minimal-doc-then-splice approach is brittle: many
  components (docspec ↔ factpack ↔ helper names ↔ splice ↔ ledger) coupled by
  string convention rather than gates, and the tool shipped with real bugs
  (it had never been run).
- The first full-depth one-pass reports proved that a single agent can produce the target
  length and structure. One pass can produce the target.
- The additive approach's headline advantage — a matched minimal/full pair with
  identical ground truth (a length ablation) — is a *bonus research artifact*,
  not the stated goal, and the annexes are **generated**
  (`pc_package/build_ground_truth.py`), so rebuilding them is cheap. The minimal docs
  remain recoverable from git history, so the trade is reversible, not lossy.

Keep two things from the two-pass design: **numeral enforcement** (every number from
the model, never typed) and vigilance against **uniform prose**. But the architecture
rule is **one document is written by one agent**, so uniformity is handled by the
writing guide's deliberate per-section register variation — *not* by isolating section
contexts. A single author is also what makes the document-scale arc, cross-references
and coreference/restatement work; splitting sections is what forced `ema_docgen`'s
brittle ledger.

`ema_docgen/` stays in the repo for now; the one-pass system supersedes only its
*densification layer*. Reused from it / the wider repo: the single source of truth
(`config/parameters.yaml` → `amab_process/` → `outputs/`), the `_pcpkg.py` /
`doe_report.py` helpers, the seeded deviation facts, and the numeral lint
(`ema_docgen/scripts/lint_numerals.py`).

---

## 2. Target architecture (the one-pass build loop)

```
per report <DOC> (e.g. PCR-003):
  1. build_brief.py <DOC>   -> authoring/out/<DOC>.brief.md   (grounded facts + helper inventory)
  2. instantiate authoring/template.qmd -> pc_package/<DOC>_<uokey>.qmd
  3. ONE agent authors the whole document, in section order, holding it all in one context.
        bound inputs: WRITING_GUIDE.md + <DOC>.brief.md + section_plan.yaml
                    + REGISTER_EXEMPLAR.md (voice) + STORY_BIBLE.md (world canon)
        writes the body into the template scaffold; all numbers = inline exprs
  4. gate:  check_render.py --render   (dry eval + numeral advisory + real quarto render)
  5. annex (separate, deliberate step): extend build_ground_truth.py, then validate_annex + check_grounding
```

**No first-pass `.qmd` is a runtime input.** Authoring depends only on config → model
→ `outputs/`, the `_pcpkg`/`doe_report` helpers, and the `authoring/` artifacts. The
corpus reports are prior knowledge, distilled once into `authoring/`.
`authoring/check_blank_repo.sh` proves independence: it moves every `pc_package/*.qmd`
aside and runs the pipeline on a generated probe.

**One document = one agent.** The single author gives the arc, cross-references and
restatement. The annex is authored **from the final text** (build-then-annex), which is
why one-pass makes span-grounding trivially satisfiable. Note the corollary
(review finding): build-then-annex grounds *text ↔ annex*, not *text ↔ model* — both
derive from the same author — so the real correctness anchor is the brief's **helper
inventory** (concept → exact expression). Keep it precise.

---

## 3. Status

**Done (this session)** — the distillation artifacts + infra, all under `authoring/`:
- `WRITING_GUIDE.md` — the writing standard (read first).
- `STORY_BIBLE.md` — world canon + grounding map (fact → helper) + campaign storyline.
- `REGISTER_EXEMPLAR.md` — verbatim passages from the published human sources (voice).
- `section_plan.yaml` — machine-readable outlines: `report_doe`, `report_nondoe`, `plan`,
  each section with scaffold / register / rigor / per-section instructions.
- `template.qmd` — the standard scaffold (instantiated into `pc_package/<DOC>_<uokey>.qmd`).
- `build_brief.py` → `authoring/out/<DOC>.brief.md` — grounded facts + helper inventory
  (config→model→helpers only; auto-detects a superseded study).
- `check_render.py` — namespace-accurate dry gate (execs chunks + evals inline exprs in
  one namespace) + `<<NEEDS:>>` scan + numeral lint (advisory; `--strict-numerals` to gate)
  + real `quarto render` with `--render`.
- `RUNNER.md` — the one-pass loop (no splice/ledger).
- `check_blank_repo.sh` — static guard + functional blank-repo proof.

**Shipped: the full 20-document corpus, one pass per document.** Every `PCP-00N` / `PCR-00N`
for Steps 3–10, plus `PTP-001`, `RA-001`, `PCMP-001` and `PCMR-001`. Each was authored
end-to-end from the `authoring/` artifacts alone by a single agent, with **every existing
`.qmd` physically moved off disk during generation** so no author could copy a sibling's
voice. All pass the authoring gate and the register gate.

### 2026-07-28/29 — the whole corpus regenerated (Claude Opus 5)

All 20 documents were re-authored from scratch on `feature/weak-claims-via-brief`, because
17 of them predated the current machinery. Every `.qmd`, `.docx` and `.pdf` was moved off
disk first, so the blank-repo condition held for every author. Per document: one agent
authored it and drove it through `check_render.py --render` itself, an independent reviewer
read it adversarially against the brief and the outline without editing anything, and a
third agent applied the findings and re-gated. Baseline tag: `pre-recreate-20260728`.

What that pass is worth knowing for:

- **The adversarial review earns its cost.** Across 20 documents the reviewers raised 43
  blocking and 111 major findings *in documents that had already passed every hard gate*.
  The gates prove chunks execute, the render succeeds and the register is human-like. They
  prove nothing about truth. The recurring defect is a sweeping summary sentence printed
  directly above the table that contradicts it — for example "it separates the active factors
  cleanly for every response" two lines above a fit table showing two models not significant.
- **Re-anchoring the annex is where false ground truth is found.** `check_grounding` asks
  whether a quote *exists*, so it is blind to a record that exists and is wrong. Re-anchoring
  the 13 regions corrected records asserting a measured galactosylation exceedance the new
  report only predicts, a design space over three parameters where the report defines four
  and says the worst case is interior, and no-impact edges for parameters the report reports
  interacting significantly. A prospective plan was again found asserting characterization
  outcomes it cannot have.
- **Registered discrepancies are now assigned through the brief** (§5c,
  `authoring/discrepancies.yaml`). D-002 had already been lost silently to a re-authoring;
  see `DISCREPANCIES.md` rule 5.
- **Two machinery bugs came from authors refusing to write something false**, which is the
  grounding rule working: `fig_vf` drew a typed 4.62 "log floor" that is an A-Mab case-study
  observation rather than this model's back-calculated 3.89 floor, and a deviation lot was
  attributed to a factorial run whose design conductivity contradicted the recorded re-test.
- **Quarto trap:** referencing the same markdown-image figure twice silently breaks the first
  reference, which renders as a bare numeral instead of "Figure N.M", in both docx and pdf.
  Repeated *table* references are unaffected. Reference each image figure once.

---

## 3a. Perturbations applied to the model and tooling during the corpus build

Everything below changed the corpus or the machinery *outside* the authoring loop. Recorded
here because each one alters what documents say or how they are checked, and because several
were found by authors refusing to write something incoherent — which is the grounding rule
working as intended.

**Model / world-canon changes (change what documents state).**

| Change | Effect |
|---|---|
| `config`: bioreactor `do`, `medium_conc`, `feed_vol` `study: multivariate` → `univariate` | They are factors of no design. Bioreactor now reads 5 multivariate / 4 univariate; campaign totals 22 / 15 (were 25 / 12). |
| `outputs/data/parameter_classification.csv` regenerated | Was stale against the config above. See the post-mortem below. |

**Tooling changes (change what is checked or how it renders).**

| Change | Why |
|---|---|
| Unicode font block (`mainfont`/`sansfont`/`monofont`/`mathfont`: DejaVu) added to every document and to `template.qmd` | The LaTeX default font had no glyph for `≥`, `≤` or Unicode sub/superscripts, so PDFs carried **398 missing-glyph boxes across 8 documents**. `≥ 4.93` rendered as `␀ 4.93`, turning a clearance *floor* into a point value. |
| `check_render.py`: new `check_pdf_glyphs` hard gate | Nothing had ever inspected the PDF after rendering, which is why the above shipped unnoticed. |
| `check_style.py`: strip markdown images before measuring | An image caption fused with the preceding sentence (its `!` is not a sentence boundary) and inflated the measured length of both. |
| `check_style.py`: sentence-length and parenthesis bands made **two-sided** | One-sided caps let the first regeneration over-correct into staccato: 17-word mean, 41 % of sentences under 15 words, parentheses near zero. |
| `doe_report`: public `predict` / `to_coded` / `to_natural` / `meets_acceptance` / `planned_matrix_df` | Authors were reaching into `_predict_points` and re-implementing the responses-stripped design matrix. Missing API, not author error. |
| `ema_docgen/scripts/lint_numerals.py`: allow-file compiled with `re.MULTILINE` | The `^`-anchored ordered-list rule never matched, so every numbered list was flagged. |
| `tests/test_config.py`: new file, 11 tests | Config↔DoE invariants, plus **CSV↔config agreement** (see post-mortem). |
| `build_ground_truth.py`: weak claims and rhetorical spans skip/fail on mismatch | A stale curated layer used to degrade silently; a dropped rhetorical span is now a hard failure. |

**Post-mortem: the stale-CSV bug (worth reading before touching `config`).** Commit
`641d19a` asserted that `study` is display-only metadata and therefore did not require
regenerating `outputs/`. That was **wrong**: `plan_params()` / `report_params()` render
`parameter_classification.csv`, not `CFG`. The config said `univariate`, the CSV still said
`multivariate`, and the prose was edited to match the config — so the shipped PCP-003 read
"…are assessed univariately (Table 6)" while Table 6 said `multivariate`. The prose edit made
it *worse*: before it, prose and table at least agreed. `tests/test_config.py` passed
throughout, because it read `CFG` directly and never compared against the generated artifact.
The lesson is general: **a config invariant that never looks at the generated file cannot
catch drift into the rendered corpus.** `test_generated_parameter_table_matches_config` now
closes it.

**Annex-layer findings from the re-grounding pass.** All 20 annexes were re-grounded against
the new text (1338/1338 quotes). Re-anchoring surfaced records that were not merely
*unanchored* but **false** — ground truth asserting the opposite of its document, which is
worse than a missing record:

- `PCR-004` asserted turbidity stays within its NOR; the report records DEV-004-02, an
  excursion that exceeded it.
- `PCR-005` asserted the step-yield model is "adequate and predictive" (predicted R² 0.586,
  used descriptively) and that `end_of_pool_collect` does *not* affect pool HCP (it does).
- `PTP-001`, a prospective plan, asserted a drug-substance yield and a parameter
  classification — both characterization outcomes that cannot exist when it is written.
- `PCP-007` asserted a design space over pool aggregate *and* HCP; HCP does not bound it.

**Generic quotes ground while attesting nothing.** Found independently by three agents.
`check_grounding` verifies a quote *exists*, not that it is *specific*: `RA-001` used one
placeholder sentence to anchor 41 separate assertions, and bare spans like "acceptance
criteria" passed trivially. The convention the agents converged on, now the corpus standard:
anchor each per-record assertion on the **rendered table row** carrying the relation, built
from the same DataFrame the document renders, so the span contains both ends. `PCMR-001`'s
`_md_rows` / `_grid_rows` helpers are the reference implementation — note they must reproduce
tabulate's cell wrapping, or a row containing a hyphen-broken cell (`re- assayed`) will not
ground. Tracked as a gate to add.

**Seeded-data defects found but NOT changed** (each is a tracked decision, not an oversight):
the acidic-variants acceptance range is printed as 18–40 but only the ceiling is enforced
(making it two-sided would move the headline min Cpk from 1.51 to 1.03); the three equipment
`cal_due` dates pre-date `EFFECTIVE_DATE`, so calibration reads as overdue while
`calibration_status` says otherwise; and `DEV-005-01` says a buffer was prepared *below* target
at pH 3.38 but is tied to an RSM run whose design target is 3.20.

**Registered discrepancies (`authoring/DISCREPANCIES.md`).** One finding was promoted from
"defect to fix" to "benchmark item to keep": the PAR analysis holds the other factors at the
design centre while all four affected protocols commit to holding them at their set-points, and
the reports present the result under a column headed "PAR (set-point)". It is a real protocol
deviation, cross-document, and partially masked because midpoint and set-point coincide at
three of the six DoE steps. `doe_report.par_at_setpoint` was renamed to `par_at_design_centre`
so the **code** is honest; the column heading, the plans and the annex field name are left
alone so the **documents** still carry it. Read `DISCREPANCIES.md` before touching any of
them — the rule there is that an unregistered inconsistency is a bug, but removing a
registered one deletes a benchmark item.

**The register correction (important — this is why the reports were rewritten).** The
first-pass reports read as machine-written, and the cause was a feedback loop in the
artifacts themselves: `REGISTER_EXEMPLAR.md` had been distilled *from* `PCR-008_aex.qmd`,
which was itself AI-authored against an early `WRITING_GUIDE.md`. The guide then taught the
voice back to the next author. Measured against the two published human sources, the
first-pass prose ran to a 34-word mean sentence (human: 23–27), 10–13 em-dashes per 1000
words (PDA TR 60: 1.9; A-Mab: **zero**), 9–15 semicolons per 1000 (human: 2), and coined
compounds like "the quality-attribute-richest characterization in the campaign". What was
done about it:

- `REGISTER_EXEMPLAR.md` is rebuilt entirely from **verbatim** PDA TR 60 and A-Mab passages
  (88 of them, arranged by the reporting job each performs). No corpus report is a source for
  voice, ever. `authoring/check_exemplar_quotes.py` re-verifies every quote against
  `refs/text/`, so the exemplar cannot silently drift into paraphrase.
- `WRITING_GUIDE.md` §4 is a new, measurable register spec with worked corrections taken
  from the superseded prose. Several older rules were softened because they *manufactured*
  the tells: mandatory per-paragraph significance codas, mandatory restatement in fresh
  words (which produced elegant variation), and "length is defensive" (which grew subordinate
  clauses).
- `authoring/check_style.py` is a new **hard gate**, wired into `check_render.py`. Its
  thresholds are calibrated so that both human sources pass `--selftest`. Rule of thumb: if a
  threshold fails the self-test, the threshold is wrong, not the source.
- **The bands are two-sided, and that was learned the hard way.** The gate shipped with
  sentence length capped but not floored. The first regeneration promptly over-corrected into
  staccato: mean sentence 17 words (human: 24–27), 41 % of sentences under 15 words (human:
  ~20 %), and parentheses almost eliminated (0.6 per 1000 words against ~12 in both sources).
  Prose that is uniformly short is as obviously synthetic as prose that sprawls; it reads like
  a checklist. `mean_len`, `median_len`, `pct_over_40`, `pct_under_15` and `paren` are now
  ranges. When adding any future metric, ask whether an author minimising it produces something
  a human would write — if not, it needs a floor too.
- `refs/text/pda60.txt` is now generated by `scripts/extract_sources.py` alongside `amab.txt`.

**The weak-claim feature was retired, then rebuilt around the brief.** It originally planted
labeled unsupported claims into a report *after* authoring. When the reports were re-authored,
two of the three PCR-003 claims stopped being unsupported and became flat contradictions of
explicit nearby sentences, because the new report settles the questions they overreach on
(notably its honest galactosylation edge of failure). That converts the benchmark task from
evidence grounding to contradiction detection, and every gate passes it — including the
register gate, since the claims sat at the 46th–68th percentile of the document's own
sentence-length distribution with no style markers at all.

It is now **active on its own branch** (`feature/weak-claims-via-brief`), in a form that fixes
the sequencing: claims are assigned in the document's brief *before* it is written, so the
author writes them into the argument and the surrounding prose accommodates them; the wording
is recorded afterwards, which reads the document rather than editing it. Four claims across
three documents. The branch is deliberately **not merged into `main`**, which stays a corpus
where every claim is grounded. Full design, the failure analysis and a
review checklist: `authoring/WEAK_CLAIMS.md`.
Full reasoning and the condition for reviving it: `authoring/WEAK_CLAIMS.md`. The general rule
it establishes is now in CLAUDE.md: **nothing is added to a document after authoring.**

**Next**
- **Re-curate the rhetorical layer** (`authoring/rhetorical/PCR-003.spans.yaml`). Its curated
  spans quote the superseded text; 34 of 37 no longer match and are dropped with a warning.
  This layer is *annotation over existing prose*, so it does not modify the document and is
  unaffected by the weak-claim decision — it simply needs re-curating against the new text.
- **PCR-008 rhetorical layer** (neither report has one that matches the current text).
- Then the remaining reports/plans, each with its PAR + rhetorical layer.
- Optional, deliberate: if labeled benchmark negatives are wanted again, name them in the
  brief so the single author writes them into the argument in one pass (`WEAK_CLAIMS.md`).

---

## 4. Specs / corrections worth carrying forward

- **`build_brief.py` helper inventory is the correctness anchor** (see §2 corollary).
  It enumerates every `_pcpkg`/`doe_report` callable with signature + docstring, the
  structured deviation facts (from `config`), the `dev_*` scalar names, and the CQA/param
  tables. Regenerate after any config/model change.
- **`check_render.py` replicates Quarto's execution model** — one shared namespace, chunks
  then inline exprs in document order. Evaluating inline exprs against a *fresh* import
  would false-NameError on every doc-local variable; do not "fix" it that way.
- **Grounding is NOT an authoring-time gate.** No annex exists when the text is authored;
  the authoring gate is eval + render + no-`<<NEEDS:>>`. `check_grounding.py` runs in the
  *annex* step (step 5), against the rendered `.docx`.
- **Numeral lint is advisory.** The committed corpus itself carries statistical
  conventions (α=0.05, p-thresholds, n, 95% CI) the allow-file deliberately does not
  exempt; the lint flags typed *measurements* to convert to inline exprs, and does not
  hard-fail the gate unless `--strict-numerals`.
- **Deviation prose = Option A** (author writes from the brief's structured facts; the
  register exemplar teaches the moves). Not from the ema_docgen factpack.
- **Weak-claims benchmark feature — ACTIVE, assigned via the brief.** Four labeled negatives
  across three documents (WC-003-01/02 in PCR-003, WC-009-01 in PCR-009, WC-006-01 in
  PCP-006), covering four weakness types and both document classes. Each is **assigned before
  authoring** (`weak_claims.yaml` `assignment:` → brief §5b) so the author writes it into the
  argument, and its wording is **captured after** rendering. Never reinstate the injection
  step; `authoring/WEAK_CLAIMS.md` records why it failed and carries the review checklist.
- **Proven acceptable ranges (PAR).** `doe_report` computes per-CQA×parameter PARs live
  from the fitted RSM (no new outputs). Acceptance = study DS specs, except viral-clearance
  CQAs use a **back-calculated step floor** (cumulative requirement − other steps' credited
  clearance) — `D.acceptance_for(UO, resp)` returns the right criterion. Two flavours:
  `D.par_at_setpoint` (others fixed) and `D.par_nor_propagated` (others varied within NOR by
  seeded Monte-Carlo — the reproducible default; a Bayesian backend can replace
  `_mc_predictive` later). `D.par_table(UO)`, `D.fig_par(UO, resp, D.governing_factor(...))`
  (green-shaded acceptable region). New section `proven_acceptable_ranges` in `section_plan`
  (report_doe + plan). NB: `report_params` "PAR" column is renamed **"Char. range"** — the
  config range is the characterization/knowledge-space range, not a PAR (the PAR is computed).
- **Rhetorical / linguistic-pattern annex layer.** A grounded discourse layer over the
  report text (`authoring/RHETORICAL_ANNEX.md`, `authoring/build_rhetorical_annex.py`,
  curated spans in `authoring/rhetorical/<DOC>.spans.yaml` → `authoring/out/<DOC>.rhetorical.json`).
  Roles: problem_statement, claim, justification, mechanistic_warrant, hedge,
  bounded_conclusion, cross_step_credit, deviation_disposition, deferral, restatement, and
  weak_claim (merged). Relations: `supported_by` (claim←evidence), `restates` (coreference),
  `bounds`. Build-then-annex, curated by an annotator agent and grounded by the builder;
  merges into the GroundTruthAnnex when `build_ground_truth.py` is extended. PCR-003 layer:
  37 spans, 11 argument edges, 3 coreference edges.

Section order + scaffold/register/rigor per section: `authoring/section_plan.yaml`
(the machine-readable form of the CLAUDE.md canonical orders). Length is emergent — the
band is a lint hint, never a target to pad toward.

---

## 5. Environment & commands

- **Scientific stack is under `uv`** (numpy/pandas/scipy/statsmodels missing from system
  python). Always `uv run python …`.
- **Quarto** is present locally (1.10+); render for real via `check_render.py --render`.
  In a cloud env with no quarto, the dry eval + numeral lint still gate.
- Tests: `uv run --with pytest python -m pytest -q tests/` (keep green).
- Regenerate model data: `uv run python scripts/generate_data.py`.
  ⚠ **Output drift:** regenerating in a different library environment shifts the
  DoE/effects CSVs in the deep decimals. The committed `outputs/data/*.csv` are the
  baseline. **`git diff` any `outputs/` change and commit only intended new/changed data**
  (e.g. a new superseded dataset), never drifted `doe_*`/`effects_*` baselines.
- **Rendered `.docx` are git-tracked (21).** While iterating, author under a throwaway
  name (`pc_package/<DOC>_<uokey>.DRAFT.qmd`, whose `.docx` is untracked) so the committed
  baseline does not drift.

---

## 6. Grounding facts for the two documents the method was proved on

These two were the test targets when one-pass authoring was being validated, and they are
still the ones to read first: PCR-003 for structure and depth, PCR-008 for the hardest
narrative in the corpus. Both are built; the facts below are here as orientation, not as a
work order.

**PCR-003 — Production Bioreactor (USP).** key `bioreactor`, step 3. Params:
pH, temperature, co2, osmolality, duration (WC-CPP); do, ivcc, feed_vol (KPP); medium_conc
(GPP). CQAs it SETS: afucosylation, galactosylation, high_mannose, aggregates_hmw,
acidic_variants, hcp, residual_dna. DoE step — 5 CQA responses; the design-space step.
Seeded deviations: DEV-003-01 (pCO2 probe drift; `EQ-BRX-205`; **retained**) and DEV-003-02
(feed-1 under-delivery; `LOT-FED-3120`; **retained**) — both minor, a bounded-impact
argument, *not* a re-executed DoE. See `authoring/out/PCR-003.brief.md`.

**PCR-008 — Anion Exchange.** key `aex`, step 8. Flow-through polish:
SETS the MVM viral-clearance CQA (tightest Cpk); clears XMuLV/HCP/DNA/leached-PA. This is
the step with the **twice-run DoE** (deamidated-load first execution → re-executed on
requalified load) + the UV pool-stop correction. The superseded dataset is seeded and these
deviations live in `config`.

---

## 7. Pointers

- Writing standard: `authoring/WRITING_GUIDE.md`
- World canon + grounding map: `authoring/STORY_BIBLE.md`
- Voice (verbatim human-source passages, no report needed): `authoring/REGISTER_EXEMPLAR.md`
- Section outlines + per-section instructions: `authoring/section_plan.yaml`
- The build loop: `authoring/RUNNER.md`; independence proof: `authoring/check_blank_repo.sh`
- Helpers: `pc_package/_pcpkg.py`, `pc_package/doe_report.py`
- Gates: `authoring/check_render.py`, `ema_docgen/scripts/lint_numerals.py`,
  `pc_package/check_grounding.py` (annex step)
- Source of truth: `config/parameters.yaml` (`deviations:` key); corpus conventions:
  `CLAUDE.md`. Prior two-pass rationale: `ema_docgen/DESIGN.md`.

---

## 8. First action for a fresh session

Every document already exists. What you do first depends on what you are here to do.

**Just orienting.** Read `authoring/WRITING_GUIDE.md`, `authoring/STORY_BIBLE.md`,
`authoring/REGISTER_EXEMPLAR.md` and `authoring/section_plan.yaml`, then read PCR-003 as a
finished example. Confirm the corpus is intact:

```bash
cd pc_package && uv run python build_ground_truth.py && uv run python validate_annex.py \
  && uv run python check_grounding.py
```

**Changing what a document says.** Change `config/parameters.yaml`, run
`make data figures`, and let every document and annex follow. If the *prose* has to change,
re-author the whole document in one pass — never patch a paragraph, because the register gate
measures the document as a whole and a stale annex quote will strand. Then rebuild the annex
and re-anchor any quote the change broke.

**Adding a document.** `uv run python authoring/build_brief.py <DOC>`, instantiate
`authoring/template.qmd`, and have **one agent** author it in section order bound only to the
artifacts above — never to a sibling `.qmd`. Gate with
`uv run python authoring/check_render.py <path> --render`.

**Any time:** `bash authoring/check_blank_repo.sh` proves authoring does not depend on an
existing document.
