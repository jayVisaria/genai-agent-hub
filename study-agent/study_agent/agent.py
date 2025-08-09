"""Study and Learn Coordinator: Main agent orchestrating personalized learning experiences"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from .sub_agents.content_retrieval_agent import content_retrieval_agent
from .sub_agents.feedback_assessment_agent import feedback_assessment_agent
from .sub_agents.interaction_agent import interaction_agent
from .sub_agents.personalization_agent import personalization_agent
from .sub_agents.progress_tracking_agent import progress_tracking_agent

MODEL = "gemini-2.5-pro-preview-05-06"

study_coordinator = Agent(
    name="study_coordinator",
    model=MODEL,
    description=(
        "A specialized study coordinator that orchestrates a personalized and "
        "interactive learning experience through specialized agents."
    ),
    instruction=prompt.STUDY_COORDINATOR_PROMPT,
    tools=[
        AgentTool(agent=content_retrieval_agent),
        AgentTool(agent=personalization_agent),
        AgentTool(agent=interaction_agent),
        AgentTool(agent=feedback_assessment_agent),
        AgentTool(agent=progress_tracking_agent),
    ],
)

root_agent = study_coordinator
