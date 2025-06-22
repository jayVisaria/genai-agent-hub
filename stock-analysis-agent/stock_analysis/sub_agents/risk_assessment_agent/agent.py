"""Risk Assessment Agent - Comprehensive investment risk analysis"""

from datetime import datetime
from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from . import prompt

MODEL = "gemini-2.0-flash-001"

# Format current date for dynamic insertion
current_date = datetime.now().strftime("%B %d, %Y")
formatted_prompt = prompt.RISK_ASSESSMENT_PROMPT.format(current_date=current_date)

risk_assessment_agent = LlmAgent(
    name="risk_assessment_agent",
    model=MODEL,
    description=(
        "Expert risk analyst specializing in comprehensive investment risk "
        "assessment, quantitative risk modeling, and risk mitigation strategies "
        "for portfolio management and investment decision-making."
    ),
    instruction=formatted_prompt,
    output_key="risk_assessment_output",
    tools=[google_search],
)