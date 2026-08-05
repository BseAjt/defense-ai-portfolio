# Chapitre 2 — Modèles de mémoire humaine et artificielle

## 2.1 Une analogie utile, mais dangereuse

Le vocabulaire de l’intelligence artificielle emprunte fréquemment ses termes à la psychologie : mémoire, attention, apprentissage, oubli, réflexion. Ces analogies sont utiles pour raisonner, mais elles peuvent créer une illusion de similitude.

La mémoire humaine est incarnée, affective, reconstructive et liée à une identité biologique. La mémoire artificielle est encodée, adressable, programmable et dépendante d’une architecture technique.

MemoryOS ne cherche pas à copier le cerveau. Il cherche à identifier les fonctions de continuité qui doivent être présentes dans un système cognitif numérique.

## 2.2 La mémoire humaine n’est pas un enregistrement

L’être humain ne conserve pas une copie fidèle de chaque expérience. Il reconstruit le passé à partir de traces, de schémas, d’émotions et d’objectifs présents.

Cette reconstruction explique plusieurs propriétés :

- les souvenirs changent lorsqu’ils sont rappelés ;
- l’émotion influence la consolidation ;
- le contexte facilite ou empêche le rappel ;
- les connaissances générales remplacent parfois les détails ;
- l’oubli peut protéger contre la surcharge.

Un COS ne doit donc pas supposer que la mémoire idéale consiste à tout enregistrer sans transformation.

## 2.3 Mémoire sensorielle et mémoire de travail

Les modèles cognitifs distinguent généralement une mémoire sensorielle très brève et une mémoire de travail limitée.

La mémoire de travail maintient les éléments nécessaires à une activité immédiate. Elle est comparable au contexte opérationnel d’un agent : instructions actives, objectifs courants, informations récemment récupérées et contraintes de la tâche.

Dans MemoryOS, cette fonction correspond au **Working Context**. Il ne doit pas être confondu avec la mémoire persistante.

Le Working Context est :

- limité ;
- temporaire ;
- orienté vers une tâche ;
- recomposé à chaque interaction ;
- alimenté par le Memory Engine.

La qualité d’un système dépend moins de la quantité totale d’informations disponibles que de sa capacité à sélectionner le bon contexte au bon moment.

## 2.4 Mémoire épisodique

La mémoire épisodique représente les événements vécus dans leur contexte temporel.

Exemples :

- une réunion précise ;
- une conversation ;
- une erreur commise pendant un projet ;
- une décision accompagnée de ses circonstances.

Dans MemoryOS, un épisode doit relier :

- une date ou une période ;
- des participants ;
- un lieu ou un canal ;
- des actions ;
- des objets cognitifs ;
- un état émotionnel ou préférentiel, lorsqu’il est pertinent ;
- des résultats.

L’épisode constitue une unité fondamentale de la Reasoning Timeline.

## 2.5 Mémoire sémantique

La mémoire sémantique conserve les concepts, faits, règles et relations qui ne dépendent plus d’un épisode particulier.

Par exemple, plusieurs expériences peuvent conduire à la connaissance suivante :

> Les décisions sans responsable explicite sont rarement exécutées.

Cette règle peut être rappelée sans reconstruire toutes les réunions qui l’ont produite. Le système doit cependant pouvoir retrouver les épisodes qui la justifient.

La mémoire sémantique de MemoryOS repose donc sur une double capacité :

- fournir une connaissance consolidée ;
- préserver le chemin vers ses sources.

## 2.6 Mémoire procédurale

La mémoire procédurale concerne les compétences, routines et séquences d’actions.

Dans un système cognitif, elle peut représenter :

- une procédure de préparation de réunion ;
- une méthode d’analyse stratégique ;
- un workflow de validation ;
- une manière préférée de rédiger ;
- une séquence d’outils permettant d’accomplir une tâche.

Ces procédures doivent pouvoir être exécutées, évaluées et améliorées. Elles ne sont pas de simples documents. Elles possèdent des préconditions, des étapes, des sorties et des critères de réussite.

## 2.7 La consolidation

Chez l’humain, la consolidation transforme progressivement certaines expériences en souvenirs plus stables. Dans MemoryOS, la consolidation est un processus explicite.

Elle peut :

- fusionner des observations similaires ;
- extraire une règle ;
- renforcer une relation ;
- réduire la granularité de détails anciens ;
- créer un résumé durable ;
- augmenter ou diminuer la confiance.

La consolidation ne doit jamais supprimer silencieusement les sources. Une synthèse peut devenir l’objet de rappel principal, tandis que les épisodes d’origine restent accessibles.

## 2.8 L’oubli comme fonction

L’oubli n’est pas uniquement une défaillance. Il permet de réduire l’interférence et la surcharge.

Un Cognitive Operating System doit distinguer plusieurs mécanismes :

- **suppression** : effacement volontaire ou réglementaire ;
- **expiration** : perte de validité après une date ;
- **dépriorisation** : réduction du poids dans le rappel ;
- **compression** : remplacement de détails par une synthèse ;
- **archivage** : conservation hors du contexte courant ;
- **inhibition** : exclusion temporaire d’éléments non pertinents.

Le système idéal ne retient pas tout avec la même intensité. Il maintient une mémoire sélective, contrôlable et réversible lorsque cela est possible.

## 2.9 Les limites des mémoires artificielles actuelles

Les systèmes contemporains emploient plusieurs formes de mémoire :

- fenêtres de contexte ;
- historiques de conversation ;
- bases vectorielles ;
- graphes de connaissances ;
- profils utilisateur ;
- caches ;
- journaux d’événements.

Chacune résout une partie du problème.

Une fenêtre de contexte maintient une continuité locale, mais elle est limitée. Une base vectorielle retrouve des contenus proches, mais ne représente pas nécessairement la temporalité ou la causalité. Un graphe relie des entités, mais peut perdre la texture des épisodes. Un profil conserve des préférences, mais pas l’histoire de leur formation.

MemoryOS doit les combiner sans les confondre.

## 2.10 Une architecture de mémoire hybride

Le modèle cible comporte au moins cinq espaces complémentaires :

1. **Working Context** — contexte temporaire de la tâche ;
2. **Episodic Store** — événements et expériences ;
3. **Semantic Graph** — connaissances consolidées ;
4. **Procedural Library** — compétences et workflows ;
5. **Identity Memory** — préférences, rôles, objectifs et continuité personnelle.

Un sixième espace, la **Reflective Memory**, conserve les leçons tirées de l’analyse des autres mémoires.

## 2.11 Le rappel comme reconstruction

Le rappel ne doit pas être une simple recherche.

Lorsqu’un utilisateur demande :

> Pourquoi avons-nous abandonné cette option ?

le système doit reconstruire une réponse à partir :

- de la décision ;
- des alternatives ;
- des arguments ;
- du contexte historique ;
- des conséquences observées ;
- de la situation actuelle.

Le résultat est un objet de contexte produit pour une question précise. Il doit distinguer les faits retrouvés des inférences nouvelles.

## 2.12 Mémoire humaine augmentée, non remplacée

MemoryOS ne prétend pas remplacer la mémoire humaine. Il doit agir comme une infrastructure de continuité :

- retrouver ce qui est difficile à rappeler ;
- préserver le contexte ;
- révéler des relations ;
- signaler les contradictions ;
- aider à réviser une décision.

L’utilisateur demeure l’autorité sur le sens de son histoire. Le système propose, relie et explique. Il ne doit pas réécrire silencieusement l’identité de son propriétaire.

## 2.13 Conclusion

La mémoire humaine montre que se souvenir implique sélection, reconstruction, consolidation et oubli. Les systèmes artificiels apportent la traçabilité, l’adressabilité et la capacité de relier de grands volumes.

Le Cognitive Operating System doit associer ces forces sans prétendre reproduire le cerveau. Son objectif n’est pas une mémoire parfaite, mais une continuité utile, explicable et gouvernable.