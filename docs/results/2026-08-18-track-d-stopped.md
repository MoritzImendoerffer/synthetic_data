# Track D, stopped after the pilot: the register gate enforces the register it was built to stop

**2026-08-18.** Work unit `2026-08-18_02_register-track-d`. Stopped by the project owner after the
pilot of three, on the owner's reading. Decision D3 settled: **stop**.

The round re-authored three of nineteen documents — `PCP-007` (a plan), `PCR-005` (a DoE report)
and `RA-001` (never re-authored before, and the largest annex in the corpus at 317 quotes) — then
halted for a human reading before committing the remaining sixteen. That is what the pilot was
for, and it did its job: it cost three documents to find something that would have cost nineteen.

## 1. The eight numeric conditions all held

Fixed in `state.json` → `decisions.pilot_stopping_rule` before `TASK-003` ran, and not moved
afterwards. `PCR-003` is the untouched control and reads ±0.0 against its own baseline, which is
the check that the table measures what it claims to.

| condition | band | PCP-007 | PCR-005 | RA-001 | holds? |
|---|---|---|---|---|---|
| `, so ` mid-sentence | ≤ 1.0 | 0.0 (0/219) | 0.0 (0/424) | 0.0 (0/190) | yes |
| opens with a connective | ≥ 3.0 | 4.6 (10/219) | 4.5 (19/424) | 4.7 (9/190) | yes |
| `, and ` + clause, regex | ≤ 3.4 | 0.0 (0/219) | 2.1 (9/424) | 0.5 (1/190) | yes |
| `, not ` mid-sentence | ≤ 0.2 | 0.0 | 0.0 | 0.0 | yes |
| passive | 53–68 | 58.0 (127/219) | 54.3 (227/418) | 57.8 (107/185) | yes |
| topic chaining vs own baseline | not below | 59.2 (+19.9) | 39.6 (+4.8) | 44.6 (+5.5) | yes |
| copula vs own baseline | ≤ +2.0 | 13.7 (−3.0) | 18.7 (−8.6) | 17.8 (−6.9) | yes |
| register gate | passing | OK | OK | OK | yes |

Corpus state at the stop: `20/20 annexes valid`, `2084/2084 quotes grounded` with
`GROUNDING_STRICT_ANCHORS=1` and 0 weak anchors, `weak_claims` empty in all twenty,
`git diff outputs/` empty, `make test` 89 passed, `make style` 24 OK / 0 FAIL.

**Every measure the campaign has ever gated or printed was inside its band, and the documents were
still not acceptable.** That is the finding.

## 2. The ninth condition was the reading, and it failed

Recorded verbatim and dated in
`.claude/work/2026-08-18_02_register-track-d/owner-reading-2026-08-18.md`, before anything it
names was counted — the same order the three previous rounds used. The owner read the rendered
PDFs and quoted eight sentences across four messages. All eight are `PCR-005`.

## 3. What the reading counts out to

Per 100 sentences, produced by `measure_trackd.py` (§9). Sources are the four published human
documents in `refs/text/`, 3,338 sentences in total.

| | PDA | A-Mab | ISPE TT | ISPE PV | PCP-007 | PCR-005 | RA-001 | PCR-003 control | corpus/20 |
|---|---|---|---|---|---|---|---|---|---|
| `, which` | 1.10 | 1.44 | 0.60 | 2.35 | 17.4 | 16.7 | 7.9 | **15.3** | 9.82 (513) |
| `<quantifier> of which` | 0.12 | 0.00 | 0.00 | 0.00 | — | — | — | — | 0.38 (20) |
| all trailing relatives | 2.44 | 2.02 | 1.20 | 2.97 | — | — | — | — | **11.39 (595)** |
| `acts on / acts through` | **0.00** | **0.00** | **0.00** | **0.00** | — | — | — | — | 1.21 (63) |
| `follows from the …` | 0.00 | 0.00 | 0.00 | 0.00 | — | — | — | — | 0.23 (12) |
| `governs` / `sets <noun>` | 0.00 | 0.19 | 0.15 | 0.00 | — | — | — | — | 2.07 (108) |
| `aggressive(ness)` | 0 | 0 | 0 | 0 | — | 2 | — | — | 2 |

Two things follow immediately.

**`PCR-003` is the control, at `, which` 15.3.** That document was re-authored in round three and
accepted by the owner then — "The document reads better. Not perfect but ok to me." So the fault
was **not caused by the Track D instruction and was not introduced by the pilot.** It is
corpus-wide and predates all three previous rounds.

**Round three measured it and shipped anyway.** `docs/results/2026-08-18-register-round-three.md`
records `, which` rising 9.50 → 15.33 % as a regression, in a table headed "Where it got worse".
The number lived in a `.txt` file the author never saw. This is the third time the campaign has
learned the same lesson: a measure printed back to the author moves, and one that is not drifts.

## 4. The eight sentences, and what a paper would write

The owner asked for this table explicitly. Left column verbatim from `PCR-005`; right column is
what the same content looks like written as a paper would write it.

| # | as shipped | as a paper would write it |
|---|---|---|
| 1 | "The quadratic term in elution pH is significant at 1,944 (p = 0.0040), **which is the curvature a two-level design cannot see**" | "The quadratic term in elution pH is significant (1,944; p = 0.0040). Curvature of this kind cannot be estimated from a two-level design, in which every point sits at an edge of the range." |
| 2 | "The two estimates do not conflict, **because a non-significant screening estimate makes no claim about the sign**" | "The screening estimate for end of pool collect was not significant. The response-surface estimate is the one carried forward." |
| 3 | "The contours are curved instead of parallel, **which is the interaction and the pH curvature already seen in Table 5.8**" | "The contours are curved rather than parallel. Curvature reflects the quadratic term in elution pH and the load by pH interaction, both reported in Table 5.8." |
| 4 | "The leached Protein A model is retained as knowledge-space evidence and **is put to no other use in this report**" | "The leached Protein A model is retained as evidence of robustness. It supports no prediction and no range in this report." |
| 5 | "The surfaces in Figure 5.2 **follow from the physical chemistry of affinity capture** and confirm the expectations recorded in §2.1" | "Pool host cell protein rises as elution pH falls and as protein load rises, and the two effects are less than additive (Figure 5.2). Both directions were expected (§2.1)." |
| 6 | "Elution buffer pH governs pool host cell protein because it sets **the aggressiveness of desorption**" | "Elution buffer pH governs pool host cell protein because it sets how completely bound species are released. Lowering the pH protonates the histidine residues at the Fc–ligand interface and reduces affinity. The antibody elutes sooner, and the more weakly bound host cell protein elutes with it." |
| 7 | "Protein load **acts through the capacity of the bed**" | "As the protein load approaches the dynamic binding capacity of the resin, the mass transfer zone extends further down the bed. Impurity that would otherwise be washed out is carried into the eluate." |
| 8 | "Leaching of the affinity ligand **behaves as a resin property** over these ranges, since ligand release depends on the chemistry of the immobilization, on the cumulative cycle count and on the sanitization history, **none of which is a parameter of a single run**" | "Ligand leaching depends on the immobilisation chemistry, the cumulative cycle number and the sanitisation history. None of these varied within this study. No effect of the four operating parameters was therefore expected, and none was resolved." |

Three moves recur in the right column and none of them is stylistic. **Split the sentence**, so
each claim can be disagreed with separately. **Delete the gloss**, because a reader who has been
given the fact does not need to be told what to call it. **Name the cause**, where the shipped
version named a category — `aggressiveness`, `capacity of the bed`, `physical chemistry`,
`resin property` are all category labels standing where a mechanism belongs.

## 5. The verdict: why the agents do not write the right column

### 5.1 The gate forbids it. This is measured, not argued.

The eight shipped sentences and the eight rewrites, through `check_style.measure`:

| | shipped | rewritten | gated band |
|---|---|---|---|
| sentences | 8 | 18 | — |
| mean sentence length | 20.8 | **13.5** | **20.0–30.5** |
| % of sentences under 15 words | 12.5 | **55.6** | **15.0–32.0** |
| % over 40 words | 12.5 | 0.0 | 3.0–21.5 |
| trailing relatives | 3 | 0 | not gated |

**The rewrites fail the register gate on two of its twelve gated rows.** Mean length falls below
the floor and the short-sentence share rises past the ceiling. Every move that improves the prose
— split the sentence, drop the gloss, state the inference separately — pushes both numbers
straight at a gated edge.

This is eight sentences and not a document, and a whole document mixes these with ordinary
reporting prose, so the absolute figures would not be a document's figures. The *direction* is not
in doubt, and round three is the confirmation: it split sentences, `pct_under_15` went 19.5 →
26.1 % toward the 32.0 ceiling, and a staccato fault appeared at 6.86 % against sources at
0.37–3.94 %, which its own results page recorded as a regression. **The author has direct evidence
that writing shorter, more committed sentences gets punished.** The safe move under the gate is one
long sentence that packs the content and hedges it. That is exactly what the owner quoted.

The gate was built to stop machine register. It now enforces it.

### 5.2 The mechanism slot is required and unsupplied

`section_plan.yaml` demands mechanism in at least four places — "State the MECHANISM the study", a
whole `Mechanistic interpretation` section, "state directions + mechanism". Nothing supplies it:

- `REGISTER_EXEMPLAR.md` has **fifteen numbered reporting moves** — opening a unit operation,
  reporting a model, design space, capability, classification, deviations — and **not one is about
  explaining a mechanism.** It teaches how to report and never how to say why.
- The document brief runs §1 Identity, §2 Quality attributes, §3 Parameters, §4 DoE structure,
  §4b PARs, §5 Deviations, §5c discrepancies, §5d discourse targets, §6 Cross-references, §7 Helper
  inventory. **There is no mechanism section and no domain prose in it at all.**
- `STORY_BIBLE.md` §4 gives each step's **role** in the train, not its physical chemistry.

An author told to explain a mechanism, given no mechanism, and scored on surface counters will
produce a sentence shaped like an explanation. `follow from the physical chemistry of affinity
capture` passes all twelve gated rows and all five advisory ones. So does `acts through the
capacity of the bed`. Neither says anything.

### 5.3 Nothing measures whether a sentence commits to anything

There is no gate, and no advisory, that asks whether a `because` clause names a cause, whether a
term is a term of art, or whether a sentence makes a checkable statement. `check_grounding.py`
verifies that a quote appears in the document and that numbers come from the seeded CSVs. It
cannot see that `acts through the capacity of the bed` asserts nothing. The whole verification
stack is about **provenance and surface form**, and the fault is in **content**.

### 5.4 Three rounds optimised the wrong level

Rounds one to three tuned sentence *architecture*: clause packing, connective openings, the
passive, topic chaining, the copula. All three succeeded on their own terms and the numbers in §1
are the proof. None of them touched what a sentence *commits to*. Every one of the owner's eight
quotes is about commitment, and not one is about architecture.

### 5.5 The self-reference ban is right and is only half the rule

Documents may not be written from sibling documents — that ban exists because the machine register
propagated through the whole corpus once and forced all twenty to be re-authored. It is correct.
But it is not paired with any supply of human prose *about this domain* at sentence level.
`REGISTER_EXEMPLAR.md` is distilled from the sources for **voice**. Nothing carries the A-Mab or
ISPE passages on chromatography mechanism. So the author is given the shape of scientific prose
and not its substance, and returns shape without substance.

### 5.6 The review layer has the same blind spot, mine included

`rhetorical_spans` is a labelled benchmark layer. Across the nine annexed documents it carries
**26 spans labelled `mechanistic_warrant`**, and **6 of the 26 carry one of the flagged frames**
(`behaves as`, `acts on/through`, `follows from`, `aggressiveness`). Two of the six are sentences
the owner quoted; the others are in `PCR-004` and `PCR-008`.

Sentence 8 above is span `PCR-005-R17`, and it was selected **on 2026-08-18, in `TASK-006`, by this
session**, from a shortlist, as the clearest statement of mechanism in its section. The fault
passed the authoring agent, the register gate, and the annex review. All three were judging shape.

**A benchmark that labels a hollow warrant as a warrant teaches whatever trains on it that naming
a category is the same as giving a cause.** That is a worse defect than the prose, because the
prose can be rewritten and a mislabelled benchmark propagates.

## 6. What this invalidates

- **The plan's leading hypothesis was wrong.** `docs/next/register-from-four-sources.md` argues
  that `WRITING_GUIDE.md` is written in the register it forbids and that Track C is the blocker.
  The guide's own commentary does measure badly (3.77 % `, so `, 10.38 % `, and `+clause). But the
  fault the reading names is present in `PCR-003`, which was authored from that same guide and
  accepted, so the guide is not what produced it.
- **"All eight conditions hold" was never sufficient.** The stopping rule was built from measures
  that already existed. It could not fail on a fault nobody had measured.
- **Round three's own regression table was the warning.** `, which` at 15.33 % against 0.60–2.35 %
  is in it, under the heading "Where it got worse", and the round shipped.

## 7. What is left standing

The three pilot documents ship as they are. They are re-authored, rendered, annexed and grounded,
they pass every gate, and they are better on every measured axis than what they replaced. Stopping
the round does not revert them.

`TASK-001` (one gated mechanism for the rhetorical layer, 263 spans converted to YAML, all 20
annexes byte-identical) and `TASK-002` (`measure_trackd.py`, which reproduces both baselines cell
for cell) are mechanism work and are unaffected by the stop. `TASK-001` also closes half of
`docs/next/rhetorical-layer-coverage.md`.

## 8. What a fourth round would have to do differently

Not scheduled — this is the argument, not the plan.

1. **Supply the mechanism.** A per-unit-operation mechanism section in the brief, written from the
   published sources, with the terms of art. This is the largest item and the one without which
   nothing else helps.
2. **Fix the gate before using it again.** `mean_len` and `pct_under_15` currently penalise the
   sentence shape the owner asked for. A band that a good paragraph fails is a broken band.
3. **Print the trailing-relative count** to the author, as a band (sources 1.20–2.97) and never as
   a ban — a ceiling on `, so ` was met by writing `, and`, and a ban on `, which is` will be met
   by writing `, and this is`.
4. **Audit the 26 `mechanistic_warrant` spans** across all nine annexed documents, independently
   of any prose rewrite. `PCR-004` and `PCR-008` were not in this round and carry three of the six.
5. **Judge a draft on content, not only on counters.** Every gate in this repository is a surface
   measure, and the owner found in four readings what three rounds of counters did not.

## 9. Verification

```bash
W=.claude/work/2026-08-18_02_register-track-d

# the pilot table and the stopping rule, one invocation
uv run --extra discourse python $W/measure_trackd.py \
    pc_package/PCP-007_cex.qmd pc_package/PCR-005_protein_a.qmd \
    pc_package/RA-001_risk_assessment.qmd pc_package/PCR-003_bioreactor.qmd \
    > $W/measure_pilot.txt

# the script reproduces both committed baselines, and disagrees on exactly the three
# documents this round re-authored and on no other
uv run --extra discourse python $W/measure_trackd.py --check-baseline $(ls pc_package/*.qmd)

# corpus state at the stop
cd pc_package && uv run python build_ground_truth.py && uv run python validate_annex.py
GROUNDING_STRICT_ANCHORS=1 uv run python check_grounding.py
cd .. && make test PY="uv run python" && make style PY="uv run python"
```

The trailing-relative, `acts through`, `follows from` and `mechanistic_warrant` counts in §3 and
§5.6 were produced by short scripts run in this session against `check_style.prose_from_qmd` /
`prose_from_extract` over `HUMAN_SOURCES` and against `pc_package/ground_truth/*.json`. **They are
not yet in `measure_trackd.py`, and item 3 of §8 is where they belong** — which is the same defect
this round opened with, recorded here rather than repeated silently.

The owner's reading, verbatim and dated, with the counts taken afterwards in that order:
`.claude/work/2026-08-18_02_register-track-d/owner-reading-2026-08-18.md`.
