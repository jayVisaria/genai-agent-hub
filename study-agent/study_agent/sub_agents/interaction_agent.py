"""Interaction Agent: Manages the direct conversational engagement with the user."""

from google.adk.agents import Agent

from .. import prompt

MODEL = "gemini-2.5-pro-preview-05-06"

interaction_agent = Agent(
    name="interaction_agent",
    model=MODEL,
    description="Manages the direct conversational engagement with the user.",
    instruction=prompt.INTERACTION_PROMPT,
)

