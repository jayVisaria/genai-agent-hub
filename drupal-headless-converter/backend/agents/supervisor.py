from typing import TypedDict, List
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import Tool

from .parser_agent import run_parser
from .builder_agent import create_builder_agent

class SupervisorState(TypedDict):
    messages: List[BaseMessage]
    next: str


llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")

parser_agent = run_parser
builder_agent = create_builder_agent()

parser_tool = Tool(
    name="parser_agent",
    func=parser_agent,
    description="""Parse a Drupal website and return a JSON representation of the site.
    The input to this tool is the URL of the Drupal website to parse.
    The output of this tool is a JSON string representing the site structure and content.""",
)

builder_tool = Tool(
    name="builder_agent",
    func=builder_agent.invoke,
    description="""Build a new website from a JSON representation of a Drupal site.
    The input to this tool is a JSON object representing the site structure and content.
    The output of this tool is a message indicating the success or failure of the build process.""",
)


supervisor_prompt = """You are a supervisor tasked with managing a conversation between the
following workers: parser_agent, builder_agent. Given the following user request,
respond with the worker to act next. Each worker will perform a task and respond with their results
and status. When the user is satisfied, respond with FINISH."""

supervisor_agent = create_react_agent(llm, [parser_tool, builder_tool], prompt=supervisor_prompt)

def parser_node(state: SupervisorState):
    result = parser_agent(state["messages"][-1].content)
    return {"messages": [("tool", result)]}

def builder_node(state: SupervisorState):
    result = builder_agent.invoke({"messages": state["messages"]})
    return {"messages": result["messages"]}

workflow = StateGraph(SupervisorState)
workflow.add_node("parser", parser_node)
workflow.add_node("builder", builder_node)
workflow.add_node("supervisor", supervisor_agent)

workflow.add_edge("parser", "supervisor")
workflow.add_edge("builder", "supervisor")
workflow.add_conditional_edges("supervisor", lambda x: x["next"], {"parser": "parser", "builder": "builder", "FINISH": END})
workflow.set_entry_point("supervisor")

app = workflow.compile()
