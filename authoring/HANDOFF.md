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
  narrated deviations (DEV-01/DEV-02). One pass can produce the target.
- The additive approach's headline advantage — a matched minimal/full pair with
  identical ground truth (a length ablation) — is a *bonus research artifact*,
  not the stated goal (documents long enough that retrieval is actually tested),
  and the annexes are **generated** (`pc_package/build_ground_truth.py`), so
  rebuilding them is cheap. The trade favours the simpler one-pass build.

Keep two things from the two-pass design (they were load-bearing, not
brittleness): **numeral enforcement** (every number from the model, never typed),
and vigilance against **uniform prose** (the tell of a synthetic corpus). But note
the architecture rule below: **one document is written by one agent**, so
uniformity is handled by the writing guide's deliberate per-section register
variation — *not* by isolating section contexts. A single author is also what makes
the document-scale arc, cross-references and coreference/restatement work at all;
splitting sections across agents is precisely what forced `ema_docgen`'s brittle
ledger.

`ema_docgen/` stays in the repo for now; the one-pass system supersedes only its
*densification layer*. Reused from it / the wider repo: the single source of truth
(`config/parameters.yaml` → `amab_process/` → `outputs/`), the `_pcpkg.py` /
`doe_report.py` helpers, the seeded deviation facts, the gates
(`check_grounding.py`, `lint_numerals.py`, `lint_overlap.py`), and the move-taxonomy
content (now folded into `authoring/WRITING_GUIDE.md`).

---

## 2. Target architecture (the one-pass build loop)

```
per report <DOC> (e.g. PCR-003):
  1. build_brief.py <DOC>        -> authoring/out/<DOC>.brief.md   (grounded facts + helper inventory)
  2. ONE agent authors the whole document, in order, holding it all in one context.
        inputs: WRITING_GUIDE.md + <DOC>.brief.md + the section plan
              + PCR-008_aex.qmd as register/helper-usage exemplar
        writes the body into the standard template scaffold (4d)
        -> pc_package/<DOC>_<uokey>.qmd   (all numbers = inline exprs)
  3. gate:  check_render.py + lint_numerals.py            (dry gate; render for real if quarto present)
  4. annex (separate, deliberate step): extend build_ground_truth.py, then validate_annex + check_grounding
```

**One document = one agent.** A single author is what gives the arc,
cross-references and coreference/restatement — the whole point of the guide.
Uniformity is prevented by the guide's deliberate per-section register variation
(§4/§7 of the guide), not by splitting the document across agents. The annex is
authored **from the final text** (build-then-annex), which is why one-pass makes
span-grounding trivially satisfiable.

---

## 3. Status

**Done**
- `authoring/WRITING_GUIDE.md` — the writing standard. Four structural scales
  (OCAR arc / SCQA section / CCC paragraph / Gopen–Swan sentence) + a rigor
  overlay (grounding, screening-identifies-RSM-predicts, bounded conclusions,
  calibrated hedging, adverse-before-mitigation, cross-step credit, deferral names
  a location) + voice, tables, the absolute numbers rule, anti-patterns, and a
  per-section self-check. Read it first.

**Not started** (build order below): `build_brief.py`, the section plan,
`check_render.py`, `assemble.py`, `RUNNER.md`. Then run on PCR-003, then PCR-008.

---

## 4. Build order + specs for what's left

### 4a. `authoring/build_brief.py`  →  `authoring/out/<DOC>.brief.md`
Generate the grounded brief for one report from the model. Resolve
`<DOC>` → unit-op key via `_pcpkg.DOC_REGISTRY["<DOC>"]` (3rd tuple element is the
key, e.g. `PCR-003` → `bioreactor`). Emit markdown with:
- identity: doc id, class, UO name, step, `_pcpkg.UNIT_OP_ROLE[key]`.
- CQAs in scope: `cqas_for(key)` (CQAs this step *sets*) and, for clearance steps,
  `cqas_by_keys([...])` for the ones it governs — with acceptance + criticality.
- parameters: `report_params(key)` (name, unit, set-point, NOR, PAR, class, study).
- DoE structure **if a DoE step** (`bioreactor, protein_a, viral_inactivation, cex,
  aex, virus_filtration`): factors `st.DOE_FACTORS[key]`, responses
  `st.DOE_RESPONSES[key]`, RSM subset `st.RSM_TOP.get(key)`, run counts
  `doe_runs(key,'screening')` / `doe_runs(key,'rsm')`. Non-DoE steps (`harvest`,
  `ufdf`) present univariate/qualitative only — do NOT fabricate a DoE.
- seeded deviations: `dev_register("<DOC>")` (markdown table) + the deviation
  scalar names for this doc (grep `outputs/report_values.json` `dev_scalars`).
- cross-refs: `related_docs_md("<DOC>")`, plus the step's SOP/AMV subset
  (`_pcpkg.<KEY>_SOP_REFS` / `_AMV_REFS`).
- **helper inventory** (the important part): enumerate callables in `_pcpkg` and
  `doe_report` with a one-line purpose (pull `inspect.signature` + first docstring
  line), the deviation scalar names, and a note that numbers are inline
  expressions. This is the author's menu; without it they emit `<<NEEDS:>>`.

### 4b. Section plan
Machine-readable section list per report (or one shared plan keyed by report
type: DoE-report vs non-DoE-report vs plan). Canonical **report** order (from
`CLAUDE.md`), with the scaffold + register + rigor obligations per section — this
is the PCR-003 plan; adjust the deviation IDs / non-DoE handling per report:

| # | section_id | heading | scaffold | register | key rigor obligations |
|---|---|---|---|---|---|
| 1 | exec_summary | Executive summary | SCQA (answer-first, whole-doc resolution) | defensive | bounded_conclusion, capability margin, explicit non-claim |
| 2 | introduction | Introduction (product, UO, objectives, regulatory basis) | OCAR opening | procedural | step linkage; broad→narrow |
| 3 | prior_knowledge | Prior knowledge & quality risk basis | SCQA | argumentative | conservative default, discretionary band, risk basis from RA-001 |
| 4 | materials_methods | Materials & methods (SDM & qualification, operation, analytical methods, sampling, statistics) | CCC | procedural/defensive | scale-down qualification warrant, assay variance attribution, deferral names a location |
| 5 | study_design | Study design (factors/ranges, screening, RSM, univariate) | SCQA | analytical/argumentative | factor-inclusion rationale (justify the RANGE) |
| 6 | results | Results (centre-point reproducibility, screening effects, RSM + ANOVA & diagnostics, mechanistic interpretation) | CCC per subsection | analytical | table narration, mechanistic warrant, null-result→classification, **screening identifies / RSM predicts** |
| 7 | design_space | Design space | SCQA | analytical | worst-case identification, bounded conclusion |
| 8 | capability | Process capability | CCC | analytical | capability-margin statement, cross-step credit |
| 9 | parameter_classification | Parameter classification | SCQA | argumentative | null-result→classification, conservative default |
| 10 | control_strategy | Contribution to the control strategy | SCQA (resolution) | argumentative | cross-step credit, explicit non-claim |
| 11 | discussion | Discussion | CCC | argumentative | mechanistic warrant, bounded conclusion |
| 12 | conclusions | Conclusions | SCQA | defensive | bounded conclusion, explicit non-claim |
| 13 | deviations | Deviations | SCQA + table | defensive | deviation disposition, adverse-before-mitigation, `dev_register("<DOC>")` table narration |
| 14 | references | References | — | — | `# References {.unnumbered}` + `::: {#refs} :::` |
| 15 | appendices | Appendices A–D (screening matrix, RSM matrix, full effect/coeff tables, analytical methods) | table narration | boilerplate | design-matrix / coeff-table helpers |

Length is emergent (WRITING_GUIDE §7) — assign a band per section if you want a
lint, but never instruct the agent to hit a word count.

### 4c. `authoring/check_render.py`  (dry-render gate — needed because cloud has no quarto)
Parse a `.qmd`: extract every inline `` `{python} EXPR` `` and every fenced
`{python}` chunk, and evaluate them against a `from _pcpkg import *` +
`from doe_report import *` namespace (cwd = `pc_package/`) to confirm they resolve
(catch NameError / typos / bad helper calls). Report any `<<NEEDS:>>` markers.
Then run `ema_docgen/scripts/lint_numerals.py` on the file for bare numerals.
**If quarto IS present locally**, also `quarto render <doc>.qmd --to docx` and run
`pc_package/check_grounding.py` for the real grounding gate.

### 4d. `authoring/template.qmd` (the scaffold the single author fills; optional thin `assemble.py`)
So the one author doesn't retype boilerplate, give it a standard scaffold with the
corpus-standard front matter + setup chunk + closing; it writes the body sections
(§4b) between the setup chunk and the References. There are no fragments to stitch —
`assemble.py`, if you want one at all, only drops the authored body into the
template and confirms the file is under `pc_package/`. Copy the exact structure from
`pc_package/PCR-008_aex.qmd`: YAML front matter (docx `reference-doc: reference.docx`
+ pdf `documentclass: scrreprt`, `bibliography: references.bib`, `toc-depth: 3`,
`number-sections: true`, `execute: echo:false warning:false cache:false`,
`jupyter: python3`); first code chunk `sys.path.insert(0, os.path.abspath(".")); from _pcpkg import *`;
`title_block(DOC, UO_TITLE)` + `SYN_BANNER`; Approvals + Abbreviations; closing
`# References {.unnumbered}` + `::: {#refs} :::`. The file MUST live in
`pc_package/` for the relative paths (`FIG = "../outputs/figures"`, `sys.path`) to
resolve.

### 4e. `authoring/RUNNER.md`
The loop an orchestrating agent follows (mirror the clarity of
`ema_docgen/RUNNER.md`, minus the splice/ledger machinery): generate brief →
**one agent authors the whole document** (bind WRITING_GUIDE + brief + section plan
+ PCR-008 exemplar; it writes every section in order into the template, holding the
whole document in context so the arc, cross-references and restatement cohere) →
gate → report. **One document = one agent** — do NOT split a document's sections
across agents; that breaks coherence and coreference and reintroduces the ledger
problem. Different *documents* may be authored by different agents in parallel.

---

## 5. Environment & commands

- **Scientific stack is under `uv`**, not bare `python3` (numpy/pandas/scipy/
  statsmodels missing from system python). Always: `uv run python ...`.
- Tests: `uv run --with pytest python -m pytest -q tests/` (8 tests; keep green).
- **No quarto in the cloud env** — use `check_render.py`. A local session likely
  HAS quarto 1.7+ (see `CLAUDE.md`); if so, render for real and use the true
  grounding gate.
- Regenerate model data: `uv run python scripts/generate_data.py`.
  ⚠ **Output drift:** regenerating in a different library environment shifts the
  DoE/effects CSVs in the deep decimals (BLAS/lib-version float noise). The
  committed `outputs/data/*.csv` are the ground-truth baseline. **Before committing
  any `outputs/` change, `git diff` it** — commit deviation/new outputs only, not
  drifted `doe_*`/`effects_*` baselines. (This is a real reproducibility gap in the
  pipeline worth pinning the stack for; out of scope here.)

---

## 6. Grounding facts for the two test targets

**PCR-003 — Production Bioreactor (USP; the first target).** key `bioreactor`,
step 3. Parameters: pH, temperature, co2, osmolality, duration (WC-CPP); do,
feed_vol, ivcc (KPP); medium_conc (GPP). CQAs it SETS: afucosylation,
galactosylation, high_mannose, aggregates_hmw, acidic_variants, hcp, residual_dna.
DoE step — 5 CQA responses; this is the **design-space step** (richest arc).
Seeded deviations: DEV-003-01 (pCO2 probe drift; equipment EQ-BRX-205) and
DEV-003-02 (feed-1 under-delivery; lot LOT-FED-3120, method AMV-3010). Deviation
scalars: `dev_003_01_offset_mmhg`, `dev_003_02_feed_deficit_pct`,
`dev_003_02_ver_n`, `dev_003_02_ci_hw`; register via `dev_register("PCR-003")`.
Fact content: `ema_docgen/factpack/PCR-003/dev_0{1,2}.yaml`.

**PCR-008 — Anion Exchange (the generalization test).** key `aex`, step 8. This
is **also the register exemplar** — read it before authoring PCR-008, and match
its density/voice without copying sentences. Flow-through polish: SETS the MVM
viral-clearance CQA; clears XMuLV/HCP/DNA/leached-PA. Already has DEV-01/DEV-02
written directly in `PCR-008_aex.qmd` — for the test, author a fresh version and
compare register + grounding against the committed one.

---

## 7. Pointers

- Writing standard: `authoring/WRITING_GUIDE.md`
- Register exemplar: `pc_package/PCR-008_aex.qmd`; content baseline for PCR-003:
  `pc_package/PCR-003_bioreactor.qmd` (the current minimal version)
- Helpers: `pc_package/_pcpkg.py`, `pc_package/doe_report.py`
- Gates to reuse: `pc_package/check_grounding.py`, `ema_docgen/scripts/lint_numerals.py`,
  `ema_docgen/scripts/lint_overlap.py`
- Source of truth: `config/parameters.yaml`; deviations under its `deviations:` key
- Corpus conventions: `CLAUDE.md` (front matter, section order, golden rules)
- Prior design rationale (for the two-pass approach we're superseding):
  `ema_docgen/DESIGN.md`

---

## 8. First action for the local session

1. Read `authoring/WRITING_GUIDE.md` and `pc_package/PCR-008_aex.qmd`.
2. Build `authoring/build_brief.py`; run it for PCR-003; eyeball the brief.
3. Have **one agent** author PCR-003 against the guide + brief + section plan —
   start with a few sections to validate register + grounding, then continue the
   *same* agent through the full report. Then gate.
