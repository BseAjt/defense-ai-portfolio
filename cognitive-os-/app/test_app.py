from fastapi.testclient import TestClient

from main import app


def test_health() -> None:
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "memoryos", "version": "0.2.0"}


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

        listed = client.get("/api/memories")
        assert listed.status_code == 200
        assert any(item["title"] == "Test memory" for item in listed.json())


def test_all_agent_mindsets_are_available() -> None:
    with TestClient(app) as client:
        response = client.get("/api/executive/agents")
    assert response.status_code == 200
    agents = response.json()
    assert len(agents) == 15
    assert all(agent["mindset"] for agent in agents)
    assert all(agent["questions"] for agent in agents)
    assert all(agent["blind_spots"] for agent in agents)


def test_analysis_uses_agent_mindsets() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/api/executive/analyze",
            json={"idea": "Créer une plateforme IA avec un modèle business, une UX simple et une conformité RGPD."},
        )
    assert response.status_code == 200
    result = response.json()
    assert result["orchestrator"] == "ORION"
    assert result["selected_agents"] >= 8
    assert all(agent["mindset"] for agent in result["agents"])
    assert all(agent["key_question"] for agent in result["agents"])
    assert any(agent["name"] == "Portalis" for agent in result["agents"])
    assert any(agent["name"] == "Rams" for agent in result["agents"])
