"""Personalization Agent: Adapts educational content to individual user needs."""

from google.adk.agents import Agent
from langchain.memory import ConversationBufferMemory

from .. import prompt

MODEL = "gemini-2.5-pro-preview-05-06"

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

personalization_agent = Agent(
    name="personalization_agent",
    model=MODEL,
    description="Adapts educational content to individual user needs.",
    instruction=prompt.PERSONALIZATION_PROMPT,
    tools=[memory],
)
