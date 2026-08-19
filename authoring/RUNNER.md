# Runner — one-pass authoring

The loop an orchestrating agent follows to produce one A-Mab characterization document.
The rule that shapes everything: **one document is written by one agent**, in section
order, holding the whole document in one context. There is no splice, no ledger, no
per-section fan-out — those belonged to the superseded two-pass densifier and are exactly
what broke coherence.

Invoke as:

> Author `PCR-003` (Production Bioreactor) per `authoring/RUNNER.md`.

---

## Preconditions

- **Model outputs exist:** `uv run python scripts/generate_data.py` has been run and
  `outputs/data/*.csv` + `outputs/report_values.json` are present. (The scientific stack is
  under `uv`; always `uv run python …`, never bare `python3`.)
- **You must NOT read any `pc_package/*.qmd`.** Authoring depends only on: `config` → the
  model → `outputs/`, the `_pcpkg` / `doe_report` helpers, the `authoring/` artifacts
  (guide, brief, section plan, register exemplar, story bible, template, and the step's
  mechanism file `authoring/mechanism/<uokey>.yaml`, which the brief carries as §2b), and the
  published human sources in `refs/text/`. `authoring/check_blank_repo.sh` proves this.
- **The mechanism file has been read by the project owner.** `authoring/mechanism/<uokey>.yaml`
  is prose written from domain knowledge with no source to ground it against, which is why its
  `reviewed_by_owner` field carries the date the owner read it. A brief whose §2b says
  "reviewed by owner: not yet" is not ready to author from.

  This is stronger than "not needed". An earlier register exemplar was distilled *from* an
  AI-written report in `pc_package/`, which closed a loop: the machine voice fed itself and
  drifted further from human regulatory prose with each pass. The exemplar is now built from
  the published sources only, and the author must not look at a sibling report for voice.
- **Working tree:** commit or stash unrelated changes so a document's diff is reviewable.

---

## Loop (per document `<DOC>`)

```
1. brief:      uv run python authoring/build_brief.py <DOC>
               -> authoring/out/<DOC>.brief.md   (grounded facts + helper inventory)

2. scaffold:   instantiate authoring/template.qmd -> pc_package/<DOC>_<uokey>.qmd
               (replace __DOC__ / __DOC_CLASS__ / __UO_KEY__ / __UO_TITLE__; delete the
                template comment block). The file MUST live in pc_package/ so
                `from _pcpkg import *`, `../outputs/…` and reference.docx resolve.

3. author:     ONE agent writes the whole document, in section order, bound with:
                 - authoring/out/<DOC>.brief.md    (the grounded facts + helper inventory;
                                                    every number comes from here; §2b is the
                                                    step's mechanism)
                 - authoring/section_plan.yaml     (the doc-type outline: sections, headings,
                                                    helper menus, one sentence of coverage —
                                                    STRUCTURE ONLY, no obligations)
                 - authoring/STORY_BIBLE.md        (world canon + grounding map)
                 - authoring/WRITING_GUIDE.md      (how to write — short and positive)
                 - authoring/REGISTER_EXEMPLAR.md  (voice — the distilled gold excerpts)
               The author is shown NO counter and NO checklist of moves. Measured
               2026-08-19: the section written under exactly this regime was preferred blind
               over the one written under counters and obligations
               (docs/results/2026-08-19-apparatus-probe.md).
               It writes every body section between the SETUP chunk and the References,
               adding any doc-local derived scalars to the SETUP chunk. Numbers are inline
               `{python}` expressions; a value with no helper becomes `<<NEEDS: …>>`.

4. gate:       uv run python authoring/check_render.py pc_package/<DOC>_<uokey>.qmd --render
                 - HARD: every chunk execs, every inline expr evals, no <<NEEDS:>>,
                   quarto render --to docx succeeds.
                 - HARD: the tic gate (authoring/check_style.py GATED) — em-dash, semicolon,
                   colon, bold in a sentence, coined compound, banned phrases. Calibrated so
                   all four human sources pass (`--selftest`). The author sees pass/fail on
                   these and nothing else.
                 - ADVISORY: the numeral lint (flags typed measurements to convert to
                   inline exprs; statistical conventions α/p/n/CI may stay).
   review:     A REVIEWER, not the author, then reads two things: the table
               `uv run python authoring/check_style.py --review <qmd>` (the length bands and
               the clause-packing family, as signals) and authoring/REVIEW_CHECKLIST.md,
               answered against the finished sections. A "no" goes back to the author as
               what the section lacks, never as a phrase to insert.
               On a HARD failure, re-invoke the SAME agent to fix in place (or extend a
               helper if a <<NEEDS:>> is real), then re-gate. Do NOT start a fresh agent
               mid-document — that reintroduces the coherence problem.

5. annex:      SEPARATE, deliberate step, AFTER the text is final (build-then-annex):
                 uv run python pc_package/build_ground_truth.py   (extend it for <DOC>)
                 uv run python pc_package/validate_annex.py
                 uv run python pc_package/check_grounding.py      (needs the rendered .docx)
               Grounding is NOT part of step 4 — no annex exists at authoring time.

               ANCHOR EACH RECORD ON ITS OWN TABLE ROW, via row_quotes() in
               build_ground_truth.py — not on the table caption and not on a bare label.
               A caption grounds while attesting nothing: one span then stands in for every
               row of the table. The rendered row carries both ends of the relation (the
               parameter and its set-point, the attribute and its acceptance criterion),
               which is what makes the annex usable for attribution. Cells are joined by
               " | " (check_grounding.CELL_SEP) so the row can be split back into columns,
               and table_header=rows.header names those columns; a hand-built partial row
               must use _join_cells() and a partial header. Use param_rows() / cqa_rows() /
               par_rows(), which rebuild the table the .qmd renders. check_grounding reports
               quotes that fail this; GROUNDING_STRICT_ANCHORS=1 makes it a gate, and the
               corpus is at zero. See pc_package/GROUND_TRUTH.md §1.

               THE DISCOURSE LAYER IS PART OF THIS STEP, not an afterthought. Everything
               in the annex that quotes the document — entity/assertion source references,
               report-section statements, AND the rhetorical spans
               (authoring/rhetorical/<DOC>.spans.yaml) — is tied to one revision of one
               document and is invalidated wholesale when that document is re-authored.
               Re-anchor all of it in the same pass. Splitting the discourse layer off into
               a later "annotation" task is how PCR-003 shipped with an empty
               rhetorical_spans layer while PCR-008 had 25 spans: the annex rebuild owned
               the quotes it could see in build_ground_truth.py and forgot the external
               YAML. If a spans file exists, it must match the current text.
```

---

## One document = one agent (the invariant)

A single author is what makes the whole-document arc (OCAR), the cross-references, and the
restatement/coreference cohere — the very things the writing guide is built around. Splitting
a document's sections across agents destroys them and forces a ledger to fake consistency.

- **Never** split one document's sections across agents.
- **Different documents may be authored by different agents in parallel** — they are
  independent. Record which model authored each document; a corpus written by mixed models
  is a confound in your own benchmark and belongs in the release manifest.
- If the context is large, keep the *same* agent going (it holds the document); do not hand
  off. The distilled register exemplar (short excerpts, not the 1000-line report) keeps the
  bound inputs small enough that one context suffices.

---

## Deviations and superseded studies

Deviation prose is **authored from the brief's structured facts** (Option A) — the register
exemplar teaches the moves (adverse-before-mitigation, the common-mode-offset impact
argument). Where the brief shows a **superseded study** block, a real re-executed dataset
exists (e.g. anion exchange, whose first DoE ran on a non-representative deamidated load):
reference it and confirm root cause from the requalified data; analyse only the requalified
dataset. Never invent numbers — deviation magnitudes come from the `dev_*` scalars.

---

## Output-drift caution (before committing)

Regenerating `outputs/` in a different library environment shifts the DoE/effects CSVs in
the deep decimals (BLAS/lib float noise). The committed `outputs/data/*.csv` are the
baseline. **`git diff` any `outputs/` change and commit only intended new/changed data**
(e.g. a newly seeded superseded dataset), never drifted `doe_*`/`effects_*` baselines.

Rendered `.docx` files are git-tracked. While iterating on a draft, either author under a
throwaway filename (e.g. `pc_package/<DOC>_<uokey>.DRAFT.qmd`, whose `.docx` is untracked)
or regenerate the committed `.docx` only when you intend to update the baseline.

---

## Halt points

Halt and report:

- after the first document authored against any new/changed artifact (register + grounding
  check by a human before scaling);
- if re-authoring an existing document: **before** you start, list every artifact that
  quotes it (its annex builder region, its rhetorical spans file, any registry keyed on its
  prose). All of them go stale the moment the text changes, and each one that is missed
  degrades silently rather than failing loudly;
- on a HARD gate failure that a same-agent fix does not resolve in a couple of passes
  (likely a missing helper — extend `_pcpkg`/`doe_report`, then continue);
- before committing any `outputs/` change whose `git diff` is not obviously intended.
