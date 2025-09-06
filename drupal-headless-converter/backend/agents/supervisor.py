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


supervisor_prompt = """You are a supervisor tasked with managing a conversation between the
following workers: parser_agent, builder_agent. Given the following user request,
respond with the worker to act next. Each worker will perform a task and respond with their results
and status. When the user is satisfied, respond with FINISH."""

supervisor_agent = create_react_agent(llm, [], prompt=supervisor_prompt)

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



