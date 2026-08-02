"""Characterization-study contracts — designed experiments, design spaces, PARs.

Added in SCHEMA_VERSION 0.3. These are the central objects of a process
characterization plan or report and had no upstream model, so the benchmark corpus
had to define them locally (``synthetic_data/pc_package/schema_ext.py``). Field names
and types mirror that definition exactly, so a ground truth annex parses without translation.

Status: **provisional.** The evidence that these belong in the contract is one
synthetic corpus. They are deliberately *not* part of ``SectionEntityExtraction`` —
i.e. not in the default extraction prompt — until real documents confirm they occur
there too. Until then they are read (to score against ground truth), not written.
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from .base import ExtractionMetadata, SourceReference

StudyType = Literal[
    "screening_doe",
    "response_surface_doe",
    "univariate",
    "one_factor_at_a_time",
    "risk_assessment",
    "scale_down_qualification",
]


class StudyDesign(BaseModel):
    """A designed characterization study for a unit operation.

    Covers a DoE (screening or response-surface), a univariate study, a risk
    assessment, or a scale-down-model qualification.
    """
    model_config = ConfigDict(extra="forbid")

    study_id: str
    study_type: StudyType
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
    """A multivariate region within which every constrained attribute stays in spec."""
    model_config = ConfigDict(extra="forbid")

    design_space_id: str
    unit_operation: Optional[str] = None
    parameters: list[str] = Field(default_factory=list)
    quality_attributes_constrained: list[str] = Field(default_factory=list)
    definition: Optional[str] = None
    source_references: list[SourceReference] = Field(default_factory=list)
    metadata: ExtractionMetadata = Field(default_factory=ExtractionMetadata)


class ProvenAcceptableRange(BaseModel):
    """A per-attribute x parameter proven acceptable range.

    Two analyses are reported: ``par_at_setpoint`` (other factors held fixed) and
    ``par_nor_propagated`` (other factors varied within their normal operating range).
    They can legitimately differ, so a cross-document check must compare like with like.
    """
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
