# TASK-030 procedure — the documentation move

This is `/ship`'s work. Run `/ship` with no argument first: it runs every check and stops.

## What is different about this one

- **The full rebuild is mandatory and long.** 19 `.qmd` changed, so
  `make clean && PATH="$PWD/.venv/bin:$PATH" make data figures corpus PY="uv run python"` is the
  reproduction check, and it renders 40 files. Compare rendered **text** through
  `check_grounding.docx_text`, never by file hash — every binary shows modified on every render
  because of embedded timestamps. Restore the text-identical ones **by name**.
- **Re-measure the page band.** `CLAUDE.md` and `TASKS.md` item 6 carry "reports with a DoE run
  41–56 pp, non-DoE 26–28, plans 23–31". Nineteen re-authors will move it. Measure from the fresh
  PDFs and correct both files; this band has already gone stale once, when `PCR-003` went 59 → 56.
- **`docs/next/rhetorical-layer-coverage.md` must be rewritten, not ignored.** TASK-001 closed half
  of it: one mechanism now exists. What remains is the eleven documents that carry no layer.
- **The proposal.** If Track C is still open, rewrite `register-from-four-sources.md` down to Track
  C alone. If Track C is also settled, delete it and drop the row from `docs/next/README.md`.

## The rows to add

- `authoring/HANDOFF.md` §3a: one model row for the corpus-wide re-author (documents, quotes
  re-anchored, spans re-cut, page counts before and after), and one tooling row for the
  rhetorical-layer unification.
- `pc_package/TASKS.md`: anything this round found that somebody could get wrong twice.
- `docs/ROADMAP.md`: the register row says what is true. If the corpus is at one register, say so
  with the numbers and the results link.

## Then

`docs/pm/epic.md` says what shipped **and what did not**; `docs/pm/_Archive.md` gains the row
before the notes move; `uv run python scripts/pm_notes.py`; `metadata.json` → `delivered`;
`.claude/work/ACTIVE_WORK` cleared. Settle every open `docs/pm/decisions/` note or move it to
`docs/next/`.
