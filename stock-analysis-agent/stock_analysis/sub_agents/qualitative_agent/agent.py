"""Qualitative Analysis Agent - Business quality and competitive analysis"""

from datetime import datetime
from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from . import prompt

MODEL = "gemini-2.5-pro-preview-05-06"

# Format current date for dynamic insertion
current_date = datetime.now().strftime("%B %d, %Y")
formatted_prompt = prompt.QUALITATIVE_ANALYSIS_PROMPT.format(current_date=current_date)

qualitative_analysis_agent = LlmAgent(
    name="qualitative_analysis_agent",
    model=MODEL,
    description=(
        "Expert qualitative analyst specializing in management assessment, "
        "business model evaluation, competitive advantage analysis, and "
        "long-term sustainability factors for investment decisions."
    ),
    instruction=formatted_prompt,
    output_key="qualitative_analysis_output",
    tools=[google_search],
)