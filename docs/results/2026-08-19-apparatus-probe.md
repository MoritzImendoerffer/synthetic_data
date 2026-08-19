# The apparatus probe: one section, two regimes, and the reader chose the one every counter would have rejected

**2026-08-19.** Work unit `2026-08-18_03_author-facing-apparatus`, TASK-001 to TASK-005. Proposal
[`docs/next/author-facing-apparatus.md`](../next/author-facing-apparatus.md). Decision **D4 = PASS**,
settled by the project owner on 2026-08-19.

The question was whether the author-facing apparatus — the counters printed back to the author,
the per-section rigor obligations, the 818-line guide — was the cause of the prose the owner
rejected in Track D, or whether the model was. The test was one section: the two `PCR-005`
Results subsections that all eight sentences quoted on 2026-08-18 came from, re-authored under a
minimal regime and read blind against the shipped text.

## 1. The two regimes

Same model (`claude-opus-5`), same facts, same helpers, same SETUP code, same rendered scaffold.
The only variable was what the author was told.

| | Track D pilot (shipped text) | the probe |
|---|---|---|
| words of instruction read | **29,454** (`WRITING_GUIDE.md` 7,835 · `REGISTER_EXEMPLAR.md` 10,389 · `section_plan.yaml` 5,849 · `STORY_BIBLE.md` 2,019 · brief 3,362) | **5,746** (a 240-word guide · the brief with §5c/§5d removed 2,581 · `STORY_BIBLE.md` · the setup code) |
| counters shown to the author | 12 gated + 5 advisory + 5 parser rows, printed after every `check_render` | none; no checker run; one pass |
| per-section obligations | `scaffold`, `register`, `rigor: […]`, "state directions + mechanism" | none |
| voice | 19 ✗ examples, corpus percentages, round history; 1,150-line exemplar | eight positive lines, one of them: *you are the process scientist who ran this study; explain the surfaces as you would in a paper* |
| grep lists to search the draft for | yes | none |

The guide is `.claude/work/2026-08-18_03_author-facing-apparatus/probe-guide.md`; the launch
prompt is `procedures/TASK-003.md`; the agent's transcript shows it read exactly those four files
plus `doe_report.py`/`_pcpkg.py` signatures.

## 2. The reading, verbatim

`A.pdf` and `B.pdf`, identical front matter and metadata; the key drawn by `secrets.choice`
before authoring and opened only after the verdict was committed
(`owner-reading-2026-08-19.md`).

> yes, the pdfs read fine. Explain step by step what did you change?

> I did not know that there is a difference, I read just A.pdf yet. Should I read B too, I guess?

> A clearly wins

Key: **A was the probe.** No sentence was quoted from either file. Rule fixed in the proposal:
PASS iff the probe is judged the better text and fewer than three of its sentences are quoted.
Better: yes. Quoted: 0. **PASS.**

Limit recorded in D4 before the reading: the owner had read the shipped subsections four times
the day before. The question asked was which reads as a paper.

## 3. What the counts say

All from `measure_apparatus.py` over the two untracked files
(`measure_probe.txt`); sources are the four published documents. Per 100 sentences unless marked.

### 3a. What moved with the reading

| | sources | shipped (59 sent.) | **probe (90 sent.)** |
|---|---|---|---|
| `, which` | 0.6–2.4 | 25.4 (15) | **5.6 (5)** |
| all trailing relatives | 1.2–3.0 | 28.8 (17) | **6.7 (6)** |
| `follows from the` | 0 | 1.7 (1) | **0** |
| `behaves as` | 0 | 1.7 (1) | **0** |
| `physical chemistry` / `confirms the expectation` / `aggressive` | 0 | 1.7 each | **0** |
| `governs` / `sets <noun>` | 0 | 5.1 (3) | 1.1 (1) |
| `acts on / acts through` | 0 | 1.7 (1) | **3.3 (3)** |

The trailing relative — the "sentence explaining itself" the owner named first on 2026-08-18 —
fell four to five times and the hollow-warrant frames went to zero, without any rule about
either. The one frame that survived is `acts on / through`, three times: "Protein load acts
through the mass of antibody the bed carries", "Load flow rate acts on recovery rather than on
selectivity", "The two factors … act on the same physical process". Each is followed by a concrete
quantity where the shipped text had a category, so the frame is a habit of the model, not the
fault itself. A ban on the phrase would not have been the fix; asking for the cause was.

### 3b. What moved the other way, and the reader did not mind

| | sources | shipped | **probe** |
|---|---|---|---|
| mid-sentence `, so ` | 0.1–0.4 | 0.0 | **8.9** |
| `, and ` + second clause (regex / parser) | 1.1–3.4 / 1.0–3.4 | 0.0 / 0.0 | **15.6 / 19.3** |
| opens with a connective | 3.7–6.1 | 11.9 | **0.0** |
| passive construction | 56.9–64.0 | 38.6 | **31.8** |
| topic chaining | 56–62 | 35.7 | 36.8 |
| `the <noun> is` per 1k words | 3.4–6.0 | 9.8 | **15.9** |
| staccato (sentences in a run of 3+ short) | 0.4–3.9 | 5.1 | 7.8 |

**Every measure the three previous rounds set as a target and moved is at or beyond its
round-zero level in the probe, and the owner preferred the probe "clearly".** `, so ` was the
first thing round one gated at ≤ 1.0 and drove to zero; the probe writes it in one sentence in
eleven. The `, and `+clause was what the owner named on reading round two; the probe writes it in
one sentence in six. The passive was round three's rule; the probe is thirty points below the
source band. This is the finding of the round: **those measures never tracked the reader's
judgement.** They tracked the surface of four guidance documents. Three rounds moved numbers a
reader does not read.

### 3c. The gate, as it stands, on the text the owner preferred

`uv run python authoring/check_style.py pc_package/PCR-005_protein_a.PROBE.qmd`
(`check_style_probe.txt`): **FAIL, 2 thresholds exceeded, 0 banned phrases.**

| row | probe | band | |
|---|---|---|---|
| % of sentences over 40 words | **1.1** | 3.0–21.5 | FAIL, too low |
| "rather than" per 1k words | **1.6** (3 in 1,829) | ≤ 0.8 | FAIL |
| mean sentence length | 20.3 | 20.0–30.5 | at the floor |
| median sentence length | 18.0 | 18.0–26.5 | at the floor |
| % of sentences under 15 words | 31.1 | 15.0–32.0 | at the ceiling |
| parenthetical openings per 1k | 3.3 | 3.0–14.5 | at the floor |

The shipped text passes every row (`check_style_excerpt.txt`: OK). Results §5.1 predicted a fail
on `mean_len` and `pct_under_15`; both sit within a tenth of their edge and the fail came on the
neighbouring rows instead. The direction is the one predicted: **the gate rejects the text the
reader preferred and passes the one the reader rejected.** The three "rather than" are ordinary
("no demonstrated lack of fit rather than proof that the quadratic form is complete") and one of
them is the guide's own tic list — a ceiling on a two-word phrase read off four documents that
happen not to use it.

## 4. What did the trick, in one paragraph

Substance in, surface rules out. The pilot's author was handed a specification — 22 counters,
a checklist of moves per section, hundreds of lines of examples of what not to write — and a
capable model satisfies the specification it is given: it wrote sentences shaped like explanations
that passed every counter. The probe's author was handed the study, a reader, and a role: *you are
the process scientist who ran this study; explain the surfaces as you would in a paper; name the
physical cause; use the terms of art.* Nothing was measured and nothing printed back. The model
already knew the chromatography (the paper-style rewrites in the Track D results page proved
that); the apparatus was suppressing it by making the task "satisfy the spec" instead of "explain
the study".

## 5. What this settles and what it does not

Settles: D4 = PASS, so tasks 2–6 of the proposal run — the gate is split into gated tics and
reviewer-only signals, the rigor obligations leave the section plan for a reviewer's checklist,
the guide is rewritten short and positive, the mechanism is supplied per step, and a content
review runs before promotion.

Does not settle: whether a whole document under the rebuilt apparatus reads as well as two
subsections did (one whole document is the next check, and the owner's call); whether the
`REGISTER_EXEMPLAR.md` helps or hurts (arm B was not run); whether the reader would have quoted
sentences from the probe on a fourth reading the way the shipped text drew eight on its fourth.
One section, one reader, one reading. The mechanistic_warrant audit is counted here
(`--spans`: 26 spans, 7 with a flagged frame — the six the Track D page named plus `PCR-006-R14`)
and repaired in [`rhetorical-layer-coverage.md`](../next/rhetorical-layer-coverage.md).

Two counts in the Track D page could not be reproduced by any pattern with code behind it and are
printed with the disagreement in `measure_apparatus.py` rather than tuned: `follows from the` 14
against the page's 12, `governs / sets` 97 against 108.

## 6. Verification

```bash
U=.claude/work/2026-08-18_03_author-facing-apparatus

# the two files the owner read, rebuilt from the template + setup code + shipped lines 747-876
uv run python $U/build_probe_scaffold.py          # rewrites the EXCERPT; the PROBE body is the agent's
md5sum $U/A.pdf pc_package/PCR-005_protein_a.PROBE.pdf $U/B.pdf pc_package/PCR-005_protein_a.EXCERPT.pdf

# every number in §3
uv run --extra discourse python $U/measure_apparatus.py \
    pc_package/PCR-005_protein_a.EXCERPT.qmd pc_package/PCR-005_protein_a.PROBE.qmd > $U/measure_probe.txt
uv run python authoring/check_style.py pc_package/PCR-005_protein_a.PROBE.qmd     # FAIL, 2 thresholds
uv run python authoring/check_style.py pc_package/PCR-005_protein_a.EXCERPT.qmd   # OK
uv run python $U/measure_apparatus.py --spans                                     # 26 / 7

# the corpus counts the script reproduces from the Track D page
uv run --extra discourse python $U/measure_apparatus.py --blocks frames $(ls pc_package/*.qmd)
```

The probe files are untracked and were never spliced into `PCR-005`. `git diff --stat outputs/
pc_package/ground_truth/ pc_package/*.qmd` is empty.
