# Procedure — author ONE Version 2.0 document, one agent, one pass, one review cycle

Adapted on 2026-10-08 from `2026-08-19_02_fifth-round-plan-then-batches/procedures/AUTHOR-A-DOCUMENT.md`.
There are two changes, both owner's decisions (`docs/next/rev2-campaign.md`). First, a report's
author reads the RENDERED text of its own plan and of PCMP-001, for content. Second, the rules
for mechanism and for report conventions changed (WRITING_GUIDE §2 rule 1 and §7,
REVIEW_CHECKLIST "Version 2.0").

Substitute these:
- `<DOC>`
- `<uokey>`, the file key. For a corpus document this is `investigation`, `master_plan`,
  `master_report`, `transfer` or `risk_assessment`.
- `<Title>`, from `DOC_REGISTRY`.
- `<outline>`, from `section_plan.yaml`.

## 1. Inputs, fixed before the agent exists

```bash
uv run python authoring/build_brief.py <DOC>
grep -c "## 2b" authoring/out/<DOC>.brief.md     # 1 for PCP/PCR, 0 for corpus documents
grep -c "## 5d" authoring/out/<DOC>.brief.md     # 0
grep -A2 "## 5c" authoring/out/<DOC>.brief.md    # the registered discrepancy, or "None"
uv run python - <<'PY'
import re, sys
sys.path.insert(0,'pc_package'); from _pcpkg import DOC_REGISTRY
cls, title, key = DOC_REGISTRY['<DOC>']
t=open('authoring/template.qmd').read()
uo_title = "A-Mab Drug Substance" if key is None else title
t=t.replace("__DOC_CLASS__",cls).replace("__DOC__","<DOC>").replace("__UO_TITLE__",uo_title)
t=t.replace('"__UO_KEY__"', 'None' if key is None else f'"{key}"')
sub = f"A-Mab Drug Substance — <DOC>" if key is None else f"A-Mab Drug Substance — {title} — <DOC>"
t=t.replace("__SUBTITLE__", sub)
t=re.sub(r"<!--\s*=+\s*TEMPLATE — do not author here.*?-->\s*", "", t, flags=re.S)
open('pc_package/<DOC>_<uokey>.DRAFT.qmd','w').write(t)
PY
uv run python authoring/check_render.py pc_package/<DOC>_<uokey>.DRAFT.qmd | grep "all chunks"
```

## 2. The launch prompt (ONE agent, model `opus`, fresh context)

> Author `<DOC>` (<Title>) at Version 2.0 per `authoring/RUNNER.md`, into
> `pc_package/<DOC>_<uokey>.DRAFT.qmd`, which is already instantiated from the template. Write the
> whole document in one pass, in the order `authoring/section_plan.yaml` → `<outline>` gives.
>
> Read, and read nothing else for facts or voice: `authoring/RUNNER.md` (the loop),
> `authoring/out/<DOC>.brief.md` (every number comes from here through the helper inventory.
> §2b is the step's mechanism where present, §4c the Version 2.0 facts and the complex tables
> to carry, and §5c any registered discrepancy this document must carry),
> `authoring/section_plan.yaml`, `authoring/STORY_BIBLE.md` (§9b is the Version 2.0 story),
> `authoring/WRITING_GUIDE.md` and `authoring/REGISTER_EXEMPLAR.md`. `pc_package/_pcpkg.py`,
> `pc_package/doe_report.py` and `pc_package/tables.py` may be read for function signatures.
> <READS> Do not open any `pc_package/*.qmd`, `authoring/rhetorical/` or `authoring/history/`.
>
> Every value is an inline `{python}` expression or a helper call. A value with no helper becomes
> `<<NEEDS: …>>`, never a typed number. Gate as you go with
> `uv run python authoring/check_render.py pc_package/<DOC>_<uokey>.DRAFT.qmd --render`, and fix
> what it reports yourself, in this context. When it passes, render the pdf:
> `cd pc_package && PATH="$PWD/../.venv/bin:$PATH" quarto render <DOC>_<uokey>.DRAFT.qmd --to pdf`.
> Look at every complex table in the pdf once (`pdftoppm` a page to png and read it) and fix a
> table you call wrongly.
>
> Report: which model you are, how many `check_render` passes you needed, the pdf result, the
> sentence and word counts, and any `<<NEEDS:>>` left (there should be none).
>
> The repository root is /home/moritz/github_repos/synthetic_data; run every command from there.

`<READS>` per document type:
- **PCR-00N:** "For content only, and never for voice, read the rendered text of your own
  approved plan, `pdftotext -layout pc_package/PCP-00N_<uokey>.pdf -`, and of the master plan,
  `pdftotext -layout pc_package/PCMP-001_master_plan.pdf -`. The study was run under them, so
  your report states its results against what they commit to."
- **PCP-00N, PTP-001, RA-001, PCMR-001:** the rendered `PCMP-001_master_plan.pdf`, as above.
  PCMR-001 also reads every rendered `PCR-00N` PDF.
- **INV-001:** "For content only, read the rendered text of the Version 1.0 documents you
  investigate, `pdftotext -layout pc_package/superseded/rev1/<ID>_*.pdf -`. An investigation
  cites what the record said. Quote a Version 1.0 sentence only where a finding rests on it."
- **PCMP-001:** none beyond the bound inputs.

## 3. After the agent reports — the audit, then the gates

Grep the transcript for commands. If any command opened a `pc_package/*.qmd` other than its
DRAFT or the template, or ran `check_style.py --review`, `check_discourse`, `measure_*`,
`authoring/rhetorical` or `authoring/history`, the draft is set aside and a fresh agent runs.
Reading a rendered PDF that this procedure lists for the document is allowed. Any other PDF is
a finding.

```bash
uv run python authoring/check_render.py pc_package/<DOC>_<uokey>.DRAFT.qmd --render 2>&1 | grep -iE "all chunks|NEEDS|gated|banned|render|glyph|^OK|^FAIL"
grep -c '<<NEEDS' pc_package/<DOC>_<uokey>.DRAFT.qmd
grep -n "^# \|^## " pc_package/<DOC>_<uokey>.DRAFT.qmd
```

## 4. The content review, one cycle

A fresh-context agent (`opus`) is given the DRAFT's PDF text and this prompt, and nothing else.
Run 1 is filed as `<unit>/content-review-<DOC>.md`. If any question reads "no", the SAME
authoring agent gets ONE message with the flagged sentences, each stated as what it lacks (no
count, no phrase to insert). It revises and re-renders, and a second fresh judge runs. One cycle
only.

> Read the attached document, a controlled process characterization document written to support
> a Biologics License Application. Answer these questions sentence by sentence. Quote each
> sentence you flag exactly, and say in one line which question it fails and why. Then answer
> each question yes or no for the document as a whole.
>
> 1. Where the text gives a cause ("because", "since", "governs", "sets", "acts on"), does it name
>    a physical cause (a species, an interaction, a property of the resin, the buffer or the
>    culture, and a direction) in the clause where the verb stands?
> 2. Is every technical term a term of art in the chromatography, cell-culture, analytical or
>    virology literature?
> 3. Does any sentence tell the reader how to file the finding it has just stated (a trailing
>    clause that renames the finding as a category, or a gloss that answers an objection nobody
>    raised)?
> 4. Is every acceptance criterion stated with its basis, and every result reported against its
>    criterion as met or not met?
> 5. Is any statement scientifically wrong, or contradicted by a table or figure in the same
>    document? Name each one with the table it conflicts with.
> 6. Which sentences read as written by a machine rather than by a process scientist (padding,
>    restatement, hedged emphasis, a sentence that says nothing a reader would miss)? A sentence
>    that is plain and short is not a flag.
> 7. Can each sentence be understood by a reader in the field who has not read the rest of the
>    document? Flag a sentence that refers to something by a code or label alone (a finding
>    number, a rule code, a study code, a criterion code) when the thing is not named in the same
>    sentence, and a sentence whose subject is an abstract stand-in for what was done or found
>    ("the safety factor stood in for the worst case of downstream performance"). Say in a few
>    words what the sentence should name instead.
>
> Report: which model you are, the flagged sentences grouped by question, and the seven yes/no
> answers (for questions 6 and 7, "yes" means no sentence was flagged).
