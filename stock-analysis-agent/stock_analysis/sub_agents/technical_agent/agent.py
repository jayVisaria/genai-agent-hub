"""Technical Analysis Agent - Chart analysis and trading signals"""

from datetime import datetime
from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from . import prompt

MODEL = "gemini-2.5-pro-preview-05-06"

# Format current date for dynamic insertion
current_date = datetime.now().strftime("%B %d, %Y")
formatted_prompt = prompt.TECHNICAL_ANALYSIS_PROMPT.format(current_date=current_date)

technical_analysis_agent = LlmAgent(
    name="technical_analysis_agent",
    model=MODEL,
    description=(
        "Expert technical analyst specializing in chart pattern analysis, "
        "technical indicators, trend identification, and trading signal "
        "generation for investment timing and risk management."
    ),
    instruction=formatted_prompt,
    output_key="technical_analysis_output",
    tools=[google_search],
)
