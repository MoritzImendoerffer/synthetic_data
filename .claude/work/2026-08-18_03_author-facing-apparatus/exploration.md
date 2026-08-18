# Exploration — the author-facing apparatus, tested on one section first

**Proposal:** `docs/next/author-facing-apparatus.md`. This unit does not restate it.
**Predecessor:** `2026-08-18_02_register-track-d` (stopped after the pilot; its results page is
`docs/results/2026-08-18-track-d-stopped.md`, and its `measure_trackd.py` is reused here).
**Date:** 2026-08-18. **Written by:** `/explore`.

## 1. What is true today, measured

- `make style PY="uv run python"` → 24 OK / 0 FAIL, re-run in this session. The corpus passes the
  gate as it stands.
- The two shipped subsections the probe targets, `pc_package/PCR-005_protein_a.qmd` lines
  747–876 (`## Response-surface models`, `## Mechanistic interpretation`), measured through
  `check_style.prose_from_qmd` + `measure`: **59 sentences, 1,333 words**, mean 22.6, median 21,
  `pct_under_15` 18.6, `pct_over_40` 10.2, em-dash 0, semicolon 0. `evaluate()` returns no
  failure. **`, which` occurs in 15 of the 59 sentences (25 %)**, against sources at 0.6–2.4 per
  100. So the section that drew all eight quotes is clean on every gated row and six to ten times
  over on the one the owner named. This is the proposal's argument in one measurement, and it is
  the baseline the probe is compared against.
- 59 sentences is above `MIN_SENTENCES = 40` (`check_style.py:348`), so a probe of the same two
  subsections will be *evaluated* by the gate, not waved through. Good: the proposal predicts a
  `mean_len` / `pct_under_15` failure and the prediction is testable.
- The two subsections use 36 inline expressions and five `doe_report` helpers
  (`D.fit_summary_df`, `D.rsm_coeff_df`, `D.anova_lof_df`, `D.fig_rsm_contours`,
  `D.fig_diagnostics`) plus doc-local scalars from the SETUP chunk (lines 52–260): `fits_rsm`,
  `rcoef`, `rcoef_p`, `n_sig_rsm`, `n_terms_rsm`, `cp_rsm`, `cvr`, `lpa_*`, `n_pools`. **The probe
  author has to have these** or write `<<NEEDS:>>` for every number in the section (§4).
- The pilot authors were `claude-opus-5` (`../2026-08-18_02_register-track-d/state.json`,
  TASK-003/004/005 outcomes). Confirmed.

## 2. Claims in the proposal, checked

| claim | checked | result |
|---|---|---|
| bound inputs 29,454 words vs a 12,251-word document | `wc -w` re-run | holds (7,835 / 10,389 / 5,849 / 2,019 / 3,362 / 12,251) |
| `section_plan.yaml:203` "Establish the mechanistic expectation now so Results can confirm"; `:273` "state directions + mechanism"; `:280` `Mechanistic interpretation` | `sed -n` | all three lines are exactly that |
| `RHETORICAL_ANNEX.md` ties roles to rigor obligations | read | verbatim: "the roles below are the concrete text-span realizations of the scaffolds (SCQA/CCC) and rigor obligations that `section_plan.yaml` assigns each section" |
| `WRITING_GUIDE.md` 818 lines, 19 ✗ / 18 ✓ | `wc -l`, `grep -c` | holds |
| round three recorded `, which` 9.50 → 15.33 % as a regression | `grep` in `docs/results/2026-08-18-register-round-three.md` | lines 134, 226, 299 |
| `check_style.py` has one `LIMITS` dict and no gated/advisory split, no `--review` | `grep` | holds; CLI is `--selftest`, `--compare`, `--report`, `-v` |
| `check_render.py` prints the whole style table to the author | read lines 222–240 | holds; the register block is `GATE` unless `--lax-style`, which demotes the *whole* gate |
| `build_brief.py` has no mechanism section and no flag to omit §5d | `grep add_argument` → none | holds; §5d is written unconditionally at line 564 |
| A-Mab's Protein A section carries no mechanism | `refs/text/amab.txt` ≈10380–10520 | holds; a table of "Expect higher HCP at low pH", nothing on mass transfer |
| **the five extra counts are not in `measure_trackd.py`** | read lines 60–92 | **partly wrong.** `, which` IS there (`SENT_PATTERNS`, line 74) and reproduces round three cell for cell. Missing are `<quantifier> of which`, `acts on/through`, `follows from`, `governs / sets <noun>`, `aggressive(ness)` and the hollow-warrant frames, and the `mechanistic_warrant` span count. Task 1 adds those, not `, which` |
| `PCR-005` carries no registered discrepancy | `authoring/discrepancies.yaml` | holds; PCR-005 appears only in a note about the bioreactor pair |
| the pilot launch prompt is `AUTHOR-A-DOCUMENT.md` §3 | read | holds; it binds all five inputs and forbids `authoring/rhetorical/` and every `.qmd` |

**The proposal stands.** One correction, above, and one thing it under-states: `tests/test_style.py::test_limits_unchanged` asserts `len(cs.LIMITS) == 12`, so task 2 breaks a test on purpose and must rewrite it.

## 3. What the work touches, by layer

All six tasks are **machinery** (`authoring/`, gates, `docs/`), except that task 1 also writes one
untracked probe `.qmd` under `pc_package/` so `from _pcpkg import *` resolves. No task touches the
model, a shipped document, an annex, `config/`, or `outputs/`.

| task | files | already covered by |
|---|---|---|
| 1 probe | `pc_package/PCR-005_protein_a.PROBE.qmd` (untracked, from `authoring/template.qmd`); `$U/probe-guide.md`; `$U/probe-setup.py` (see §4); `$U/owner-reading-<date>.md`; `../2026-08-18_02_register-track-d/measure_trackd.py` → copied here and extended | `measure_trackd.py --check-baseline` reproduces both committed baselines; keep that green after extending |
| 2 gate split | `authoring/check_style.py` (`LIMITS` → `GATED` + `ADVISORY`, `--review`), `authoring/check_render.py` (`run_style` prints nothing but pass/fail on `GATED`), `tests/test_style.py` (`test_limits_unchanged`), `Makefile` `style` target (unchanged unless `--review` is wanted there), `CLAUDE.md` Voice rule (line ≈133 states the print-back doctrine), `WRITING_GUIDE.md` §4a | `make style`, `make test`, `--selftest` |
| 3 obligations → reviewer | `authoring/section_plan.yaml` (only `build_brief.py:423,443` mention it, as a filename — nothing parses its `rigor:` keys), new `authoring/REVIEW_CHECKLIST.md`, `authoring/RHETORICAL_ANNEX.md` (the one sentence), `authoring/RUNNER.md` step 3 | nothing programmatic; `build_brief.py` on all 20 documents as a smoke test |
| 4 short guide | `authoring/WRITING_GUIDE.md` (rewrite), history → `docs/results/` or `authoring/history/`, `CLAUDE.md` Voice rule, `RUNNER.md`, `template.qmd` comment block (names the guide), `build_brief.py:423` (names it) | `check_exemplar_quotes.py` guards the exemplar only; nothing guards the guide |
| 5 mechanism | new `authoring/mechanism/<uokey>.yaml` × 8, `authoring/build_brief.py` (emit §2b) | `build_brief.py` on all 20; a `grep -cE "[0-9]"` on the prose → 0 |
| 6 content review | `authoring/REVIEW_CHECKLIST.md` (+4 questions), the annex procedure file of the next round | none; recorded per run in the work unit |

## 4. What could go wrong

- **The probe author needs the SETUP scalars.** The shipped subsections rest on ~15 doc-local
  scalars derived in `PCR-005`'s SETUP chunk. If the probe agent must derive them itself from the
  helper inventory, most of its effort goes into code, and a helper mismatch would change the
  numbers between shipped and probe, confounding the reading. Recommendation for `/plan`: extract
  lines 52–260 of `PCR-005_protein_a.qmd` to `$U/probe-setup.py` (code only, comments stripped of
  anything but helper names), and give the agent that file. `RUNNER.md` allows reading
  `_pcpkg.py` / `doe_report.py` "because they are code, not documents"; the SETUP chunk is the same
  kind of thing. The ban is on voice, and a code chunk carries none. The agent still must not open
  the `.qmd`.
- **A section-sized author has no arc to hold.** The probe writes two subsections cold. If it
  reads badly for lack of context, that is not evidence for the apparatus. Mitigation: the probe
  guide names what precedes (screening effects, Table 5.8's role) in one sentence, and the owner
  is told they are reading a section, not a document.
- **Blindness.** The owner has read the shipped text four times today and may recognise it.
  Recorded as a limit; the reading is still the test, because the question is which reads as a
  paper, not which is new.
- **The probe must not touch the shipped document or its annex.** `git status --short pc_package/`
  after the probe must show only the untracked `PROBE` files.
- **Task 2 changes what `make style` fails on.** Every shipped document already passes `GATED`
  (they pass the superset), so no document goes red. But the two-sided length bands stop being
  enforced for future documents, and that is the point; the CLAUDE.md line "Enforced by
  `authoring/check_style.py`, whose thresholds are calibrated so all four human sources pass" stays
  true for `GATED` and has to be reworded for what is now advisory.
- **Task 3 removes text an author has been reading for four rounds.** Anything that quotes the
  scaffold or rigor names must be found: `grep -rn "SCQA\|CCC\|rigor_glossary\|bounded_conclusion"`
  across `authoring/`, `docs/`, `CLAUDE.md`, `pc_package/TASKS.md` before editing.
- **Task 5 is prose written from domain knowledge.** It carries no numbers, so reseeding cannot
  stale it, but it can be *wrong*, and nothing automated will say so. The owner reads each file
  once; the proposal says so and the plan must schedule that read as a halt point.

## 5. Ground rules that bite here

- **A number changes?** No. Every probe number is an inline expression from the same helpers as
  the shipped text.
- **Prose changes?** No shipped prose changes in this unit. The probe is a new untracked file and
  is never spliced into `PCR-005`.
- **Registered discrepancy in scope?** No; `PCR-005` carries none.
- **`annex_contract` / `nlp_reports`?** Not touched.
- **Weak claims?** Not touched; `main` only.
- **Something added to a document after authoring?** No document is edited.

## 6. Open questions for `/plan`

1. Arm B (minimal + `REGISTER_EXEMPLAR.md`): run it, or not? Two readings cost the owner twice.
   Recommendation: run arm A only; if it passes, one whole document under the rebuilt apparatus is
   the next check anyway, and the exemplar question can ride on that.
2. Where do the probe's SETUP scalars come from — `$U/probe-setup.py` extracted from the shipped
   chunk (recommended, §4) or derived afresh by the agent?
3. Does the blind reading go through the rendered PDF (as the four previous readings did) or the
   `.qmd`? PDF, so the inline expressions resolve to the numbers the owner has been quoting.
4. Task 2's `--review`: does the reviewer table also go into `check_render.py` under a flag, or is
   `check_style.py --review` enough? Enough, unless the annex procedure wants one command.
