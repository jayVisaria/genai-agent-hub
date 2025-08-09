"""Interaction Agent: Manages the direct conversational engagement with the user."""

from google.adk.agents import Agent
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI

from .. import prompt

MODEL = "gemini-2.5-pro-preview-05-06"

llm = ChatGoogleGenerativeAI(model=MODEL)
memory = ConversationBufferMemory()
conversation_chain = ConversationChain(llm=llm, memory=memory)

interaction_agent = Agent(
    name="interaction_agent",
    model=MODEL,
    description="Manages the direct conversational engagement with the user.",
    instruction=prompt.INTERACTION_PROMPT,
    tools=[conversation_chain],
)
