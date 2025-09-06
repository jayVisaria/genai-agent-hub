from typing import TypedDict, List
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent

from .parser_agent import run_parser
from .builder_agent import create_builder_agent

class SupervisorState(TypedDict):
    messages: List[BaseMessage]
    next: str


llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")

parser_agent = run_parser
builder_agent = create_builder_agent()


