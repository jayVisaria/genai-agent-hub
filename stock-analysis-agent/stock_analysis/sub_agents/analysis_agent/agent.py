"""Analysis orchestrator agent - coordinates all specialized analysis agents"""

from datetime import datetime
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from stock_analysis.prompts import analysis_prompt
from ..fundamental_agent import fundamental_analysis_agent
from ..technical_agent import technical_analysis_agent
from ..sentiment_agent import sentiment_analysis_agent
from ..qualitative_agent import qualitative_analysis_agent
from ..risk_assessment_agent import risk_assessment_agent
from ..prediction_agent import stock_prediction_agent

MODEL = "gemini-2.5-pro-preview-05-06"

# Format current date for dynamic insertion
current_date = datetime.now().strftime("%B %d, %Y")
formatted_prompt = analysis_prompt.ANALYSIS_ORCHESTRATOR_PROMPT.format(current_date=current_date)

analysis_orchestrator = Agent(
    name="analysis_orchestrator",
    model=MODEL,
    description=(
        "Master orchestrator that coordinates specialized analysis agents to produce "
        "institutional-grade investment reports matching the quality of top-tier financial institutions."
    ),
    instruction=formatted_prompt,
    tools=[
        AgentTool(agent=fundamental_analysis_agent),
        AgentTool(agent=technical_analysis_agent),
        AgentTool(agent=sentiment_analysis_agent),
        AgentTool(agent=qualitative_analysis_agent),
        AgentTool(agent=risk_assessment_agent),
        AgentTool(agent=stock_prediction_agent),
    ],
)

