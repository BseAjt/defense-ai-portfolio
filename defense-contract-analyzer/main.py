"""
Defense Contract Analyzer — CLI & synthetic example generator

Since we can't ship real defense contracts, this module generates
a realistic synthetic contract PDF for testing and demonstration.
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def generate_synthetic_contract_pdf(output_path: str):
    """Generate a realistic synthetic defense IT contract as PDF for testing."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.units import cm
        from reportlab.lib import colors
    except ImportError:
        print("Installing reportlab for PDF generation...")
        os.system("pip install reportlab --break-system-packages -q")
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.units import cm

    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            leftMargin=2.5*cm, rightMargin=2.5*cm,
                            topMargin=2.5*cm, bottomMargin=2.5*cm)
    styles = getSampleStyleSheet()
    h1 = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=14, spaceAfter=12)
    h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=11, spaceAfter=8)
    body = ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, spaceAfter=6, leading=14)

    content = [
        Paragraph("MARCHÉ PUBLIC DE SERVICES INFORMATIQUES", h1),
        Paragraph("CONTRAT N° DIRISI-2025-IT-0847-A", h1),
        Paragraph("Plateforme ITSM Souveraine — Lot 1 : Licences et Intégration", styles['Heading2']),
        Spacer(1, 0.5*cm),

        Paragraph("ENTRE LES SOUSSIGNÉS", h2),
        Paragraph("La Direction Interarmées des Réseaux d'Infrastructure et des Systèmes d'Information (DIRISI), établissement public sous tutelle du Ministère des Armées, représentée par son Directeur Central, ci-après dénommée « le Pouvoir Adjudicateur » ou « le Ministère »,", body),
        Paragraph("ET", body),
        Paragraph("La société TechDefense SAS, au capital de 2 500 000 euros, immatriculée au RCS de Paris sous le numéro 512 345 678, représentée par son Directeur Général, ci-après dénommée « le Titulaire ».", body),
        Spacer(1, 0.3*cm),

        Paragraph("Article 1 — Objet du Marché", h2),
        Paragraph("Le présent marché a pour objet la fourniture, l'intégration et la maintenance en condition opérationnelle (MCO) d'une plateforme de gestion des services informatiques (ITSM) souveraine pour la DIRISI, incluant les licences d'utilisation pour 80 000 utilisateurs finaux, les services d'intégration avec les systèmes d'information ministériels existants, et le support technique pour une durée de quatre (4) ans.", body),

        Paragraph("Article 2 — Montant et Conditions Financières", h2),
        Paragraph("2.1 Le montant total du marché est fixé à 8 500 000 euros HT (huit millions cinq cent mille euros hors taxes), réparti comme suit : Licences et souscriptions annuelles : 4 200 000 € HT ; Services d'intégration et de déploiement : 2 800 000 € HT ; Support et maintenance MCO : 1 500 000 € HT.", body),
        Paragraph("2.2 Les prix sont fermes et non révisables pour la première année. À compter de la deuxième année, les prix pourront être révisés selon la formule : P = P0 × (1 + 0,5 × (SYNTEC(n)/SYNTEC(0) - 1)), où SYNTEC(n) est l'indice SYNTEC du mois de révision.", body),

        Paragraph("Article 5 — Obligations de Souveraineté et Localisation des Données", h2),
        Paragraph("5.1 LOCALISATION : L'ensemble des données traitées dans le cadre du présent marché devra être hébergé exclusivement sur le territoire de la République française, sur des infrastructures sous contrôle de ressortissants français ou de personnes morales de droit français, et ne pouvant être soumises à aucune législation extraterritoriale étrangère, notamment le CLOUD Act américain ou tout règlement équivalent.", body),
        Paragraph("5.2 CERTIFICATION : Le Titulaire s'engage à obtenir, dans un délai de dix-huit (18) mois suivant la notification du marché, la qualification SecNumCloud de l'ANSSI pour les composants hébergeant des données à caractère sensible. À défaut d'obtention dans ce délai, le Ministère pourra résilier le marché aux torts exclusifs du Titulaire, sans indemnité.", body),
        Paragraph("5.3 CONTRÔLE : Le Ministère se réserve le droit de procéder à des audits techniques inopinés de l'infrastructure du Titulaire, avec un préavis de 48 heures, afin de vérifier le respect des obligations de souveraineté. Le Titulaire ne pourra s'opposer à ces audits.", body),

        Paragraph("Article 7 — Pénalités de Retard et de Non-Conformité", h2),
        Paragraph("7.1 RETARD DE LIVRAISON : En cas de retard dans la livraison des jalons définis au calendrier contractuel (Annexe B), le Titulaire sera redevable de pénalités de retard calculées à raison de 1/1000 (un millième) du montant total HT du marché par jour calendaire de retard, sans mise en demeure préalable.", body),
        Paragraph("7.2 NON-RESPECT DES SLA : Le non-respect des niveaux de service définis à l'Article 8 entraîne l'application automatique de pénalités de service selon le barème suivant : disponibilité inférieure à 99% : 5% du mensuel ; inférieure à 97% : 15% du mensuel ; inférieure à 95% : résiliation pour faute.", body),
        Paragraph("7.3 PLAFOND : Le cumul des pénalités de toute nature est plafonné à 15% (quinze pour cent) du montant total HT du marché. L'application du plafond ne fait pas obstacle à la résiliation du marché.", body),

        Paragraph("Article 8 — Niveaux de Service (SLA)", h2),
        Paragraph("Le Titulaire s'engage à maintenir les niveaux de service suivants : Disponibilité de la plateforme : 99,5% calculée sur base mensuelle, hors fenêtres de maintenance planifiées (maximum 4h/mois, entre 22h et 6h) ; Temps de résolution des incidents critiques (P1) : 4 heures ouvrées ; Temps de résolution des incidents majeurs (P2) : 8 heures ouvrées ; Plage de support : 7j/7, 24h/24 pour les incidents P1.", body),

        Paragraph("Article 10 — Propriété Intellectuelle", h2),
        Paragraph("10.1 DÉVELOPPEMENTS SPÉCIFIQUES : Tous les développements, adaptations, configurations et paramétrages réalisés spécifiquement dans le cadre du présent marché sont cédés au Ministère dès leur livraison, à titre exclusif, pour toute durée et tout territoire. Cette cession inclut le droit de modifier, reproduire, distribuer et exploiter ces développements, y compris à des fins autres que celles du présent marché.", body),
        Paragraph("10.2 PROPRIÉTÉ DU TITULAIRE : Les droits sur les composants standards du Titulaire antérieurs au marché (logiciels, méthodologies, outils) restent la propriété exclusive du Titulaire. Toutefois, le Titulaire accorde au Ministère une licence perpétuelle, irrévocable et cessible sur ces composants pour les besoins du présent marché et de son exploitation ultérieure.", body),

        Paragraph("Article 12 — Résiliation", h2),
        Paragraph("12.1 RÉSILIATION POUR MOTIF D'INTÉRÊT GÉNÉRAL : Le Ministère peut résilier le marché à tout moment pour motif d'intérêt général, moyennant un préavis de trois (3) mois. Dans ce cas, le Titulaire sera indemnisé des prestations réalisées et des frais engagés non amortis, sans indemnité au titre du manque à gagner sur la durée restante du marché.", body),
        Paragraph("12.2 RÉSILIATION AUX TORTS : En cas de manquement grave du Titulaire à ses obligations contractuelles, notamment en cas de violation des obligations de souveraineté, de dépassement du plafond de pénalités, ou de défaillance technique majeure, le Ministère pourra résilier le marché aux torts exclusifs du Titulaire sans indemnité, après mise en demeure restée sans effet pendant trente (30) jours.", body),
        Paragraph("12.3 TRANSFERT DE COMPÉTENCES : En cas de résiliation, quelle qu'en soit la cause, le Titulaire s'engage à assurer une période de réversibilité de six (6) mois, pendant laquelle il mettra à disposition ses équipes et sa documentation pour faciliter la reprise par un nouveau prestataire. Cette période de réversibilité sera rémunérée au tarif journalier défini en Annexe C.", body),

        Paragraph("Article 14 — Loi Applicable et Juridiction", h2),
        Paragraph("Le présent marché est soumis au droit français. En cas de litige, les parties conviennent de rechercher une solution amiable. À défaut, le Tribunal Administratif de Paris sera seul compétent pour trancher tout différend relatif à l'interprétation ou l'exécution du présent marché.", body),

        Spacer(1, 1*cm),
        Paragraph("Fait à Paris, le 15 mars 2025", body),
        Paragraph("Pour le Pouvoir Adjudicateur : [Signature]     Pour le Titulaire : [Signature]", body),
    ]

    doc.build(content)
    print(f"  📄 Synthetic contract generated: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Analyze defense contract PDFs with Claude")
    parser.add_argument("--file", type=str, help="Path to contract PDF (or comma-separated list for multi-doc)")
    parser.add_argument("--demo", action="store_true", help="Generate a synthetic contract and analyze it")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    from src.analyzer import ContractAnalyzer, render_summary

    analyzer = ContractAnalyzer()

    if args.demo or not args.file:
        print("🛡️  Defense Contract Analyzer — Demo Mode")
        print("Generating synthetic DIRISI-2025-IT-0847-A contract...\n")
        pdf_path = "/tmp/DIRISI_2025_IT_0847_A.pdf"
        generate_synthetic_contract_pdf(pdf_path)

        print("\n🔍 Analyzing contract with Claude...\n")
        summary = analyzer.analyze_pdf(pdf_path)

        if args.json:
            import dataclasses
            print(json.dumps(dataclasses.asdict(summary), ensure_ascii=False, indent=2))
        else:
            print(render_summary(summary))

        print(f"\n⏱  {summary.processing_time_s}s | {summary.tokens_used} tokens")

    elif "," in args.file:
        paths = [p.strip() for p in args.file.split(",")]
        print(f"🛡️  Analyzing {len(paths)} contracts...\n")
        report = analyzer.analyze_multiple(paths)
        print(f"\n{'='*60}")
        print(f"CONSOLIDATED RISK: {report.consolidated_risk}")
        print(f"ACTION: {report.recommended_action}")
        if report.cross_document_conflicts:
            print(f"\nCONFLICTS DETECTED:")
            for c in report.cross_document_conflicts:
                print(f"  ⚠️  {c}")
    else:
        summary = analyzer.analyze_pdf(args.file)
        print(render_summary(summary))


if __name__ == "__main__":
    import json
    main()
