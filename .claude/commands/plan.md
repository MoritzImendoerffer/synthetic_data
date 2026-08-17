---
description: Turn an explored proposal into an ordered task list another session can implement
---

Break one backlog item into tasks, and write them where a different session can pick them up.
Second of four commands: `/explore` → `/plan` → `/next` → `/ship`. See
[`docs/PROJECT_WORKFLOW.md`](../../docs/PROJECT_WORKFLOW.md).

**Input**: `$ARGUMENTS` may name a work unit id. When empty, use `.claude/work/ACTIVE_WORK`.

If there is no active work unit, say so and recommend `/explore <proposal>`. Do not invent
requirements from the conversation. The proposal is the requirements, and if no proposal was
explored there is nothing to plan against.

## The rule that shapes this command

**The plan is written for a session that was not here.** Everything a later session needs must be
in `state.json` and `implementation-plan.md`. A task that only makes sense to someone who read
this conversation is a task that will be implemented wrongly.

So each task states its acceptance criterion as something a command can check, not as an
intention. "`GROUNDING_STRICT_ANCHORS=1 python check_grounding.py` passes with the quote count
printed" can be checked. "Improve the annex" cannot.

**Every major claim carries a concrete example**, taken from this repository rather than invented.
A reader who was not in the session cannot check a claim stated in the abstract, and a claim with
no example survives review because there is nothing to check it against.

- Not "the annexes anchor badly". Instead: "PCR-005 anchored six `ProcessParameter` records on
  one table caption, and reuse of 6 passed because the cap was 8."
- Not "the rhetorical layer is inconsistent". Instead: "PCR-003's 35 spans come from
  `authoring/rhetorical/PCR-003.spans.yaml`; the other eight documents' 280 come from Python
  builders in `build_ground_truth.py` (`h_rhetorical_spans`, `pa_rhetorical_spans`, …)."
- Not "the config edit was risky". Instead: "the config said `univariate`, the CSV still said
  `multivariate`, and `tests/test_config.py` passed throughout because it read `CFG` and never
  the generated file."

## Steps

1. **Load the unit.** Read `metadata.json`, the proposal it names, and `exploration.md`. If
   `exploration.md` says the proposal no longer stands, stop and report that instead of planning
   around it.

2. **Break the work into tasks.** One responsibility each, and small enough to finish and verify
   in one sitting. Order them so the repository is green at every boundary: at each task's end
   the annexes still validate and `check_grounding.py` still passes, not only at the end of the
   plan.

3. **Give every task an acceptance criterion a command can check.** Prefer:
   - a gate command whose output must contain something specific
     (`20/20 annexes valid`, `2084/2084 quotes grounded`, `check_style.py` passing on a named
     document),
   - a test name that must exist and pass,
   - a count with its denominator, taken from a run.

4. **Add the two tasks this project keeps needing.** They are not optional, because their absence
   is the defect that has recurred most often here:

   - **A rebuild-and-reground task.** A change to the config, a helper or a document is not done
     when the source is edited. `make data figures` regenerates the CSVs the documents actually
     read, the documents re-render, and every annex quote that touched the changed text has to be
     re-anchored. Commit `641d19a` skipped this on the assumption that `study` was display-only
     metadata and shipped a document contradicting its own table. If the plan changes anything
     upstream of a rendered document, one task runs the rebuild and names the gate output it
     expects.
   - **The documentation move.** When the work lands, a measurement goes to `docs/results/`, a
     change to what the documents say or how they are checked goes to `authoring/HANDOFF.md`
     §3a, a thing somebody could get wrong twice goes to `pc_package/TASKS.md` or `CLAUDE.md`,
     the `docs/ROADMAP.md` row is updated, and the proposal is deleted. `/ship` does this, and
     the plan must leave room for it.

5. **Write `state.json`** into the work unit:

   ```json
   {
     "status": "planning_complete",
     "proposal": "docs/next/<name>.md",
     "current_task": null,
     "tasks": [
       {
         "id": "TASK-001",
         "title": "one line, imperative",
         "type": "mechanism",
         "status": "pending",
         "dependencies": [],
         "files": ["pc_package/build_ground_truth.py"],
         "acceptance": ["check_grounding.py reports 2084/2084 with strict anchors", "..."],
         "notes": "anything a session that was not here would get wrong"
       }
     ]
   }
   ```

   `scripts/pm_notes.py` renders this into `docs/pm/`, which is where the project owner reads it.
   Use the `type` values in the sizing table below, so the board's Kind column means something.

6. **Write `implementation-plan.md`** beside it, for a person: what is being built, the order and
   why that order, what could go wrong, and what will not be attempted.

7. **Regenerate the board** so the plan is visible outside this session:

   ```bash
   uv run python scripts/pm_notes.py
   ```

8. **Report** the task count, the critical path, and anything the proposal left undecided that the
   plan had to decide. Say which decisions were yours, so they can be overruled. A decision that
   is the owner's rather than yours goes in `docs/pm/decisions/` as its own note, and the board
   prints it.

## Sizing

| Type | What it covers |
|---|---|
| `model` | a change under `config/parameters.yaml` or `amab_process/`. It moves numbers, so it forces a full rebuild |
| `document` | a one-pass re-author of a `.qmd`. Never a paragraph patch, and never fold two documents into one task |
| `annex` | `build_ground_truth.py` / `schema_ext.py`, ending in validate + ground |
| `mechanism` | a helper, a gate or a script under `authoring/`, `pc_package/` or `scripts/` |
| `measurement` | the run that produces a number, and the `docs/results/` page that holds it |
| `documentation` | the `docs/` page, the HANDOFF or TASKS row, the ROADMAP entry, and deleting the proposal |

## What this command does not do

It writes no implementation code, renders no document and rebuilds no annex.

It also does not renumber the backlog: if the work turns out larger than the ROADMAP assumed, say
so and let the user reprioritise.
