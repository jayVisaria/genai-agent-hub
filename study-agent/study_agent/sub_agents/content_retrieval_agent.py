"""Content Retrieval Agent: Fetches educational content from various sources."""

from google.adk.agents import Agent
from google.adk.tools import google_search

from .. import prompt

MODEL = "gemini-2.5-pro"

content_retrieval_agent = Agent(
    name="content_retrieval_agent",
    model=MODEL,
    description="Fetches educational content from various sources.",
    instruction=prompt.CONTENT_RETRIEVAL_PROMPT,
    tools=[google_search],
)

