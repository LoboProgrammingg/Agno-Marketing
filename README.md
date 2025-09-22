# Agno Playground + Copywriter Agent + Video Transcription

A project that combines:

- An AI copywriter agent served via Agno Playground
- A structured prompt (XML with CDATA preserving original Markdown)
- A video transcription utility (`transcripter.py`) that scans `videos/`, extracts audio with ffmpeg, and transcribes using Groq Whisper

This README documents setup, environment configuration, running with UV, API usage, and troubleshooting.

## Contents

- [Features](#features)
- [Requirements](#requirements)
- [Environment (.env)](#environment-env)
- [Installation (UV)](#installation-uv)
- [Run the Agno Playground](#run-the-agno-playground)
  - [OpenAPI/Docs](#openapidocs)
  - [Test via cURL](#test-via-curl)
  - [Use with Agno Playground UI](#use-with-agno-playground-ui)
- [Video Transcription (Groq Whisper)](#video-transcription-groq-whisper)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

## Features

- Copywriter agent powered by Google Gemini and Tavily tools
- Prompt stored as XML with CDATA to preserve the original Markdown content verbatim
- API endpoints exposed under `/v1/playground/...` with FastAPI + Uvicorn
- Batch transcription across nested video folders, saving per-creator JSON outputs

## Requirements

- Python 3.12+
- UV (dependency and venv manager): `https://docs.astral.sh/uv/`
- ffmpeg (only for the transcription workflow)

## Environment (.env)

Create a `.env` in the project root with your keys:

```
GOOGLE_API_KEY=...       # Gemini (Copywriter agent)
TAVILY_API_KEY=...       # Tavily (web search)
GROQ_API_KEY=...         # Groq (Whisper transcription)
```

Both `agent.py` and `transcripter.py` load environment variables with `python-dotenv`.

## Installation (UV)

```bash
cd "/home/loboprogramming/Área de trabalho/agno"
uv sync
```

Add new dependencies when needed:

```bash
uv add <package>[extras]==<version>
uv sync
```

## Run the Agno Playground

The copywriter agent is defined in `agent.py` (Gemini + Tavily, prompt in `prompts/copywriter.md`).

Start the Playground (recommended):

```bash
uv run python agent.py
```

Expected output includes:

- Server on `http://localhost:7777`
- A Playground URL similar to: `https://app.agno.com/playground?endpoint=localhost%3A7777`

Alternative (run the ASGI app directly):

```bash
uv run python -m uvicorn agent:app --reload --port 8001
```

### OpenAPI/Docs

- Swagger UI: `http://localhost:7777/docs`
- All routes are under `/v1/playground/...`

### Test via cURL

Health check:

```bash
curl http://127.0.0.1:7777/v1/playground/status
```

List agents and capture `agent_id`:

```bash
curl http://127.0.0.1:7777/v1/playground/agents
```

Run the agent (non-streaming):

```bash
AGENT_ID="<your-agent-id>"
curl -X POST "http://127.0.0.1:7777/v1/playground/agents/$AGENT_ID/runs" \
  -F message="Escreva um copy curto sobre café" \
  -F stream=false
```

Run the agent (SSE streaming):

```bash
curl -N -X POST "http://127.0.0.1:7777/v1/playground/agents/$AGENT_ID/runs" \
  -F message="Escreva um copy curto sobre café (stream)" \
  -F stream=true
```

### Use with Agno Playground UI

- Endpoint: `http://localhost:7777`
- Prefix: `/v1`
- If a single URL is required: `http://localhost:7777/v1`

From another device on the same network, replace `localhost` with your LAN IP (e.g., `http://192.168.0.10:7777` with prefix `/v1`).

## Video Transcription (Groq Whisper)

`transcripter.py` performs:

- Recursive scan under `videos/` (e.g., `videos/joao-bezerra/video1.mp4`)
- Audio extraction via ffmpeg (mono, 16kHz)
- Transcription using Groq Whisper (`whisper-large-v3`)
- Per-creator output at `transcripts/<creator>.json`

Prerequisites:

- `ffmpeg` installed
- `GROQ_API_KEY` available in `.env`

Run:

```bash
uv run python transcripter.py
```

Example layout and output:

```
videos/
  joao-bezerra/
    video1.mp4
    video2.mov
transcripts/
  joao-bezerra.json
```

Each JSON file accumulates entries like:

```json
[
  {
    "creator": "joao-bezerra",
    "video": "joao-bezerra/video1.mp4",
    "transcript": "..."
  }
]
```

## Project Structure

```
agno/
  agent.py                # Playground app + Copywriter agent (Gemini + Tavily)
  prompts/copywriter.md   # XML + CDATA, preserves original Markdown prompt
  transcripter.py         # Batch transcription (Groq Whisper + ffmpeg)
  README.md               # This guide
  pyproject.toml          # Dependencies and Python version
  uv.lock                 # UV lockfile
  videos/                 # Source videos (scanned recursively)
  transcripts/            # Output JSON (created on demand)
```

## Troubleshooting

- Port in use (7777/8000)
  - Change port (e.g., `--port 8001`) or kill the conflicting process
  - `lsof -i :7777 -sTCP:LISTEN` → `kill -9 <PID>`
- 404 on `/` or `/v1`
  - Expected. Use `/docs` and `/v1/playground/...`
- Missing credentials
  - Ensure `.env` is present and keys are correct; restart the server after changes
- ffmpeg not found
  - Install `ffmpeg` via your OS package manager
- Groq authentication errors (403/401)
  - Verify `GROQ_API_KEY` and network access

---

For enhancements or issues, open an issue or adjust the scripts and re-run with `uv run ...`. This project is designed to be minimal, reproducible, and easy to extend.
