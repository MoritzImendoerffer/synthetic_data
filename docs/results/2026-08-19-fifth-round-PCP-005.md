# The fifth round, pilot: a plan under the rebuilt apparatus, preferred blind on one sentence's evidence

**2026-08-19.** Work unit `2026-08-19_02_fifth-round-plan-then-batches`, TASK-001 to TASK-004.
Proposal [`docs/next/register-from-four-sources.md`](../next/register-from-four-sources.md), its
"what remains" pointer. **D7 = PASS**, settled by the project owner on 2026-08-19.

`PCR-007` (a report) passed blind on 2026-08-19 under `RUNNER.md` as rebuilt
([`2026-08-19-fourth-round-PCR-007.md`](2026-08-19-fourth-round-PCR-007.md)). Half the corpus is
plans — prospective, `plan_params`, no findings, no rhetorical layer, already high on the passive —
and nothing had tested the regime on one. The owner chose `PCP-005` (Protein A, no registered
discrepancy, never read) as the pilot before the batches.

## 1. The regime, unchanged

One agent (`opus`; self-reported Claude Opus 5), one pass, `procedures/AUTHOR-A-DOCUMENT.md`: the
brief with the Protein A mechanism (§2b), the section plan as structure, the story bible, the
122-line guide, the exemplar — **21,415 words**, none a counter. The transcript audit is clean: two
`Read`s and `cat` of the rest, `check_render` the only checker, no sentence listing, no rewrite
script, no other `.qmd`. `check_render` passed on its first pass. 31 pages (the shipped plan is 31
too), 259 sentences / 5,750 words as authored, 262 / 5,785 after the review cycle, 11 chunks, 42
inline expressions, 0 `<<NEEDS>>`, no missing glyph.

## 2. The content review, one cycle

| | run 1 (as authored) | run 2 (after one return to the author) |
|---|---|---|
| Q1 causal verb without cause/direction in its clause | 8 (§4.1's walk through the parameters) | **0** — "every causal claim about the process passes" |
| Q2 coinages | 4 (*assurance factor*, *the undivided ceiling*, *governed attribute / governing parameter*, *carboxylate contacts*) | **0** — "every technical term is standard" |
| Q3 not deniable alone | 3 | **0** — "all 46 sentences of §4.1 make a checkable claim" |
| Q4 files its own finding | 9 | **5** (§4.1 "Characterization confirms and bounds them for this molecule rather than discovering them."; §4.2 "The outcome is a continuum of criticality rather than a binary split (…)."; §7 "It states no outcome, and every criterion below is fixed before the data are generated."; §12 two trailing "rather than taken on trust" / "justifies by mechanism" clauses) |

Three of four clean after one cycle, against `PCR-007` where none of the four was. Not clean by the
checklist's letter (Q4 "the fault present"); it went to the reading as the plan says.

**Found on the way:** *carboxylate contacts*, flagged as a coinage, came from
`authoring/mechanism/protein_a.yaml` (`elution_ph`: "protonating the carboxylate contacts that
remain") through brief §2b. The file says "hydrogen bonds and salt bridges" at ship; the regime is
frozen in the unit and the correction is recorded.

## 3. The reading, verbatim

`A.pdf`/`B.pdf`, key drawn before authoring, no page count printed this time
(`owner-reading-PCP-005-2026-08-19.md`). Suggested subset: Purpose and scope; Prior knowledge;
Study design; Acceptance and decision criteria; Risks and assumptions.

> A reads better. In B, following sentence clearly revealed it's origin: "Three mechanisms frame
> what the study expects to find.

Key: **A was the new plan**; the quoted sentence occurs once in the shipped `.qmd` and never in the
new one — and it is exactly the paragraph-frame the content review's Q4 flags (the shipped text
carries it; the new one shed five like it in its one cycle). Rule: new preferred, 0 < 5 quoted →
**PASS.**

## 4. What the counts say (`measure_after_PCP-005.txt`, `check_style_after_PCP-005.txt`)

Per 100 sentences unless marked; sources in brackets; shipped (192 sentences) → new (262).

| | sources | shipped | **new** | what `PCR-007` did |
|---|---|---|---|---|
| `acts on / acts through` | 0 | 1.56 (3) | **0.38 (1)** | 2.05 → 0.41 |
| `governs` / `sets <noun>` | 0 | 2.08 (4) | **1.15 (3)** | 2.05 → 0.62 |
| `, which` | 0.6–2.4 | 5.7 (11) | **6.9 (18)** | 10.5 → 5.8 |
| all trailing relatives | 1.2–3.0 | 5.7 (11) | **7.6 (20)** | 11.9 → 6.6 |
| mid-sentence `, so ` | 0.1–0.4 | 11.5 | **3.8** | 10.3 → 11.0 |
| `, and ` + second clause (regex / parser) | 1.1–3.4 / 1.0–3.4 | 26.6 / 35.4 | **17.2 / 22.8** | 21.6 → 14.9 / 26.5 → 20.3 |
| opens with a connective | 3.7–6.1 | 0.0 | **0.4** | 0.7 → 0.0 |
| passive construction | 57–64 | 66.7 | **67.7** | 48.8 → 48.9 |
| topic chaining | 56–62 | 30.9 | **34.0** | 37.2 → 39.5 |
| `its` per 1k words | 0.27–0.40 | 8.25 | **6.22** | 5.81 → 6.26 |
| mean sentence length | 24–30 | 24.0 | 22.1 | 24.3 → 22.2 |
| % under 15 words | 16–21 | 16.7 | 29.0 | 20.5 → 27.2 |

Both pass the five-tic gate; under `--review` the new plan sits outside the advisory band on
parentheses (0.2 per 1k, floor 3.0) and "rather than" (2.1, ceiling 0.8) — the same two rows as
`PCR-007`.

**What this adds to the report's result.** The plan started with far fewer mechanism frames than
the report (the shipped `PCP-005` had 3 `acts through` and 11 `, which` in 192 sentences; the
shipped `PCR-007` had 9 and 46 in 439), so there was less to shed and the trailing relative did not
fall — it rose a little. The owner preferred the new plan anyway, on the evidence of one sentence
in the old one that announces its paragraph's shape. Two things hold across both genres: the
reading does not track the round-one-to-three counters (`, so ` fell here and rose in the report;
the passive moved nowhere in either; the owner preferred both), and what the content review's
four questions remove is what the reader notices.

## 5. What this settles and what it does not

Settles: a plan written under the frozen regime plus one review cycle is preferred blind by the
owner; `PCP-005` is promoted (TASK-005, 48 quotes, no spans); the batches run (D7).

Does not settle: whether the trailing relative in plans is worth a question of its own (it rose
6.9 → 7.6 here and nobody minded); what a second review cycle would have removed; the model
self-report question carried from the fourth round (this agent said Opus 5).

## 6. Verification

```bash
U=.claude/work/2026-08-19_02_fifth-round-plan-then-batches
P=.claude/work/2026-08-18_03_author-facing-apparatus
md5sum $U/A.pdf $U/B.pdf $U/PCP-005.DRAFT.post-review.pdf
uv run --extra discourse python $P/measure_apparatus.py pc_package/PCP-005_protein_a.qmd $U/PCP-005.DRAFT.post-review.qmd   # run before promotion against the DRAFT
uv run python authoring/check_style.py --review pc_package/PCP-005_protein_a.qmd
```

After TASK-005 the promoted document is `pc_package/PCP-005_protein_a.qmd`; the shipped round-zero
text is in git history at `40ffaaf`.
