"""
Liste toutes tes voix ElevenLabs avec leur voice_id.
Utile pour trouver le voice_id de "Irène".

Usage : python list_voices.py
(nécessite ELEVENLABS_API_KEY défini dans l'environnement)
"""

import os
import requests

api_key = os.environ.get("ELEVENLABS_API_KEY")

if not api_key:
    print("Définis d'abord ELEVENLABS_API_KEY dans ton terminal.")
    exit(1)

response = requests.get(
    "https://api.elevenlabs.io/v1/voices",
    headers={"xi-api-key": api_key},
)

if response.status_code != 200:
    print(f"Erreur ({response.status_code}) : {response.text}")
    exit(1)

voices = response.json()["voices"]

for v in voices:
    print(f"{v['name']:20s} {v['voice_id']}")
