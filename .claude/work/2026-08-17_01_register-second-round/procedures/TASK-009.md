# TASK-009 procedure — the documentation move (`/ship`)

Read `state.json` → `TASK-009` first. This runs under `/ship`; do not do it before TASK-008's page
exists and the owner's reading is on it. Two branches — pick by TASK-008's verdict AND the
owner's reading (decision D1 assumes both must agree for Track 2 to open).

## 1. `authoring/HANDOFF.md` §3a — "Tooling changes" table (starts line ~103)

Add one row each, in the table's existing column shape (what changed | why | effect):

- `check_style.py` — advisory clause-packing line and three `--compare` rows (mid-sentence
  `, so `, sentence-initial connective, 2+ coordinators); gated by nothing.
- `check_discourse.py` — chaining / copula / front field, spaCy behind `--extra discourse`,
  degrades to one line; wired to a `discourse` Makefile target only.
- `build_brief.py` §5d — discourse targets + the previous revision's own numbers; §1 scale line.
- `WRITING_GUIDE.md` §2d rule restated as a substitution; Correction 0 (owner's sentence) and the
  referent rule; §2d Correction 2's ✓ fixed; §2d bis substitution + band; Shape 4 positive
  example; §4a two rows; §4b "where the connective goes". `REGISTER_EXEMPLAR.md` "The step after
  the full stop".
- `PCP-003` / `PCR-003` re-authored a second time (round two); N spans re-anchored; new span count.

## 2. `pc_package/TASKS.md` — "Things that will catch you out" (line ~79)

Append two numbered items after the existing ones (there were seven after round one):

8. An inline `{python}` expression that yields a **name** (a response, a parameter) must never be
   the subject of a verb that agrees with it: `lof_p_lo_resp.lower()` produced "acidic variants is
   the case to watch". Put a runtime name after "is" or after a preposition.
9. The writing guide's own commentary is written in the register it forbids (0 % sentence-initial
   connectives, `, so ` in 1.5–5.9 % of its sentences). Verify voice against `refs/text/`, never
   against the guide's prose or the exemplar's commentary — only the *quotes* in the exemplar are
   source register.

## 3. `CLAUDE.md`

The Voice bullet: one sentence that the packing measures exist and are advisory, if TASK-003's
Environment sentence does not already cover it. Nothing else.

## 4. `docs/ROADMAP.md` — the register row

Say what is now true in one row: round two ran on <date>; the verdict; the owner's reading in a
clause. Branch:

- **open** → "Track 2: the remaining eighteen; budget ~40 re-anchored spans and an explicit pdf
  render per document; per-document counts from round two: <n>, <n>". Link the results page.
- **stop** → "the next target is <what the owner quoted>; the guide's-own-register hypothesis
  (exploration §4) is the first candidate". Link the results page.

The row stays unnumbered unless the owner places it.

## 5. `docs/next/register-from-four-sources.md` and `docs/next/README.md`

- **open** → rewrite the proposal to Track 2 alone: the problem (corpus split 2-of-20 on
  register), what it would take (18 one-pass re-authors, ~720 spans, 36 renders, the discrepancy
  carrier for D-001/D-002 already in place), verification (`make style` 20/20, strict grounding at
  the new N/N, `check_style --compare` on all 20 within the packing bands), what it does not do.
  Update the README row and its Status line.
- **stop** → rewrite the proposal to the new target with the owner's quoted sentences as the
  measurement, and the guide-commentary hypothesis as the first idea, with the numbers from
  exploration §4. Update the README row.
- If nothing remains → delete the file and its README row (git keeps it).

## 6. `docs/pm/decisions/D1-track-two-on-the-verdict.md`

Add "**Settled <date> by the project owner: option A/B.**" and set `status: settled`. If the owner
has not answered, the note moves to `docs/next/` as an open question (README rule) and is deleted
from `decisions/`.

## 7. `docs/pm/epic.md` and `docs/pm/_Archive.md`

- `epic.md`: change `status: planned` → `shipped`, add a **Shipped <date>** paragraph (what
  landed, the verdict, the link) — the previous epic's `epic.md` in
  `docs/pm/archive/2026-08-16_01_register-from-four-sources/epic.md` is the model.
- `_Archive.md`: add this epic's row to the second table (Epic | Shipped | What it produced), and
  leave the "currently on the board" sentence — the next `/explore` will change it.

Then `uv run python scripts/pm_notes.py` and check the board shows 9 of 9 done.

## 8. `docs/results/README.md`

TASK-008 added the row; check it links and that the page name matches.

## 9. Final gates, from a clean checkout of the branch

```bash
make test PY="uv run python" | tail -2
make style PY="uv run python" | tail -2
cd pc_package && uv run python build_ground_truth.py && uv run python validate_annex.py | tail -1 \
   && GROUNDING_STRICT_ANCHORS=1 uv run python check_grounding.py | tail -2 && cd ..
bash authoring/check_blank_repo.sh | tail -3
git diff --stat outputs/           # empty
```

Commit only the files whose text changed (the two rendered pairs, annexes, authoring artefacts,
docs); if a full rebuild rewrote other `.docx`/`.pdf`, restore each by name.
