---
type: pm-index
tags: [pm]
---

# docs/pm — the epic that is running now

Open **[[_Board]]**. That is the page this folder exists for.

## What is here

| Note | What it is | Written by |
|---|---|---|
| [[_Board]] | the epic at a glance: waiting, unfinished, done | **generated** |
| [[epic]] | why this epic happened and what it built | a person |
| `TASK-*.md` | one per task: what it owes, what it did, what it touched | **generated** |
| `decisions/` | an argument someone has to settle | a person |
| [[_Artifacts]] | the corpus, the outputs and the gates a task's work has to survive | a person |
| [[_Archive]] | one line per finished epic, pointing at its results | a person |

**A generated note carries `generated: true` and is overwritten.** Its source is
`.claude/work/<epic>/state.json`, and the regenerator is `scripts/pm_notes.py`:

```bash
uv run python scripts/pm_notes.py     # or: make pm PY="uv run python"
```

Generated and hand-written notes are separate **files**, never two halves of one file. A note that
mixes a render with hand-written prose loses the prose on the next run, without a warning.

## One epic at a time, and the last one is archived rather than deleted

**The rule is the epic boundary, not a note count.** `docs/pm/` shows the epic being worked on.
When `.claude/work/ACTIVE_WORK` names a different one, `scripts/pm_notes.py` moves everything
belonging to the old epic into `docs/pm/archive/<epic>/` — its board, its epic note, its task notes
and its decisions — and starts a fresh board.

**Nothing is deleted.** An old cycle is still there and still openable; it has just stopped being
the thing on the board. [[_Archive]] is the index of them.

**Archiving happens when a new epic starts, not when one ships.** A shipped epic stays on the board
until something replaces it, which is exactly when you most want to look at it.

So the board is always one epic deep, however many have been run.

## How it relates to everything else

| Question | Where it lives | Survives the epic |
|---|---|---|
| what is being worked on **right now** | **here** | archived, not lost |
| why it is worth doing | `docs/next/<name>.md` | until delivered |
| what it measured | `docs/results/` | **yes** |
| what is open, in what order | `docs/ROADMAP.md` | **yes** |
| how the corpus itself is built | `docs/WORKFLOW.md`, `pc_package/TASKS.md` | **yes** |

`docs/pm/` is `state.json` made readable. It is not a second backlog: a thing that is not being
worked on now belongs in `docs/next/`, not here.

## Opening it in Obsidian

Open the **repository root** as the vault. Then `docs/`, `docs/pm/`, `docs/next/` and
`docs/results/` are all in one graph, and a link from a task to the page it changed resolves.

A task links to the **corpus documents** it is about by id (`PCR-003`), with the `.qmd` path beside
it. Those are not wikilinks: Obsidian indexes `.md`, and a `.qmd` would not resolve.

The board uses Dataview for its second view. Without the plugin the queries render as code blocks
and the plain tables above them are the board.
