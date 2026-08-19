# Shared procedure — author ONE document under the rebuilt apparatus, one agent, one pass

**Used by every `document` task in this unit** (the pilot `PCP-005` and the eighteen batch
documents). Tested end to end on `PCR-007` in `2026-08-19_01_fourth-round-one-document`. The
regime is frozen: nothing here may be added to, and if the RUNNER is found wanting that is a
finding for the results page, not an edit to the prompt.

Substitute `<DOC>` (e.g. `PCP-005`), `<uokey>` (`protein_a`), `<Title>` (from `DOC_REGISTRY`,
e.g. `Protein A Chromatography (Step 5)`) and `<outline>` (`plan`, `report_doe`, `report_nondoe`,
`transfer_plan`, `risk_assessment`, `master_plan`, `master_report`).

## 1. Inputs, fixed before the agent exists

```bash
U=.claude/work/2026-08-19_02_fifth-round-plan-then-batches
uv run python authoring/build_brief.py <DOC>
grep -c "## 2b" authoring/out/<DOC>.brief.md       # 1 for a per-UO document (PCP/PCR), 0 for PTP/RA/PCMP/PCMR
grep -c "## 5d" authoring/out/<DOC>.brief.md       # 0 — no counter reaches the author
grep -A2 "## 5c" authoring/out/<DOC>.brief.md      # the registered-discrepancy assignment, or "None"
uv run python - <<'PY'
import re, sys
sys.path.insert(0,'pc_package'); from _pcpkg import DOC_REGISTRY
cls, title, key = DOC_REGISTRY['<DOC>']
t=open('authoring/template.qmd').read()
t=t.replace("__DOC_CLASS__",cls).replace("__DOC__","<DOC>").replace("__UO_KEY__",key).replace("__UO_TITLE__",title)
t=re.sub(r"<!--\s*=+\s*TEMPLATE — do not author here.*?-->\s*", "", t, flags=re.S)
open('pc_package/<DOC>_<uokey>.DRAFT.qmd','w').write(t)
PY
uv run python authoring/check_render.py pc_package/<DOC>_<uokey>.DRAFT.qmd | grep "all chunks"
```

The session that launches the agent must not have opened the shipped `pc_package/<DOC>_<uokey>.qmd`.

## 2. The launch prompt, verbatim (ONE agent, model override `opus`, fresh context)

> Author `<DOC>` (<Title>) per `authoring/RUNNER.md`, into
> `pc_package/<DOC>_<uokey>.DRAFT.qmd`, which is already instantiated from the template. Write the
> whole document in one pass, in the order `authoring/section_plan.yaml` → `<outline>` gives.
>
> Read, and read nothing else for facts or voice: `authoring/RUNNER.md` (the loop),
> `authoring/out/<DOC>.brief.md` (every number comes from here through the helper inventory;
> §2b is the step's mechanism, where present; §5c names any registered discrepancy this document
> must carry), `authoring/section_plan.yaml`, `authoring/STORY_BIBLE.md`,
> `authoring/WRITING_GUIDE.md`, `authoring/REGISTER_EXEMPLAR.md`. `pc_package/_pcpkg.py` and
> `pc_package/doe_report.py` may be read for function signatures. Do not open any
> `pc_package/*.qmd`, `authoring/rhetorical/` or `authoring/history/`.
>
> Every value is an inline `{python}` expression; a value with no helper becomes
> `<<NEEDS: …>>`, never a typed number. Gate as you go with
> `uv run python authoring/check_render.py pc_package/<DOC>_<uokey>.DRAFT.qmd --render` and fix
> what it reports yourself, in this context. When it passes, render the pdf:
> `cd pc_package && PATH="$PWD/../.venv/bin:$PATH" quarto render <DOC>_<uokey>.DRAFT.qmd --to pdf`.
>
> Report: which model you are, how many `check_render` passes you needed, the pdf result, the
> sentence and word counts, and any `<<NEEDS:>>` left (there should be none).
>
> The repository root is /home/moritz/github_repos/synthetic_data; run every command from there.

## 3. After the agent reports — the audit comes first

```bash
T=<the agent's transcript path>      # grep it; never read it into the session
python3 - <<'PY'
import json
T="<path>"; cmds=[]; reads=[]
def walk(o):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=='command' and isinstance(v,str): cmds.append(v)
            if k=='file_path' and isinstance(v,str): reads.append(v)
            walk(v)
    elif isinstance(o,list):
        for x in o: walk(x)
for line in open(T):
    try: walk(json.loads(line))
    except: pass
bad=[c.split('\n')[0][:140] for c in cmds if any(k in c for k in ("--review","check_discourse","measure_","reflow","shorts",".sentences(","prose_from_qmd","authoring/rhetorical","authoring/history"))]
qmd=[c.split('\n')[0][:120] for c in cmds if ".qmd" in c and "DRAFT" not in c and "template" not in c]
print("reads:", sorted(set(reads))); print("suspect:", bad); print("other qmd:", qmd)
PY
```

**If `suspect` or `other qmd` is non-empty, the draft is set aside** (copy it into the unit as
`<DOC>.DRAFT.runN-selfmeasured.qmd` with the offending commands), the finding is recorded, and a
fresh agent is launched with the same prompt. A `check_style.py --report … | head -6` for the counts
the prompt asks for is allowed (it prints gated rows only). Reading `check_style.py`'s source is
allowed (the guide points there for `BANNED`).

Then:

```bash
uv run python authoring/check_render.py pc_package/<DOC>_<uokey>.DRAFT.qmd --render 2>&1 | grep -iE "all chunks|NEEDS|gated|banned|render|glyph|^OK|^FAIL"
grep -c '<<NEEDS' pc_package/<DOC>_<uokey>.DRAFT.qmd                                 # 0
grep -nE "\b[0-9]+(\.[0-9]+)?\s?(%|°C|mmHg|g/L|L\b|mM|h\b|cm/hr|CV\b|mS/cm|psi|NTU|DV|days?)" pc_package/<DOC>_<uokey>.DRAFT.qmd | grep -v 'python}'   # each hit a statistical convention or code
grep -n "^# \|^## " pc_package/<DOC>_<uokey>.DRAFT.qmd                               # against section_plan.yaml <outline>
```

If the document carries a registered discrepancy (brief §5c not "None"), confirm the draft carries
the commitment in substance (ANNEX-A-BATCH §5); the wording may differ, the strength may not.

Counts: `check_style.sentences(check_style.prose_from_qmd(path))` — the count only — and pages from
the fresh pdf. Outcome: model (self-reported), passes needed, render, glyphs, `<<NEEDS>>`,
sentences, words, pages, the audit result. **No style row, no frame count, no discourse row.**

## 4. The content review, one cycle (part of the same task)

`2026-08-18_03_author-facing-apparatus/procedures/REVIEW-BEFORE-PROMOTION.md`: a fresh-context
agent (`opus`), the four questions verbatim, the DRAFT's PDF, nothing else. File run 1 as
`$U/content-review-<DOC>.md`. If any question reads "no": send the SAME authoring agent ONE message
with the flagged sentences as what each lacks (no count, no phrase to insert, the reviewer's
questions restated), let it revise and re-run `check_render` and the pdf itself; then a second
fresh judge, filed as run 2. One cycle only. Keep the pre-review draft as
`$U/<DOC>.DRAFT.pre-review.qmd`. Record run-1/run-2 counts per question in the outcome.
