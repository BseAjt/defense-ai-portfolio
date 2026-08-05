# Chapitre 1 — Donnée, information, connaissance, mémoire et raisonnement

## 1.1 Pourquoi ces distinctions sont indispensables

Les systèmes numériques emploient souvent les mots *donnée*, *information*, *connaissance* et *mémoire* comme s’ils étaient interchangeables. Cette confusion est acceptable dans une application ordinaire. Elle devient dangereuse dans un Cognitive Operating System.

Un COS doit savoir ce qu’il reçoit, ce qu’il transforme, ce qu’il croit, ce qu’il rappelle et ce qu’il déduit. Sans séparation conceptuelle, il ne peut ni expliquer ses recommandations, ni gérer l’incertitude, ni détecter qu’une connaissance a vieilli.

MemoryOS adopte donc une hiérarchie opérationnelle :

```text
Donnée → Information → Connaissance → Mémoire → Raisonnement → Décision → Apprentissage
```

Cette représentation n’est pas une chaîne rigide. Les éléments peuvent revenir en arrière, être corrigés, fusionnés ou invalidés. Elle constitue néanmoins une carte utile des transformations cognitives.

## 1.2 La donnée : une observation encodée

Une donnée est une représentation élémentaire d’un état, d’un événement ou d’une mesure.

Exemples :

- `14:00` ;
- une température de 22 °C ;
- le nom d’un participant ;
- un clic sur un bouton ;
- une phrase extraite d’un message.

Une donnée ne porte pas seule sa signification. `14:00` peut désigner le début d’une réunion, une heure de livraison ou un délai. Son interprétation dépend d’un schéma, d’une source et d’un contexte.

Dans MemoryOS, toute donnée doit être accompagnée, autant que possible, de trois propriétés :

1. **provenance** — d’où vient-elle ?
2. **temporalité** — quand a-t-elle été produite ou observée ?
3. **portée** — à quel objet, personne ou projet se rapporte-t-elle ?

Une donnée sans provenance peut être utile. Elle ne doit jamais être traitée comme aussi fiable qu’une donnée traçable.

## 1.3 L’information : une donnée contextualisée

Une information apparaît lorsqu’une donnée reçoit une interprétation suffisante pour réduire une incertitude.

La donnée `14:00` devient une information lorsque le système sait :

> La réunion de cadrage MemoryOS commence à 14:00 le 5 août 2026.

L’information possède donc une structure relationnelle. Elle associe une valeur à un sujet, un contexte et une période.

Une information peut être correcte sans être utile. Son utilité dépend de l’objectif actif. L’heure d’une réunion est importante avant la réunion et presque sans valeur plusieurs mois plus tard, sauf si elle permet de reconstruire une chronologie.

Le COS doit distinguer :

- la **validité** d’une information ;
- sa **pertinence** pour une tâche ;
- sa **durée de vie** ;
- sa **sensibilité** ;
- son **niveau de confiance**.

## 1.4 La connaissance : une relation stabilisée

La connaissance n’est pas une information plus longue. Elle est une relation suffisamment validée pour être réutilisée dans plusieurs contextes.

Exemple :

> Les décisions produit sont généralement validées pendant la réunion de cadrage hebdomadaire.

Cette connaissance agrège plusieurs observations et conserve une certaine stabilité. Elle peut être descriptive, procédurale, causale ou normative.

MemoryOS distingue notamment :

- **connaissance déclarative** : savoir que quelque chose est vrai ;
- **connaissance procédurale** : savoir comment accomplir une action ;
- **connaissance causale** : savoir pourquoi un effet se produit ;
- **connaissance contextuelle** : savoir dans quelles conditions une règle est valable ;
- **connaissance préférentielle** : savoir ce qu’un utilisateur privilégie ;
- **connaissance sociale** : savoir qui connaît quoi, qui décide et qui influence.

Une connaissance doit rester révisable. La stabilité n’est pas l’immuabilité.

## 1.5 La mémoire : la connaissance replacée dans une histoire

La mémoire conserve plus qu’un contenu. Elle conserve une continuité entre un événement passé et une situation présente.

Un souvenir cognitif contient généralement :

- ce qui s’est passé ;
- le contexte ;
- les acteurs ;
- l’état des connaissances à ce moment ;
- les émotions ou préférences pertinentes ;
- les décisions prises ;
- les conséquences observées ;
- les liens avec d’autres expériences.

La mémoire est donc temporelle, relationnelle et sélective.

Un système qui stocke tout sans hiérarchie ne possède pas une meilleure mémoire. Il possède une archive plus volumineuse. La mémoire exige des mécanismes de consolidation, d’oubli contrôlé, de rappel contextuel et de réinterprétation.

## 1.6 Le raisonnement : transformer la mémoire en hypothèse

Le raisonnement est l’activité par laquelle le système combine des connaissances, des objectifs et des contraintes afin de produire une conclusion, une hypothèse ou une action possible.

Il peut prendre plusieurs formes :

- déduction ;
- induction ;
- analogie ;
- abduction ;
- comparaison de scénarios ;
- raisonnement contrefactuel ;
- optimisation sous contraintes.

Dans MemoryOS, un raisonnement ne doit pas être enregistré uniquement par son résultat. Il doit conserver au minimum :

1. les prémisses utilisées ;
2. les objets cognitifs mobilisés ;
3. les hypothèses ;
4. les étapes majeures ;
5. le niveau de confiance ;
6. les alternatives rejetées ;
7. la date et le contexte.

Cette exigence permet ensuite de répondre à une question fondamentale :

> Pourquoi cette conclusion paraissait-elle raisonnable à ce moment-là ?

## 1.7 La décision : un raisonnement engagé

Une décision est un raisonnement qui modifie l’état du monde ou engage une intention.

Elle relie :

- une situation ;
- un objectif ;
- des alternatives ;
- des critères ;
- un choix ;
- un responsable ;
- une échéance ;
- des conséquences attendues.

Le Decision Engine doit distinguer une préférence exprimée, une recommandation, une intention et une décision effectivement engagée.

Cette distinction évite qu’une idée exploratoire soit ultérieurement interprétée comme un choix officiel.

## 1.8 L’apprentissage : une modification durable

Un système apprend lorsqu’une expérience modifie durablement sa manière de rappeler, de prédire, de raisonner ou d’agir.

L’accumulation de documents n’est donc pas un apprentissage. L’apprentissage suppose une transformation interne :

- révision d’une croyance ;
- création d’une règle ;
- ajustement d’un niveau de confiance ;
- détection d’un motif ;
- modification d’une préférence ;
- amélioration d’une stratégie.

Le Reflection Engine est responsable de cette transition entre expérience et apprentissage.

## 1.9 Une ontologie dynamique

Les catégories précédentes ne doivent pas devenir des silos techniques. Un même objet peut changer de statut.

Une observation brute devient une information. Plusieurs informations forment une connaissance. Une connaissance replacée dans une séquence d’événements devient une mémoire. Cette mémoire nourrit un raisonnement, lequel produit une décision. Les effets de la décision génèrent de nouvelles données.

Le système cognitif est donc une boucle :

```text
Observer → Interpréter → Relier → Se souvenir → Raisonner → Décider → Agir → Réévaluer
```

## 1.10 Conséquences architecturales

Cette théorie impose plusieurs propriétés au futur kernel :

- typage explicite des objets cognitifs ;
- provenance obligatoire pour les objets critiques ;
- versionnement des connaissances ;
- temporalité native ;
- relations entre preuves, hypothèses, décisions et résultats ;
- capacité à représenter l’incertitude ;
- séparation entre mémoire persistante et contexte de travail temporaire ;
- explicabilité des transitions.

MemoryOS ne doit donc pas être conçu comme une base de notes enrichie par un LLM. Il doit être conçu comme un système de transformation cognitive où chaque étape reste traçable.

## 1.11 Conclusion

La donnée représente. L’information contextualise. La connaissance stabilise. La mémoire inscrit dans le temps. Le raisonnement transforme. La décision engage. L’apprentissage modifie durablement.

Ces distinctions constituent le vocabulaire minimal d’un Cognitive Operating System. Sans elles, le système peut produire des réponses impressionnantes. Avec elles, il peut commencer à construire une histoire cohérente, révisable et explicable.