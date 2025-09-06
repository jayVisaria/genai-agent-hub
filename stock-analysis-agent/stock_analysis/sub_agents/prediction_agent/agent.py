"""Stock Prediction Agent for stock predictions with deep research"""

from datetime import datetime
from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.adk.planners import BuiltInPlanner
from google.genai import types as genai_types

from stock_analysis.prompts import prediction_prompt
MODEL = "gemini-2.5-pro-preview-05-06"

# Format current date for dynamic insertion
current_date = datetime.now().strftime("%B %d, %Y")
formatted_prompt = prediction_prompt.STOCK_PREDICTION_PROMPT.format(current_date=current_date)

stock_prediction_agent = LlmAgent(
    name="stock_prediction_agent",
    model=MODEL,
    planner=BuiltInPlanner(
        thinking_config=genai_types.ThinkingConfig(include_thoughts=True)
    ),
    description=(
        "Prediction Agent - High-precision global stock forecasting specialist with "
        "comprehensive research capabilities. Integrates real-time macro/economic trends, "
        "institutional flows, sector rotation, technical setups, and fundamentals through "
        "extensive web research to predict which stocks across global markets are likely "
        "to outperform. Provides institutional-grade predictions with transparent "
        "multi-pillar analysis backed by current market data from verified sources. "
        "Covers US, European, Asian, Indian, and emerging markets with cross-market "
        "intelligence and real-time flow analysis."
    ),
    instruction=formatted_prompt,
    output_key="stock_prediction_output",
    tools=[google_search],
)



