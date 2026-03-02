# Exemple d'appel d'offres — Fictional, à des fins de test uniquement
# Inspiré de la structure réelle des marchés défense BOAMP/PLACE

AO_SAMPLE_TEXT = """
AVIS DE MARCHÉ — FOURNITURES ET SERVICES

Référence : AO-2025-DIRISI-0847
Section I — Pouvoir adjudicateur
I.1) Nom, adresses et point(s) de contact :
Direction Interarmées des Réseaux d'Infrastructure et des Systèmes d'Information (DIRISI)
BP 73 — 00998 Armées
Point de contact : Bureau Achats Informatique — bai.dirisi@intradef.gouv.fr

Section II — Objet du marché
II.1.1) Intitulé : Acquisition d'une plateforme ITSM souveraine avec capacités d'automatisation IA
II.1.2) Type de marché : Services et fournitures
II.1.5) Description succincte :
La DIRISI lance un marché pour l'acquisition, le déploiement et le maintien en condition opérationnelle (MCO) 
d'une plateforme de gestion des services informatiques (ITSM) intégrant des capacités d'intelligence artificielle 
pour l'automatisation des incidents et des demandes de service. La solution devra être déployée en mode 
souverain (Self-Hosted ou Hébergement HDS/SecNumCloud qualifié) et s'interfacer avec les SI ministériels 
existants dont ALLIANCE (messagerie), CONCERTO (annuaire), et le réseau ISIS.

La solution devra impérativement respecter le cadre IGI 1300 pour les données Diffusion Restreinte (DR), 
la PSSIE (Politique de Sécurité des Systèmes d'Information de l'État), et le référentiel général de sécurité (RGS v2).
Toute donnée devra rester sur le territoire national français.

II.1.6) Classification CPV : 72212000-4 (Services de développement de logiciels applicatifs)
II.2.1) Quantité ou étendue du marché :
Valeur estimée hors TVA : 8 500 000 EUR
Ce montant comprend la licence, l'intégration, la formation, et le MCO sur 4 ans.
Option de renouvellement : 2 ans supplémentaires pour un total de 6 ans / 12 000 000 EUR maximum.

Section III — Renseignements d'ordre juridique, économique, financier et technique
III.1.1) Conditions de participation :
- Habilitation SECRET DÉFENSE pour l'équipe projet (minimum 5 personnes)
- Référence(s) dans le secteur défense ou sécurité nationale française (au minimum 2 références > 1M€ sur 5 ans)
- Certification ISO 27001 de l'entreprise ou de son sous-traitant hébergement
- La solution proposée devra être qualifiée ou en cours de qualification ANSSI (niveau Standard minimum)

III.2.3) Capacité technique :
- L'intégration avec CONCERTO (annuaire LDAP/AD du MinArm) est obligatoire
- L'intégration avec ALLIANCE (messagerie défense) via API REST est requise
- Compatibilité avec Oracle Exadata (infrastructure base de données DIRISI) requise
- Temps de déploiement maximum : 18 mois pour le périmètre initial (15 000 utilisateurs)
- La solution doit supporter 80 000 utilisateurs à terme

Section IV — Procédure
IV.1.1) Type de procédure : Appel d'offres restreint avec négociation (article R2124-3 du CMP)
IV.2.1) Critères d'attribution :
- Valeur technique : 60 points
  * Pertinence fonctionnelle et adéquation aux besoins (25 pts)
  * Architecture technique et sécurité (20 pts)
  * Capacités d'intégration (15 pts)
- Prix : 30 points
- Délais et planning : 10 points

IV.3.4) Date limite de réception des offres : 2025-09-30T17:00:00+02:00
IV.3.6) Délai minimum pendant lequel le soumissionnaire est tenu de maintenir son offre : 180 jours

Section VI — Renseignements complémentaires
VI.3) Informations complémentaires :
Le présent marché est soumis aux dispositions du code des marchés de défense et de sécurité (CMDS).
Les variantes ne sont pas autorisées.
Un accord de confidentialité devra être signé préalablement à la communication du dossier de consultation.
Des pénalités de retard sont prévues : 0,5% du montant mensuel par semaine de retard, plafonnées à 10%.
Une clause de résiliation pour motif d'intérêt général est incluse (art. L2195-4 CMP).

Concurrent(s) identifié(s) sur ce marché : une ESN française ayant déjà réalisé une mission similaire 
pour le Ministère de l'Intérieur est pressentie. Un éditeur américain est également en position, 
mais sa conformité souveraineté est questionnée par le MOA.
"""
