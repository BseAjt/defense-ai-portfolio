from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from typing import Any

from .database import connection
from .schemas import DecisionCreate, MemoryCreate


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def row_to_memory(row: sqlite3.Row) -> dict[str, Any]:
    item = dict(row)
    item["tags"] = json.loads(item["tags"])
    return item


class MemoryRepository:
    def create(self, payload: MemoryCreate) -> dict[str, Any]:
        now = utc_now()
        with connection() as db:
            cursor = db.execute(
                """
                INSERT INTO memories(kind, title, content, tags, confidence, source, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payload.kind,
                    payload.title.strip(),
                    payload.content.strip(),
                    json.dumps(payload.tags, ensure_ascii=False),
                    payload.confidence,
                    payload.source,
                    now,
                    now,
                ),
            )
            row = db.execute("SELECT * FROM memories WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return row_to_memory(row)

    def list(self, limit: int = 100) -> list[dict[str, Any]]:
        with connection() as db:
            rows = db.execute(
                "SELECT * FROM memories ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
        return [row_to_memory(row) for row in rows]

    def delete(self, memory_id: int) -> bool:
        with connection() as db:
            cursor = db.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
        return cursor.rowcount > 0


class DecisionRepository:
    def create(self, payload: DecisionCreate) -> dict[str, Any]:
        with connection() as db:
            cursor = db.execute(
                """
                INSERT INTO decisions(title, context, choice, alternatives, rationale, review_at, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payload.title.strip(),
                    payload.context.strip(),
                    payload.choice.strip(),
                    json.dumps(payload.alternatives, ensure_ascii=False),
                    payload.rationale.strip(),
                    payload.review_at,
                    utc_now(),
                ),
            )
            row = db.execute("SELECT * FROM decisions WHERE id = ?", (cursor.lastrowid,)).fetchone()
        item = dict(row)
        item["alternatives"] = json.loads(item["alternatives"])
        return item

    def list(self) -> list[dict[str, Any]]:
        with connection() as db:
            rows = db.execute("SELECT * FROM decisions ORDER BY created_at DESC").fetchall()
        result: list[dict[str, Any]] = []
        for row in rows:
            item = dict(row)
            item["alternatives"] = json.loads(item["alternatives"])
            result.append(item)
        return result
