"""
Defense Dual-Agent Debrief — CLI
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from src.debrief_agent import DualAgentDebriefSynthesizer, render_synthesis, run_evals

# ── Realistic DIADÈME project debrief sample ─────────────────────────────────
SAMPLE_DEBRIEF = """
COMPTE-RENDU DE DEBRIEF PROJET
Projet : Déploiement DIADÈME Phase 2 — Extension DIRISI Île-de-France
Date : Janvier 2026 | Chef de projet : CDT Martin | Durée réelle : 14 mois (prévu : 9 mois)

RÉSUMÉ EXÉCUTIF
Le déploiement a finalement abouti mais avec 5 mois de retard et un dépassement budgétaire de 23%. 
Les 12 000 nouveaux utilisateurs (AND et DGNUM) sont opérationnels depuis le 15 janvier 2026. 
La satisfaction utilisateur à 30 jours est de 67% (objectif : 80%).

POINTS POSITIFS
- L'intégration avec CONCERTO (annuaire LDAP) s'est passée sans incident après la correction du bug 
  d'encodage UTF-8 sur les noms à caractères spéciaux (semaine 8)
- Le module Service Portal responsive a été adopté immédiatement par les personnels mobiles
- L'équipe projet a maintenu un excellent niveau de communication malgré les tensions
- Zéro incident de sécurité pendant la migration des données

PROBLÈMES RENCONTRÉS
1. TECHNIQUE — Compatibilité Oracle Exadata : Le middleware d'intégration entre ServiceNow et Oracle 
   Exadata v19c a nécessité 3 refontes majeures. La documentation ServiceNow ne couvrait pas la version 
   Exadata déployée au DIRISI. Un patch JDBC custom a dû être développé par l'équipe (6 semaines de travail non planifié).

2. RÉGLEMENTAIRE — Validation ANSSI : La demande d'homologation pour le traitement des données DR a pris 
   18 semaines au lieu des 8 semaines prévues. L'ANSSI a demandé une analyse de risque complémentaire 
   sur le chiffrement des données au repos (AES-256 jugé insuffisant pour certains types de données, 
   nécessité de passer à AES-256-GCM avec validation de l'IV). 2 aller-retours avec l'ANSSI.

3. RH/COMPÉTENCES : L'intégrateur (Sopra Steria) a changé son architecte technique en semaine 12, 
   entraînant une perte de connaissance significative. La reprise en main par le nouvel architecte 
   a pris 4 semaines. Le chef de projet côté Sopra manquait d'expérience sur les contraintes défense.

4. OPÉRATIONNEL — Formation : Le plan de formation initial sous-estimait la diversité des profils 
   utilisateurs (militaires vs civils vs contractuels). 3 parcours de formation distincts auraient dû 
   être préparés dès le départ au lieu d'un parcours unique adapté en urgence en semaine 30.

5. FINANCIER : Le poste "développements spécifiques" a dépassé de 340% son budget initial (180k€ 
   initiaux → 612k€ final) principalement à cause du patch Exadata et des adaptations ANSSI non prévues.

RISQUES RÉSIDUELS
- La CMDB reste à 67% de complétude (objectif contractuel : 95%). Un plan de remédiation est en cours.
- 3 workflows critiques utilisent encore l'ancienne API ServiceNow (dépréciée en 2027). Migration à planifier.
- La documentation technique du patch Exadata n'est pas encore formalisée.

RECOMMANDATIONS DE L'ÉQUIPE
- Intégrer une clause contractuelle d'expérience défense obligatoire pour les architectes des intégrateurs
- Prévoir systématiquement 4 mois pour les homologations ANSSI (jamais moins)
- Constituer une "bibliothèque de patchs" pour les intégrations récurrentes (Exadata, CONCERTO, ALLIANCE)
- Inclure la CMDB dans le périmètre de recette (condition sine qua non de réception)
"""


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Defense Dual-Agent Debrief Synthesizer")
    parser.add_argument("--file", type=str, help="Path to debrief text file")
    parser.add_argument("--project", type=str, default="DIADÈME Phase 2", help="Project name")
    parser.add_argument("--eval", action="store_true", help="Run eval suite")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            debrief_text = f.read()
    else:
        print("Using built-in DIADÈME Phase 2 debrief sample.\n")
        debrief_text = SAMPLE_DEBRIEF

    synthesizer = DualAgentDebriefSynthesizer()
    synthesis = synthesizer.synthesize(debrief_text, project_name=args.project)

    print("\n" + "="*55)

    if args.json:
        import dataclasses, json
        print(json.dumps(dataclasses.asdict(synthesis), ensure_ascii=False, indent=2))
    else:
        evals = run_evals(synthesis) if args.eval else None
        print(render_synthesis(synthesis, evals))

    print(f"\n⏱  Total: {synthesis.processing_time_s}s | {synthesis.total_tokens} tokens (3 LLM calls)")


if __name__ == "__main__":
    main()
