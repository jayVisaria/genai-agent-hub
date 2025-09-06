import wikipedia
from google.adk.tools import Tool

def search_wikipedia(query: str) -> str:
    """Searches Wikipedia for a given query."""
    return wikipedia.summary(query)

wikipedia_tool = Tool(
    name="search_wikipedia",
    description="Searches Wikipedia for a given query.",
    func=search_wikipedia,
)
