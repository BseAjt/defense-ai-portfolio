from __future__ import annotations

import json
import re
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator, Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from agents import analyze_with_agent, get_agents, select_agents

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "memoryos.db"
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="MemoryOS MVP",
    version="0.2.0",
    description="Local Cognitive Operating System with mindset-driven ExecutiveOS agents.",
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@contextmanager
def db() -> Iterator[sqlite3.Connection]:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def init_db() -> None:
    with db() as connection:
        connection.executescript(
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
            """
        )


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


def row_to_memory(row: sqlite3.Row) -> dict[str, Any]:
    item = dict(row)
    item["tags"] = json.loads(item["tags"])
    return item


def tokenize(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-zA-ZÀ-ÿ0-9_-]{3,}", text.lower())
        if token not in {"avec", "dans", "pour", "mais", "plus", "cette", "that", "this", "from", "have"}
    }


def similarity(query: str, text: str) -> float:
    query_tokens = tokenize(query)
    text_tokens = tokenize(text)
    if not query_tokens or not text_tokens:
        return 0.0
    return len(query_tokens & text_tokens) / len(query_tokens | text_tokens)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "memoryos", "version": "0.2.0"}


@app.post("/api/memories", status_code=201)
def create_memory(payload: MemoryCreate) -> dict[str, Any]:
    now = utc_now()
    with db() as connection:
        cursor = connection.execute(
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
        row = connection.execute("SELECT * FROM memories WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return row_to_memory(row)


@app.get("/api/memories")
def list_memories(limit: int = Query(default=100, ge=1, le=500)) -> list[dict[str, Any]]:
    with db() as connection:
        rows = connection.execute(
            "SELECT * FROM memories ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
    return [row_to_memory(row) for row in rows]


@app.get("/api/search")
def search_memories(q: str = Query(min_length=2), limit: int = Query(default=10, ge=1, le=50)) -> list[dict[str, Any]]:
    with db() as connection:
        rows = connection.execute("SELECT * FROM memories ORDER BY created_at DESC").fetchall()
    scored: list[dict[str, Any]] = []
    for row in rows:
        memory = row_to_memory(row)
        score = similarity(q, f"{memory['title']} {memory['content']} {' '.join(memory['tags'])}")
        if score > 0:
            memory["score"] = round(score, 4)
            scored.append(memory)
    return sorted(scored, key=lambda item: item["score"], reverse=True)[:limit]


@app.delete("/api/memories/{memory_id}", status_code=204)
def delete_memory(memory_id: int) -> None:
    with db() as connection:
        cursor = connection.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Memory not found")


@app.post("/api/decisions", status_code=201)
def create_decision(payload: DecisionCreate) -> dict[str, Any]:
    with db() as connection:
        cursor = connection.execute(
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
        row = connection.execute("SELECT * FROM decisions WHERE id = ?", (cursor.lastrowid,)).fetchone()
    item = dict(row)
    item["alternatives"] = json.loads(item["alternatives"])
    return item


@app.get("/api/decisions")
def list_decisions() -> list[dict[str, Any]]:
    with db() as connection:
        rows = connection.execute("SELECT * FROM decisions ORDER BY created_at DESC").fetchall()
    result = []
    for row in rows:
        item = dict(row)
        item["alternatives"] = json.loads(item["alternatives"])
        result.append(item)
    return result


@app.get("/api/reflections")
def reflections() -> dict[str, Any]:
    with db() as connection:
        memories = [row_to_memory(row) for row in connection.execute("SELECT * FROM memories").fetchall()]
        decisions = [dict(row) for row in connection.execute("SELECT * FROM decisions").fetchall()]

    low_confidence = [item for item in memories if item["confidence"] < 0.5]
    stale_decisions = [item for item in decisions if item.get("review_at") and item["review_at"] <= utc_now()]
    duplicated_titles: dict[str, int] = {}
    for item in memories:
        key = item["title"].strip().lower()
        duplicated_titles[key] = duplicated_titles.get(key, 0) + 1

    return {
        "summary": {
            "memories": len(memories),
            "decisions": len(decisions),
            "low_confidence": len(low_confidence),
            "decisions_to_review": len(stale_decisions),
        },
        "signals": [
            {"type": "low_confidence", "message": f"{len(low_confidence)} mémoire(s) à confirmer."},
            {"type": "review", "message": f"{len(stale_decisions)} décision(s) à réexaminer."},
            {
                "type": "duplicates",
                "message": f"{sum(1 for count in duplicated_titles.values() if count > 1)} titre(s) potentiellement dupliqué(s).",
            },
        ],
    }


@app.get("/api/executive/agents")
def list_executive_agents() -> list[dict[str, Any]]:
    """Return the complete cognitive profile of every ExecutiveOS agent."""
    return get_agents()


@app.post("/api/executive/analyze")
def analyze_idea(payload: IdeaRequest) -> dict[str, Any]:
    idea = payload.idea.strip()
    selected = select_agents(idea)
    analyses = [analyze_with_agent(agent, idea) for agent in selected]

    tensions = []
    selected_names = {agent["name"] for agent in selected}
    if {"Jobs", "Buffett"}.issubset(selected_names):
        tensions.append("Jobs pousse l'excellence produit tandis que Buffett exige une marge de sécurité financière.")
    if {"Hormozi", "Portalis"}.issubset(selected_names):
        tensions.append("Hormozi privilégie la vitesse de croissance ; Portalis protège la confiance et la conformité.")
    if {"Turing", "Rams"}.issubset(selected_names):
        tensions.append("Turing accepte la complexité interne ; Rams exige qu'elle disparaisse de l'expérience utilisateur.")

    return {
        "idea": idea,
        "orchestrator": "ORION",
        "executive_summary": "Le Board recommande de transformer l'idée en hypothèse testable, puis de confronter vision, désirabilité, faisabilité, risque et alignement personnel.",
        "selected_agents": len(selected),
        "agents": analyses,
        "debate": tensions,
        "risks": [
            "Problème insuffisamment précis",
            "Complexité construite avant validation de l'usage",
            "Absence de métrique de succès",
        ],
        "recommendation": "Formuler une hypothèse falsifiable, construire un prototype limité et interroger cinq utilisateurs cibles.",
        "action_plan": [
            "Écrire le problème en une phrase",
            "Définir un utilisateur cible prioritaire",
            "Choisir une métrique de validation",
            "Construire un test réalisable en sept jours",
        ],
        "confidence": 0.78,
    }
