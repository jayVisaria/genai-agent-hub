"""Content Retrieval Agent: Fetches educational content from various sources."""

from google.adk.agents import Agent
from langchain_community.tools import WikipediaSearch

from .. import prompt

MODEL = "gemini-2.5-pro-preview-05-06"

content_retrieval_agent = Agent(
    name="content_retrieval_agent",
    model=MODEL,
    description="Fetches educational content from various sources.",
    instruction=prompt.CONTENT_RETRIEVAL_PROMPT,
    tools=[WikipediaSearch()],
)

