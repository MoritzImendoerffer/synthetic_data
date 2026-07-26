# One-pass authoring — handoff

Pick-up notes for a fresh Claude Code session. Assume no prior conversation
context; everything needed is here or linked. Branch: `claude/pharma-corpus-expansion-plan-jh2i13`.

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
- `pc_package/PCR-008_aex.qmd` is the existence proof: it is the densest report,
  written **directly at full depth**, in the corpus's own voice, already carrying
  narrated deviations (DEV-01/DEV-02). One pass can produce the target. Its voice is
  now **distilled** into `authoring/REGISTER_EXEMPLAR.md`, so authoring no longer
  depends on the report file.
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
- `REGISTER_EXEMPLAR.md` — distilled gold excerpts from PCR-008 (voice, with no report present).
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

**Shipped (this session): the full PCR-003 report.** `pc_package/PCR-003_bioreactor.qmd`
is authored end-to-end (15 sections, ~30–35 pp), replacing the superseded minimal version.
One agent authored it from the artifacts alone; the hard gate is clean (22 chunks, 105
inline exprs, no `<<NEEDS:>>`) and a real `quarto render --to docx` succeeds. It hosts the
three labeled weak claims and the rhetorical layer (both re-grounded against it). The
`.DRAFT.qmd` was the validation intermediate and has been retired. Two small artifact
refinements are still worth making: (a) a one-line "which-CQA-is-tightest / σ-margin" recipe
for `cap_for` in the brief; (b) an *indexed* frame example (`.set_index(...)`) in the
template SETUP hint. Neither blocked authoring.

**Also shipped: the full PCR-008 (anion exchange).** `pc_package/PCR-008_aex.qmd`
authored one-pass from the artifacts (generalization test passed): 19 headings, the PAR
section, and the DEV-008-01 twice-run-DoE narrative from the real superseded dataset. Hard
gate clean; real render succeeds. Both PCR-003 and PCR-008 carry the Proven-acceptable-ranges
section.

**Next**
- **Rebuild the ground-truth annexes** for PCR-003 and PCR-008 from the new full text
  (`build_ground_truth.py`). The committed `ground_truth/PCR-00{3,8}.json` target the *old*
  versions, so `check_grounding` for them is stale — and merge in the PCR-003 weak-claims
  (`support=unsupported`) and rhetorical (roles + argument graph) layers, and add the PAR /
  linguistic layers for PCR-008.
- **PCR-008 weak-claims + rhetorical layers** (PCR-003 has them; PCR-008 does not yet).
- Then the remaining reports/plans, each with its PAR + weak-claims + rhetorical layers.

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
- **Weak-claims benchmark feature.** A few deliberately unsupported/overstated claims are
  planted and LABELED (`authoring/weak_claims.yaml`, `authoring/WEAK_CLAIMS.md`,
  `authoring/build_weak_claims_annex.py` → `authoring/out/<DOC>.weak_claims.json`). They
  ground (the quote exists in the doc) but are labeled `support=unsupported` in the annex.
  Injected/registered by the maintainer, never by the authoring agent; the render/numeral
  gates deliberately don't catch prose overstatement, so the label lives in the annex.
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

## 6. Grounding facts for the two test targets

**PCR-003 — Production Bioreactor (USP; first target).** key `bioreactor`, step 3. Params:
pH, temperature, co2, osmolality, duration (WC-CPP); do, ivcc, feed_vol (KPP); medium_conc
(GPP). CQAs it SETS: afucosylation, galactosylation, high_mannose, aggregates_hmw,
acidic_variants, hcp, residual_dna. DoE step — 5 CQA responses; the design-space step.
Seeded deviations: DEV-003-01 (pCO2 probe drift; `EQ-BRX-205`; **retained**) and DEV-003-02
(feed-1 under-delivery; `LOT-FED-3120`; **retained**) — both minor, a bounded-impact
argument, *not* a re-executed DoE. See `authoring/out/PCR-003.brief.md`.

**PCR-008 — Anion Exchange (generalization test).** key `aex`, step 8. Flow-through polish:
SETS the MVM viral-clearance CQA (tightest Cpk); clears XMuLV/HCP/DNA/leached-PA. This is
the step with the **twice-run DoE** (deamidated-load first execution → re-executed on
requalified load) + the UV pool-stop correction. Task 9 seeds the superseded dataset and
moves these deviations into `config`. `REGISTER_EXEMPLAR.md` was distilled from the current
`PCR-008_aex.qmd`; author a fresh version and compare register + grounding.

---

## 7. Pointers

- Writing standard: `authoring/WRITING_GUIDE.md`
- World canon + grounding map: `authoring/STORY_BIBLE.md`
- Voice (distilled, no report needed): `authoring/REGISTER_EXEMPLAR.md`
- Section outlines + per-section instructions: `authoring/section_plan.yaml`
- The build loop: `authoring/RUNNER.md`; independence proof: `authoring/check_blank_repo.sh`
- Helpers: `pc_package/_pcpkg.py`, `pc_package/doe_report.py`
- Gates: `authoring/check_render.py`, `ema_docgen/scripts/lint_numerals.py`,
  `pc_package/check_grounding.py` (annex step)
- Source of truth: `config/parameters.yaml` (`deviations:` key); corpus conventions:
  `CLAUDE.md`. Prior two-pass rationale: `ema_docgen/DESIGN.md`.

---

## 8. First action for a fresh session

1. Read `authoring/WRITING_GUIDE.md`, `authoring/STORY_BIBLE.md`,
   `authoring/REGISTER_EXEMPLAR.md`, `authoring/section_plan.yaml`.
2. `uv run python authoring/build_brief.py PCR-003`; eyeball `authoring/out/PCR-003.brief.md`.
3. Instantiate `authoring/template.qmd` → `pc_package/PCR-003_bioreactor.qmd`; have **one
   agent** author it in section order, bound with the artifacts above. Gate with
   `uv run python authoring/check_render.py pc_package/PCR-003_bioreactor.qmd --render`.
4. Prove independence any time: `bash authoring/check_blank_repo.sh`.
