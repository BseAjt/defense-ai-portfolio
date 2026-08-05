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
        assert created.json()["graph_node_id"] > 0

        listed = client.get("/api/memories")
        assert listed.status_code == 200
        assert any(item["id"] == memory_id for item in listed.json())

        searched = client.get("/api/search", params={"q": "persistent memory"})
        assert searched.status_code == 200
        assert any(item["id"] == memory_id for item in searched.json())

        deleted = client.delete(f"/api/memories/{memory_id}")
        assert deleted.status_code == 204


def test_memory_engine_sync_context_and_consolidation() -> None:
    with TestClient(app) as client:
        memory = client.post(
            "/api/memories",
            json={
                "kind": "idea",
                "title": "Contextual Memory Engine",
                "content": "Relier les souvenirs aux décisions du produit.",
                "tags": ["memory-engine", "context"],
                "confidence": 0.92,
            },
        )
        decision = client.post(
            "/api/decisions",
            json={
                "title": "Adopter le graphe contextuel",
                "context": "Le produit doit conserver les raisons de ses choix.",
                "choice": "Synchroniser les décisions avec le Cognitive Graph.",
                "alternatives": ["Conserver uniquement une base relationnelle"],
                "rationale": "Le graphe rend les relations explicites et navigables.",
            },
        )
        assert memory.status_code == 201
        assert decision.status_code == 201
        memory_node_id = memory.json()["graph_node_id"]
        decision_node_id = decision.json()["graph_node_id"]

        relation = client.post(
            "/api/graph/edges",
            json={
                "source_id": decision_node_id,
                "target_id": memory_node_id,
                "relation_type": "derived_from",
                "confidence": 0.95,
                "metadata": {"test": True},
            },
        )
        assert relation.status_code == 201

        contextual = client.get(
            "/api/memory-engine/context",
            params={"q": "souvenirs décisions produit"},
        )
        assert contextual.status_code == 200
        results = contextual.json()["results"]
        match = next(item for item in results if item["id"] == memory.json()["id"])
        assert match["graph_node_id"] == memory_node_id
        assert any(item["node"]["id"] == decision_node_id for item in match["context"])

        consolidated = client.post("/api/memory-engine/consolidate")
        assert consolidated.status_code == 200
        assert consolidated.json()["status"] == "consolidated"

        status = client.get("/api/memory-engine/status")
        assert status.status_code == 200
        assert status.json()["version"] == "0.5.0"
        assert "automatic_graph_sync" in status.json()["capabilities"]

        deleted = client.delete(f"/api/memories/{memory.json()['id']}")
        assert deleted.status_code == 204
        missing_node = client.get(f"/api/graph/nodes/{memory_node_id}")
        assert missing_node.status_code == 404


def test_cognitive_graph_round_trip_and_cascade() -> None:
    with TestClient(app) as client:
        idea = client.post(
            "/api/graph/nodes",
            json={
                "node_type": "idea",
                "label": "MemoryOS",
                "content": "A cognitive operating system",
                "metadata": {"owner": "CEO"},
                "confidence": 0.9,
            },
        )
        project = client.post(
            "/api/graph/nodes",
            json={"node_type": "project", "label": "MVP", "metadata": {}},
        )
        assert idea.status_code == 201
        assert project.status_code == 201
        idea_id = idea.json()["id"]
        project_id = project.json()["id"]

        edge = client.post(
            "/api/graph/edges",
            json={
                "source_id": idea_id,
                "target_id": project_id,
                "relation_type": "belongs_to",
                "metadata": {"reason": "implementation"},
                "confidence": 0.95,
            },
        )
        assert edge.status_code == 201

        neighbors = client.get(f"/api/graph/nodes/{idea_id}/neighbors")
        assert neighbors.status_code == 200
        assert neighbors.json()["neighbors"][0]["node"]["id"] == project_id

        snapshot = client.get("/api/graph")
        assert snapshot.status_code == 200
        assert snapshot.json()["summary"]["node_count"] >= 2
        assert snapshot.json()["summary"]["edge_count"] >= 1

        deleted = client.delete(f"/api/graph/nodes/{idea_id}")
        assert deleted.status_code == 204
        remaining_edges = client.get("/api/graph/edges").json()
        assert all(item["source_id"] != idea_id and item["target_id"] != idea_id for item in remaining_edges)
        client.delete(f"/api/graph/nodes/{project_id}")


def test_graph_rejects_unknown_nodes() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/api/graph/edges",
            json={"source_id": 999999, "target_id": 999998, "relation_type": "supports"},
        )
    assert response.status_code == 422


def test_executive_agents_have_cognitive_profiles() -> None:
    with TestClient(app) as client:
        agents = client.get("/api/executive/agents")
        analysis = client.post(
            "/api/executive/analyze",
            json={"idea": "Créer une plateforme IA avec un modèle économique durable"},
        )
        reloaded = client.post("/api/executive/agents/reload")

    assert agents.status_code == 200
    assert len(agents.json()) == 15
    assert all(agent["mindset"] and agent["questions"] for agent in agents.json())

    assert analysis.status_code == 200
    payload = analysis.json()
    assert payload["agents"]
    assert payload["agent_configuration"].endswith("config/agents.json")
    assert all("blind_spots" in agent and "refuses" in agent for agent in payload["agents"])

    assert reloaded.status_code == 200
    assert reloaded.json()["status"] == "reloaded"
    assert reloaded.json()["agents"] == 15


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
    assert "/api/executive/agents/reload" in paths
    assert "/api/graph/nodes" in paths
    assert "/api/graph/edges" in paths
    assert "/api/graph" in paths
    assert "/api/memory-engine/status" in paths
    assert "/api/memory-engine/consolidate" in paths
    assert "/api/memory-engine/context" in paths
