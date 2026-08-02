"""
Assemble tous les clips générés + du silence calculé en un unique MP3,
en respectant les ancrages temporels (fin_exacte / debut_immediate) définis
dans docs/Consignes._Anticipation_.

Règle : si une annonce est trop longue pour la place disponible avant elle,
on décale la suite plutôt que de couper l'audio (jamais de mot coupé).
Décision produit actée : dans ce cas, le MP3 final peut dépasser légèrement
la durée TrainingPeaks - c'est voulu, pas un bug.

⚠️ NON TESTÉ DE BOUT EN BOUT : dépend de tts.py, lui-même bloqué réseau
côté sandbox Claude. À exécuter en local (voir INSTALLATION.md).
"""

import subprocess
from pathlib import Path


def build_events(announcements, durations):
    """
    Calcule, pour chaque annonce, l'intervalle [start, end] qu'elle occupe
    dans le fichier final, avant tout décalage éventuel.
    """

    events = []

    for ann, dur in zip(announcements, durations):

        if ann.anchor_type == "fin_exacte":
            start = ann.anchor_time - dur
            end = ann.anchor_time
        else:  # debut_immediate
            start = ann.anchor_time
            end = ann.anchor_time + dur

        events.append({
            "announcement": ann,
            "duration": dur,
            "start": start,
            "end": end,
        })

    # Important : on trie par anchor_time (l'ordre chronologique réel des
    # étapes de la séance), PAS par "start" calculé. Le "start" recule
    # artificiellement pour une annonce longue en fin_exacte (start = anchor
    # - durée), ce qui inverserait l'ordre par rapport à une annonce
    # debut_immediate courte qui la précède réellement dans la séance.
    events.sort(key=lambda e: (e["announcement"].anchor_time, e["announcement"].anchor_type != "debut_immediate"))

    return events


def resolve_timeline(events):
    """
    Parcourt les événements triés par ordre naturel et calcule leur position
    finale réelle, en décalant (jamais en coupant) en cas de chevauchement.

    Modifie chaque event en place (ajoute actual_start / actual_end) et
    retourne le décalage total accumulé (0 si tout tenait dans le temps
    prévu par TrainingPeaks).
    """

    cursor = 0.0
    total_shift = 0.0

    for e in events:

        desired_start = e["start"] + total_shift

        if desired_start < cursor:
            shift_added = cursor - desired_start
            total_shift += shift_added
            desired_start = cursor

        e["actual_start"] = desired_start
        e["actual_end"] = desired_start + e["duration"]

        cursor = e["actual_end"]

    return events, total_shift


def assemble(events, output_path, workdir):
    """
    Construit le MP3 final : silence calculé + clip, silence + clip, ...
    Chaque event doit déjà porter "clip_path" (chemin du fichier audio
    généré par ElevenLabs pour cette annonce).

    Retourne la durée totale réelle du fichier généré (secondes).
    """

    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)

    concat_list_path = workdir / "concat_list.txt"

    parts = []
    cursor = 0.0

    for i, e in enumerate(events):

        silence_duration = e["actual_start"] - cursor

        if silence_duration > 0.01:
            silence_path = workdir / f"silence_{i}.mp3"
            _generate_silence(silence_path, silence_duration)
            parts.append(silence_path)

        parts.append(Path(e["clip_path"]))
        cursor = e["actual_end"]

    with open(concat_list_path, "w") as f:
        for p in parts:
            f.write(f"file '{p.resolve()}'\n")

    subprocess.run(
        [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_list_path),
            "-c", "copy",
            str(output_path),
        ],
        check=True, capture_output=True,
    )

    return cursor


def _generate_silence(output_path, duration_seconds):

    subprocess.run(
        [
            "ffmpeg", "-y", "-f", "lavfi",
            "-i", "anullsrc=r=44100:cl=mono",
            "-t", str(duration_seconds),
            "-q:a", "9",
            str(output_path),
        ],
        check=True, capture_output=True,
    )
