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


def resolve_creator_name(name: str) -> str:
    """Resolve user-provided creator name to a known creator slug.
    - Normalizes case
    - Replaces spaces/underscores with hyphens
    - Tries exact and simple heuristic matches
    Returns empty string if not found.
    """
    candidates = set(list_creators())
    if not candidates:
        return ""

    raw = name.strip()
    if not raw:
        return ""

    # basic normalizations
    variants = []
    variants.append(raw)
    variants.append(raw.lower())
    variants.append(raw.replace(" ", "-").lower())
    variants.append(raw.replace("_", "-").lower())

    for v in variants:
        if v in candidates:
            return v

    # case-insensitive match
    lower_map = {c.lower(): c for c in candidates}
    for v in variants:
        if v.lower() in lower_map:
            return lower_map[v.lower()]

    # startswith/contains heuristics
    for c in candidates:
        if any(v in c for v in variants):
            return c

    return ""


if __name__ == "__main__":
    print("\n".join(list_creators())) 