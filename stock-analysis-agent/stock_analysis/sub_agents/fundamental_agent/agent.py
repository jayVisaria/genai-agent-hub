"""Fundamental Analysis Agent - Financial statement and ratio analysis"""

from datetime import datetime
from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from . import prompt

MODEL = "gemini-2.5-pro-preview-05-06"

# Format current date for dynamic insertion
current_date = datetime.now().strftime("%B %d, %Y")
formatted_prompt = prompt.FUNDAMENTAL_ANALYSIS_PROMPT.format(current_date=current_date)

fundamental_analysis_agent = LlmAgent(
    name="fundamental_analysis_agent",
    model=MODEL,
    description=(
        "Expert fundamental analyst specializing in financial statement analysis, "
        "ratio analysis, valuation models, and intrinsic value calculation for "
        "equity research and investment decision-making."
    ),
    instruction=formatted_prompt,
    output_key="fundamental_analysis_output",
    tools=[google_search],
)