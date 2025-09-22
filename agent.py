from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.tavily import TavilyTools
from agno.storage.sqlite import SqliteStorage
from agno.playground import Playground, serve_playground_app
from dotenv import load_dotenv
from typing import Annotated, List, Dict, Any
from tools.transcripts import (
    get_creator_transcripts_markdown,
    get_creator_transcripts_list,
    prepare_creator_context as _prepare_creator_context,
)
from tools.creators import list_creators as _list_creators, resolve_creator_name

load_dotenv()


def read_creator_transcripts(
    creator: Annotated[str, "Nome do criador (nome da pasta em transcripts/). Aceita variações (espaços/_ serão normalizados)."],
) -> str:
    slug = resolve_creator_name(creator) or creator
    return get_creator_transcripts_markdown(slug)


def list_creators() -> List[str]:
    return _list_creators()


def sample_creator_transcripts(
    creator: Annotated[str, "Nome do criador (nome da pasta em transcripts/). Aceita variações."],
    limit: Annotated[int, "Limite de exemplos (opcional)"] = 5,
) -> List[str]:
    slug = resolve_creator_name(creator) or creator
    return get_creator_transcripts_list(slug, limit=limit)


def prepare_creator_context(
    creator: Annotated[str, "Nome do criador (nome da pasta em transcripts/). Aceita variações."],
    limit: Annotated[int, "Quantidade de exemplos para análise"] = 5,
) -> Dict[str, Any]:
    slug = resolve_creator_name(creator) or creator
    return _prepare_creator_context(slug, limit=limit)


copywriter = Agent(
    model=Gemini(id="gemini-1.5-flash"),
    name="copywriter",
    add_history_to_messages=True,
    num_history_runs=3,
    storage=SqliteStorage(
        table_name="agent_sessions",
        db_file="tmp/storage.db"
    ),
    tools=[
        list_creators,
        prepare_creator_context,
        sample_creator_transcripts,
        read_creator_transcripts,
        TavilyTools(),
    ],
    show_tool_calls=True,
    instructions=open("prompts/copywriter.md").read()
)

app = Playground(agents=[copywriter]).get_app()

if __name__ == '__main__':
    serve_playground_app('agent:app', reload=True)
