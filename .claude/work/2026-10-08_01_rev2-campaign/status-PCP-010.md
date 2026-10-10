# Status — PCP-010 (UF/DF plan, Version 2.0) authoring

Author: Claude Opus 5.5 (claude-opus-5-5), one-pass, per authoring/RUNNER.md.
Draft: pc_package/PCP-010_ufdf.DRAFT.qmd
Scratch: /tmp/claude-1000/-home-moritz-github-repos-synthetic-data/be14bf3c-e46a-46fd-b419-65482c2add0e/scratchpad/pcp010/

## Inputs read (2026-10-10)
- [x] authoring/RUNNER.md
- [x] authoring/out/PCP-010.brief.md
- [x] authoring/section_plan.yaml (plan)
- [x] authoring/STORY_BIBLE.md
- [x] authoring/WRITING_GUIDE.md
- [x] authoring/REGISTER_EXEMPLAR.md
- [x] procedures/PLAN-LESSONS.md
- [x] data-state-2026-10-09b.md
- [x] helper signatures (_pcpkg, doe_report, tables, ctable) + probes of the data (scratch probe1-4.py)

## Decisions
- Data facts (probed): no IAC row and no criteria_rev1 row for ufdf (assert both); effective_acceptance =
  DS criteria (agg <= 5 upper, acidic 18-40 two-sided), basis "drug substance"; method_plan lmw_in_scope False
  for all UF/DF studies (fragments not measured); sdm_qualification.csv has NO ufdf rows (data gap, flag in
  report); rev1_date(PCP-010)=2026-02-23 < S-UFDF-SDM start 2026-02-25; SDM ends before UNI starts; EQ-TFF-142
  due 2026-04-22, both windows close before; S-UFDF-UNI2 (EQ-TFF-188) is PD-010-01 -> not described.
- Keep V1.0 design: 3 levels (edges + set-point) per parameter, set-point shared; counts computed as
  n_par*n_lev (9), n_par*(n_lev-1) edge (6), n_par set-point runs (3, one per series) -> no typed count.
- SDM: keep V1.0 qualification design (n_scale_down runs vs pilot+commercial record on yield, flux, final conc,
  aggregate change); apply PCMP-001 V2 §7.1 parts 1,2,4; part 3 (decision on RSM) -> plan says it has no rule
  for this step (PLAN-LESSONS rule 9 / bible "plan says it has none"). Acidic variants + buffer exchange not
  compared -> offset unknown, representativeness by mechanism.
- Criteria: DS criteria via PCMP-001 §7.6 (no IAC). Upstream criteria credit UF/DF with no change in aggregate /
  acidic variants / fragments (iac.csv last rows basis DS, added 0) -> state, plus "§7.5 verification needs RSM,
  none planned here". No new rule.
- Changes list: (1) criteria basis, (2) offset qualification replaces equivalence, (3) judgement stats + alpha,
  adequacy/verification n/a, (4) AMD-001 fragments not measured, (5) execution windows + title-block date;
  plus INV-002 changes nothing; studies not foreseen -> PCR-010 discrepancy (generic, UNI2 not named).
- A-Mab case study leaves UF/DF out [@amab2009, p. 86]: say so where expectations are stated (4.1).
- Tables: related_docs_md, T.sop_references(UFDF lists), cqas_by_keys via T.frame (+legend), show(plan_params),
  T.methods_by_study(["ufdf"]), own T.frame tables: SDM outputs, sampling, windows, roles, Appendix A levels.

## Progress
- status file created
- [x] rendered PCMP-001 read (content): UF/DF has no IAC in Table 7.1 -> DS criterion applies (§7.6);
      SDM outputs compared list in §5 does not include UF/DF; §7.1 offset rule; §7.8 fragments nrCE-SDS;
      Table 7.3 UF/DF "no DoE"; Table 5.1 EQ-TFF-142 due 2026-04-22; S-UFDF-SDM/UNI windows.
- [x] frozen Version 1.0 PCP-010 read: design 3 levels x 3 params, set-point x3 shared, 9 runs;
      sampling table (load, pre-DF retentate, DF series cond/pH, final retentate A280/SEC/icIEF, permeate A280);
      §5.5 slope test alpha 0.05, pure error from 3 set-point runs; buffer exchange plateau analysis;
      §7.1 SDM equivalence (alpha 0.05) -> replaced by offset rule (PCMP-001 V2 §7.1);
      §7.2 DS criteria at final retentate; §7.3 decision rules (keep verbatim in substance);
      §7.4 classification; §8 PAR = contiguous span of acceptable levels, 3 bounds; §12 risks (pilot repeat, pool bridging).
- draft v1 written (all sections), running check_render pass 1
- check_render pass 1: all HARD gates OK (numeral lint advisory: identifiers only)
- review fixes after pass 1: §4.1 two routes (mechanical/chemical), §1 clearance wording, tables 5.1/11.1 headers, typed 'two', finding 5/PA3 named, §7.2 double sign
- voice refinements (documents not as deciding agents), counts computed (w(len(CQA_DF)))
- check_render pass 2 (after review fixes): all HARD gates OK
- explicit renders: quarto --to pdf (29 pp) and --to docx OK; check_render pass 3: all HARD gates OK
  (322 sentences, 5930 words of prose per check_render; no <<NEEDS:>>; gated tics all 0.0)
- every table page viewed in the PDF (pp. 9, 11, 14, 15, 16, 18, 24, 25, 28): Tables 3.1, 3.2, 4.1, 5.1, 5.2,
  5.3, 6.1, 10.1, 11.1, A.1 render correctly; headers max two lines; merged cells in Table 3.2 and 11.1.
- section_plan.yaml changed on disk during the run (report_doe notes only) -> no effect on the plan outline.

## DONE (2026-10-10). Open points for the coordinator
1. sdm_qualification.csv has no UF/DF (or harvest) rows; the plan keeps the V1.0 qualification design
   (S-UFDF-SDM, n_scale_down runs vs pilot+commercial record on yield, flux, final conc, aggregate change),
   so PCR-010 will find no offsets. PCMP-001 §5's list of compared outputs omits UF/DF.
2. PCMP-001 §7.1 decides qualification on the RSM model; the plan says it has no rule for UF/DF and
   PCR-010 states its approach. Config plan_discrepancies for PCR-010 has only PD-010-01.
3. The IAC derivation credits every step after CEX (UF/DF included) with zero aggregate increase; the plan
   states this and that PCR-010 reports the increment; no verification exists for a step without a DoE.
4. PCMP-001 §7.8 wording "nrCE-SDS in every study at every step" vs UF/DF studies measuring no fragments.
5. Config analytics.univariate_nodoe.assay.aggregate_out_pct = "AMV-3221" (not in AMV registry).
