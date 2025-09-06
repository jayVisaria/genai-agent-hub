"""Socratic Teacher Agent"""

from google.adk.agents import LlmAgent
from .prompts.teacher_prompt import SOCRATIC_TEACHER_PROMPT
from .tools import wikipedia_tool

MODEL = "gemini-1.5-pro-preview-0514"

socratic_teacher_agent = LlmAgent(
    name="socratic_teacher_agent",
    model=MODEL,
    description="A Socratic teacher that guides students to discover answers on their own.",
    instruction=SOCRATIC_TEACHER_PROMPT,
    output_key="socratic_dialogue_output",
    tools=[wikipedia_tool],
)
