from __future__ import annotations

from typing import Literal

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
