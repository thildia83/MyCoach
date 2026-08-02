"""
Client ElevenLabs : convertit un texte en audio (mp3) et mesure la durée
réelle du fichier généré (via ffprobe) - c'est cette mesure réelle qui
permet le système d'ancrage précis (voir docs/Consignes._Anticipation_).

⚠️ NON TESTÉ DE BOUT EN BOUT PAR CLAUDE : le bac à sable n'a pas accès
réseau à api.elevenlabs.io. Ce module doit être exécuté en local. En cas
d'erreur, renvoie le message complet pour qu'on la corrige ensemble.
"""

import os
import subprocess

import requests

API_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"


class ElevenLabsClient:

    def __init__(self, api_key=None, voice_id=None, model_id="eleven_multilingual_v2"):

        self.api_key = api_key or os.environ.get("ELEVENLABS_API_KEY")
        self.voice_id = voice_id or os.environ.get("ELEVENLABS_VOICE_ID")
        self.model_id = model_id

        if not self.api_key:
            raise ValueError("Clé API ElevenLabs manquante (variable ELEVENLABS_API_KEY).")

        if not self.voice_id:
            raise ValueError("voice_id manquant (variable ELEVENLABS_VOICE_ID).")

    def generate(self, text, output_path):
        """Génère l'audio pour `text` et l'écrit dans output_path (mp3)."""

        url = API_URL.format(voice_id=self.voice_id)

        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
        }

        payload = {
            "text": text,
            "model_id": self.model_id,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
            },
        }

        response = requests.post(url, headers=headers, json=payload, timeout=60)

        if response.status_code != 200:
            raise RuntimeError(
                f"Erreur ElevenLabs ({response.status_code}) : {response.text}"
            )

        with open(output_path, "wb") as f:
            f.write(response.content)

        return output_path


def get_audio_duration(filepath):
    """Mesure la durée réelle d'un fichier audio via ffprobe (en secondes)."""

    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(filepath),
        ],
        capture_output=True, text=True, check=True,
    )

    return float(result.stdout.strip())
