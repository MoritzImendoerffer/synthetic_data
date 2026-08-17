# The planning workflow: from a backlog item to delivered work

Four commands carry one item from `docs/next/` to done, across as many sessions as it takes. They
live in `.claude/commands/` and are specific to this repository.

This is about changing the **project**. [`WORKFLOW.md`](WORKFLOW.md) is about how the A-Mab model
and the corpus work; read that first if the question is "where does this number come from".

```
docs/ROADMAP.md          you pick the item, in the order the roadmap gives
   │
   ▼
/explore <proposal>      opens a work unit, reads the repository, checks the proposal is still true
   │
   ▼
/plan                    writes state.json and implementation-plan.md
   │
   ▼
/next                    implements one task, runs the gates, updates state.json
   │  (repeat)
   ▼
/ship                    proves it reproduces, moves findings into docs/, retires the proposal
```

## Why it is built this way

**A session ends and the work does not.** These commands write the state down, so a second session
picks up from files rather than from a conversation it never saw. Everything a later session needs
is in the work unit and the proposal.

**The proposal is the requirements, and there is only one copy.** `/explore` records the *path* to
`docs/next/<name>.md` and never copies its content. Two descriptions of one task drift, and the
drift is invisible until somebody builds the wrong one.

**A status line is worth its last verification.** On 2026-08-16 three "open items" in this
repository's own documentation were checked against the code and all three were already closed:
`nlp_reports` recognises this corpus's document ids after all, the PCR-003 rhetorical layer builds
35 spans and drops none, and DEV-005-01 was fixed in the config. That is why `/explore` step 4
verifies every claim of absence before anything is planned, and `/ship` step 4 re-checks every
sentence it is about to write into `docs/`.

## First: are you changing the corpus, or the machinery?

**Much of what you will want to do needs none of this workflow.** Changing what a document *says*
is a config edit and a rebuild — no work unit, no proposal, no plan.

| What you want | What it is | What to do |
|---|---|---|
| a different set-point, range or limit | **corpus content** | edit `config/parameters.yaml`, `make data figures`, `make corpus` |
| a different seed | **corpus content** | the same, and every document follows |
| a document that reads differently | **corpus content** | re-author it in one pass from the `authoring/` artifacts. `pc_package/TASKS.md` is the procedure |
| a new unit operation | **corpus content**, at scale | `pc_package/TASKS.md` §"Adding a unit operation" |
| a new field an annex can carry | machinery | `/explore` → `/plan` → `/next` → `/ship` |
| a new gate, or a change to one | machinery | the same four |
| a measurement nobody has made | machinery | the same four, and it ends in `docs/results/` |

**The test is whether the change is reproducible without you.** If editing the config and running
`make` produces it, it is content. If it changes what `make` *does*, it is machinery.

## `docs/pm/` — the epic you can see

`state.json` is the machine's task list and nobody outside the session can read it, so "what step
are we at, what is left, what is waiting on me" had no home.

[`pm/`](pm/) is `state.json` rendered as Markdown notes with YAML frontmatter: one note per task, a
board, the epic, and one note per decision waiting on a person. Regenerate with:

```bash
uv run python scripts/pm_notes.py      # or: make pm PY="uv run python"
```

**Generated and hand-written notes are separate files, never two halves of one.** The board and the
task notes are generated and carry `generated: true`; the epic note, the decisions, the README and
the archive are written by a person and the script never touches them.

**It holds one epic, and the previous one is archived rather than deleted.** When
`.claude/work/ACTIVE_WORK` names a different epic, `scripts/pm_notes.py` moves everything belonging
to the old one into `docs/pm/archive/<epic>/` and starts a fresh board. Archiving happens when a
new epic starts, not when one ships: a shipped epic is the one a reader most wants to look at.

**On CCPM and GitHub issues.** The structure is CCPM's
(<https://aroussi.com/post/ccpm-claude-code-project-management>) with GitHub swapped for the
repository, adapted from the sibling `nlp_reports` project where it has run since 2026-08-07. The
board is versioned with the corpus it describes, and a task can link to the document it changed —
neither of which an issue tracker does.

## Who owns what

| Question | Answer lives in | Survives the work |
|---|---|---|
| What should we build, and why? | `docs/next/<name>.md` | no, it is deleted on delivery |
| In what order? | the table at the top of `docs/ROADMAP.md` | yes |
| What does the repository look like today? | `.claude/work/<id>/exploration.md` | no |
| Which tasks, in what order? | `.claude/work/<id>/state.json` | no |
| What is being worked on right now? | `docs/pm/` | archived, not lost |
| What was built and what did it measure? | `docs/results/` and the relevant `docs/` page | yes |
| How the corpus is built and changed | `docs/WORKFLOW.md`, `pc_package/TASKS.md`, `authoring/RUNNER.md` | yes |

`docs/next/` and `.claude/work/` do different jobs and must not duplicate. `docs/next/` is
reviewed, committed and permanent until the work lands. A work unit is scratch space for one
implementation attempt, and it is disposable the moment `/ship` has moved the findings out.

## The work unit

```
.claude/work/
├── ACTIVE_WORK                      # the id of the unit in progress
└── 2026-08-16_01_rhetorical-layer/
    ├── metadata.json                # proposal path, status, roadmap priority
    ├── exploration.md               # what the repository looks like now
    ├── state.json                   # the task list and its progress
    └── implementation-plan.md       # the same plan, for a person
```

`metadata.json` names the proposal instead of holding a copy of it.

**One unit predates this workflow.** `2026-08-03_01_annex-anchors` holds a `requirements.md`
instead of naming a proposal, and its tasks carry no acceptance criteria. `scripts/pm_notes.py`
reads that older shape on purpose: a board that will not render is a board nobody looks at.

## The commands

### `/explore <proposal>`

Opens the work unit and reads the repository. Run it with no argument to list the backlog in
priority order. It checks every claim in the proposal against the code before planning starts, and
records which of this project's ground rules bite: whether a number moves, whether prose has to be
re-authored, whether a registered discrepancy is in scope, whether the change reaches a read-only
contract.

### `/plan`

Breaks the work into tasks, each with an acceptance criterion a command can check.
"`check_grounding.py` reports 2084/2084 with strict anchors" can be checked. "Improve the annex"
cannot.

It always adds two tasks, because their absence is this project's most repeated defect:

- **A rebuild-and-reground task.** A config edit is not live until `make data figures` runs, and
  the documents read the generated CSVs rather than `CFG`. Commit `641d19a` assumed otherwise and
  shipped a PCP-003 whose prose said "univariate" while its own Table 6 said `multivariate`.
- **A documentation task.** Findings to `docs/results/`, the perturbation to `HANDOFF.md` §3a, the
  trap to `TASKS.md`, the ROADMAP row updated, the proposal deleted.

### `/next`

Implements one task. Its whole input is `state.json`, the proposal and `exploration.md` — not the
conversation, because a later session did not have one.

Everything runs under `uv`. For `make corpus`, `PY=` is not enough: Quarto starts its own Jupyter
kernel and resolves `python3` from `PATH`, so the venv goes on `PATH` for the whole build.

`--status`, `--preview` and `--task TASK-003` are available.

### `/ship`

Closes the unit. With no argument it runs every check and stops. `--commit` applies the changes.

Its most important check is **reproduction**. In a repository whose whole claim is that changing
the seed and re-running regenerates the corpus with no manual edits, the equivalent of dead code is
a result that cannot be rebuilt. So `/ship` rebuilds at the depth the change reaches, reads the
diff for numbers that were typed rather than pulled, and checks that `outputs/` did not drift in
the deep decimals.

Then it moves the findings out, updates the ROADMAP to what is now true, and deletes the proposal.
If part of the proposal is still open, the file is rewritten down to what remains rather than
deleted.

## Worked example

```bash
/explore rhetorical-layer-coverage   # opens .claude/work/2026-08-16_01_rhetorical-layer/
/plan                                # writes state.json, and the board under docs/pm/
/next --preview                      # what TASK-001 would change
/next                                # implement, run the gates, update state, regenerate the board
/next                                # ... and so on
/ship                                # checks only, nothing changed
/ship --commit                       # docs moved, ROADMAP updated, proposal deleted
```

A different session can join at any point. It reads `ACTIVE_WORK` and continues.

## What this workflow does not do

- **It does not choose priority.** `docs/ROADMAP.md` holds the order and the argument for it.
- **It does not commit unless asked.** `/next` and `/ship` commit only when told to.
- **It does not touch the corpus's own rules.** The golden rules in `CLAUDE.md` outrank every
  command here: single source of truth, reproducible by construction, everything grounded, nothing
  added to a document after authoring.
