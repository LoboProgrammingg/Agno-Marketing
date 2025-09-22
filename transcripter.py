import os
import json
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile
from groq import Groq
from dotenv import load_dotenv


load_dotenv()


VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v"}
VIDEOS_DIR = Path("videos")
OUTPUT_DIR = Path("transcripts")
MODEL = "whisper-large-v3"


def extract_audio(input_path: Path) -> Path:
    tmp = NamedTemporaryFile(suffix=".wav", delete=False)
    tmp_path = Path(tmp.name)
    tmp.close()
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        str(tmp_path),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return tmp_path


def transcribe_file(client: Groq, audio_path: Path) -> str:
    with open(audio_path, "rb") as f:
        resp = client.audio.transcriptions.create(
            model=MODEL,
            file=(audio_path.name, f),
        )
    return resp.text


def main() -> None:
    if not VIDEOS_DIR.exists():
        print("Pasta 'videos' não encontrada.")
        return

    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for video in VIDEOS_DIR.rglob("*"):
        if not video.is_file() or video.suffix.lower() not in VIDEO_EXTS:
            continue
        try:
            creator = video.relative_to(VIDEOS_DIR).parts[0]
        except Exception:
            continue

        audio_path = extract_audio(video)
        try:
            text = transcribe_file(client, audio_path)
        finally:
            try:
                audio_path.unlink(missing_ok=True)
            except Exception:
                pass

        out_path = OUTPUT_DIR / f"{creator}.json"
        data = []
        if out_path.exists():
            try:
                data = json.loads(out_path.read_text(encoding="utf-8"))
            except Exception:
                data = []

        data.append({
            "creator": creator,
            "video": str(video.relative_to(VIDEOS_DIR)),
            "transcript": text,
        })
        out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Transcrito: {video} → {out_path}")


if __name__ == "__main__":
    main()
