"""Workflow agent for the Study and Learn Agent system."""
from google.adk.agents import ParallelAgent, SequentialAgent

from .sub_agents.content_retrieval_agent import content_retrieval_agent
from .sub_agents.feedback_assessment_agent import feedback_assessment_agent
from .sub_agents.interaction_agent import interaction_agent
from .sub_agents.learning_plan_agent import learning_plan_agent
from .sub_agents.personalization_agent import personalization_agent
from .sub_agents.progress_tracking_agent import progress_tracking_agent

parallel_task_agent = ParallelAgent(
    name="parallel_task_agent",
    sub_agents=[
        content_retrieval_agent,
        personalization_agent,
    ],
)

workflow_agent = SequentialAgent(
    name="workflow_agent",
    sub_agents=[
        learning_plan_agent,
        parallel_task_agent,
        interaction_agent,
        feedback_assessment_agent,
        progress_tracking_agent,
    ],
)

root_agent = workflow_agent


