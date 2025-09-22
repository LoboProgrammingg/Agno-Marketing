import json
from pathlib import Path
from typing import List, Dict, Any

TRANSCRIPTS_DIR = Path("transcripts")


def get_creator_transcripts_markdown(creator: str) -> str:
    """Return all transcripts for the given creator as a single markdown string.

    Output format:

    Transcript 1
    <transcrição>

    Transcript 2
    <transcrição>
    """
    file_path = TRANSCRIPTS_DIR / f"{creator}.json"
    if not file_path.exists():
        return ""

    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except Exception:
        return ""

    if not isinstance(data, list):
        return ""

    transcripts: List[str] = []
    index = 1
    for item in data:
        if not isinstance(item, dict):
            continue
        text = item.get("transcript")
        if not text:
            continue
        transcripts.append(f"Transcript {index}\n{text}")
        index += 1

    return ("\n\n".join(transcripts)).strip()


def get_creator_transcripts_list(creator: str, limit: int | None = None) -> List[str]:
    """Return a list of transcript strings for the given creator.
    Optionally limit the number of items returned.
    """
    file_path = TRANSCRIPTS_DIR / f"{creator}.json"
    if not file_path.exists():
        return []

    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except Exception:
        return []

    if not isinstance(data, list):
        return []

    texts: List[str] = []
    for item in data:
        if isinstance(item, dict):
            text = item.get("transcript")
            if text:
                texts.append(str(text))
        if limit is not None and len(texts) >= limit:
            break
    return texts


def prepare_creator_context(creator: str, limit: int = 5) -> Dict[str, Any]:
    """Return a composite object with samples (list) and markdown (string)."""
    samples = get_creator_transcripts_list(creator, limit=limit)
    markdown = get_creator_transcripts_markdown(creator)
    return {"creator": creator, "samples": samples, "markdown": markdown}


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m tools.transcripts <creator>")
        raise SystemExit(2)

    creator_arg = sys.argv[1]
    output = get_creator_transcripts_markdown(creator_arg)
    print(output) 