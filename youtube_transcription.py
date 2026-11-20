# pip install -U youtube-transcript-api yt-dlp faster-whisper
# 
from youtube_transcript_api import YouTubeTranscriptApi
from faster_whisper import WhisperModel
from yt_dlp import YoutubeDL
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import tempfile

def extraire_id(url):
    parsed = urlparse(url)
    host = parsed.netloc.lower().removeprefix("www.")

    if host == "youtu.be":
        return parsed.path.strip("/").split("/")[0]

    if host in ("youtube.com", "m.youtube.com", "music.youtube.com"):
        if parsed.path == "/watch":
            return parse_qs(parsed.query)["v"][0]
        if parsed.path.startswith(("/shorts/", "/live/", "/embed/")):
            return parsed.path.strip("/").split("/")[1]

    raise ValueError("Lien YouTube non reconnu")


def recuperer_sous_titres(video_id):
    api = YouTubeTranscriptApi()
    disponibles = list(api.list(video_id))

    # Priorité au français, puis à l'anglais
    selection = next(
        (t for langue in ("fr", "en")
         for t in disponibles if t.language_code == langue),
        disponibles[0]
    )

    return [
        (segment.start, segment.text.replace("\n", " "))
        for segment in selection.fetch()
    ]


def transcrire_audio(url):
    print("Téléchargement de l'audio...")

    with tempfile.TemporaryDirectory() as dossier:
        options = {
            "format": "bestaudio/best",
            "outtmpl": str(Path(dossier) / "%(id)s.%(ext)s"),
            "noplaylist": True
        }

        with YoutubeDL(options) as ydl:
            infos = ydl.extract_info(url, download=True)
            chemin_audio = ydl.prepare_filename(infos)

        print("Transcription avec Whisper...")

        modele = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8"
        )

        segments, infos = modele.transcribe(
            chemin_audio,
            beam_size=5,
            vad_filter=True
        )

        # return [
        #     (segment.start, segment.text.strip())
        #     for segment in segments
        # ]
        resultat = []

        for segment in segments:
            texte = segment.text.strip()
            resultat.append((segment.start, texte))
        
            print(f"[{segment.start:.1f}s] {texte}", flush=True)
        
        return resultat


def main():
    url = input("Lien YouTube : ").strip()
    video_id = extraire_id(url)

    try:
        print("Recherche des sous-titres YouTube...")
        segments = recuperer_sous_titres(video_id)
        print("Sous-titres récupérés !")

    except Exception as erreur:
        print(f"Sous-titres indisponibles : {erreur}")
        print("Passage à la transcription audio...")
        segments = transcrire_audio(url)

    # Transcription complète
    texte = " ".join(texte for _, texte in segments)

    Path("transcription.txt").write_text(
        texte, encoding="utf-8"
    )

    # Transcription avec horodatage
    with open("transcription_horodatee.txt", "w", encoding="utf-8") as f:
        for secondes, phrase in segments:
            minutes = int(secondes) // 60
            secondes_restantes = int(secondes) % 60

            f.write(
                f"[{minutes:02}:{secondes_restantes:02}] "
                f"{phrase}\n"
            )

    print("\nTerminé !")
    print("Fichiers créés :")
    print("- transcription.txt")
    print("- transcription_horodatee.txt")


if __name__ == "__main__":
    main()
