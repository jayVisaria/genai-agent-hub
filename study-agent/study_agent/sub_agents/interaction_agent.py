"""Interaction Agent: Manages the direct conversational engagement with the user."""

from google.adk.agents import Agent

from .. import prompt

MODEL = "gemini-2.5-pro"

interaction_agent = Agent(
    name="interaction_agent",
    model=MODEL,
    description="Manages the direct conversational engagement with the user.",
    instruction=prompt.INTERACTION_PROMPT,
)

