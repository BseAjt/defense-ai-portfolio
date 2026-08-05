from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query

from .graph import GraphRepository, GraphService
from .repositories import DecisionRepository, MemoryRepository
from .schemas import DecisionCreate, GraphEdgeCreate, GraphNodeCreate, IdeaRequest, MemoryCreate
from .services import ExecutiveService, MemoryService, ReflectionService

router = APIRouter()
memories = MemoryRepository()
decisions = DecisionRepository()
graph = GraphRepository()
graph_service = GraphService(graph)
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


@router.post("/api/executive/agents/reload")
def reload_agents() -> dict[str, Any]:
    return executive_service.reload_agents()


@router.post("/api/executive/analyze")
def analyze_idea(payload: IdeaRequest) -> dict[str, Any]:
    return executive_service.analyze(payload.idea.strip())


@router.post("/api/graph/nodes", status_code=201)
def create_graph_node(payload: GraphNodeCreate) -> dict[str, Any]:
    return graph.create_node(payload)


@router.get("/api/graph/nodes")
def list_graph_nodes(
    node_type: str | None = None,
    limit: int = Query(default=200, ge=1, le=1000),
) -> list[dict[str, Any]]:
    return graph.list_nodes(node_type=node_type, limit=limit)


@router.get("/api/graph/nodes/{node_id}")
def get_graph_node(node_id: int) -> dict[str, Any]:
    node = graph.get_node(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Graph node not found")
    return node


@router.delete("/api/graph/nodes/{node_id}", status_code=204)
def delete_graph_node(node_id: int) -> None:
    if not graph.delete_node(node_id):
        raise HTTPException(status_code=404, detail="Graph node not found")


@router.post("/api/graph/edges", status_code=201)
def create_graph_edge(payload: GraphEdgeCreate) -> dict[str, Any]:
    try:
        return graph.create_edge(payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/api/graph/edges")
def list_graph_edges(limit: int = Query(default=500, ge=1, le=2000)) -> list[dict[str, Any]]:
    return graph.list_edges(limit=limit)


@router.get("/api/graph/nodes/{node_id}/neighbors")
def graph_neighbors(node_id: int, relation_type: str | None = None) -> dict[str, Any]:
    try:
        return graph.neighbors(node_id=node_id, relation_type=relation_type)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Graph node not found") from exc


@router.get("/api/graph")
def graph_snapshot(node_type: str | None = None) -> dict[str, Any]:
    return graph_service.snapshot(node_type=node_type)
