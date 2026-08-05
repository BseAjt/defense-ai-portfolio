from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query

from .repositories import DecisionRepository, MemoryRepository
from .schemas import DecisionCreate, IdeaRequest, MemoryCreate
from .services import ExecutiveService, MemoryService, ReflectionService

router = APIRouter()
memories = MemoryRepository()
decisions = DecisionRepository()
memory_service = MemoryService(memories)
reflection_service = ReflectionService(memories, decisions)
executive_service = ExecutiveService()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "memoryos"}


@router.post("/api/memories", status_code=201)
def create_memory(payload: MemoryCreate) -> dict[str, Any]:
    return memories.create(payload)


@router.get("/api/memories")
def list_memories(limit: int = Query(default=100, ge=1, le=500)) -> list[dict[str, Any]]:
    return memories.list(limit)


@router.get("/api/search")
def search_memories(
    q: str = Query(min_length=2),
    limit: int = Query(default=10, ge=1, le=50),
) -> list[dict[str, Any]]:
    return memory_service.search(q, limit)


@router.delete("/api/memories/{memory_id}", status_code=204)
def delete_memory(memory_id: int) -> None:
    if not memories.delete(memory_id):
        raise HTTPException(status_code=404, detail="Memory not found")


@router.post("/api/decisions", status_code=201)
def create_decision(payload: DecisionCreate) -> dict[str, Any]:
    return decisions.create(payload)


@router.get("/api/decisions")
def list_decisions() -> list[dict[str, Any]]:
    return decisions.list()


@router.get("/api/reflections")
def reflections() -> dict[str, Any]:
    return reflection_service.analyze()


@router.get("/api/executive/agents")
def list_agents() -> list[dict[str, Any]]:
    return executive_service.agents()


@router.post("/api/executive/analyze")
def analyze_idea(payload: IdeaRequest) -> dict[str, Any]:
    return executive_service.analyze(payload.idea.strip())
