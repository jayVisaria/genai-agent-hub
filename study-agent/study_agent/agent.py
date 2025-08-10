"""Study and Learn Coordinator: Main agent orchestrating personalized learning experiences"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool, google_search

from . import prompt

MODEL = "gemini-2.5-pro"


def score_answer(answer: str, correct_answer: str) -> dict:
    """Scores the user's answer and provides feedback."""
    # This is a placeholder for a more sophisticated scoring logic
    score = 1 if answer.lower() == correct_answer.lower() else 0
    feedback = "Correct!" if score == 1 else "Incorrect. Please try again."
    return {"score": score, "feedback": feedback}


def record_progress(user_id: str, topic: str, performance_data: dict) -> str:
    """Records the user's progress in a structured format."""
    # This is a placeholder for a more sophisticated progress logging mechanism
    print(f"Recording progress for user {user_id} on topic {topic}: {performance_data}")
    return "Progress recorded successfully."


study_coordinator = Agent(
    name="study_coordinator",
    model=MODEL,
    description=(
        "A specialized study coordinator that orchestrates a personalized and "
        "interactive learning experience."
    ),
    instruction=prompt.STUDY_COORDINATOR_PROMPT,
    memory=True,
    tools=[
        google_search,
        FunctionTool(func=score_answer),
        FunctionTool(func=record_progress),
    ],
)

root_agent = study_coordinator

