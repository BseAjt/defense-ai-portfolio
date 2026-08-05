# MemoryOS MVP

MVP local du Cognitive Operating System décrit dans le dossier `cognitive-os-`.

## Capacités

- capture de mémoires structurées ;
- timeline persistante SQLite ;
- recherche lexicale pondérée ;
- journal de décisions ;
- signaux de réflexion ;
- analyse d’idées avec ExecutiveOS ;
- profils cognitifs pour 15 agents ;
- interface web intégrée ;
- aucune clé d’API requise.

## Architecture — Sprint 1

```text
app/
├── main.py                 # point d’entrée ASGI
├── agents.py               # profils cognitifs ExecutiveOS
├── memoryos/
│   ├── app_factory.py      # assemblage FastAPI
│   ├── api.py              # routes HTTP
│   ├── config.py           # configuration et chemins
│   ├── database.py         # cycle de vie SQLite
│   ├── repositories.py     # accès aux données
│   ├── schemas.py          # contrats Pydantic
│   └── services.py         # logique métier
├── static/
│   └── index.html
└── test_app.py
```

Les routes publiques sont inchangées. La logique métier, l’API et la persistance peuvent désormais évoluer indépendamment.

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

La variable `MEMORYOS_DATA_DIR` permet de choisir le répertoire de données. Par défaut, la base est créée dans `app/data/memoryos.db`.

```bash
export MEMORYOS_DATA_DIR=/chemin/vers/memoryos-data
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

- `POST /api/memories`
- `GET /api/memories`
- `GET /api/search?q=...`
- `POST /api/decisions`
- `GET /api/decisions`
- `GET /api/reflections`
- `GET /api/executive/agents`
- `POST /api/executive/analyze`
- `GET /health`

## Limites de cette version

La recherche reste locale et lexicale. ExecutiveOS utilise une orchestration déterministe. Les prochains sprints ajouteront la configuration externe des agents, le Cognitive Graph, le chiffrement, l’authentification et les connecteurs.
