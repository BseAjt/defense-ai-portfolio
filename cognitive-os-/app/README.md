# MemoryOS MVP

MVP local du Cognitive Operating System décrit dans le dossier `cognitive-os-`.

## Capacités

- capture de mémoires structurées ;
- timeline persistante SQLite ;
- recherche lexicale pondérée ;
- journal de décisions via API ;
- signaux de réflexion ;
- analyse d’idées avec ExecutiveOS ;
- interface web intégrée ;
- aucune clé d’API requise.

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

Puis ouvrir :

```text
http://127.0.0.1:8000
```

Documentation interactive de l’API :

```text
http://127.0.0.1:8000/docs
```

## Lancement Docker

```bash
docker build -t memoryos-mvp .
docker run --rm -p 8000:8000 -v memoryos-data:/app/data memoryos-mvp
```

## Endpoints principaux

- `POST /api/memories`
- `GET /api/memories`
- `GET /api/search?q=...`
- `POST /api/decisions`
- `GET /api/decisions`
- `GET /api/reflections`
- `POST /api/executive/analyze`
- `GET /health`

## Limites de cette version

La recherche est volontairement locale et sans modèle d’embeddings. ExecutiveOS utilise une orchestration déterministe. Les prochaines versions pourront ajouter un LLM, un graphe de connaissances, le chiffrement, l’authentification et des connecteurs externes.
