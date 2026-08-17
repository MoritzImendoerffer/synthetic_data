---
type: pm-task
epic: 2026-08-17_01_register-second-round
sprint: 2026-08-17_01_register-second-round
task: TASK-003
status: done
kind: mechanism
title: "Add authoring/check_discourse.py with spaCy as an optional extra that the build never needs"
generated: true
waiting_on: —
tags: [pm/task, pm/done]
about: ["PCP-003", "PCR-003"]
---

> [!warning] Generated from `.claude/work/2026-08-17_01_register-second-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-003 — Add authoring/check_discourse.py with spaCy as an optional extra that the build never needs

**Epic:** [[epic]] · **Status:** `done` · **Waiting on:** — · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-003.md in this work unit — numbered steps, code, commands and the output each must print. Follow it top to bottom.  OWNER DECISION 2026-08-17: spaCy is an OPTIONAL dependency, never a hard one; the corpus must build, render, annex and ground on a checkout that never installed a parser (proposal open question 1, with the four commitments listed there).  WHERE THE CODE COMES FROM. authoring/register_analysis.ipynb cell 30 (topic_chaining: subject lemma set ∩ previous sentence's NOUN/PROPN/ADJ lemmas, or subject is PRON; limit=600) and cell 46 (copula: ROOT lemma 'be'; front field: any non-punct token before the subject subtree; limit=450). Port them verbatim in logic; the acceptance numbers are that notebook's §13 output and are printed on docs/results/2026-08-17-register-pilot.md.  THE MODEL WHEEL. Same URL the results page uses: https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl. Pin spaCy to the 3.8 line the model was built for; a different minor breaks the model load, and the parse changes with the model version, which is why the reproduction acceptance exists.  DEGRADE, NOT FAIL. `try: import spacy` at the top; on ImportError print one line and return 0. `nlp = spacy.load('en_core_web_sm')` can also fail with the extra half-installed — catch OSError the same way.  DO NOT put it in check_render.py or the style target. Advisory means advisory.  LAND WITH THE LOCK. uv.lock changes in this task and nowhere else; the proposal says a lock change with no consumer is churn on the tested path.  AFTER THE ACCEPTANCE RUN on the base sync, re-run `uv sync --extra discourse` so TASK-004's brief can print the numbers.

## Acceptance criteria

- [x] pyproject.toml has [project.optional-dependencies] discourse = spaCy 3.8.x plus en_core_web_sm 3.8.0 as a direct wheel URL; `uv lock` succeeds and uv.lock is committed with it; requirements-discourse.txt mirrors the group; requirements.txt is unchanged
- [x] on a base sync (`uv sync`, no extra) `uv run python authoring/check_discourse.py pc_package/PCR-003_bioreactor.qmd` prints ONE line naming `uv sync --extra discourse` and exits 0
- [x] `uv sync --extra discourse` installs; `uv run --extra discourse python authoring/check_discourse.py --cap pc_package/PCR-003_bioreactor.qmd pc_package/PCP-003_bioreactor.qmd` prints, for the four sources and both documents, topic chaining %, copula %, front field %, each as 'pct (count/denominator)', and reproduces the pilot's numbers within ±0.5 points: PCR-003 chaining 30.7 (127/414), copula 32.5 (135/415), front 9.2 (38/415); PCP-003 34.4 (77/224), 27.6 (62/225), 10.2 (23/225); PDA TR 60 chaining 59.4 (332/559)
- [x] without --cap it measures every sentence; the help text says --cap reproduces the notebook's 600/450 sentence caps
- [x] it imports prose_from_qmd, prose_from_extract, sentences and HUMAN_SOURCES from check_style and does not re-implement them; it replaces 'NUM' with '12.3' before parsing, as notebook cell 40 does
- [x] a `discourse` Makefile target exists and is not a prerequisite of corpus, style, test or all; `make test PY="uv run python"` and `make style PY="uv run python"` pass on the base sync
- [x] CLAUDE.md Environment names the extra in one sentence and says the corpus builds without it
- [x] the script prints the same output as `--json` when asked, so build_brief.py (TASK-004) can read it

## What was built

authoring/check_discourse.py measures topic chaining, copula rate and adjunct front field behind an optional spaCy extra. It imports prose_from_qmd, prose_from_extract, sentences and HUMAN_SOURCES from check_style and re-implements none of them, so it reads exactly the text the register gate reads; prep() replaces the NUM placeholder with 12.3 before parsing, as notebook cell 40 does. The chaining and copula/front logic is ported from cells 30 and 46 unchanged.

REPRODUCTION. `uv run --extra discourse python authoring/check_discourse.py --cap pc_package/PCR-003_bioreactor.qmd pc_package/PCP-003_bioreactor.qmd` (36 s) reproduces the pilot's section 13 table EXACTLY -- all 18 cells, percentages and both counts, not merely within the +/-0.5 point tolerance:

                     PDA TR 60   A-Mab      ISPE TT    ISPE PV    PCR-003    PCP-003
chaining        59.4 (332/559)  59.0 (315/534)  61.9 (348/562)  57.0 (321/563)  30.7 (127/414)  34.4 (77/224)
copula           17.6 (74/420)  14.8 (61/412)   22.4 (95/424)  26.1 (110/422)  32.5 (135/415)  27.6 (62/225)
front           27.1 (114/420)  33.5 (138/412)  35.6 (151/424)  36.3 (153/422)    9.2 (38/415)  10.2 (23/225)

UNCAPPED (51 s), which is what TASK-008 should quote and say so: PDA TR 60 chaining 60.5 (465/769), copula 20.1 (155/770), front 28.4 (219/770); A-Mab 56.1 (539/960), 13.5 (130/961), 32.9 (316/961); ISPE TT 61.9 (388/627), 22.8 (143/628), 34.2 (215/628); ISPE PV 57.3 (435/759), 26.3 (200/760), 37.1 (282/760). Both corpus documents are under both caps, so PCR-003 and PCP-003 are identical capped and uncapped -- the caps only ever bit the four sources. The source columns move by up to 2.9 points (A-Mab chaining 59.0 -> 56.1), so a round-two number compared against a capped source column would be comparing two different measurements.

DEGRADATION, proved on a base `uv sync` with the extra removed: `uv run python authoring/check_discourse.py pc_package/PCR-003_bioreactor.qmd` prints exactly the one DEGRADE line naming `uv sync --extra discourse` and exits 0. On that same base environment `make test PY="uv run python"` reports 88 passed and `make style PY="uv run python"` exits 0 with 24 OK lines and 0 FAIL, so nothing on the tested path acquired a parser dependency. `make discourse PY="uv run python"` also exits 0 there, printing the same line. The extra was re-installed afterwards for TASK-004.

DEPENDENCIES. pyproject.toml gains [project.optional-dependencies] discourse = spacy>=3.8,<3.9 plus en-core-web-sm as a PEP 508 direct wheel URL at 3.8.0. `uv lock` succeeded and uv.lock grew by 883 lines (23 transitive packages: thinc, srsly, preshed, murmurhash, cymem, wasabi, weasel, typer, rich and the rest); spacy resolved to 3.8.15, and `spacy.load('en_core_web_sm')` succeeds. requirements-discourse.txt mirrors the group for the pip path and requirements.txt is untouched (git reports 0 changed lines in it).

WIRING. The Makefile gains a `discourse` target, a .PHONY entry and a help line, and no target lists it as a prerequisite -- all, corpus, style, test, figures and data are unchanged. CLAUDE.md §Environment names the extra in one sentence and states that the corpus builds, renders, annexes and grounds without it. A repository-wide grep for spacy finds it only in pyproject.toml, requirements-discourse.txt, the Makefile comment and check_discourse.py itself; the two hits in pc_package/annex_contract/base.py are pre-existing string literals in an ExtractionSource Literal, not imports.

--json emits the same measurements as a JSON object keyed by column name, which is what TASK-004's brief section reads.

## Documents it is about

- **PCP-003** — `pc_package/PCP-003_bioreactor.qmd`
- **PCR-003** — `pc_package/PCR-003_bioreactor.qmd`

## Files it touched

- `authoring/check_discourse.py`
- `pyproject.toml`
- `uv.lock`
- `requirements-discourse.txt`
- `Makefile`
- `CLAUDE.md`
