"""Study and Learn Coordinator: Main agent orchestrating personalized learning experiences"""

from google.adk.agents import Agent
from google.adk.tools import google_search

from . import prompt

MODEL = "gemini-2.5-pro"


study_coordinator = Agent(
    name="study_coordinator",
    model=MODEL,
    description=("A specialized study coordinator that facilitates personalized and interactive learning experiences."),
    instruction=prompt.STUDY_COORDINATOR_PROMPT,
    tools=[google_search],
)

root_agent = study_coordinator

