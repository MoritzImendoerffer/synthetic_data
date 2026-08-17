#!/usr/bin/env python3
"""Write `docs/pm/` from the active work unit, so project state is readable and navigable.

`.claude/work/<id>/state.json` is the machine's task list and nobody outside the session can
read it. This renders it as Markdown notes with YAML frontmatter, so "what is done, what is
left, what is waiting on me" has an answer that is not a chat message.

## What is generated and what is not

**Generated, overwritten on every run:** `_Board.md` and one `TASK-*.md` per task. Each carries
`generated: true` and says edits are lost. The source is `state.json`.

**Hand-written, never touched here:** `README.md`, `epic.md`, `_Artifacts.md`, `_Archive.md` and
everything under `decisions/`. A decision is an argument, and an argument is written by a person.

The two are separate **files**, never two halves of one. A note that mixes a render with
hand-written prose loses the prose on the next run, silently.

## One epic at a time, and the previous one is archived rather than deleted

`docs/pm/` holds the **active epic**. When `ACTIVE_WORK` names a different one, everything
belonging to the old epic moves to `docs/pm/archive/<epic>/` — notes, decisions and all — and the
board starts again. **Nothing is deleted**, so an old cycle can still be opened, and the board
only ever shows the epic being worked on.

Archiving happens at the **start of a new epic**, not at ship. A shipped epic stays on the board
until something replaces it, which is when you most want to look at it.

## Two shapes of state.json

The reader is deliberately tolerant. Work unit `2026-08-03_01_annex-anchors` predates this
workflow and writes `detail` where later units write `notes`, with no `acceptance` and no `type`.
Both read, and a missing field prints as "not recorded" rather than crashing the board. A board
that will not render is a board nobody looks at.

Run it:

    uv run python scripts/pm_notes.py
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PM = ROOT / "docs" / "pm"
ARCHIVE = PM / "archive"
WORK = ROOT / ".claude" / "work"

#: The corpus identifier scheme, fixed in CLAUDE.md. A task note links to the documents it is
#: about, which is how a reader gets from "TASK-003" to the thing that changed.
DOC_ID = re.compile(r"\b(?:PTP-001|RA-001|PCMP-001|PCMR-001|PC[PR]-0(?:0[3-9]|10))\b")

#: How many documents one task note may link to. A task that touches all 20 is a task whose note
#: is one long list, and the corpus index in `pc_package/README.md` is where a full list belongs.
MAX_DOC_LINKS = 8

#: `state.json` status to the word the board shows. Five, because a reader scanning a column
#: needs to tell "nobody has started" from "somebody is blocked".
STATUS = {"completed": "done", "pending": "todo", "in_progress": "doing",
          "blocked": "blocked", "partly_completed": "partly"}

#: The task kinds `/plan` assigns. They say what a task costs to verify: a `model` task forces a
#: full rebuild, an `annex` task does not.
KIND = {"model": "model", "document": "document", "annex": "annex", "mechanism": "mechanism",
        "measurement": "measurement", "documentation": "documentation", "wiring": "wiring",
        "contract": "contract"}

HEADER = ("> [!warning] Generated from `.claude/work/{unit}/state.json` by "
          "`scripts/pm_notes.py`.\n> Anything written here by hand is lost on the next run.\n")

UNFINISHED = ("todo", "doing", "blocked", "partly")

#: Who each unfinished state is waiting on. **Every row of the board names an actor**, because a
#: board that lists work without saying whose it is reads as a list of things the reader must do.
#: Only a `decisions/` note ever waits on the project owner; a task never does.
WAITING_ON = {"todo": "the assistant", "doing": "the assistant",
              "partly": "the assistant", "blocked": "another task", "done": "—"}


def active_unit() -> str:
    """The work unit `docs/pm/` is about, from `.claude/work/ACTIVE_WORK`.

    Empty when no unit is open. That is a normal state between epics, not an error.
    """
    marker = WORK / "ACTIVE_WORK"
    return marker.read_text().strip() if marker.exists() else ""


def generated_notes() -> list[Path]:
    """Every note in `docs/pm/` this script wrote, found by its `generated: true` marker.

    **Never by filename prefix.** An earlier version globbed `TASK-*.md`, which silently missed
    the whole of work unit `2026-08-03_01_annex-anchors`: its task ids are `T1` … `T11`, so its
    eleven notes matched nothing. The archive step then found no previous epic and would have left
    two epics' notes side by side on one board. The frontmatter marker is written by this script
    and does not depend on how a plan numbers its tasks.
    """
    return sorted(p for p in PM.glob("*.md") if "generated: true" in p.read_text())


def unit_on_disk() -> str:
    """Which epic the notes currently in `docs/pm/` belong to, or empty when there are none.

    Read from a generated note's `sprint:` line rather than from a file of its own. A separate
    marker file can disagree with the notes beside it, and then nothing says which is right.
    """
    for note in generated_notes():
        for line in note.read_text().splitlines():
            if line.startswith("sprint:"):
                return line.split(":", 1)[1].strip()
    return ""


def archive(previous: str) -> int:
    """Move the previous epic's notes into `archive/<epic>/`, and return how many moved.

    **Moved, never deleted.** An old cycle stays openable; it just stops being on the board.
    """
    if not previous:
        return 0
    target = ARCHIVE / previous
    target.mkdir(parents=True, exist_ok=True)
    moved = 0
    # Every generated note (the board and the task notes, whatever their ids) plus `epic.md`,
    # which is hand-written but belongs to the epic it describes.
    for note in generated_notes() + [PM / "epic.md"]:
        if note.exists():
            shutil.move(str(note), str(target / note.name))
            moved += 1
    decisions = PM / "decisions"
    if decisions.exists():
        for note in decisions.glob("*.md"):
            if note.name == "README.md":
                continue
            (target / "decisions").mkdir(exist_ok=True)
            shutil.move(str(note), str(target / "decisions" / note.name))
            moved += 1
    return moved


def corpus_documents() -> dict[str, str]:
    """Every corpus document id on disk, mapped to its `.qmd` path.

    Read from the filesystem rather than from a list in this file. A hard-coded roster goes stale
    the day a unit operation is added, and this script would then link a reader to nothing.
    """
    found: dict[str, str] = {}
    for qmd in sorted((ROOT / "pc_package").glob("*.qmd")):
        # Split on the first underscore rather than matching `DOC_ID` against the stem. `_` is a
        # word character, so the trailing `\b` never fires inside `PCR-003_bioreactor` and the
        # roster came back empty — the board printed "0 documents on disk" beside 20 of them.
        head = qmd.stem.split("_")[0]
        if DOC_ID.fullmatch(head):
            found[head] = f"pc_package/{qmd.name}"
    return found


def documents_mentioned(text: str, documents: dict[str, str]) -> list[str]:
    """The corpus documents this text names, in the order the corpus numbers them.

    Only an id that has a `.qmd` on disk is returned, so a note never points at a document that
    does not exist.
    """
    found = sorted({m for m in DOC_ID.findall(text) if m in documents})
    return found[:MAX_DOC_LINKS]


def file_link(path: str) -> str:
    """One file a task touched: a wikilink when a note sits at the other end, else code.

    `docs/PROJECT_WORKFLOW.md` becomes `[[PROJECT_WORKFLOW]]`, joining a task to the page it
    changed. A Python module or a `.qmd` stays code: there is no note to open, and a link that
    does not resolve is worse than none.
    """
    if path.endswith(".md") and path.split("/")[0] in ("docs", "authoring", "pc_package"):
        return f"[[{Path(path).stem}]] — `{path}`"
    return f"`{path}`"


def task_note(task: dict, unit: str, documents: dict[str, str]) -> str:
    """One task: what it owes, what it did, what it is about and what it touched."""
    status = STATUS.get(task["status"], task["status"])
    notes = task.get("notes") or task.get("detail") or ""
    about = documents_mentioned(
        " ".join([notes, task.get("outcome", ""), task["title"], " ".join(task.get("files", []))]),
        documents)

    lines = ["---", "type: pm-task", f"epic: {unit}", f"sprint: {unit}",
             f"task: {task['id']}", f"status: {status}",
             f"kind: {KIND.get(task.get('type', ''), task.get('type', ''))}",
             f"title: {json.dumps(task['title'])}", "generated: true",
             f"waiting_on: {WAITING_ON.get(status, '?')}",
             f"tags: [pm/task, pm/{status}]"]
    if about:
        lines.append("about: [" + ", ".join(f'"{d}"' for d in about) + "]")
    lines += ["---", "", HEADER.format(unit=unit),
              f"# {task['id']} — {task['title']}", "",
              f"**Epic:** [[epic]] · **Status:** `{status}` · "
              f"**Waiting on:** {WAITING_ON.get(status, '?')} · **Board:** [[_Board]]", ""]

    if task.get("requirement"):
        lines += [f"**Answers:** {task['requirement']}", ""]
    if notes:
        lines += ["## Why it exists", "", notes.strip(), ""]

    lines += ["## Acceptance criteria", ""]
    ticked = "x" if task["status"] == "completed" else " "
    lines += [f"- [{ticked}] {item}" for item in task.get("acceptance", [])] or \
             ["*Not recorded. This unit predates the acceptance-criterion rule.*"]
    if task.get("dependencies"):
        lines += ["", "**Depends on:** " + ", ".join(f"[[{d}]]" for d in task["dependencies"])]
    if task.get("outcome"):
        lines += ["", "## What was built", "", task["outcome"].strip()]
    if about:
        lines += ["", "## Documents it is about", ""]
        lines += [f"- **{doc}** — `{documents[doc]}`" for doc in about]
    lines += ["", "## Files it touched", ""]
    lines += [f"- {file_link(f)}" for f in task.get("files", [])] or ["- not recorded"]
    return "\n".join(lines) + "\n"


def task_table(tasks: list[dict], wanted: tuple[str, ...]) -> str:
    """A plain Markdown table of the tasks in `wanted` states.

    **Written out rather than queried.** The board is generated from the same file the tasks are,
    so a static table is correct the moment it is written and needs no plugin. The Dataview blocks
    below it are an alternative view, not the only way to read the page.
    """
    picked = [t for t in tasks if STATUS.get(t["status"], "todo") in wanted]
    if not picked:
        return "*None.*"
    rows = ["| Task | Status | Waiting on | Kind | What it is |", "|---|---|---|---|---|"]
    for task in picked:
        word = STATUS.get(task["status"], task["status"])
        rows.append(f"| [[{task['id']}]] | `{word}` | {WAITING_ON.get(word, '?')} | "
                    f"{KIND.get(task.get('type', ''), '')} | {task['title']} |")
    return "\n".join(rows)


def decision_table() -> tuple[str, bool]:
    """The open decisions, and whether any of them blocks a task.

    Returns `(table, blocks_a_task)`. They are hand-written and this script never writes them, so
    it lists what is on disk.

    **Each row prints what the decision blocks**, from the note's own `blocks:` line, and the
    sentence above the table is derived from the same field. A fixed sentence saying no decision
    blocks anything is false the first time one does, and an owner reading it would take every
    decision as optional.
    """
    folder = PM / "decisions"
    if not folder.exists():
        return "*None.*", False
    rows = ["| Decision | Waiting on | Blocks |", "|---|---|---|"]
    blocking = False
    for note in sorted(folder.glob("*.md")):
        # `README.md` documents the shape of a decision note and therefore contains a worked
        # example with `status: open` in it. Without this the folder's own instructions appeared
        # on the board as an open decision blocking two tasks that do not exist.
        if note.name == "README.md":
            continue
        text = note.read_text()
        if "status: open" not in text:
            continue
        title = next((line[2:].strip() for line in text.splitlines()
                      if line.startswith("# ")), note.stem)
        who = next((line.split(":", 1)[1].strip() for line in text.splitlines()
                    if line.startswith("waiting_on:")), "?")
        blocks = next((line.split(":", 1)[1].strip() for line in text.splitlines()
                       if line.startswith("blocks:")), "?")
        if "TASK-" in blocks:
            blocking = True
            blocks = ", ".join(f"[[{part.strip()}]]" if part.strip().startswith("TASK-")
                               else part.strip() for part in blocks.split(","))
        rows.append(f"| [[{note.stem}|{title}]] | {who} | {blocks} |")
    return ("\n".join(rows) if len(rows) > 2 else "*None.*"), blocking


def board(tasks: list[dict], unit: str) -> str:
    """The one page to open."""
    counted: dict[str, int] = {}
    for task in tasks:
        word = STATUS.get(task["status"], "todo")
        counted[word] = counted.get(word, 0) + 1
    summary = " · ".join(f"{n} {word}" for word, n in sorted(counted.items()) if word != "done")
    decisions, blocking = decision_table()
    consequence = ("**One of them blocks a task below**, named in its own row: until it is settled "
                   "that work cannot start." if blocking else
                   "None of them blocks the work below.")
    return f"""---
type: pm-board
epic: {unit}
sprint: {unit}
generated: true
tags: [pm/board]
---

{HEADER.format(unit=unit)}
# Board — the active epic

**[[epic|{unit}]]** · **{counted.get('done', 0)} of {len(tasks)} done**\
{' · ' + summary if summary else ''}

[[epic|Why this epic]] · [[_Artifacts|The corpus and its gates]] · [[_Archive|Finished epics]]

## Waiting on the project owner

**This is the only section that is yours.** Each is an argument a person has to settle.
{consequence}

{decisions}

## Not finished — the assistant's work, not the owner's

Nothing in this table needs the project owner. It is what the coding assistant has still to do,
and it is here so the state is visible, not so anyone else acts on it.

{task_table(tasks, UNFINISHED)}

## Done

{task_table(tasks, ("done",))}

---

## The same, as live queries

These need the Dataview plugin in Obsidian. **They query by tag, not by folder**, so they work
wherever the vault is rooted. A folder source such as `FROM "docs/pm"` only resolves when the
vault is opened at the repository root, which is the usual reason a table comes back empty.

Without the plugin these render as code blocks, and the tables above are the board.

```dataview
TABLE status, kind, title
FROM #pm/task
WHERE status != "done"
SORT status ASC
```

```dataview
TABLE waiting_on AS "waiting on"
FROM #pm/decision
WHERE status = "open"
```
"""


def main() -> int:
    unit = active_unit()
    PM.mkdir(parents=True, exist_ok=True)
    previous = unit_on_disk()

    if not unit:
        print("no active work unit (.claude/work/ACTIVE_WORK is empty or absent).")
        print(f"docs/pm/ still shows {previous or 'nothing'}. "
              "Run /explore <proposal> to open the next epic.")
        return 0

    # Load the new epic's tasks BEFORE archiving the old epic's notes. `/explore` opens a unit and
    # writes `ACTIVE_WORK`; `/plan` writes its `state.json` afterwards. A run in between used to
    # archive the previous board and then fail, leaving `docs/pm/` with no board at all — the old
    # epic was safe in `archive/`, but anyone opening the folder saw nothing.
    state_path = WORK / unit / "state.json"
    if not state_path.exists():
        print(f"ERROR  {state_path} does not exist. Run /plan before the board can show tasks.")
        print(f"docs/pm/ still shows {previous or 'nothing'}, and nothing was archived.")
        return 1
    state = json.loads(state_path.read_text())

    if previous and previous != unit:
        moved = archive(previous)
        print(f"archived {moved} note(s) of {previous} -> docs/pm/archive/{previous}/")
        print("Add a line to docs/pm/_Archive.md and write a new docs/pm/epic.md.")

    # A note left over from a task that no longer exists is removed. A stale note is worse than a
    # missing one: it reads as current.
    wanted = {f"{task['id']}.md" for task in state["tasks"]} | {"_Board.md"}
    for stale in generated_notes():
        if stale.name not in wanted:
            stale.unlink()
            print(f"removed stale {stale.name}")

    documents = corpus_documents()
    linked = 0
    for task in state["tasks"]:
        note = task_note(task, unit, documents)
        linked += "## Documents it is about" in note
        (PM / f"{task['id']}.md").write_text(note)
    (PM / "_Board.md").write_text(board(state["tasks"], unit))

    print(f"{len(state['tasks'])} task note(s) + the board -> {PM}")
    print(f"active epic: {unit}")
    print(f"corpus: {len(documents)} document(s) on disk, {linked} task(s) name one")
    return 0


if __name__ == "__main__":
    sys.exit(main())
