# docs/pm/decisions — arguments a person has to settle

One note per decision that is **not the coding assistant's to make**. The board prints every open
one in its own section, above the task tables, because that section is the only part of the board
addressed to the project owner.

This README is skipped by the generator: a note is only listed when it carries `status: open`.

## The shape

```markdown
---
type: pm-decision
sprint: 2026-08-16_01_example
status: open          # open | settled
waiting_on: project owner
blocks: TASK-004, TASK-005      # or: nothing; it decides the next epic's scope
tags: [pm/decision]
---

# D1 — the question, as a question

**What is being asked.** One paragraph, with the numbers that make it a real choice.

**Option A.** What it costs and what it buys.

**Option B.** The same.

**What the plan assumes meanwhile**, so the work is not blocked while the argument is open.

**Settled 2026-08-20 by the project owner: option B.** <!-- added when it is answered -->
```

`blocks:` is read by `scripts/pm_notes.py`. A value containing a `TASK-` id makes the board say, in
its own sentence above the table, that a decision is holding work up. Say "nothing" when it holds
nothing up — an optional decision dressed as a blocker teaches the owner to ignore the section.

## What happens to one

`/ship` settles every open note before the epic closes. A settled decision records the answer and
who gave it and sets `status: settled`. One still open at ship time moves to `docs/next/`, because
an unresolved argument belongs where arguments live, and it is then deleted from here.

Settled notes are archived with their epic into `docs/pm/archive/<epic>/decisions/`. Nothing is
deleted.
