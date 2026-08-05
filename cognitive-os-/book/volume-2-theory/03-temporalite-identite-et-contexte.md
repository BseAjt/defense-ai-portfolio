# Chapitre 3 — Temporalité, identité et contexte

## 3.1 La cognition existe dans le temps

Une intelligence sans temporalité ne possède qu’un présent perpétuel. Elle peut traiter des contenus, mais elle ne peut pas distinguer ce qui était vrai, ce qui est devenu faux, ce qui a été décidé, ce qui reste envisagé et ce qui doit être réévalué.

La continuité cognitive exige donc une représentation native du temps.

MemoryOS ne considère pas le temps comme une simple métadonnée. Il le considère comme une dimension structurante de tout objet cognitif.

## 3.2 Plusieurs temps pour un même objet

Un objet cognitif peut posséder plusieurs temporalités :

- **temps de l’événement** : quand le fait s’est produit ;
- **temps de l’observation** : quand il a été perçu ou enregistré ;
- **temps d’enregistrement** : quand il est entré dans MemoryOS ;
- **temps de validité** : période pendant laquelle il est considéré comme vrai ;
- **temps de décision** : moment où il a influencé un choix ;
- **temps de révision** : moment où il a été corrigé ou réinterprété.

Confondre ces temporalités crée des erreurs importantes. Un document importé aujourd’hui peut décrire un état ancien. Une opinion exprimée hier peut ne plus représenter la préférence actuelle. Une décision prise en janvier peut rester valide jusqu’à ce qu’une condition précise change.

## 3.3 État présent et histoire des états

Les applications traditionnelles privilégient l’état courant. Lorsqu’une valeur change, l’ancienne est souvent remplacée.

Un Cognitive Operating System doit préserver l’histoire.

La préférence actuelle d’un utilisateur est utile. L’évolution de cette préférence peut l’être davantage. Elle révèle :

- les expériences qui ont modifié son jugement ;
- les compromis récurrents ;
- les contradictions apparentes ;
- les conditions dans lesquelles une préférence s’inverse.

MemoryOS doit donc utiliser un modèle bitemporel ou événementiel pour les objets dont l’histoire possède une valeur cognitive.

## 3.4 L’identité comme continuité, non comme fiche de profil

Une identité numérique est souvent réduite à un ensemble de champs : nom, fonction, langue, préférences.

L’identité cognitive est plus riche. Elle comprend :

- des rôles ;
- des objectifs ;
- des valeurs ;
- des relations ;
- des engagements ;
- des compétences ;
- des habitudes ;
- des récits personnels ;
- une manière de décider ;
- une histoire d’évolution.

L’Identity Engine ne doit pas figer l’utilisateur dans un profil. Il doit représenter une identité plurielle, contextuelle et révisable.

Une personne peut être dirigeant dans un projet, parent dans un autre contexte, expert technique dans une réunion et apprenant dans un domaine nouveau. Le système doit éviter de transférer automatiquement des attributs d’un rôle à un autre.

## 3.5 Identité déclarée, observée et inférée

MemoryOS distingue trois sources identitaires :

1. **déclarée** — ce que l’utilisateur affirme explicitement ;
2. **observée** — ce que ses actions répétées indiquent ;
3. **inférée** — ce que le système suppose à partir de motifs.

Ces trois niveaux ne possèdent pas la même autorité.

Une préférence déclarée doit généralement primer sur une inférence. Une observation contradictoire peut conduire le système à poser une question, mais pas à réécrire silencieusement l’identité.

Toute inférence identitaire significative doit être :

- traçable ;
- accompagnée d’un niveau de confiance ;
- révisable ;
- visible lorsque son usage influence une recommandation.

## 3.6 Le contexte comme sélection pertinente

Le contexte est l’ensemble minimal d’éléments nécessaires pour interpréter correctement une situation.

Il peut inclure :

- l’objectif actif ;
- le rôle de l’utilisateur ;
- le projet concerné ;
- les participants ;
- les contraintes ;
- les décisions antérieures ;
- les informations récentes ;
- les règles applicables ;
- le niveau de confidentialité.

Le contexte n’est pas équivalent à l’historique complet. Trop peu de contexte produit des réponses superficielles. Trop de contexte dilue les signaux importants et augmente le coût de traitement.

La construction du contexte est donc une fonction cognitive centrale.

## 3.7 Les frontières de contexte

Un système de mémoire doit empêcher les fuites entre espaces qui ne devraient pas se mélanger.

Exemples :

- une information professionnelle confidentielle ne doit pas apparaître dans une conversation personnelle ;
- une préférence propre à un projet ne doit pas devenir une préférence globale ;
- une hypothèse exploratoire ne doit pas être présentée comme un fait établi ;
- le souvenir d’un agent ne doit pas être automatiquement accessible à tous les autres.

Les frontières de contexte reposent sur :

- l’ownership ;
- les permissions ;
- la finalité ;
- le rôle ;
- la sensibilité ;
- le consentement ;
- la portée temporelle.

## 3.8 Contexte explicite et contexte implicite

Une partie du contexte est fournie directement : « analyse ce projet comme un investissement personnel ».

Une autre partie est implicite : langue habituelle, calendrier, décisions passées, contraintes budgétaires ou expertise du demandeur.

MemoryOS doit utiliser le contexte implicite avec prudence. Il doit éviter deux erreurs opposées :

- ignorer l’histoire et obliger l’utilisateur à tout répéter ;
- surinterpréter l’histoire et enfermer l’utilisateur dans ses choix passés.

Le système doit permettre des commandes telles que :

- « réponds sans utiliser ma mémoire personnelle » ;
- « limite-toi au projet X » ;
- « considère que mes préférences ont changé » ;
- « montre-moi les souvenirs utilisés ».

## 3.9 Les événements de changement de contexte

Certains événements doivent déclencher une réévaluation :

- changement de poste ;
- nouvelle réglementation ;
- modification d’un objectif ;
- dépassement d’un budget ;
- arrivée d’un nouvel acteur ;
- résultat inattendu ;
- expiration d’une hypothèse.

Le Decision Engine peut alors identifier les décisions dépendantes de l’ancien contexte et proposer leur réexamen.

Cette capacité transforme la mémoire en système actif. Elle ne se contente plus de rappeler le passé ; elle détecte quand le passé doit être relu.

## 3.10 La Reasoning Timeline

La Reasoning Timeline représente l’évolution d’une pensée dans le temps.

Elle relie :

```text
Question → Hypothèses → Informations → Raisonnements → Décision → Action → Résultat → Réflexion
```

Chaque étape peut être versionnée et comparée.

La timeline permet notamment de répondre :

- Quand notre position a-t-elle changé ?
- Quel nouvel élément a provoqué ce changement ?
- Quelles hypothèses étaient actives lors de la décision ?
- Avons-nous déjà rencontré une situation comparable ?
- Pourquoi deux décisions apparemment contradictoires étaient-elles cohérentes dans leurs contextes respectifs ?

## 3.11 Identité et droit à l’évolution

Une mémoire permanente peut devenir oppressive si elle fige les individus dans leur passé.

Le droit à la continuité doit être accompagné d’un droit à l’évolution.

MemoryOS doit donc permettre :

- la correction ;
- la contextualisation d’un comportement ancien ;
- l’expiration de certaines préférences ;
- la séparation entre identité actuelle et historique ;
- la suppression lorsque la loi ou l’utilisateur l’exige.

Se souvenir ne signifie pas condamner une personne à rester identique.

## 3.12 Conséquences pour l’architecture

La temporalité, l’identité et le contexte imposent au kernel :

- des objets versionnés ;
- des intervalles de validité ;
- des journaux d’événements ;
- des portées de contexte explicites ;
- une gestion fine des permissions ;
- des identités multi-rôles ;
- une séparation entre attribut déclaré, observé et inféré ;
- une capacité de reconstruction historique ;
- des déclencheurs de réévaluation.

## 3.13 Conclusion

La mémoire donne une histoire. Le temps ordonne cette histoire. L’identité lui donne un sujet. Le contexte détermine son sens.

Un Cognitive Operating System doit maintenir ces quatre dimensions ensemble. Sans temps, il ne sait pas ce qui a changé. Sans identité, il ne sait pas à qui appartient la continuité. Sans contexte, il ne sait pas ce qui est pertinent. Sans mémoire, il ne peut relier le présent au passé.

MemoryOS doit donc être conçu comme une infrastructure temporelle et identitaire autant que comme une infrastructure de connaissances.