"""Progress Tracking Agent: Monitors and logs the user's learning journey."""

from google.adk.agents import Agent
from langchain.tools import tool

from .. import prompt

MODEL = "gemini-2.5-pro-preview-05-06"


@tool
def record_progress(user_id: str, topic: str, performance_data: dict) -> str:
    """Records the user's progress in a structured format."""
    # This is a placeholder for a more sophisticated progress logging mechanism
    print(f"Recording progress for user {user_id} on topic {topic}: {performance_data}")
    return "Progress recorded successfully."


progress_tracking_agent = Agent(
    name="progress_tracking_agent",
    model=MODEL,
    description="Monitors and logs the user's learning journey.",
    instruction=prompt.PROGRESS_TRACKING_PROMPT,
    tools=[record_progress],
)
