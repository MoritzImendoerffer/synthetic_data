# TASK-003 procedure — brief §5d rows, and the guide's write-the-passive rule

Read `state.json` → `TASK-003` first. Depends on TASK-001 (regex keys) and TASK-002 (JSON keys).
Owner decision stands from round two: **minimum guide edits** — the rule, the search strings, the
numbers, the ✓ blocks; the guide's own commentary is Track C and is not touched here.

## 1. `authoring/build_brief.py` §5d — three rows (line ~238–262)

In the `rows` list after `_pct_coord2`:

```python
            ("mid-sentence `, and ` joining a second clause (%) — regex, a FLOOR; target <= 3.4", "_pct_and_clause"),
            ("mid-sentence `, not ` (%) — target <= 0.2", "_pct_not_tail"),
```

In `disc_rows` after front field:

```python
                     ("sentences with a passive construction (%) — a BAND, sources 54-60, never a floor", "passive"),
                     ("`, and ` + second clause, parser (%) — the other half of the regex row", "and_clause"),
```

The degrade branch already prints one "not measured" row for the spaCy measures; make its label
say `topic chaining / copula / front field / passive`. The two regex rows print regardless.

In the rules list, two entries **stated as substitutions**:

```python
    w("- A second independent clause after `, and ` becomes its own sentence. Search your draft for "
      "`, and the`, `, and this`, `, and both`, `, and it`, `, and each`, `, and none`; each is a full "
      "stop the sources would have written. This is the shape that gave round two away on its first "
      "sentence.\n")
    w("- Where the sources would write a passive, write the passive. A study, a design, a model or a "
      "process is never the AGENT of retain, carry, identify, select or show. Search your draft for "
      "`screening retained`, `the design carries`, `the model identifies`, `the study selected`. The "
      "sources put a passive in 54–60 % of their sentences; the previous revision of this report is at "
      "35 %, and \"the 4 factors that screening retained\" is what avoiding the passive produced.\n")
```

Then:

```bash
uv run --extra discourse python authoring/build_brief.py PCR-003 PCP-003
grep -n -A 22 "## 5d" authoring/out/PCR-003.brief.md | grep -E "and \` joining|not \`|passive|parser"
uv sync && uv run python authoring/build_brief.py PCR-003 | tail -1 && grep -c "not measured" authoring/out/PCR-003.brief.md && uv sync --extra discourse
bash authoring/check_blank_repo.sh | tail -1        # PASS
```

Expected in PCR-003's document column: `22.6`, `4.3`, `35.4 (146/413)`, `24.9 (105/413)`;
PCP-003: `18.2`, `0.0`, its passive and parser figures from TASK-002.

## 2. `WRITING_GUIDE.md` §2d — the write-the-passive rule (after line ~190)

Directly after Correction 0's last paragraph ("Put a runtime name after "is" or after a preposition,
never before the verb."), add:

```markdown
**Where the sources would write a passive, write the passive.** The same failure one step further
out. Correction 0 is an author supplying a *subject* the fact does not have; this is an author
supplying an *agent*. A study, a design, a model or a process does not retain, carry, identify,
select or show anything — the people who ran it did, and the sources say so with a passive. The
four sources put a passive construction in 54 to 60 % of their sentences (§4b); the round-two
`PCR-003` was at 35 %, having fallen at every revision, and the project owner's reading of it
named the cost. From `PCR-003`, *Executive summary*, as it stood on 2026-08-18:

> ✗ The 4 factors that screening retained then entered a face centred response surface design of
> 28 runs, and the remaining 4 parameters were assessed one at a time.

Screening is a study. It retained nothing. The sentence also carries the balanced `, and` second
clause that is its own fault (§2d above).

> ✓ The four factors retained from screening then entered a face centred response surface design
> of 28 runs. The remaining four parameters were assessed one at a time.

Every fact survives, the agent is gone, and the two steps are two sentences. Search a draft for
`screening retained`, `the design carries`, `the model identifies`, `the study selected`; each is a
place to write the passive the sources would have written.
```

Numbers in the ✓/✗ are quoted from the rendered round-two text as it stood; label the date. (This
is a guide example, not a document, so a typed number is permitted here as it is in the other
worked corrections.)

## 3. §2d's substitution paragraph (line ~164) — two more search strings

Where it says "Search for `, so ` and for `, and ` that introduces a second clause", make it:
"Search for `, so `, for `, and ` that introduces a second clause (`, and the`, `, and this`,
`, and both`, `, and it`), and for `, not `. Each one is a place where the sources would have
written a full stop." And add the two rates: "`, and ` + a second clause runs at 18 to 23 % of
corpus sentences against 1.1 to 3.4 % in the sources; mid-sentence `, not ` reached 4.3 % in the
round-two `PCR-003` against 0.0 to 0.2 %. `check_style.py` prints both back."

## 4. §4a — three diagnostic rows (after line ~497)

```markdown
| *Sentences with `, and ` + a second clause (regex, a floor) — not gated* | *diagnostic* | *3.4 %* | *1.1 %* | *1.3 %* | *3.1 %* |
| *Sentences with a mid-sentence `, not ` — not gated* | *diagnostic* | *0.2 %* | *0.0 %* | *0.1 %* | *0.0 %* |
| *Sentences with a passive construction — a BAND, not gated* | *diagnostic* | *54.3 %* | *59.8 %* | *59.6 %* | *58.4 %* |
```

and one sentence under the table's note: "The three rows added on 2026-08-18 are what the project
owner's reading of round two named; the passive row is a band — the plan sits inside it — and none
of the three fails anything."

## 5. The ✓-block scan — no ✓ block may model either new pattern

```bash
uv run python - <<'PY'
import re
for f in ('authoring/WRITING_GUIDE.md', 'authoring/REGISTER_EXEMPLAR.md'):
    lines = open(f).read().split('\n'); i, bad = 0, []
    AND = re.compile(r",\s+and\s+(?:the|this|that|these|those|it|they|its|their|a|an|[a-z]+ing)\b", re.I)
    NOT = re.compile(r",\s+not\s+", re.I)
    while i < len(lines):
        if lines[i].startswith('>'):
            j = i
            while j < len(lines) and lines[j].startswith('>'): j += 1
            text = ' '.join(l[1:].strip() for l in lines[i:j])
            for seg in re.split(r'(?=✓|✗)', text):
                if seg.startswith('✓') and (AND.search(seg) or NOT.search(seg)): bad.append((i+1, seg[:90]))
            i = j
        else: i += 1
    print(f, '-> ✓ blocks with , and +clause or , not :', len(bad)); [print('  ', b) for b in bad]
PY
```

Round two's TASK-002 found two ✓ blocks a line grep missed. **Fix every hit** by re-cutting the ✓
text into two sentences (keeping every fact); do not fix a ✗. Report the final count (0).

## 6. `REGISTER_EXEMPLAR.md` — the passive with a study as patient

Under "The step after the full stop", add **"The study is the patient, not the agent"** with at
least three verbatim source sentences where parameters/factors are *retained / carried forward /
identified / selected* in the passive. Search:

```bash
grep -n -i "were retained\|was carried forward\|were carried forward\|were identified as\|were selected" refs/text/amab.txt refs/text/pda60.txt refs/text/ispe_tt.txt refs/text/ispe_pv.txt | head -20
```

Pick sentences inside one page, from at least two sources, that name a study/design/screening and
use the passive. Attribute the way the file does. Then:

```bash
uv run python authoring/check_exemplar_quotes.py | tail -1        # N checked, 0 failed (N > 128)
make style PY="uv run python" | tail -1
```

## 7. Done when

Every acceptance line in `state.json` → `TASK-003` is true. Record the line numbers of each edit,
the ✓-scan count, and the exemplar checker's new total and pages.
