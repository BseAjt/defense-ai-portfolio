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
- interface web intégrée ;
- aucune clé d’API requise.

## Architecture — Sprints 1 et 2

```text
app/
├── main.py
├── config/
│   ├── agents.json         # source de vérité du Board
│   └── README.md
├── memoryos/
│   ├── agent_registry.py   # chargement, validation et sélection
│   ├── app_factory.py
│   ├── api.py
│   ├── config.py
│   ├── database.py
│   ├── repositories.py
│   ├── schemas.py
│   └── services.py
├── static/
│   └── index.html
└── test_app.py
```

Les routes publiques restent stables. Les agents et leurs mindsets peuvent désormais évoluer indépendamment du code Python.

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

La variable `MEMORYOS_DATA_DIR` choisit le répertoire de données. Par défaut, la base est créée dans `app/data/memoryos.db`.

```bash
export MEMORYOS_DATA_DIR=/chemin/vers/memoryos-data
```

### Équipe ExecutiveOS

Le Board est défini dans `config/agents.json`. Une équipe alternative peut être chargée avec :

```bash
export MEMORYOS_AGENT_CONFIG=/chemin/vers/mon-equipe.json
```

Après une modification, rechargez les profils sans redémarrer l’application :

```bash
curl -X POST http://127.0.0.1:8000/api/executive/agents/reload
```

Le format complet est documenté dans `config/README.md`.

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

- `POST /api/memories`
- `GET /api/memories`
- `GET /api/search?q=...`
- `POST /api/decisions`
- `GET /api/decisions`
- `GET /api/reflections`
- `GET /api/executive/agents`
- `POST /api/executive/agents/reload`
- `POST /api/executive/analyze`
- `GET /health`

## Limites de cette version

La recherche reste locale et lexicale. ExecutiveOS utilise encore une orchestration déterministe. Le prochain sprint introduira le Cognitive Graph pour relier mémoires, décisions, personnes, projets et idées.
