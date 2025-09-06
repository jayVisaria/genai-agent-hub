"""Study and Learn Coordinator: Main agent orchestrating personalized learning experiences"""

from google.adk.agents import Agent
from .prompts.coordinator_prompt import STUDY_COORDINATOR_PROMPT
from .socratic_teacher_agent import socratic_teacher_agent

MODEL = "gemini-2.5-pro"

study_coordinator = Agent(
    name="study_coordinator",
    model=MODEL,
    description=("A specialized study coordinator that facilitates personalized and interactive learning experiences."),
    instruction=STUDY_COORDINATOR_PROMPT,
    sub_agents=[socratic_teacher_agent],
)

root_agent = study_coordinator


