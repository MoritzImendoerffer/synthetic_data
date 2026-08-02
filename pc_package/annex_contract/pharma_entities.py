"""CMC / manufacturing entity contracts (Phase 3 extraction targets)."""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

from .base import ExtractionMetadata, SourceReference
from .discourse import DocumentRelationship, ExplicitNonClaim
from .results import (
    ControlStrategyElement,
    Deviation,
    ModularContribution,
    PerformanceMeasure,
    ProcessCapability,
    StatisticalModelFit,
)
from .studies import DesignSpace, StudyDesign

#: The criticality continuum. ``WC-CPP`` (well-controlled CPP) and ``GPP`` (general
#: process parameter) were added in SCHEMA_VERSION 0.3: the A-Mab continuum and ICH Q8
#: risk-based classification both use them, and treating them as ``unclassified`` loses
#: the majority of parameters in a characterization report.
ParameterType = Literal["CPP", "WC-CPP", "KPP", "GPP", "non_critical", "unclassified"]

#: Parameter classifications that carry a criticality claim and therefore belong in a
#: control strategy. Prefer this over comparing against ``"CPP"`` alone.
CRITICAL_PARAMETER_TYPES: frozenset[str] = frozenset({"CPP", "WC-CPP"})

#: Risk-ranking band for a quality attribute (A-Mab Tool #1/#2).
CriticalityLevel = Literal["VL", "L", "L-M", "M", "M-H", "H", "VH"]


class ManufacturingSite(BaseModel):
    site_id: Optional[str] = None
    site_name: str
    site_role: Optional[Literal["sending", "receiving", "testing", "packaging", "release", "unknown"]] = "unknown"
    location: Optional[str] = None
    source_references: list[SourceReference] = Field(default_factory=list)
    metadata: ExtractionMetadata = Field(default_factory=ExtractionMetadata)


class Equipment(BaseModel):
    equipment_id: Optional[str] = None
    equipment_name: str
    equipment_type: Optional[str] = None
    site_name: Optional[str] = None
    source_references: list[SourceReference] = Field(default_factory=list)
    metadata: ExtractionMetadata = Field(default_factory=ExtractionMetadata)


class ProcessStep(BaseModel):
    step_id: Optional[str] = None
    step_name: str
    step_number: Optional[str] = None
    unit_operation: Optional[str] = None
    description: Optional[str] = None
    input_materials: list[str] = Field(default_factory=list)
    output_materials: list[str] = Field(default_factory=list)
    equipment: list[str] = Field(default_factory=list)
    source_references: list[SourceReference] = Field(default_factory=list)
    metadata: ExtractionMetadata = Field(default_factory=ExtractionMetadata)


class ProcessParameter(BaseModel):
    parameter_id: Optional[str] = None
    parameter_name: str
    parameter_type: Optional[ParameterType] = "unclassified"
    unit: Optional[str] = None
    target_value: Optional[str] = None
    NOR: Optional[str] = None  # Normal Operating Range
    PAR: Optional[str] = None  # Proven Acceptable Range
    associated_step: Optional[str] = None
    rationale_for_criticality: Optional[str] = None
    #: How the parameter was studied — "multivariate", "univariate". Added in 0.4 because
    #: the corpus author recorded its absence: "Parameter study-type
    #: (multivariate/univariate) has no ProcessParameter field" (PCP-003). It decides how
    #: much a range is worth: a proven acceptable range from a multivariate design and one
    #: from a one-factor-at-a-time study support different claims.
    study_type: Optional[str] = None
    source_references: list[SourceReference] = Field(default_factory=list)
    metadata: ExtractionMetadata = Field(default_factory=ExtractionMetadata)


class QualityAttribute(BaseModel):
    attribute_id: Optional[str] = None
    attribute_name: str
    attribute_type: Optional[Literal["CQA", "KQA", "IPC", "release", "stability", "unclassified"]] = "unclassified"
    unit: Optional[str] = None
    acceptance_criteria: list[str] = Field(default_factory=list)
    analytical_method: Optional[str] = None
    associated_steps: list[str] = Field(default_factory=list)
    rationale_for_criticality: Optional[str] = None
    # Structured criticality, added in SCHEMA_VERSION 0.3 (additive, all optional).
    # rationale_for_criticality carries the prose; these carry the ranking behind it.
    criticality_level: Optional[CriticalityLevel] = None
    tool1_score: Optional[int] = None  # impact x uncertainty
    tool2_severity: Optional[int] = None
    source_references: list[SourceReference] = Field(default_factory=list)
    metadata: ExtractionMetadata = Field(default_factory=ExtractionMetadata)


class AnalyticalMethod(BaseModel):
    method_id: Optional[str] = None
    method_name: str
    method_type: Optional[str] = None
    analytes: list[str] = Field(default_factory=list)
    associated_attributes: list[str] = Field(default_factory=list)
    validation_status: Optional[str] = None
    source_references: list[SourceReference] = Field(default_factory=list)
    metadata: ExtractionMetadata = Field(default_factory=ExtractionMetadata)


class SectionEntityExtraction(BaseModel):
    """Target schema for section-level LLM (or coding-assistant) extraction.

    This is the contract injected into the entity-extraction prompt.

    The six original buckets carry the entities the pipeline was built for. The ten added
    in 0.4 carry what measurement said it was discarding: capability, modular
    contributions, process-performance results, model fit, deviations, document
    relationships, explicit non-claims, control-strategy elements, study designs and
    design spaces. Every one is optional, so a document set that never mentions them
    leaves them empty and nothing changes.

    All sixteen entity buckets are lists that default to empty, which is what makes this
    contract safe to extend. A consumer written against 0.3 keeps working, because the
    fields it reads have not moved.
    """
    document_id: str
    section_id: Optional[str] = None
    process_steps: list[ProcessStep] = Field(default_factory=list)
    parameters: list[ProcessParameter] = Field(default_factory=list)
    quality_attributes: list[QualityAttribute] = Field(default_factory=list)
    analytical_methods: list[AnalyticalMethod] = Field(default_factory=list)
    equipment: list[Equipment] = Field(default_factory=list)
    sites: list[ManufacturingSite] = Field(default_factory=list)

    # --- added in 0.4, evidenced by measurement and by the corpus author's own notes ---
    capabilities: list[ProcessCapability] = Field(default_factory=list)
    contributions: list[ModularContribution] = Field(default_factory=list)
    performance_measures: list[PerformanceMeasure] = Field(default_factory=list)
    model_fits: list[StatisticalModelFit] = Field(default_factory=list)
    deviations: list[Deviation] = Field(default_factory=list)
    document_relationships: list[DocumentRelationship] = Field(default_factory=list)
    non_claims: list[ExplicitNonClaim] = Field(default_factory=list)
    control_strategy: list[ControlStrategyElement] = Field(default_factory=list)
    #: Promoted from read-only in 0.4. `studies.py` shipped these in 0.3 so ground truth annexes
    #: would parse, deliberately kept out of the extraction target until there was
    #: evidence they occur in documents rather than only in an answer key. There is now:
    #: the open arms found designed experiments and design spaces repeatedly, with no
    #: field to put them in.
    studies: list[StudyDesign] = Field(default_factory=list)
    design_spaces: list[DesignSpace] = Field(default_factory=list)

    warnings: list[str] = Field(default_factory=list)
