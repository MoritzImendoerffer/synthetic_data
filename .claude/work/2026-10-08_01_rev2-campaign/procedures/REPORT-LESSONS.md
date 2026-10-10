# What the reviews of PCR-005 found, as rules for the next report

Written 2026-10-10 from the three content reviews, three factual passes and three feedback rounds of
PCR-005 in this work unit, with the owner's decisions to that date (`rev2-pilot-reading.md`,
`backlog-consistency-sweep.md`, `data-state-2026-10-09b.md`). Each rule below was broken at least once
by a careful author and caught by a fresh reader, or is an owner's decision that a report must apply.
Where the sources disagreed, or the owner reversed an earlier call, only the current rule is kept. The
rules say what must be true in the report, not how to word it. Read the rendered plan and PCMP-001 for
the rules a report applies. This file says where a report went wrong when applying them. "DoE steps"
are the bioreactor, Protein A, low-pH inactivation, cation exchange, anion exchange and virus
filtration. A rule marked "DoE steps" does not apply to harvest or UF/DF.

## 1. The rules the report applies

1. **What is judged, on which statistic.** A quality attribute is judged per batch: the 95 %
   prediction interval of a single run at every combination of NOR low, set-point and NOR high of the
   response-surface parameters, with the offset applied where one was measured. The engine's interval
   is two-sided, so its upper end is a one-sided 97.5 % limit, and the report says so where it defines
   the statistic. Viral clearance is judged on the mean predicted log reduction at the least favourable
   of those combinations (owner, 2026-10-08), with the per-batch value for information only. Where the
   claim rests on an adequate model, a single run below it is not the claim failing. An output without
   a model (harvest, UF/DF, any output with no adequate model) is judged on its individual results.
   Whatever is derived from a judgement uses the same statistic, or says why not: an influence or
   sensitivity analysis, the impact of a deviation, the level expected to enter a hold. A results table
   shows the value compared with the criterion (the prediction limit, not only the centre), so the
   margin can be read.
2. **Every general claim holds output by output.** A sentence about every output, every run or every
   conclusion, or a count of outputs, is true of each one it covers. Fragments have nrCE-SDS results
   only in the studies `T.methods_by_study` marks, so a fragment claim covers those samples only. An
   output with no criterion is reported for information: it is neither qualified nor met. (PCR-005 said
   fragments met their criterion in every run of both designs, wrote for three outputs what held for
   host cell protein only, and called the scale-down model qualified for outputs with no criterion.)
3. **The scale-down qualification** (DoE steps). For each output with a criterion the report gives the
   conclusion over the NOR with the offset at its estimate and at both ends of its 90 % interval, the
   runs it rests on and the criterion it is judged against. Where the outcome depends on a choice, the
   alternative is computed and stated: the criterion without its widening, the NOR as characterized,
   the planned runs alone, a model near the selected one (§2 rule 2). The offset is on the scale of the
   model. For a log-scale output it is a ratio of geometric means, a prediction is divided by it, and
   it scales a difference instead of cancelling from it. Titles and legends follow. An output the
   qualification did not compare (fragments, at most steps) has no measured offset. Its conclusions are
   at the scale of the laboratory model and rest on an assumption that the report states with its
   evidence (a bound from a hold study, for example), and no sentence about manufacturing scale
   includes it. The plan requires the offset before the first characterization run, so runs made later
   depart from it and are recorded (§3 rule 2).
4. **The NOR in force and the NOR as characterized.** Where the config changed a NOR (`T.nor_change`),
   every judgement names the NOR it uses by its range. The conclusions over the NOR, the PARs, the
   scale-down qualification and the capability simulation use the NOR in force. The verification of
   platform worst cases and every comparison with Version 1.0 use the NOR as characterized
   (STORY_BIBLE §9b, "Version 2.0 NOR and set-point decisions"). Where a conclusion differs between the
   two, give both. A NOR change is an owner's decision held in the config. The report states the
   changes the config holds, with their reasons, and makes none of its own. A NOR is the range routine
   manufacture is controlled in, so an attribute that fails at a NOR corner which no change addresses
   is reported as not met, with the risk acceptance the owner decided where one exists (STORY_BIBLE
   §9b, PCR-003 and PCR-006). A NOR change the data argue for, or a failure with no decided acceptance,
   goes into your hand-back. A NOR narrowed because the scale-down model is not qualified over the
   wider one reflects the evidence, not an effect of the parameter, and supports no class.
5. **Every criterion with its basis, judged at both ends, with one verdict.** Each criterion used at
   the step is given with its derivation, including those applied from another step, such as the
   criteria a held pool is judged against. A two-sided criterion is judged at both ends in every table
   and sentence. A statement that no criterion was tightened or widened separates the step's own
   criteria from those it applies from other steps. The executive summary, the numbered findings, the
   conclusions and the body give the verdict the table gives (PCR-005 broke this for the hold, the
   adequacy criteria and the qualification). State once, where the criteria are given, that the
   Version 1.0 limit was set at analysis and was in no approved plan, and add no sentence that the
   wider criterion does not loosen anything. Where the criterion in force is wider than its a priori
   Version 2.0 value, the report says that too and argues it (rule 6). A priori means derived from the
   drug substance criteria and the platform worst cases without this campaign's data. PCMP-001
   Version 2.0, which states the rule, was issued after the studies ran, and no sentence suggests that
   the rule preceded the data.
6. **A changed criterion is argued by its risk** (owner, 2026-10-09). The report whose criterion moved
   argues it, and the downstream report that verified the platform value gives the bound, its runs and
   its model adequacy. The bound is the one-sided 95 % prediction bound of a single batch at the least
   favourable combination of the downstream step's NOR as characterized (`D.VERIFICATION_BOUND`),
   never a confidence bound of the mean and never a point prediction. A widening also needs a
   downstream model that passes PCMP-001 §7.2, which an exact fit never does. A tightening needs no
   such test. The argument gives the bound, the runs behind it, why the downstream performance at A-Mab
   is known well enough, and the risk: who bears it (producer or patient), whether and where an
   excursion is detected (the in-process or release test and its limit of quantitation), what the
   downstream steps must then clear, and the probability that the drug substance is out of
   specification (`D.p_oos()`). It says where the bound stops, decided per attribute from
   `iac_verification.csv` (`observed_edge` against `assumed`, `model_adequate`). Runs at the edges of
   the range studied may have done worse than the platform value, and a 180-min platform hold replaced
   by a NOR that ends at 120 min reflects the shorter hold, not a more stable product. A downstream
   model that fails §7.2 confirms nothing, and no value is called confirmed on it. The criteria rest on
   the planned runs, as fixed when INV-001 closed. For an augmented downstream design, give the value on
   all runs beside it (`D.verification_all_runs()`).
7. **Model selection is a discrepancy from the plan** (DoE steps; owner, 2026-10-09: "all DoEs should
   be analyzed correctly"). The plan prescribes the full quadratic. The report analyses every
   response-surface output by the selection of STORY_BIBLE §9b ("How every DoE is analysed") and
   records it as the computed entry of `discrepancy_register(DOC)`: what was planned, what was done,
   why, and what it changed (`D.ca3_criteria_sensitivity()`). The statistical methods explain the log
   scale and the search to the standard of STORY_BIBLE §9b ("Explaining the log scale and the search
   to a reader"), with this step's numbers, and state the AICc convention (the residual variance is
   counted as a parameter). Every model table, diagnostic, figure and finding is of the selected model.
   The full quadratic appears only as the plan's model, where the report says what was planned or
   compares with Version 1.0 (`D.planned_full_models()`), named as such and with the run settings it
   was fitted on. Terms are counted one way throughout, and the report says whether the intercept is
   one. An augmented design follows STORY_BIBLE §9b (INV-002, "The reports"), and what the augmentation
   changed in each model is stated as computed.
8. **Adequacy, criterion by criterion** (DoE steps). PCMP-001 §7.2 has four criteria: the model F-test,
   lack of fit against pure error, R² minus predicted R² against its limit (against R², as PCMP-001
   states it, not adjusted R²), and the residuals and influence. Each selected model is reported
   against each of the four. A model with no term has no F-test, so that criterion is not applicable,
   never met. An exact fit (results with no scatter) is never adequate. Its output is judged on its
   measured results, sets no range, and its bound replaces no platform value (owner, 2026-10-09). The
   residual and influence criterion is judged as the plan states it, per test at α = 0.05 and Cook's
   distance against 4/n. Where it is not met, the report says so, and the analysis that carries the
   conclusion (each flagged run deleted and the judgement of rule 1 repeated) is a discrepancy from the
   plan. A 4/n flag is not explained away by leverage. Cook's distance already combines leverage and
   residual, and the cut-off flags a run or two in most correct models of this size.
9. **A rule chosen after the result never decides.** The decision is the rule the plan or PCMP-001
   stated: the level of each test, the interval, the runs. A multiplicity correction, a pooling with
   another study or a different interval chosen once a result is known is the pattern INV-001 was
   opened over. Where the pre-set rule is not met, the report says so and records any further analysis
   as a discrepancy. An acceptance despite the failure rests only on a risk argument the owner
   accepted. Runs or studies added after a result was seen are named as such, and a conclusion that
   rests on them carries that limitation (optional stopping; STORY_BIBLE §9b, PD-005-01).
10. **The PARs and the design space** (DoE steps). The univariate PAR at set-point and the
    NOR-propagated PAR are defined at first use as PCMP-001 §6.4 defines them (brief §5c: a registered
    discrepancy here stays as registered), with the acceptance limit of the second (which percentiles
    of the simulated batches must lie within the criterion) and the claim it supports. A PAR comes only
    from an adequate model. An output with no adequate model is judged on its measured results, and no
    table, finding or figure gives it a PAR or a predicted level. The design space is defined on the
    statistic the engine uses (the mean prediction, the median on a log scale), on a stated grid, with
    every fraction computed on that grid (`D.design_space_grid`). A sentence about an excluded region
    names the statistic that excludes it (a median can meet a criterion where a single batch does not)
    and the settings of the other parameters it assumes.
11. **Capability.** Each Cpk is stated against the target and the minimum of PCMP-001 with a verdict,
    including a value below the target, which is judged here and not passed on to PCMR-001. Where a Cpk
    is not meaningful (an attribute far below its limit), the report says how the attribute is judged
    instead. The probability out of specification (`D.p_oos()`) is given, or, when no simulated batch
    falls outside, its upper bound, which covers the sampling of the simulation and not the uncertainty
    of the integrated process model. A simulation input from outside this step's data that a claim
    depends on (the DNA clearance of each downstream step, for example) is named with its source. A
    quality attribute in scope with no intermediate criterion (residual DNA) carries the reason
    PCMP-001 gives for none.
12. **Classification.** Each class is stated with the evidence the classification rule uses, the effect
    size across the PAR and the margin of the PAR to the NOR, and the rule is named in words. No
    numerical threshold exists for "practically relevant" or "wide", so neither word decides a class. A
    well-controlled CPP is a critical process parameter, so a step with one never reads as having no
    CPP. The evidence for a parameter with no detected effect covers only the attributes its study
    measured (§2 rule 9).

## 2. Science and statistics

1. **Absence of evidence.** A term that is not significant is not shown to be absent. A lack-of-fit
   test that is not significant is reported with its p-value, not as an absence of lack of fit. A
   parameter with no detected effect has no effect detected within the range studied, at the precision
   of the runs. A conclusion drawn from the absence of a term the selection removed is circular.
2. **Near-equivalent models** (DoE steps). When other models lie within 2 AICc units of the selected
   one, a feature only some of them carry (an interaction, a curvature) is not a finding. Compute them
   (`adequacy.hierarchical_subsets`, `adequacy.aicc`), say what they share and where they differ, and
   say whether any conclusion over the NOR or any scale-down qualification changes among them. A
   feature a model has by construction is no evidence: the contours of a model with no interaction term
   are parallel on any scale.
3. **A run a deviation affects** (DoE steps). Where the deviation record holds the setting actually
   run, the run is analysed at it (`D.setting_corrections` lists those the engine applies; report any
   it misses), and the report gives the run's residual on the model used and the analysis with the run
   at its design setting and excluded. A statement that no single run decides a conclusion, or that the
   deviations did not change the conclusions, holds for every conclusion it covers, the terms of the
   selected model included.
4. **A replaced result.** Where a re-assay replaced a result on a suspected, not confirmed, cause, the
   report gives both results, which one is used and why, and the analysis with the first result in
   place, and states whether any conclusion changes. No summary says that all data were retained when a
   result was replaced.
5. **The same evidence, read the same way.** Evidence of equal weight is read the same way for every
   output: a lone significant term in a weak model is not a finding for one output and chance for
   another. Agreement in direction is claimed only against a direction the prior-knowledge section
   stated. Where the screening and response-surface designs disagree (an effect that changes sign), the
   difference is tested and reported as a result. A candidate cause is offered only as far as the data
   name a property and a direction, and the response-surface model stays the predictive one.
6. **Mechanism.** WRITING_GUIDE §2 rules 1 and 4 say where and how a cause is given. The causes PCR-005
   gave failed in these ways.
   - The unit of the output decides what can explain it. An output per mg of antibody does not rise
     because more antibody is loaded, and a reporting convention is not a cause. An effect that no
     mechanism explains is reported as observed, with no cause.
   - A cause the study did not test (the cause of an offset, an expectation from the A-Mab case study)
     is an expectation, and is called one.
   - A cause given for one output is checked against what it predicts for the step's other outputs (a
     protease in the load that cleaves ligand also clips antibody, and its contact time depends on the
     load and the flow rate).
   - A claim that a step retains, passes or leaves an attribute unchanged names the property it rests on
     and its known exceptions, and needs the attribute measured in the load and in the pool. Measured in
     the pool alone it is an assumption, and a criterion upstream that relies on it rests on that
     assumption.
   - An absolute claim with no data in the report is supported or cut.
7. **Causal verbs are for physical causes.** A statistical or mathematical relation is stated as one:
   which output's criterion limits a PAR, which model term carries an effect, that two effects are
   additive on the log scale. PCR-005 used "sets", "because the two effects multiply" and "acts on ...
   through a small curvature" for such relations.
8. **A method measures what the report says, in that matrix.** The antibody in clarified harvest is
   measured by the titre assay (Protein A affinity HPLC), because A280 there counts host cell protein
   too. A purified intermediate is measured by A280. A value per mg of antibody in a load needs the
   antibody in that load. A method that differs from the plan's is a discrepancy (PD-005-06).
9. **Univariate evidence** (the univariate parameters of the DoE steps, and the whole of harvest and
   UF/DF). A range is supported only for the attributes the study measured. An attribute with a
   criterion that was not measured is "n.t.", and no support is claimed for it. The individual results
   at each level are reported against the criterion (at manufacturing scale where an offset applies),
   and a difference not detected carries the precision of the comparison. For harvest and UF/DF,
   STORY_BIBLE §9b ("Harvest and UF/DF univariate studies") applies in full.
10. **Hold studies** (harvest, Protein A, low-pH inactivation). One pool made at set-point was held, at
    the temperatures and for the time tested, and the claim stops there. No plan sets a hold criterion,
    so the report states its approach and records it within the hold-study discrepancy. The verdict
    concerns what the hold adds: the highest level expected to enter the hold plus the largest change
    over it. The expected level is the single-batch limit over the NOR of the step that sets the
    attribute, at manufacturing scale, or that step's measured results where it has no adequate model.
    A limit not met by the level entering the hold is shown as not met, in the table and in the text,
    with the report that owns it. A change smaller than the difference between the day-0 aliquots is
    not resolved, decided on unrounded values (§4 rule 6).

## 3. The record: deviations, discrepancies from the plan, chronology

1. **One reference plan, the registers as the record.** section_plan defines the two words. A
   departure from a rule of the approved plan (a required measurement not made, a sequence not
   followed) is a deviation, and work the plan did not foresee is a discrepancy. The reference is the
   approved Version 2.0 plan the report states results against, so every study made after Version 1.0
   (hold, augmentation, confirmation and support studies, a second univariate study, added scale-down
   runs) is a discrepancy. `dev_register(DOC)` and `discrepancy_register(DOC)` as they render are the
   record. Every mention of an entry in the text matches the entry's scope, and where the brief words
   an entry differently, the register wins.
2. **Every departure is recorded, none silently.** Compare the study as run with every rule,
   measurement, sequence and design of the rendered plan, and record each departure as a deviation or a
   discrepancy (for PCR-003, the list in `pcr003-departures.md`). An unplanned replicate, a method the
   plan does not name and an analysis the plan does not contain are departures too. Where the plan sets
   no rule the report needs, the report states its approach, applies it and records it as a
   discrepancy, never as the plan's rule. A departure that is in neither register goes into your
   hand-back. Do not invent an identifier.
3. **The plan as it is written.** A quotation or close paraphrase of the plan (objectives, criteria,
   section numbers) matches the rendered plan, with no condition dropped or added. A plan criterion is
   cited by what it is and its section, because criterion numbers changed between plan revisions.
4. **Chronology.** Every date range comes from `study_chronology.csv`. The studies made during the
   re-analysis are named apart from the characterization studies, and no single window leaves them out.
   The report says when a decision to add runs or studies was taken relative to the result it answered.
5. **What added work changed** is computed and asserted (WRITING_GUIDE §3), whatever it is, and its
   direction is never assumed. The outcome of PD-005-01 reversed twice while the data moved.
6. **Changes in this revision.** Every statement there that something is unchanged is checked against
   the new runs, models, studies, NOR changes and criteria.
7. **What the record does not hold is not written.** A statement about how a study was run (the
   columns, the procedures, the lots) needs a source in the brief or the data. SOP and AMV titles come
   from the register (`T.sop_references`, `all_sop_table()`), never typed, and a method with no entry
   is a `<<NEEDS:>>`.

## 4. Tables

1. Never retype or override a builder's header, note or verdict. If a builder or helper is wrong (for
   example `D.governing_factor` naming a parameter that is not the largest effect of the selected
   model), report it.
2. Beyond WRITING_GUIDE §6, your own tables have at most two header lines, units in the header, no
   constant column and a legend for every code. A header says what its column holds: a median or a
   mean, a measured or a predicted value, the limit compared with the criterion.
3. A verdict column agrees with the text, shows both ends of a two-sided criterion, and marks a test
   that does not apply as not applicable.
4. A model table shows only the models the report uses, and a Version 1.0 model is labelled as one. A
   column that repeats the range studied in every row is one sentence instead.
5. One format per kind of value across the document: criteria and ranges written one way, a true minus
   sign, the same precision for the same quantity, thousands separators, no more digits than the
   measurement supports, nothing below the limit of quantitation printed as a number, and changes of a
   percentage attribute in percentage points. One label per attribute in every table and figure, plain
   compounds in table text, and parameter names and units from the config
   (`CFG.unit_op(UO).param(key).name` and `.unit`), never typed.
6. Prose and table come from the same unrounded values. A comparison word (smaller, no more than, the
   same) is decided on unrounded values and computed. Where the printed digits cannot show a
   difference, the sentence does not claim one. A table whose totals differ from its printed parts says
   that it is computed from unrounded values.
7. Every attribute the report judges is in its table of attributes in scope, and every attribute named
   in the capability text is in the capability table. Figures use the units of the tables.

## 5. Readability

WRITING_GUIDE §2 rule 11 is the owner's rule. PCR-005 broke it in these ways.

1. Codes left bare: plan criterion numbers (name the test), the findings and actions of the
   investigations, the method decision, study codes and the registers. A section of this report is
   cross-referenced by its label (`@sec-…`), never by a typed number, so a moved section cannot leave
   a wrong one.
2. Internal labels used as terms (the hold rule, the offset rule, widened on verification, the NOR in
   force, decision statistic, assurance target, ratio offset, the limit on predictive power). Say what
   each means, with the range or the number. A term PCMP-001 defines is defined once at first use,
   then used.
3. Restatement: the offset subtraction four times, a co-elution point five times, a results section
   repeated in the Discussion. Each fact is said once, in its section, and cross-referenced after. The
   executive summary and the conclusions are the exceptions.
4. An effect that a designed experiment shows within the range studied is stated with its size and
   direction, not as an association.
5. Cut a sentence that answers an objection nobody raised (that a criterion is not loosened, that the
   master plan was not changed, that a point prediction is never used), files a finding elsewhere
   instead of judging it, calls a result conservative or reassuring where that holds only in part,
   opens a paragraph without content, states an aphorism, or recommends without a basis. A sentence
   frame repeated across sections reads as templated.

## Not rules: open owner questions

- **The criteria of a held pool.** PCR-005 used the criteria in force for the next step's load
  (tightened and widened on verification). An earlier coordinator note said a priori.
- **The statistic of the design space.** It is drawn on the mean (median) prediction, while the PARs
  and conclusions are per batch (PCP-003 review).
- **Detectability of host cell protein.** The record has no coverage figure for the ELISA, so a risk
  argument can name only the release test and its limit of quantitation.
- **Residual DNA.** The unit of the drug substance criterion (ng/dose), and no intermediate criterion.
- **The class of a parameter for an attribute its study did not measure** (Protein A, fragments).
- **A qualification that depends on the choice among near-equivalent models** (two of the nine
  Protein A models within 2 AICc units would not qualify the scale-down model).
- **An out-of-trend result with no out-of-trend limit in the deviation record** (DEV-005-02).
