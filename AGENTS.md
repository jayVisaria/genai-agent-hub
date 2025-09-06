<general_rules>
- When creating new functions or agents, first search the existing codebase to see if a similar implementation already exists.
- Follow the existing code style and conventions.
- Prompts are a key part of this repository. When creating or editing prompts, ensure they are clear, concise, and well-structured.
- No specific linting or formatting scripts are currently in place.
</general_rules>
<repository_structure>
The repository is a collection of AI agent prototypes. Each agent is contained within its own directory and functions as a standalone project.

- `stock-analysis-agent/`: A multi-agent system for financial analysis. It has a hierarchical architecture with a Coordinator, an Orchestrator, and several specialized sub-agents (e.g., Fundamental, Technical, Sentiment).
- `study-agent/`: A single-agent system designed for personalized and interactive learning.

Each agent directory contains:
- `pyproject.toml`: Defines the project's dependencies and metadata.
- `README.md`: Provides specific instructions for that agent.
- A source directory (e.g., `stock_analysis/`, `study_agent/`) containing the agent's implementation.
</repository_structure>
<dependencies_and_installation>
The following are required for all agents in this repository:

- Python 3.12+
- Poetry for dependency management. Install it with `pip install poetry`.
- A Google Cloud Project with the following roles:
  - Vertex AI User
  - Storage Admin
  - Service Usage Consumer
  - Logs Viewer
- The Google Cloud SDK. Authenticate by running `gcloud auth login`.
- Enable the AI Platform API: `gcloud services enable aiplatform.googleapis.com`.

To install dependencies for a specific agent, navigate to its directory and run:
`poetry install`

Set the following environment variables:
- `GOOGLE_GENAI_USE_VERTEXAI=1`
- `GOOGLE_CLOUD_PROJECT=<your-gcp-project-id>`
- `GOOGLE_CLOUD_LOCATION=<your-gcp-region>`
</dependencies_and_installation>
<testing_instructions>
There are currently no specific testing frameworks or instructions for this repository.
</testing_instructions>
<pull_request_formatting>
