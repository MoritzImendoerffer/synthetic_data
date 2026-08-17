---
type: pm-task
epic: 2026-08-17_01_register-second-round
sprint: 2026-08-17_01_register-second-round
task: TASK-003
status: todo
kind: mechanism
title: "Add authoring/check_discourse.py with spaCy as an optional extra that the build never needs"
generated: true
waiting_on: the assistant
tags: [pm/task, pm/todo]
---

> [!warning] Generated from `.claude/work/2026-08-17_01_register-second-round/state.json` by `scripts/pm_notes.py`.
> Anything written here by hand is lost on the next run.

# TASK-003 — Add authoring/check_discourse.py with spaCy as an optional extra that the build never needs

**Epic:** [[epic]] · **Status:** `todo` · **Waiting on:** the assistant · **Board:** [[_Board]]

## Why it exists

PROCEDURE: procedures/TASK-003.md in this work unit — numbered steps, code, commands and the output each must print. Follow it top to bottom.  OWNER DECISION 2026-08-17: spaCy is an OPTIONAL dependency, never a hard one; the corpus must build, render, annex and ground on a checkout that never installed a parser (proposal open question 1, with the four commitments listed there).  WHERE THE CODE COMES FROM. authoring/register_analysis.ipynb cell 30 (topic_chaining: subject lemma set ∩ previous sentence's NOUN/PROPN/ADJ lemmas, or subject is PRON; limit=600) and cell 46 (copula: ROOT lemma 'be'; front field: any non-punct token before the subject subtree; limit=450). Port them verbatim in logic; the acceptance numbers are that notebook's §13 output and are printed on docs/results/2026-08-17-register-pilot.md.  THE MODEL WHEEL. Same URL the results page uses: https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl. Pin spaCy to the 3.8 line the model was built for; a different minor breaks the model load, and the parse changes with the model version, which is why the reproduction acceptance exists.  DEGRADE, NOT FAIL. `try: import spacy` at the top; on ImportError print one line and return 0. `nlp = spacy.load('en_core_web_sm')` can also fail with the extra half-installed — catch OSError the same way.  DO NOT put it in check_render.py or the style target. Advisory means advisory.  LAND WITH THE LOCK. uv.lock changes in this task and nowhere else; the proposal says a lock change with no consumer is churn on the tested path.  AFTER THE ACCEPTANCE RUN on the base sync, re-run `uv sync --extra discourse` so TASK-004's brief can print the numbers.

## Acceptance criteria

- [ ] pyproject.toml has [project.optional-dependencies] discourse = spaCy 3.8.x plus en_core_web_sm 3.8.0 as a direct wheel URL; `uv lock` succeeds and uv.lock is committed with it; requirements-discourse.txt mirrors the group; requirements.txt is unchanged
- [ ] on a base sync (`uv sync`, no extra) `uv run python authoring/check_discourse.py pc_package/PCR-003_bioreactor.qmd` prints ONE line naming `uv sync --extra discourse` and exits 0
- [ ] `uv sync --extra discourse` installs; `uv run --extra discourse python authoring/check_discourse.py --cap pc_package/PCR-003_bioreactor.qmd pc_package/PCP-003_bioreactor.qmd` prints, for the four sources and both documents, topic chaining %, copula %, front field %, each as 'pct (count/denominator)', and reproduces the pilot's numbers within ±0.5 points: PCR-003 chaining 30.7 (127/414), copula 32.5 (135/415), front 9.2 (38/415); PCP-003 34.4 (77/224), 27.6 (62/225), 10.2 (23/225); PDA TR 60 chaining 59.4 (332/559)
- [ ] without --cap it measures every sentence; the help text says --cap reproduces the notebook's 600/450 sentence caps
- [ ] it imports prose_from_qmd, prose_from_extract, sentences and HUMAN_SOURCES from check_style and does not re-implement them; it replaces 'NUM' with '12.3' before parsing, as notebook cell 40 does
- [ ] a `discourse` Makefile target exists and is not a prerequisite of corpus, style, test or all; `make test PY="uv run python"` and `make style PY="uv run python"` pass on the base sync
- [ ] CLAUDE.md Environment names the extra in one sentence and says the corpus builds without it
- [ ] the script prints the same output as `--json` when asked, so build_brief.py (TASK-004) can read it

## Files it touched

- `authoring/check_discourse.py`
- `pyproject.toml`
- `uv.lock`
- `requirements-discourse.txt`
- `Makefile`
- `CLAUDE.md`
