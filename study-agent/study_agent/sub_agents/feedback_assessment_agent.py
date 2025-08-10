"""Feedback and Assessment Agent: Evaluates user responses and provides feedback."""

from google.adk.agents import Agent
from google.adk.tools import Tool

from .. import prompt

MODEL = "gemini-2.5-pro-preview-05-06"


def score_answer(answer: str, correct_answer: str) -> dict:
    """Scores the user's answer and provides feedback."""
    # This is a placeholder for a more sophisticated scoring logic
    score = 1 if answer.lower() == correct_answer.lower() else 0
    feedback = "Correct!" if score == 1 else "Incorrect. Please try again."
    return {"score": score, "feedback": feedback}

score_answer_tool = Tool(
    name="score_answer",
    description="Scores the user's answer and provides feedback.",
    func=score_answer,
)

feedback_assessment_agent = Agent(
    name="feedback_assessment_agent",
    model=MODEL,
    description="Evaluates user responses to quizzes and exercises.",
    instruction=prompt.FEEDBACK_ASSESSMENT_PROMPT,
    tools=[score_answer_tool],
)

