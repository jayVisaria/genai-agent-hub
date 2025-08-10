"""Learning Plan Agent: Creates structured, phase-based learning roadmaps for personalized education."""

from google.adk.agents import Agent

from .. import prompt

MODEL = "gemini-2.5-pro"

learning_plan_agent = Agent(
    name="learning_plan_agent",
    model=MODEL,
    description="Creates structured, phase-based learning roadmaps with clear progression paths.",
    instruction=prompt.LEARNING_PLAN_PROMPT,
)
