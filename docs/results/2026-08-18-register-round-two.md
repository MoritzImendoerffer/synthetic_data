# The second round: the author was told the number

**Run date:** 2026-08-18. **Work unit:** `2026-08-17_01_register-second-round`, TASK-001 to
TASK-008. **Documents:** `PCP-003` (plan) and `PCR-003` (report), the production bioreactor pair,
for the third time.

**Three points, one method.** Round zero is the text at `b0361f1`, kept at
`.claude/work/2026-08-16_01_register-from-four-sources/pre-rewrite/`. Round one is the text at
`f06f1a7`, kept at `.claude/work/2026-08-17_01_register-second-round/pre-rewrite/`. Round two is
`pc_package/`. All three were measured in **one invocation each** of `check_style.py --compare`
and `check_discourse.py`, because the pilot page's "before" chaining values did not reproduce when
two runs measured differently.

**Verdict in one line: every line of the stopping rule holds, so Track 2 opens.** The line that
decided it is the one the round was built on — mid-sentence `, so ` fell from 10.6 % and 8.0 % of
sentences to **0.0 % in both documents**, while sentence-initial connectives rose from 1.8 % and
0.9 % to **4.9 % and 4.0 %**, inside the 3.7–6.1 % source band.

> **One acceptance line of this page is still open.** The human check for this round is the
> project owner reading the re-authored pair (owner decision, 2026-08-17). That reading is not
> recorded yet; the section below says so and states what is being asked. The numbers do not
> depend on it, and the stopping rule is a rule about numbers — but the owner's reading is what
> decides whether the *target* was the right one, which is a different question.

## Why the run happened

The pilot returned one clean win in five. The project owner then read the re-authored `PCR-003`
and named a defect none of the five measures covered: argument steps packed into one sentence with
`, so … , and …`, and a sentence that counts "the four that matter" without naming them. The count
confirmed the reading — mid-sentence `, so ` ran at 20 to 30 times the source rate — and the
pilot's own re-authoring had made it **worse** in both documents.

The pilot's explanation for why two shapes moved and three did not was that an author can execute
and self-verify a substitution and cannot self-verify a rate. This round tests that directly. The
rule was restated in `WRITING_GUIDE.md` §2d as a substitution with the strings to search for; the
counts were added to `check_style.py` as an advisory line printed on every run; and brief §5d gave
each author **its own document's round-one number** beside the four source columns. Nothing else
about the authoring loop changed.

## What changed — the two packing measures

From `check_style.py --compare`, six document columns. Every rate is over sentences of prose; the
denominators are the last row.

| measure | PDA TR 60 | A-Mab | ISPE TT | ISPE PV | PCP-003 r0 | r1 | **r2** | PCR-003 r0 | r1 | **r2** |
|---|---|---|---|---|---|---|---|---|---|---|
| mid-sentence `, so ` % | 0.1 | 0.3 | 0.4 | 0.4 | 7.9 | 10.6 | **0.0** | 6.5 | 8.0 | **0.0** |
| opens with a connective % | 4.8 | 6.1 | 4.2 | 3.7 | 0.0 | 1.8 | **4.9** | 2.1 | 0.9 | **4.0** |
| 2+ clause coordinators % | 2.3 | 1.2 | 1.5 | 3.1 | 6.4 | 9.3 | **3.0** | 8.8 | 5.4 | **1.7** |
| (sentences of prose) | 820 | 1041 | 669 | 808 | 202 | 226 | 203 | 433 | 423 | 421 |

Both documents cleared both targets, and the coordinator family came with them rather than
absorbing the traffic. That last row is the one that would have exposed a cheat: a ceiling on
`, so ` is met by writing `, and`, and the coordinator count fell instead of rising.

**The overshoot is real and should be recorded as such.** 0.0 % is below *every* source. The
sources write the construction about once in 250 to 1000 sentences; both documents now write it
never. That is the possessive result repeating in a new place — a rule stated as a substitution is
executed to exhaustion — and it is the first thing to watch when the eighteen are re-authored. It
did not cost anything measurable here, which is why it is a note and not a regression.

## The connective repertoire

| measure | PDA TR 60 | A-Mab | ISPE TT | ISPE PV | PCP-003 r0 | r1 | **r2** | PCR-003 r0 | r1 | **r2** |
|---|---|---|---|---|---|---|---|---|---|---|
| connectives per 1k words | 2.7 | 2.7 | 2.2 | 2.6 | 1.3 | 3.5 | **2.9** | 3.7 | 3.5 | **3.2** |
| of the nine, how many used | 9 | 7 | 7 | 6 | 3 | 6 | **7** | 3 | 6 | **9** |

`PCR-003` uses **all nine**, which no document in this corpus has done. The rate fell slightly in
both documents while the spread widened, which is the shape you want: fewer repetitions of
"therefore", more of the connectives that carry a specific relation.

## Topic chaining, copula, front field

From `check_discourse.py`, **uncapped** — every sentence measured. Both corpus documents sit under
the notebook's caps, so their figures are identical either way; only the source columns move.[^cap]

| measure | PDA TR 60 | A-Mab | ISPE TT | ISPE PV | PCP-003 r0 | r1 | **r2** | PCR-003 r0 | r1 | **r2** |
|---|---|---|---|---|---|---|---|---|---|---|
| topic chaining % | 60.5 | 56.1 | 61.9 | 57.3 | 31.0 | 34.4 | **46.0** | 35.1 | 30.7 | **46.1** |
| chained/pairs | 465/769 | 539/960 | 388/627 | 435/759 | 62/200 | 77/224 | 92/200 | 148/422 | 127/414 | 190/412 |
| copula main verb % | 20.1 | 13.5 | 22.8 | 26.3 | 18.4 | 27.6 | **21.9** | 34.0 | 32.5 | **25.7** |
| copula/n | 155/770 | 130/961 | 143/628 | 200/760 | 37/201 | 62/225 | 44/201 | 144/423 | 135/415 | 106/413 |
| adjunct front field % | 28.4 | 32.9 | 34.2 | 37.1 | 11.9 | 10.2 | **22.4** | 14.7 | 9.2 | **17.4** |
| front/n | 219/770 | 316/961 | 215/628 | 282/760 | 24/201 | 23/225 | 45/201 | 62/423 | 38/415 | 72/413 |

**Chaining was not asked for, and it moved anyway.** No instruction in this round mentioned topic
chaining; the proposal's 45 % bar was explicitly dropped as a target. Two agents that never saw
each other's draft landed at 46.0 % and 46.1 %, from 34.4 % and 30.7 %. That is the strongest
result on the page, because it is the one nobody could have gamed: the number was printed in the
brief as context and never set as a goal.

The mechanism is visible in the front-field row. One argument step per sentence, with the next
step opening on its connective, *is* a front field — so the substitution that fixed packing also
doubled the adjunct front field and gave each sentence a subject that refers back to the previous
one. One rule moved three measures. Both documents are still well short of the sources on chaining
(56–62 %) and on front field (28–37 %).

**Copula came back inside the band.** Round one's plan traded 25 possessives for 23 expletive
subjects and left the copula rate at 27.6 %, outside all four sources. `WRITING_GUIDE.md` §2d bis
now names the substitution as the definite article or the noun and forbids `it is`, and the plan is
at 21.9 %, inside the 13.5–26.3 % band. The report fell from 32.5 % to 25.7 % on the same rule.

[^cap]: With `--cap` (the notebook's 600/450 sentence caps, which the pilot page used) the source
columns read: chaining 59.4 / 59.0 / 61.9 / 57.0, copula 17.6 / 14.8 / 22.4 / 26.1, front field
27.1 / 33.5 / 35.6 / 36.3. The six document columns are unchanged. Quote the uncapped table unless
you are comparing directly with the pilot page.

## Possessives and what the substitution cost

Per 1000 words of prose, counts in brackets.

| | its | their | it is/was | the \<noun\> is |
|---|---|---|---|---|
| PDA TR 60 | 0.40 (8) | 0.96 (19) | 1.11 (22) | 3.83 (76) |
| A-Mab | 0.32 (9) | 0.50 (14) | 1.00 (28) | 6.00 (168) |
| ISPE TT | 0.27 (6) | 0.63 (14) | 1.85 (41) | 3.42 (76) |
| ISPE PV | 0.36 (9) | 0.69 (17) | 2.02 (50) | 5.58 (138) |
| PCP-003 round zero | 5.72 (27) | 3.18 (15) | 1.48 (7) | 8.26 (39) |
| PCP-003 round one | 0.36 (2) | 0.18 (1) | **3.82 (21)** | 8.74 (48) |
| **PCP-003 round two** | **0.00 (0)** | **0.00 (0)** | **0.84 (4)** | 9.62 (46) |
| PCR-003 round zero | 6.66 (69) | 4.15 (43) | 5.12 (53) | 10.14 (105) |
| PCR-003 round one | 0.31 (3) | 0.83 (8) | 2.28 (22) | 10.69 (103) |
| **PCR-003 round two** | **0.51 (5)** | **0.81 (8)** | **0.41 (4)** | 9.67 (95) |

The bill round one ran up is paid. `it is/was` in the plan went 7 → 21 → 4, which is below every
source. The report sits at 0.51 and 0.81 for *its* and *their*, inside the source bands the guide
now states (0.27–0.40 and 0.50–0.96) — the first time either document has landed inside them
rather than above or below.

**The plan overshot in the other direction: zero possessives in 4,783 words.** The guide asks for a
band and says a document at 0.02 has driven out the licensed exception too. `PCP-003` is at 0.00.
Nothing in the register gate catches that, and it is the second thing to watch in Track 2.

`the <noun> is` did not move in either document and sits above every source. No instruction in this
round addressed it.

## The register gate's own numbers

All twelve gated rows pass for both documents (TASK-007 re-ran `make style`: 24 OK lines, 0 FAIL).
The two that the round put under pressure:

| measure | band | PDA | A-Mab | ISPE TT | ISPE PV | PCP-003 r0 | r1 | **r2** | PCR-003 r0 | r1 | **r2** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sentences under 15 words % | 15.0–32.0 | 20.5 | 19.5 | 16.3 | 16.2 | 18.3 | 20.4 | **23.6** | 22.4 | 22.7 | **19.5** |
| sentences over 40 words % | 3.0–21.5 | 9.8 | 13.4 | 14.8 | 20.8 | 7.9 | 6.6 | **7.4** | 5.8 | 4.5 | **5.9** |

The headroom question is answered: **splitting sentences did not push either document out of the
band, and the cost was smaller than the plan expected.** The plan predicted 5 to 8 points of
`pct_under_15` for splitting one sentence in ten. `PCP-003` paid 3.2 points against a 32.0 ceiling.
`PCR-003` paid nothing — it went *down* 3.2 points, because splitting a packed sentence into two
20-word sentences moves mass out of the long tail without creating short ones. Both documents also
moved *up* on `pct_over_40`, away from the 3.0 floor they were near.

## The stopping rule, line by line

Fixed in `decisions.stopping_rule_edges` before the round ran, and not moved after the numbers
were seen.

| condition | edge | PCP-003 | PCR-003 | holds? |
|---|---|---|---|---|
| mid-sentence `, so ` | ≤ 1.0 % of sentences | 0.0 | 0.0 | **yes** |
| opens with a connective | ≥ 3.0 % of sentences | 4.9 | 4.0 | **yes** |
| topic chaining | not more than 2.0 pt below round one (≥ 32.4 / ≥ 28.7) | 46.0 | 46.1 | **yes** |
| copula | not more than 2.0 pt above round one (≤ 29.6 / ≤ 34.5) | 21.9 | 25.7 | **yes** |
| register gate | `check_style.py` passes both | OK | OK | **yes** |

No line is within 0.5 points of its edge, so nothing here is a judgement call. Front field was
reported and not gated, as the rule says.

**The proposal's original rule also holds, and it was not applied.** Before the owner replaced it,
`docs/next/register-from-four-sources.md` said "go to Track 2 if chaining clears roughly 45 % in
*both* genres and neither copula nor front field regresses". Chaining is at 46.0 % and 46.1 %,
copula fell in both documents and front field roughly doubled in both. The rule that was dropped
for being unreachable by authoring instructions is cleared by the round that stopped aiming at it.

**Verdict: Track 2 opens.**

## The owner's reading

**Not recorded yet.** The human check for this round, fixed by owner decision on 2026-08-17, is
the project owner reading the two re-authored PDFs (`pc_package/PCP-003_bioreactor.pdf`, 29 pp;
`pc_package/PCR-003_bioreactor.pdf`, 59 pp) and answering two questions:

1. Is the pair still *immediately* recognisable as machine-written?
2. If so, which sentences give it away?

**The reading is not blind, and that was accepted in advance.** The owner has now read both
documents twice, so no discrimination test involving them can be valid. The pilot recorded why the
blind test was dropped: three rounds scored 64 of 64 and every one was decided by something other
than register. The reading is worth more than the test precisely because it is not blind — the
owner is looking for what is wrong, not guessing which of two texts is generated.

Whatever the owner quotes becomes the next unit's target, the way the two sentences quoted on
2026-08-17 became this one's. If the reading says the pair is still obviously machine-written
*after* both stated targets were cleared, that is evidence about the measures rather than about
the documents, and decision D1 should be settled with it in hand.

## The hypothesis, answered

The pilot's claim was: **an author can execute and self-verify a substitution and cannot
self-verify a rate — so give the author the rate and it will move.** Per document, per measure:

| measure | told the number? | PCP-003 | PCR-003 |
|---|---|---|---|
| mid-sentence `, so ` | yes, in brief §5d and on every render | moved, 10.6 → 0.0 | moved, 8.0 → 0.0 |
| opens with a connective | yes, same | moved, 1.8 → 4.9 | moved, 0.9 → 4.0 |
| copula | yes, §5d, with the substitution named | moved, 27.6 → 21.9 | moved, 32.5 → 25.7 |
| topic chaining | printed as context, never set as a goal | moved, 34.4 → 46.0 | moved, 30.7 → 46.1 |
| front field | printed as context, never set as a goal | moved, 10.2 → 22.4 | moved, 9.2 → 17.4 |

Five for five in both genres, against one for five in the pilot. **The hypothesis survives, but
this round cannot separate its two halves.** Round two changed three things at once: the rule
became a substitution, the count was printed back on every render, and the brief carried the
document's own figure. Round one had already shown that a substitution *without* a number moves
(possessives, 6.66 → 0.31) and that examples without a substitution do not (chaining, copula,
front field). What round two adds is that the combination moves measures **nobody asked for** —
chaining and front field were context, not targets, and both moved further than any pilot measure
did. The cleanest reading is that one well-stated substitution reorganised the sentence and the
other measures followed the reorganisation, not the instruction.

## What was found on the way

- **The two findings the pilot left open are both closed.** The round-one `PCR-003` never stated
  the commercial scale it characterizes (`grep -c "15,000\|15 000"` = 0). Round two states it three
  times, through `V["commercial_scale_l"]`, first in the executive summary. The `acidic variants
  is` agreement fault — an inline expression yielding a response name used as the subject of a verb
  that must agree with it — occurs once in round one and zero times in round two, in either
  document.
- **The report is eight pages longer** (59 pp against 51) on flat prose: 9,822 words against 9,614,
  421 sentences against 423, and the same nine figures. The growth is table and appendix layout.
  `CLAUDE.md` records DoE reports as running 41–55 pp "as built", which is now false at the top
  end; that line needs re-checking rather than defending.
- **Two annex extractors disagree on superscripts.** `build_rhetorical_annex.doc_text` reads
  `word/document.xml` and yields `R²`; `check_grounding.docx_text` yields `R2`. A curated span
  containing that character grounds in one and fails in the other. Test every span against both
  before running the builder.
- **Re-anchoring cost less than the pilot budgeted.** 44 quote instances moved across the pair
  (21 + 23) from 37 edited strings, against 80 in round one. Every table-row quote survived
  untouched, because the row builders rebuild the row from the DataFrame the document renders. The
  proposal's Track 2 budget of ~40 spans per document is therefore an overestimate for documents
  without a curated rhetorical layer; 33 of the 35 curated `PCR-003` spans needed a new quote.

## Verification

```bash
R0=.claude/work/2026-08-16_01_register-from-four-sources/pre-rewrite
R1=.claude/work/2026-08-17_01_register-second-round/pre-rewrite
W=.claude/work/2026-08-17_01_register-second-round

uv run python authoring/check_style.py --compare \
   $R0/PCP-003_bioreactor.qmd $R1/PCP-003_bioreactor.qmd pc_package/PCP-003_bioreactor.qmd \
   $R0/PCR-003_bioreactor.qmd $R1/PCR-003_bioreactor.qmd pc_package/PCR-003_bioreactor.qmd \
   > $W/measure_style.txt

uv run --extra discourse python authoring/check_discourse.py <same six> > $W/measure_discourse.txt
uv run --extra discourse python authoring/check_discourse.py --cap <same six> \
   > $W/measure_discourse_cap.txt
```

Possessives and constructions (`$W/measure_possessive.txt`):

```bash
uv run python - <<'EOF'
import re, sys, os
sys.path.insert(0, "authoring")
from check_style import prose_from_qmd, prose_from_extract, HUMAN_SOURCES
PATS = [("its", r"\bits\b"), ("their", r"\btheir\b"),
        ("it is/was", r"\bit (is|was|will be)\b"),
        ("the <noun> is", r"\bthe \w+(?: \w+)? (is|are|was|were)\b")]
# ...one row per source and per revision, rate per 1000 words with the count
EOF
```

**These two scripts are the method for these measures.** `authoring/register_analysis.ipynb` §13
is superseded for clause packing, chaining, copula and front field: it applied 600/450 sentence
caps that the scripts make optional, and it is not re-executed here. The notebook remains the
method for the analyses the scripts do not cover.

The corpus state behind these numbers (TASK-007): 2084/2084 quotes grounded across 20 annexes with
`GROUNDING_STRICT_ANCHORS=1` and no weak anchors, 20/20 annexes valid, `weak_claims` empty in both,
`git diff outputs/` empty, `make test` 88 passed, `make style` 24 OK and 0 FAIL, both PDFs rendered
fresh with no missing glyphs.

## Files

| File | What it carries |
|---|---|
| `authoring/check_style.py` | the three advisory packing measures, printed and gated by nothing |
| `authoring/check_discourse.py` | chaining, copula, front field, behind the optional `discourse` extra |
| `authoring/WRITING_GUIDE.md` | §2d as a substitution, the referent rule, §2d bis's named substitution and band, Shape 4's positive correction |
| `authoring/REGISTER_EXEMPLAR.md` | "The step after the full stop", four verbatim pairs from three sources |
| `authoring/build_brief.py` | §5d, which prints the targets and the document's own numbers |
| `pc_package/PCP-003_bioreactor.qmd`, `PCR-003_bioreactor.qmd` | re-authored in one pass each |
| `authoring/rhetorical/PCR-003.spans.yaml` | 35 spans re-curated, none dropped |
| `.claude/work/2026-08-17_01_register-second-round/measure_*.txt` | the raw output every number here comes from |
