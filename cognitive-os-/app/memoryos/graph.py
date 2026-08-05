from __future__ import annotations

import json
from typing import Any

from .database import connection
from .repositories import utc_now
from .schemas import GraphEdgeCreate, GraphNodeCreate


class GraphRepository:
    def create_node(self, payload: GraphNodeCreate) -> dict[str, Any]:
        now = utc_now()
        with connection() as db:
            cursor = db.execute(
                """
                INSERT INTO graph_nodes(node_type, label, content, metadata, confidence, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payload.node_type,
                    payload.label.strip(),
                    payload.content.strip() if payload.content else None,
                    json.dumps(payload.metadata, ensure_ascii=False),
                    payload.confidence,
                    now,
                    now,
                ),
            )
            row = db.execute("SELECT * FROM graph_nodes WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return self._node(row)

    def list_nodes(self, node_type: str | None = None, limit: int = 200) -> list[dict[str, Any]]:
        with connection() as db:
            if node_type:
                rows = db.execute(
                    "SELECT * FROM graph_nodes WHERE node_type = ? ORDER BY created_at DESC LIMIT ?",
                    (node_type, limit),
                ).fetchall()
            else:
                rows = db.execute(
                    "SELECT * FROM graph_nodes ORDER BY created_at DESC LIMIT ?",
                    (limit,),
                ).fetchall()
        return [self._node(row) for row in rows]

    def get_node(self, node_id: int) -> dict[str, Any] | None:
        with connection() as db:
            row = db.execute("SELECT * FROM graph_nodes WHERE id = ?", (node_id,)).fetchone()
        return self._node(row) if row else None

    def delete_node(self, node_id: int) -> bool:
        with connection() as db:
            cursor = db.execute("DELETE FROM graph_nodes WHERE id = ?", (node_id,))
        return cursor.rowcount > 0

    def create_edge(self, payload: GraphEdgeCreate) -> dict[str, Any]:
        with connection() as db:
            source = db.execute("SELECT id FROM graph_nodes WHERE id = ?", (payload.source_id,)).fetchone()
            target = db.execute("SELECT id FROM graph_nodes WHERE id = ?", (payload.target_id,)).fetchone()
            if not source or not target:
                raise ValueError("Source or target node does not exist")
            cursor = db.execute(
                """
                INSERT INTO graph_edges(source_id, target_id, relation_type, metadata, confidence, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    payload.source_id,
                    payload.target_id,
                    payload.relation_type,
                    json.dumps(payload.metadata, ensure_ascii=False),
                    payload.confidence,
                    utc_now(),
                ),
            )
            row = db.execute("SELECT * FROM graph_edges WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return self._edge(row)

    def list_edges(self, limit: int = 500) -> list[dict[str, Any]]:
        with connection() as db:
            rows = db.execute(
                "SELECT * FROM graph_edges ORDER BY created_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [self._edge(row) for row in rows]

    def neighbors(self, node_id: int, relation_type: str | None = None) -> dict[str, Any]:
        node = self.get_node(node_id)
        if not node:
            raise KeyError(node_id)
        query = """
            SELECT e.*, n.id AS neighbor_id, n.node_type AS neighbor_type,
                   n.label AS neighbor_label, n.content AS neighbor_content,
                   n.metadata AS neighbor_metadata, n.confidence AS neighbor_confidence,
                   CASE WHEN e.source_id = ? THEN 'outgoing' ELSE 'incoming' END AS direction
            FROM graph_edges e
            JOIN graph_nodes n ON n.id = CASE WHEN e.source_id = ? THEN e.target_id ELSE e.source_id END
            WHERE (e.source_id = ? OR e.target_id = ?)
        """
        params: list[Any] = [node_id, node_id, node_id, node_id]
        if relation_type:
            query += " AND e.relation_type = ?"
            params.append(relation_type)
        query += " ORDER BY e.created_at DESC"
        with connection() as db:
            rows = db.execute(query, params).fetchall()
        neighbors = []
        for row in rows:
            item = dict(row)
            neighbors.append(
                {
                    "edge": {
                        "id": item["id"],
                        "source_id": item["source_id"],
                        "target_id": item["target_id"],
                        "relation_type": item["relation_type"],
                        "metadata": json.loads(item["metadata"]),
                        "confidence": item["confidence"],
                        "created_at": item["created_at"],
                        "direction": item["direction"],
                    },
                    "node": {
                        "id": item["neighbor_id"],
                        "node_type": item["neighbor_type"],
                        "label": item["neighbor_label"],
                        "content": item["neighbor_content"],
                        "metadata": json.loads(item["neighbor_metadata"]),
                        "confidence": item["neighbor_confidence"],
                    },
                }
            )
        return {"node": node, "neighbors": neighbors}

    @staticmethod
    def _node(row: Any) -> dict[str, Any]:
        item = dict(row)
        item["metadata"] = json.loads(item["metadata"])
        return item

    @staticmethod
    def _edge(row: Any) -> dict[str, Any]:
        item = dict(row)
        item["metadata"] = json.loads(item["metadata"])
        return item


class GraphService:
    def __init__(self, repository: GraphRepository | None = None) -> None:
        self.repository = repository or GraphRepository()

    def snapshot(self, node_type: str | None = None) -> dict[str, Any]:
        nodes = self.repository.list_nodes(node_type=node_type, limit=1000)
        node_ids = {node["id"] for node in nodes}
        edges = [
            edge
            for edge in self.repository.list_edges(limit=2000)
            if edge["source_id"] in node_ids and edge["target_id"] in node_ids
        ]
        relation_counts: dict[str, int] = {}
        for edge in edges:
            relation = edge["relation_type"]
            relation_counts[relation] = relation_counts.get(relation, 0) + 1
        return {
            "nodes": nodes,
            "edges": edges,
            "summary": {
                "node_count": len(nodes),
                "edge_count": len(edges),
                "relation_counts": relation_counts,
            },
        }
