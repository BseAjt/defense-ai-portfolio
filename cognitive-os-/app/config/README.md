# Configuration des agents ExecutiveOS

Le fichier `agents.json` est la source de vérité des profils cognitifs. Aucun changement Python n’est nécessaire pour modifier un agent, ses mots-clés ou le Board convoqué par défaut.

## Structure racine

```json
{
  "version": 1,
  "default_agents": ["Augustus", "Sun Tzu"],
  "agents": []
}
```

## Champs obligatoires d’un agent

- `name`
- `inspiration`
- `role`
- `mission`
- `mindset`
- `questions`
- `refuses`
- `blind_spots`
- `style`
- `analysis`
- `keywords`

Les champs `mindset`, `questions`, `refuses`, `blind_spots` et `keywords` sont des listes de chaînes non vides.

## Sélection des agents

Les agents présents dans `default_agents` sont toujours convoqués. Les autres sont ajoutés lorsque l’un de leurs `keywords` apparaît dans le sujet analysé.

## Rechargement

Après modification du JSON :

```bash
curl -X POST http://127.0.0.1:8000/api/executive/agents/reload
```

Une configuration invalide est refusée explicitement : champ manquant, nom dupliqué, liste mal formée ou agent par défaut inconnu.

## Fichier alternatif

La variable suivante permet de charger une autre équipe :

```bash
export MEMORYOS_AGENT_CONFIG=/chemin/vers/mon-equipe.json
```

Cette capacité permet de créer plusieurs Boards spécialisés sans forker le code applicatif.
