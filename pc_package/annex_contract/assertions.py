"""Phase 5 — evidence-backed assertions and conflict groups (boilerplate).

Implemented enough to be used; the conflict-detection *logic* lives in
nlp_reports/pipelines/run_assertions.py and is marked TODO for pickup.
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

from .base import ExtractionMetadata, SourceReference

Predicate = Literal[
    "process_has_step",
    "step_uses_equipment",
    "step_has_parameter",
    "step_has_quality_attribute",
    "parameter_impacts_attribute",
    "parameter_does_not_significantly_impact_attribute",
    "attribute_measured_by_method",
    "attribute_has_acceptance_criterion",
    "batch_used_in_validation",
    "transfer_has_gap",
]


class Rationale(BaseModel):
    rationale_id: str
    rationale_type: Literal[
        "entity_classification",
        "criticality_assignment",
        "relationship_explanation",
        "process_decision",
        "control_strategy_decision",
        "transfer_gap_explanation",
        "summary_statement_support",
    ]
    subject_id: Optional[str] = None
    rationale_text: str
    basis: Literal["explicitly_stated", "inferred_from_context", "not_supported", "human_authored", "unknown"]
    source_references: list[SourceReference] = Field(default_factory=list)
    metadata: ExtractionMetadata = Field(default_factory=ExtractionMetadata)


class EvidenceBackedAssertion(BaseModel):
    assertion_id: str
    subject_id: str  # concept_id
    predicate: Predicate
    object_id: str  # concept_id or literal value id
    assertion_text: Optional[str] = None
    rationale_ids: list[str] = Field(default_factory=list)
    source_references: list[SourceReference] = Field(default_factory=list)
    metadata: ExtractionMetadata = Field(default_factory=ExtractionMetadata)


class ConflictGroup(BaseModel):
    conflict_id: str
    topic: str  # e.g. "hold time for step:granulation"
    assertion_ids: list[str] = Field(default_factory=list)
    requires_human_review: bool = True
    notes: Optional[str] = None


class AssertionStore(BaseModel):
    run_id: Optional[str] = None
    assertions: list[EvidenceBackedAssertion] = Field(default_factory=list)
    rationales: list[Rationale] = Field(default_factory=list)
    conflicts: list[ConflictGroup] = Field(default_factory=list)
