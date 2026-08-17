# TASK-007 procedure — promote, render, re-anchor, re-ground

Read `state.json` → `TASK-007` first. This is the boundary that must close: from step 1 until
step 8 passes, the corpus is mid-change. Do the steps in this order; the order is the point.

## 0. Before: list what quotes the two documents (RUNNER.md halt point)

- `pc_package/build_ground_truth.py` lines ~230–870: every `quote=`/`st(...)`/`add(...)` string in
  `build_step`, `build_equipment`, `build_sites`, `build_params`, `build_cqas`, `build_methods`,
  `build_studies`, `build_assertions`, `build_report_sections`, `build_design_spaces`,
  `build_proven_acceptable_ranges` (bioreactor pair; the other steps use `h_`, `pa_`, `vi_`, …
  prefixes and are NOT touched).
- `authoring/rhetorical/PCR-003.spans.yaml` — 35 curated spans, all over round-one text.
- `authoring/discrepancies.yaml` — D-001 (`PCP-003`) and D-002 (`PCR-003`) `registered_sentence`.
- `authoring/DISCREPANCIES.md` — quotes the registered sentences.
- `authoring/WRITING_GUIDE.md` — TASK-002 quoted round-one sentences as dated ✗ examples; they
  say "as it stood on 2026-08-17" and need no change. Confirm with
  `grep -n "as it stood" authoring/WRITING_GUIDE.md`.

## 1. Promote both drafts

```bash
cd pc_package
mv PCP-003_bioreactor.DRAFT.qmd PCP-003_bioreactor.qmd
mv PCR-003_bioreactor.DRAFT.qmd PCR-003_bioreactor.qmd
rm -f PCP-003_bioreactor.DRAFT.docx PCP-003_bioreactor.DRAFT.pdf PCR-003_bioreactor.DRAFT.docx PCR-003_bioreactor.DRAFT.pdf
cd ..
```

Inside each promoted file, check the title/subtitle no longer says DRAFT anywhere:
`grep -n DRAFT pc_package/PCP-003_bioreactor.qmd pc_package/PCR-003_bioreactor.qmd` → nothing.

## 2. Render both formats, explicitly

```bash
export PATH="$PWD/.venv/bin:$PATH"          # Quarto resolves python3 from PATH, not from uv
cd pc_package
quarto render PCP-003_bioreactor.qmd --to docx && quarto render PCP-003_bioreactor.qmd --to pdf
quarto render PCR-003_bioreactor.qmd --to docx && quarto render PCR-003_bioreactor.qmd --to pdf
cd ..
uv run python authoring/check_render.py pc_package/PCP-003_bioreactor.qmd pc_package/PCR-003_bioreactor.qmd | grep -iE "glyph|OK|FAIL"
```

`check_render.py` (without `--render`) glyph-checks the pdf on disk — which is now fresh. Expect 0
missing glyphs for both, and the style gate OK. Note page counts (`pdfinfo` or the render log);
round one was 30 pp and 51 pp.

## 3. Re-curate the PCR-003 rhetorical spans FIRST

If you skip this, `build_ground_truth.py` raises `SystemExit` at `build_rhetorical_spans` and
writes **nothing** — including `PCP-003.json` — and any grounding count you take is of stale files.

```bash
uv run python authoring/build_rhetorical_annex.py --doc PCR-003 --file pc_package/PCR-003_bioreactor.docx
```

It prints `FAIL RS-xxx [role] ungrounded quote: '…'` per missing span. For each: open
`authoring/rhetorical/PCR-003.spans.yaml`, find the span, read its `role` and `section`, find the
sentence in the NEW rendered text that plays that role in that section
(`uv run python -c "import sys; sys.path.insert(0,'pc_package'); from check_grounding import docx_text; print(docx_text('pc_package/PCR-003_bioreactor.docx'))" | grep -n "<key phrase>"`),
and replace the `quote` with a verbatim, whitespace-collapsed substring of it. Prefer number-free
spans (a seed change must not break them); a quote may not cross an inline number, a
cross-reference or bold. If a role genuinely has no sentence any more, delete the span and say so
in `outcome`; keep the `supported_by`/`restates`/`bounds` targets resolvable (the builder checks).
Update the file's header comment: "Re-curated <date> against the report re-authored in work unit
2026-08-17_01_register-second-round, TASK-007."

Re-run until it prints `OK    wrote authoring/out/PCR-003.rhetorical.json` with the span count.
Round one had 35; report the new count.

## 4. Rebuild the annexes and read the misses

```bash
cd pc_package
uv run python build_ground_truth.py 2>&1 | tail -5
uv run python validate_annex.py | tail -3                       # 20/20 valid
GROUNDING_VERBOSE=1 uv run python check_grounding.py 2>&1 | grep -E "^(OK|FAIL) +(PCP-003|PCR-003)|ungrounded quote|weak anchor" 
cd ..
```

Every `ungrounded quote: '…'` line is a string in `build_ground_truth.py` (or a curated span,
if step 3 missed one). For each:

1. `grep -n "<first six words of the quote>" pc_package/build_ground_truth.py` → the line.
2. Decide what the quote attests (which parameter, attribute, study, assertion, section).
3. Find the sentence or table row in the new rendered text that names the same record.
   - **Table rows**: rebuild the row from the same DataFrame the document renders, with
     `row_quotes()` / `param_row_quotes()` / `cqa_row_quotes()` and `table_header=rows.header`;
     never join cells with a space (`_join_cells()` uses `" | "`). If the row builders already
     produce the row, the quote may not need editing at all — the table did not change.
   - **Prose**: replace the string with a verbatim substring of the new sentence that names the
     record. The document is never edited to fit the quote.
4. Rebuild and re-check. Repeat until:

```bash
cd pc_package && GROUNDING_STRICT_ANCHORS=1 uv run python check_grounding.py | tail -3 && cd ..
```

prints `N/N quotes grounded across 20 annexes.` with no weak anchors. Report N against 2084 and
the number of quotes changed per document (round one: 24 and 56).

## 5. D-001 and D-002 survive

```bash
grep -n -A 8 "D-001\|D-002" authoring/discrepancies.yaml
```

For each, find the `registered_sentence` in the new rendered text of its document. If the wording
moved, update `registered_sentence` to the new verbatim sentence **without changing what it
claims** (the at-set-point commitment for D-001; the unqualified absolute for D-002), and update
the matching quote in `authoring/DISCREPANCIES.md`. Then confirm the annex still carries D-002:

```bash
grep -o '"description": "[^"]*"' pc_package/ground_truth/PCR-003.json | grep -i "step:production_bioreactor" ; grep -c "the only step" pc_package/ground_truth/PCR-003.json
```

(adjust the grep to the absolute D-002 actually registers; read `discrepancies.yaml` for it).

## 6. Weak claims still empty

```bash
uv run python -c "import json; [print(d, len(json.load(open(f'pc_package/ground_truth/{d}.json'))['weak_claims'])) for d in ('PCP-003','PCR-003')]"   # both 0
```

## 7. Nothing upstream moved

```bash
git diff --stat outputs/            # empty
make test PY="uv run python" | tail -2
make style PY="uv run python" | tail -2       # 20/20
```

## 8. What may be modified at the end

`git status --short` should list: the two `.qmd`, their `.docx` and `.pdf`, `build_ground_truth.py`,
`ground_truth/PCP-003.json`, `ground_truth/PCR-003.json`, `authoring/rhetorical/PCR-003.spans.yaml`,
`authoring/out/PCR-003.rhetorical.json`, `authoring/discrepancies.yaml`, `authoring/DISCREPANCIES.md`,
the two briefs. **No other rendered document and no other annex** — if `git status` shows other
`.docx`/`.json` files modified, you ran a full `make corpus`; restore each of the others by name
(`git checkout -- pc_package/PCR-005_protein_a.docx`), never a directory.

## 9. Done when

Every acceptance line in `state.json` → `TASK-007` is true; `outcome` records N/2084, the
re-anchored counts per document, the new span count, both page counts and both glyph results.
