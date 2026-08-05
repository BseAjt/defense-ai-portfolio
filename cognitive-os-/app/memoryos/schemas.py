from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class MemoryCreate(BaseModel):
    kind: Literal["idea", "fact", "learning", "experience", "goal", "reflection"] = "idea"
    title: str = Field(min_length=2, max_length=160)
    content: str = Field(min_length=2)
    tags: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.7, ge=0.0, le=1.0)
    source: str | None = None


class DecisionCreate(BaseModel):
    title: str = Field(min_length=2, max_length=160)
    context: str = Field(min_length=2)
    choice: str = Field(min_length=2)
    alternatives: list[str] = Field(default_factory=list)
    rationale: str = Field(min_length=2)
    review_at: str | None = None


class IdeaRequest(BaseModel):
    idea: str = Field(min_length=4)


class GraphNodeCreate(BaseModel):
    node_type: Literal[
        "memory",
        "idea",
        "decision",
        "goal",
        "project",
        "person",
        "concept",
        "document",
        "conversation",
        "event",
    ]
    label: str = Field(min_length=2, max_length=200)
    content: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    confidence: float = Field(default=0.7, ge=0.0, le=1.0)


class GraphEdgeCreate(BaseModel):
    source_id: int = Field(gt=0)
    target_id: int = Field(gt=0)
    relation_type: Literal[
        "supports",
        "contradicts",
        "derived_from",
        "depends_on",
        "created_by",
        "mentions",
        "belongs_to",
        "validated_by",
        "causes",
        "references",
        "duplicates",
        "supersedes",
    ]
    metadata: dict[str, Any] = Field(default_factory=dict)
    confidence: float = Field(default=0.7, ge=0.0, le=1.0)
