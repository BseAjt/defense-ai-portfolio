# MemoryOS MVP

MVP local du Cognitive Operating System décrit dans le dossier `cognitive-os-`.

## Capacités

- capture de mémoires structurées ;
- timeline persistante SQLite ;
- recherche lexicale pondérée ;
- journal de décisions ;
- signaux de réflexion ;
- analyse d’idées avec ExecutiveOS ;
- profils cognitifs configurables pour 15 agents ;
- rechargement à chaud de l’équipe ;
- Cognitive Graph persistant ;
- interface web intégrée ;
- aucune clé d’API requise.

## Architecture — Sprints 1 à 3

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
│   ├── graph.py             # nœuds, relations, voisinage, snapshot
│   ├── repositories.py
│   ├── schemas.py
│   └── services.py
├── static/
│   └── index.html
└── test_app.py
```

## Cognitive Graph

Types de nœuds :

- `memory`, `idea`, `decision`, `goal`, `project`, `person` ;
- `concept`, `document`, `conversation`, `event`.

Relations disponibles :

- `supports`, `contradicts`, `derived_from`, `depends_on` ;
- `created_by`, `mentions`, `belongs_to`, `validated_by` ;
- `causes`, `references`, `duplicates`, `supersedes`.

Chaque nœud et relation possède un niveau de confiance et des métadonnées JSON. La suppression d’un nœud supprime automatiquement ses relations.

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

`MEMORYOS_DATA_DIR` choisit le répertoire de données. `MEMORYOS_AGENT_CONFIG` permet de charger une équipe ExecutiveOS alternative.

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
- `GET /api/search?q=...`
- `POST /api/decisions`
- `GET /api/decisions`
- `GET /api/reflections`

### ExecutiveOS

- `GET /api/executive/agents`
- `POST /api/executive/agents/reload`
- `POST /api/executive/analyze`

### Cognitive Graph

- `POST /api/graph/nodes`
- `GET /api/graph/nodes`
- `GET /api/graph/nodes/{id}`
- `DELETE /api/graph/nodes/{id}`
- `POST /api/graph/edges`
- `GET /api/graph/edges`
- `GET /api/graph/nodes/{id}/neighbors`
- `GET /api/graph`

## Limites de cette version

Les nœuds du graphe sont encore créés explicitement via l’API. Le prochain sprint pourra automatiser la transformation des mémoires et décisions en objets du graphe, puis ajouter consolidation, détection de similarités et réflexion multi-hop.
