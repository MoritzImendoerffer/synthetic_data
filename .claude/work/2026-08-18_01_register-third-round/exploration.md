# Exploration — round three: measure the three faults the reader named, on PCR-003

**Proposal:** `docs/next/register-from-four-sources.md`, Track A + Track B, on `PCR-003` alone.
This unit does not restate it.
**Predecessors:** `2026-08-16_01_register-from-four-sources` (round one, measured in
`docs/results/2026-08-17-register-pilot.md`) and `2026-08-17_01_register-second-round` (round two,
`docs/results/2026-08-18-register-round-two.md`). Both shipped.
**Date:** 2026-08-18. **Written by:** `/explore`.

## 1. What triggered this unit

Round two cleared every target it set and every line of a stopping rule fixed in advance. The
project owner then read the pair and recognised it on the first sentence of the report, and named
three faults nothing had measured. Counted afterwards, they are real and large:

| fault | sources | PCR-003 r0 → r1 → r2 |
|---|---|---|
| `, and ` joining a second clause | 1.1–3.4 % of sentences | 24.9 → 21.0 → **22.6 %** |
| `, not ` contrastive tail | 0.0–0.2 % | 0.0 → 0.0 → **4.3 %** |
| sentences carrying a passive | 54.3–59.8 % | 44.1 → 41.6 → **34.4 %** |

The finding that reshaped the proposal: every measure printed back to the author moved, and these
three are exactly the ones that were not printed back — two of them already forbidden in words by
`WRITING_GUIDE.md`. So this round is about the measures. The owner settled two things on
2026-08-18: measures first (Track A before Track C), and `PCR-003` alone, for a fourth point on
the longest series.

## 2. Every claim in the proposal, checked against the repository today

All hold. Verified by running, not by reading.

- **`check_style.py` does not count `, and ` joining a clause, or `, not `.** True. It has
  `CLAUSE_COORD` (comma + one of nine coordinators, counted per sentence and reported as **2+**),
  `SO_MID` and `INITIAL_CONNECTIVE`, and nothing else in the family. A sentence with exactly one
  `, and ` joining two clauses is invisible to it — the round-two blind spot the proposal names.
- **`check_discourse.py` does not measure the passive.** True. `nsubjpass` appears twice, both
  times only to *find* a subject for chaining and front field. Nothing counts `auxpass` or reports
  a passive rate.
- **§2d already forbids `, and …` carrying a second claim** — line 161. **§4b already says the
  sources almost never build "not X but Y"** — line 563. **§4b already says passive is fine and
  the sources use it heavily** — line 581. All three are rules with no measure behind them.
- **The false agency is in the shipped `PCR-003`** — and not once but **three times**: lines 494
  ("the factors that screening retained"), 915 ("factors screening retained") and 1588 ("the four
  that screening retained"). The proposal quotes one; the document has three, all the same verb.
  Track B's rule has one concrete target sentence pattern.
- **The four-point series is intact.** Round zero at
  `.claude/work/2026-08-16_01_register-from-four-sources/pre-rewrite/PCR-003_bioreactor.qmd` is
  byte-identical to `git show b0361f1:…`; round one at
  `.claude/work/2026-08-17_01_register-second-round/pre-rewrite/PCR-003_bioreactor.qmd` is
  byte-identical to `git show f06f1a7:…`; round two is the committed `pc_package/PCR-003_bioreactor.qmd`
  at `e7a4768`. Round three will be the fourth point.
- **The runtime-noun rule sits at §2d Correction 0, lines 188–190**, so Track B's write-the-passive
  rule has the neighbour the proposal names.

## 3. What the proposal does not say, and this round has to know

**The round-two counts were produced by code that was never saved.** `measure_owner_reading.txt`
holds the numbers, but the regexes that produced them lived in an inline heredoc in the TASK-008
session and are in no file. `clause_pack.py` in the previous unit does not have them. The first
thing this round does is make the measure a file, and it should reproduce the round-two table
exactly before it becomes the gate's line — the same discipline TASK-001 applied to `clause_pack.py`.

**The `, and `-clause regex is a proxy, and its limits are known.** Reconstructed today from the
results page, it is comma + `and` + one of a fixed list of clause openers (`the`, `this`, `that`,
`it`, `they`, `its`, `their`, `a`, `an`, a present participle …). Tested against the owner's three
sentences: **all three match**. Tested against four controls: an Oxford comma before a noun, an
`, and` before a prepositional phrase, and `, and to` all correctly do *not* match — but a genuine
second clause with a bare-noun subject ("…were carried forward, and osmolality was not") also does
not match. So the count is a floor on the real rate, and the source-versus-corpus gap of six to
twenty times is if anything understated. Good enough for an advisory line; not good enough to
gate, which is another reason nothing here is gated. A parser (`cc` + `conj` where the conjunct
has its own `nsubj`) would count it exactly, at the cost of belonging in `check_discourse.py`
rather than `check_style.py`. Both are worth printing; the regex one is the one that runs without
the extra.

**The passive count is spaCy's and needs the extra**, which is installed today (spacy 3.8.15,
`uv sync --extra discourse`). It goes in `check_discourse.py` beside chaining/copula/front, as a
**band** — `PCP-003` is inside the source band and `PCR-003` is under it; a floor would push the
plan the wrong way. It should print the same way the other three do, with denominators, and it
should be in the brief's §5d table so the author sees it.

**Two overshoots from round two are the pattern to expect again.** `, so ` went to 0.0 %, below
every source, and `PCP-003` reached zero possessives. A rule stated as a substitution is executed
to exhaustion. If Track A's `, and ` measure is stated as a substitution, expect 0.0 % `, and `
clauses in the re-authored report — which is again below the sources (1.1–3.4 %). Whether that is
acceptable is for the results page to say; it should be predicted here so it is not read as a
surprise.

**A one-genre round loses the both-genres check.** The proposal states this cost. It bears
repeating in the plan: if a measure moves in `PCR-003`, the page says "moved in the report".

## 4. What the work touches, by layer

| Layer | Files | Cost |
|---|---|---|
| machinery | `authoring/check_style.py` (two regex counts beside the packing line, `render()` and `compare()`; `--selftest` must still pass 4/4), `authoring/check_discourse.py` (passive rate, band, denominators, `--json`), `authoring/build_brief.py` §5d (three new rows), `authoring/WRITING_GUIDE.md` (Track B rule beside Correction 0; §2d names `, and `-clause and `, not ` as strings to search for; §4a two diagnostic rows), `tests/test_style.py` (fixture for the two new counts) | `make style` 20/20 stays green; `check_blank_repo.sh` PASS |
| document | `pc_package/PCR-003_bioreactor.qmd` only | one one-pass re-author, one agent, from the amended artifacts; render docx **and** pdf explicitly |
| annex | `pc_package/build_ground_truth.py` (bioreactor report quotes; the plan's stay), `authoring/rhetorical/PCR-003.spans.yaml` (35 spans, likely most re-cut again), `authoring/discrepancies.yaml` D-002 re-verified | round two: 23 quotes + 33 spans for this document |
| model | none | `git diff outputs/` empty at ship |

Tests covering this today: `check_style.py --selftest` (4/4), `tests/test_style.py` (3 tests),
`make style` (24 OK), `check_exemplar_quotes.py` (128), `check_render.py`,
`build_ground_truth.py` + `validate_annex.py` + `check_grounding.py` strict (2084/2084),
`make test` (88), `check_blank_repo.sh` (PASS). Nothing tests the two new regexes or the passive
count yet; `test_style.py` is where the fixture goes.

## 5. Ground rules that bite here

- **No number changes.** Nothing in `config` moves. `outputs/` must be unchanged at ship.
- **Prose changes → one-pass re-author of `PCR-003`, never a patch.** The three
  "screening retained" sentences are not to be edited in place; the author writes the whole
  document again with the passive rule in hand.
- **D-002 is in scope** and must survive a third re-author, unqualified, in the introduction.
  Brief §5c carries it. Re-verify `registered_sentence` against the new text at ship.
- **The rhetorical layer is 35 spans, none dropped.** Re-curate before rebuilding, and test every
  span against **both** extractors — `build_rhetorical_annex.doc_text` yields `R²`,
  `check_grounding.docx_text` yields `R2` — the trap round two hit at RS-J02.
- **`, and ` and `, not ` are advisory.** Not in `LIMITS`. A ceiling on `, and ` is met by a
  semicolon; the semicolon ceiling (4.5 per 1k) already exists and should be watched.
- **The passive is a band.** Never a floor. `PCP-003` at 54.7 % is inside it.
- **Nothing added after authoring.** The rules go into the guide and the brief before the author
  starts. Grounding failures are fixed by re-anchoring.
- **The extra stays optional.** `check_discourse.py` degrades to one line without it; nothing on
  `test`, `style` or `corpus` may start depending on it.

## 6. What could go wrong

- **The measure moves and the reading does not, again.** Round two's lesson is that the round that
  clears a measure exposes the next one. The page should say so in advance, and the owner's reading
  stays the human check.
- **The `, and ` substitution produces semicolons or `, which`.** Both are already measured (the
  semicolon ceiling; `, which` is in `CLAUSE_COORD`). Print them together.
- **Passive rate rises past the band.** Told to "write the passive", an author may write it
  everywhere. The band (54–60 %) is the guard, and the plan is inside it, so a floor is not needed
  and a ceiling exists in the band. Watch the plan-genre value even though the plan is not
  re-authored — it is the control.
- **The regex proxy under-counts.** Stated above; the results page quotes it as a floor.
- **The reader is not blind, three times over.** Stated in the proposal; the reading is still the
  test.

## 6b. Regex or parser for the `, and ` clause — measured, 2026-08-18

Asked by the owner. Answered by running both (`andclause.py` in this unit, spaCy `en_core_web_sm`
3.8.0), over the same prose the gate reads:

| | regex (comma + `and` + clause opener) | parser (`cc` + `conj` with its own `nsubj`, comma before) |
|---|---|---|
| PDA TR 60 | 3.4 % (28/820) | 3.2 % (26/820) |
| A-Mab | 1.1 % (11/1041) | 1.2 % (13/1041) |
| ISPE TT | 1.3 % (9/669) | 0.9 % (6/669) |
| ISPE PV | 3.1 % (25/808) | 2.8 % (23/808) |
| PCR-003 round zero | 24.9 % (108/433) | 28.9 % (125/433) |
| PCR-003 round one | 21.0 % (89/423) | 25.3 % (107/423) |
| PCR-003 round two | 22.6 % (95/421) | 24.9 % (105/421) |
| PCP-003 round two | 18.2 % (37/203) | 24.6 % (50/203) |

The source columns agree to within half a point, so the 6–20× gap is real under both. On the
corpus the regex undercounts by 2 to 6 points: it is a floor.

**But neither is a superset of the other**, and the disagreements are the useful part. On round-two
`PCR-003`, 37 sentences are parser-only and 27 are regex-only:

- **Parser catches, regex misses:** a second clause opening on a bare noun or a quantifier —
  "…recorded 2 deviations, **and both** were retained", "…deamidation of asparagine, **and
  deamidation** is base catalysed", "…two things, **and both of them** shaped this study". The
  regex's fixed opener list cannot see these, and they are exactly the owner's shape.
- **Regex catches, parser misses:** long coordinated noun phrases where `en_core_web_sm` attaches
  the `and` to the wrong head — **including two of the three sentences the owner quoted** ("The 4
  factors that screening retained then entered … , and the remaining 4 parameters were assessed";
  "…the design space and the proven acceptable ranges … rest on it, not on…"). The small model is
  unreliable on 40-word sentences with stacked coordination, which is the sentence type at issue.

**Decision for /plan: print both, on separate lines, and say which is which.** The regex goes in
`check_style.py` beside the packing line because it runs without the extra; the parser count goes
in `check_discourse.py` beside chaining because it is the more exact one where the parse is
right. Neither is gated. Where they disagree the union is closest to the truth, and the results
page reports both. Do **not** replace the regex with the parser (it loses two of the three
sentences that started this) and do **not** move to `en_core_web_trf` for accuracy — that turns
an optional 50 MB extra into a 500 MB one plus torch, on a diagnostic that fails nothing.

## 7. Open questions for /plan

1. ~~**Regex or parser for the `, and ` clause, or both?**~~ **Both — settled by measurement in
   §6b.**
2. **Does the stopping rule get edges?** The proposal deliberately gates nothing. A results-page
   rule of the round-two kind (fixed in advance, applied line by line) is still useful for the
   *verdict*; the edges are the source bands: `, and ` clause ≤ 3.4 %, `, not ` ≤ 0.2 %, passive
   54–60 %, plus no regression on the five round-two measures. Recommend fixing them in `/plan`
   under `decisions.stopping_rule_edges`, as before.
3. **Does the plan get its brief §5d rows too, though it is not re-authored?** Recommendation:
   yes — the rows are generated, cost nothing, and `PCP-003`'s value is the control that says
   whether a report-only move is a report-genre effect.
