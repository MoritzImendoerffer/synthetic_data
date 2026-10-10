# Content review run 1: PCP-009 Version 2.0 (virus filtration plan)

Judge: Claude Opus 5.5 (claude-opus-5-5), fresh context, read only `PCP-009_virus_filtration.DRAFT.txt`.
The first attempt was stopped by a safety classifier; this is the retry, with short quotes. Saved by the
coordinator (condensed). Answers: 1 Yes, 2 No, 3 five cases, 4 No, 5 five errors, 6 No, 7 No.

## Q1 Causes
No failures. Coverage note: "The MVM requirement therefore rests on anion exchange and on this step alone"
excludes only low pH by its reason; the other steps' exclusion rests on the claim sum in §7.

## Q2 Terms
"Filtration volume (load)" in L/m2 (a throughput or volumetric loading, not a volume); "NOR-propagated
analysis" (coordinator: PCMP-001 term, define at first use); Table 5.1 "Flux decay at the end of the load"
(at the maximum volumetric load).

## Q3 Glosses
"Any manual entry of a value into the analysis is a data integrity finding ... and will be handled as
one"; "The named individuals are recorded in the approval table ... so that a change of personnel does not
require a revision"; "The two analyses will form the two panels of one figure, so that the cost of ...";
"The cut-off 4/n is a common convention, and it falls as the number ..."; "PCR-009 will report its size
from the fitted models and will not assert ...".

## Q4 Criteria
"The normal quantile plot of the residuals shows no material departure from normality." and "The residual
standard error is small against the distance between the predicted response ..." (no threshold, no
basis); "Conditions 5 and 6 are specific to this plan." (say they are Version 1.0 rules kept).

## Q5 Wrong or contradicted
1. "For fragments, the analysis draws 2,000 values of the other parameter at each grid point" / "This
   assumes that the NOR spans ±3 standard deviations of the routine variation" vs Table 6.1: neither
   set-point is the NOR midpoint (load 90 in 50 to 105; pressure 13 in 10 to 20), so the draw centred on
   the set-point with SD NOR width/6 does not span the NOR. Shared item 7.
2. The revision history "Reissued under INV-001 and INV-002" vs Table 3.1 (INV-001 alone) and §1.1 (every
   change attributed to INV-001). Shared item 10.
3. "The study will be considered successful where the scale-down model is qualified, both LRF models ..."
   vs Table 5.1 and §5.1 (no output with a criterion compared at both scales); the sentence omits fragments
   though Table 7.1 and §8 give fragments a criterion (coordinator: Version 1.0 success criterion, keep;
   add how it reads under PCMP-001 §7.1, as factual error 5).
4. "XMuLV is many times larger than the pores. It is expected to be retained completely" with the
   detection-limit reporting and the success condition requiring an adequate XMuLV model: censored results
   have no scatter, so no model can be adequate, yet it is a success condition (coordinator: a Version 1.0
   tension the report meets; the plan states the Version 1.0 rules; do not add a rule).
5. "The flux decay profile, the step yield and the post-use integrity test result will be compared" vs
   Table 5.1 (no integrity row).
Version 2.0 scope: "Every run of both designs has an nrCE-SDS result for fragments, and aggregate was not
..." (execution record in Materials and methods; a third time in the Table 5.3 footnote); "The studies of
this step used none of the instrumented systems under calibration and change ..." (past-tense execution
record; coordinator: allowed by PA3 as a recorded fact, once).

## Q6 Machine-like
"The NOR lies toward the low end of both ranges, because both ranges extend further" (circular); "The
NOR-propagated range is therefore in general the narrower of the two." (restatement); "Criteria apply to
the scale-down model, to the fitted models, ..." (announces contents); "Each phase begins when the
preceding phase has met its criterion in Section 7." (fifth statement of the qualification timing); "The
screening model identifies effects. The response-surface model is the predictive model ..." (restates §2);
"The deliverable of the study is the report PCR-009." (repeats); "Prior knowledge does not replace the
study." (slogan); fragments ≤ 2.00 % three times; "Fragments are judged on nrCE-SDS results only" twice;
the fragment mechanism three times.

## Q7 Codes and stand-ins
INV-002 bare in the revision history (name it); "Conditions 1 to 4 ... Conditions 5 and 6" by number (name
them: the normal quantile plot, the residual standard error against the margin, both Version 1.0);
"Each phase begins when the preceding phase has met its criterion in Section 7." (name the criteria);
"the verification at other steps" (name it); "its output is judged against the criterion for fragments"
(the filtrate pool); "It was assigned by rule" ("It" has no antecedent); Table 5.1 "Flux decay at the end
of the load".

## Tables
Table 6.1 and 6.2 constant columns; Table 7.1 spanner mostly "not applicable", "Increase" explained only in
a footnote; Table 5.1 repeated cells (merge candidates), wrapped header; Table 5.3 one informative row;
Table 4.1 "Tool #1" code, clipped "Acceptance" header; Tables A.1 and B.1 long wrapped header, unmerged
run-type labels, identical factorial rows; Table 3.2 "Standard operating procedure" broken over four lines.
