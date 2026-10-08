# Procedure — revise ONE pilot document for the owner's comments of 2026-10-08

The four pilot documents (INV-001, PCMP-001, PCP-005, PCR-005) were authored before the owner read
them. The owner's comments (`docs/pm/decisions/rev2-pilot-reading.md`, both the comment block and
the two decision tables at the bottom) changed the machinery. This procedure revises each document
once, by one fresh agent, against an explicit list of required changes. The review cycle is the one
of `AUTHOR-A-DOCUMENT.md` §4 (seven questions, including readability), followed by one factual pass.

Order: PCMP-001 and INV-001 first (in parallel), then PCP-005 (reads the revised PCMP-001 PDF), then
PCR-005 (reads both revised plans' PDFs).

## 1. Inputs

```bash
uv run python authoring/build_brief.py <DOC>
cp pc_package/<DOC>_<uokey>.qmd pc_package/<DOC>_<uokey>.DRAFT.qmd
```

The DRAFT is the shipped document. The agent edits the DRAFT only. The shipped `.qmd` stays in place
until the review passes; then the DRAFT replaces it.

## 2. The launch prompt (ONE agent, model `opus`, fresh context)

> Revise `<DOC>` (<Title>), Version 2.0, in `pc_package/<DOC>_<uokey>.DRAFT.qmd`. The draft is the
> document as it stood before its owner read it. The owner's comments changed the rules and some
> of the data machinery, and the draft must now be brought into line with them. You are its author
> for this revision: change what the list below requires, and leave alone what it does not touch,
> except where the readability rule makes you rewrite a sentence.
>
> Read, and read nothing else for facts or voice: `docs/pm/decisions/rev2-pilot-reading.md` (the
> owner's comments and the decisions taken on them), `authoring/out/<DOC>.brief.md` (every number
> comes from here through the helper inventory, and §4c lists the complex tables to carry),
> `authoring/section_plan.yaml`, `authoring/STORY_BIBLE.md` (§9b is the Version 2.0 story),
> `authoring/WRITING_GUIDE.md` (rule 11 is new) and `authoring/REGISTER_EXEMPLAR.md`.
> `pc_package/_pcpkg.py`, `pc_package/doe_report.py` and `pc_package/tables.py` may be read for
> function signatures and docstrings. <READS> Do not open any other `pc_package/*.qmd`,
> `authoring/rhetorical/` or `authoring/history/`.
>
> Required changes:
> <CHANGES>
>
> In every section, apply WRITING_GUIDE rule 11: a reader who knows the field but has not just read
> the paragraph before must understand each sentence on its own. Name the thing, not its code.
> Where a code is needed, give the name with it. Rewrite any sentence whose subject is an abstract
> stand-in for what was done or found. The owner's two examples are in the comments file.
>
> The data changed since the draft was written (widened and tightened criteria, offsets applied to
> every judgement, a revised verification table). A sentence whose deciding word (met, not met,
> all, none, wider, narrower, within, outside) was typed may now be false. Every such word must be
> computed in the setup chunk or asserted there (WRITING_GUIDE §3). Check every one.
>
> Every value is an inline `{python}` expression or a helper call. A value with no helper becomes
> `<<NEEDS: …>>`, never a typed number. Gate as you go with
> `uv run python authoring/check_render.py pc_package/<DOC>_<uokey>.DRAFT.qmd --render`, and fix
> what it reports yourself, in this context. When it passes, render the pdf:
> `cd pc_package && PATH="$PWD/../.venv/bin:$PATH" quarto render <DOC>_<uokey>.DRAFT.qmd --to pdf`
> and the docx (`--to docx`). Look at every complex table in the pdf once (`pdftoppm` a page to
> png and read it) and fix a table you call wrongly.
>
> Report: which model you are, the list of required changes with where each was made, how many
> `check_render` passes you needed, the pdf result, and any `<<NEEDS:>>` left (there should be
> none).
>
> The repository root is /home/moritz/github_repos/synthetic_data; run every command from there.

## 3. Required changes per document (`<CHANGES>`)

Common to all four: the front matter is already converted (page breaks, revision table, the
abbreviations as `abbreviations_table([...])`). Keep it, and add or remove abbreviation pairs as the
text now uses them.

**PCMP-001**
1. Viral clearance is judged at the worst case: the mean predicted log reduction with the other
   parameters at the least favourable combination of their NOR low, set-point and NOR high
   (`doe_report.decision_statistic`). The draft says the mean. Change the statement and its reason.
2. The widening rule replaces "Data may tighten a criterion and may never loosen it". Verification
   tightens a criterion where a step does worse within its NOR than the platform worst case. It
   widens a criterion only where the 95 % confidence bound of the A-Mab worst case beats the platform
   value, and then the bound, never the point prediction, replaces the platform value. The report
   that relies on a widened criterion gives the argument. State that the rule is set here, before
   any report used it, which is what distinguishes it from the Version 1.0 criteria fitted to data.
   `T.iac_derivation()` and `T.worst_case_verification()` now mark widened rows.
3. Scale-down qualification is by offsets, not equivalence (STORY_BIBLE §9b, section_plan
   `sdm_strategy` and `acceptance_framework`). State the rule once: offset = scale-down mean minus
   manufacturing mean, with its 90 % confidence interval (config `analytics.sdm.offset_ci`); every
   judgement against a criterion subtracts it, so results are stated at manufacturing scale; the
   model is qualified for an output when its conclusion over the NOR is the same with the offset at
   either end of the interval; an output with no criterion has its offset recorded only.
4. Thresholds: add the significance level for model terms (`THRESHOLDS["effect_alpha"]` or the
   config) where the statistical approach names one.
5. Readability (rule 11) throughout.

**INV-001**
1. Table 4.4 is now `T.calibration_windows()` (merged equipment rows). It is already in the draft.
   Check that the prose around it still matches it.
2. The scope paragraph that cites DEV-005-03 is now wrong. The six supplementary set-point runs of
   S-PA-SDM2 were made to narrow the confidence interval of the offset for pool host cell protein.
   PCR-005 records them as a discrepancy from the plan (PD-005-01), not as a deviation. The
   variables `dev_005_03_*` no longer exist; the run counts come from the data
   (`csv("sdm_qualification.csv")`, config `analytics.sdm`).
3. Where the investigation names the rules that replaced the Version 1.0 practice (corrective
   actions, the a priori criteria), mention the widening rule and the offset rule as PCMP-001
   Version 2.0 states them. Keep the dates consistent: the investigation closed before PCMP-001
   Version 2.0 took effect. Say "PCMP-001 Version 2.0 states", not that the investigation set them.
4. Viral clearance is now judged at the worst case (see PCMP-001 item 1). Any statement of the XMuLV
   clearance of low-pH inactivation at a NOR corner must be computed, and its wording must follow it.
5. Readability (rule 11). The owner's two examples are both in this document: "The safety factor
   stood in for the worst case of downstream performance without being derived from it" and "The
   viral clearance criteria of R3 have the same weakness". Rewrite both, and every sentence like
   them, so that each names what it refers to.

**PCP-005**
1. Scale-down qualification by offsets replaces the equivalence test and its margin, in the
   qualification section, the acceptance criteria (criterion 1) and the risks and assumptions.
   Point to PCMP-001 for the rule.
2. The intermediate acceptance criteria for this step now include widened values. The plan states
   the criteria in force and the rule by which verification may tighten or widen them (PCMP-001).
3. Readability (rule 11).

**PCR-005**
1. Scale-down qualification by offsets replaces the equivalence test throughout (methods, results,
   F1, discussion, conclusions). Carry `T.sdm_offsets(["protein_a"])` and, for the discrepancy,
   `T.sdm_offsets(["protein_a"], studies=["S-PA-SDM"], label="tbl-sdm-offsets-planned")`. The
   qualification conclusion is computed (`D.offset_qualification`). Leached Protein A is lower in
   the scale-down model. Under the offset rule this is the offset of that output, and its cause (the
   longer load hold at scale) is given once. The draft's own TOST code and the "equivalence margin"
   are retired.
2. DEV-005-03 is gone. The six supplementary runs are PD-005-01, a discrepancy from the plan
   (`discrepancy_register(DOC)`, `PLAN_DISCREPANCIES`). The section becomes "Deviations and
   discrepancies from the plan". Keep the words apart: a deviation is a departure from an approved
   procedure or a GMP requirement, or an unplanned event in execution, and a discrepancy from the
   plan is work the plan did not foresee. State what was planned, what was done, why, and that the
   conclusion is the same on the three planned runs alone (computed from the planned-runs table).
3. The pool host cell protein criterion is now widened (`D.iac_table(UO)`, basis "widened on
   verification"). Give the argument: which downstream steps' clearance supports it, at which
   confidence bound (`D.iac_verification`, `T.worst_case_verification`), and that the rule was stated
   in PCMP-001 before this report used it. Then say once, plainly, that a criterion wider than the
   Version 1.0 limit is not a loosening of an approved criterion (STORY_BIBLE §9b).
4. Every result judged against a criterion is now at manufacturing scale (the offset is subtracted).
   PAR, design space and the outputs-against-criteria table changed. Every deciding word computed.
5. Readability (rule 11).

## 4. Review

As `AUTHOR-A-DOCUMENT.md` §4 (seven questions). Run 1 by a fresh judge; flagged sentences go back to
the SAME revision agent once; run 2 by a second fresh judge. Then one factual pass: a fresh agent
checks every number-bearing sentence against the tables of the same PDF and against the brief.

## 5. After the review

```bash
mv pc_package/<DOC>_<uokey>.DRAFT.qmd pc_package/<DOC>_<uokey>.qmd
# render both formats, then rebuild that document's annex and re-anchor its quotes
```
