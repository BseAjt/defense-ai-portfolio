# MemoryOS MVP

MVP local du Cognitive Operating System décrit dans le dossier `cognitive-os-`.

## Capacités

- capture de mémoires structurées ;
- journal de décisions ;
- Cognitive Graph persistant ;
- synchronisation automatique mémoire/décision vers le graphe ;
- recherche lexicale et recherche contextuelle ;
- consolidation des données historiques ;
- détection prudente de doublons ;
- signaux de réflexion ;
- ExecutiveOS avec 15 profils cognitifs configurables ;
- interface web intégrée ;
- aucune clé d’API requise.

## Architecture — Sprints 1 à 4

```text
app/
├── main.py
├── config/
│   ├── agents.json
│   └── README.md
├── memoryos/
│   ├── agent_registry.py
│   ├── app_factory.py
│   ├── api.py
│   ├── config.py
│   ├── database.py
│   ├── graph.py
│   ├── memory_engine.py
│   ├── repositories.py
│   ├── schemas.py
│   └── services.py
├── static/
│   └── index.html
└── test_app.py
```

### Memory Engine v0.5

Toute mémoire ou décision créée par l’API est automatiquement transformée en nœud du Cognitive Graph. La table `cognitive_links` maintient une correspondance stable entre l’objet métier et son nœud cognitif.

Le moteur permet également :

- le rattrapage des anciennes données avec une consolidation ;
- la suppression cohérente d’une mémoire et de son nœud ;
- la recherche d’une mémoire avec son voisinage cognitif ;
- la création de relations `duplicates` lorsque la similarité est forte ;
- l’observation de l’état du moteur.

## Lancement local

```bash
cd cognitive-os-/app
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Sous Windows :

```powershell
.venv\Scripts\activate
```

Puis ouvrir `http://127.0.0.1:8000`.

Documentation API : `http://127.0.0.1:8000/docs`.

## Configuration

### Données

```bash
export MEMORYOS_DATA_DIR=/chemin/vers/memoryos-data
```

Par défaut, la base est créée dans `app/data/memoryos.db`.

### Équipe ExecutiveOS

```bash
export MEMORYOS_AGENT_CONFIG=/chemin/vers/mon-equipe.json
```

Rechargement sans redémarrage :

```bash
curl -X POST http://127.0.0.1:8000/api/executive/agents/reload
```

## Memory Engine

Consolider les mémoires et décisions existantes :

```bash
curl -X POST http://127.0.0.1:8000/api/memory-engine/consolidate
```

Consulter l’état du moteur :

```bash
curl http://127.0.0.1:8000/api/memory-engine/status
```

Recherche contextuelle :

```bash
curl 'http://127.0.0.1:8000/api/memory-engine/context?q=strategie+produit'
```

## Docker

```bash
docker build -t memoryos-mvp .
docker run --rm -p 8000:8000 -v memoryos-data:/app/data memoryos-mvp
```

## Tests

```bash
pytest -q
```

## Endpoints principaux

### Mémoire et décisions

- `POST /api/memories`
- `GET /api/memories`
- `DELETE /api/memories/{id}`
- `GET /api/search?q=...`
- `POST /api/decisions`
- `GET /api/decisions`

### Memory Engine

- `GET /api/memory-engine/status`
- `POST /api/memory-engine/consolidate`
- `GET /api/memory-engine/context?q=...`

### Cognitive Graph

- `POST /api/graph/nodes`
- `GET /api/graph/nodes`
- `POST /api/graph/edges`
- `GET /api/graph/edges`
- `GET /api/graph/nodes/{id}/neighbors`
- `GET /api/graph`

### ExecutiveOS

- `GET /api/executive/agents`
- `POST /api/executive/agents/reload`
- `POST /api/executive/analyze`

## Limites de la version 0.5.0

La recherche reste lexicale et le moteur de doublons utilise une similarité de tokens. ExecutiveOS demeure déterministe. Les prochains sprints pourront ajouter un Reflection Engine enrichi, des embeddings optionnels, le chiffrement, l’authentification et les connecteurs externes.
