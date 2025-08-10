"""Personalization Agent: Adapts educational content to individual user needs."""

from google.adk.agents import Agent

from .. import prompt

MODEL = "gemini-2.5-pro"

personalization_agent = Agent(
    name="personalization_agent",
    model=MODEL,
    description="Adapts educational content to individual user needs.",
    instruction=prompt.PERSONALIZATION_PROMPT,
)

