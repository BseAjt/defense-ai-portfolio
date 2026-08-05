# Chapitre 4 — Les principes fondateurs

## 4.1 Un système cognitif exige des principes

Une architecture peut évoluer. Les modèles, les interfaces et les infrastructures peuvent être remplacés. Les principes doivent rester suffisamment stables pour guider ces transformations.

MemoryOS repose sur un ensemble de principes fondateurs destinés à orienter toute implémentation future.

## 4.2 La mémoire est indépendante du modèle

La mémoire ne doit appartenir ni à un modèle de langage, ni à une application, ni à un fournisseur.

Un utilisateur doit pouvoir changer de moteur de raisonnement sans perdre son histoire. Les modèles sont des capacités d’interprétation et de génération. La mémoire est un patrimoine durable.

Cette séparation est la première condition de souveraineté cognitive.

## 4.3 Le contexte fait partie de la connaissance

Un contenu privé de son contexte perd une partie de sa signification.

Toute connaissance importante doit pouvoir conserver :

- son origine ;
- sa date ;
- son objectif ;
- ses relations ;
- ses hypothèses ;
- son niveau de confiance ;
- son domaine de validité.

Le contexte ne doit pas être reconstruit après coup. Il doit être capturé avec l’objet.

## 4.4 Toute décision possède une histoire

Une décision ne doit jamais être réduite à son résultat.

Le système doit préserver les alternatives, les contraintes, les arguments, les désaccords et les critères ayant conduit au choix.

Cette histoire rend la décision explicable. Elle permet également de la réévaluer lorsque le contexte change.

## 4.5 La connaissance est relationnelle

Les objets cognitifs ne sont pas des unités isolées.

Ils existent par leurs liens avec des personnes, des projets, des objectifs, des événements, des conversations, des hypothèses et d’autres connaissances.

Toute implémentation doit donc traiter les relations comme des éléments de premier ordre, avec leur propre provenance, leur temporalité et leur niveau de confiance.

## 4.6 La mémoire est sélective

Tout conserver ne signifie pas tout mémoriser.

Une mémoire utile sélectionne, hiérarchise et compresse. Elle distingue l’éphémère du durable, le bruit du signal, l’information opérationnelle de l’apprentissage structurant.

MemoryOS doit permettre plusieurs niveaux de rétention, de granularité et d’importance.

## 4.7 Le système doit savoir douter

Une architecture cognitive ne doit pas présenter toutes ses connaissances avec la même certitude.

Elle doit distinguer :

- les faits vérifiés ;
- les déclarations rapportées ;
- les hypothèses ;
- les interprétations ;
- les préférences ;
- les prédictions.

Elle doit aussi signaler les contradictions et conserver plusieurs points de vue lorsqu’aucun arbitrage légitime n’est possible.

## 4.8 Les connaissances vieillissent

Chaque connaissance possède une temporalité.

Le système doit pouvoir identifier les objets qui nécessitent une révision en raison de leur ancienneté, d’un changement de contexte, d’une nouvelle source ou d’une contradiction apparue plus tard.

La maintenance de la mémoire est une fonction native, pas une opération exceptionnelle.

## 4.9 La réflexion est une boucle permanente

La valeur d’une mémoire augmente lorsqu’elle peut examiner son propre contenu.

Le système doit rechercher :

- les erreurs répétées ;
- les biais récurrents ;
- les décisions incohérentes ;
- les objectifs abandonnés mais encore actifs ;
- les apprentissages applicables à de nouvelles situations.

La réflexion transforme une histoire accumulée en capacité d’amélioration.

## 4.10 L’explicabilité précède l’autorité

Plus un système influence une décision importante, plus il doit être capable d’expliquer :

- quelles sources ont été utilisées ;
- quels souvenirs ont été mobilisés ;
- quelles hypothèses ont été formulées ;
- quelles incertitudes subsistent ;
- pourquoi une recommandation a été privilégiée.

Un système qui ne peut pas expliquer son raisonnement ne doit pas recevoir une autorité disproportionnée.

## 4.11 L’utilisateur reste propriétaire

La mémoire cognitive appartient à la personne ou à l’organisation qui l’a produite.

Elle doit être exportable, corrigible, supprimable et portable. Les mécanismes de consentement doivent être compréhensibles. Les usages secondaires doivent être limités et explicités.

La continuité cognitive ne peut être construite au prix de la perte de contrôle.

## 4.12 La sécurité est une propriété du noyau

Une mémoire cognitive peut contenir les éléments les plus sensibles d’une vie ou d’une organisation.

Le chiffrement, la séparation des rôles, l’audit, la minimisation et la gestion fine des accès doivent être intégrés dès l’architecture initiale.

La sécurité ne peut pas être ajoutée après la croissance du système.

## 4.13 L’action reste sous contrôle

Transformer une mémoire en action crée de la valeur, mais aussi du risque.

Le système doit distinguer la suggestion, la préparation, la validation et l’exécution. Les actions importantes doivent respecter des politiques explicites et, lorsque nécessaire, une confirmation humaine.

L’autonomie doit être proportionnelle à la confiance, à la réversibilité et à l’impact.

## 4.14 Une fondation durable

Ces principes définissent un contrat d’architecture.

Ils ne dictent pas une interface unique ni une technologie particulière. Ils établissent les conditions minimales pour qu’un système puisse prétendre préserver une continuité cognitive de manière utile, explicable et souveraine.
