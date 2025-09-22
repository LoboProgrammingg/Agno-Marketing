import json
from pathlib import Path
from typing import List

TRANSCRIPTS_DIR = Path("transcripts")


def get_creator_transcripts_markdown(creator: str) -> str:
    """Return all transcripts for the given creator as a single markdown string.

    Args:
        creator_name (str): Nome do criador (ex: 'gran_concursos')
        
    Returns:
        str: Transcricoes formatadas em markdown ou mensagem de erro.
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


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m tools.transcripts <creator>")
        raise SystemExit(2)

    creator_arg = sys.argv[1]
    output = get_creator_transcripts_markdown(creator_arg)
    print(output) 