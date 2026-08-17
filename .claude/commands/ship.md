---
description: Close a work unit: prove it reproduces, move the findings into docs, retire the proposal
---

Deliver finished work and retire its proposal. Last of four commands: `/explore` → `/plan` →
`/next` → `/ship`. See [`docs/PROJECT_WORKFLOW.md`](../../docs/PROJECT_WORKFLOW.md).

**Input**: `$ARGUMENTS`

| Argument | Effect |
|---|---|
| *(empty)* | run every check, report, and stop before changing anything |
| `--commit` | after the checks pass, apply the documentation moves and commit |
| `--pr` | as `--commit`, then open a pull request |

The default changes nothing. Delivery is the step that edits the ROADMAP and deletes a proposal,
so it asks first.

## The check that matters most

**Does the work reproduce, or does it only exist in this working tree?** In a repository whose
whole claim is that changing `meta.seed` and re-running regenerates the corpus with no manual
edits, the equivalent of dead code is a result that cannot be rebuilt.

So:

1. **Rebuild from the source of truth**, at the depth the change reaches:

   | The unit touched | Run |
   |---|---|
   | `config/`, `amab_process/`, `scripts/`, a helper, or any `.qmd` | `make clean && PATH="$PWD/.venv/bin:$PATH" make data figures corpus PY="uv run python"` |
   | annexes or gates only | `make test PY="uv run python"`, then rebuild, validate and ground the annexes |

   Say which of the two you ran. Reporting a green annex run as though it were a full rebuild is
   the failure this check exists to prevent.

2. **Read the diff for typed numbers.** `git diff` every changed `.qmd`, helper and annex builder
   and check that no set-point, range, effect, p-value or Cpk was typed in rather than pulled
   through `_pcpkg.py` / `doe_report.py` or read from a CSV. One typed number is a value that
   stops tracking the config the next time the seed moves.

3. **Check `outputs/` did not drift.** If `outputs/data/doe_*.csv` or `effects_*.csv` changed and
   the work did not intend to change them, that is library drift in the deep decimals, not a
   result. Restore the baseline and say so.

## Steps

1. **Load the unit** from `.claude/work/ACTIVE_WORK`. Every task must be `completed`. If any is
   not, list them and stop.

2. **Run the gates**, and report the counts rather than asserting success:

   ```bash
   make test PY="uv run python"
   make style PY="uv run python"
   cd pc_package && uv run python build_ground_truth.py && uv run python validate_annex.py \
     && GROUNDING_STRICT_ANCHORS=1 uv run python check_grounding.py
   ```

   The expected shapes are `20/20 annexes valid` and `N/N quotes grounded across 20 annexes`.
   For a document that was re-authored, `uv run python authoring/check_render.py <doc> --render`
   must also pass, including its PDF glyph check — a dropped `≥` once turned a clearance floor
   into a point value, and nothing had ever inspected the PDF after rendering.

3. **Run the reproduction check above**, and name which rebuild you ran.

4. **Check the claims the work will make.** For each sentence about to be written into `docs/`,
   verify it against the repository. Two "open item" claims in this repository's own
   documentation were checked on 2026-08-16 and both were already false. A claim in a status
   file is worth exactly as much as its last verification.

5. **Move the findings.** This is the delivery, and it is what makes the backlog honest:

   | If the work produced | It goes to |
   |---|---|
   | a measurement | a new dated report in `docs/results/`, and a row in `docs/results/README.md` saying why the run happened |
   | a mechanism or a gate | the relevant `docs/`, `authoring/` or `pc_package/` page, in the section a reader would look in |
   | a change to what documents say, or how they are checked | a row in `authoring/HANDOFF.md` §3a, which is the record of every perturbation applied to the corpus |
   | a rule somebody could get wrong twice | "Things that will catch you out" in `pc_package/TASKS.md`, or a golden rule in `CLAUDE.md` |
   | a deliberate inconsistency kept as a benchmark item | `authoring/DISCREPANCIES.md`, with its exact span |
   | a schema departure | `pc_package/schema_ext.py`, recorded in `schema_extensions_used` — never `annex_contract/` |

6. **Update `docs/ROADMAP.md`.** Change the item's status to what is now true, and remove it from
   the ordering table if it is finished. If the work is only partly done, say precisely what
   remains. A ticked box on something that cannot be rebuilt is the failure this whole command
   exists to prevent.

7. **Delete the proposal.** `docs/next/<name>.md` is removed once its content has moved, and
   `docs/next/README.md` drops the row. `git` keeps the history, and a plan that no longer matches
   the repository is worse than no plan. If some of the proposal is still open, do not delete it:
   rewrite it down to what remains and say so.

8. **Commit** with this repository's message style: an imperative subject naming what changed, then
   prose giving the defect, the evidence and the numbers. State what was verified and how.

9. **Archive the work unit.** Set `status` to `delivered` in `metadata.json` and clear
   `.claude/work/ACTIVE_WORK`.

10. **Offer a memory entry**, if the work produced a durable preference or a lesson that the
    repository and git history do not already record.

## Leave `docs/pm/` on the board, and settle what is open

**Do not delete or archive the epic here.** `docs/pm/` shows the epic being worked on, and a
shipped epic is the one a reader most wants to look at. It is archived when the **next** epic
starts, by `scripts/pm_notes.py`, which moves it whole into `docs/pm/archive/<epic>/`.

What `/ship` does owe `docs/pm/`:

1. **regenerate it**, so the board matches the final `state.json`:

   ```bash
   uv run python scripts/pm_notes.py
   ```

2. **settle every decision under `docs/pm/decisions/`.** A settled one records the answer and who
   gave it, and sets `status: settled`. One still open moves to `docs/next/`, because an unresolved
   argument belongs where arguments live, and it is then deleted from here;
3. **update `docs/pm/epic.md`** so its first paragraph says what shipped and what did not, and
   points at the `docs/results/` page;
4. **add the epic's row to `docs/pm/_Archive.md`** with its results link, so the index is right
   before the notes move.

## What this command does not do

It does not push and it does not merge unless asked. It never merges
`feature/weak-claims-via-brief` into `main` under any argument: that branch is carried forward by
rebasing `main` onto it, and PR #6 merged it once against the instruction in its own commit
message and had to be reverted.

It does not report success it did not verify. If a gate fails, or a result cannot be rebuilt, say
so plainly and leave the unit open.
