---
description: Implement the next task from a stored plan, in this project's environment and gates
---

Execute pending tasks from the active work unit. Third of four commands: `/explore` → `/plan` →
`/next` → `/ship`. See [`docs/PROJECT_WORKFLOW.md`](../../docs/PROJECT_WORKFLOW.md).

**Input**: `$ARGUMENTS`

| Argument | Effect |
|---|---|
| *(empty)* | run the next task whose dependencies are met |
| `--status` | print completed, pending and blocked tasks, then stop |
| `--preview` | print what the next task would change, then stop |
| `--task TASK-003` | run one named task |

## Start here, not from the conversation

Read `.claude/work/ACTIVE_WORK`, then `state.json`, then the proposal it names, then
`exploration.md`. **This is the whole input.** A session picking work up later was not present
for the planning, and behaving as though it was is how a plan gets implemented wrongly.

- No `ACTIVE_WORK` → say so and recommend `/explore <proposal>`.
- No `state.json` → recommend `/plan`.
- `status` is not `planning_complete` or `implementing` → report the status and stop.

## The environment

**Everything runs under `uv`.** numpy, pandas, scipy and statsmodels are not in the system
python, so a bare `python` either fails or silently reaches a different interpreter:

```bash
uv run python <script>
make test PY="uv run python"
```

**`PY=` is not enough for `make corpus`.** Quarto starts its own Jupyter kernel and resolves
`python3` from `PATH`, not from `PY`. With a conda `python3` first on `PATH`, every render dies
with "Jupyter is not available in this Python installation". Put the venv on `PATH` for the whole
build:

```bash
PATH="$PWD/.venv/bin:$PATH" make corpus PY="uv run python"
```

The gates, and what each is for:

| Command | Gates |
|---|---|
| `make test PY="uv run python"` | config ↔ DoE invariants, and CSV against config |
| `uv run python authoring/check_style.py <doc>.qmd` | the register. `--selftest` proves the thresholds pass real human prose |
| `uv run python authoring/check_render.py <doc>.qmd --render` | dry eval, `<<NEEDS:>>` scan, numeral advisory, real render, PDF glyphs, and it runs `check_style.py` |
| `cd pc_package && uv run python build_ground_truth.py && uv run python validate_annex.py` | the annexes build and validate |
| `cd pc_package && GROUNDING_STRICT_ANCHORS=1 uv run python check_grounding.py` | every quote verbatim in the rendered `.docx`, and no weak anchors |

While iterating on a document, author under a throwaway name
(`pc_package/<DOC>_<uokey>.DRAFT.qmd`, whose `.docx` is untracked) so the committed baseline of
21 rendered files does not drift.

## Steps

1. **Pick the task.** The first pending one whose dependencies are all completed, or the one named
   by `--task`. If every pending task is blocked, print what blocks each and stop.

2. **Implement it**, in the layer the plan says. Reuse the shared machinery — `_pcpkg.py`,
   `doe_report.py`, `schema_ext.py`, `build_ground_truth.py` — rather than writing a local
   variant. Write code that reads like the code around it.

3. **Never hard-code a value that lives in the config or `outputs/`.** If you catch yourself
   typing a set-point, a range, an effect, a p-value or a Cpk into a `.qmd`, a helper or an
   annex, stop and pull it through the helper instead. This is the rule the whole build rests on.

4. **If the task changes prose, re-author the whole document in one pass**, from
   `WRITING_GUIDE.md`, `REGISTER_EXEMPLAR.md`, `STORY_BIBLE.md`, `section_plan.yaml` and the
   document's brief. Never patch a paragraph, and never read a sibling `.qmd`. The register gate
   measures the document as a whole, and the sibling-copying loop is what forced all 20 documents
   to be re-authored once already.

5. **If the task changes a number, change the config and rebuild.** `make data figures`
   regenerates the CSVs, and the documents read the CSVs rather than `CFG`. A config edit that
   skips this leaves the corpus contradicting itself, and `tests/test_config.py` will not catch
   it unless the assertion reads the generated file.

6. **Rebuild and re-ground whatever the change touched.** Re-authoring or re-rendering invalidates
   every annex quote over the changed text. Rebuild the annex and re-anchor to the new text —
   never edit a document to suit a stale quote, and never raise a threshold to make a weak anchor
   pass. Fix a weak anchor by finding the span that names the record.

7. **Check the acceptance criteria literally.** Run what they name. Do not substitute a judgement
   that it looks right.

8. **Run the gates the task's layer needs**, and report their counts rather than asserting
   success. If a gate fails, say so with the output.

9. **Update `state.json`**: the task's `status` becomes `completed`, `current_task` moves on, and
   the unit's `status` becomes `implementing`. **Then regenerate the visible board:**

   ```bash
   uv run python scripts/pm_notes.py
   ```

   `docs/pm/` is the only place the project owner can see task state — `state.json` is invisible
   to them. A task marked done in `state.json` and not regenerated is a task that is done for you
   and unfinished for everybody else. Commit the notes with the task. The script also archives the
   previous epic when `ACTIVE_WORK` has moved.

10. **If the outside view changed, update it.** Not on every task — that is churn nobody reads.
    Only when one of these three happens:

    - **A task became blocked.** Say so in that proposal's row in `docs/next/README.md`, with what
      would unblock it and who has to do it. A blocker recorded only in `state.json` is a blocker
      nobody outside this session can see.
    - **The last task of a track completed**, so something now exists that did not.
    - **A claim in `docs/next/` or `docs/ROADMAP.md` became false.** Building the thing usually
      falsifies the sentence that argued for it.

11. **Commit, if the user has asked for commits.** One commit per task, in this repository's
    style: an imperative subject naming what changed, then prose giving the defect and the
    evidence. Not Conventional Commits, and never a bare "fix". Include the task id.

12. **Report** what changed, what the gates said, and what the next available task is.

## Numbers, and the two ways this project has got them wrong

- **Quote every rate with its denominator.** "2084/2084 quotes grounded across 20 annexes", not
  "grounding passes". A bare percentage hides which run produced it.
- **Do not regenerate `outputs/` casually.** Re-running `scripts/generate_data.py` in a different
  library environment shifts the DoE and effects CSVs in the deep decimals. The committed CSVs are
  the baseline. `git diff` any `outputs/` change and commit only intended new or changed data,
  never a drifted `doe_*` / `effects_*` baseline.
- **A number goes into `docs/results/` with the command that produced it**, not into a commit
  message.

## What this command does not do

It does not deliver. Moving findings into `docs/`, updating the ROADMAP and deleting the proposal
is `/ship`. Step 10 is the narrow exception and it is not delivery: it keeps a status line true
while the work is in flight.

It does not silently widen the plan: if a task cannot be done as written, stop, say why, and let
the plan be corrected.

It does not add anything to a finished document. The document a one-pass author produced is the
document that ships; post-authoring steps build artifacts around the text and never change what
it claims.
