# Rev 2: a-priori acceptance criteria, a method change, and tables that look like real ones

**Status:** in progress since 2026-10-08, work unit `2026-10-08_01_rev2-campaign`. Proposed and
decided the same day at the owner's request (decisions below).
Replaces [`seeded-data-tensions.md`](seeded-data-tensions.md), whose two live items are resolved
here.

## The problem

Three things, each checked against the repository on 2026-10-08.

**1. The in-process limits were fitted to the data they judge.** `config/parameters.yaml`
`ipc_limits` was added at analysis time, after PCR-005 showed that a Protein A pool cannot be
judged against a drug-substance limit. Its own comment says why the per-step safety factors differ
(3.2, 4.5, 4.6, 5.0, 6.0, 6.8): "the limit must also sit above that step's own nominal and
design-centre values". So each factor was chosen so that the step passes at its own set-point. The
glycan and acidic-variant limits are `mean + 2.5 sd` of `capability.csv`, which means that the data
being judged set the criterion. The ceilings use the nominal downstream clearance from this
campaign's own data, not a worst case known before the studies ran. None of the criteria is in an
approved protocol. The arbitrary numbers drive findings. For example, PCR-007 §7.3 says the upper
load NOR is "not supported" for aggregate only because 5 % HMW ÷ 5 = 1 % HMW.

**2. The tables are flat.** Every table is `df.to_markdown()`, so the corpus has no two-level header,
no merged cell, no footnote marker and no "n.t." anywhere. Real study reports are full of them, and
a document-parsing benchmark needs them. The owner's reference examples are
`~/Nextcloud/Datasets/doctool/results/2026-09-30-checkpoint-2/messy/` (`messy.tex`, `messy.png`):
- a two-level header;
- batch cells merged over two and three rows;
- a merged "not applicable" cell;
- superscript footnote markers;
- footnote rows inside and below the table;
- one parameter carried on two rows.

**3. The analytical story has no seams.** Each attribute is measured by one method at every step and
in every study. In a real campaign, method fitness differs by matrix and changes during the
campaign.

## Decisions taken (owner, 2026-10-08)

| Question | Decision |
|---|---|
| Story scope | All 20 documents reissued as **Rev 2.0** with a revision history. Today's 20 documents are **frozen as Rev 1.0, superseded**, and kept in the corpus. One **new investigation report** is added. |
| Limit strategy | **Specification-driven intermediate acceptance criteria (IACs)**, derived a priori from the drug-substance specification and worst-case **platform** clearance, with no tuned margin. Non-cleared attributes keep the drug-substance criterion. An integrated Monte-Carlo process model reports P(OOS) at the drug substance. |
| D-001, D-002 | **Kept.** Both are re-planted through the Rev 2 brief. The two seeded-data tensions are **resolved**: acidic variants get a two-sided Cpk, and execution dates are recorded. |
| Authoring rules | **Changed.** A report author may read its paired plan and PCMP-001 for content. Mechanism is confined to the mechanistic-interpretation and Discussion sections. Report conventions are added: revision history, Criterion / Result / Met tables, n.t. and <LOQ. |

## The idea

The story is one that a real campaign tells.
- **The deviation.** QA review of PCMR-001 Rev 1.0 raises a deviation. The acceptance criteria for
  the proven-acceptable-range analysis were set after the data were seen and outside the approved
  protocols.
- **The investigation.** The investigation (new document `INV-001`) finds:
  - the tuned margins;
  - the circular capability limits;
  - the nominal rather than worst-case downstream clearance;
  - the one-sided acidic-variant assessment;
  - the missing execution dates;
  - a separately raised method finding. The CEX fraction study ran SEC and non-reduced CE-SDS side
    by side and showed that SEC LMW is biased high in capture-stage matrices (co-eluting host cell
    protein and leached Protein A ligand), so the fragment data from the Protein A and viral
    inactivation steps cannot be read by SEC.
- **The CAPA.** PCMP-001 Rev 2.0 derives IACs from the drug-substance specification through the
  worst-case clearance of the prior products X-Mab, Y-Mab and Z-Mab. That derivation uses no data
  from the studies it judges, so applying it retrospectively is justified and the justification is
  recorded. Protocols are amended (PCP Rev 2.0). Reports are re-analysed (PCR Rev 2.0). Fragments
  move to nrCE-SDS for every study executed after the method decision. Retained Protein A RSM
  samples are re-tested, and the screening SEC data are kept but footnoted as not used.
- **The repeat.** The anion exchange DoE already has a first execution invalidated by DEV-008-01.
  Its re-execution measures fragments by nrCE-SDS where the first used SEC. One method across the
  train is what makes a step-to-step fragment balance arithmetic.

## What it would take

| Layer | Change |
|---|---|
| Config + model | <ul><li>`fragments_lmw` CQA</li><li>a per-study analytical method assignment with dates</li><li>a SEC matrix-interference model</li><li>execution chronology</li><li>intermediate hold studies (harvest, Protein A pool, VI neutralized pool)</li><li>a CEX fraction comparability study</li><li>`iac:` with platform worst-case clearance replacing `ipc_limits`</li><li>the Rev 1.0 criteria kept as data, so that INV-001 can tabulate old against new</li></ul> New draws on independent RNG streams, so that every existing DoE response stays byte-identical: Rev 1.0 and Rev 2.0 analyse the same experiments. |
| Analysis | `doe_report`: <ul><li>IAC functions</li><li>a PAR judged against IACs</li><li>integrated-model P(OOS)</li><li>verification that observed downstream clearance meets the assumed worst case</li></ul> |
| Tables | `ctable()` in `_pcpkg.py`: <ul><li>one table spec, emitted as an HTML table for DOCX (real `gridSpan`/`vMerge`) and as raw `booktabs`/`multirow` LaTeX for PDF, because pandoc's LaTeX writer collapses spanned tables (tested 2026-10-08)</li><li>`check_grounding` and `row_quotes()` read merged rows</li></ul> |
| Registry | `INV-001` in `DOC_REGISTRY` and in the ID scheme; `pc_package/superseded/rev1/` holding the frozen Rev 1.0 DOCX, PDF and annexes, tagged `corpus-rev1.0` |
| Authoring | <ul><li>`CLAUDE.md`, `WRITING_GUIDE.md`, `REVIEW_CHECKLIST.md`, `section_plan.yaml` and `STORY_BIBLE.md` per the decisions</li><li>`build_brief.py` carries the new facts and tables</li></ul> |
| Corpus | 21 documents authored in one pass each. Pilot: PCP-005 + PCR-005. The owner reads the pilot before the remaining 19. |

## Where the messy tables go

| Table | Features | Documents |
|---|---|---|
| Analytical method by step and study | step merged down; Screening / RSM two-level header; footnotes on the method switch | PCMP-001, PCMR-001, INV-001, each PCR App. D |
| IAC derivation | attribute merged over steps; "not applicable" merged for non-cleared attributes; basis footnotes | PCMP-001, each PCR, INV-001 |
| Rev 1.0 against Rev 2.0 criteria | two-level header Rev 1.0 / Rev 2.0 | INV-001, each revised document's revision section |
| Process parameters | step merged; NOR / PAR with Low / High; merged "not applicable"; one parameter on two rows | PTP-001, PCMR-001 |
| Intermediate hold stability | pool and temperature merged; time-point header; n.t.; method footnotes | PCR-004, PCR-005, PCR-006 |
| DoE results with method sub-columns | HMW (SEC), LMW (SEC), LMW (nrCE-SDS); n.t.; footnotes for deviations and re-assays | PCR appendices |
| SEC against CE-SDS comparability | sample type merged; bias; footnotes | PCR-007, INV-001 |
| Acceptance criterion / result / met | attribute merged | every report |
| Revision history | — | every document |

## Verification

- `outputs/` DoE response columns byte-identical to `corpus-rev1.0` for the same seed (a test).
- No IAC depends on a value in `outputs/` from the study it judges (a test that perturbs the DoE
  outputs and asserts the IACs do not move).
- `make clean && make data figures corpus`: 21/21 annexes valid, every quote grounded with
  `GROUNDING_STRICT_ANCHORS=1`, and no missing glyphs. Each merged table is checked in the PDF by
  eye on the pilot.
- `check_style.py` passes on all 21. The owner reads the pilot pair.

## What it deliberately does not do

It does not change the DoE designs or ranges. Rev 2.0 is a re-analysis of the same experiments plus
the measurements the method decision required. It does not move viral clearance out of the DoE
responses. It does not make Rev 1.0 rebuildable from `main`: the superseded set is a frozen record,
and is regenerated by checking out the tag.

## Open questions

None blocking. The IAC worst-case clearance values are prior-product facts. They are written into
`config/` with a source comment, because they are inputs, not outputs.
