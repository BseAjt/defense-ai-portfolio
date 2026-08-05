from __future__ import annotations

from typing import Any

from .database import connection
from .graph import GraphRepository
from .repositories import DecisionRepository, MemoryRepository
from .schemas import DecisionCreate, GraphEdgeCreate, GraphNodeCreate, MemoryCreate
from .services import similarity


MEMORY_NODE_TYPES = {
    "idea": "idea",
    "goal": "goal",
    "reflection": "memory",
    "fact": "memory",
    "learning": "memory",
    "experience": "memory",
}


class CognitiveLinkRepository:
    """Maps domain records to graph nodes without coupling their table schemas."""

    def get(self, entity_type: str, entity_id: int) -> int | None:
        with connection() as db:
            row = db.execute(
                "SELECT graph_node_id FROM cognitive_links WHERE entity_type = ? AND entity_id = ?",
                (entity_type, entity_id),
            ).fetchone()
        return int(row["graph_node_id"]) if row else None

    def create(self, entity_type: str, entity_id: int, graph_node_id: int) -> None:
        with connection() as db:
            db.execute(
                """
                INSERT OR REPLACE INTO cognitive_links(entity_type, entity_id, graph_node_id)
                VALUES (?, ?, ?)
                """,
                (entity_type, entity_id, graph_node_id),
            )

    def delete(self, entity_type: str, entity_id: int) -> None:
        with connection() as db:
            db.execute(
                "DELETE FROM cognitive_links WHERE entity_type = ? AND entity_id = ?",
                (entity_type, entity_id),
            )

    def stats(self) -> dict[str, int]:
        with connection() as db:
            rows = db.execute(
                "SELECT entity_type, COUNT(*) AS total FROM cognitive_links GROUP BY entity_type"
            ).fetchall()
        return {str(row["entity_type"]): int(row["total"]) for row in rows}


class CognitiveMemoryEngine:
    def __init__(
        self,
        memories: MemoryRepository | None = None,
        decisions: DecisionRepository | None = None,
        graph: GraphRepository | None = None,
        links: CognitiveLinkRepository | None = None,
    ) -> None:
        self.memories = memories or MemoryRepository()
        self.decisions = decisions or DecisionRepository()
        self.graph = graph or GraphRepository()
        self.links = links or CognitiveLinkRepository()

    def create_memory(self, payload: MemoryCreate) -> dict[str, Any]:
        memory = self.memories.create(payload)
        node = self._ensure_memory_node(memory)
        memory["graph_node_id"] = node["id"]
        return memory

    def delete_memory(self, memory_id: int) -> bool:
        node_id = self.links.get("memory", memory_id)
        deleted = self.memories.delete(memory_id)
        if not deleted:
            return False
        if node_id:
            self.graph.delete_node(node_id)
        self.links.delete("memory", memory_id)
        return True

    def create_decision(self, payload: DecisionCreate) -> dict[str, Any]:
        decision = self.decisions.create(payload)
        node = self._ensure_decision_node(decision)
        decision["graph_node_id"] = node["id"]
        return decision

    def consolidate(self) -> dict[str, Any]:
        created_memory_nodes = 0
        created_decision_nodes = 0

        for memory in self.memories.list(limit=5000):
            if self.links.get("memory", memory["id"]) is None:
                self._ensure_memory_node(memory)
                created_memory_nodes += 1

        for decision in self.decisions.list():
            if self.links.get("decision", decision["id"]) is None:
                self._ensure_decision_node(decision)
                created_decision_nodes += 1

        duplicate_edges = self._link_probable_duplicates()
        return {
            "status": "consolidated",
            "created_memory_nodes": created_memory_nodes,
            "created_decision_nodes": created_decision_nodes,
            "created_duplicate_edges": duplicate_edges,
            "links": self.links.stats(),
        }

    def contextual_search(self, query: str, limit: int = 10) -> dict[str, Any]:
        ranked: list[dict[str, Any]] = []
        for memory in self.memories.list(limit=5000):
            score = similarity(
                query,
                f"{memory['title']} {memory['content']} {' '.join(memory['tags'])}",
            )
            if score <= 0:
                continue
            item = dict(memory)
            item["score"] = round(score, 4)
            node_id = self.links.get("memory", memory["id"])
            item["graph_node_id"] = node_id
            item["context"] = self._context_for_node(node_id) if node_id else []
            ranked.append(item)

        ranked.sort(key=lambda item: item["score"], reverse=True)
        return {
            "query": query,
            "results": ranked[:limit],
            "summary": {
                "matches": min(len(ranked), limit),
                "linked_entities": self.links.stats(),
            },
        }

    def status(self) -> dict[str, Any]:
        nodes = self.graph.list_nodes(limit=5000)
        edges = self.graph.list_edges(limit=10000)
        return {
            "version": "0.5.0",
            "links": self.links.stats(),
            "graph_nodes": len(nodes),
            "graph_edges": len(edges),
            "capabilities": [
                "automatic_graph_sync",
                "backfill_consolidation",
                "contextual_search",
                "duplicate_detection",
                "coherent_deletion",
            ],
        }

    def _ensure_memory_node(self, memory: dict[str, Any]) -> dict[str, Any]:
        existing_id = self.links.get("memory", memory["id"])
        if existing_id:
            existing = self.graph.get_node(existing_id)
            if existing:
                return existing

        node = self.graph.create_node(
            GraphNodeCreate(
                node_type=MEMORY_NODE_TYPES.get(memory["kind"], "memory"),
                label=memory["title"],
                content=memory["content"],
                confidence=memory["confidence"],
                metadata={
                    "entity_type": "memory",
                    "entity_id": memory["id"],
                    "memory_kind": memory["kind"],
                    "tags": memory["tags"],
                    "source": memory.get("source"),
                },
            )
        )
        self.links.create("memory", memory["id"], node["id"])
        return node

    def _ensure_decision_node(self, decision: dict[str, Any]) -> dict[str, Any]:
        existing_id = self.links.get("decision", decision["id"])
        if existing_id:
            existing = self.graph.get_node(existing_id)
            if existing:
                return existing

        content = (
            f"Contexte: {decision['context']}\n"
            f"Choix: {decision['choice']}\n"
            f"Raisonnement: {decision['rationale']}"
        )
        node = self.graph.create_node(
            GraphNodeCreate(
                node_type="decision",
                label=decision["title"],
                content=content,
                confidence=0.8,
                metadata={
                    "entity_type": "decision",
                    "entity_id": decision["id"],
                    "alternatives": decision["alternatives"],
                    "status": decision["status"],
                    "review_at": decision.get("review_at"),
                },
            )
        )
        self.links.create("decision", decision["id"], node["id"])
        return node

    def _context_for_node(self, node_id: int) -> list[dict[str, Any]]:
        try:
            neighborhood = self.graph.neighbors(node_id)
        except KeyError:
            return []
        return [
            {
                "relation": item["edge"]["relation_type"],
                "direction": item["edge"]["direction"],
                "node": item["node"],
            }
            for item in neighborhood["neighbors"][:10]
        ]

    def _link_probable_duplicates(self) -> int:
        nodes = self.graph.list_nodes(limit=5000)
        edges = self.graph.list_edges(limit=10000)
        existing_pairs = {
            (edge["source_id"], edge["target_id"], edge["relation_type"])
            for edge in edges
        }
        created = 0
        for index, source in enumerate(nodes):
            if source["node_type"] not in {"memory", "idea", "goal"}:
                continue
            for target in nodes[index + 1 :]:
                if target["node_type"] not in {"memory", "idea", "goal"}:
                    continue
                score = similarity(
                    f"{source['label']} {source.get('content') or ''}",
                    f"{target['label']} {target.get('content') or ''}",
                )
                if score < 0.72:
                    continue
                pair = (source["id"], target["id"], "duplicates")
                reverse = (target["id"], source["id"], "duplicates")
                if pair in existing_pairs or reverse in existing_pairs:
                    continue
                self.graph.create_edge(
                    GraphEdgeCreate(
                        source_id=source["id"],
                        target_id=target["id"],
                        relation_type="duplicates",
                        confidence=round(score, 4),
                        metadata={"generated_by": "memory_engine", "similarity": round(score, 4)},
                    )
                )
                existing_pairs.add(pair)
                created += 1
        return created
