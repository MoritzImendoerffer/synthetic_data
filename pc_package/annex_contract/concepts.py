"""Phase 4 — canonical concepts (normalized entities)."""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

from .base import SourceReference


class Concept(BaseModel):
    concept_id: str  # e.g. "param:blend_time", "attr:blend_uniformity"
    concept_type: str  # PROCESS_PARAMETER, QUALITY_ATTRIBUTE, ...
    canonical_name: str
    aliases: list[str] = Field(default_factory=list)
    definition: Optional[str] = None
    linked_mention_ids: list[str] = Field(default_factory=list)
    source_references: list[SourceReference] = Field(default_factory=list)
    review_status: Literal[
        "auto_created", "auto_matched", "human_verified", "rejected", "needs_review"
    ] = "auto_created"


class ConceptStore(BaseModel):
    run_id: Optional[str] = None
    concepts: list[Concept] = Field(default_factory=list)
