# Register exemplar — verbatim passages from the published sources

This file teaches the **voice** of an A-Mab characterization document. Read it before you
write, and keep it open while you write.

Every passage below is **verbatim** from one of the four published human documents this
corpus is modelled on. All four are in the repository as page-marked text:

- `refs/text/amab.txt` — *A-Mab: A Case Study in Bioprocess Development*, CMC Biotech
  Working Group, v2.1 (2009). **This is the closer model for a report.** It narrates real
  data and defends real conclusions, which is what you are doing.
- `refs/text/pda60.txt` — PDA Technical Report No. 60, *Process Validation: A Lifecycle
  Approach*, Parenteral Drug Association (2013). Guidance, so it says "should" where a
  report says "was". Take its sentence rhythm, not its modality.
- `refs/text/ispe_tt.txt` — ISPE Good Practice Guide: *Technology Transfer*, third edition
  (2023). **This is the closer model for a plan.** Ten of the twenty corpus documents are
  plans, `PTP-001` is a technology transfer plan, and until 2026-08-16 no source here was
  plan-shaped at all. It commits, permits and conditions in three different modalities,
  which is the move a plan lives on.
- `refs/text/ispe_pv.txt` — ISPE Good Practice Guide: *Practical Implementation of the
  Lifecycle Approach to Process Validation* (2023). Also guidance. It writes the longest
  sentences of the four, so take its moves rather than its length.

**Citations.** A-Mab page numbers are the document's own, and match the `PAGE N` markers in
the extract. The other three number their printed pages differently from the extract markers,
by a constant 8 for PDA TR 60 and a constant 2 for both ISPE guides, so both are given:
printed p. 23 is `PAGE 31` in `refs/text/pda60.txt`.

**Transcription.** Words are unchanged. Where the PDF layer split a word across a line
break it has been rejoined, and curly quotes have been normalised. Real typos in the
sources have been left in place; a few are pointed out, because they are a useful reminder
that published documents are not polished to machine smoothness.

---

## How to use this file

Study the shape of each passage: how long the sentences are, where the qualification goes,
how plain the connectives are, and how little decoration there is. Then write your own
step's sentences. **Do not copy these sentences and do not reuse their facts** — they
describe a different process at a different point in its lifecycle.

Three habits to notice before you start, because they are what most often goes wrong:

1. **These documents almost never use an em-dash.** The A-Mab case study contains none at
   all in 278 pages. A qualification gets its own sentence, or parentheses.
2. **They repeat nouns instead of varying them.** "The design space" stays "the design
   space". It never becomes "the multivariate envelope" for the sake of variety.
3. **They stop when the point is made.** Very few paragraphs end with a sentence explaining
   why the paragraph mattered.

## What NOT to imitate

The corpus's own first-pass reports are **not** a voice reference, and you must not open
them. They were written in a machine register: 34-word average sentences, an em-dash aside
every third sentence, coined compounds such as "the quality-attribute-richest
characterization in the campaign", and a "what this means" clause welded to every paragraph.
`authoring/check_style.py` exists to catch that drift, and its thresholds are the measured
properties of the four documents quoted below. Note what that does and does not buy you: the
band is the union of four house styles, so writing at its edge matches none of them. Aim at the
per-source columns in `WRITING_GUIDE.md` §4a.

---

# Part 1 — The reporting moves

## 1. Opening a unit operation: what it is and what it does

> The Protein A step is the first chromatographic unit operation in the purification process.
> This step uses an immobilized Protein A resin which binds the mAb from the harvested cell
> culture fluid (clarified harvest). The affinity capture is an inherently robust processing
> step, with a rich platform performance history that supports the proposed design space.
> Process impurities such as HCP, DNA, and small molecules are removed in the flow through or
> wash. A low pH buffer elutes the mAb and sets up the subsequent low pH inactivation step.
> While viral clearance can be demonstrated for Protein A chromatography steps, there are no
> claims made for this step.
> — A-Mab, p. 118

> AEX chromatography is the final purification step in the A-Mab downstream process. It is
> operated in the flow-through mode binding impurities such as HCP, DNA and endotoxins to the
> resin (or membrane) while the antibody passes through. A viral clearance claim can be made
> for this step and details to support it are discussed below.
> — A-Mab, p. 140

> The CEX step utilizes a strong cation exchange resin operating in a bind and elute mode to
> capture the A-Mab. The step is operated with a step elution designed to provide separation
> of HCP and aggregate, while also providing clearance of DNA and leached ProA. Charge and
> glycosylation variants are unaffected across the step when operated within platform
> conditions. Although some viral clearance can be demonstrated across this step, no claims
> are made.
> — A-Mab, p. 134

**Note.** Three openings, three steps, and every one ends by saying what is *not* claimed.
That is the explicit-non-claim obligation in its natural register: one plain sentence, no
build-up. Note also the sentence lengths — 14, 27, 24, 17, 17, 19 words in the first passage.

---

## 2. Purpose and objectives of a study

> The following sections describe the approaches used to identify parameters linked to product
> quality and process performance that serve as the basis for defining the design space for
> each process step. The classification of process parameters used in this section is based on
> the decision logic presented in the Control Strategy Section.
> — A-Mab, p. 117

> An initial risk assessment was completed for the production bioreactor and the N-1 seed
> culture steps with the purpose of identifying equipment design, control parameters,
> processing conditions and starting materials that pose a significant risk to the quality
> attributes of the product.
> — A-Mab, p. 73

> Process characterization is a set of documented studies in which operational parameters are
> purposely varied to determine their effect on product quality attributes and process
> performance. The approach uses the knowledge and information from the risk assessments to
> determine a set of process characterization studies to examine proposed ranges and
> interactions for process parameters. The resulting information is used to define the PPQ
> ranges and acceptance criteria.
> — PDA TR 60, printed p. 23 / extract p. 31

---

## 3. Prior knowledge as the basis for a study

> The downstream process for A-Mab represents a well established platform with extensive
> process performance history. It has been used for the production of commercially licensed
> antibodies and the supply of multiple clinical studies. The large body of knowledge derived
> from this experience has demonstrated that the downstream process is robust and consistently
> produces Drug Substance of acceptable yield and quality. This extensive process experience
> therefore reduced the amount of process optimization studies required for the A-Mab
> downstream process.
> — A-Mab, p. 111

> Low pH viral inactivation step has been used extensively to manufacture three previous
> licensed antibodies (X-Mab, Y-Mab and Z-Mab) as well as many other therapeutic proteins.
> Moreover, the low pH step process conditions have remained essentially unchanged for these
> products and throughout the A-Mab development process. Thus, experience gained from the
> characterization of low pH inactivation studies constitutes prior product knowledge and may
> be applied directly to the A-Mab process.
> — A-Mab, p. 128

> The small virus retentive filtration step has been used extensively for the manufacture of
> several other antibodies. Extensive experience has been gained from the characterization of
> virus filtration studies for 3 mAbs with "Type F" filters. This prior knowledge can be
> applied directly to the A-Mab process because the mechanism of virus clearance is identical
> and no differences in performance are expected with A-Mab.
> — A-Mab, p. 153

**Note.** The prior-knowledge argument is made in four sentences: what the platform is, how
much experience there is, what it demonstrated, and what follows for this study. The
transfer of credit is always justified by a stated mechanism, never asserted.

---

## 4. Quality attributes and how criticality was assigned

> The outcome of this approach is not a binary classification of quality attributes into
> "Critical" and "Non-Critical". Rather, the result is a "Continuum of Criticality" that more
> accurately reflects the complexity of structure-function relationships in large molecules
> and the reality that there is uncertainty around attribute classification.
> — A-Mab, p. 20

> Although both Tools #1 and #2 do not categorize attributes specifically as Critical or
> Non-Critical, a level of criticality has been assigned to all of the attributes in Table
> 2.28. The levels are very low (VL), low (L), moderate (M), high (H) and very high (VH). The
> attributes that are of high and very high criticality have been called "Critical".
> — A-Mab, p. 54

> The lack of clearance or modification of glycosylation variants through the downstream
> platform process is consistent with the binding mechanisms of the respective chromatography
> steps. Protein A, when operated under platform conditions, does not separate glycosylation
> variants of monoclonal antibodies. The charge-based separation steps, cation exchange and
> anion exchange chromatography, also do not discriminate between different glycosylation
> variants, except for sialylated structures. However, sialylation variants are only present
> at very low levels in A-Mab and thus are not considered critical to product quality.
> — A-Mab, p. 116

**Note.** The third passage is a complete mechanistic argument in four sentences, and the
exception is handled by "However … and thus", not by a subordinate clause.

---

## 5. Risk assessment deciding which parameters are studied

> A risk assessment approach was used to categorize all Protein A process parameters into
> three groups: i) parameters warranting multivariate evaluation, ii) secondary parameters
> whose ranges could be supported by univariate studies, and iii) parameters which did not
> require new studies, but instead would employ ranges based on knowledge space or modular
> claims established from prior knowledge.
> — A-Mab, p. 119

> The risk assessment approach used risk ranking to classify process variables based on their
> potential impact to CQAs, process performance and possible interaction with other
> parameters. Each parameter was assigned two rankings: one based on the potential impact to
> CQAs (main effect) and the other based on the potential of interactions with other
> parameters. The rankings for impact to CQAs were weighted more severely than the impact to
> lower criticality QAs or process attributes (Table 4.4). If no data or rationale were
> available to make an assessment, the parameter was ranked at the highest level.
> — A-Mab, p. 119

> The cumulative scores represent the relative importance of the parameter for the unit
> operations, so parameters with high scores were considered to be high risk. Prior knowledge
> was used to prioritize and group parameters for multivariate experiments, for example,
> parameters with scores greater than 300 were studied in DOE-1.
> — A-Mab, p. 142

> Some high risk parameters were studied as a single variable (OFAT). Parameters with scores
> below 250 were not studied as they were considered to be low risk.
> — A-Mab, p. 142

**Note.** The last passage is two sentences and 28 words total. It disposes of an entire
class of parameters. Compare what the machine register would have made of it.

---

## 6. Scale-down model and its qualification

> A scale-down laboratory system was qualified as a model of the manufacturing-scale process.
> The model was designed based on well-established principles of chromatography scaling,
> maintaining the same bed height, linear flow velocities, load, wash and elution volumes
> (normalized to column volumes), and column efficiency based on plate count and peak
> asymmetry. The model qualification used triplicate runs of the lab-scale system, with
> statistical comparisons of the mean values of the performance parameters for lab, pilot- and
> manufacturing-scale, product yield, peak volume, impurity removal (e.g. HCP, DNA, and
> insulin), and levels of leached Protein A. In all cases, there were no statistically
> significant differences in column efficiency or performance parameters between scales (data
> not shown) and therefore, the scale-down model accurately represents the full-scale system
> and is suitable for use in process characterization studies.
> — A-Mab, p. 118

> The scaled-down model for the production bioreactor has a similar design and capabilities to
> the full-scale production vessels. Both are stirred tank bioreactors with equivalent design
> characteristics (e.g., mixing, aeration, mass transfer) and process control capabilities
> (e.g., pH, dissolved oxygen, temperature, nutrient addition, etc). For the qualification
> studies, scale-independent variables (pH, temperature, iVCC, DO, culture duration, etc) in
> the scale-down bioreactors were operated at the proposed target process values of commercial
> operations. For scale-dependent parameters (agitation, gas flow rates, pressure, volume,
> pCO2, etc), operating conditions at small scale were established to match process
> performance at full-scale.
> — A-Mab, p. 94

> When the process is run at target values of controlled parameters, the quality and process
> performance is comparable across scales, demonstrating the linearity of process scale-up
> (Table 4.20) and the validity of the scale-down model.
> — A-Mab, p. 134

> The ability of laboratory-scale studies to predict process performance is desirable. When a
> laboratory scale model is used in development, the adequacy of the model should be verified
> and justified. When there are differences between actual and expected performance,
> laboratory models and model predictions should be appropriately modified. In that the
> conclusions drawn from the studies are applied directly to the commercial-scale process,
> qualification of laboratory-scale models is essential. Qualification of the scaled-down
> models should confirm that they perform in a manner that is representative of the full-scale
> process.
> — PDA TR 60, printed p. 23 / extract p. 31

**Note.** Our corpus never writes "data not shown" — every deferral names a location. But
notice everything else about that first passage: the scale-down warrant is built and closed
in four sentences, and the conclusion arrives with a plain "and therefore".

---

## 7. Describing a designed experiment

> Based on this risk assessment (Table 4.7), five variables were identified for the
> multivariate studies: protein load, flow rate, temperature, elution buffer pH, and end of
> collection based on column volumes. A randomized 19-run study was conducted with six-factor,
> 16 run Resolution IV fractional factorial design which included a link to the cell culture
> process. Two culture harvests, one early and one late harvest were used to get feed stocks
> with extremes of low and high viability and titers, since these parameters could impact the
> Protein A performance. The three center points consisted of equal volume mixture of the two
> extreme feed stocks.
> — A-Mab, p. 121

> Process characterization was based on multi-factorial experiments (DOE) that included
> process parameters ranked either high (red) or medium (yellow) in the above risk analysis.
> The parameters and ranges used in the DOE studies are given in Table 3.14. The parameters
> were tested in an initial screening study, a resolution IV fractional factorial experimental
> design augmented with four center points. This type of experimental design is not able to
> resolve all the interactions between parameters and it would have to be augmented on the
> subset of parameters shown to impact CQAs. The center-point conditions align with the target
> process conditions.
> — A-Mab, p. 77

> The process characterization studies were designed around the target and process control
> ranges used for clinical manufacturing at the 5K L scale. The ranges were expanded to 2 or
> 3X of the routine control ranges to assess process performance and impact on CQAs over a
> wider range and determine process robustness. The wider ranges also provided process
> understanding to support future potential process improvements and movement within the
> design space.
> — A-Mab, p. 144

> The purpose of a screening experiment is to identify the critical parameters that have the
> most important statistical effect on the quality attributes. Since screening designs do not
> always clearly identify interactions, the reduced number of parameters identified by the
> screening experiment will be included in further experiments.
> — PDA TR 60, printed p. 57 / extract p. 65

**Note the second passage.** "This type of experimental design is not able to resolve all
the interactions between parameters" is the screening-identifies limitation, stated in one
flat sentence with no hedging apparatus around it. That is how to satisfy the
screening-versus-response-surface obligation. Note the third passage for range
justification: why the ranges are wider than the NOR, in two sentences.

---

## 8. Reporting results: what mattered and what did not

> HCP levels were impacted by protein load, wash conductivity, and HCP levels in the input
> feed-stream. A significant interaction between protein load and wash conductivity was
> identified.
> — A-Mab, p. 137

> Aggregate levels were impacted by protein load, elution stop collect, elution pH, and
> aggregate levels in the input feed-stream. A significant interaction between protein load
> and elution pH was identified as well as significant curvature due to elution stop collect
> and elution pH.
> — A-Mab, p. 137

> Results also showed that none of the process parameters had a significant effect on
> aggregate or acidic variants (deamidation). While small differences in these product quality
> attributes was seen in Protein A pools of the multivariate runs, no significant statistical
> correlation was established. Based on these results, all other process parameters were
> classified as General Process Parameters (GPPs)
> — A-Mab, p. 123

> Grey arrows indicate the effect was detected statistically but is too small to have an
> appreciable effect on the quality of the material produced. For example, it is seen that
> medium concentration had a statistically significant effect on aFucosylation (p = 0.001).
> However, by reviewing Figure 3.4 it is seen that its effect was very shallow. In this case,
> changing the medium concentration from 0.8 to 1.6 X only changed the aFucosylation levels by
> 0.3 %.
> — A-Mab, p. 77

**Note.** The first two are the standard results move, and they are two sentences each.
Results reporting in this register is *terse*. The last passage is the best example in
either document of separating statistical significance from practical significance, and it
is worth imitating whenever an effect is significant but small. The third shows the
null-result move: no effect, therefore a classification, in three sentences.

---

## 9. Reporting a model, and how much is claimed for it

> A statistical analysis was performed to assess the effects of the process parameters on each
> CQA. Statistically significant effects were detected and a predictive model developed for
> step yield, aggregate, and HCP.
> — A-Mab, p. 137

> Estimates are scaled based on the ranges tested in the DOEs, so that they measure change in
> the response value by half-range. These estimates represent the coefficients of the response
> surface that models changes in the CQAs as a function of the level of the process
> parameters. Only effects that are significant at p < 0.05 level are shown.
> — A-Mab, p. 80

> This model is suitable for predicting mean levels of the CQAs over the ranges of the process
> parameters included.
> — A-Mab, p. 80

> Since the response surface models used to create Figure 3.5 represent mean levels, the
> reliability of the process at the edges of the shaded regions in would be roughly 50% if the
> variability is symmetrical around the mean values.
> — A-Mab, p. 83

> This model was verified at small scale by experimentally linking all the steps at target and
> extreme conditions. The results predicted by Equation 6 correlate well with the measured
> values (Table 4.35). Thus, the model used to establish the design space was confirmed
> through experimental verification in the representative scale models and considered robust
> and predictive of performance at commercial scale.
> — A-Mab, p. 159

**Note.** The p. 80 and p. 83 pair is the most important thing in this file for the results
sections. The model is claimed to be "suitable for predicting mean levels", and then the
document immediately concedes that a mean-level model gives only about 50 % reliability at
its own edge. The claim is bounded by the next sentence, not by a clause. (The p. 83
sentence also contains a missing word, "shaded regions in would be". It is quoted as
printed.)

---

## 10. Design space, and the ranges nested inside it

> It is important to note that the ability to properly categorize process parameters and
> accurately assess the significance and effect of the variability of a parameter on CQAs
> depends on process/product understanding and the size of the characterized process space
> (i.e., knowledge space). The design space is a subset of the knowledge space that is known to
> result in acceptable values for the Critical Quality Attributes. Typically, the process is
> operated within a more limited control space which lies within the design space.
> — A-Mab, p. 241

> The preceding sections show how the process parameters affect the outputs of each individual
> unit operation. In order to create a design space for the entire process, we need to
> understand how the individual unit operations interact. All three chromatography unit
> operations remove HCP, so the full design space for parameters that influence HCP cannot be
> determined for a single step in isolation from the other steps. One solution is to set
> arbitrary in-process limits on HCP at each step, which would then determine acceptable
> parameter ranges for each step. While this approach is simple, it unnecessarily constrains
> the design space.
> — A-Mab, p. 158

> As stated in ICH Q8(R2), working within the design space is not considered a change (from a
> regulatory filing perspective). However, as stated in ICH Q10, from a pharmaceutical quality
> system standpoint, all changes should be evaluated by a company's change management system.
> Planned movement within a design space does require a prospective assessment of the risks
> associated with the particular move to be performed within the quality system and a
> conclusion that the proposed change is supported by the existing product and process
> knowledge.
> — A-Mab, p. 264

> The intersection of the acceptable operating ranges derived from the process characterization
> and viral clearance studies defines the design space for the low pH viral inactivation step
> and is shown graphically in Figure 4.4. Note that the design space is also constrained by the
> acceptable temperature range 15°-25° C.
> — A-Mab, p. 133

> The viral clearance design space represents only the range of parameter values that will be
> considered to provide assurance of a LRF of ≥ 5.5 for XMuLV and ≥ 4.0 for MVM. The process
> must be run within the narrower design space for operation of the AEX step in order to assure
> control of other quality attributes.
> — A-Mab, p. 150

> An element of process characterization may include multivariate designed experiments to
> define process design space. While univariate approaches are appropriate for some variables
> to establish a proven acceptable range (PAR), multivariate studies account for interactions
> between process parameters/material attributes (1).
> — PDA TR 60, printed p. 23 / extract p. 31

> It may also be used to assess the severity of process deviations caused by parameter
> excursions. Parameter ranges may be designated as normal operating ranges (NORs), or where
> proven by supportive data, as proven acceptable ranges (PARs).
> — PDA TR 60, printed p. 25 / extract p. 33

**Note.** "where proven by supportive data" is exactly the bound a PAR claim needs, and it
costs five words inside the sentence that makes the claim. Note also that A-Mab is willing
to describe an approach it rejected ("One solution is … While this approach is simple, it
unnecessarily constrains the design space"). Considering and dismissing an alternative in
two sentences is a strong, cheap move.

---

## 11. Capability and statistical assurance

A-Mab contains **no Cpk and no Monte-Carlo language anywhere**. It expresses assurance as a
prediction interval or as a reliability contour. Cpk language comes from PDA TR 60. Both are
legitimate for our reports; take the phrasing from whichever matches what you are reporting.

> In order to provide assurance that the operational settings of the process parameters will
> reliably produce HCP levels below the specification limit, the uncertainty of the prediction
> must be considered and accounted for. This includes process, measurement and sampling
> variation as well as uncertainty of the model itself (parameter estimates, parameters
> studied, form of the model). For this case study a 99.5% prediction interval was added to the
> mean predicted HCP levels to reflect the desired level of assurance in the design space that
> specifications will be met.
> — A-Mab, p. 159

> Notice that in this case the contours in the plot represent the probability levels that all
> the quality attributes included in the model will be within the acceptable limits defined in
> Table 3.17. In this case study the design space is defined as the multidimensional subset of
> process conditions that result in a reliability >99% of satisfying these limits
> simultaneously.
> — A-Mab, p. 83

> Statistical process control charts answer the question, "Is the process stable and
> consistent?" Process capability statistics answer the question, "Is the process capable of
> meeting specifications?" Process capability is the ability of a process to manufacture
> product that meets pre-defined requirements. It can be assessed using a variety of tools,
> including histograms and process capability statistics. The two most common process
> capability statistics, Cp and Cpk, are shown in Figure 6.2.2.1.3-1. Cp measures the
> capability of a process to meet specifications if it is centered between the specification
> limits. Cpk assesses if the process is actually meeting specifications when any lack of
> centering is considered.
> — PDA TR 60, printed p. 62 / extract p. 70

> Acceptable values for Cpk depend on the criticality of the characteristic, but 1.0 and 1.33
> are commonly selected minimum values.
> — PDA TR 60, printed p. 64 / extract p. 72

**Note.** The second passage is the whole capability-bounding obligation in one sentence:
the assurance level, what it covers, and what it is conditioned on. The A-Mab p. 159 passage
lists the sources of uncertainty *before* stating the assurance figure.

---

## 12. Parameter classification, with the reason for the class

> Both, CPPs and WC-CPPs, are process parameters whose variability have an impact on a
> critical quality attribute and therefore should be monitored or controlled to ensure the
> process produces the desired quality. A WC-CPP has a low risk of falling outside the design
> space. A CPP has a high risk of falling outside the design space. Here, the assessment of
> risk is based on a combination of factors that include equipment design considerations,
> process control capability and complexity, the size and reliability of the design space,
> ability to detect/measure a parameter deviation, etc.
> — A-Mab, p. 117

> Results show that both pH and time are important parameters to assure viral safety. pH was
> designated a critical process parameter (CPP) because the range is relatively narrow and pH
> values above 4.0 have not been demonstrated to effectively inactivate XMuLV within 60
> minutes. Because time is readily controlled and had no adverse impact on the Quality
> Attributes over a broad range, it was designated a well-controlled critical process parameter
> (WC-CPP). Similarly, temperature is a WC-CPP because slightly lower rates of virus
> inactivation are observed at lower temperature, but it is readily maintained within the
> 15°-25° C that has been demonstrated to effectively inactivate XMuLV. On the other hand,
> protein concentration had little or no effect on inactivation kinetics, product aggregation
> or acidic variants and was therefore classified as a general process parameter (GPP).
> — A-Mab, p. 132

> Risk analysis, process characterization studies and process performance history demonstrate
> that the Protein A step does not have any Critical process Parameter (CPPs). Only two
> parameters were linked to CQAs (Protein Load and Elution buffer pH) and were classified as
> WC-CPP based control capabilities to operate within the proposed design space.
> — A-Mab, p. 125

> These results confirm that the total filtration volume is important for assuring effective
> removal of virus. Because the volumetric load is easy to control, it was classified as a
> WC-CPP.
> — A-Mab, p. 157

> Since pressure is easy to control it was classified as a WC-CPP and not a CPP.
> — A-Mab, p. 157

**Note.** This is the single most useful passage set in the file for the classification
section. The A-Mab p. 132 passage classifies four parameters in five sentences, each with
its reason attached by "because", "Similarly … because", or "and was therefore classified
as". The p. 157 example does it in fourteen words. Do not write a paragraph per parameter
where a sentence will do.

---

## 13. Viral clearance and cross-step credit

> Consistent with the FDA Points to Consider in the Manufacture and Testing of Monoclonal
> Antibody Products for Human Use (1997), the modular clearance study demonstrated virus
> removal or inactivation in individual steps during the purification process. Here, each
> module in the purification scheme was studied independently of the other modules.
> — A-Mab, p. 116

> The results obtained for five antibodies purified using similar purification steps with well
> characterized mechanisms of removal or inactivation showed that there is less than 1
> retrovirus particle for every 1.67 x 109 doses of antibody, thus presenting a minimal risk to
> patient safety. This assessment is based on three of five purification steps namely, low pH
> treatment, anion exchange chromatography and small virus retentive filtration. Prior product
> knowledge indicates that cation exchange chromatography usually removes approximately 2 logs
> of XMuLV and Protein A chromatography exhibits robust removal of 4-6 logs based on the flow
> through fraction from a spiked load (without the low pH elution). Collectively, these steps
> typically remove 4-8 logs of XMuLV, resulting in an overall 12-18 log safety margin with a
> minimal risk to patient safety.
> — A-Mab, p. 167

> It should be noted that although virus breakthrough may be observed for MVM at higher
> volumetric loads, no breakthrough has been observed with XMuLV in any mAb processes that use
> this type filter, even under conditions when the typical load volumes are exceeded.
> — A-Mab, p. 157

**Note.** The p. 167 passage is cross-step credit done properly: which steps the claim rests
on, which steps contribute but are not claimed, and the cumulative figure last.

---

## 14. Conclusions and the contribution to the control strategy

> Results of Protein A step characterization studies demonstrated that this step does not
> impact the distribution of product variant CQAs (e.g. acidic isoforms). Moreover, this step
> was shown to have robust process performance even when challenged with a wide range of feed
> stream inputs (HCP, DNA, Titer, and Viability).
> — A-Mab, p. 125

> The proposed control strategy for the downstream process has a dual purpose: 1) Ensure
> product quality and safety, 2) Ensure that the commercial manufacturing process is consistent
> and robust. Product quality and safety are ensured by controlling all quality-linked process
> parameters (CPP and WC-CPP) within the limits of the design space. Process consistency is
> ensured by controlling key process parameters (KPPs) within established limits and by
> monitoring relevant process attributes.
> — A-Mab, p. 164

> Although key process parameters and key process attributes have been shown not to impact
> product quality, they are included in the control strategy because their monitoring and
> control ensures that the process is operated in a consistent and predictable manner.
> — A-Mab, p. 93

> In conclusion, the cumulative process understanding gained from prior knowledge, results from
> process characterization studies and risk analysis show that the A-Mab seed expansion steps
> from vial thaw through N-1 seed bioreactor do not impact product quality and thus do not need
> to be included in the definition of the design space.
> — A-Mab, p. 68

---

## 15. Deviations, limitations and things that went wrong

This is the hardest register to fake, and A-Mab is rich in it. The recurring shape is:
**state the problem plainly, give the mechanism, state the disposition, then state what is
or is not claimed as a result.**

**A worse result, dispositioned by downstream capability:**

> In most cases, the levels of host-cell or media-derived impurities were similar or better for
> Resin B than for Resin A. For leached Protein A levels, however, for Resin B had modestly
> higher levels of leached Protein A (up to two-fold higher), yet subsequent processing steps
> removed the leached Protein A to comparable levels using an appropriate qualified assay,
> indistinguishable from material produced by Resin A.
> — A-Mab, p. 127

**A real effect deliberately not claimed, because it is not predictable:**

> Note: Precipitation of HCP often occurs during low pH inactivation and is removed during
> subsequent depth filtration. However, the clearance is not predictable and for the purposes
> of this case study HCP clearance will not be claimed in this step. Therefore, the HCP output
> level of the Protein A chromatography step will be assumed to carry through low pH
> inactivation to serve as the input for cation exchange chromatography.
> — A-Mab, p. 127

**An adverse trend characterized rather than hidden:**

> Based on process characterization studies, the LRF achieved for MVM in the small virus
> retentive filters decreases slightly with increasing load volume. To further characterize
> this observation, MVM breakthrough was assessed as a function of load volume challenge.
> — A-Mab, p. 156

**An off-target result explained by mechanism, then used as evidence for the model:**

> Of particular interest is the process performance of the 5K bioreactor; where the average
> titer was approximately 15% lower than in the 15K commercial scale. The lower titer is a
> consequence of a lower Integral of Viable Cell Concentration (IVC) that is associated with
> the higher pCO2 accumulation at the 5K scale. These results are aligned with the multivariate
> model predictions based on DOE studies that show higher pCO2 levels lead to lower IVCs and
> thus lower titers.
> — A-Mab, p. 105

**An analytical limitation forcing extra work:**

> The sensitivities of the assays for methotrexate and Antifoam C were insufficient to
> determine the effectiveness of clearance by process mapping. Therefore, the clearance of
> these two cell culture impurities over Protein A chromatography was determined with spiking
> studies using the laboratory model developed for the process characterization.
> — A-Mab, p. 169

**Limitations stated flatly, without cushioning:**

> However, it is recognized that such a reduced number of batches cannot adequately capture the
> expected process variability at commercial manufacturing scale.
> — A-Mab, p. 108

> Design spaces are not confirmed at scale at the edges of the ranges.
> — A-Mab, p. 263

> In this case study, both the low and high limits for galactosylation and afucosylation were
> exceeded when the process was operated within the tested ranges thus defining edges of
> failure and imposing limits within the multidimensional cubic form of the knowledge space.
> — A-Mab, p. 90

**The normative framing from the guidance:**

> Protocol excursions and unexpected results should be included and fully described in the
> report. A reference to the root cause analysis should be provided if documented separately
> from the PPQ report. Any corrective actions and their impact on PPQ should be outlined in
> the report.
> — PDA TR 60, printed p. 42 / extract p. 50

**Note.** "Design spaces are not confirmed at scale at the edges of the ranges." Eleven
words, no cushioning, no mitigation attached. A limitation does not need a paragraph.

---

# Part 2 — Sentence-level habits

## The connective inventory

These are the connectives the two documents actually use:

*Therefore · Thus · However · Since · Because · By contrast · In addition · On the other
hand · As expected · While · Although · Moreover · Furthermore · Also · For this reason ·
Consequently · In these cases · Collectively · First / Finally · Note that · Notice that*

They rarely use "rather than" (about 0.1 per 1000 words, against 3.3 in the first-pass
corpus), and they do not build "not X but Y" constructions. Notice how often the connective
carries a *decision* rather than just a fact:

> Since subsequent steps (AEX and CEX) can reduce HCP to safe and consistent levels, the
> acceptable HCP output levels from the Protein A are linked to the operating conditions of
> these subsequent steps.
> — A-Mab, p. 125

> Because there are no claims for virus removal by this chromatography step, there are no data
> generated on virus clearance by Resin B.
> — A-Mab, p. 127

> Therefore, aggregate removal does not constrain the design space of the CEX step.
> — A-Mab, p. 138

> Since there are no further reduction/clearance steps for aggregate downstream of the CEX
> step, it is important to demonstrate that this step consistently reduces aggregate to
> acceptable levels for drug substance.
> — A-Mab, p. 138

> This approach is justified because the purity of the feed-stream after Protein A
> chromatography is sufficiently high and consistent that no significant differences are
> expected in the CEX process performance with different mAbs.
> — A-Mab, p. 139

> By contrast, the extensive prior knowledge has demonstrated that the distribution of
> glycosylation variants (e.g. galactosylation and fucosylation) is minimally impacted by
> downstream processing and is mainly influenced by the upstream process conditions.
> — A-Mab, p. 116

### The step after the full stop

Where the connective sits matters as much as which one it is. In all four sources the premise
finishes as a sentence and the consequence opens the next one. The corpus does the opposite: it
joins the two with ", so " in 6 to 11 % of its sentences and opens 0 to 2 % of them with a
connective, against 3.7 to 6.1 % in the sources. Read these as pairs, not as single sentences.

> At an early stage of process development, the information available on product attributes may
> be limited. For this reason, the first set of CQAs may come from prior knowledge obtained
> during early development and/or from similar products rather than from extensive product
> characterization.
> — PDA TR 60, printed p. 13 / extract p. 21

> The specifics of the CPV sampling/testing strategy may not be finalized until completion of
> PPQ. Therefore, the process validation master plan may include general commitments to the
> planned CPV strategy.
> — PDA TR 60, printed p. 44 / extract p. 52

> Results also showed that there are no Critical Process Parameters (CPPs) in Step 3 since all
> parameters are well controlled within their acceptable limits and have demonstrated robust
> process operation. Thus, all quality-linked process parameters for Step 3 were classified as
> WC-CPPs.
> — A-Mab, p. 87

> In many regulatory regions, a minimum of three successful, consecutive lots are used. However,
> other regulatory bodies may accept more (or less) lots depending on the knowledge available for
> the product.
> — ISPE Technology Transfer, printed p. 93 / extract p. 95

**Note.** Each first sentence is complete on its own and each second sentence carries one step,
not two. The A-Mab pair is the one to study: the finding and its evidence sit in sentence one,
including a "since" clause, and the classification that follows from them gets its own sentence
and its own connective. A corpus author would have written all of it as one sentence with
", so … , and …".

### The study is the patient, not the agent

A decision is made by people and reported in the passive. The study, the design and the model are
what the decision was made *from*, so they sit in a prepositional phrase or in the subject of a
verb that reports what they contained, never as the agent that retained, carried or selected
anything. The four sources put a passive construction in 57 to 64 % of their sentences. The
corpus report re-authored in round two was at 35 %, and what avoiding the passive produced there
was "the 4 factors that screening retained".

> The process model included two main effects as well as a non-linear interaction term. Based on
> these results, flow rate and end collection (CV) were classified as Key Process Parameters
> (KPPs).
> — A-Mab, p. 122

> The experimental design used was a fractional factorial in order to determine the critical
> formulation parameters for further characterization. The critical formulation parameters were
> identified as pH and protein concentration for aggregation and polysorbate 20 level for
> particulate matter.
> — A-Mab, p. 184

> From studies with three other mAbs as well as information supplied by the filter manufacturer,
> filtration load volume, chase volume, and filtration pressure were identified as process
> parameters that potentially impact the effectiveness of the virus removal for ―Type F‖ filters.
> — A-Mab, p. 153

> Potential process parameters that impact the CQAs were identified for each unit operation based
> on platform information.
> — PDA TR 60, printed p. 75 / extract p. 83

> Output parameters were classified as IPCs*, IPTs**, or In Process Measurements (IPMs). IPCs and
> IPTs were further classified as critical or not.
> — ISPE Practical Implementation, printed p. 152 / extract p. 154

**Note.** Read where the study went in each one. In the first it is the subject of *included*,
which reports what the model contained and decides nothing; the decision that follows is a
passive. In the second the design is the subject of a copula. In the third the studies are inside
"From studies with three other mAbs", a front field, and the parameters they informed are the
subject. A corpus author would have written "the model identified two main effects", "the
fractional factorial design determined the critical formulation parameters" and "studies with
three other mAbs identified filtration load volume", and each of those is a study doing something
a person did.

Reporting evidence is a different move and the sources do it in the active voice: "Results
showed", "studies showed", "the data shows", "The analysis shows". The distinction is whether the
verb reports an observation or a decision.

## Introducing and discussing a table or figure

The move is short. Almost always *[object] + verb + what it shows*, with the discussion
following in the next sentence.

> The Protein A risk ranking results are summarized in Table 4.7.
> — A-Mab, p. 120

> Table 4.8 lists the multivariate parameters and test ranges, their potential interactions,
> and rationale for inclusion in the study.
> — A-Mab, p. 121

> Samples were taken periodically and assayed for aggregation and changes in acidic variants.
> The results are given in Table 4.17.
> — A-Mab, p. 131

> The prediction profile displayed in Figure 4.5 shows the relative effects of each process or
> input parameter on yield, aggregate output, and HCP output.
> — A-Mab, p. 137

> The data in Figure 4.7 demonstrate the dependence of virus removal on the pH and conductivity
> of the anion exchange load, as well as the interactions between these parameters in the
> observed effects. The data also shows that there is little dependence of virus removal on the
> buffering salt system.
> — A-Mab, p. 146

> Another way to represent the multivariate equation is graphical depiction of contour plots
> (Figure 4.16). The green areas represent the design space and correspond to conditions that
> meet the HCP criteria. The red area represents conditions that do not meet the HCP criteria
> and thus are outside the design space.
> — A-Mab, p. 160

> Notice that the limits on acidic variants and soluble aggregates are not exceeded within the
> ranges tested in the DOEs.
> — A-Mab, p. 81

> However, by reviewing Figure 3.4 it is seen that its effect was very shallow.
> — A-Mab, p. 77

> Here only a selected subset of quality and process parameters is shown to exemplify the
> approach.
> — A-Mab, p. 142

They do not walk every row, and they do not append a significance clause to each one. They
name the rows that carry the argument and stop.

## Hedging

The hedges are ordinary words: *may, can, should, is expected to, appears, fairly, slightly,
generally, typically, in certain circumstances, potentially, is considered, desirable,
little or no*.

> The design space for this unit operation is fairly complex due to the interactions and
> non-linear behavior found in the DOE studies.
> — A-Mab, p. 81

> Also, a slight but not significant increase in the acidic variants was observed over the 240
> minute time course.
> — A-Mab, p. 130

> Although the extent of the effects may differ slightly, viral clearance decreases as pH
> decreases and conductivity increases.
> — A-Mab, p. 146

> The effect of protein concentration in the load was evaluated further in the viral clearance
> studies although it was not expected to have a significant impact on virus removal.
> — A-Mab, p. 147

> The data demonstrate that for the virus filter used in this study (Type-F), minimal flux
> decay is observed at filtration volumes as high as 124 L/m2, suggesting there is no
> appreciable degree of pore plugging.
> — A-Mab, p. 153

> Previous univariate experiments have indicated that antibody precipitation may occur at pH
> 3.1 or below. Therefore pH 3.2 was chosen as the lowest pH to assure precipitation did not
> occur during the study.
> — A-Mab, p. 129

> Platform process conditions might not be optimal for all cell lines, but have been
> demonstrated to result in consistent and robust process performance.
> — A-Mab, p. 70

> Although mixing time is an average bulk measurement and thus cannot describe the possibility
> for non-homogeneity, it provides valuable information on the performance of the bioreactor.
> — A-Mab, p. 100

Note the last two. An adverse fact comes first, then its bounded value, in one plain sentence
joined by "but" or "although". That is adverse-before-mitigation in its natural register.

## Sentence length

Aim for a mean near 24 words and a median near 22. Write some sentences of six words. The two
sources put roughly one sentence in five under 15 words, and fewer than one in ten over 40.

If you have written a 45-word sentence, it is almost always two sentences with a full stop
missing from the middle.

---

# Part 3 — The argument moves

Parts 1 and 2 teach what a section says and how a sentence sounds. This part teaches the seven
moves that carry an **argument**, which is the layer the corpus was missing. They were found by
parsing the four sources and pulling out the sentences that instantiate each construction, so
every example here is a real sentence somebody published, not a shape invented to illustrate a
rule.

Read this part beside `WRITING_GUIDE.md` §2c and §2d. Four of the seven have a worked correction
there, built from a real corpus sentence. Here you get the passages.

## 16. The frame comes before the subject

Human sentences carry about nine tokens before the main verb; corpus documents carry six. The
difference is not length, it is what the opening slot holds. The sources put the case in hand,
the condition, the basis or the contrast there. The corpus puts a counter: *First*, *Second*,
*For galactosylation*.

> In order to meet anticipated commercial demand, Process 1 was further optimized to increase
> product titers while ensuring no significant impact on product quality.
> — A-Mab, p. 71

> For the purposes of this case study, only a subset of quality attributes was considered in
> the analysis of drug substance and drug product development; these include aggregate,
> galactosylation, a-fucosylation, deamidation, and HCP.
> — A-Mab, p. 64

> Occasionally, the science behind a process will be understood well enough to skip screening
> and 2-level factorial experiments and start with response surface experiments.
> — PDA TR 60, printed p. 58 / extract p. 66

> Once the overall risk level is estimated for each gap, the team should determine the need
> for risk mitigation based on acceptability of risk and then prioritize activities.
> — ISPE Technology Transfer, printed p. 40 / extract p. 42

> When designing experiments to determine the multivariate ranges or PARs of CPPs, both
> measurement uncertainty and common cause variability of the commercial manufacturing
> equipment should be considered.
> — ISPE Practical Implementation, printed p. 37 / extract p. 39

**Note.** *In order to*, *For the purposes of*, *Occasionally*, *Once*, *When designing*. Each
tells the reader what kind of sentence is coming before the sentence arrives. None of them is a
number.

---

## 17. The main verb names the event

`be` is the root verb of about one sentence in six in the human sources and of one in three in
`PCR-003`. When something happened, a lexical verb says so.

> Collectively, these steps typically remove 4-8 logs of XMuLV, resulting in an overall 12-18
> log safety margin with a minimal risk to patient safety.
> — A-Mab, p. 167

> Longer culture times resulted in higher titers and lower a-fucosylation levels.
> — A-Mab, p. 73

> Increasing airflow rate strips carbon dioxide and thus reduces pH and potentially leads to
> an overall reduction of caustic addition.
> — A-Mab, p. 103

> Protein loads on the AEX Membrane uniformly exceeded 10 gram/ml in these studies, providing
> a worst case value for the maximum AEX Membrane load in the manufacturing process.
> — A-Mab, p. 148

> The use of media such as hydrolysates or that contain animal components can introduce more
> variability into a process, which can affect process comparability between sites.
> — ISPE Technology Transfer, printed p. 79 / extract p. 81

**Note.** *remove*, *resulted in*, *strips*, *reduces*, *leads to*, *exceeded*, *introduce*,
*affect*. Not one of these passages says *X is a Y of Z*. This is the move a screening-effects
section needs most, and it is the one most often replaced by a copula.

---

## 18. Concede first, then commit

The concession goes first and subordinated. The commitment is the main clause, so it is what
survives a skim. Over the pages measured by `check_style.py --selftest`, `However` appears 59
times across the four sources. It appears twice in the whole corpus.

> However, sialylation variants are only present at very low levels in A-Mab and thus are not
> considered critical to product quality.
> — A-Mab, p. 116

> While these parameters are very valuable to describe bioreactor performance, on their own
> they do not provide sufficient information to predict possible non-homogeneity in the
> culture environment.
> — A-Mab, p. 97

> While univariate approaches are appropriate for some variables to establish a proven
> acceptable range (PAR), multivariate studies account for interactions between process
> parameters/material attributes (1).
> — PDA TR 60, printed p. 23 / extract p. 31

> Although site selection is not discussed in this Guide, facility fit and site expertise are
> important factors to consider as they can have significant impact on the timeline and costs.
> — ISPE Technology Transfer, printed p. 38 / extract p. 40

> The measured output of each step is preferable as an intermediate CQA or a final product
> CQA; however, if these cannot be measured directly, other measurements might be possible
> that indicate the performance and quality of the process.
> — ISPE Practical Implementation, printed p. 39 / extract p. 41

**Note.** The A-Mab sialylation passage does the whole job in 21 words: a turn, a reason and a
classification decision. The ISPE PV passage is the one to study for a caveat that has to stay
attached to its claim.

---

## 19. A finding is reported by a verb, and the qualification rides with it

*show*, *indicate*, *demonstrate*, *confirm*. The qualification stays in the same sentence
instead of being deferred to a later section, and it is stated in consequence terms.

> Results showed worst case at the following bioreactor conditions: High pH, high Temp, high
> iVCC, and late harvest.
> — A-Mab, p. 73

> Moreover, results show that process performance has been consistent and robust demonstrating
> that all three options may be used to culture cells in the seed expansion stage.
> — A-Mab, p. 65

> This prior information has demonstrated that the cell culture expansion steps are robust and
> reproducible in different scale of operations and bioreactor configurations.
> — A-Mab, p. 66

> Qualification should demonstrate that the equipment is designed appropriately, built to suit
> user and process requirements, and fit for its intended use.
> — ISPE Practical Implementation, printed p. 50 / extract p. 52

**Note.** The A-Mab worst-case sentence is 18 words and settles a question. Compare it with the
same finding reported as *the worst case was found to be associated with*, which is longer, has a
copula for a main verb and commits to less.

---

## 20. Modality carries the risk posture

**This is the plan-genre gap, and it is the largest one measured.** `should` runs at 11.5 per
1000 words in ISPE Technology Transfer and 11.2 in PDA TR 60. Across all twenty corpus documents
it runs at **0.23**, which is 27 occurrences in 119,000 words, and twelve documents never use it
at all. `may` shows the same collapse: 7.9 and 7.8 in the two guides, 0.13 in the corpus.
`PCP-003` answers with `will` at 19.7 per 1000 words against a human 2.0 to 3.3.

A plan does three different things and needs three different modals. `will` commits. `may`
permits and leaves the choice open. `should` recommends and admits a considered exception.
Flattening all three into `will` reads as a machine issuing instructions.

> Specific success criteria should be documented in the technology transfer plan.
> — ISPE Technology Transfer, printed p. 28 / extract p. 30

> Depending upon the complexity of the project, a technical lead and project manager may be
> the same person.
> — ISPE Technology Transfer, printed p. 32 / extract p. 34

> If the process or analytical method qualification does not meet the acceptance criteria, the
> cause of the failure should be investigated and addressed before repeating the exercise.
> — ISPE Technology Transfer, printed p. 47 / extract p. 49

> Due to the dependence of aggregation on pH, the formulation range for pH should not exceed
> 5.6.
> — A-Mab, p. 186

> CQAs for commercial products should be defined prior to initiation of Stage 2 activities.
> — PDA TR 60, printed p. 14 / extract p. 22

**Note.** Four sentences, four postures: a documentation requirement, a permission, a
conditional obligation, a hard limit with its mechanism given, and a deadline. Only the A-Mab
one states a number, and it is the only one that needs to.

---

## 21. The author manages the reader

The sources steer attention. They say what to skip, what to notice and what a chapter is for.
Across the whole corpus, *we*/*our* and *Note that*/*Notice that* are **zero**, and *For example*
occurs **once** in 119,000 words against 0.2 to 1.3 per 1000 words in the four sources.

> If the reader is not interested in studying the data and rationale that support the above
> statement, the reader can skip this section and go to Step 3 (Production Bioreactor).
> — A-Mab, p. 65

> However for purpose of brevity, only data for MVM and XMuLV are provided in the case study.
> — A-Mab, p. 116

> This chapter can be read as a stand-alone guide for drug substance technology transfer.
> — ISPE Technology Transfer, printed p. 67 / extract p. 69

> Note that many of the principles of drug substance transfer, covered in Chapter 5, are
> applicable to drug products.
> — ISPE Technology Transfer, printed p. 83 / extract p. 85

**Note.** The A-Mab "skip this section" passage is worth reading twice. A published case study
tells its reader not to read part of it. A document that treats every attribute identically
forces the reader to weigh them all, which is the uniformity §7 of the writing guide already
calls a signal of machine authorship.

---

## 22. State the scope you are not covering

Name the limit of the method inside the section that uses it, not in a general caveat at the
end.

> In a real-life case scenario, the examples and approaches described here would include all
> relevant product quality and material attributes.
> — A-Mab, p. 64

> This type of experimental design is not able to resolve all the interactions between
> parameters and it would have to be augmented on the subset of parameters shown to impact
> CQAs.
> — A-Mab, p. 77

> This "one-factor-at-a-time" type of experimentation cannot determine process parameter
> interactions, where the effect of one parameter on a quality attribute differs depending on
> the level of the other parameters.
> — PDA TR 60, printed p. 57 / extract p. 65

> The focus of this chapter is on the product and process specific requirements of the
> technology transfer (from the initial high level technology transfer proposal to operational
> readiness and process/procedure qualification) as analytical method requirements are covered
> in Chapter 4.
> — ISPE Technology Transfer, printed p. 67 / extract p. 69

**Note.** *is not able to resolve*, *cannot determine*, *would include*, *are covered in Chapter
4*. Three of the four name what the reader should go and read instead. The corpus does this well
once, in `PCR-003`'s "Three bounds apply to this claim", and almost nowhere else.

---

## 23. Carrying the topic forward

The subject of a sentence opens on something the sentence before it established. Measured over
the pages the self-test reads, the four sources do this in 57.0 to 61.9 % of their sentences.
The 20 corpus documents manage a median of 36.3 %, so two sentences in three start a fresh
topic. `WRITING_GUIDE.md` §2d states the rule and now carries three worked corrections; these
are the passages to imitate.

> The cultures from this study were subsequently passaged into the production bioreactor stage
> also performed in a 2L scaled-down bioreactor. The production bioreactor stage was operated
> at the set-point conditions. The harvest samples from the production bioreactor were tested
> for product quality.
> — A-Mab, p. 67

> This assessment identified the production bioreactor as the only upstream process step that
> posed a significant risk to product quality. The other process steps (seed expansion and
> harvest) had a low risk of impact to product quality.
> — A-Mab, p. 64

> Team leads should assemble the technology transfer core team by including required SMEs. The
> composition of the core team is determined by the process being transferred and the required
> expertise to support the transfer.
> — ISPE Technology Transfer, printed p. 32 / extract p. 34

> Measurement uncertainty is commonly managed by reducing the PAR or multivariate limits (as
> applicable) to a value inside the limit determined during development. These tighter limits
> can be included in the batch records as alert limits or decision limits. Typically, these
> new limits are determined based on a selected level of statistical assurance that the actual
> value is within the PAR or multivariate range for interacting parameters.
> — ISPE Practical Implementation, printed p. 37 / extract p. 39

**Note.** Watch what the subjects do. *The cultures* → *The production bioreactor stage* → *The
harvest samples from the production bioreactor*. *Team leads* → *the core team*. *the PAR or
multivariate limits* → *These tighter limits* → *these new limits*. Every one of them repeats a
noun from the sentence before rather than reaching for a synonym, which is the habit §2 of this
file's opening notes already asks for. Chaining and noun repetition are the same discipline.
