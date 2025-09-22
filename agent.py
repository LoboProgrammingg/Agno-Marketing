from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.tavily import TavilyTools
from agno.storage.sqlite import SqliteStorage
from agno.playground import Playground, serve_playground_app
from dotenv import load_dotenv
from typing import Annotated, List
from tools.transcripts import get_creator_transcripts_markdown
from tools.creators import list_creators as _list_creators

load_dotenv()


def read_creator_transcripts(
    creator: Annotated[str, "Nome do criador (nome da pasta em transcripts/)"],
) -> str:
    return get_creator_transcripts_markdown(creator)


def list_creators() -> List[str]:
    return _list_creators()


copywriter = Agent(
    model=Gemini(id="gemini-1.5-flash"),
    name="copywriter",
    add_history_to_messages=True,
    num_history_runs=3,
    storage=SqliteStorage(
        table_name="agent_sessions",
        db_file="tmp/storage.db"
    ),
    tools=[TavilyTools(), list_creators, read_creator_transcripts],
    show_tool_calls=True,
    instructions=open("prompts/copywriter.md").read()
)

app = Playground(agents=[copywriter]).get_app()

if __name__ == '__main__':
    serve_playground_app('agent:app', reload=True)
