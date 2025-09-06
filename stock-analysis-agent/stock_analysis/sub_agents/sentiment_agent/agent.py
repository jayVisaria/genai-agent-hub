"""Sentiment Analysis Agent - Market sentiment and news analysis"""

from datetime import datetime
from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from stock_analysis.prompts import sentiment_prompt

MODEL = "gemini-2.5-pro-preview-05-06"

# Format current date for dynamic insertion
current_date = datetime.now().strftime("%B %d, %Y")
formatted_prompt = sentiment_prompt.SENTIMENT_ANALYSIS_PROMPT.format(current_date=current_date)

sentiment_analysis_agent = LlmAgent(
    name="sentiment_analysis_agent",
    model=MODEL,
    description=(
        "Expert sentiment analyst specializing in market sentiment analysis, "
        "news sentiment evaluation, analyst opinion aggregation, and "
        "contrarian opportunity identification for investment decisions."
    ),
    instruction=formatted_prompt,
    output_key="sentiment_analysis_output",
    tools=[google_search],
)


