# Chapitre 2 — Pourquoi les systèmes actuels oublient

## 2.1 L’oubli n’est pas un accident

Les systèmes numériques contemporains n’oublient pas parce qu’ils seraient mal conçus. Ils oublient parce qu’ils ont été conçus pour autre chose.

La messagerie transmet. Le calendrier ordonne le temps. Le traitement de texte produit des documents. La base de données conserve des enregistrements. Le moteur de recherche retrouve des contenus. Le modèle de langage génère une réponse à partir d’un contexte donné.

Aucun de ces outils n’a reçu pour mission principale de préserver une continuité cognitive.

Ce que nous appelons oubli est donc souvent la conséquence logique d’une architecture orientée fichier, message ou transaction, mais rarement orientée histoire, intention ou apprentissage.

## 2.2 Une fenêtre de contexte n’est pas une mémoire

Une fenêtre de contexte regroupe les éléments disponibles au moment d’un calcul. Elle permet au modèle de produire une réponse cohérente avec ce qui lui est fourni. Mais lorsque cette fenêtre disparaît, l’histoire peut disparaître avec elle.

La mémoire exige davantage :

- une persistance indépendante de la session ;
- une sélection de ce qui mérite d’être conservé ;
- une organisation selon le sens, le temps et les relations ;
- une capacité à mettre à jour ce qui a changé ;
- une capacité à expliquer l’origine d’un souvenir ;
- une distinction entre fait, hypothèse et opinion.

Une fenêtre de contexte est un espace de travail. Une mémoire est une structure de continuité.

## 2.3 Les fichiers conservent le contenu, pas l’intention

Le fichier permet de conserver et déplacer une unité de contenu. Mais il ne sait pas pourquoi il existe.

Il ne connaît pas nécessairement le problème auquel il répond, les alternatives rejetées, la décision qui en découle, les hypothèses qu’il contient ou les conditions qui pourraient le rendre obsolète.

Le fichier conserve une forme finale. La cognition a besoin de préserver le chemin.

## 2.4 Les applications fragmentent l’histoire

Une même décision peut être dispersée entre une invitation de calendrier, plusieurs messages, un document, un enregistrement de réunion, une tâche et une conversation avec une IA.

Pour l’utilisateur, il s’agit d’un seul épisode cognitif. Pour les systèmes, il s’agit de plusieurs objets sans relation native.

L’oubli naît souvent de cette absence de liaison.

## 2.5 Les connaissances vieillissent silencieusement

Une information exacte au moment de sa création peut devenir fausse plusieurs mois plus tard. Pourtant, beaucoup de systèmes conservent le contenu sans conserver ses conditions de validité.

Une connaissance durable devrait indiquer sa date d’observation, sa source, son niveau de confiance, son domaine de validité, ses hypothèses et les événements susceptibles de l’invalider.

Sans ces propriétés, l’accumulation augmente le volume mais pas nécessairement la qualité de la mémoire.

## 2.6 Le RAG retrouve, mais ne se souvient pas nécessairement

Le Retrieval-Augmented Generation améliore l’accès aux contenus. Il permet de retrouver des passages pertinents puis de les fournir à un modèle génératif.

Cette capacité est utile, mais elle ne constitue pas à elle seule une mémoire cognitive.

Le RAG demande principalement quels contenus ressemblent à la requête actuelle. Une mémoire doit aussi savoir ce que nous pensions auparavant, pourquoi une décision avait été prise, ce qui a changé, quelles contradictions apparaissent et quelle version d’une connaissance était valide à une date donnée.

La récupération est une fonction de la mémoire. Elle n’en est pas la totalité.

## 2.7 La dépendance aux fournisseurs

Lorsque la mémoire est intégrée directement à une application, changer d’assistant peut signifier perdre les préférences apprises, les projets suivis, les relations entre sujets et les décisions passées.

Un Cognitive Operating System doit séparer la mémoire, les moteurs de raisonnement et les applications d’interaction.

Les modèles deviennent remplaçables. L’histoire demeure.

## 2.8 L’oubli organisationnel

Les organisations oublient lorsqu’une personne part, lorsqu’un outil change ou lorsqu’une décision n’est documentée que par son résultat.

Les procédures décrivent ce qui doit être fait, mais rarement pourquoi elles ont été créées. Les comptes rendus enregistrent les conclusions, mais rarement les hypothèses et les signaux faibles qui les ont façonnées.

Une organisation peut donc posséder de nombreuses archives tout en conservant une faible capacité d’apprentissage.

Elle sait ce qu’elle a produit. Elle ne sait plus toujours ce qu’elle a compris.

## 2.9 Concevoir contre l’oubli

Préserver la continuité impose de capturer les événements cognitifs, relier les objets issus de plusieurs applications, versionner la connaissance, préserver les alternatives, rendre la provenance vérifiable et déclencher une réévaluation lorsque le contexte change.

Un système n’acquiert pas une mémoire simplement parce qu’il stocke davantage.

Il acquiert une mémoire lorsqu’il est conçu pour préserver la continuité du sens.
