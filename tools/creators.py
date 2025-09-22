from pathlib import Path
from typing import List

TRANSCRIPTS_DIR = Path("transcripts")
VIDEOS_DIR = Path("videos")


def list_creators_from_transcripts() -> List[str]:
    if not TRANSCRIPTS_DIR.exists():
        return []
    creators: List[str] = []
    for p in TRANSCRIPTS_DIR.glob("*.json"):
        if p.is_file():
            creators.append(p.stem)
    return sorted(set(creators))


def list_creators_from_videos() -> List[str]:
    if not VIDEOS_DIR.exists():
        return []
    creators: List[str] = []
    for sub in VIDEOS_DIR.iterdir():
        if sub.is_dir():
            creators.append(sub.name)
    return sorted(set(creators))


def list_creators() -> List[str]:
    creators = list_creators_from_transcripts()
    if creators:
        return creators
    return list_creators_from_videos()


if __name__ == "__main__":
    print("\n".join(list_creators())) 