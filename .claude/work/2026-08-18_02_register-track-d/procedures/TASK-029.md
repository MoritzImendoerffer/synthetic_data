# TASK-029 procedure — measure the whole corpus, one method

## 1. One invocation, all 20

```bash
U=.claude/work/2026-08-18_02_register-track-d
uv run python $U/measure_trackd.py $(ls pc_package/*.qmd) > $U/measure_final.txt
```

Nothing else produces a number for the page. Compare every document against its own row in
`measure_baseline_style.txt` / `measure_baseline_discourse.txt`.

## 2. The corpus stopping rule, per document, all 19

`state.json` → `decisions.corpus_stopping_rule`. Nine conditions per document, plus two corpus
conditions: the median topic chaining across the 19 rises at least 5 points from the baseline
median, and `git diff outputs/` is empty with `weak_claims` empty in all 20 annexes. Within 0.5 pt
of an edge on any document: say so, write the plan's edge down first, and let the owner decide.

## 3. What the page must not claim

**There is no control column but `PCR-003` and the four sources.** Every previous round held a
document fixed and could therefore separate "the instruction works" from "the corpus drifted". If a
measure moves in all 19, the page reports that it moved and does not claim the instruction caused
it. `PCR-003` is the one document at the target register that this round did not touch; state its
row unchanged beside the 19.

## 4. Report the regressions this campaign already knows to look for

Round three found six measures moving away from the sources while the three targeted ones moved
toward them. Measure all of them across the 19 whether or not they were targeted, and report them
in their own section:

| measure | sources | what round three did |
|---|---|---|
| `, which` | 0.60–2.35 % | 9.50 → 15.33 % |
| staccato share | 0.37–3.94 % | 0.00 → 6.86 % |
| % under 15 words | 16.2–20.5 % | 19.5 → 26.1 % |
| mean sentence length | 24.2–30.2 | 23.3 → 22.1 |
| `its` per 1k | 0.27–0.40 | 0.51 → 1.66 |
| colons per 1k | 2.1–4.3 | 2.2 → 1.3 |

If they moved the same way in 19 documents, that is the strongest evidence the campaign has
produced about a substitution overshooting, and it is the input to whatever comes after Track D.

## 5. The page

`docs/results/<today>-register-track-d.md`, in the shape of
`docs/results/2026-08-18-register-round-three.md`. Per measure: four source columns, a baseline and
an after column for each of the 19, `PCR-003` as the control, every cell with its denominator.
Then the stopping rule line by line, the verdict in one sentence naming the line that decided it,
the owner's reading verbatim, and a `Files` table.

**Verify by script that every cell traces to `measure_final.txt`**, over every table row, as
round three did over its 71. Then add the row to `docs/results/README.md`.
