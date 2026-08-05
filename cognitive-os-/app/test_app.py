import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from main import app
from memoryos.agent_registry import AgentConfigurationError, AgentRegistry


def test_health() -> None:
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "memoryos"}


def test_memory_round_trip() -> None:
    with TestClient(app) as client:
        created = client.post(
            "/api/memories",
            json={
                "kind": "learning",
                "title": "Test memory",
                "content": "A persistent memory can be retrieved later.",
                "tags": ["test"],
                "confidence": 0.9,
            },
        )
        assert created.status_code == 201
        memory_id = created.json()["id"]

        listed = client.get("/api/memories")
        assert listed.status_code == 200
        assert any(item["id"] == memory_id for item in listed.json())

        searched = client.get("/api/search", params={"q": "persistent memory"})
        assert searched.status_code == 200
        assert any(item["id"] == memory_id for item in searched.json())

        deleted = client.delete(f"/api/memories/{memory_id}")
        assert deleted.status_code == 204


def test_executive_agents_have_cognitive_profiles() -> None:
    with TestClient(app) as client:
        agents = client.get("/api/executive/agents")
        analysis = client.post(
            "/api/executive/analyze",
            json={"idea": "Créer une plateforme IA avec un modèle économique durable"},
        )

    assert agents.status_code == 200
    assert len(agents.json()) == 15
    assert all(agent["mindset"] and agent["questions"] for agent in agents.json())

    assert analysis.status_code == 200
    payload = analysis.json()
    assert payload["agents"]
    assert payload["agent_configuration"].endswith("config/agents.json")
    assert all("blind_spots" in agent and "refuses" in agent for agent in payload["agents"])


def test_registry_loads_custom_configuration(tmp_path: Path) -> None:
    custom_path = tmp_path / "agents.json"
    custom_path.write_text(
        json.dumps(
            {
                "default_agents": ["Test Agent"],
                "agents": [
                    {
                        "name": "Test Agent",
                        "inspiration": "Test",
                        "role": "Tester",
                        "mission": "Validate configuration loading.",
                        "mindset": ["verify"],
                        "questions": ["Does it load?"],
                        "refuses": ["silent failure"],
                        "blind_spots": ["test-only profile"],
                        "style": "precise",
                        "analysis": "Checks configuration behavior.",
                        "keywords": ["custom"],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    registry = AgentRegistry.load(custom_path)
    assert [agent["name"] for agent in registry.list()] == ["Test Agent"]
    assert [agent["name"] for agent in registry.select("custom subject")] == ["Test Agent"]


def test_registry_rejects_invalid_configuration(tmp_path: Path) -> None:
    invalid_path = tmp_path / "agents.json"
    invalid_path.write_text('{"default_agents": [], "agents": [{"name": "Broken"}]}', encoding="utf-8")

    with pytest.raises(AgentConfigurationError):
        AgentRegistry.load(invalid_path)


def test_openapi_contains_stable_public_routes() -> None:
    with TestClient(app) as client:
        schema = client.get("/openapi.json").json()

    paths = schema["paths"]
    assert "/api/memories" in paths
    assert "/api/decisions" in paths
    assert "/api/reflections" in paths
    assert "/api/executive/analyze" in paths
