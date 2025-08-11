# Study and Learn Agent

## Overview

The Study and Learn Agent is a comprehensive AI-powered educational system that provides personalized and interactive learning experiences. The agent acts as an expert study coordinator and interactive learning companion, integrating all essential learning capabilities into a streamlined single-agent architecture.

## Agent Details

| Attribute | Detail |
|---|---|
| Interaction Type | Conversational |
| Complexity | Medium |
| Agent Type | Single Agent |
| Components | Integrated learning capabilities |
| Vertical | Education |

### Agent Architecture

The Study and Learn Agent uses a unified single-agent architecture that integrates all learning capabilities:

- **Study Coordinator**: A comprehensive agent that handles all aspects of the learning process, including content retrieval, personalization, interaction, assessment, and progress tracking.

The agent leverages Google Search for content retrieval and utilizes built-in memory capabilities for personalization and progress tracking.

## Tools and APIs Used

The Study and Learn Agent leverages the following tools and capabilities:

| Tool/Capability | Description |
|-----------------|-------------|
| Google Search   | Retrieves relevant educational content and information from the web |
| Agent Memory    | Stores and retrieves user learning data for personalization and progress tracking |
| Natural Language Processing | Evaluates user responses and provides intelligent feedback |

## Core Capabilities

The single agent integrates all essential learning functionalities:

- **Learning Plan Generation**: Creates structured, phase-based learning roadmaps with clear milestones
- **Content Retrieval and Synthesis**: Finds and synthesizes high-quality educational content from the web
- **Personalization and Adaptation**: Tailors the learning experience to individual user needs and skill levels
- **Interactive and Socratic Dialogue**: Fosters critical thinking through strategic questioning and conversation
- **Feedback and Assessment**: Evaluates understanding and provides constructive, actionable feedback
- **Progress Tracking and Reporting**: Monitors learning journeys and maintains comprehensive learning history

## Features

- **Unified Learning Experience**: Single agent architecture that seamlessly integrates all learning capabilities
- **Personalized Learning**: Adapts to individual user needs, learning styles, and skill levels
- **Interactive Socratic Method**: Engages users with strategic questioning and guided discovery
- **Comprehensive Content Retrieval**: Searches and synthesizes information from web sources
- **Intelligent Assessment**: Provides constructive feedback and evaluates understanding
- **Progress Tracking**: Monitors and maintains detailed learning history across sessions
- **Structured Learning Plans**: Creates phase-based roadmaps with clear milestones
- **Cognitive Load Management**: Breaks complex topics into digestible, well-organized sections

## Setup and Installation

### Prerequisites

- Python 3.12+
- Poetry for dependency management and packaging
  - See the official [Poetry website](https://python-poetry.org/docs/) for more information. To install Poetry run:
  ```bash
  pip install poetry
  ```
- Google Cloud Project with the following roles assigned:
  - Vertex AI User
  - Storage Admin
  - Service Usage Consumer
  - Logs Viewer

Once you have created your project, [install the Google Cloud SDK](https://cloud.google.com/sdk/docs/install). Then run the following command to authenticate:
```bash
gcloud auth login
```

You also need to enable certain APIs. Run the following command to enable:
```bash
gcloud services enable aiplatform.googleapis.com
```

## Agent Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd study-agent
   ```

2. Install the dependencies:
   ```bash
   poetry install
   ```

3. Configure settings:
   - Set the following environment variables. You can set them in your `.env` file (modify and rename `.env.example` file to `.env`) or set them directly in your shell. For example:
   ```bash
   export GOOGLE_GENAI_USE_VERTEXAI=1
   export GOOGLE_CLOUD_PROJECT=my-project
   export GOOGLE_CLOUD_LOCATION=my-region
   ```

## Usage

Run the agent:
```bash
poetry run adk web
```

## Sample Workflow

This example demonstrates how a user request to "Teach me about photosynthesis" is processed through the unified agent system.

1. **User Request**: The user asks the Study and Learn Agent to explain photosynthesis.

2. **Goal Setting and Assessment**: The agent begins by understanding the user's learning objectives and assessing their current knowledge level through strategic questions.

3. **Learning Plan Creation**: Based on the assessment, the agent creates a structured, phase-based learning plan:
   - 🔹 **Phase 1**: Basic concepts and terminology
   - 🔸 **Phase 2**: Detailed process and chemical reactions  
   - 🔹 **Phase 3**: Real-world applications and significance

4. **Content Retrieval and Synthesis**: The agent uses Google Search to find current, accurate information about photosynthesis and synthesizes it into clear, digestible explanations tailored to the user's level.

5. **Interactive Learning**: The agent presents information using Socratic questioning and interactive prompts:
   - "Before I explain photosynthesis, what do you think plants need to make their own food?"
   - Provides scaffolded explanations with visual formatting and clear connections

6. **Knowledge Checks**: Throughout the learning process, the agent administers quick assessments to verify understanding and provides immediate, constructive feedback.

7. **Progress Tracking**: The agent continuously monitors the user's progress, noting topics covered, comprehension levels, and learning patterns for future sessions.

8. **Session Summary**: At the end, the agent provides a comprehensive summary of what was learned and suggests next steps for continued learning.
