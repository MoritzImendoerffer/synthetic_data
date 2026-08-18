# The third round: the measures the reader's eye had already made

**Run date:** 2026-08-18. **Work unit:** `.claude/work/2026-08-18_01_register-third-round`.
**Document:** `PCR-003` (Production Bioreactor process characterization report) **only**.
**Control:** `PCP-003` at round two, not re-authored.
**Proposal:** `docs/next/register-from-four-sources.md`, Track A (three measures) + Track B
(write the passive).
**Page this one is written against:** [`2026-08-18-register-round-two.md`](2026-08-18-register-round-two.md).

| point | file | commit |
|---|---|---|
| round zero | `.claude/work/2026-08-16_01_register-from-four-sources/pre-rewrite/PCR-003_bioreactor.qmd` | `b0361f1` |
| round one | `.claude/work/2026-08-17_01_register-second-round/pre-rewrite/PCR-003_bioreactor.qmd` | `f06f1a7` |
| round two | `.claude/work/2026-08-18_01_register-third-round/pre-rewrite/PCR-003_bioreactor.qmd` | `e7a4768` |
| round three | `pc_package/PCR-003_bioreactor.qmd` | this unit |
| control | `pc_package/PCP-003_bioreactor.qmd` (round two, untouched) | `e7a4768` |

All four were verified byte-identical to their commits with `git show <commit>:… | diff -q -`
before anything was measured.

**Verdict: every line of the stopping rule holds, and the line that decided it is the passive —
35.4 % to 57.4 %, from twenty points below every source to inside their range, on a rule that was
never given as a count.** One genre only, so the honest phrasing is: *it moved in the report.*

## Why the run happened

Round two cleared every target it set. The project owner then read the pair and recognised it as
machine-written on the first sentence, and named three faults that no measure in the repository
counted: the balanced `, and ` second clause, the `, not ` contrastive tail, and the missing
passive. Counted afterwards, all three were real and large. This round did the one thing round two
had shown to work — print the number back to the author — for exactly those three.

## What round two's reading named, four points

Every cell below is from `measure_style.txt` (regex measures) or `measure_discourse.txt` (parser
measures), one invocation each over all five files.

| measure | PDA TR 60 | A-Mab | ISPE TT | ISPE PV | r0 | r1 | r2 | **r3** | PCP-003 r2 |
|---|---|---|---|---|---|---|---|---|---|
| `, and ` + second clause, **regex** (% of sentences) | 3.4 | 1.1 | 1.3 | 3.1 | 24.9 | 21.0 | 22.6 | **0.5** | 18.2 |
| `, and ` + second clause, **parser** (% of n) | 3.4 (26/770) | 1.4 (13/961) | 1.0 (6/628) | 3.0 (23/760) | 29.6 (125/423) | 25.8 (107/415) | 25.4 (105/413) | **0.7 (3/430)** | 24.9 (50/201) |
| mid-sentence `, not ` (% of sentences) | 0.2 | 0.0 | 0.1 | 0.0 | 0.0 | 0.0 | 4.3 | **0.0** | 0.0 |
| passive construction (% of n) | 56.9 (438/770) | 64.0 (615/961) | 62.9 (395/628) | 60.1 (457/760) | 44.9 (190/423) | 42.4 (176/415) | 35.4 (146/413) | **57.4 (247/430)** | 55.2 (111/201) |

`n` is the sentences that have a root and a subject, which is a few fewer than the sentence count.
On the all-sentences denominator the same passive counts read 43.9 → 41.6 → 34.7 → **56.5 %**, and
the sources 53.4 / 59.1 / 59.0 / 56.6 %; the shape of the series is the same either way.

The round-two page reported the passive as 34.4 %, from a heredoc that was never saved to a file.
`check_discourse.py` counts 146 passive sentences where that heredoc counted 145, and divides by
the root-and-subject denominator rather than by all sentences. Both differences were measured and
written down by `/plan` before this round ran (`state.json` → `decisions.one_denominator`), so the
0.7-point step between the two pages is a change of method, not a change in the text.

## The five measures round two moved, held

| measure | sources | r0 | r1 | r2 | **r3** | PCP-003 r2 |
|---|---|---|---|---|---|---|
| mid-sentence `, so ` (%) | 0.1–0.4 | 6.5 | 8.0 | 0.0 | **0.0** | 0.0 |
| opens with a connective (%) | 3.7–6.1 | 2.1 | 0.9 | 4.0 | **3.7** | 4.9 |
| 2+ clause coordinators (%) | 1.2–3.1 | 8.8 | 5.4 | 1.7 | **1.8** | 3.0 |
| topic chaining (%) | 56.1–61.9 | 35.1 (148/422) | 30.7 (127/414) | 46.1 (190/412) | **47.6 (204/429)** | 46.0 (92/200) |
| copula main verb (%) | 13.5–26.3 | 34.0 (144/423) | 32.5 (135/415) | 25.7 (106/413) | **16.5 (71/430)** | 21.9 (44/201) |

Nothing regressed. Copula fell 9.2 points without being targeted at all this round, from the top of
the source band to near its floor.

## Adjunct front field, and the repertoire

| measure | sources | r0 | r1 | r2 | **r3** | PCP-003 r2 |
|---|---|---|---|---|---|---|
| adjunct front field (%) | 28.4–37.1 | 14.7 (62/423) | 9.2 (38/415) | 17.4 (72/413) | **30.2 (130/430)** | 22.4 (45/201) |
| connectives per 1k words | 2.2–2.7 | 3.7 | 3.5 | 3.2 | **2.4** | 2.9 |
| of the nine, how many used | 6–9 | 3 | 6 | 9 | **8** | 7 |

Front field is the second unasked-for move of the round: from below every source at round two to
inside their range, +12.8 points. The connective rate fell to 2.4 per 1k, which is inside the
source range for the first time in the series, at the cost of one of the nine connectives.

## Possessives and constructions

From `measure_possessive.txt`, rate per 1000 words with the count.

| | `its` | `their` | `it is/was` | `the <noun> is` |
|---|---|---|---|---|
| PDA TR 60 | 0.40 (8) | 0.96 (19) | 1.11 (22) | 3.83 (76) |
| A-Mab case study | 0.32 (9) | 0.50 (14) | 1.00 (28) | 6.00 (168) |
| ISPE TT | 0.27 (6) | 0.63 (14) | 1.85 (41) | 3.42 (76) |
| ISPE PV | 0.36 (9) | 0.69 (17) | 2.02 (50) | 5.58 (138) |
| PCR-003 r0 | 6.66 (69) | 4.15 (43) | 5.12 (53) | 10.14 (105) |
| PCR-003 r1 | 0.31 (3) | 0.83 (8) | 2.28 (22) | 10.69 (103) |
| PCR-003 r2 | 0.51 (5) | 0.81 (8) | 0.41 (4) | 9.67 (95) |
| **PCR-003 r3** | **1.66 (16)** | **1.04 (10)** | **0.73 (7)** | **9.85 (95)** |
| PCP-003 r2 | 0.00 (0) | 0.00 (0) | 0.84 (4) | 9.62 (46) |

`its` rose to 1.66 per 1k, which is four times the highest source. Round one's lesson was a rule
executed to exhaustion in one direction; this is the same rule drifting back the other way once it
stopped being the thing the author was told to watch. It is not gated and it is not in the stopping
rule, and it should be printed to the author in round four rather than argued about here.

## The register gate's own numbers

| measure | band | r0 | r1 | r2 | **r3** | PCP-003 r2 |
|---|---|---|---|---|---|---|
| mean sentence length | 20.0–30.5 | 23.9 | 22.7 | 23.3 | **22.1** | 23.6 |
| median sentence length | 18.0–26.5 | 24.0 | 22.0 | 22.0 | **21.0** | 23.0 |
| % over 40 words | 3.0–21.5 | 5.8 | 4.5 | 5.9 | **6.9** | 7.4 |
| % over 55 words | ≤ 9.5 | 0.0 | 0.2 | 0.2 | **0.0** | 0.0 |
| % under 15 words | 15.0–32.0 | 22.4 | 22.7 | 19.5 | **26.1** | 23.6 |

The gate passed on all twelve rows at round three: `OK register is within the human-source
envelope`.

## The overshoot check, which the plan predicted in writing

Exploration §3 predicted, before the document was written, that a rule stated as a substitution is
executed to exhaustion, and that `, and ` + clause would land near zero, below the sources' band.
It did.

- **`, and ` + clause is an overshoot.** 0.5 % by regex against sources at 1.1–3.4, and 0.7 % (3 of
  430) by parser against sources at 1.0–3.4. Below all four on both halves of the pair. This is the
  third overshoot in three rounds: `, so ` went to 0.0 % in round two, `PCP-003` went to zero
  possessives in round one, and now this.
- **`, not ` is at the floor, not below it.** 0.0 %, which two of the four sources also are. Nothing
  to report beyond the collapse from 4.3 %.
- **The passive is inside the band, not above it.** 57.4 % against sources at 56.9–64.0 on the same
  denominator. It sits 0.5 points above the lowest source, so the band's lower edge is where it
  landed, and a fourth round should not push it further.

**What paid for the `, and ` collapse.** Two things, both counted (`measure_whatpaid.txt`):

| | sources | r0 | r1 | r2 | **r3** |
|---|---|---|---|---|---|
| `, which` (% of sentences) | 0.60–2.35 | 8.31 | 8.98 | 9.50 | **15.33** |
| semicolons (% of sentences) | 2.85–5.08 | 1.39 | 0.47 | 0.95 | **1.37** |
| `% under 15 words` | 15.0–32.0 | 22.4 | 22.7 | 19.5 | **26.1** |

Semicolons did not pay for it — they stayed near zero, nowhere near the 4.5 per 1k ceiling that was
being watched. Two other things did. Sentences were split, which cost 6.6 points of `pct_under_15`
against a 32.0 ceiling, exactly as the plan warned the author. And coordination became
**subordination**: `, which` rose 5.8 points to 15.33 % of sentences, against sources that run
0.60–2.35 %. The clause the author was told to stop coordinating did not disappear; a good part of
it was re-attached with a relative pronoun instead. That measure was already six times the sources
before this round and is now more than six times the highest of them. **It is the strongest
candidate for round four's target**, and it was found by measuring what paid rather than by reading.

## The three "screening retained" sentences

Gone. `grep -c 'screening retained\|screening identified\|the design carries\|the model
identifies\|the study selected'` returns **0** on the round-three document, against 3 hits of
`screening retained` alone at round two. Each was replaced in place by the passive participle the
guide's worked correction gives, and each stayed in its own section:

| section | round two | round three |
|---|---|---|
| Executive summary | "The `n_rsm_f` factors that screening retained then entered a face centred response surface design of `n_rsm` runs, and the remaining `n_uv` parameters were assessed one at a time." | "The `n_rsm_f` factors retained from screening were then studied in a face centred central composite design of `n_rsm` runs, which supports a full quadratic model over three levels of every factor it carries." |
| Response-surface design | "The response surface design is a face centred central composite design in the `n_rsm_f` factors screening retained, augmented with `cp_rsm` centre points, for `n_rsm` runs." | "At the second stage, a face centred central composite layout was used in the `n_rsm_f` factors retained from screening: `fjoin(rsm_f)`." |
| Discussion | "A screening design ranked the `n_scr_f` factors and a response surface design modelled the region defined by the `n_rsm_f` that screening retained: `rsm_list`." | "The four factors retained from screening are modelled by a response surface design: `fjoin(rsm_f)`." |

The Executive summary row is worth reading twice. The guide's ✗ example carried two faults in one
sentence — the false agent and the balanced `, and ` — and the correction fixed both: the agent is
gone and the second clause became its own sentence. But the new sentence closes on `, which
supports a full quadratic model`, so within the same correction the coordination it was told to
drop came back as subordination. That is the trade the table above counts.

**One instance of the same fault survives, deliberately.** `pc_package/PCR-003_bioreactor.qmd:879`,
§5.3: "Within that region, those models carry the predictive claim of this report." A model is the
agent of *carry*, which `WRITING_GUIDE.md` §2d forbids, but it matches none of the five search
strings the author was given and none of the five in the acceptance check. It was found during
verification and left in, because editing it would have made this page credit the **rule** for what
an orchestrator's grep actually did. Counted crudely (a study, design or model within sixty
characters of *carry / retain / select / identify*), round two has 5 such hits and round three has
2, of which one is a false positive of that regex and one is this sentence.

A second instance was found and *was* fixed, by the same agent in its own context, because it
failed the task's acceptance grep outright: the Executive summary closed on "those response surface
models carry the predictive claim and the basis of the design space in §6, whereas screening
identified only which factors matter". It now reads "In this report both the predictive claim for
those responses and the basis of the design space in §6 rest on the response surface models,
whereas the factors that matter were identified by screening."

## The stopping rule, line by line

The eight conditions were fixed in `state.json` → `decisions.stopping_rule_edges` by `/plan`,
before the document was written, and no edge was moved after the numbers were seen.

| # | condition | edge | round two | **round three** | holds? |
|---|---|---|---|---|---|
| 1 | `, and ` + clause (regex) | ≤ 3.4 % | 22.6 | **0.5** | ✅ |
| 2 | mid-sentence `, not ` | ≤ 0.2 % | 4.3 | **0.0** | ✅ |
| 3 | passive construction | 50–62 % | 35.4 | **57.4** | ✅ |
| 4 | mid-sentence `, so ` | ≤ 1.0 % | 0.0 | **0.0** | ✅ |
| 5 | opens with a connective | ≥ 3.0 % | 4.0 | **3.7** | ✅ |
| 6 | topic chaining | not > 2.0 pt below 46.1 | 46.1 | **47.6** | ✅ |
| 7 | copula main verb | not > 2.0 pt above 25.7 | 25.7 | **16.5** | ✅ |
| 8 | register gate | passes | passes | **passes, 12/12** | ✅ |

Nothing is within 0.5 points of an edge, so the "owner decides" clause of the rule is not invoked.

**Verdict: all eight hold. The line that decided the round is line 3** — the passive, which moved
22 points from twenty below every source to inside their range, on an instruction that gave a band
and a rule and never a count to hit.

**The one-genre caveat.** `PCP-003` was not re-authored, by owner decision, to spend the round on a
fourth point of the longest series instead. So every move above is a move *in the report*. The
control column shows where the plan genre stands without the round: `, and ` + clause still at
18.2 % by regex and 24.9 % by parser, `, not ` at 0.0, passive at 55.2 %. Whether the three new
measures move a plan the way they moved a report is not known and cannot be inferred from this page.

## The hypothesis, answered

Round two's finding was that every measure printed back to the author moved, and the three faults
the owner named were exactly the three that were not printed. Round three printed them.

| measure | printed to the author? | round two → round three |
|---|---|---|
| `, and ` + clause | **new this round** | 22.6 → 0.5 %, overshot below the sources |
| `, not ` | **new this round** | 4.3 → 0.0 %, to the floor |
| passive | **new this round** (band, in the brief) | 35.4 → 57.4 %, into the band |
| `, so ` | yes, since round two | 0.0 → 0.0 %, held |
| initial connective | yes, since round two | 4.0 → 3.7 %, held |
| 2+ coordinators | yes, since round two | 1.7 → 1.8 %, held |
| chaining | printed as context, never a goal | 46.1 → 47.6 %, rose |
| copula | printed as context, never a goal | 25.7 → 16.5 %, fell 9.2 pt |
| front field | printed as context, never a goal | 17.4 → 30.2 %, rose 12.8 pt |
| `, which` | **not printed to the author** | 9.50 → 15.33 %, rose |
| `its` per 1k | not printed since round two | 0.51 → 1.66, rose |

The pattern is now three rounds old and did not break: **what is measured and printed moves, and
what is not measured drifts.** Both of this round's regressions — `, which` and `its` — are
unprinted measures. Both of this round's unasked-for gains — copula and front field — are measures
that are printed as context even though nobody set them as a goal. Printing a number appears to be
enough; setting it as a target is not required, and setting it as a *substitution* is what produces
the overshoot.

## What was found on the way

- **The commercial scale is stated**, through `V["commercial_scale_l"]`, four times (Executive
  summary, §1.1, §3.1 twice). No typed measurement is anywhere in the document; the numeral lint's
  38 advisory hits are identifiers and statistical conventions.
- **No `{python}` expression yielding a name is the subject of a verb that agrees with it.** The
  grep from the previous unit returns nothing.
- **D-002 survived a third re-author**, verbatim as registered, unqualified, in §1.1 — and the
  narrower true elaboration follows it. `discrepancies.yaml` and `DISCREPANCIES.md` needed no edit.
- **The rhetorical layer needed a complete re-cut.** All 35 spans were ungrounded against the new
  text, against 33 of 35 at round two. Each was tested against **both** extractors before the
  builder ran — `check_grounding.docx_text` yields `R2` and `build_rhetorical_annex.doc_text` yields
  `R²` from the same 93,085-character extraction — and 35/35 passed under both on the first try, so
  the trap that cost round two a cycle cost this one nothing.
- **22 of 177 annex quotes needed re-anchoring**, against 23 at round two. Every table-row quote
  survived untouched again.
- **Two annex report-summary statements had to be rewritten, not just re-quoted.** One asserted the
  models are "predictive for four of them", which the re-authored report does not say anywhere. An
  annex statement can outlive the sentence it summarizes, and no gate catches that — only the
  re-anchoring pass does, and only if the person doing it reads the statement rather than hunting
  for a substring.
- **The acceptance grep and the guide disagree about `screening identified`.** The task's check
  forbids it; `WRITING_GUIDE.md:372` carries a ✓ example that writes "screening identifies the
  factors that matter" and §4 line 468 states the framing rule the same way. Nothing turned on it
  here, because the sentence that failed was a genuine fault on the rule's wording either way. It
  should be reconciled before round four.
- **The pages differ on the passive by 0.7 points for the same text.** Method, not text; see the
  note under the first table.

## The owner's reading

Recorded verbatim, 2026-08-18, after reading `pc_package/PCR-003_bioreactor.pdf` (56 pp,
rendered the same day):

> The document reads better. Not perfect but ok to me.

**This is the first reading in the series that names no sentence.** After round one the owner said
the prose "is written in a way no SME would write". After round two the owner recognised the report
on its first sentence and named three specific faults, all three of which counted out as real and
large and became this round's measures. After round three: nothing is named.

The reading is **not blind** — it is the fourth read of the same document by the same reader — and
that was accepted when the check was set up (`state.json` → `decisions.human_check`), because no
blind reader is available and one consistent reader across four points is worth more to the series
than a fresh reader at one point. A reader who has watched a document improve three times is a
reader disposed to see it improve a fourth. That caveat belongs on this page more than on any
earlier one, because this is the reading that stopped finding things.

**What follows from it, and what does not.** The rule the series has run on is *a reader finds it,
the count confirms it* — in that order. This round breaks the order: the reading found nothing, so
the section below was produced the other way round, by asking the numbers where the document moved
**away** from the four human sources while the three targeted measures moved toward them. Anything
that comes out of it is a count-led candidate, not a reading-led one, and round four should treat it
as the weaker kind of evidence. The distinction is the point of recording it.

## Where it got worse, count-led

The three targeted measures moved a long way toward the sources. Six others moved away from them in
the same re-author, and two of those crossed from inside the source range to outside it. Every cell
is from the same `measure_*.txt` files as the rest of the page.

| measure | sources | r2 | **r3** | what happened |
|---|---|---|---|---|
| `, which` (% of sentences) | 0.60–2.35 | 9.50 | **15.33** | already six times the sources, now more so |
| sentences inside a run of 3+ consecutive sentences under 15 words | 0.37–3.94 | **0.00** | **6.86** | from none at all to nearly twice the highest source |
| % of sentences under 15 words | 16.2–20.5 | 19.5 | **26.1** | inside the source range → above all four |
| mean sentence length (words) | 24.2–30.2 | 23.3 | **22.1** | below all four → further below |
| `their` per 1k words | 0.50–0.96 | 0.81 | **1.04** | inside → above all four |
| `its` per 1k words | 0.27–0.40 | 0.51 | **1.66** | above → four times the highest source |
| colons per 1k words | 2.1–4.3 | 2.2 | **1.3** | inside → below all four |
| parenthetical openings per 1k | 10.7–14.2 | 7.5 | **6.6** | below all four → further below |
| connectives, of the nine distinct | 6–9 | **9** | 8 | the full repertoire, reached once, lost |

Two of these are worth reading as prose rather than as rows.

**The staccato is new, and it is the clearest of them.** Round one and round two contain **zero**
runs of three or more consecutive sentences under fifteen words. Round three contains **eight**, the
longest five sentences long. The four human sources all have such runs — 1 to 10 of them, up to
eight sentences long — so the shape is not itself a fault; the frequency is. The rule "one argument
step per sentence, and the next step opens the next sentence" was executed to exhaustion, and this
is what exhaustion sounds like:

> The second tightest capability belongs to Galactosylation (total %Gal), at 2.86. By contrast, the
> remaining attributes sit far from their limits. Their capability indices therefore show only that
> none of them constrains the process. The furthest of those attributes from a limit is Aggregates
> (HMW), at 16.1. The capability index of that attribute is reported in Table 22 for completeness.

Five sentences, 56 words, five full stops. Round two wrote that passage as fewer, longer sentences
and scored 0.00 % on this measure.

**The subordination is the trade the round made, and it is visible in the sentence the guide itself
corrected.** The worked correction in `WRITING_GUIDE.md` §2d takes an Executive-summary sentence
with two faults — a study as agent, and a balanced `, and ` second clause — and fixes both. The
author applied it. Here is what the sentence became:

| | text |
|---|---|
| round two | "The 4 factors **that screening retained** then entered a face centred response surface design of 28 runs, **and** the remaining 4 parameters were assessed one at a time." |
| round three | "The 4 factors **retained from screening** were then studied in a face centred central composite design of 28 runs, **which** supports a full quadratic model over three levels of every factor it carries." |

The false agent is gone and the coordinated clause is gone. In their place is a trailing relative
clause. Across the document that trade repeats: 40 sentences carried a `, which` at round two and
**65** carry one at round three, and one sentence now carries two.

Neither regression was visible to the reading. Both were found by asking what paid for the wins.
`its` in particular is a count with almost no prose damage behind it — the sixteen instances are
"its normal operating range", "its own", "its calibration interval", each of them unremarkable. A
measure can move a long way without a reader ever noticing, which is the argument for measuring and
against relying on a reading alone. It is also the argument for the reverse: a reader who notices
nothing has not proved that nothing is there.

## Verification

```bash
R0=.claude/work/2026-08-16_01_register-from-four-sources/pre-rewrite
R1=.claude/work/2026-08-17_01_register-second-round/pre-rewrite
R2=.claude/work/2026-08-18_01_register-third-round/pre-rewrite
W=.claude/work/2026-08-18_01_register-third-round
F="$R0/PCR-003_bioreactor.qmd $R1/PCR-003_bioreactor.qmd $R2/PCR-003_bioreactor.qmd \
   pc_package/PCR-003_bioreactor.qmd pc_package/PCP-003_bioreactor.qmd"

uv run python authoring/check_style.py --compare $F              > $W/measure_style.txt
uv run --extra discourse python authoring/check_discourse.py $F       > $W/measure_discourse.txt
uv run --extra discourse python authoring/check_discourse.py --cap $F > $W/measure_discourse_cap.txt
```

The two claims made by grep rather than by a measure file:

```bash
grep -c 'screening retained\|screening identified\|the design carries\|the model identifies\|the study selected' \
     pc_package/PCR-003_bioreactor.qmd                       # 0  (round two: 3 of 'screening retained')
grep -cEi '\b(screening|the study|the studies|those studies|the design|the designs|those designs|the model|the models|those models)\b[^.]{0,60}\b(carr(y|ies|ied)|retain(s|ed)?|select(s|ed)?|identif(y|ies|ied))\b' \
     $R2/PCR-003_bioreactor.qmd pc_package/PCR-003_bioreactor.qmd   # 5 and 2
```

Possessives (`$W/measure_possessive.txt`), the subordination counts (`$W/measure_whatpaid.txt`)
and the staccato runs (`$W/measure_staccato.txt`) use the same prose extraction — `check_style.prose_from_qmd` and `check_style.prose_from_extract`
over `HUMAN_SOURCES` — and count by regex per 1000 words and per sentence respectively.

**Those three measures now have a script behind them**, written on 2026-08-18 because they did
not:

```bash
uv run --extra discourse python .claude/work/2026-08-18_02_register-track-d/measure_trackd.py \
    $(ls pc_package/*.qmd)
```

Its third block reproduces every figure in `measure_staccato.txt` and `measure_whatpaid.txt`
exactly, on all four sources and on both documents those files cover, and three of the four
possessive rates as well. **One does not.** The `it is/was` row here reads 22 / 28 / 41 / 50 on the
four sources and 4 on PCP-003; the script's pattern gives 18 / 28 / 40 / 50 and 3. Every candidate
pattern that lifts PDA TR 60 to 22 overshoots the other three, so the pattern behind the published
figure cannot be recovered from its output, and it was never written down. That number is not
stale, it is uncheckable, and it is the reason the script exists. Read the script's figure, not
this one.

Two definitions the file names did not record, and the script now does. The four subordination
rows count **occurrences over the whole prose, divided by the sentence count** — a rate per 100
sentences, not the share of sentences that carry one. PCR-003 carries 67 `, which` in 66
sentences, and 15.33 % is 67/437. The semicolon row separates the two further: 6 semicolons, only
1 of them inside a sentence the splitter kept. The possessive rates divide by
`len(text.split())`, the whole prose, which is up to 19 % larger than the word count
`check_style` divides by.

**The two scripts are the method for these measures.** `authoring/register_analysis.ipynb` §13 is
superseded for clause packing, chaining, copula, front field, the passive and the two and-clause
counts, and it was not re-executed here. The notebook remains the method for the analyses the
scripts do not cover.

The corpus state behind these numbers (TASK-005): 2084/2084 quotes grounded across 20 annexes with
`GROUNDING_STRICT_ANCHORS=1` and no weak anchors, 20/20 annexes valid, `weak_claims` empty in both
bioreactor annexes, `git diff outputs/` empty, `make test` 89 passed, `make style` 24 OK and 0 FAIL,
`PCR-003_bioreactor.pdf` rendered fresh at 56 pages with no missing glyphs.

## Files

| file | what it holds |
|---|---|
| `.claude/work/2026-08-18_01_register-third-round/measure_style.txt` | the regex measures and the register gate, five files, one invocation |
| `…/measure_discourse.txt` | chaining, copula, front field, passive, parser and-clause, uncapped |
| `…/measure_discourse_cap.txt` | the same under the notebook's 600/450 caps, for comparison with earlier pages |
| `…/measure_possessive.txt` | `its`, `their`, `it is/was`, `the <noun> is` per 1000 words |
| `…/measure_whatpaid.txt` | `, which`, `, where`, semicolons, `, because` per sentence |
| `…/measure_staccato.txt` | runs of 3+ consecutive sentences under 15 words, and the share of sentences inside one |
| `…/pre-rewrite/PCR-003_bioreactor.qmd` | round two, byte-identical to `e7a4768` |
