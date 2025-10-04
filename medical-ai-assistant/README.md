# Medical AI Assistant

The Medical AI Assistant is a multi-modal AI agent designed to assist with medical inquiries. It can process text, images (including DICOM files), and documents (PDFs) to provide information and analysis. The assistant is built using FastAPI for the backend and LangGraph for the agentic workflow.

## Features

- **Multi-modal Input:** The assistant can handle various types of input, including text, images (JPEG, PNG), DICOM files, and PDFs.
- **Specialized Agents:** The system uses a supervisor agent to route tasks to specialized agents for:
  - **Image Analysis:** Analyzes medical images and provides a report.
  - **Symptom Triage:** Triages patient symptoms and provides a preliminary assessment.
  - **Medical Knowledge Retrieval:** Retrieves information from a medical knowledge base.
- **FastAPI Backend:** The application is built with FastAPI, providing a robust and efficient API for handling requests.
- **LangGraph Workflow:** The agentic workflow is powered by LangGraph, allowing for a flexible and scalable multi-agent system.

## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repo/medical-ai-assistant.git
   cd medical-ai-assistant
   ```

2. **Install dependencies:**
   The project uses Poetry for dependency management. Make sure you have Poetry installed.
   ```bash
   poetry install
   ```

3. **Run the application:**
   ```bash
   poetry run uvicorn medical_ai_assistant.main:app --reload
   ```

The application will be available at `http://127.0.0.1:8000`.

## Disclaimer

**This Medical AI Assistant is for informational purposes only and should not be used for medical advice, diagnosis, or treatment.** The information provided by the assistant is not a substitute for professional medical advice. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. Never disregard professional medical advice or delay in seeking it because of something you have read or received from this application.

The developers of this application are not responsible for any actions or decisions made based on the information provided by the assistant. Use of this application is at your own risk.

---
