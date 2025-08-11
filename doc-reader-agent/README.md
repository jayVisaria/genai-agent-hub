# Documentation Reader Agent

This agent is designed to autonomously read and summarize documentation from a given URL. It recursively crawls all pages under the provided URL, stores the content, and generates a structured summary.

## How it Works

The agent starts with a root URL and uses a crawling tool to explore all linked pages within the same domain. The content of each page is saved to a virtual file system. Once the crawling is complete, the agent uses the Gemini model to synthesize all the gathered information into a comprehensive, structured summary in Markdown format.

This project uses [`deepagents`](https://github.com/hwchase17/deepagents) to orchestrate the agent's behavior and manage its state.

## Setup

### 1. Install Dependencies

To install the required Python packages, run the following command in your terminal:

```bash
pip install -e .
```

### 2. Set Up Environment Variables

You will need a Google API key to use the Gemini model. Export your key as an environment variable:

```bash
export GOOGLE_API_KEY="your-google-api-key"
```

## Usage

To run the agent, you can use it as a library or run it from a Python script. Here is an example of how to invoke the agent with a documentation URL:

```python
from doc_reader_agent.agent import doc_reader_agent

result = doc_reader_agent.invoke({"messages": [{"role": "user", "content": "Please crawl and summarize the documentation at https://docs.langgraph.dev"}]})

print(result['messages'][-1].content)
