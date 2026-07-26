"""Ground-truth annex schema for the A-Mab document package.

The ground-truth JSON annex for every document validates against
``GroundTruthAnnex`` (bottom of this file). Wherever the ``nlp_reports`` Pydantic
contract (``app/models`` in the sibling repo) already covers a concept, that model
is reused **verbatim** — same field names, same types. Where the contract has a
gap, a *local* extension is defined here, in this project, so that the
``nlp_reports`` repository is never modified.

Extensions added (and why the upstream contract could not express them):

  * ``ProcessParameter.parameter_type`` — upstream Literal only allows
    ``CPP | KPP | non_critical | unclassified``; the A-Mab continuum also uses
    ``WC-CPP`` (well-controlled CPP) and ``GPP`` (general process parameter),
    which every bioreactor parameter needs. Widened here.
  * ``DocumentInventoryItem.predicted_document_type`` — upstream DocumentType has
    no value for a characterization *plan*, *master plan* or *master report*, nor
    a *process transfer plan*. Added here.
  * ``QualityAttribute`` — upstream carries acceptance criteria but no structured
    criticality level / risk score; ``criticality_level`` / ``tool1_score`` /
    ``tool2_severity`` added (additive, optional).
  * ``StudyDesign`` / ``DesignSpace`` — no upstream model represents a designed
    experiment (DoE) or a multivariate design space, which are the central
    objects of a characterization plan/report. New models.

Each of these is a candidate to upstream into ``nlp_reports/app/models`` later;
that is a change to *that* repo and is intentionally left for its owner.
"""
from __future__ import annotations

import os
import sys
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

# Make the nlp_reports contract importable read-only, without modifying it.
_NLP_REPORTS = os.environ.get("NLP_REPORTS_PATH", "/home/moritz/github_repos/nlp_reports")
if _NLP_REPORTS not in sys.path:
    sys.path.insert(0, _NLP_REPORTS)

from app.models.base import ExtractionMetadata, SourceReference  # noqa: E402
from app.models.pharma_entities import (  # noqa: E402
    AnalyticalMethod,
    Equipment,
    ManufacturingSite,
    ProcessStep,
)
from app.models.pharma_entities import ProcessParameter as _ProcessParameter  # noqa: E402
from app.models.pharma_entities import QualityAttribute as _QualityAttribute  # noqa: E402
from app.models.pharma_entities import SectionEntityExtraction as _SectionEntityExtraction  # noqa: E402
from app.models.inventory import DocumentInventoryItem as _DocumentInventoryItem  # noqa: E402
from app.models.assertions import AssertionStore  # noqa: E402
from app.models.concepts import ConceptStore  # noqa: E402
from app.models.summaries import ReportSection, TransferGap  # noqa: E402

# Re-export the reused-as-is contracts so annex builders import everything from here.
__all__ = [
    "AnalyticalMethod", "Equipment", "ManufacturingSite", "ProcessStep",
    "ProcessParameter", "QualityAttribute", "DocumentInventoryItem",
    "SectionEntityExtraction", "StudyDesign", "DesignSpace", "ProvenAcceptableRange",
    "WeakClaim", "RhetoricalSpan",
    "AssertionStore", "ConceptStore", "ReportSection", "TransferGap",
    "SourceReference", "ExtractionMetadata", "GroundTruthAnnex",
]

# --------------------------------------------------------------------------- #
# Widened enums                                                               #
# --------------------------------------------------------------------------- #
ParameterType = Literal["CPP", "WC-CPP", "KPP", "GPP", "non_critical", "unclassified"]

CriticalityLevel = Literal["VL", "L", "L-M", "M", "M-H", "H", "VH"]

DocumentType = Literal[
    # --- reused verbatim from nlp_reports app/models/inventory.py ---
    "process_characterization_report",
    "process_validation_report",
    "technology_transfer_protocol",
    "technology_transfer_report",
    "control_strategy",
    "analytical_method",
    "analytical_method_validation_report",
    "specification",
    "batch_record",
    "risk_assessment",
    "manufacturing_process_description",
    "unknown",
    # --- local additions ---
    "process_transfer_plan",
    "process_characterization_plan",
    "process_characterization_master_plan",
    "process_characterization_master_report",
]


# --------------------------------------------------------------------------- #
# Extended entity models (widen a single field; everything else inherited)     #
# --------------------------------------------------------------------------- #
class ProcessParameter(_ProcessParameter):
    """nlp_reports ProcessParameter with the A-Mab WC-CPP / GPP designations added."""
    parameter_type: Optional[ParameterType] = "unclassified"


class QualityAttribute(_QualityAttribute):
    """nlp_reports QualityAttribute plus structured criticality (A-Mab Tool #1/#2)."""
    criticality_level: Optional[CriticalityLevel] = None
    tool1_score: Optional[int] = None
    tool2_severity: Optional[int] = None


class DocumentInventoryItem(_DocumentInventoryItem):
    """nlp_reports inventory item with characterization-plan document types added."""
    predicted_document_type: DocumentType = "unknown"


class SectionEntityExtraction(_SectionEntityExtraction):
    """nlp_reports section extraction using the extended parameter/attribute models."""
    parameters: list[ProcessParameter] = Field(default_factory=list)
    quality_attributes: list[QualityAttribute] = Field(default_factory=list)


# --------------------------------------------------------------------------- #
# New concepts (no upstream equivalent)                                        #
# --------------------------------------------------------------------------- #
class StudyDesign(BaseModel):
    """A designed characterization study for a unit operation.

    Represents a DoE (screening / response-surface), a univariate study, a risk
    assessment or a scale-down-model qualification. No nlp_reports model covers
    experimental design, so this is a local extension.
    """
    model_config = ConfigDict(extra="forbid")

    study_id: str
    study_type: Literal[
        "screening_doe", "response_surface_doe", "univariate",
        "one_factor_at_a_time", "risk_assessment", "scale_down_qualification",
    ]
    design_name: Optional[str] = None  # e.g. "resolution-V fractional factorial"
    unit_operation: Optional[str] = None
    factors: list[str] = Field(default_factory=list)
    responses: list[str] = Field(default_factory=list)
    n_runs: Optional[int] = None
    n_center_points: Optional[int] = None
    scale_down_model: Optional[str] = None
    associated_parameters: list[str] = Field(default_factory=list)
    source_references: list[SourceReference] = Field(default_factory=list)
    metadata: ExtractionMetadata = Field(default_factory=ExtractionMetadata)


class DesignSpace(BaseModel):
    """A multivariate design space / proven acceptable region. Local extension."""
    model_config = ConfigDict(extra="forbid")

    design_space_id: str
    unit_operation: Optional[str] = None
    parameters: list[str] = Field(default_factory=list)
    quality_attributes_constrained: list[str] = Field(default_factory=list)
    definition: Optional[str] = None
    source_references: list[SourceReference] = Field(default_factory=list)
    metadata: ExtractionMetadata = Field(default_factory=ExtractionMetadata)


class ProvenAcceptableRange(BaseModel):
    """A computed per-CQA×parameter proven acceptable range (PAR). Local extension.

    Two analyses: ``par_at_setpoint`` (other factors fixed) and ``par_nor_propagated``
    (other factors varied within NOR by Monte-Carlo of the fitted model). The acceptance
    basis is the study DS spec, or a back-calculated required step contribution for a
    cumulative viral-clearance CQA."""
    model_config = ConfigDict(extra="forbid")

    par_id: str
    unit_operation: Optional[str] = None
    quality_attribute: str
    parameter: str
    characterization_range: Optional[str] = None
    par_at_setpoint: Optional[str] = None
    par_nor_propagated: Optional[str] = None
    acceptance_basis: Optional[str] = None
    source_references: list[SourceReference] = Field(default_factory=list)
    metadata: ExtractionMetadata = Field(default_factory=ExtractionMetadata)


# --------------------------------------------------------------------------- #
# Discourse / benchmark-annotation extensions (no upstream equivalent).        #
# --------------------------------------------------------------------------- #
WeaknessType = Literal[
    "unsupported_prior_knowledge", "overstated_outcome",
    "unbounded_generalization", "missing_citation",
]


class WeakClaim(BaseModel):
    """A deliberately planted, LABELED unsupported/overstated claim (benchmark negative).
    It grounds (the quote exists in the document) but is labeled ``support='unsupported'``."""
    model_config = ConfigDict(extra="forbid")

    claim_id: str
    section: Optional[str] = None
    support: Literal["unsupported"] = "unsupported"
    weakness_type: WeaknessType
    source_reference: SourceReference
    rationale: Optional[str] = None
    correct_version: Optional[str] = None
    metadata: ExtractionMetadata = Field(default_factory=ExtractionMetadata)


RhetoricalRole = Literal[
    "problem_statement", "claim", "justification", "mechanistic_warrant", "hedge",
    "bounded_conclusion", "cross_step_credit", "deviation_disposition", "deferral",
    "restatement", "weak_claim",
]


class RhetoricalSpan(BaseModel):
    """A rhetorical-role span over the report text (discourse / argument structure).
    ``supported_by`` links a claim to its justification spans; ``restates`` links a
    restatement to the original claim; ``bounds`` links a bound to the claim it bounds."""
    model_config = ConfigDict(extra="forbid")

    span_id: str
    section: Optional[str] = None
    role: RhetoricalRole
    source_reference: SourceReference
    supported_by: list[str] = Field(default_factory=list)
    restates: Optional[str] = None
    bounds: Optional[str] = None


# --------------------------------------------------------------------------- #
# The composite annex wrapper                                                  #
# --------------------------------------------------------------------------- #
class GroundTruthAnnex(BaseModel):
    """Ground truth for one document, covering all target NLP tasks.

    Each block validates against a named model: ``inventory`` (document-type
    classification), ``entities`` (NER + entity linking, one entry per section),
    ``studies`` / ``design_spaces`` (characterization objects), ``report_sections``
    (extractive-summarization targets with statement-level citations),
    ``transfer_gaps`` (gap/QA), ``assertions`` (relation/QA), ``concepts``
    (canonical entity-linking targets). The wrapper is a container, not a new
    entity schema.
    """
    model_config = ConfigDict(extra="forbid")

    document_id: str
    document_title: str
    document_class: str
    version: str
    effective_date: str
    synthetic: bool = True
    schema_note: str = (
        "Blocks validate against nlp_reports app/models; parameter_type, "
        "document_type, QualityAttribute criticality fields, StudyDesign and "
        "DesignSpace are local extensions (see schema_extensions_used)."
    )
    schema_extensions_used: list[str] = Field(default_factory=list)
    out_of_schema_notes: list[str] = Field(default_factory=list)

    inventory: DocumentInventoryItem
    entities: list[SectionEntityExtraction] = Field(default_factory=list)
    studies: list[StudyDesign] = Field(default_factory=list)
    design_spaces: list[DesignSpace] = Field(default_factory=list)
    proven_acceptable_ranges: list[ProvenAcceptableRange] = Field(default_factory=list)
    report_sections: list[ReportSection] = Field(default_factory=list)
    transfer_gaps: list[TransferGap] = Field(default_factory=list)
    assertions: Optional[AssertionStore] = None
    concepts: Optional[ConceptStore] = None
    # discourse / benchmark-annotation layers (local extensions)
    weak_claims: list[WeakClaim] = Field(default_factory=list)
    rhetorical_spans: list[RhetoricalSpan] = Field(default_factory=list)
