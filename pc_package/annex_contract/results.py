"""Study-result contracts — capability, modular contributions, performance, model fit.

Added in SCHEMA_VERSION 0.4. `studies.py` holds what a study *was*; this holds what it
*found*, which had no home at all.

Two independent lines of evidence name these fields, which is why they are being added now
rather than argued about:

**Measured, from open extraction.** Extracting one characterization report with no schema
and mapping the result back put 56–61% of findings outside the contract. The largest
recurring groups were statistical model summaries (×8), process capability (×4) and
per-step clearance claims (×4). See `docs/results/2026-07-27-schema-arms.md`.

**Declared, by the corpus author.** Independently, `out_of_schema_notes` in the ground truth
annexes says the same thing in the author's own words: *"Process-capability (Cpk) values
have no dedicated field"* (PCR-003, PCMR-001, PTP-001), *"cumulative viral clearance
(18.87 / 10.03) … no dedicated field"* (PCMR-001), *"Process-performance measures (yield,
turbidity, throughput) have no dedicated field"* (PCP-004, PCP-010, PCR-004, PCR-010),
*"Per-step MVM/XMuLV log-reductions are modular contributions with no released spec"*
(PCP-009, PCR-009).

Both lines point at the same fields. That is a stronger basis than either alone, because
the second was written by someone who had not seen the first.

**Still provisional.** The evidence is one synthetic corpus and one document class. These
models are additive and optional everywhere, so a document set that never mentions
capability simply leaves them empty. What is *not* claimed is that this list is complete.
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from .base import ExtractionMetadata, SourceReference

#: Which side of the acceptance range a capability index is evaluated against. A one-sided
#: index compared to the wrong bound is not a smaller error than a wrong number — it
#: silently inverts the margin.
SpecificationSide = Literal["upper", "lower", "two_sided"]

#: Where a capability figure comes from. A simulated index and an index from real batches
#: support very different claims, and a report that conflates them is making the stronger
#: one without saying so.
CapabilityBasis = Literal["simulated", "observed", "unspecified"]


class ProcessCapability(BaseModel):
    """A capability index for one quality attribute, with what it was computed from.

    `basis` and `n_batches` are not decoration. "Cpk = 1.51" from a Monte-Carlo simulation
    of 2,000 batches within the normal operating ranges and "Cpk = 1.51" from a five-batch
    qualification campaign are different claims, and only the second is evidence about the
    commercial process. Recording the number without its basis loses the distinction that
    a reviewer cares about most.
    """
    model_config = ConfigDict(extra="forbid")

    capability_id: str
    quality_attribute: str
    #: Cpk, Ppk, or whatever the document reports. Kept as written.
    index_name: Optional[str] = None
    index_value: Optional[float] = None
    specification_side: Optional[SpecificationSide] = None
    acceptance_range: Optional[str] = None
    mean: Optional[str] = None
    standard_deviation: Optional[str] = None
    unit: Optional[str] = None
    basis: CapabilityBasis = "unspecified"
    n_batches: Optional[int] = None
    unit_operation: Optional[str] = None
    #: True when the document claims this is the lowest capability in the process. That
    #: claim is checkable across documents and, on this corpus, two reports disagree
    #: about it — which is exactly the kind of defect cross-document grounding exists for.
    claimed_process_minimum: bool = False
    source_references: list[SourceReference] = Field(default_factory=list)
    metadata: ExtractionMetadata = Field(default_factory=ExtractionMetadata)


class ModularContribution(BaseModel):
    """One step's contribution to a cumulative, cross-step quantity.

    Viral clearance is the clearest case: no single step clears a virus to specification,
    the claim is the sum across independent mechanisms, and the acceptance criterion is
    cumulative. Yield behaves the same way — a step yield of 97.7% contributes to an
    overall 83.2%.

    Modelling this as its own object rather than as a value on the attribute is what makes
    the ledger checkable. A cumulative total that does not equal the sum of its stated
    contributions is a defect, and it cannot be seen while the contributions live only in
    prose.
    """
    model_config = ConfigDict(extra="forbid")

    contribution_id: str
    #: What is accumulating — "Viral clearance — XMuLV (enveloped)", "step yield".
    quantity: str
    unit_operation: Optional[str] = None
    step_value: Optional[str] = None
    cumulative_value: Optional[str] = None
    requirement: Optional[str] = None
    unit: Optional[str] = None
    #: The other steps credited with the same quantity, when the document names them.
    #: Independence is what licenses adding the contributions up, so a document that
    #: claims a sum should also say why the mechanisms are independent.
    contributing_steps: list[str] = Field(default_factory=list)
    source_references: list[SourceReference] = Field(default_factory=list)
    metadata: ExtractionMetadata = Field(default_factory=ExtractionMetadata)


class PerformanceMeasure(BaseModel):
    """A measured process-performance result that is not a released quality attribute.

    Step yield, turbidity, filter throughput, buffer-exchange completeness, an in-process
    pool concentration. These govern whether a step works, they are characterized and
    ranged like any parameter, and `QualityAttribute` is the wrong home because they carry
    no drug-substance specification.

    Two whole unit operations in the benchmark corpus — harvest and UF/DF — form no quality
    attribute at all and are justified entirely on these. Without this model their reports
    extract to almost nothing, which is what the arm comparison showed.
    """
    model_config = ConfigDict(extra="forbid")

    measure_id: str
    measure_name: str
    unit_operation: Optional[str] = None
    value: Optional[str] = None
    unit: Optional[str] = None
    #: The basis stated for the result — "mass balance across primary recovery",
    #: "within NOR 1-10 NTU". Usually the only thing that makes the number interpretable.
    basis: Optional[str] = None
    normal_operating_range: Optional[str] = None
    #: True for an in-process response with no released specification, e.g. eluate-pool
    #: HCP. The corpus author flagged these repeatedly as having nowhere to go.
    in_process_only: bool = False
    source_references: list[SourceReference] = Field(default_factory=list)
    metadata: ExtractionMetadata = Field(default_factory=ExtractionMetadata)


class ModelTerm(BaseModel):
    """One term in a fitted model, with the evidence for its effect.

    This is what makes an impact claim quantitative. `parameter_impacts_attribute` could
    already record *that* pH affects the log-reduction; it could not record that the
    standardized effect is -2.08 with p = 0.000376, while a different term sits at 0.203
    with p = 0.34. After extraction a dominant effect and a statistically insignificant
    one looked identical, which is the single most misleading thing the contract did.
    """
    model_config = ConfigDict(extra="forbid")

    #: The term as the document labels it — "A", "BC", "Culture pH".
    term: str
    #: The factor the label refers to, when the document gives a key.
    factor: Optional[str] = None
    effect: Optional[float] = None
    coefficient: Optional[float] = None
    standard_error: Optional[float] = None
    t_statistic: Optional[float] = None
    p_value: Optional[float] = None
    significant: Optional[bool] = None


class ControlStrategyElement(BaseModel):
    """One element of the control strategy a step contributes.

    The control strategy is the deliverable of a characterization report — "control the
    CPP to a tight NOR with in-process pH verification", "end-of-hold testing of aggregate
    and charge variants". Five recurring instances in a single report had no field, and a
    summary that omits them omits the point of the document.
    """
    model_config = ConfigDict(extra="forbid")

    element_id: str
    description: str
    unit_operation: Optional[str] = None
    #: What is being controlled — a parameter, an attribute, a step.
    controls: Optional[str] = None
    #: "in-process monitoring", "end-of-hold testing", "procedural", "specification".
    control_type: Optional[str] = None
    source_references: list[SourceReference] = Field(default_factory=list)
    metadata: ExtractionMetadata = Field(default_factory=ExtractionMetadata)


class StatisticalModelFit(BaseModel):
    """The fit statistics that decide whether a claimed effect is supported.

    The typed contract could already record *that* a parameter impacts an attribute. It
    could not record how strongly, how precisely, or whether the model was adequate — so a
    dominant effect and a marginal one were indistinguishable after extraction.

    `lack_of_fit_p` matters more than it looks. A model with a high coefficient of
    determination and a significant lack of fit is not adequate, and reporting the first
    without the second is the most common way a weak model is made to look strong.
    """
    model_config = ConfigDict(extra="forbid")

    model_fit_id: str
    response: str
    unit_operation: Optional[str] = None
    #: "screening", "response surface", "full quadratic" — as the document names it.
    model_form: Optional[str] = None
    n_runs: Optional[int] = None
    r_squared: Optional[float] = None
    adjusted_r_squared: Optional[float] = None
    predicted_r_squared: Optional[float] = None
    f_statistic: Optional[float] = None
    p_value: Optional[float] = None
    rmse: Optional[float] = None
    lack_of_fit_p: Optional[float] = None
    #: The document's own verdict — "adequate", "excellent", "not significant".
    adequacy_statement: Optional[str] = None
    #: Per-term effect evidence. Without it an impact claim carries no strength.
    terms: list[ModelTerm] = Field(default_factory=list)

    # -- replicate statistics, which are the pure-error term ------------------------
    #: Mean, standard deviation and coefficient of variation over replicated centre
    #: points. These are what the lack-of-fit test is measured against, and they set the
    #: resolution of the whole study: an effect smaller than the replicate scatter cannot
    #: be separated from assay noise, however small its p-value looks.
    replicate_n: Optional[int] = None
    replicate_mean: Optional[str] = None
    replicate_sd: Optional[str] = None
    replicate_cv: Optional[str] = None
    source_references: list[SourceReference] = Field(default_factory=list)
    metadata: ExtractionMetadata = Field(default_factory=ExtractionMetadata)


class Deviation(BaseModel):
    """A recorded departure from the plan, with its disposition.

    A deviation that invalidated a study and forced re-execution changes how every result
    in that report should be read. On this corpus one did exactly that, and the corpus
    author noted the deviations were "narrative" — meaning the annex could not hold them.
    A summary that omits them is not merely incomplete; it is more reassuring than the
    evidence supports.
    """
    model_config = ConfigDict(extra="forbid")

    deviation_id: str
    summary: str
    unit_operation: Optional[str] = None
    detected_during: Optional[str] = None
    #: "retained", "corrected", "re-executed", "excluded" — as written.
    disposition: Optional[str] = None
    impact_statement: Optional[str] = None
    #: True when the document says this changed no classification and no operating
    #: boundary. The claim is worth recording separately because it is the one a reviewer
    #: will want to check.
    no_impact_on_conclusions: bool = False
    source_references: list[SourceReference] = Field(default_factory=list)
    metadata: ExtractionMetadata = Field(default_factory=ExtractionMetadata)
