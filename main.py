"""
MyCoach - point d'entrée.

Usage :
    python main.py Samples/workout.jsonV2

Variables d'environnement nécessaires pour générer le vrai MP3 :
    ELEVENLABS_API_KEY   - ta clé API ElevenLabs
    ELEVENLABS_VOICE_ID  - le voice_id de la voix "Irène"

Sans ces variables, la commande affiche seulement le script complet de la
séance (mode aperçu), pour valider le contenu et le timing sans dépenser de
crédits ElevenLabs.
"""

import os
import sys

sys.path.insert(0, "src")

from Parser import WorkoutParser
from Coach import Coach
from tts import ElevenLabsClient, get_audio_duration
from assembler import build_events, resolve_timeline, assemble


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

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    voice_id = os.environ.get("ELEVENLABS_VOICE_ID")

    if not api_key or not voice_id:
        print("🚧 ELEVENLABS_API_KEY / ELEVENLABS_VOICE_ID non définis.")
        print("   Mode aperçu uniquement : output/workout.mp3 pas généré.")
        return

    generate_mp3(scenario, filepath, api_key, voice_id)


def generate_mp3(scenario, source_filepath, api_key, voice_id):

    client = ElevenLabsClient(api_key=api_key, voice_id=voice_id)

    workdir = "output/tmp_clips"
    os.makedirs(workdir, exist_ok=True)

    print(f"Génération de {len(scenario)} clips audio via ElevenLabs...")

    durations = []

    for i, announcement in enumerate(scenario):

        clip_path = os.path.join(workdir, f"clip_{i:03d}.mp3")

        client.generate(announcement.text, clip_path)

        duration = get_audio_duration(clip_path)
        durations.append(duration)

        announcement_events_clip_path = clip_path  # noqa: référencé plus bas

        print(f"  [{i+1}/{len(scenario)}] {duration:.2f}s  {announcement.text[:50]}")

        # On attache le chemin du clip pour l'étape d'assemblage
        announcement.clip_path = clip_path

    events = build_events(scenario, durations)

    for e in events:
        e["clip_path"] = e["announcement"].clip_path

    events, total_shift = resolve_timeline(events)

    os.makedirs("output", exist_ok=True)
    output_path = "output/workout.mp3"

    final_duration = assemble(events, output_path, workdir)

    print()
    print(f"✅ MP3 généré : {output_path}")
    print(f"   Durée totale : {final_duration:.1f}s ({final_duration/60:.1f} min)")

    if total_shift > 0.5:
        print(f"   ⚠️  Décalage de {total_shift:.1f}s par rapport à la durée TrainingPeaks")
        print("      (une ou plusieurs annonces avaient besoin de plus de place).")


if __name__ == "__main__":
    main()
