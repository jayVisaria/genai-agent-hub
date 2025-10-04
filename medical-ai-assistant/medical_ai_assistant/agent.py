from typing import Annotated, Any, Dict, List, Optional, Sequence, TypedDict
import operator

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers.openai_functions import JsonOutputFunctionsParser


@tool
def analyze_image(image_path: str):
    """Analyzes a medical image and returns a report."""
    return f"Image analysis report for {image_path}"


@tool
def triage_symptoms(symptoms: str):
    """Triages patient symptoms and provides a preliminary assessment."""
    return f"Symptom triage report for: {symptoms}"


@tool
def medical_knowledge_retrieval(query: str):
    """Retrieves medical knowledge based on a query."""
    return f"Medical knowledge retrieval for: {query}"


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str


class Agent:
    def __init__(self, model, tools, system=""):
        self.system = system
        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_openai)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges("llm", self.exists_action, {True: "action", False: END})
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile()
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)

    def exists_action(self, state: AgentState):
        result = state['messages'][-1]
        return len(result.tool_calls) > 0

    def call_openai(self, state: AgentState):
        messages = state['messages']
        if self.system:
            messages = [HumanMessage(content=self.system)] + list(messages)
        message = self.model.invoke(messages)
        return {'messages': [message]}

    def take_action(self, state: AgentState):
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            result = self.tools[t['name']].invoke(t['args'])
            results.append(HumanMessage(content=str(result), name=t['name']))
        return {'messages': results}


class Supervisor:
    def __init__(self, model, agents):
        self.model = model
        self.agents = agents
        self.supervisor_chain = self.create_supervisor_chain()

    def create_supervisor_chain(self):
        members = list(self.agents.keys())
        system_prompt = ("You are a supervisor tasked with managing a conversation between the"
                         " following workers:  {members}. Given the following user request,"
                         " respond with the worker to act next. Each worker will perform a"
                         " task and respond with their results and status. When the user is satisfied,"
                         " respond with FINISH.")
        options = ["FINISH"] + members
        function_def = {
            "name": "route",
            "description": "Select the next role.",
            "parameters": {"title": "routeSchema", "type": "object", "properties": {
                "next": {"title": "Next", "anyOf": [{"enum": options}]}}, "required": ["next"]},
        }
        prompt = ChatPromptTemplate.from_messages([("system", system_prompt),
                                                   MessagesPlaceholder(variable_name="messages"),
                                                   ("system", "Given the conversation above, who should act next?"
                                                              " Or should we FINISH? Select one of: {options}"),
                                                   ]).partial(options=str(options), members=", ".join(members))
        return (prompt | self.model.bind_functions(functions=[function_def], function_call="route") | JsonOutputFunctionsParser())

    def call_supervisor(self, state: AgentState):
        result = self.supervisor_chain.invoke(state)
        return {"next": result["next"]}


llm = ChatGoogleGenerativeAI(model="gemini-pro")
image_agent = Agent(llm, [analyze_image], "You are a medical image analysis expert.")
symptom_agent = Agent(llm, [triage_symptoms], "You are a symptom triage expert.")
knowledge_agent = Agent(llm, [medical_knowledge_retrieval], "You are a medical knowledge retrieval expert.")
agents = {
    "image_analyzer": image_agent,
    "symptom_triager": symptom_agent,
    "knowledge_retriever": knowledge_agent,
}
supervisor = Supervisor(llm, agents)
workflow = StateGraph(AgentState)
workflow.add_node("supervisor", supervisor.call_supervisor)
for member, agent in agents.items():
    workflow.add_node(member, agent.graph.invoke)
