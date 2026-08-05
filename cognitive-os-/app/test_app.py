from fastapi.testclient import TestClient

from main import app


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
    assert analysis.json()["agents"]
    assert all("blind_spots" in agent for agent in analysis.json()["agents"])


def test_openapi_contains_stable_public_routes() -> None:
    with TestClient(app) as client:
        schema = client.get("/openapi.json").json()

    paths = schema["paths"]
    assert "/api/memories" in paths
    assert "/api/decisions" in paths
    assert "/api/reflections" in paths
    assert "/api/executive/analyze" in paths
