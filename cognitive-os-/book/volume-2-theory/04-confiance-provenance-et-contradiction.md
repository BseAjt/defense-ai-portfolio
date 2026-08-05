# Chapitre 4 — Confiance, provenance et contradiction

## 4.1 Pourquoi la mémoire ne peut pas tout croire

Une mémoire cognitive ne doit jamais traiter toutes les informations comme équivalentes.

Un souvenir personnel, une donnée mesurée, une hypothèse, une rumeur, une décision officielle et une synthèse produite par un modèle de langage n'ont ni le même statut ni la même fiabilité. Pourtant, de nombreux systèmes numériques les stockent sous une forme homogène, comme si la présence d'une information suffisait à lui donner de la valeur.

Un Cognitive Operating System doit au contraire représenter explicitement l'incertitude. Il ne doit pas seulement mémoriser ce qui a été affirmé, mais aussi qui l'a affirmé, à quel moment, dans quel contexte, avec quelles preuves et avec quel niveau de confiance.

La confiance n'est pas un attribut décoratif. Elle conditionne la capacité du système à raisonner correctement.

## 4.2 La provenance comme propriété native

La provenance décrit l'origine d'un objet cognitif.

Elle répond notamment aux questions suivantes :

- Qui a produit cette information ?
- À partir de quelle source ?
- À quel moment ?
- Dans quel contexte ?
- Par quel processus de transformation ?
- Quelles étapes intermédiaires ont conduit à cet objet ?

Dans MemoryOS, la provenance doit être conservée dès la capture. Elle ne doit pas être reconstruite après coup.

Un objet cognitif sans provenance peut encore être utile, mais il doit être considéré comme moins fiable. À l'inverse, une provenance riche permet d'auditer, de comparer et de réévaluer une connaissance lorsque le contexte change.

## 4.3 Les dimensions de la confiance

La confiance ne se réduit pas à une note unique. Elle peut être décomposée en plusieurs dimensions.

### Fiabilité de la source

La source a-t-elle déjà produit des informations exactes ? Possède-t-elle une compétence reconnue sur le sujet ? Est-elle indépendante ou intéressée ?

### Qualité de la preuve

L'affirmation repose-t-elle sur une observation directe, une donnée mesurée, un document officiel, une interprétation ou une intuition ?

### Récence

L'information est-elle encore actuelle ? Une connaissance exacte il y a deux ans peut être devenue obsolète.

### Cohérence

L'information est-elle compatible avec d'autres objets cognitifs fiables ?

### Réplication

Plusieurs sources indépendantes arrivent-elles à la même conclusion ?

### Stabilité contextuelle

La validité de l'information dépend-elle fortement d'un contexte particulier ?

Une architecture robuste doit préserver ces dimensions séparément avant, éventuellement, de les agréger dans un score synthétique.

## 4.4 Le score de confiance

Un score de confiance peut être utile pour comparer des objets, mais il ne doit jamais masquer les raisons qui le composent.

Un score purement numérique crée une illusion de précision. Deux objets notés à 0,78 peuvent avoir des profils très différents : l'un peut reposer sur une excellente source mais être ancien ; l'autre peut être récent mais mal documenté.

MemoryOS doit donc associer à chaque score :

- ses composantes ;
- la méthode de calcul ;
- la date de calcul ;
- les éléments ayant augmenté ou diminué la confiance ;
- les conditions susceptibles de modifier le résultat.

Le système doit pouvoir répondre non seulement à « quel est le niveau de confiance ? », mais aussi à « pourquoi ? ».

## 4.5 La contradiction comme signal

Une contradiction n'est pas nécessairement une erreur.

Deux objets cognitifs peuvent s'opposer parce qu'ils concernent des périodes différentes, des contextes distincts, des populations différentes ou des définitions incompatibles.

Par exemple :

- « Le projet est prioritaire » peut être vrai en janvier et faux en juin.
- « Le produit est rentable » peut être vrai pour un segment et faux pour un autre.
- « Cette stratégie fonctionne » peut dépendre d'une contrainte réglementaire aujourd'hui disparue.

Le système ne doit donc pas supprimer automatiquement l'une des versions. Il doit représenter la contradiction, ses conditions et son évolution.

## 4.6 Typologie des contradictions

Un Cognitive Operating System doit distinguer plusieurs formes de contradiction.

### Contradiction logique

Deux affirmations ne peuvent pas être vraies simultanément dans le même contexte.

### Contradiction temporelle

Deux affirmations sont vraies à des moments différents.

### Contradiction contextuelle

Deux affirmations diffèrent parce que les conditions ne sont pas les mêmes.

### Contradiction de source

Deux sources décrivent différemment le même phénomène.

### Contradiction d'interprétation

Les faits sont similaires, mais les conclusions diffèrent.

### Contradiction d'objectif

Deux décisions paraissent incompatibles parce qu'elles optimisent des objectifs différents.

Cette typologie permet d'éviter les résolutions simplistes.

## 4.7 Résoudre sans effacer

La résolution d'une contradiction ne doit pas conduire à l'effacement de l'historique.

MemoryOS doit conserver :

- les versions en conflit ;
- les sources ;
- le contexte de chaque affirmation ;
- la décision de résolution ;
- la justification ;
- le niveau de confiance avant et après résolution.

La résolution peut produire plusieurs résultats :

- une version est invalidée ;
- les deux versions sont maintenues avec des contextes distincts ;
- la contradiction reste ouverte ;
- une nouvelle hypothèse explique les deux positions ;
- une décision humaine est requise.

Le système doit rendre visible le fait qu'une connaissance a été contestée.

## 4.8 Le vieillissement des connaissances

La confiance doit évoluer dans le temps.

Certaines connaissances sont stables, comme une définition mathématique. D'autres vieillissent rapidement, comme un tarif, une réglementation, une responsabilité organisationnelle ou une préférence personnelle.

Chaque objet cognitif devrait posséder une politique de vieillissement adaptée à sa nature.

Cette politique peut inclure :

- une date d'expiration ;
- une fréquence de réévaluation ;
- des événements déclencheurs ;
- une baisse progressive de confiance ;
- une obligation de confirmation externe.

Une connaissance ancienne ne devient pas nécessairement fausse. Elle devient simplement moins sûre dans le présent.

## 4.9 Confiance locale et confiance transférée

La confiance peut être locale à un utilisateur, une équipe ou une organisation.

Une personne peut considérer une source comme fiable en raison d'une expérience passée que d'autres ne partagent pas. Une organisation peut appliquer ses propres règles de validation. Une communauté scientifique peut exiger une réplication indépendante.

MemoryOS doit donc éviter l'idée d'une confiance universelle unique.

Il doit permettre :

- des politiques de confiance personnalisées ;
- des profils de validation différents ;
- des seuils adaptés au risque ;
- une séparation entre confiance personnelle et confiance collective.

La confiance est toujours liée à un acteur, un objectif et un niveau de risque.

## 4.10 Le rôle de l'explicabilité

Un système qui recommande une action à partir d'une mémoire doit pouvoir expliquer les objets sur lesquels il s'est appuyé.

Cette explicabilité doit inclure :

- les sources mobilisées ;
- les objets écartés ;
- les contradictions détectées ;
- les hypothèses retenues ;
- le niveau d'incertitude ;
- les conditions qui pourraient modifier la recommandation.

L'explicabilité n'est pas un supplément d'interface. Elle constitue une condition de confiance dans le système.

## 4.11 Principes d'architecture

La gestion de la confiance, de la provenance et des contradictions doit respecter plusieurs principes.

1. Toute affirmation importante doit conserver sa source.
2. Toute transformation doit être traçable.
3. Toute confiance doit être justifiable.
4. Toute contradiction doit être représentée avant d'être résolue.
5. Toute résolution doit préserver l'historique.
6. Toute connaissance doit pouvoir être réévaluée.
7. Toute recommandation doit exposer son incertitude.

## 4.12 Conclusion

Une mémoire utile ne se contente pas de conserver ce qui a été dit. Elle sait distinguer ce qui est établi, probable, contesté, ancien ou contextuel.

La confiance donne un poids aux connaissances. La provenance permet de les auditer. La contradiction empêche le système de transformer une collection d'affirmations en vérité artificielle.

MemoryOS doit donc être conçu comme une mémoire critique, capable de douter, de comparer et de réviser.

Sans cette capacité, il ne serait qu'un entrepôt d'informations. Avec elle, il peut devenir un véritable système de continuité cognitive.
