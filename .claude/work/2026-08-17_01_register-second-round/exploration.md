# Exploration — the second two-document round, after the owner read PCR-003

**Proposal:** `docs/next/register-from-four-sources.md`, Track 1. This unit does not restate it.
**Predecessor:** `2026-08-16_01_register-from-four-sources`, delivered; measured in
`docs/results/2026-08-17-register-pilot.md`.
**Date:** 2026-08-17. **Written by:** `/explore`.

## 1. What triggered this unit

The project owner read the re-authored `PCR-003` (the owner wrote "PCR-008" and corrected it to
PCR-003 in the same sitting; both quoted sentences are in `pc_package/PCR-003_bioreactor.qmd`).
The verdict: better than the previous revision, still clearly machine-written. Two sentences
were quoted, both from `# Discussion`:

1. Line 707: *"The lack-of-fit tests rest on 4 centre-point replicates, so a non-significant
   result bounds the evidence for the model form without establishing it, and acidic variants is
   the case to watch (p = 0.15)."* Owner: hard to understand, too many arguments in one sentence,
   with a recommendation in the last part. "A classical case for fillers like 'Therefore, ',
   'However, ', 'As a consequence, '."
2. Line 701: *"The step is understood well enough to support the ranges proposed for Stage 2,
   and that understanding rests on a screening design that ranked the factors and a
   response-surface design that models the four that matter."* Owner: "the four that matter …
   what four?"
3. In general: "the structure and logical reasoning could be improved."

This is the second human reading taken in the campaign. The first (2026-08-17, same owner)
withdrew the possessive result. This one names a defect the pilot did not measure.

## 2. What the two sentences show, read closely

**Sentence 1** carries three argument steps — a premise (four replicates), a consequence (the
test bounds without establishing), and a recommendation (watch acidic variants) — joined by
`, so … , and …`. The sources make one step per sentence and open the next with a connective.
Two further faults sit inside it, and neither is register:

- `acidic variants is` — the subject is `{python} lof_p_lo_resp.lower()`, a computed response
  name dropped into a sentence written for a singular. Number agreement cannot be checked when
  the noun is a runtime value. Any inline expression used as a grammatical subject has this
  exposure; `pred_lo_resp.lower()` in the executive summary is the same pattern (there it is an
  object, so it survives).
- The recommendation clause is a corpus tic. `the case to watch`, `the item to revisit` (line
  707, two sentences later) — a sentence-final verdict tacked onto a finding. Not counted; noted.

**Sentence 2** counts a set the paragraph has not named. "The four" is resolvable only from
`## Response-surface design` at line 425 (culture pH, temperature, culture duration, dissolved
CO2), 270 lines earlier, or from `# Conclusions` at line 715, which names them in full. The
Discussion never does. This is exactly the referent-binding fault §2d Correction 3 describes for
possessives, at the level of a numeral: the reader is asked to bind "four" from memory.

## 3. The measurement — the owner's diagnosis reproduces, and it was not on the pilot's list

Regex over the same prose the gate reads (`check_style.prose_from_qmd` / `prose_from_extract` /
`sentences`, source page ranges from `HUMAN_SOURCES`). Script: `clause_pack.py` in this unit;
`uv run python .claude/work/2026-08-17_01_register-second-round/clause_pack.py`. No spaCy.

| | n sent | ≥2 clause coordinators | mid-sentence `, so ` | `, so … , and ` | sentence-initial connective |
|---|---|---|---|---|---|
| PDA TR 60 | 820 | 2.3 % | **0.1 %** | 0.0 % | **4.8 %** |
| A-Mab | 1041 | 1.2 % | **0.3 %** | 0.0 % | **6.1 %** |
| ISPE TT | 669 | 1.5 % | **0.4 %** | 0.1 % | **4.2 %** |
| ISPE PV | 808 | 3.1 % | **0.4 %** | 0.0 % | **3.7 %** |
| `PCR-003` before | 433 | 8.8 % | 6.5 % | 0.9 % | 2.1 % |
| `PCR-003` after | 423 | 5.4 % | **8.0 %** | 1.4 % | **0.9 %** |
| `PCP-003` before | 202 | 6.4 % | 7.9 % | 1.5 % | 0.0 % |
| `PCP-003` after | 226 | 9.3 % | **10.6 %** | 1.8 % | 1.8 % |
| `PCR-008` (untouched) | 414 | 9.2 % | 6.3 % | 1.4 % | 0.0 % |
| `PCR-005` (untouched) | 374 | 6.7 % | 11.0 % | 0.8 % | 0.0 % |

Coordinators counted: `, so | , and | , but | , since | , because | , which | , while | , whereas
| , yet`. Sentence-initial connectives: However, Therefore, Consequently, As a result, In
addition, For this reason, By contrast, For example, Thus, Hence, Moreover, Furthermore,
Nevertheless, Instead, First/Second/Third, Finally, Overall.

Three things follow.

- **The corpus reasons inside the sentence; the sources reason across sentences.** Mid-sentence
  `, so ` runs 20 to 30 times the source rate — one sentence in 9 to 12 in the corpus, one in
  250 to 1000 in the sources. Sentence-initial connectives run at a fifth to nothing of the
  source rate. The two numbers are the same defect seen from both ends: the step the sources
  put after a full stop, the corpus puts after a comma.
- **The re-authoring made it worse in both documents.** `, so ` went 6.5 → 8.0 % in the report
  and 7.9 → 10.6 % in the plan. The pilot's one clean win, the connective repertoire (3/9 →
  6/9 distinct), was counted from words anywhere in the sentence — `since`, `once`,
  `consequently` inside a clause count the same as at its head. It did not see that the
  sentence-initial rate stayed at 0.9 % and 1.8 %.
- **This is a substitution, and the pilot found that substitutions land.** "Never join two
  argument steps with `, so`; end the sentence and open the next with the connective" is finite
  and self-checkable — search the draft for `, so `. The possessive experience says the
  substitution must be named or the cost lands in another metric (there: copulas). Here the
  substitution *is* the sentence-initial connective, and the front-field measure (Shape 4, which
  fell 14.7 → 9.2 % in the report) is where the payoff would show. One rule serves two of the
  pilot's failed shapes.

**Density is not the whole argument, and the pilot says so.** `its` at one in 6.3 sentences was
not perceived; `, so ` at one in 12 was — the owner quoted an instance unprompted. What differs is
load: a possessive is a word, a packed sentence is where the reasoning is. Record this as *a
reader found it and the count confirms it*, in that order, which is the order the pilot's lesson
("ask a reader before promoting a metric") demands.

## 4. What the proposal and its predecessor did not have

- **`syntax-analysis.md` §"Coordination is identical" measured the wrong coordination.**
  "Longest in-sentence list chain 0.72–0.95 on both sides" is `conj` chain length — noun lists.
  It never measured clausal coordination, and the null result was read as "coordination is not
  the difference". It is, at the clause level, by an order of magnitude.
- **The proposal's Track 1 measures (chaining, copula, front field) all need spaCy.** The
  measure that matches what the reader saw needs a regex, and can sit in `check_style.py`
  beside `CONNECTIVES` today, printed and gated by nothing. It does not depend on the optional
  dependency landing.
- **The guide already has the rule and its own prose breaks it.** §2d: "One sentence, one point;
  if a sentence carries two claims, make it two sentences." §4b: "The default way to add a
  qualification … is a new sentence. Not … a subordinate clause." Yet §2d Correction 2's ✓ text
  is *"The remaining attributes sit far from their limits, so the capability indices show only
  that …"* — the exact construction — and the author-facing artifacts model zero sentence-initial
  connectives: `WRITING_GUIDE.md` commentary 0.0 % (n=262, `, so ` 1.5 %),
  `REGISTER_EXEMPLAR.md` commentary 0.0 % (n=129, `, so ` 5.4 %), `STORY_BIBLE.md` 0.0 %,
  `PCR-003.brief.md` 0.0 %, `CLAUDE.md` 0.0 %, and this proposal itself 0.0 % with `, so ` at
  11.5 %. The author reads 700 lines of guide written in the register the guide forbids. The
  source *quotes* in the exemplar are at the source rate; the commentary around them is not.
- **The proposal's stopping rule cannot see this.** "Chaining clears 45 % in both genres and
  neither copula nor front field regresses" would pass a document at 10 % `, so `.
- **The `15,000` finding stands.** The pilot recorded that the re-authored `PCR-003` never
  states the commercial scale; `grep -c "15,000\|15 000" pc_package/PCR-003_bioreactor.qmd` is
  still 0 (checked 2026-08-17). A brief-side requirement, not a register one.

Claims of absence re-verified today: `authoring/check_discourse.py` does not exist; no `spacy`
in `pyproject.toml`, `requirements.txt` or `uv.lock`; no `[project.optional-dependencies]`;
the brief runs §5 → §5c → §6 so §5d is free; `tests/` holds `test_config`, `test_grounding`,
`test_process` and no style test (the gate's test is `check_style.py --selftest`, run by
`make style`).

## 5. Does the proposal still stand?

**Track 1 stands. Its list is short by one item and its stopping rule is blind to the defect
the reader found.** Nothing in the proposal is now wrong; the four items (`check_discourse.py`,
brief §5d, §2d bis substitution, Shape 4 positive example) are still the right machinery. What
this exploration adds:

- a fifth item, cheaper than the other four and independent of spaCy: **measure clausal packing
  and sentence-initial connectives in `check_style.py`** (advisory, printed like `CONNECTIVES`),
  and **rewrite the guide's rule as a substitution**: one argument step per sentence; the next
  step opens the next sentence with the connective; `, so ` and `, and <clause>` are the
  constructions to search a draft for. Correction 2's ✓ text has to change or be relabelled,
  since it currently teaches the fault.
- a **brief-side referent rule** for §5d: a sentence that counts a set ("the four", "both",
  "the three") names it in the same paragraph or in the sentence. Not measurable cheaply;
  authorable and reviewable.
- **the stopping rule gains a line**: `, so ` at or under about 1 % of sentences and
  sentence-initial connectives at or above about 3 % in both genres, alongside chaining. These
  are the source bands from the table above; the exact edges are for `/plan`.
- the pilot's own caution applies to the new number too: **a ceiling on `, so ` is met by
  writing `, and` or `; ` or `, which`.** Measure the whole coordinator family and the
  sentence-initial rate together, so the substitution shows up where it goes. The semicolon
  ceiling (4.5 per 1k) already catches one escape route.

The proposal text itself is not edited by this command. `/plan` should carry the additions in;
if the owner wants the proposal amended first, that is a five-line edit to Track 1 and the
stopping rule.

## 6. What the work touches, by layer

| Layer | Files | Cost |
|---|---|---|
| machinery | `authoring/check_style.py` (new advisory measures beside `CONNECTIVES`; `measure()`, `connective_line()`, `render()`; `--selftest` must still pass on all four sources), `authoring/check_discourse.py` (new; spaCy, degrades to one line + exit 0), `authoring/WRITING_GUIDE.md` §2d / §2d bis / §4b / Shape 4, `authoring/REGISTER_EXEMPLAR.md` (source quotes with the connective-led second sentence), `authoring/build_brief.py` (§5d), `pyproject.toml` + `uv.lock` + `requirements-discourse.txt` (optional group), `Makefile` (`style` target unchanged; a `discourse` target if wanted, never on the `corpus` path) | whatever the gate reads; `make style` 20/20 must stay green on the untouched 18 |
| document | `pc_package/PCP-003_bioreactor.qmd`, `pc_package/PCR-003_bioreactor.qmd` | one-pass re-author each, one agent each, from the brief and the amended guide; never from a sibling; render docx **and** pdf explicitly (`check_render.py --render` glyph-checks the stale pdf) |
| annex | `pc_package/build_ground_truth.py` (bioreactor quotes), `authoring/rhetorical/PCR-003.spans.yaml` (35 curated spans), `authoring/discrepancies.yaml` | budget ~40 re-anchored spans per document (pilot: 24 + 56, of which 34 were the curated layer); D-001 and D-002 sentences re-verified |
| model | none | no number changes; `git diff outputs/` must be empty at ship |

Tests that cover this today: `check_style.py --selftest` (four sources pass the band),
`make style` (20 documents), `check_exemplar_quotes.py` (every exemplar quote verbatim in
`refs/text/`), `check_render.py` (render + glyphs + style gate), `build_ground_truth.py` +
`validate_annex.py` + `check_grounding.py` with `GROUNDING_STRICT_ANCHORS=1` (2084/2084 today),
`make test` (85). Nothing tests `prose_from_qmd`/`sentences` directly; a new advisory measure
should get a small fixture test or a self-test line.

## 7. Ground rules that bite here

- **No number changes.** The two quoted sentences pull `cp_rsm`, `lof_p_lo`, `lof_p_lo_resp`
  through inline expressions; that stays. The agreement fault (`acidic variants is`) is fixed
  by the author choosing a frame the runtime noun cannot break ("the weakest case is …",
  "for `{python} …`"), not by typing the name. Worth one line in the brief's helper notes.
- **Prose changes → one-pass re-author, both documents, no patching.** The pilot's TASK-007
  is the template. The two quoted sentences are not to be edited in place.
- **D-001 (`PCP-003`) and D-002 (`PCR-003`) are in scope** and must survive; brief §5c carries
  them; `DISCREPANCIES.md` entries are re-verified against the new text at ship, as the pilot
  did.
- **`nlp_reports` and `pc_package/annex_contract/` untouched.** No schema change is implied.
- **Weak claims:** not touched; `main` stays at zero. The branch falls further behind by two
  more re-authorings, which `docs/next/weak-claims-branch.md` already prices.
- **Nothing added after authoring.** The referent rule and the packing rule go into the guide
  and the brief before the author starts. Grounding failures are fixed by re-anchoring quotes.
- **`make corpus` may not depend on spaCy.** `check_discourse.py` exits 0 with one line when
  the parser is missing; the `corpus`, `style` and `test` targets never call it.

## 8. What could go wrong

- **Sentence splitting pushes `pct_under_15` up.** Band 15.0–32.0; `PCR-003` after sits at
  22.7 %, `PCP-003` at 20.4 %. Splitting one sentence in ten into two adds roughly 5–8 points.
  Room exists; the author has to know the ceiling. `pct_over_40` is already near its floor
  (4.5 % vs 3.0), so the split must not also flatten the long tail.
- **The escape routes.** `, so ` → `, and`, `; `, `, which`, `so that`. Count the family, print
  it, and watch the semicolon ceiling. A rise in `, which` is a rise in relative clauses per
  sentence, which the earlier syntax analysis measured at parity (0.24–0.28) — a cheap
  before/after check.
- **A floor on sentence-initial connectives is met by typing "Therefore,".** Keep it advisory;
  the guide already says a produced connective is a worse tell than a missing one. The measure
  exists to show the author where the reasoning went, not to be a target.
- **The guide is read by the same author that writes.** If the guide's commentary keeps
  modelling `, so ` at 1.5–5.9 % and initial connectives at 0 %, the rule competes with 700
  lines of counter-example. Rewriting the guide's own commentary is a real task, and a large
  one; the minimum is Correction 2's ✓ text and Shape 4's example. This is the same loop
  `CLAUDE.md` warns about for sibling `.qmd`s, one level up.
- **The owner is no longer a blind reader of PCR-003 or PCP-003.** Open question 2 of the
  proposal (a valid discrimination test) is now harder, not easier: the only reader who has
  been asked has read both documents twice. A third round would need a passage-level blind
  read by someone else, or a different document.
- **"Structure and logical reasoning could be improved" is not yet operational.** The two
  quoted sentences give two operational rules (one step per sentence; name the set you count).
  The general remark is not measured here and this exploration does not claim to cover it.

## 9. Open questions — answered by the project owner, 2026-08-17

1. **Clause packing displaces chaining as the primary target.** The round's stopping rule is
   the packing line — mid-sentence `, so ` at or under about 1 % of sentences and
   sentence-initial connectives at or above about 3 %, in both genres — with chaining and
   copula reported and required **not to regress**. Chaining is not required to clear 45 %.
   Reason: packing was found by a reader and confirmed by a count; chaining was found by a
   count and no reader has confirmed it. `/plan` sets the exact edges from the source table
   in §3.
2. **Guide: minimum now, full rewrite as a hypothesis.** Change §2d Correction 2's ✓ text
   (it teaches the fault) and give Shape 4 a positive example. Do not re-author the guide's
   commentary in this round. If both re-authored documents still pack sentences after the
   rule is stated as a substitution and the count is printed back to the author, the guide's
   own register becomes the next suspect and the full rewrite is the next unit.
3. **The discrimination test is dropped as the acceptance criterion; the owner's reading is
   the human check.** Owner: "it is immediately obvious that the text is AI generated." A
   blind passage test would score at ceiling for the same reason the three pilot rounds did,
   and would tell nothing the owner's reading does not. The round's human bar is therefore
   qualitative and stated in advance: the owner reads the re-authored pair and reports whether
   it is still *immediately* recognisable as machine-written, and if so quotes what gives it
   away, as was done for `PCR-003` today. Same pair (`PCP-003` + `PCR-003`), for the third
   comparable measurement.
