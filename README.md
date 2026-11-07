# YouTube Transcription

Petit projet Python pour récupérer **tout ce qui est dit dans une vidéo YouTube** et l'enregistrer dans un fichier texte. Le but est simple : pouvoir relire une vidéo, chercher une information précise ou analyser son contenu sans devoir tout réécouter.

## Fonctionnement

Le script essaie d'abord de récupérer les sous-titres de YouTube (en français en priorité, puis en anglais). Si la vidéo n'a pas de sous-titres accessibles, il télécharge l'audio et utilise **Whisper en local** pour faire la transcription.

Pas besoin de clé API ni d'abonnement.

## Installation

Il faut avoir **Python 3.10 ou plus récent** installé.

Dans un terminal, à la racine du projet :

```bash
pip install -U youtube-transcript-api yt-dlp faster-whisper
```

## Utilisation

Lancer le script :

```bash
python youtube_transcription.py
```

Coller ensuite le lien de la vidéo YouTube quand il est demandé :

```text
Lien YouTube : https://www.youtube.com/watch?v=XXXXXXXXXXX
```

Le script s'occupe du reste.

## Fichiers générés

Deux fichiers sont créés à la racine du projet :

- **`transcription.txt`** : tout le texte de la vidéo, sans les horaires.
- **`transcription_horodatee.txt`** : la transcription avec les minutes et secondes, pour retrouver un passage dans la vidéo.

Exemple :

```text
[00:12] Bonjour à tous, aujourd'hui on va parler du recrutement.
[01:35] Les candidatures sont ouvertes jusqu'au 16 novembre.
```

*Les phrases ci-dessus sont uniquement un exemple de format.*

## À savoir

- La récupération des sous-titres est généralement plus rapide que la transcription audio.
- Si Whisper est utilisé, le modèle est téléchargé lors de la première utilisation. Ensuite, la transcription se fait sur l'ordinateur.
- Le script utilise le modèle **`small`** de Whisper sur CPU. Pour gagner en précision, on peut remplacer `small` par `medium` dans le code, mais ce sera plus lent.
- Certaines vidéos peuvent bloquer l'accès aux sous-titres ou le téléchargement de l'audio.
- La transcription n'est pas forcément parfaite, surtout pour les noms propres, les chiffres et les passages avec du bruit.
- Les fichiers de sortie sont **écrasés** à chaque nouvelle transcription : penser à les renommer si on veut les garder.

## Pourquoi ce projet ?

Je voulais surtout pouvoir récupérer le contenu complet d'un webinaire ou d'une vidéo, puis rechercher rapidement une date, une consigne ou une information importante. Une fois le fichier `.txt` généré, je peux aussi le donner à une IA pour vérifier certains passages.
