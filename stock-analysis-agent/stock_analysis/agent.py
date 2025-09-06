"""Stock Analysis Coordinator: Main agent orchestrating comprehensive stock analysis"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .prompts import coordinator_prompt
from .sub_agents.analysis_agent import analysis_orchestrator
from .sub_agents.prediction_agent import stock_prediction_agent

MODEL = "gemini-2.5-pro-preview-05-06"

stock_analysis_coordinator = Agent(
    name="stock_analysis_coordinator",
    model=MODEL,
    description=(
        "Institutional-grade stock analysis coordinator that orchestrates "
        "comprehensive multi-factor analysis through specialized agents to "
        "deliver professional investment reports matching top-tier financial institutions."
    ),
    instruction=coordinator_prompt.STOCK_ANALYSIS_COORDINATOR_PROMPT,
    tools=[
        AgentTool(agent=analysis_orchestrator),
        AgentTool(agent=stock_prediction_agent),
    ],
)

root_agent = stock_analysis_coordinator
