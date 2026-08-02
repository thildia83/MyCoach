"""
Génère le scénario complet de la séance : une liste d'annonces avec leur
ancrage temporel, prêtes pour la synthèse vocale.

Deux types d'ancrage (voir docs/Consignes_Anticipation.md) :

- "fin_exacte"      : l'annonce doit se terminer PILE à ce temps (avant un
                      effort). Le "Go" tombe exactement au bon moment.
- "debut_immediate" : l'annonce démarre à ce temps, pas de contrainte de
                      précision sur sa fin (récupération, briefing).

Chaque annonce porte aussi le temps disponible avant elle (available_seconds)
pour qu'on puisse vérifier, avant même de générer l'audio, qu'un texte n'est
pas trop long pour la place qu'il a.
"""

from dataclasses import dataclass
from typing import Optional

from Pace import target_pace_text
from Timeline import build_timeline

# Vitesse de parole estimée (mots / seconde), countdown inclus.
# Volontairement prudente : mieux vaut sous-estimer la place disponible
# que de produire un "Go" en retard.
WORDS_PER_SECOND = 2.5

COUNTDOWN_WORDS = ["Trois.", "Deux.", "Un.", "Go."]


@dataclass
class Announcement:

    anchor_type: str  # "fin_exacte" ou "debut_immediate"
    anchor_time: int
    text: str
    available_seconds: Optional[float] = None

    def estimated_speech_seconds(self):
        word_count = len(self.text.split())
        return word_count / WORDS_PER_SECOND

    def fits(self):
        if self.available_seconds is None:
            return True
        return self.estimated_speech_seconds() <= self.available_seconds


class Coach:

    def __init__(self, threshold_speed):
        self.threshold_speed = threshold_speed

    def build_scenario(self, workout):
        """Construit la liste ordonnée des annonces pour toute la séance."""

        timeline = build_timeline(workout["steps"])

        announcements = []

        # Briefing initial (exception à la règle des 10 secondes)
        announcements.append(
            Announcement(
                anchor_type="debut_immediate",
                anchor_time=0,
                text=self._briefing(workout),
            )
        )

        for index, step in enumerate(timeline):

            previous_step = timeline[index - 1] if index > 0 else None

            if step.intensity_class == "Active":

                text = self._effort_text(step)

                # Cas particulier : aucun step avant le premier effort
                # (ex. une "sortie longue" qui démarre direct en effort).
                # Décision produit : le countdown est lancé en tout début
                # de fichier. Le MP3 dépassera alors légèrement la durée
                # TrainingPeaks (de la durée de ce countdown), au lieu de
                # supprimer le "3. 2. 1. Go." pour cet effort.
                available = previous_step.duration if previous_step else None

                announcements.append(
                    Announcement(
                        anchor_type="fin_exacte",
                        anchor_time=step.start,
                        text=text,
                        available_seconds=available,
                    )
                )

            else:
                # Warm up (hors tout premier step, déjà couvert par le
                # briefing), récupération, repos, retour au calme.
                if index == 0:
                    continue

                text = self._rest_text(step)

                announcements.append(
                    Announcement(
                        anchor_type="debut_immediate",
                        anchor_time=step.start,
                        text=text,
                    )
                )

        return announcements

    # ------------------------------------------------------------------
    # Construction des textes
    # ------------------------------------------------------------------

    def _briefing(self, workout):
        return f"Aujourd'hui : {workout['title']}. C'est parti."

    def _effort_text(self, step):

        parts = []

        if step.is_first_in_repeat_block and step.repeat_total and step.repeat_total > 1:
            if step.repeat_index == 1:
                parts.append(f"Bloc de {step.repeat_total} répétitions.")
            parts.append(f"Répétition {step.repeat_index} sur {step.repeat_total}.")

        duration_text = self._duration(step.duration)
        pace = target_pace_text(step.target, self.threshold_speed)

        if pace:
            parts.append(f"{duration_text} à {pace}.")
        else:
            parts.append(f"{duration_text}.")

        parts.extend(COUNTDOWN_WORDS)

        return " ".join(parts)

    def _rest_text(self, step):

        duration_text = self._duration(step.duration)
        pace = target_pace_text(step.target, self.threshold_speed)

        label = "Récupération" if step.intensity_class == "Rest" else step.name

        if pace:
            return f"{label}. {duration_text} à {pace}."

        return f"{label}. {duration_text}."

    def _duration(self, seconds):

        minutes = seconds // 60
        sec = seconds % 60

        if minutes and sec:
            return f"{minutes} minutes {sec} secondes"

        if minutes:
            return f"{minutes} minutes"

        return f"{sec} secondes"
