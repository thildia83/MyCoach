"""
MyCoach - point d'entrée.

Usage :
    python main.py Samples/workout.jsonV2

Sprint 1 (en cours) : le scénario complet (texte + timing) est généré et
validé. La synthèse vocale (ElevenLabs) et l'assemblage MP3 ne sont pas
encore branchés - ils sont bloqués en attente de la clé API ElevenLabs et
du voice_id de la voix "Irène".

Tant que ce blocage n'est pas levé, cette commande affiche le script complet
de la séance à la place de générer le MP3, pour que le contenu et le timing
puissent être validés avant de dépenser des crédits ElevenLabs.
"""

import sys

sys.path.insert(0, "src")

from Parser import WorkoutParser
from Coach import Coach


def main():

    if len(sys.argv) < 2:
        print("Usage : python main.py <fichier.jsonV2>")
        sys.exit(1)

    filepath = sys.argv[1]

    parser = WorkoutParser(filepath)
    workout = parser.parse()

    coach = Coach(threshold_speed=workout["threshold_speed"])
    scenario = coach.build_scenario(workout)

    problems = [a for a in scenario if not a.fits()]

    print(f"Séance : {workout['title']}")
    print(f"{len(scenario)} annonces générées.")
    print()

    for a in scenario:
        marker = "" if a.fits() else "  <<< NE TIENT PAS DANS LE TEMPS DISPONIBLE"
        print(f"[{a.anchor_type:16s} t={a.anchor_time:5d}s]  {a.text}{marker}")

    print()

    if problems:
        print(f"⚠️  {len(problems)} annonce(s) ne tiennent pas dans le temps disponible.")
    else:
        print("✅ Toutes les annonces tiennent dans le temps disponible.")

    print()
    print("🚧 Génération audio (ElevenLabs) non encore branchée : clé API et")
    print("   voice_id 'Irène' en attente. output/workout.mp3 pas encore produit.")


if __name__ == "__main__":
    main()
