from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.tavily import TavilyTools
from agno.storage.sqlite import SqliteStorage
from agno.playground import Playground, serve_playground_app
from dotenv import load_dotenv

load_dotenv()

copywriter = Agent(
    model=Gemini(id="gemini-1.5-flash"),
    name="copywriter",
    add_history_to_messages=True,
    num_history_runs=3,
    storage=SqliteStorage(
        table_name="agent_sessions",
        db_file="tmp/storage.db"
    ),
    tools=[TavilyTools()],
    show_tool_calls=True,
    instructions=open("prompts/copywriter.md").read()
)

app = Playground(agents=[copywriter]).get_app()

if __name__ == '__main__':
    serve_playground_app('agent:app', reload=True)
