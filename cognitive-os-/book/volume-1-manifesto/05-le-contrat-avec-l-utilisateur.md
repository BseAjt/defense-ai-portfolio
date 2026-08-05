# Chapitre 5 — Le contrat avec l’utilisateur

## 5.1 La mémoire comme relation de confiance

Un Cognitive Operating System n’est pas un outil ordinaire.

Il peut connaître les décisions, les relations, les doutes, les objectifs, les erreurs et les apprentissages d’une personne ou d’une organisation. Sa valeur dépend donc directement de la confiance qu’il inspire.

Cette confiance ne peut pas reposer uniquement sur une promesse commerciale. Elle doit être formalisée comme un contrat entre le système et son utilisateur.

## 5.2 Droit de propriété

L’utilisateur reste propriétaire de sa mémoire cognitive.

Cette propriété inclut les contenus bruts, les objets cognitifs dérivés, les relations construites, les profils, les préférences, les historiques de décision et les représentations générées à partir de ces éléments.

Le fournisseur de l’infrastructure ne doit pas confondre hébergement, traitement et propriété.

## 5.3 Droit d’accès

L’utilisateur doit pouvoir consulter ce que le système sait de lui.

Cet accès ne doit pas se limiter à une liste de fichiers. Il doit permettre d’examiner :

- les souvenirs conservés ;
- les relations créées ;
- les inférences produites ;
- les niveaux de confiance ;
- les sources utilisées ;
- les règles de rétention ;
- les actions déclenchées.

Une mémoire invisible devient rapidement incontrôlable.

## 5.4 Droit de correction

La mémoire peut se tromper.

Elle peut attribuer une intention erronée, relier deux objets à tort, conserver une information devenue fausse ou transformer une hypothèse en certitude.

L’utilisateur doit pouvoir corriger, annoter ou contester chaque objet et chaque relation. Le système doit préserver l’historique de la correction sans maintenir l’erreur comme vérité active.

## 5.5 Droit à l’oubli

La continuité cognitive ne signifie pas conservation illimitée.

L’utilisateur doit pouvoir supprimer un objet, un ensemble d’objets, une période, une source ou l’intégralité de sa mémoire.

Cette suppression doit être compréhensible, vérifiable et propagée aux index, représentations dérivées et sauvegardes selon des règles annoncées.

Le droit de se souvenir implique le droit de choisir ce qui doit disparaître.

## 5.6 Droit à la portabilité

Une mémoire cognitive ne doit pas devenir un mécanisme d’enfermement.

L’utilisateur doit pouvoir exporter son patrimoine dans un format documenté, lisible et exploitable par d’autres systèmes.

La portabilité doit inclure les contenus, les métadonnées, les relations, les versions, les sources, les permissions et les niveaux de confiance.

Exporter uniquement le texte détruirait une partie essentielle de la cognition représentée.

## 5.7 Droit à l’explication

Lorsqu’une recommandation ou une action s’appuie sur la mémoire, l’utilisateur doit pouvoir demander :

- quels éléments ont influencé le résultat ;
- pourquoi ils ont été jugés pertinents ;
- quelles hypothèses ont été ajoutées ;
- quelles alternatives ont été écartées ;
- quel niveau d’incertitude demeure.

L’explication doit être adaptée à l’enjeu. Une suggestion anodine et une décision critique n’exigent pas le même niveau de justification.

## 5.8 Droit au consentement granulaire

L’accès à une mémoire cognitive ne peut pas être gouverné par un consentement unique et permanent.

L’utilisateur doit pouvoir définir qui ou quoi peut accéder à chaque catégorie d’objet, pour quelle finalité, pendant quelle durée et avec quel niveau d’action.

Un agent autorisé à lire un calendrier ne doit pas automatiquement accéder à des réflexions personnelles. Une application autorisée à proposer une tâche ne doit pas nécessairement pouvoir l’exécuter.

## 5.9 Droit à la séparation des contextes

Une même personne peut posséder plusieurs rôles : professionnel, familial, créatif, médical, associatif ou privé.

Le système doit permettre de séparer ces contextes et de contrôler leurs intersections.

La continuité ne doit pas devenir une fusion indiscriminée de toutes les facettes d’une identité.

## 5.10 Droit à la réversibilité

Toute action automatisée devrait être réversible lorsque cela est techniquement possible.

Le système doit conserver une trace des actions, de leur origine et de leur justification. Pour les opérations sensibles, il doit prévoir des mécanismes d’annulation, de validation ou de restauration.

L’autonomie sans réversibilité augmente le risque de manière disproportionnée.

## 5.11 Devoir de minimisation

Le système ne doit pas capturer tout ce qu’il peut capturer.

Il doit collecter ce qui est nécessaire à la finalité annoncée, appliquer des règles de durée et permettre des niveaux de granularité différents.

La meilleure mémoire n’est pas la plus volumineuse. C’est celle qui conserve suffisamment pour être utile sans devenir envahissante.

## 5.12 Devoir de loyauté

Le système doit agir dans l’intérêt déclaré de l’utilisateur.

Il ne doit pas exploiter ses vulnérabilités, dissimuler des usages secondaires ou manipuler ses décisions au bénéfice d’un tiers non déclaré.

Un Cognitive Operating System ne peut devenir un intermédiaire publicitaire caché entre une personne et sa propre histoire.

## 5.13 Devoir de sécurité

Le fournisseur doit protéger la confidentialité, l’intégrité et la disponibilité de la mémoire.

Il doit limiter les accès, chiffrer les données sensibles, journaliser les opérations, gérer les incidents et informer clairement l’utilisateur lorsqu’un risque significatif apparaît.

La sécurité n’est pas seulement une obligation technique. Elle est une condition de légitimité.

## 5.14 Devoir d’incertitude

Le système doit reconnaître ce qu’il ne sait pas.

Il doit éviter de présenter une inférence comme un souvenir certain, une corrélation comme une cause ou une recommandation comme une obligation.

La capacité à exprimer le doute est une forme essentielle d’honnêteté cognitive.

## 5.15 Le contrat fondateur

Le contrat entre MemoryOS et son utilisateur peut être résumé ainsi :

> Nous préserverons votre continuité sans confisquer votre histoire.

Le système promet de se souvenir, mais aussi d’expliquer. Il promet d’aider, mais pas de dissimuler. Il promet de relier, mais pas de mélanger sans consentement. Il promet d’agir, mais sous des règles contrôlables.

Ce contrat clôt le manifeste et prépare les volumes suivants, qui définiront la théorie, l’architecture et l’implémentation nécessaires pour le rendre réel.
