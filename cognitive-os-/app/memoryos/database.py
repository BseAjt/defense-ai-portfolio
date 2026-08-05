from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from typing import Iterator

from .config import settings


@contextmanager
def connection() -> Iterator[sqlite3.Connection]:
    db = sqlite3.connect(settings.database_path)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    try:
        yield db
        db.commit()
    finally:
        db.close()


def initialize_database() -> None:
    with connection() as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kind TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                tags TEXT NOT NULL DEFAULT '[]',
                confidence REAL NOT NULL DEFAULT 0.7,
                source TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                context TEXT NOT NULL,
                choice TEXT NOT NULL,
                alternatives TEXT NOT NULL DEFAULT '[]',
                rationale TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'active',
                review_at TEXT,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS graph_nodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                node_type TEXT NOT NULL,
                label TEXT NOT NULL,
                content TEXT,
                metadata TEXT NOT NULL DEFAULT '{}',
                confidence REAL NOT NULL DEFAULT 0.7,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS graph_edges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id INTEGER NOT NULL,
                target_id INTEGER NOT NULL,
                relation_type TEXT NOT NULL,
                metadata TEXT NOT NULL DEFAULT '{}',
                confidence REAL NOT NULL DEFAULT 0.7,
                created_at TEXT NOT NULL,
                FOREIGN KEY(source_id) REFERENCES graph_nodes(id) ON DELETE CASCADE,
                FOREIGN KEY(target_id) REFERENCES graph_nodes(id) ON DELETE CASCADE,
                CHECK(source_id <> target_id)
            );

            CREATE INDEX IF NOT EXISTS idx_graph_nodes_type ON graph_nodes(node_type);
            CREATE INDEX IF NOT EXISTS idx_graph_edges_source ON graph_edges(source_id);
            CREATE INDEX IF NOT EXISTS idx_graph_edges_target ON graph_edges(target_id);
            CREATE INDEX IF NOT EXISTS idx_graph_edges_relation ON graph_edges(relation_type);
            """
        )
