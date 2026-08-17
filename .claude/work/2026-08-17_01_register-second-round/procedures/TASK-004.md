# TASK-004 procedure — brief §5d: discourse targets and the document's own numbers

Read `state.json` → `TASK-004` first. Depends on TASK-001 (the packing measures) and TASK-003
(`check_discourse.py --json`).

## 0. Two rules of `build_brief.py` you must not break

1. **`authoring/check_blank_repo.sh` greps every `authoring/` file** for a line that has one of
   `read|open|bind|exemplar|source|baseline` AND a literal `pc_package/<name>.qmd` path on the
   same line, and fails if it finds one. So: build the path from variables
   (`os.path.join(PCPKG, f"{doc_id}_{key}.qmd")`), and never write a comment like
   "reads pc_package/PCR-003_bioreactor.qmd". Say "the previous revision" in comments.
2. **The brief never quotes a `.qmd`'s content.** §5d reads the previous revision only through
   `check_style.measure()` and `check_discourse.py --json`, to print numbers. Not one word of the
   document's prose enters the brief. Say this in the section's own note. The functional half of
   `check_blank_repo.sh` moves every `.qmd` aside; the brief must then print "no previous
   revision" and still build.

Run the probe before and after: `bash authoring/check_blank_repo.sh` (no `--render`) → exit 0.

## 1. Where

`authoring/build_brief.py`, in `build()`: §5c is written by `w(_discrepancy_assignments(doc_id))`
(~line 415) and §6 starts with `w("## 6. Cross-references\n\n")` (~417). Insert §5d between them,
**always emitted** — a section that disappears is indistinguishable from one that stopped being
generated (the same rule §5c follows).

## 2. Helper functions to add (module level, near `_discrepancy_assignments`)

```python
# The four source columns of the discourse targets. Read from check_style so the brief cannot
# drift from the gate; the packing figures are printed by check_style on every run.
def _register_columns():
    sys.path.insert(0, HERE)
    import check_style as cs
    cols = {}
    for name, fname, lo, hi in cs.HUMAN_SOURCES:
        path = os.path.join(ROOT, "refs", "text", fname)
        if os.path.exists(path):
            cols[name] = cs.measure(cs.prose_from_extract(path, lo, hi))[0]
    return cols


def _previous_revision_path(doc_id, key):
    """The committed .qmd of this document, or None. Used only to MEASURE its register."""
    if key is None:
        # corpus-level documents: PTP-001_transfer, RA-001_risk_assessment, PCMP-001_master_plan,
        # PCMR-001_master_report — take the filename from the registry's stem map if one exists,
        # else glob doc_id + "_*.qmd" in PCPKG.
        import glob
        hits = glob.glob(os.path.join(PCPKG, f"{doc_id}_*.qmd"))
        return hits[0] if hits else None
    p = os.path.join(PCPKG, f"{doc_id}_{key}.qmd")
    return p if os.path.exists(p) else None


def _discourse_json(path):
    """check_discourse --json --cap on one file, or None when spaCy is absent."""
    import json, subprocess
    out = subprocess.run([sys.executable, os.path.join(HERE, "check_discourse.py"),
                          "--json", "--cap", "--no-sources", path],
                         capture_output=True, text=True).stdout
    if not out.lstrip().startswith("{"):
        return None            # the one-line degrade message
    return json.loads(out)["columns"][os.path.basename(path)]


def _discourse_section(doc_id, key):
    import io
    b = io.StringIO(); w = b.write
    w("## 5d. Discourse targets — the numbers this document is written against\n\n")
    w("> Added 2026-08-17 (register round two). The previous revision of this document is read "
      "here ONLY to measure it; not a word of it is quoted, and it is not a voice model. "
      "`check_style.py` prints the first three rows back to you on every `check_render.py` run.\n\n")
    src = _register_columns()
    names = list(src)
    prev = _previous_revision_path(doc_id, key)
    mine = None
    if prev:
        sys.path.insert(0, HERE)
        import check_style as cs
        mine = cs.measure(cs.prose_from_qmd(prev))[0]
    w("| measure | " + " | ".join(names) + " | this document, previous revision |\n")
    w("|---|" + "---|" * (len(names) + 1) + "\n")
    rows = [("mid-sentence ', so ' (% of sentences) — target ≤ 1.0", "_pct_so_mid"),
            ("opens with a connective (% of sentences) — target ≥ 3.0", "_pct_initial_conn"),
            ("2+ clause coordinators (% of sentences)", "_pct_coord2"),
            ("sentences under 15 words (%) — band 15–32", "pct_under_15"),
            ("sentences over 40 words (%) — band 3–21.5", "pct_over_40")]
    for label, k in rows:
        cells = [f"{src[n][k]:.1f}" for n in names]
        cells.append(f"{mine[k]:.1f}" if mine else "no previous revision")
        w(f"| {label} | " + " | ".join(cells) + " |\n")
    disc = _discourse_json(prev) if prev else None
    if disc:
        w(f"| topic chaining (%) — must not fall more than 2 pt | 59.4 | 59.0 | 61.9 | 57.0 | {disc['chaining_pct']:.1f} ({disc['chaining'][0]}/{disc['chaining'][1]}) |\n")
        w(f"| copula main verb (%) — must not rise more than 2 pt | 17.6 | 14.8 | 22.4 | 26.1 | {disc['copula_pct']:.1f} ({disc['copula'][0]}/{disc['copula'][1]}) |\n")
        w(f"| adjunct front field (%) | 27.1 | 33.5 | 35.6 | 36.3 | {disc['front_pct']:.1f} ({disc['front'][0]}/{disc['front'][1]}) |\n")
    else:
        w("| topic chaining / copula / front field | | | | | not measured — `uv sync --extra discourse` |\n")
    w("\n**The rules, as substitutions (WRITING_GUIDE §2d, §2d bis):**\n\n")
    w("- One argument step per sentence. The next step opens the NEXT sentence with the "
      "connective (Therefore, However, As a result, For this reason). Search your draft for "
      "`, so ` and for `, and ` that starts a second clause; each is a full stop the sources would "
      "have written.\n")
    w("- The definite article or the noun, never `it is` / `it was`. Possessives sit in a band "
      "(its 0.27–0.40, their 0.50–0.96 per 1000 words), not at zero.\n")
    w("- Name the set you count: 'the four', 'both', 'the three' are named in the sentence or the "
      "paragraph already has.\n")
    w("- A `{python}` expression that yields a response or parameter NAME is never the subject of "
      "a verb that must agree with it. Put it after 'is' or after a preposition.\n")
    w("- Do not produce a connective to hit a count. Write the sentence that needs one.\n\n")
    return b.getvalue()
```

The hard-coded source values in the three spaCy rows (59.4 / 59.0 / …) are the pilot's published
figures with `--cap`; if you prefer, call `check_discourse.py --json --cap` without `--no-sources`
once and read them — slower (four sources parsed per brief) but never stale. Either is acceptable;
say which in `outcome`.

## 3. Wire it in

In `build()`, after `w(_discrepancy_assignments(doc_id))`:

```python
    # 5d. Discourse targets ------------------------------------------------------
    w(_discourse_section(doc_id, key))
```

## 3b. The module docstring

`build_brief.py`'s docstring says the brief "never reads a ``pc_package/*.qmd``". Amend that
sentence: "…never reads a ``pc_package/*.qmd`` for content. Since 2026-08-17 §5d measures the
previous revision's register (numbers only, through `check_style.measure`) so the author starts
knowing where it stood; on a blank repo it prints 'no previous revision'." Keep `*.qmd` with the
asterisk — the blank-repo grep matches only concrete file names.

## 4. §1 Identity — the scale line

In the `## 1. Identity` block, add for `key is not None`:

```python
        w("- **Commercial scale:** state it in the introduction via `V[\"commercial_scale_l\"]` "
          "(config `meta.commercial_scale_l`); the round-one PCR-003 never did.\n")
```

Check `V` is what the documents call `report_values` (PCP-003 line 91: `scale_l = V["commercial_scale_l"]`).

## 5. Run and check

```bash
uv run python authoring/build_brief.py PCR-003 PCP-003
grep -n -A 12 "## 5d" authoring/out/PCR-003.brief.md
```

Expect in the PCR-003 table: `8.0`, `0.9`, `5.4` in the last column of the first three rows, and
`30.7 (127/414)`, `32.5 (135/415)`, `9.2 (38/415)` if the extra is installed. PCP-003: `10.6`,
`1.8`, `9.3`; `34.4 (77/224)`, `27.6 (62/225)`, `10.2 (23/225)`.

Then:

```bash
bash authoring/check_blank_repo.sh | tail -4      # OK on both checks; the brief prints "no previous revision"
make test PY="uv run python" | tail -2
cd pc_package && uv run python build_ground_truth.py | tail -2 && uv run python validate_annex.py | tail -1   # 20/20
```

## 6. Done when

Every acceptance line in `state.json` → `TASK-004` is true. No `> ✓`/`✗` block and no example
sentence appears in §5d — grep the emitted brief for `✓` and `✗` and get nothing in that section.
