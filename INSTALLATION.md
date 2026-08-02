# Installation - MyCoach

## Prérequis

- Python 3.10+
- ffmpeg (pour l'assemblage audio)

### Installer ffmpeg

**Mac** : `brew install ffmpeg`
**Windows** : télécharge sur https://ffmpeg.org/download.html et ajoute-le au PATH
**Linux** : `sudo apt install ffmpeg`

Vérifie que ça fonctionne :
```
ffmpeg -version
```

## Installer les dépendances Python

```
pip install -r requirements.txt
```

## Configurer les identifiants ElevenLabs

Récupère :
1. Ta clé API : elevenlabs.io → profil → API Keys
2. Le voice_id de la voix "Irène" : Voice Library → cherche la voix → "..." → Copy Voice ID
   (ou lance `python list_voices.py` une fois ta clé API définie, ça affiche toutes tes voix avec leur ID)

Puis, dans ton terminal, avant de lancer le script :

**Mac/Linux :**
```
export ELEVENLABS_API_KEY="ta_clé"
export ELEVENLABS_VOICE_ID="le_voice_id"
```

**Windows (PowerShell) :**
```
$env:ELEVENLABS_API_KEY="ta_clé"
$env:ELEVENLABS_VOICE_ID="le_voice_id"
```

⚠️ Ne mets jamais ta clé API directement dans le code ou dans un fichier commité sur GitHub.

## Lancer

```
python main.py "Samples/workout-Int4x2-30-30.jsonV2"
```

Sans les variables d'environnement définies : affiche seulement le script de la séance (aperçu).
Avec les variables définies : génère `output/workout.mp3`.

## En cas d'erreur

Copie-colle le message d'erreur complet dans notre conversation, je corrige.
