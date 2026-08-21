# One-pass authoring — handoff

Pick-up notes for a fresh Claude Code session. Assume no prior conversation context;
everything needed is here or linked.

**Status: the corpus is finished.** All 20 documents are authored, rendered, annexed and
grounded, on `main`. This file explains how it was built and what to respect when changing
it. It is not a build list — do not follow it top to bottom and re-author a document that
already exists.

---

## 1. The decision this implements

We are replacing the two-pass **additive densification** harness (`ema_docgen/`)
with **one-pass, full-depth authoring, report by report**. No backward
compatibility with the minimal documents is required.

Why the pivot (so you don't re-litigate it):

- `ema_docgen`'s densify-a-minimal-doc-then-splice approach is brittle: many
  components (docspec ↔ factpack ↔ helper names ↔ splice ↔ ledger) coupled by
  string convention rather than gates, and the tool shipped with real bugs
  (it had never been run).
- The first full-depth one-pass reports proved that a single agent can produce the target
  length and structure. One pass can produce the target.
- The additive approach's headline advantage — a matched minimal/full pair with
  identical ground truth (a length ablation) — is a *bonus research artifact*,
  not the stated goal, and the annexes are **generated**
  (`pc_package/build_ground_truth.py`), so rebuilding them is cheap. The minimal docs
  remain recoverable from git history, so the trade is reversible, not lossy.

Keep two things from the two-pass design: **numeral enforcement** (every number from
the model, never typed) and vigilance against **uniform prose**. But the architecture
rule is **one document is written by one agent**, so uniformity is handled by the
writing guide's deliberate per-section register variation — *not* by isolating section
contexts. A single author is also what makes the document-scale arc, cross-references
and coreference/restatement work; splitting sections is what forced `ema_docgen`'s
brittle ledger.

`ema_docgen/` stays in the repo for now; the one-pass system supersedes only its
*densification layer*. Reused from it / the wider repo: the single source of truth
(`config/parameters.yaml` → `amab_process/` → `outputs/`), the `_pcpkg.py` /
`doe_report.py` helpers, the seeded deviation facts, and the numeral lint
(`ema_docgen/scripts/lint_numerals.py`).

---

## 2. Target architecture (the one-pass build loop)

```
per report <DOC> (e.g. PCR-003):
  1. build_brief.py <DOC>   -> authoring/out/<DOC>.brief.md   (grounded facts + helper inventory)
  2. instantiate authoring/template.qmd -> pc_package/<DOC>_<uokey>.qmd
  3. ONE agent authors the whole document, in section order, holding it all in one context.
        bound inputs: WRITING_GUIDE.md + <DOC>.brief.md + section_plan.yaml
                    + REGISTER_EXEMPLAR.md (voice) + STORY_BIBLE.md (world canon)
        writes the body into the template scaffold; all numbers = inline exprs
  4. gate:  check_render.py --render   (dry eval + numeral advisory + real quarto render)
  5. annex (separate, deliberate step): extend build_ground_truth.py, then validate_annex + check_grounding
```

**No first-pass `.qmd` is a runtime input.** Authoring depends only on config → model
→ `outputs/`, the `_pcpkg`/`doe_report` helpers, and the `authoring/` artifacts. The
corpus reports are prior knowledge, distilled once into `authoring/`.
`authoring/check_blank_repo.sh` proves independence: it moves every `pc_package/*.qmd`
aside and runs the pipeline on a generated probe.

**One document = one agent.** The single author gives the arc, cross-references and
restatement. The annex is authored **from the final text** (build-then-annex), which is
why one-pass makes span-grounding trivially satisfiable. Note the corollary
(review finding): build-then-annex grounds *text ↔ annex*, not *text ↔ model* — both
derive from the same author — so the real correctness anchor is the brief's **helper
inventory** (concept → exact expression). Keep it precise.

---

## 3. Status

**Done (this session)** — the distillation artifacts + infra, all under `authoring/`:
- `WRITING_GUIDE.md` — the writing standard (read first).
- `STORY_BIBLE.md` — world canon + grounding map (fact → helper) + campaign storyline.
- `REGISTER_EXEMPLAR.md` — verbatim passages from the published human sources (voice).
- `section_plan.yaml` — machine-readable outlines: `report_doe`, `report_nondoe`, `plan`,
  each section with scaffold / register / rigor / per-section instructions.
- `template.qmd` — the standard scaffold (instantiated into `pc_package/<DOC>_<uokey>.qmd`).
- `build_brief.py` → `authoring/out/<DOC>.brief.md` — grounded facts + helper inventory
  (config→model→helpers only; auto-detects a superseded study).
- `check_render.py` — namespace-accurate dry gate (execs chunks + evals inline exprs in
  one namespace) + `<<NEEDS:>>` scan + numeral lint (advisory; `--strict-numerals` to gate)
  + real `quarto render` with `--render`.
- `RUNNER.md` — the one-pass loop (no splice/ledger).
- `check_blank_repo.sh` — static guard + functional blank-repo proof.

**Shipped: the full 20-document corpus, one pass per document.** Every `PCP-00N` / `PCR-00N`
for Steps 3–10, plus `PTP-001`, `RA-001`, `PCMP-001` and `PCMR-001`. Each was authored
end-to-end from the `authoring/` artifacts alone by a single agent, with **every existing
`.qmd` physically moved off disk during generation** so no author could copy a sibling's
voice. All pass the authoring gate and the register gate.

---

## 3a. Perturbations applied to the model and tooling during the corpus build

Everything below changed the corpus or the machinery *outside* the authoring loop. Recorded
here because each one alters what documents say or how they are checked, and because several
were found by authors refusing to write something incoherent — which is the grounding rule
working as intended.

**Model / world-canon changes (change what documents state).**

| Change | Effect |
|---|---|
| `config`: bioreactor `do`, `medium_conc`, `feed_vol` `study: multivariate` → `univariate` | They are factors of no design. Bioreactor now reads 5 multivariate / 4 univariate; campaign totals 22 / 15 (were 25 / 12). |
| `outputs/data/parameter_classification.csv` regenerated | Was stale against the config above. See the post-mortem below. |
| **`PCP-003` and `PCR-003` re-authored in one pass each, 2026-08-17** | The register pilot. Both were rewritten from the amended guide, exemplar and brief; neither agent read the other's draft or any sibling `.qmd`. What they *state* is unchanged in substance — both registered discrepancies survived and were re-verified — but almost every sentence is new, so 80 annex spans had to be re-anchored (24 of `PCP-003`'s 105 quotes, 56 of `PCR-003`'s 177, of which 34 were the curated rhetorical layer). The corpus is now split 2-of-20 on register until the remaining eighteen follow. Measurements: [`docs/results/2026-08-17-register-pilot.md`](../docs/results/2026-08-17-register-pilot.md). |
| **`PCP-003` and `PCR-003` re-authored a second time, 2026-08-18** | Register round two. Same rule: one agent each, one pass, neither reading the other's draft or any sibling `.qmd`. What they state is unchanged in substance and both registered discrepancies survived again (D-001's wording moved, so `discrepancies.yaml` now carries the live sentence). Re-anchoring cost **44 quote instances across the pair** (21 of `PCP-003`'s 105, 23 of `PCR-003`'s 177) from 37 edited strings, against 80 in round one — every table-row quote survived untouched, because the row builders rebuild the row from the DataFrame the document renders. The curated rhetorical layer needed 33 of its 35 spans re-cut and still carries 35. The corpus stays split 2-of-20 on register. Measurements: [`docs/results/2026-08-18-register-round-two.md`](../docs/results/2026-08-18-register-round-two.md). |
| **`PCR-003` re-authored a third time, 2026-08-18** | Register round three, **one genre only** by owner decision: `PCP-003` was held at round two as the control and is untouched. Same rule again — one agent, one pass, no sibling `.qmd` and not the rhetorical spans. What it states is unchanged in substance and D-002 survived verbatim, so `discrepancies.yaml` and `DISCREPANCIES.md` needed no edit this time. Re-anchoring cost **22 of `PCR-003`'s 177 quotes**, against 23 in round two and 56 in round one; every table-row quote survived untouched again. The curated rhetorical layer needed **all 35** of its spans re-cut, against 33 of 35 in round two, and still carries 35. Two annex report-summary statements had to be **rewritten rather than re-quoted**, because the new report no longer says what they asserted — no gate catches that, only a re-anchoring pass that reads the statement. The document went 59 pp → **56 pp**. The corpus stays split 2-of-20 on register, now at two different rounds. Measurements: [`docs/results/2026-08-18-register-round-three.md`](../docs/results/2026-08-18-register-round-three.md). |
| **All 20 documents re-authored, 2026-08-19 to 2026-08-21** | The fifth round, and the end of the register split: every document in the corpus is now written under the rebuilt apparatus by one fresh-context agent in one pass, from the brief, guide, exemplar and story bible and from no sibling `.qmd`, each with one content-review cycle. Run as a pilot (`PCP-005`) then five batches. What the documents state is unchanged in substance: all four registered-discrepancy carriers touched (`PCP-003`, `PCP-006`, `PCP-008`, `PCP-009`) still carry D-001, and `PCR-003` still carries D-002. Re-anchoring cost **52 quotes for B4** (`PCP-003`, `PCP-007`) and **342 for B5** (`PTP-001`, `PCMP-001`, `RA-001`, `PCMR-001`), with **all 32** of `PCMR-001`'s rhetorical spans re-cut. Final state **2089/2089 quotes grounded across 20 annexes**, 20/20 valid, 0 weak anchors. Corpus-wide the passive rate fell 56.0 → 49.8 %, `, and `+clause 26.8 → 20.9 %, parenthetical openings 7.0 → 1.8 per 1k words, sentences over 40 words 8.1 → 4.0 %, median sentence 23 → 21 words; the gated tics are at zero. **The round introduced one tic of its own: `rather than` rose 0.0 → 1.8 per 1k words**, named independently by three judges and not fixed. Nine blind readings ran (5 PASS / 4 FAIL), all on B1–B3; the owner declined the B4 and B5 samples, so **eleven of the twenty documents were promoted on the content review and the gates alone**. Measurements: [`docs/results/2026-08-21-fifth-round-batches.md`](../docs/results/2026-08-21-fifth-round-batches.md) and [`docs/results/2026-08-19-fifth-round-PCP-005.md`](../docs/results/2026-08-19-fifth-round-PCP-005.md). |

**Tooling changes (change what is checked or how it renders).**

| Change | Why |
|---|---|
| Unicode font block (`mainfont`/`sansfont`/`monofont`/`mathfont`: DejaVu) added to every document and to `template.qmd` | The LaTeX default font had no glyph for `≥`, `≤` or Unicode sub/superscripts, so PDFs carried **398 missing-glyph boxes across 8 documents**. `≥ 4.93` rendered as `␀ 4.93`, turning a clearance *floor* into a point value. |
| `check_render.py`: new `check_pdf_glyphs` hard gate | Nothing had ever inspected the PDF after rendering, which is why the above shipped unnoticed. |
| `check_style.py`: strip markdown images before measuring | An image caption fused with the preceding sentence (its `!` is not a sentence boundary) and inflated the measured length of both. |
| `_pcpkg.all_sop_table()`: `endswith("SOP_REFS")`, not `"_SOP_REFS"` | The base `SOP_REFS` / `AMV_REFS` lists carry no step prefix, so requiring one silently excluded them and the campaign-wide register omitted **7 SOPs and 1 AMV** — the bioreactor operation procedures, every shared analytical SOP and `AMV-3010`. `PTP-001` and `PCMP-001` rendered an operation SOP for Steps 4–10 and none for Step 3. Found independently by three authors before it was fixed. Fixing it re-rendered those two documents (26 → 27 pp and 23 → 24 pp) and left grounding unchanged, because no annex quote anchors on that table. |
| `authoring/template.qmd`: subtitle parameterised | For the four corpus-level documents `UO_TITLE` **is** "A-Mab Drug Substance", so the old template rendered it twice. All four B5 drafts carried the duplicate; the shipped `PTP-001`, `PCMP-001` and `PCMR-001` did not, so promoting as drafted would have regressed two shipped documents. |
| `authoring/build_brief.py`: surfaces `ra_content` for `RA-001` | `section_plan.yaml` names that module as the content source for the risk assessment and the helper inventory never listed it, so `RA-001`'s author had to find it unaided. |
| `check_style.py`: sentence-length and parenthesis bands made **two-sided** | One-sided caps let the first regeneration over-correct into staccato: 17-word mean, 41 % of sentences under 15 words, parentheses near zero. |
| `doe_report`: public `predict` / `to_coded` / `to_natural` / `meets_acceptance` / `planned_matrix_df` | Authors were reaching into `_predict_points` and re-implementing the responses-stripped design matrix. Missing API, not author error. |
| `ema_docgen/scripts/lint_numerals.py`: allow-file compiled with `re.MULTILINE` | The `^`-anchored ordered-list rule never matched, so every numbered list was flagged. |
| `tests/test_config.py`: new file, 11 tests | Config↔DoE invariants, plus **CSV↔config agreement** (see post-mortem). |
| `build_ground_truth.py`: weak claims and rhetorical spans skip/fail on mismatch | A stale curated layer used to degrade silently; a dropped rhetorical span is now a hard failure. |
| **`scripts/extract_sources.py`: two published sources → four** (2026-08-16) | `refs/text/` gained `ispe_tt.txt` and `ispe_pv.txt` beside `amab.txt` and `pda60.txt`. Neither previously extracted source is a *plan*, and 10 of 20 documents are plans. Each source needs its own boilerplate filter: unfiltered, the ISPE per-page DRM footer put "under 15 words" at 41.2 % against a human band of 15–32 %; filtered it is 19.5 %. The project owner permitted quoting both ISPE guides, which commits text watermarked "for personal use only" to `refs/text/`. |
| **`check_style.py`: `--selftest` calibrated on four sources, and the `therefore` ceiling removed** (2026-08-16) | The band is now the union of four human sources, so `mean_len` went to 30.5, `pct_over_40` to 21.5 and `pct_over_55` to 9.5 to admit ISPE PV, whose extraction fuses list items into pseudo-sentences. **Write to the per-source column in `WRITING_GUIDE.md` §4a, not to the edge.** The cap on `therefore` is gone: it was the only connective still in service, so a ceiling on it pushed down on the last one left. The nine connectives are now counted and printed as a diagnostic that fails nothing. |
| **`WRITING_GUIDE.md` §2c/§2d/§2d bis amended** (2026-08-16/17) | "One paragraph, one point" and "one sentence, one point" were read as forbidding a claim beside its counter-consideration, and the corpus complied: not one "However" in ~30,000 words. Both now keep one point as the default and name one licensed exception, with four shapes and seven verbatim source examples. §2d states the given-new rule with three worked corrections; §2d bis states the possessive rule with its measured table. **The pilot measured what this bought**: see the results page. Four ✗ examples quote `PCP-003`/`PCR-003` as they stood before 2026-08-17 and are labelled with that date. |
| **`authoring/discrepancies.yaml` + brief §5c: the discrepancy carrier** (2026-08-17) | A registered discrepancy is a property of *prose*, so re-authoring a document silently deletes one — while `DISCREPANCIES.md` goes on calling the item open and no gate notices, because `check_grounding.py` inspects `SourceReference.quote` and never a description. The brief now quotes the registered sentence verbatim **before** the document is written, for all 20 documents (8 with an assignment, 12 empty). This is **not** the weak-claims layer and must never become it: a registered discrepancy is labelled nowhere, and `weak_claims` is still empty in 20/20 annexes. |
| **`check_style.py`: five tics gate, the rest is the reviewer's** (2026-08-19) | `LIMITS` split into `GATED` (em-dash, semicolon, colon, bold, coined compound, plus `BANNED`) and `ADVISORY` (the five length rows, `paren`, `rather_than`, and the clause-packing family). `evaluate()` fails on GATED only; `--selftest` still asserts the union on all four sources; `--review` prints the advisory table for a **reviewer** and the author sees pass/fail on the tics and nothing else. No band edge moved. Why, measured: the section the owner preferred blind on 2026-08-19 **failed** the gate as it stood (`pct_over_40` 1.1 vs floor 3.0, `rather than` 1.6 vs 0.8) and the shipped section it beat passed every row; and every measure rounds one to three had gated or printed sat at or beyond round-zero in the preferred text. A measure printed back to the author is a target, not a signal. `check_render.py` prints only the gated rows. `tests/test_style.py::test_limits_split` pins 5 / 7 / 12 in the baseline row order. Measurements: [`docs/results/2026-08-19-apparatus-probe.md`](../docs/results/2026-08-19-apparatus-probe.md). |
| **`section_plan.yaml` is an outline again; the obligations moved to `authoring/REVIEW_CHECKLIST.md`** (2026-08-19) | Every section's `scaffold`, `register` and `rigor` list, and `meta`'s scaffold / register / rigor glossary, are gone; each section keeps its heading, subsections, `pull:` menu, length band and one `covers:` sentence. Each of the eight sentences the owner rejected in `PCR-005` on 2026-08-18 was one of those obligations being *performed* ("is put to no other use in this report" is `explicit_non_claim`). They are now questions a reviewer asks of a finished section, plus a **Content** block of four questions (does the `because` name a cause in its own clause; is every term a term of art; can each mechanism sentence be denied on its own; does any sentence file its own finding) run by a fresh-context judge before promotion — calibrated on the shipped and probe texts, seven of the eight owner-quoted sentences flagged. `RHETORICAL_ANNEX.md` no longer ties span roles to authoring and requires a `mechanistic_warrant` to name a physical cause. |
| **`WRITING_GUIDE.md` replaced by 122 positive lines; the old guide is `authoring/history/WRITING_GUIDE-2026-08-18.md`** (2026-08-19) | Ten rules stated as what to do, the numbers rule kept whole, the five gated tics in a table, and no ✗ example, no percentage, no round history. It passes its own gate, which caught two things in its first draft (bold lead-ins; the banned phrases quoted as examples). The brief carries no counter any more: `build_brief.py --review` emits §5d for the reviewer, and the "rules as substitutions" list is gone from the builder. `REGISTER_EXEMPLAR.md`, `STORY_BIBLE.md`, `template.qmd`, `RUNNER.md`, `CLAUDE.md` point at the new numbering and role. |
| **`authoring/mechanism/<uokey>.yaml`, eight files, emitted as brief §2b** (2026-08-19) | The physical chemistry of every attribute a step sets or clears and every parameter it studies, in the terms of art, written from domain knowledge (the published sources describe what a step does, not why — checked against A-Mab's Protein A section) and read once by the owner (`reviewed_by_owner: 2026-08-19` in all eight). **No number in the prose**, so a reseed cannot stale them: `tests/test_mechanism.py`. Directions are committed only where the chemistry is unambiguous and agrees with the seeded model's sign; elsewhere the pathway is named and the sign left to the data. Until this, nothing supplied the mechanism the reports were asked to explain, and an author given none wrote category labels in its place. The brief prints display names, never the config keys (`do`, `co2`, `ivcc`), on the owner's read. |
| **`measure_trackd.py` → `measure_apparatus.py`, and a baseline-check bug** (2026-08-19) | The Track D measurement script, copied into `2026-08-18_03_author-facing-apparatus` and extended with the trailing-relative family and the mechanism frames per 100 sentences (reproducing results §3 on `, which` 513, all trailing relatives 595, `acts through` 63; not on `follows from the` 14 vs 12 or `governs / sets` 97 vs 108, both printed with the disagreement rather than tuned) and a `--spans` audit (26 `mechanistic_warrant` spans, 7 with a flagged frame). Found on the way: the predecessor's TASK-007 commit had broken its own `--check-baseline` by looking source columns up without the ` (human)` suffix the baseline header carries, so it had compared 340 cells and skipped all four sources as MISS since 2026-08-18 while its outcome recorded 408; fixed in the copy, 408 cells again. |
| **`PCR-007` re-authored in one pass under the rebuilt apparatus, 2026-08-19** | The fourth register round, one document: one agent, `RUNNER.md` as rebuilt (brief with §2b mechanism, section plan as structure, story bible, the 122-line guide, the exemplar; no counter), one content-review cycle (four questions, fresh judge, one return to the same author: Q3 14 → 1, Q4 ~24 → 11, the coinages replaced), then read blind by the owner against the shipped report and preferred "clearly" with no sentence quoted from it (D6 = PASS). What it states is what the data say; `PCR-007` carries no registered discrepancy. Re-anchoring cost **31 of its 110 annex quotes** (cx_report_sections 10, cx_assertions 11, cx_studies 4, CXMETHOD_QUOTE 4, cx_equipment 1, cx_design_spaces 1); every table-row quote rebuilt itself; **all ten report-section statements were read against the new text and three rewritten** (one had claimed "no other step in the train changes the attribute", which the new §8 does not say); the curated rhetorical layer needed **all 33 spans re-cut**, none dropped, no role changed, ten moved section with the argument. Two annex-data corrections in the CEX region (`ds:cex` gains `attr:hcp`; the PAR builder's pool-HCP rows carry their unit via `_par_interval()`). 51 → **50 pp**. Corpus: 2084/2084 grounded, 20/20 valid, `outputs/` untouched. The corpus is now split across registers — `PCR-007` at the rebuilt apparatus, `PCR-003` round three, `PCP-003` round two, `PCP-007`/`PCR-005`/`RA-001` the Track D pilot, fourteen at round zero. Measurements: [`docs/results/2026-08-19-fourth-round-PCR-007.md`](../docs/results/2026-08-19-fourth-round-PCR-007.md). |
| **`RUNNER.md` step 3: the author runs `check_render` and nothing else on its draft** (2026-08-19) | The first `PCR-007` agent, given the RUNNER as rebuilt, ran `check_style.py --review` on its own draft at its 72nd command, unprompted, listed every sentence with its word count and revised nine times toward the advisory bands — its own report: `, so ` 8.6 → 0.2 %. An autonomous author with the reviewer's tool in reach will use it unasked, and "print nothing to the author" is defeated from inside. The draft was set aside unread; the RUNNER now says it in step 3 and step 4 ("never the author, never in the authoring context"); the second run, same prompt, stayed inside the regime. Evidence: `2026-08-19_01_fourth-round-one-document/run1-self-measurement-commands.md`. |
| **`check_style.py`: advisory clause-packing measures** (2026-08-17) | Three counts beside `CONNECTIVES`, printed on every run as one line and added to no `LIMITS` entry: mid-sentence `, so `, sentences opening with one of 21 connectives, and sentences carrying two or more clause coordinators. `--compare` gains the three rows. They are advisory on purpose — a ceiling on `, so ` is met by writing `, and` or a semicolon — so the whole family is printed together and the semicolon ceiling stays. `tests/test_style.py` is the first direct test of `sentences()` and `measure()`. **Known gap:** a sentence with exactly ONE `, and ` joining two clauses is caught by neither the `, so ` count nor the 2+ coordinator count, and that shape runs at 18–23 % of corpus sentences against 1.1–3.4 % in the sources. |
| **`authoring/check_discourse.py` + the optional `discourse` extra** (2026-08-17) | Topic chaining, copula rate and adjunct front field — the three measures a writer cannot self-verify by reading — with denominators and the four source columns, reusing `check_style`'s prose extraction so it reads the text the gate reads. spaCy is an **optional** extra (`uv sync --extra discourse`, mirrored in `requirements-discourse.txt`): without it the script prints one line and exits 0, and `make test`, `make style` and `make corpus` never call it. `--cap` reproduces the notebook's 600/450 sentence caps exactly, cell for cell. |
| **`build_brief.py` §5d and the §1 scale line** (2026-08-17) | §5d prints the discourse targets, the four source columns and **the previous revision's own numbers**, measured live rather than carried as constants. It generates no example sentence, deliberately: a template-generated chain is machine prose handed to the author. §1 tells the author to state the commercial scale through `V["commercial_scale_l"]`, which the round-one `PCR-003` never did. The brief reads a document only through `check_style.measure`, never for content, and `check_blank_repo.sh` still passes. |
| **`WRITING_GUIDE.md` §2d restated as a substitution** (2026-08-17) | The rule was "one sentence, one point" and a ✓ block twelve lines later modelled the exact construction it forbids. §2d now says one argument step per sentence, names the three strings to search a draft for (`, so `, `, and ` carrying a second claim, `, which ` carrying a new claim), and carries Correction 0 built from the sentence the project owner quoted. Also: the referent rule (name the set you count), §2d bis naming the substitution and stating a band, Shape 4's positive example, §4a's two diagnostic rows, §4b on where a connective goes, and `REGISTER_EXEMPLAR.md`'s "The step after the full stop". **Two ✓ blocks had to be fixed beyond the plan's list** — a line-by-line grep cannot see `, so ` broken across a line end. |
| **`check_style.py`: two more advisory counts** (2026-08-18) | `', and '` followed by a clause opener, and mid-sentence `', not '`, printed on the same packing line and gated by nothing. Both are faults the project owner's eye found that no measure counted. **The and-clause regex is a FLOOR**, not the rate: it misses a second clause with a bare-noun subject ("…were carried forward, and osmolality was not"), so the source-versus-corpus gap it reports is if anything understated. The parser half lives in `check_discourse.py`; report both or neither. |
| **`check_discourse.py`: passive rate and the parser and-clause** (2026-08-18) | Counted inside `copula_front()`'s loop, so passive, copula, front field and the and-clause all divide by the same `n` — the sentences with a root and a subject. **The passive is a BAND and never a floor** (sources 54–60 % of all sentences, 57–64 % on that `n`); a floor would push the plan genre the wrong way, since `PCP-003` was already inside it at 55.2 %. Sharing `n` moved the reported PCR-003 figure 34.4 → 35.4 % for the same text, which is a change of denominator and not of prose. |
| **`build_brief.py` §5d: three more rows, and the write-the-passive rule** (2026-08-18) | The brief now prints the two and-clause counts and the passive band back to the author, and `WRITING_GUIDE.md` §2d gained the rule beside Correction 0: a study, a design, a model or a process is never the AGENT of *retain / carry / identify / select*. Round three moved all three measures, so the pattern holds for a third time: what is measured and printed moves, and what is not measured drifts. |

**Post-mortem: the stale-CSV bug (worth reading before touching `config`).** Commit
`641d19a` asserted that `study` is display-only metadata and therefore did not require
regenerating `outputs/`. That was **wrong**: `plan_params()` / `report_params()` render
`parameter_classification.csv`, not `CFG`. The config said `univariate`, the CSV still said
`multivariate`, and the prose was edited to match the config — so the shipped PCP-003 read
"…are assessed univariately (Table 6)" while Table 6 said `multivariate`. The prose edit made
it *worse*: before it, prose and table at least agreed. `tests/test_config.py` passed
throughout, because it read `CFG` directly and never compared against the generated artifact.
The lesson is general: **a config invariant that never looks at the generated file cannot
catch drift into the rendered corpus.** `test_generated_parameter_table_matches_config` now
closes it.

**Annex-layer findings from the re-grounding pass.** All 20 annexes were re-grounded against
the new text (1338/1338 quotes). Re-anchoring surfaced records that were not merely
*unanchored* but **false** — ground truth asserting the opposite of its document, which is
worse than a missing record:

- `PCR-004` asserted turbidity stays within its NOR; the report records DEV-004-02, an
  excursion that exceeded it.
- `PCR-005` asserted the step-yield model is "adequate and predictive" (predicted R² 0.586,
  used descriptively) and that `end_of_pool_collect` does *not* affect pool HCP (it does).
- `PTP-001`, a prospective plan, asserted a drug-substance yield and a parameter
  classification — both characterization outcomes that cannot exist when it is written.
- `PCP-007` asserted a design space over pool aggregate *and* HCP; HCP does not bound it.

**Generic quotes ground while attesting nothing.** Found independently by three agents.
`check_grounding` verifies a quote *exists*, not that it is *specific*: `RA-001` used one
placeholder sentence to anchor 41 separate assertions, and bare spans like "acceptance
criteria" passed trivially. The convention the agents converged on, now the corpus standard:
anchor each per-record assertion on the **rendered table row** carrying the relation, built
from the same DataFrame the document renders, so the span contains both ends. `PCMR-001`'s
`_md_rows` / `_grid_rows` helpers are the reference implementation — note they must reproduce
tabulate's cell wrapping, or a row containing a hyphen-broken cell (`re- assayed`) will not
ground. Tracked as a gate to add.

**Seeded-data defects found but NOT changed** (each is a tracked decision, not an oversight):
the acidic-variants acceptance range is printed as 18–40 but only the ceiling is enforced
(making it two-sided would move the headline min Cpk from 1.51 to 1.03); the three equipment
`cal_due` dates pre-date `EFFECTIVE_DATE`, so calibration reads as overdue while
`calibration_status` says otherwise; and ~~`DEV-005-01` says a buffer was prepared *below* target
at pH 3.38 but is tied to an RSM run whose design target is 3.20~~ — **that third one is fixed**:
`LOT-BUF-5290` is bound to RSM run 23, with the reason recorded at `config/parameters.yaml:559`.
The two live ones are neither registered nor resolved, which is the one state `CLAUDE.md` does not
allow; the argument is in
[`../docs/next/seeded-data-tensions.md`](../docs/next/seeded-data-tensions.md).

**Registered discrepancies (`authoring/DISCREPANCIES.md`).** One finding was promoted from
"defect to fix" to "benchmark item to keep": the PAR analysis holds the other factors at the
design centre while all four affected protocols commit to holding them at their set-points, and
the reports present the result under a column headed "PAR (set-point)". It is a real protocol
deviation, cross-document, and partially masked because midpoint and set-point coincide at
three of the six DoE steps. `doe_report.par_at_setpoint` was renamed to `par_at_design_centre`
so the **code** is honest; the column heading, the plans and the annex field name are left
alone so the **documents** still carry it. Read `DISCREPANCIES.md` before touching any of
them — the rule there is that an unregistered inconsistency is a bug, but removing a
registered one deletes a benchmark item.

**The register correction (important — this is why the reports were rewritten).** The
first-pass reports read as machine-written, and the cause was a feedback loop in the
artifacts themselves: `REGISTER_EXEMPLAR.md` had been distilled *from* `PCR-008_aex.qmd`,
which was itself AI-authored against an early `WRITING_GUIDE.md`. The guide then taught the
voice back to the next author. Measured against the two human sources committed at the time
(PDA TR 60 and A-Mab; two more were added on 2026-08-16 and moved several ceilings up), the
first-pass prose ran to a 34-word mean sentence (human: 23–27), 10–13 em-dashes per 1000
words (PDA TR 60: 1.9; A-Mab: **zero**), 9–15 semicolons per 1000 (human: 2), and coined
compounds like "the quality-attribute-richest characterization in the campaign". What was
done about it:

- `REGISTER_EXEMPLAR.md` is rebuilt entirely from **verbatim** source passages, arranged by
  the reporting job each performs. No corpus report is a source for voice, ever.
  `authoring/check_exemplar_quotes.py` re-verifies every quote against `refs/text/`, so the
  exemplar cannot silently drift into paraphrase. It carried 88 quotes from PDA TR 60 and
  A-Mab; on 2026-08-16 a seven-pattern argument-moves catalogue took it to 120, drawn from
  all four sources, with the two 2023 ISPE Good Practice Guides supplying the plan-genre
  passages that neither original source could.
- `WRITING_GUIDE.md` §4 is a new, measurable register spec with worked corrections taken
  from the superseded prose. Several older rules were softened because they *manufactured*
  the tells: mandatory per-paragraph significance codas, mandatory restatement in fresh
  words (which produced elegant variation), and "length is defensive" (which grew subordinate
  clauses).
- `authoring/check_style.py` is a new **hard gate**, wired into `check_render.py`. Its
  thresholds are calibrated so that **all four** human sources pass `--selftest`, and a source
  missing from `refs/text/` fails rather than being skipped. Rule of thumb: if a threshold
  fails the self-test, the threshold is wrong, not the source.
- **The bands are two-sided, and that was learned the hard way.** The gate shipped with
  sentence length capped but not floored. The first regeneration promptly over-corrected into
  staccato: mean sentence 17 words (human: 24–27), 41 % of sentences under 15 words (human:
  ~20 %), and parentheses almost eliminated (0.6 per 1000 words against ~12 in both sources).
  Prose that is uniformly short is as obviously synthetic as prose that sprawls; it reads like
  a checklist. `mean_len`, `median_len`, `pct_over_40`, `pct_under_15` and `paren` are now
  ranges. When adding any future metric, ask whether an author minimising it produces something
  a human would write — if not, it needs a floor too.
- `refs/text/pda60.txt` is now generated by `scripts/extract_sources.py` alongside `amab.txt`.

**The weak-claim feature is RETIRED.** It planted labeled unsupported claims into a report
*after* authoring. When the reports were re-authored, two of the three PCR-003 claims stopped
being unsupported and became flat contradictions of explicit nearby sentences, because the new
report settles the questions they overreach on (notably its honest galactosylation edge of
failure). That converts the benchmark task from evidence grounding to contradiction detection,
and every gate passes it — including the register gate, since the claims sat at the 46th–68th
percentile of the document's own sentence-length distribution with no style markers at all.
Full reasoning and the condition for reviving it: `authoring/WEAK_CLAIMS.md`. The general rule
it establishes is now in CLAUDE.md: **nothing is added to a document after authoring.**

**Next**

What is open now lives in [`../docs/ROADMAP.md`](../docs/ROADMAP.md), with a proposal per item in
[`../docs/next/`](../docs/next/) and the active epic on
[`../docs/pm/_Board.md`](../docs/pm/_Board.md). This list is kept for the record of what it said.

- ~~**Re-curate the rhetorical layer** (`authoring/rhetorical/PCR-003.spans.yaml`); 34 of 37 spans
  quote superseded text and are dropped with a warning.~~ **Done, and verified 2026-08-16**:
  `build_rhetorical_annex.py --doc PCR-003` writes 35 spans and drops none.
- ~~**PCR-008 rhetorical layer** (neither report has one that matches the current text).~~
  **Done**: PCR-008 carries 25 spans, in `authoring/rhetorical/PCR-008.spans.yaml` since the
  mechanism was unified on 2026-08-18.
- **The remaining plans**, each with its rhetorical layer. Eleven documents still carry none — the
  eight `PCP-00N`, plus `PTP-001`, `RA-001` and `PCMP-001`. ~~and the layer is built two ways~~ —
  one mechanism since 2026-08-18, all of it YAML.
  Proposal: [`../docs/next/rhetorical-layer-coverage.md`](../docs/next/rhetorical-layer-coverage.md).
- Optional, deliberate: if labeled benchmark negatives are wanted again, name them in the
  brief so the single author writes them into the argument in one pass (`WEAK_CLAIMS.md`).
  Proposal: [`../docs/next/weak-claims-branch.md`](../docs/next/weak-claims-branch.md).

---

## 4. Specs / corrections worth carrying forward

- **`build_brief.py` helper inventory is the correctness anchor** (see §2 corollary).
  It enumerates every `_pcpkg`/`doe_report` callable with signature + docstring, the
  structured deviation facts (from `config`), the `dev_*` scalar names, and the CQA/param
  tables. Regenerate after any config/model change.
- **`check_render.py` replicates Quarto's execution model** — one shared namespace, chunks
  then inline exprs in document order. Evaluating inline exprs against a *fresh* import
  would false-NameError on every doc-local variable; do not "fix" it that way.
- **Grounding is NOT an authoring-time gate.** No annex exists when the text is authored;
  the authoring gate is eval + render + no-`<<NEEDS:>>`. `check_grounding.py` runs in the
  *annex* step (step 5), against the rendered `.docx`.
- **Numeral lint is advisory.** The committed corpus itself carries statistical
  conventions (α=0.05, p-thresholds, n, 95% CI) the allow-file deliberately does not
  exempt; the lint flags typed *measurements* to convert to inline exprs, and does not
  hard-fail the gate unless `--strict-numerals`.
- **Deviation prose = Option A** (author writes from the brief's structured facts; the
  register exemplar teaches the moves). Not from the ema_docgen factpack.
- **Weak-claims benchmark feature — RETIRED, do not reinstate the injection step.** See the
  Status section above and `authoring/WEAK_CLAIMS.md`. `weak_claims.yaml` and
  `build_weak_claims_annex.py` are retained as a record and a starting point; nothing reads
  them into a shipped document. `build_ground_truth.py`'s `build_weak_claims()` skips any
  registered claim absent from the document and warns, so "no planted claims" is a clean,
  buildable state.
- **Proven acceptable ranges (PAR).** `doe_report` computes per-CQA×parameter PARs live
  from the fitted RSM (no new outputs). Acceptance = study DS specs, except viral-clearance
  CQAs use a **back-calculated step floor** (cumulative requirement − other steps' credited
  clearance) — `D.acceptance_for(UO, resp)` returns the right criterion. Two flavours:
  `D.par_at_setpoint` (others fixed) and `D.par_nor_propagated` (others varied within NOR by
  seeded Monte-Carlo — the reproducible default; a Bayesian backend can replace
  `_mc_predictive` later). `D.par_table(UO)`, `D.fig_par(UO, resp, D.governing_factor(...))`
  (green-shaded acceptable region). New section `proven_acceptable_ranges` in `section_plan`
  (report_doe + plan). NB: `report_params` "PAR" column is renamed **"Char. range"** — the
  config range is the characterization/knowledge-space range, not a PAR (the PAR is computed).
- **Rhetorical / linguistic-pattern annex layer.** A grounded discourse layer over the
  report text (`authoring/RHETORICAL_ANNEX.md`, `authoring/build_rhetorical_annex.py`,
  curated spans in `authoring/rhetorical/<DOC>.spans.yaml` → `authoring/out/<DOC>.rhetorical.json`).
  Roles: problem_statement, claim, justification, mechanistic_warrant, hedge,
  bounded_conclusion, cross_step_credit, deviation_disposition, deferral, restatement, and
  weak_claim (merged). Relations: `supported_by` (claim←evidence), `restates` (coreference),
  `bounds`. Build-then-annex, curated by an annotator agent and grounded by the builder;
  merges into the GroundTruthAnnex when `build_ground_truth.py` is extended. PCR-003 layer:
  37 spans, 11 argument edges, 3 coreference edges.

Section order + scaffold/register/rigor per section: `authoring/section_plan.yaml`
(the machine-readable form of the CLAUDE.md canonical orders). Length is emergent — the
band is a lint hint, never a target to pad toward.

---

## 5. Environment & commands

- **Scientific stack is under `uv`** (numpy/pandas/scipy/statsmodels missing from system
  python). Always `uv run python …`.
- **Quarto** is present locally (1.10+); render for real via `check_render.py --render`.
  In a cloud env with no quarto, the dry eval + numeral lint still gate.
- Tests: `uv run --with pytest python -m pytest -q tests/` (keep green).
- Regenerate model data: `uv run python scripts/generate_data.py`.
  ⚠ **Output drift:** regenerating in a different library environment shifts the
  DoE/effects CSVs in the deep decimals. The committed `outputs/data/*.csv` are the
  baseline. **`git diff` any `outputs/` change and commit only intended new/changed data**
  (e.g. a new superseded dataset), never drifted `doe_*`/`effects_*` baselines.
- **Rendered `.docx` are git-tracked (21).** While iterating, author under a throwaway
  name (`pc_package/<DOC>_<uokey>.DRAFT.qmd`, whose `.docx` is untracked) so the committed
  baseline does not drift.

---

## 6. Grounding facts for the two documents the method was proved on

These two were the test targets when one-pass authoring was being validated, and they are
still the ones to read first: PCR-003 for structure and depth, PCR-008 for the hardest
narrative in the corpus. Both are built; the facts below are here as orientation, not as a
work order.

**PCR-003 — Production Bioreactor (USP).** key `bioreactor`, step 3. Params:
pH, temperature, co2, osmolality, duration (WC-CPP); do, ivcc, feed_vol (KPP); medium_conc
(GPP). CQAs it SETS: afucosylation, galactosylation, high_mannose, aggregates_hmw,
acidic_variants, hcp, residual_dna. DoE step — 5 CQA responses; the design-space step.
Seeded deviations: DEV-003-01 (pCO2 probe drift; `EQ-BRX-205`; **retained**) and DEV-003-02
(feed-1 under-delivery; `LOT-FED-3120`; **retained**) — both minor, a bounded-impact
argument, *not* a re-executed DoE. See `authoring/out/PCR-003.brief.md`.

**PCR-008 — Anion Exchange.** key `aex`, step 8. Flow-through polish:
SETS the MVM viral-clearance CQA (tightest Cpk); clears XMuLV/HCP/DNA/leached-PA. This is
the step with the **twice-run DoE** (deamidated-load first execution → re-executed on
requalified load) + the UV pool-stop correction. The superseded dataset is seeded and these
deviations live in `config`.

---

## 7. Pointers

- Writing standard: `authoring/WRITING_GUIDE.md`
- World canon + grounding map: `authoring/STORY_BIBLE.md`
- Voice (verbatim human-source passages, no report needed): `authoring/REGISTER_EXEMPLAR.md`
- Section outlines + per-section instructions: `authoring/section_plan.yaml`
- The build loop: `authoring/RUNNER.md`; independence proof: `authoring/check_blank_repo.sh`
- Helpers: `pc_package/_pcpkg.py`, `pc_package/doe_report.py`
- Gates: `authoring/check_render.py`, `ema_docgen/scripts/lint_numerals.py`,
  `pc_package/check_grounding.py` (annex step)
- Source of truth: `config/parameters.yaml` (`deviations:` key); corpus conventions:
  `CLAUDE.md`. Prior two-pass rationale: `ema_docgen/DESIGN.md`.

---

## 8. First action for a fresh session

Every document already exists. What you do first depends on what you are here to do.

**Just orienting.** Read `authoring/WRITING_GUIDE.md`, `authoring/STORY_BIBLE.md`,
`authoring/REGISTER_EXEMPLAR.md` and `authoring/section_plan.yaml`, then read PCR-003 as a
finished example. Confirm the corpus is intact:

```bash
cd pc_package && uv run python build_ground_truth.py && uv run python validate_annex.py \
  && uv run python check_grounding.py
```

**Changing what a document says.** Change `config/parameters.yaml`, run
`make data figures`, and let every document and annex follow. If the *prose* has to change,
re-author the whole document in one pass — never patch a paragraph, because the register gate
measures the document as a whole and a stale annex quote will strand. Then rebuild the annex
and re-anchor any quote the change broke.

**Adding a document.** `uv run python authoring/build_brief.py <DOC>`, instantiate
`authoring/template.qmd`, and have **one agent** author it in section order bound only to the
artifacts above — never to a sibling `.qmd`. Gate with
`uv run python authoring/check_render.py <path> --render`.

**Any time:** `bash authoring/check_blank_repo.sh` proves authoring does not depend on an
existing document.
