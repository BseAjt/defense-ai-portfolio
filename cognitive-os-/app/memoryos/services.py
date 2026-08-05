from __future__ import annotations

import re
from typing import Any

from .agent_registry import AgentRegistry
from .repositories import DecisionRepository, MemoryRepository, utc_now


STOP_WORDS = {"avec", "dans", "pour", "mais", "plus", "cette", "that", "this", "from", "have"}


def tokenize(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-zA-ZÀ-ÿ0-9_-]{3,}", text.lower())
        if token not in STOP_WORDS
    }


def similarity(query: str, text: str) -> float:
    query_tokens = tokenize(query)
    text_tokens = tokenize(text)
    if not query_tokens or not text_tokens:
        return 0.0
    return len(query_tokens & text_tokens) / len(query_tokens | text_tokens)


class MemoryService:
    def __init__(self, repository: MemoryRepository | None = None) -> None:
        self.repository = repository or MemoryRepository()

    def search(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        scored: list[dict[str, Any]] = []
        for memory in self.repository.list(limit=500):
            haystack = f"{memory['title']} {memory['content']} {' '.join(memory['tags'])}"
            score = similarity(query, haystack)
            if score > 0:
                item = dict(memory)
                item["score"] = round(score, 4)
                scored.append(item)
        return sorted(scored, key=lambda item: item["score"], reverse=True)[:limit]


class ReflectionService:
    def __init__(
        self,
        memories: MemoryRepository | None = None,
        decisions: DecisionRepository | None = None,
    ) -> None:
        self.memories = memories or MemoryRepository()
        self.decisions = decisions or DecisionRepository()

    def analyze(self) -> dict[str, Any]:
        memories = self.memories.list(limit=500)
        decisions = self.decisions.list()
        low_confidence = [item for item in memories if item["confidence"] < 0.5]
        stale_decisions = [
            item for item in decisions
            if item.get("review_at") and item["review_at"] <= utc_now()
        ]
        titles: dict[str, int] = {}
        for item in memories:
            key = item["title"].strip().lower()
            titles[key] = titles.get(key, 0) + 1
        duplicates = sum(1 for count in titles.values() if count > 1)
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
                {"type": "duplicates", "message": f"{duplicates} titre(s) potentiellement dupliqué(s)."},
            ],
        }


class ExecutiveService:
    def __init__(self, registry: AgentRegistry | None = None) -> None:
        self.registry = registry or AgentRegistry.load()

    def agents(self) -> list[dict[str, Any]]:
        return self.registry.list()

    def analyze(self, idea: str) -> dict[str, Any]:
        selected = self.registry.select(idea)
        analyses = [
            {
                "name": agent["name"],
                "inspiration": agent["inspiration"],
                "role": agent["role"],
                "mission": agent["mission"],
                "mindset": agent["mindset"],
                "questions": agent["questions"],
                "refuses": agent["refuses"],
                "blind_spots": agent["blind_spots"],
                "style": agent["style"],
                "analysis": agent["analysis"],
            }
            for agent in selected
        ]
        return {
            "idea": idea,
            "executive_summary": "Le Board recommande un test court, mesurable et réversible avant tout investissement lourd.",
            "agents": analyses,
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
            "confidence": 0.72,
            "agent_configuration": str(self.registry.source_path),
        }
