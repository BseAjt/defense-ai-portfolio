"""
Defense Incident Classifier — CLI

Usage:
    python main.py                      # Run on demo incidents (streaming visible)
    python main.py --incident "text"    # Classify a single incident
    python main.py --batch              # Run all demo incidents + eval suite
    python main.py --no-stream          # Suppress streaming output
"""

import sys, os, argparse, json
sys.path.insert(0, os.path.dirname(__file__))

from src.classifier import IncidentClassifier, render_classification, run_evals

# ── Demo incidents — realistic ITSM scenarios for French defense ──────────────
DEMO_INCIDENTS = [
    {
        "id": "INC-2025-0341",
        "description": (
            "Panne totale du réseau ISIS sur la base aérienne de Mont-de-Marsan. "
            "Environ 800 utilisateurs sont sans accès au réseau intradef depuis 07h30. "
            "Le centre opérations n'a plus accès aux systèmes de commandement. "
            "La cellule SSI signale une possible tentative d'intrusion détectée la veille."
        )
    },
    {
        "id": "INC-2025-0342",
        "description": (
            "Impossible d'ouvrir mes fichiers de travail sur le serveur partagé depuis ce matin. "
            "Message d'erreur : 'Accès refusé'. Mon collègue a le même problème. "
            "Nous sommes dans le bureau des ressources humaines de l'état-major."
        )
    },
    {
        "id": "INC-2025-0343",
        "description": (
            "L'application ALLIANCE ne répond plus depuis 30 minutes. "
            "Environ 200 agents de la DIRISI Île-de-France ne peuvent plus envoyer ni recevoir de messages. "
            "Des courriels contenant des documents DR (Diffusion Restreinte) étaient en cours d'envoi."
        )
    },
    {
        "id": "INC-2025-0344",
        "description": (
            "Le serveur d'impression du couloir B3 ne répond plus. "
            "Seulement 3 personnes utilisent cette imprimante. "
            "Nous avons redémarré l'imprimante mais le problème persiste."
        )
    },
    {
        "id": "INC-2025-0345",
        "description": (
            "Détection d'une tentative d'accès non autorisée sur notre instance ServiceNow DIADÈME. "
            "Les logs montrent 347 tentatives de connexion échouées depuis une IP externe en 10 minutes. "
            "L'IP source semble appartenir à un pays non-OTAN. "
            "Aucune compromission confirmée à ce stade mais l'activité est suspecte. "
            "Des données IGI 1300 niveau DR sont stockées dans cette instance."
        )
    },
]


def main():
    parser = argparse.ArgumentParser(description="Defense ITSM Incident Classifier")
    parser.add_argument("--incident", type=str, help="Classify a single incident description")
    parser.add_argument("--batch", action="store_true", help="Run all demo incidents with eval suite")
    parser.add_argument("--no-stream", action="store_true", help="Suppress streaming output")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    classifier = IncidentClassifier()
    show_stream = not args.no_stream

    if args.incident:
        # Single incident from CLI arg
        result = classifier.classify_streaming(
            incident_text=args.incident,
            incident_id="INC-CLI",
            show_stream=show_stream
        )
        evals = run_evals(result, args.incident)
        print("\n" + render_classification(result, evals))

    elif args.batch:
        # Full batch with eval summary
        print("🛡️  Defense Incident Classifier — Batch Mode")
        print(f"Processing {len(DEMO_INCIDENTS)} incidents...\n")

        results = []
        for inc in DEMO_INCIDENTS:
            c = classifier.classify_streaming(
                incident_text=inc["description"],
                incident_id=inc["id"],
                show_stream=show_stream
            )
            evals = run_evals(c, inc["description"])
            results.append((c, evals))

        print("\n" + "="*60)
        print("BATCH RESULTS SUMMARY")
        print("="*60)
        for c, evals in results:
            status = "✅" if evals["passed"] else "❌"
            sovereign = " 🔐" if c.sovereign_flag else ""
            print(f"{status} {c.incident_id} → {c.priority} | {c.assigned_team}{sovereign} | eval {evals['overall']:.0%}")

        passed = sum(1 for _, e in results if e["passed"])
        avg_time = sum(c.processing_time_s for c, _ in results) / len(results)
        avg_tokens = sum(c.tokens_used for c, _ in results) / len(results)
        print(f"\nEval pass rate: {passed}/{len(results)} | Avg {avg_time:.1f}s | Avg {avg_tokens:.0f} tokens/incident")

    else:
        # Default: demo on first 2 incidents with streaming visible
        print("🛡️  Defense Incident Classifier — Demo Mode")
        print("Streaming classification in real-time...\n")

        for inc in DEMO_INCIDENTS[:2]:
            print(f"\n📥 INCIDENT: {inc['id']}")
            print(f"Description: {inc['description'][:120]}...")
            c = classifier.classify_streaming(
                incident_text=inc["description"],
                incident_id=inc["id"],
                show_stream=True
            )
            evals = run_evals(c, inc["description"])
            print("\n" + render_classification(c, evals))
            print()


if __name__ == "__main__":
    main()
