# Shared procedure — promote a batch, render, re-anchor, re-ground

**Used by all 6 `annex` tasks.** This is the boundary that must close: from step 1 until step 7
passes, the corpus is mid-change. Do the steps in this order; the order is the point. Generalised
from `2026-08-18_01_register-third-round/procedures/TASK-005.md`, which did it for one document.

**Serial.** `pc_package/build_ground_truth.py` is one 7600-line file. Two agents editing it
concurrently lose each other's writes, so no annex task overlaps another, or any authoring.

## 1. Promote every draft in the batch

```bash
cd pc_package
for f in <DOC>_<uokey> …; do git mv "$f.DRAFT.qmd" "$f.qmd" -f; rm -f "$f.DRAFT.docx" "$f.DRAFT.pdf"; done
cd ..
grep -n DRAFT pc_package/<each>.qmd       # nothing
```

## 2. Render both formats, explicitly

```bash
export PATH="$PWD/.venv/bin:$PATH"        # Quarto resolves python3 from PATH, not from PY
cd pc_package
for f in <each>; do quarto render "$f.qmd" --to docx && quarto render "$f.qmd" --to pdf; done
cd ..
uv run python authoring/check_render.py pc_package/<each>.qmd | grep -iE "glyph|OK|FAIL"
```

Expect 0 missing glyphs on each **fresh** pdf. Record every page count — the corpus page band in
`CLAUDE.md` and `TASKS.md` is re-measured from these at ship, and it has moved once already.

## 3. Re-curate the rhetorical spans FIRST, for every document in the batch that has one

After TASK-001 all nine live in `authoring/rhetorical/<DOC>.spans.yaml`. If you skip this,
`build_ground_truth.py` raises at `build_rhetorical_spans` and writes **nothing** — including the
annexes of documents this batch did not touch — and any grounding count you then take is of stale
files.

```bash
uv run python authoring/build_rhetorical_annex.py --doc <DOC> --file pc_package/<DOC>_<uokey>.docx
```

For each `FAIL … ungrounded quote`, open the spans file, read the span's `role` and `section`,
find the sentence in the NEW rendered text that plays that role in that section, and replace the
quote with a verbatim whitespace-collapsed substring of it. Prefer quotes with **no digits** and
**no `R²`/`R2`** — a quote crossing an inline value breaks on a seed change, and the two
extractors disagree on the superscript.

**Test every span under BOTH extractors before the builder runs.** This trap cost round two a
cycle at RS-J02:

```bash
uv run python - <<'EOF'
import sys, re, yaml
sys.path.insert(0,'pc_package'); sys.path.insert(0,'authoring')
from check_grounding import docx_text as cg          # yields "R2"
import build_rhetorical_annex as bra                 # yields "R²"
f = "pc_package/<DOC>_<uokey>.docx"
a, b = cg(f), bra.doc_text(f)
collapse = lambda s: re.sub(r"\s+", " ", s).strip()
for s in yaml.safe_load(open("authoring/rhetorical/<DOC>.spans.yaml"))["spans"]:
    q = collapse(s["quote"])
    if not (q in a and q in b):
        print("FAIL", s["id"], q in a, q in b, q[:80])
EOF
```

Update the file's header comment with the date and this work unit. Re-run until the builder prints
`OK wrote authoring/out/<DOC>.rhetorical.json` with the span count, and **drops none**.

## 4. Rebuild the annexes and read the misses

```bash
cd pc_package
uv run python build_ground_truth.py 2>&1 | tail -3
uv run python validate_annex.py | tail -2                       # 20/20 valid
GROUNDING_VERBOSE=1 uv run python check_grounding.py 2>&1 | grep -E "^(OK|FAIL)|ungrounded quote|weak anchor"
cd ..
```

Every `ungrounded quote` is a string in `build_ground_truth.py`. For each:

1. `grep -n "<first six words>" pc_package/build_ground_truth.py`.
2. Decide what the quote attests — which parameter, attribute, study, assertion or section.
3. Find the sentence or row in the new text that names the same record.
   - **Table rows** usually need nothing: the row builders rebuild the row from the DataFrame the
     document renders, so every table-row quote survived untouched in rounds two and three. Never
     join cells with a space; `_join_cells()` uses `" | "`.
   - **Prose**: replace with a verbatim substring of the new sentence that names the record. The
     document is never edited to fit a quote, and no threshold is ever raised to make a weak
     anchor pass.
4. Rebuild and re-check until `GROUNDING_STRICT_ANCHORS=1 uv run python check_grounding.py` prints
   `N/N quotes grounded across 20 annexes` with no weak anchors.

**Read every `report_sections` statement of every document in the batch, not just its quote.**
Round three found two statements asserting something the re-authored report no longer said — one
claimed the models were "predictive for four of them", which the new text never says. The quote
grounded; the statement was false. No gate catches this.

## 5. Registered discrepancies

For every document in the batch carrying one — `D-001` in `PCP-003`, `PCP-006`, `PCP-008`,
`PCP-009`, `PCR-006`, `PCR-008`, `PCR-009`; `D-002` in `PCR-003`, which this round does not touch:

```bash
uv run python -c "
import yaml,re,sys; sys.path.insert(0,'pc_package')
from check_grounding import docx_text
d=yaml.safe_load(open('authoring/discrepancies.yaml'))
rs=d['items']['<DOC>'][0]['assignment']['registered_sentence']
print(re.sub(r'\s+',' ',rs) in re.sub(r'\s+',' ',docx_text('pc_package/<DOC>_<uokey>.docx')))"
```

If the wording moved, update `registered_sentence` **without changing what it claims**, and update
the quote in `authoring/DISCREPANCIES.md` to match. The two files must agree.

## 6. Weak claims still empty

```bash
uv run python -c "import json,glob;print({f.split('/')[-1][:-5]: len(json.load(open(f))['weak_claims']) for f in sorted(glob.glob('pc_package/ground_truth/*.json'))})"
```

All 20 must be 0.

## 7. Nothing outside the batch moved

```bash
git status --short
git diff --stat outputs/          # empty
make test PY="uv run python" | tail -1
make style PY="uv run python" | grep -cE "^OK"     # 24
```

`git status` must list only this batch's `.qmd`/`.docx`/`.pdf`, `build_ground_truth.py`, this
batch's `ground_truth/*.json`, its `authoring/rhetorical/*.spans.yaml`, and the discrepancy files
if a wording moved. If another document's rendered file or annex appears, a full `make corpus`
ran — restore each of the others **by name**, never `git checkout -- pc_package/`, which also
holds the uncommitted work this task is producing.

## 8. Done when

Every acceptance line in `state.json` for that task is true. `outcome` records N/2084, the quotes
re-anchored **per document**, the span counts, every page count and every glyph result.
