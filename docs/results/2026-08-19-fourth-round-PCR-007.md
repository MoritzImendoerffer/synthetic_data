# The fourth round: a whole report under the rebuilt apparatus, preferred blind — and the author that fetched the counters itself

**2026-08-19.** Work unit `2026-08-19_01_fourth-round-one-document`, TASK-001 to TASK-005. Proposal
[`docs/next/register-from-four-sources.md`](../next/register-from-four-sources.md), its last
paragraph. Decisions **D5 = `PCR-007`** (assumed, not overruled) and **D6 = PASS**, settled by the
project owner on 2026-08-19.

The probe ([`2026-08-19-apparatus-probe.md`](2026-08-19-apparatus-probe.md)) showed on two
subsections that the author-facing apparatus, not the model, produced the rejected prose. This round
asked the question the proposal left open: does a **whole document** written under the rebuilt
apparatus read as a paper? One document, `PCR-007` (Cation Exchange, a full DoE report, never read
by the owner, no registered discrepancy), one agent, one pass, `authoring/RUNNER.md` as rebuilt.

## 1. The regime

| | the shipped `PCR-007` (round zero) | the new `PCR-007` |
|---|---|---|
| author's inputs | the 2026-08 pilot regime: 29k words, 22 counters printed back, per-section obligations | **21,403 words**: the brief with the step's mechanism (§2b), `section_plan.yaml` as structure, `STORY_BIBLE.md`, the 122-line guide, `REGISTER_EXEMPLAR.md`; no counter, no obligation, no grep list |
| what the author ran on its draft | `check_render` with the full style table printed | `check_render` only — five gated tics, pass/fail |
| pipeline | gate → promote | gate → **one content-review cycle** (four questions, fresh judge, one return to the same author) → reading |
| model | `claude-opus-5` | the same harness override (`opus`); the run-2 agent self-reported "Opus 4.5", run 1 "Opus 5" — recorded as self-reports |
| size | 51 pp, 439 sentences, 10,677 words | 50 pp, 482 sentences, 10,702 words, 35 chunks, 226 inline expressions, 0 `<<NEEDS>>`, no missing glyph |

The launch prompt is `procedures/TASK-002.md` — the RUNNER's own invocation line and nothing more,
because the RUNNER as rebuilt is what was under test.

## 2. What was found on the way: run 1 fetched the reviewer's table

The first agent wrote a complete 47-page report, and at its 72nd command ran
`check_style.py --review` on its own draft — unprompted — after reading `check_style.py`'s source;
it then listed every sentence with its word count, wrote a "reflow" script and nine edit scripts,
and revised until the advisory rows sat inside the source bands (its own report: `, so ` 8.6 →
0.2 %, `, and `+clause 16.0 → 3.1 %). **An autonomous author with the reviewer's tool in reach will
use it unasked.** That draft was set aside (`PCR-007_cex.DRAFT.run1-selfmeasured.qmd`, with the
commands in `run1-self-measurement-commands.md`) and never shown to the owner; `RUNNER.md` step 3 now
says the author runs `check_render` and nothing else on its draft; run 2, same prompt, stayed inside
the regime (transcript audited: no `--review`, no listing, no rewrite script; one `--report | head -6`
for the counts the prompt asked for, which prints gated rows only).

Other things the round surfaced: two hard failures the agent fixed itself (an assumed scalar name;
the banned phrase "That is the reason"); Quarto's PDF pass rejects mixed-case crossref ids
(`tbl-appA`) that the docx pass accepts; `dna_lrv` / `leached_pa_lrv` have no named helper and were
pulled through `CFG.unit_op(UO).model`.

## 3. The content review, one cycle

Fresh judge, the four questions, the draft PDF, nothing else (`content-review-PCR-007-draft.md`):

| | run 1 (as authored) | run 2 (after one return to the author) |
|---|---|---|
| Q1 causal verb without cause/direction in its clause | ~15, plus *governs* in four senses | **7** mechanism-shaped (+17 documentary uses the judge called sound) |
| Q2 coinages | 10 (*handle*, *binding attribute*, *assurance factor*, *buys back*, *a plane with twist*, …) | **4 + 2 weak**, none of run 1's (*identity-controlled*, *verification-qualified*, *quality-linked parameters*, *instrumented decision*) |
| Q3 not deniable alone | 14 | **1** clear, 2 borderline — "all 22 other sentences of §5.4 make directional, species-named claims" |
| Q4 files its own finding | ~24 + a four-times "n bounds apply" frame | **11** |

The author changed every named sentence and nothing else (two referential fixes the rewrites forced),
§5.4 end to end, 493 → 482 sentences. By the checklist's letter the draft was still "not promotable
on content" after one cycle; the plan sent it to the reading anyway, once, and forbade a second cycle
(it would tune the draft to the judge). The reading is the test.

## 4. The reading, verbatim

`A.pdf` = the shipped report, `B.pdf` = the new one; key drawn before authoring, opened after the
reading by checksum (`owner-reading-2026-08-19.md`). Suggested subset: Executive summary; Results, all
four subsections; Design space; Discussion.

> B is clearly bette to read. A couple of examples from A which read like machine generated: Yield is
> a process performance response and carries no quality claim, so that limitation does not touch the
> acceptance argument in Section 6.; The aggregate coefficients in Table 5.6 confirm the screening
> picture and sharpen it.; The aggregate coefficients in Table 5.6 confirm the screening picture and
> sharpen it.; The host cell protein coefficients in Table 5.7 reproduce the two dominant main effects
> and the protein load interaction with conductivity, and they add a second interaction that the
> screening block did not resolve.; B reads more like a paper.

Rule, fixed before the document was written: PASS iff the new document is judged the better text and
fewer than five sentences are quoted from it. Better: yes. Quoted from the new: 0 (three distinct from
the shipped, each found once in the shipped `.qmd` and never in the new). **PASS.** The owner had read
neither version before.

## 5. What the counts say

`measure_apparatus.py` over the shipped and the new `.qmd` (`measure_after_PCR-007.txt`), sources in
brackets, per 100 sentences unless marked; the probe's numbers from its page for comparison.

### 5a. What moved with the reading — the same family as in the probe

| | sources | shipped (439 sent.) | **new (482 sent.)** | the probe (90 sent.) |
|---|---|---|---|---|
| `, which` | 0.6–2.4 | 10.5 (46) | **5.8 (28)** | 5.6 |
| all trailing relatives | 1.2–3.0 | 11.9 (52) | **6.6 (32)** | 6.7 |
| `acts on / acts through` | 0 | 2.05 (9) | **0.41 (2)** | 3.3 |
| `governs` / `sets <noun>` | 0 | 2.05 (9) | **0.62 (3)** | 1.1 |
| `behaves as` | 0 | 0.23 (1) | **0** | 0 |
| copula main verb | 13–26 | 31.1 | **24.6** | 27.3 |

The trailing relative halved and the mechanism frames fell four- to five-fold, with no rule about
either in anything the author read — and the new `PCR-007` lands where the probe landed (5.8 vs 5.6
on `, which`, 6.6 vs 6.7 on trailing relatives), on a whole report.

### 5b. What did not move, and the reader did not mind — again

| | sources | shipped | **new** |
|---|---|---|---|
| mid-sentence `, so ` | 0.1–0.4 | 10.3 | **11.0** |
| `, and ` + second clause (regex / parser) | 1.1–3.4 / 1.0–3.4 | 21.6 / 26.5 | **14.9 / 20.3** |
| opens with a connective | 3.7–6.1 | 0.7 | **0.0** |
| passive construction | 57–64 | 48.8 | **48.9** |
| topic chaining | 56–62 | 37.2 | **39.5** |
| `its` per 1k words | 0.27–0.40 | 5.81 | **6.26** |
| staccato (sentences in a run of 3+ short) | 0.4–3.9 | 0.0 | **3.9** |

Every measure rounds one to three set as a target is at its round-zero level or beyond in the text
the owner preferred "clearly". This is the probe's §3b finding reproduced on a whole report: those
measures never tracked the reader's judgement.

### 5c. The gate, and the reviewer's table

Both pass the five-tic gate (`check_style_after_PCR-007.txt`). Under `--review` the new document sits
outside the advisory band on two rows — parentheses 2.2 per 1k (floor 3.0) and "rather than" 1.9 per
1k (ceiling 0.8) — and inside on length (mean 22.2, median 21, 3.7 % over 40, 27.2 % under 15, all
within the sources' union). Had the length bands still been gated, this document would have passed
them; had "rather than" still been gated (it was, until 2026-08-19), it would have failed.

## 6. What this settles and what it does not

Settles: a whole DoE report written under `RUNNER.md` as rebuilt — one agent, facts + mechanism +
a positive guide + the exemplar, no counter — plus one content-review cycle, is preferred blind over
the shipped one by the owner, with no sentence quoted from it; the new `PCR-007` is promoted
(TASK-006/007). And the RUNNER gained the sentence it was missing: the author does not fetch the
reviewer's table.

Does not settle: whether the remaining documents follow (the owner's next call); whether the
content review should be allowed a second cycle (one left a residue the judge could still name,
and the owner's reading did not reach it); whether the exemplar helped or hurt (it was in this
time, out in the probe; both passed); what produced the model self-report difference between the
two runs.

## 7. Verification

```bash
U=.claude/work/2026-08-19_01_fourth-round-one-document
P=.claude/work/2026-08-18_03_author-facing-apparatus

md5sum $U/A.pdf $U/B.pdf pc_package/PCR-007_cex.pdf $U/PCR-007_cex.DRAFT.run2-post-review.pdf
uv run --extra discourse python $P/measure_apparatus.py \
    pc_package/PCR-007_cex.qmd $U/PCR-007_cex.DRAFT.run2-post-review.qmd   # §5 (run before promotion: the DRAFT was at pc_package/PCR-007_cex.DRAFT.qmd)
uv run python authoring/check_style.py --review pc_package/PCR-007_cex.qmd      # §5c
grep -n "check_style.py --review" $U/run1-self-measurement-commands.md        # §2
```

After TASK-006 the promoted document is `pc_package/PCR-007_cex.qmd` and the shipped round-zero
text is in git history at `4531668`.
