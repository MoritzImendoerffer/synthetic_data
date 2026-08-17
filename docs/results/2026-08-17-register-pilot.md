# The register pilot: two documents re-authored, five shapes measured

**Run date:** 2026-08-17. **Work unit:** `2026-08-16_01_register-from-four-sources`, TASK-007
to TASK-009. **Documents:** `PCP-003` (plan) and `PCR-003` (report), the production bioreactor
pair. **Before** is the text at commit `b0361f1`, kept at
`.claude/work/2026-08-16_01_register-from-four-sources/pre-rewrite/`.

**Verdict in one line: run one more two-document round before committing to the other eighteen.**
Of the five shapes, one moved cleanly, one moved but should not be counted as a win, and three
did not move — two of them backwards.

**This page was revised on 2026-08-17, after it was first written.** Its first version reported
"two of five moved" and led with the possessive result. The project owner then read `PCR-003`
and reported that the possessives had not struck them as excessive. Checking that against the
text showed they were right, and that the possessive rule had a measured cost in the plan. The
sections *The one that should not be counted* and *Why two moved and three did not* are the
result. The measurements themselves did not change.

## Why the run happened

The project owner's complaint was that the corpus "is written in a way no SME would write".
`docs/next/register-from-four-sources.md` established that this is a discourse problem rather
than a sentence-statistics problem, that the writing guide's own rules were part of the cause,
and that no threshold of the kind `check_style.py` already has could reach it. Six tasks then
amended the guide (§2c, §2d, §2d bis), added a seven-pattern argument-moves catalogue to the
exemplar, removed the `therefore` ceiling, extracted the two ISPE sources, and gave the brief a
discrepancies section. Nothing had been authored from any of it.

TASK-007 re-authored both documents in one pass, one agent each, neither reading the other's
draft or any sibling `.qmd`. This page measures the result.

## What changed

All figures from `register_analysis.ipynb` §13, re-executed end to end on 2026-08-17. The four
human sources are read at the page ranges `check_style.HUMAN_SOURCES` itself calibrates on, so
the reference columns cannot drift from the gate's. Sentence counts: PDA TR 60 820, A-Mab 1041,
ISPE TT 669, ISPE PV 808; `PCP-003` 202 → 226, `PCR-003` 433 → 423.

### The one that worked

**The connective repertoire**, from `check_style.measure`, so these are the numbers the gate
prints on every run.

| | rate per 1k | distinct | count / words |
|---|---|---|---|
| PDA TR 60 | 2.72 | 9/9 | 54 / 19,856 |
| A-Mab | 2.68 | 7/9 | 74 / 27,649 |
| ISPE TT | 2.24 | 7/9 | 42 / 18,731 |
| ISPE PV | 2.62 | 6/9 | 64 / 24,425 |
| `PCP-003` before | 1.27 | **3/9** | 6 / 4,718 |
| `PCP-003` after | 3.46 | **6/9** | 19 / 5,489 |
| `PCR-003` before | 3.67 | **3/9** | 38 / 10,346 |
| `PCR-003` after | 3.54 | **6/9** | 34 / 9,614 |

The repertoire doubled in both, from 3 of 9 to 6 of 9. Note what the *rate* column shows: the
old `PCR-003` was already at 3.67 per 1000 words, above every source, while using three
connectives. The rate was never the defect and would have been a misleading target. The
diagnostic that matters is the distinct count.

### The one that should not be counted

**Possessives per 1000 words.** This was reported as the largest single divergence any method
found, and it moved further than anything else. It should still not be scored as a win.

| | PDA TR 60 | A-Mab | ISPE TT | ISPE PV | PCP-003 before → after | PCR-003 before → after |
|---|---|---|---|---|---|---|
| *its* | 0.40 | 0.32 | 0.27 | 0.36 | 5.72 → 0.36 | 6.66 → 0.31 |
| *their* | 0.96 | 0.50 | 0.63 | 0.69 | 3.18 → 0.18 | 4.15 → 0.83 |
| *it* | 3.12 | 1.75 | 3.33 | 3.19 | 7.42 → **12.02** | 10.62 → 8.20 |

Denominators: 4,719 → 5,491 words for `PCP-003`, 10,354 → 9,631 for `PCR-003`.

**The magnitude is a ratio artefact.** Fourteen times the source rate sounds decisive. In counts
it is 69 instances of `its` in 10,354 words of `PCR-003`, which is one every 6.3 sentences — a
density no reader experiences as a tic. The project owner read the report and reported that the
possessives had not struck them as excessive, which is the only human reading taken during this
epic and it contradicts the measure. A large ratio on a rare feature is not a perceptible defect,
and the corpus now has two instances of that mistake: this one, and the one-sided sentence-length
cap whose correction over-corrected into 17-word averages (`authoring/HANDOFF.md` §3a, tooling
changes).

**A fifth of the instances were the case the rule licenses.** The most frequent phrases in the
old `PCR-003` were `its normal operating range` (6), `its characterized range` (5) and
`its set-point` (4). The range does belong to that parameter. §2d bis says so itself: "Keep a
possessive for a genuine relationship the reader would otherwise mistake — 'its characterization
range' when two parameters are in play and the range belongs to one of them."

**And in the plan it was paid for in copulas.** Counting the constructions directly:

| `PCP-003` (plan) | `its` | `it is` / `it was` / `it will be` | `the <noun> is` |
|---|---|---|---|
| before | 27 | 7 | 39 |
| after | **2** | **21** | **48** |

| `PCR-003` (report) | `its` | `it is` / `it was` / `it will be` | `the <noun> is` |
|---|---|---|---|
| before | 69 | 53 | 105 |
| after | **3** | **22** | **103** |

The plan removed 25 possessives and added 23 copulas. That accounts for its whole copula
regression below (18.4 % → 27.6 %) and for `it` rising to 12.02 per 1000 words against a source
ceiling of 3.33. The report removed 66 possessives and 31 expletives, with `the <noun> is` flat,
and its copula rate barely moved.

Same rule, two agents, opposite implementations. **The rule is not wrong, it is
under-specified**: it says what to remove and not what to put there. §2d bis needs the
substitution named — the definite article or the noun, never `it is` — and the target bounded
rather than minimised, so the licensed exception shows up in the numbers instead of being
driven out of them.

### The three that did not

**Topic chaining** — the largest single finding of the original analysis, and the one no rule
could reach directly.

| | chained / pairs | % |
|---|---|---|
| PDA TR 60 | 332/559 | 59.4 |
| A-Mab | 315/534 | 59.0 |
| ISPE TT | 348/562 | 61.9 |
| ISPE PV | 321/563 | 57.0 |
| `PCP-003` before | 62/200 | 31.0 |
| `PCP-003` after | 77/224 | **34.4** |
| `PCR-003` before | 148/422 | 35.1 |
| `PCR-003` after | 127/414 | **30.7** |

Up 3.4 points in the plan, **down 4.4 points in the report**. Both sit around 32 % against a
source floor of 57 %. This is the null result the plan asked to be reported, and it is the most
important line on this page: §2d has stated the given-new rule all along, TASK-005 exemplified
it with three worked corrections, and the measure did not move. Exemplifying a rule is not
enough to make an author apply it 400 times in a row.

**Copula main verb** (ROOT lemma is `be`).

| | copula / n | % |
|---|---|---|
| A-Mab | 61/412 | 14.8 |
| PDA TR 60 | 74/420 | 17.6 |
| ISPE TT | 95/424 | 22.4 |
| ISPE PV | 110/422 | 26.1 |
| `PCP-003` before | 37/201 | 18.4 |
| `PCP-003` after | 62/225 | **27.6** |
| `PCR-003` before | 144/423 | 34.0 |
| `PCR-003` after | 135/415 | **32.5** |

The report barely moved. **The plan got substantially worse**, from 18.4 % to 27.6 %, and it was
the document that had been *inside* the source band before. The band spans 14.8 to 26.1 across
the four sources, so `PCP-003` after is now outside all of them.

**The cause is measured, not guessed.** The construction counts in *The one that should not be
counted* show the plan removing 25 possessives and adding 23 copulas (`it is` 7 → 21,
`the <noun> is` 39 → 48). The possessive rule produced this regression. The report, which
removed possessives without substituting copulas, did not regress. So this is not evidence that
the copula rate is out of an author's reach — it is evidence that one rule in the guide has an
unnamed failure mode, and it is the cheapest of the three failures to fix.

**Adjunct front field** (any non-punctuation token before the subject phrase).

| | front / n | % |
|---|---|---|
| PDA TR 60 | 114/420 | 27.1 |
| A-Mab | 138/412 | 33.5 |
| ISPE TT | 151/424 | 35.6 |
| ISPE PV | 153/422 | 36.3 |
| `PCP-003` before | 24/201 | 11.9 |
| `PCP-003` after | 23/225 | **10.2** |
| `PCR-003` before | 62/423 | 14.7 |
| `PCR-003` after | 38/415 | **9.2** |

Down in both, and `PCR-003` fell by more than a third, from 14.7 % to 9.2 % against a source
floor of 27.1 %. Shape 4 of §2d is exactly this rule, with three source examples and a worked
correction, and the corpus moved away from it. The likely reason is visible in the worked
correction itself: it teaches the author to *delete* a bad front field ("First, Second, Third,
Fourth") and does not teach them to write a good one. Deleting is the easier half and it is the
half that got done.

### The register gate's own numbers

TASK-002 raised `mean_len` to 30.5, `pct_over_40` to 21.5 and `pct_over_55` to 9.5 to
accommodate ISPE PV, whose extraction fuses list items into pseudo-sentences. The question this
run had to answer is whether either re-authored document drifted into that new headroom.

| | mean_len | median_len | pct_over_40 | pct_over_55 | pct_under_15 |
|---|---|---|---|---|---|
| **band** | 20.0–30.5 | 18.0–26.5 | 3.0–21.5 | ≤9.5 | 15.0–32.0 |
| PDA TR 60 | 24.2 | 21.0 | 9.8 | 2.9 | 20.5 |
| A-Mab | 26.6 | 23.0 | 13.4 | 5.2 | 19.5 |
| ISPE TT | 28.0 | 24.0 | 14.8 | 5.8 | 16.3 |
| ISPE PV | 30.2 | 26.0 | 20.8 | 9.0 | 16.2 |
| `PCP-003` after | 24.3 | 24.0 | 6.6 | 0.4 | 20.4 |
| `PCR-003` after | 22.7 | 22.0 | 4.5 | 0.2 | 22.7 |

**Neither drifted.** Both sit at or below PDA TR 60, the tightest of the four sources, on every
length measure, and nowhere near the ISPE PV ceilings. The widened band did no harm here. If
anything both documents are now shorter-sentenced than three of the four sources, which is worth
watching: `pct_over_40` at 4.5 % is close to the 3.0 % floor, and the floor exists because the
earlier one-sided cap over-corrected into 17-word averages (`authoring/HANDOFF.md` §3a).

## The acceptance test: discrimination

The plan is explicit that the acceptance test is whether a reader can tell a re-authored passage
from a source passage, not whether a count moved. It was run three times, because the first two
rounds turned out to measure something other than the writing. Scoring in all three: **64 of 64
correct** (20/20, 24/24, 20/20).

**Round 1 — 20/20 (10 corpus, 10 A-Mab), and it means nothing.** 18 of the 20 passages carried a
decisive non-register tell. A-Mab passages carry PDF extraction damage — a sentence truncated
mid-clause, a bibliography line bleeding into the body — and typed measurements ("pH 5.0 ± 0.2",
"Figure 3.14"). Corpus passages carry the `Ref` stand-in that `prose_from_qmd` leaves where a
cross-reference was, and cannot contain a typed measurement at all, because §6 of the writing
guide forbids one. The test measured the extraction pipeline.

**Round 2 — 24/24 (12 and 12).** Passages with a sentence spaCy cannot parse as a clause were
dropped, and every digit run, figure reference and stand-in was masked on both sides. The calls
were then made on **subject matter and document identifiers**: the pilot covers one unit
operation and A-Mab's body covers ten, so any passage about anion exchange or virus filtration
is A-Mab by elimination, and any passage carrying `PCR-` or `SOP-` is corpus by elimination.

**Round 3 — 20/20 (10 and 10).** Both pools restricted to cell-culture subject matter, and every
document, procedure and product code masked to `[id]`. This is the only round that asks the
right question, and it still scores 20/20 — but the residual tells are real and I can name them:
`§` appears only in corpus prose and `e.g.` only in A-Mab; the well-formedness filter works per
sentence, so a table caption merged into a neighbouring sentence still leaks damage into three of
the ten A-Mab passages; and **I had read both re-authored documents earlier in the same session,
so I am not a blind reader.** Four of the ten corpus passages I recognised outright.

**So the counts do not support a conclusion, and the qualitative reading does.** Setting the
artifacts aside, the re-authored prose is recognisably closer to A-Mab in sentence shape. It now
opens paragraphs the way the sources do — "The four exceptions are informative.", "Two
expectations were held less firmly.", "Two operational risks remain." — with lexical main verbs
and concessive turns where there were none. What still separates the two, and it is not a defect
the epic named, is **regularity**: every corpus paragraph is a finished three-sentence argument,
while A-Mab is uneven. A-Mab drops a bare label mid-paragraph, repeats a sentence, leaves a claim
half-supported, and changes register between sections because different people wrote them. The
corpus reads as edited; A-Mab reads as written. That is now the strongest single tell, and no
threshold or shape catalogue addresses it.

**The test needs a reader who has not read the documents.** Nothing in this section should be
treated as a blind result.

## Why two moved and three did not

The obvious reading is lexical-versus-discourse, and the pilot refutes it. TASK-005 gave §2d
**three** worked corrections for the given-new rule (Corrections 1 to 3, from `PCR-004`,
`PCMR-001` and `PCP-004`) and §2d bis the possessive rule with its measured table. Adjacent
sections of the same guide, same author, same one-pass write. Possessives moved 5.72 → 0.36.
Chaining moved 31.0 → 34.4 and 35.1 → **30.7**. Both were taught the same way and only one
landed.

What separates them is that **an author can execute and self-verify a substitution and cannot
self-verify a rate.** Searching a draft for `its` and deciding each one is a finite, checkable
job. Knowing whether 37 % or 55 % of your sentences continue the previous topic is not available
to a writer without a parser. The connective repertoire is the confirming case: it is a
discourse property, not an ornament, and it moved — because `check_style.py` prints the distinct
count back to the author on every run.

So the lever is feedback at write time, not more examples in the guide. Three worked corrections
did not move chaining; a fourth will not either.

## Is this worth extending to the remaining eighteen?

**Not yet. Run one more two-document round first.**

Scored honestly, the amended artifacts produced **one clean win out of five** — the connective
repertoire. Possessives moved furthest and should not be counted, for the reasons above. Three
shapes did not move and two moved backwards. Committing eighteen documents on that evidence
would repeat the pilot's own mistake at nine times the cost: six tasks changed the guide, the
exemplar, the gate and the brief, and nobody knew what any of it did until a document was
written and measured.

The second round costs two documents and tests a real hypothesis rather than a hope: **does
giving the author the measurement change the outcome, when giving them examples did not?** Use
the same two documents — they are already split from the corpus, both genres stay covered, and a
third point is directly comparable to the two here.

What has to exist before it runs:

1. **`authoring/check_discourse.py`** — chaining, copula and front field with denominators and
   the four source columns, reusing `check_style.prose_from_qmd` / `sentences` /
   `HUMAN_SOURCES` so it measures the same text the gate does. **Advisory, never a gate**: a
   floor on chaining is met by typing a pronoun, which is the failure mode this epic already
   documented. It needs spaCy, which the proposal deliberately kept out of the dependency set,
   so whether that becomes an optional extra is a decision for the project owner.
2. **A discourse section in the brief** (§5d is free; the brief runs 5, 5c, 6). The targets
   matter less than the worked chains, which the brief can generate **from the document's own
   grounded facts** rather than quoting another document. This is pre-authoring, so it respects
   the rule that nothing is added to a document after authoring.
3. **§2d bis names the substitution and bounds the target** — the definite article or the noun,
   never `it is`, and a band rather than a minimum. This is the one fix the pilot has direct
   evidence for.
4. **Shape 4 gains a positive front-field example.** Cheap, worth doing, and not expected to
   carry load on its own.

The loop is measure, then **re-author in one pass** with the numbers in the brief. Never patch:
a second one-pass author is not post-editing, it is what TASK-007 already did.

**Stopping rule, fixed in advance**, because otherwise this iterates forever:

- **Extend to the eighteen** if chaining clears roughly 45 % in *both* genres and neither copula
  nor front field regresses.
- **Stop and change the target** if it does not. That would mean the discourse hypothesis is not
  reachable by authoring instructions, and the better use of the next epic is the tell found
  qualitatively below, which no measure here covers: the corpus reads as *edited* and A-Mab
  reads as *written*.

**The two-document pilot earned its keep**, and this is the argument for keeping the second
round at two as well. Every regression except the front field is worse in one genre than the
other, and both of the worst (copula 18.4 → 27.6, `it` 7.42 → 12.02) are in the **plan**, which
was inside the source band on both before. A `PCR-003`-only pilot would have reported "no
change" on copula and missed the regression entirely.

## What was found on the way

- **A large ratio on a rare feature is not a perceptible defect, and this page led with one.**
  `its` at fourteen times the source rate is 69 instances in 10,354 words — one every 6.3
  sentences. The measure was picked by ranking word frequencies, which is exactly the method
  that finds ratio artefacts, and no reader was asked until after the campaign had been
  recommended. **Ask a reader before promoting a metric to a finding.** The check is cheap: the
  one reading taken during this epic overturned the headline result in a sentence.
- **A rule that says what to remove and not what to write instead will be paid for somewhere.**
  §2d bis names three pronouns and forbids them. One of the two authors bought the possessives
  back as expletive subjects — `it is` 7 → 21 in `PCP-003` — which is a copula, which is another
  measure on the same page. The cost landed in a different metric from the one the rule
  governed, so nothing connected them until the constructions were counted directly.
- **`check_render.py --render` checks PDF glyphs against whatever `.pdf` is already on disk, and
  only ever renders the `.docx` itself.** On a document whose PDF is stale it reports "no missing
  glyphs" about the *old* file. Both PDFs here were rendered separately with
  `quarto render --to pdf` and re-checked. This is a real hole in the verification checklist.
- **A curated span layer that no longer matches its document stops the whole build, by design,
  and that hides the state of every other annex.** `build_rhetorical_spans` raises `SystemExit`
  when a span goes missing, so the first rebuild after the re-authoring wrote *nothing* —
  including `PCP-003.json`, whose own quotes had already been fixed. A grounding count taken
  between those two states measures the stale files on disk, not the build. The design is right;
  the trap is reading the count in between.
- **The re-authored `PCR-003` never states the commercial scale.** "15,000" does not occur
  anywhere in the rendered report, where the previous revision gave it in §1.1. The `Equipment`
  entity is still named "15,000 L production bioreactor" from the config. `PCP-003` still states
  it, so the figure is not lost from the pair, but the brief does not require a report to state
  the scale it is characterizing and probably should.
- **80 annex spans had to be re-anchored** — 24 of `PCP-003`'s 105 quotes and 56 of `PCR-003`'s
  177, of which 34 were the curated rhetorical layer. The total is unchanged at 2084 because the
  re-anchoring replaced spans one for one. Budget roughly 40 spans per re-authored document for
  the remaining eighteen.
- **Three of the five topic-chaining "before" values quoted in the implementation plan do not
  reproduce.** The plan recorded `PCP-003` at 30.0 % and `PCR-003` at 37.2 %; measured here under
  one run with a single method they are 31.0 % and 35.1 %. Before and after on this page are
  measured the same way in the same run, so the deltas hold; the plan's figures should not be
  quoted against them.

## Verification

```bash
# the measurements, re-executed end to end (section 13 of the notebook)
uv run --with spacy \
  --with 'https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl' \
  --with jupyter jupyter nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.timeout=1800 \
  authoring/register_analysis.ipynb

# the construction counts behind "The one that should not be counted" (no spaCy needed)
uv run python - <<'EOF'
import re, sys; sys.path.insert(0, "authoring")
from check_style import prose_from_qmd
W = ".claude/work/2026-08-16_01_register-from-four-sources/pre-rewrite"
PATS = [("its", r"\bits\b"),
        ("it is/was", r"\bit (is|was|will be)\b"),
        ("the <noun> is", r"\bthe \w+(?: \w+)? (is|are|was|were)\b")]
for doc in ("PCP-003", "PCR-003"):
    for label, path in (("before", f"{W}/{doc}_bioreactor.qmd"),
                        ("after",  f"pc_package/{doc}_bioreactor.qmd")):
        t = prose_from_qmd(path)
        cells = "   ".join("%s %3d" % (k, len(re.findall(p, t, re.I))) for k, p in PATS)
        print("%-8s %-7s %s" % (doc, label, cells))
EOF

# the corpus is green at the same commit
make test PY="uv run python"                       # 85 passed
make style PY="uv run python"                      # 20/20 documents ok, exit 0
cd pc_package && uv run python build_ground_truth.py \
  && uv run python validate_annex.py               # 20/20 annexes valid
cd pc_package && GROUNDING_STRICT_ANCHORS=1 uv run python check_grounding.py
                                                   # 2084/2084 quotes grounded, 0 weak anchors
git diff outputs/                                  # empty: no dataset moved
```

Rendered: `PCP-003` 30 pp, `PCR-003` 51 pp, 0 missing glyphs in either
(`fitz`, counting `\x00`, the same test `check_render.check_pdf_glyphs` applies).

## Files

| File | What happened |
|---|---|
| `pc_package/PCP-003_bioreactor.qmd`, `.docx`, `.pdf` | re-authored, promoted from DRAFT, re-rendered |
| `pc_package/PCR-003_bioreactor.qmd`, `.docx`, `.pdf` | re-authored, promoted from DRAFT, re-rendered |
| `pc_package/build_ground_truth.py` | bioreactor entity, study, assertion and report-section quotes re-anchored |
| `pc_package/ground_truth/PCP-003.json`, `PCR-003.json` | rebuilt |
| `authoring/rhetorical/PCR-003.spans.yaml` | all 35 spans re-curated |
| `authoring/discrepancies.yaml`, `authoring/DISCREPANCIES.md` | D-001 and D-002 registered sentences re-verified against the new text |
| `authoring/WRITING_GUIDE.md` | four worked corrections relabelled as pre-2026-08-17 prose |
| `authoring/register_analysis.ipynb` | section 13 added (the pilot, measured); moved here from the work unit so it sits beside the guide it explains |
| `.claude/work/…/pre-rewrite/` | the two documents as they stood at `b0361f1`, read by §13. Work-unit directories persist after delivery; if one is ever cleared, restore with `git show b0361f1:pc_package/<doc>_bioreactor.qmd` |
