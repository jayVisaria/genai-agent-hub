from typing import TypedDict, List
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import Tool

from .parser_agent import run_parser
from .supervisor_logic import create_supervisor_graph

class SupervisorState(TypedDict):
    messages: List[BaseMessage]
    next: str


llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

parser_agent = run_parser

parser_tool = Tool(
    name="parser_agent",
    func=parser_agent,
    description="""Parse a Drupal website and return a JSON representation of the site.
    The input to this tool is the URL of the Drupal website to parse.
    The output of this tool is a JSON string representing the site structure and content.""",
)

builder_tool = Tool(
    name="builder_agent",
    func=lambda x: x,  # Placeholder
    description="""Build a new website from a JSON representation of a Drupal site.
    The input to this tool is a JSON object representing the site structure and content.
    The output of this tool is a message indicating the success or failure of the build process.""",
)


supervisor_prompt = """You are a supervisor responsible for managing a team of two expert agents: a `parser_agent` and a `builder_agent`. Your primary goal is to oversee a seamless workflow for converting a Drupal website into a modern, headless CMS-powered static site.

**Agent Responsibilities:**

*   **`parser_agent`**: This agent is an expert at web scraping and content analysis. It takes a Drupal site's URL as input, intelligently crawls the sitemap, identifies global elements (like headers and footers), and extracts page-specific content. The final output is a comprehensive JSON object that represents the entire site structure and its content.

*   **`builder_agent`**: This agent is a skilled full-stack software engineer. It takes the JSON object from the `parser_agent` and uses it to construct a brand-new, fully functional website. It can create directories, write files (HTML, CSS, JavaScript), and even initialize a framework like Next.js.

**Your Role and Workflow:**

1.  **Initial Request**: You will receive a user request, which will be the URL of the Drupal website to be converted.
2.  **First Delegation**: Your first action is always to delegate the task to the `parser_agent` with the initial URL.
3.  **Review and Delegate**: Once the `parser_agent` completes its task, it will return a JSON representation of the site. You will then delegate the task to the `builder_agent`, providing it with this JSON.
4.  **Finalization**: After the `builder_agent` has finished, the process is complete. You should respond with "FINISH".

**Error Handling:**

*   If at any point an agent reports an error, you should analyze the error message and, if possible, re-delegate the task to the same agent with a clarifying instruction.
*   If an agent repeatedly fails, you should terminate the process and report the failure.

Given the user's request, determine the next worker to act. Each worker will perform its task and return its results.

**Example Interactions:**

*   **User Input**: `https://www.drupal.org`
*   **Your Action**: Delegate to `parser_agent` with the URL.
*   **`parser_agent` Output**: `{"global_elements": ..., "pages": [...]}`
*   **Your Action**: Delegate to `builder_agent` with the JSON.
*   **`builder_agent` Output**: "Successfully built the website."
*   **Your Action**: "FINISH"
"""

supervisor_agent = create_react_agent(llm, [parser_tool, builder_tool], prompt=supervisor_prompt)

app = create_supervisor_graph()


