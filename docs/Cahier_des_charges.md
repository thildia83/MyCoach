# PROJECT MyCoach
## Cahier des charges fonctionnel (Version 1.0)

# Vision

Créer le meilleur coach audio intelligent pour la course à pied.

Le coach ne lit pas un entraînement.

Il accompagne un coureur.

Son objectif est de permettre au sportif de courir sans regarder sa montre tout en se sentant accompagné par un véritable entraîneur.

Le succès ne sera pas mesuré par la technologie mais par une seule question :

> "Est-ce que j'ai envie de repartir courir demain avec ce coach dans les oreilles ?"

---

# Origine du projet

Le projet est né d'un constat simple.

Les séances de TrainingPeaks sont excellentes.

Le guidage Garmin est insuffisant.

Le guidage de Runna est agréable mais limité aux séances créées dans Runna.

Le besoin est donc de conserver les plans d'entraînement de TrainingPeaks tout en bénéficiant d'un guidage audio largement supérieur.

---

# Objectifs

Le système doit permettre de :

- suivre une séance sans regarder la montre ;
- connaître à tout moment ce qui arrive ensuite ;
- connaître les objectifs précis de chaque intervalle ;
- être rassuré sur sa progression ;
- rester concentré sur la course.

---

# Public cible

Version initiale :

Coureurs utilisant :

- TrainingPeaks
- Garmin
- Coros
- Polar
- Suunto

Version future :

Tous les sportifs réalisant des séances structurées.

---

# Entrées

Le système doit accepter automatiquement :

- fichiers JSONV2 TrainingPeaks
- FIT
- ZWO
- FIT Workout (à terme)

Aucune séance ne doit être saisie manuellement.

---

# Sortie

Le système génère automatiquement :

- un briefing
- les annonces de séance
- les annonces de récupération
- les rappels utiles
- les comptes à rebours
- le fichier audio synchronisé

---

# Guidage audio

Le coach intervient uniquement lorsque cela apporte de la valeur.

Chaque annonce contient si nécessaire :

- où l'on se situe dans la séance ;
- ce qui arrive ensuite ;
- durée ;
- allure cible ;
- zone cardio ;
- puissance ;
- cadence ;
- objectif technique ;
- compte à rebours.

---

# Exemples

Dans dix secondes.

Premier bloc.

Quatre répétitions.

Première répétition.

Une minute trente à cinq minutes vingt au kilomètre.

Puis quarante-cinq secondes de récupération à huit minutes trente.

Les vingt premières secondes servent à trouver ton allure.

Trois.

Deux.

Un.

Go.

---

Récupération.

Quarante-cinq secondes.

Respire.

Relâche les épaules.

Prépare la suivante.

---

Dernière répétition.

Tu connais parfaitement cette allure.

Ne cherche pas à accélérer.

Cherche à être régulière.

Go.

---

# Philosophie du coach

Le coach parle peu.

Mais il parle juste.

Chaque intervention doit avoir une utilité.

Il ne remplit jamais les silences.

---

# Types d'interventions

Technique

Motivation

Gestion d'effort

Respiration

Hydratation

Nutrition

Sécurité

Informations de course

Rappel d'objectif

---

# Personnalités

Le coach est entièrement personnalisable.

Profils prévus :

Technique

Technique + motivant

Motivant

Exigeant

Minimaliste

Silencieux

Le coureur peut changer de personnalité avant ou pendant la séance.

---

# Coach adaptatif

Le coach adapte ses interventions :

à la difficulté de la séance ;

au moment de la séance ;

à la fatigue ;

au ressenti du coureur ;

aux données physiologiques.

---

# Interaction vocale

Version avancée.

Le coureur peut parler naturellement.

Exemples :

"J'en ai marre."

"Encore combien ?"

"Je suis dans le rythme ?"

"J'ai mal au dos."

"Booste-moi."

"Laisse-moi tranquille."

Le coach répond naturellement.

---

# Analyse temps réel

Connexion à la montre.

Lecture des données en direct.

Le coach analyse :

- allure ;
- fréquence cardiaque ;
- puissance ;
- cadence ;
- altitude ;
- température ;
- fatigue.

Puis adapte automatiquement ses annonces.

Exemple :

"Tu es huit secondes trop rapide."

"Ralentis légèrement."

ou

"Tu es parfaitement dans l'objectif."

---

# Fonctionnement

Le moteur doit :

1. Lire automatiquement le fichier TrainingPeaks.

2. Comprendre la structure complète de la séance.

3. Identifier :

- échauffement ;
- intervalles ;
- récupérations ;
- blocs ;
- retour au calme.

4. Calculer automatiquement tous les temps de déclenchement.

5. Générer automatiquement les annonces.

6. Générer les fichiers audio via ElevenLabs (ou équivalent).

7. Assembler automatiquement les annonces.

8. Ajouter automatiquement les silences.

9. Générer un unique MP3 synchronisé.

---

# Contraintes

Les annonces sont :

courtes ;

naturelles ;

humaines ;

jamais répétitives.

Durée maximale :

10 secondes.

Exception :

briefing.

---

# Architecture

Le système doit être totalement modulaire.

Lecture séance.

↓

Analyse.

↓

Scénarisation.

↓

Personnalisation.

↓

Synthèse vocale.

↓

Assemblage audio.

↓

Export.

Chaque module doit pouvoir évoluer indépendamment.

---

# Roadmap

## MVP

Lecture JSONV2.

↓

Scénarisation.

↓

Génération MP3.

↓

Test terrain.

Critère de réussite :

Je réalise une séance complète sans regarder ma montre.

---

## Version 2

Application mobile.

Lecture en temps réel.

Interruptions Spotify.

Notifications.

Historique.

---

## Version 3

Coach conversationnel.

Mémoire de la séance.

Personnalités.

Adaptation dynamique.

---

## Version 4

Connexion Garmin.

Analyse temps réel.

Corrections d'allure.

Analyse biomécanique.

Conseils personnalisés.

---

## Version 5

Coach IA complet.

Dialogue permanent.

Connaissance de l'historique sportif.

Préparation des objectifs.

Adaptation automatique des séances.

Analyse post-entraînement.

Débriefing personnalisé.

---

# Principes de développement

Le projet suit les règles suivantes.

Une idée validée devient un engagement.

Les nouvelles idées sont ajoutées au backlog.

Elles ne modifient jamais le sprint en cours.

Chaque sprint possède un objectif unique.

Un sprint n'est terminé que lorsqu'un livrable est réellement utilisable.

Le premier objectif n'est pas une application.

Le premier objectif est un MP3 permettant de courir une vraie séance.

---

# Critères de réussite

Le projet sera considéré comme réussi si :

- le coureur ne regarde presque plus sa montre ;
- il comprend parfaitement chaque exercice ;
- il respecte mieux les allures ;
- il ressent une présence utile sans être envahissante ;
- il termine la séance avec l'impression d'avoir couru avec un véritable entraîneur.

Le coach ne doit jamais donner l'impression de lire un script.

Il doit donner l'impression de connaître le coureur.
