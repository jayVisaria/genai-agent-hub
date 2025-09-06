import os
import subprocess

from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI

@tool
def read_file(path: str) -> str:
    """Reads the content of a file."""
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

@tool
def write_file(path: str, content: str) -> str:
    """Writes content to a file."""
    try:
        with open(path, "w") as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing to file: {e}"

@tool
def list_files(path: str = ".") -> str:
    """Lists the files in a directory."""
    try:
        return "\n".join(os.listdir(path))
    except Exception as e:
        return f"Error listing files: {e}"

@tool
def make_directory(path: str) -> str:
    """Creates a new directory."""
    try:
        os.makedirs(path, exist_ok=True)
        return f"Successfully created directory {path}"
    except Exception as e:
        return f"Error creating directory: {e}"

@tool
def hugo_new_site(path: str) -> str:
    """Creates a new Hugo site at the specified path."""
    try:
        result = subprocess.run(["hugo", "new", "site", path], capture_output=True, text=True, check=True)
        return result.stdout or result.stderr
    except Exception as e:
        return f"Error running command: {e}"

@tool
def hugo_build(path: str) -> str:
    """Runs the Hugo build process in the specified directory."""
    try:
        result = subprocess.run(["hugo"], cwd=path, capture_output=True, text=True, check=True)
        return result.stdout or result.stderr
    except Exception as e:
        return f"Error running command: {e}"


def create_builder_agent():
    """Creates the Full-Stack SWE-Agent."""
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
    tools = [read_file, write_file, list_files, make_directory, hugo_new_site, hugo_build]
    prompt = """You are a world-class Full-Stack Software Engineering Agent. Your mission is to construct a new, fully functional website from a JSON object that represents the structure and content of a legacy Drupal site.

**Your Core Task:**

You will be given a JSON object with two main keys: `global_elements` and `pages`.
- `global_elements`: Contains the HTML for the site's header, footer, and navigation.
- `pages`: An array of objects, each representing a page with its URL and a list of content components (e.g., hero banners, text blocks).

**Your Workflow:**

1.  **Analyze the JSON**: Begin by thoroughly inspecting the JSON to understand the site's architecture, content hierarchy, and the components used on each page.
2.  **Plan Your Approach**: Formulate a clear, step-by-step plan to build the website. You have the autonomy to choose the best technical stack. A static site generator like Hugo or a modern JavaScript framework like Next.js are excellent choices.
3.  **Directory Structure**: Create a logical and clean directory structure for your project. Use the `hugo_new_site` tool to initialize a new Hugo project.
4.  **Implementation**:
    *   Create all necessary files and directories.
    *   Write the code for the website, integrating the `global_elements` into a base template or layout.
    *   For each page in the `pages` array, create the corresponding file and populate it with the specified content components.
5.  **Verification**: Once the site is built, double-check that all pages are correctly generated and that the content is in its proper place.
6.  **Finalization**: Once you are confident that the website is complete, use the `hugo_build` tool to compile the final static site.

**Example Plan (Framework-Agnostic):**

1.  **Initialization**: Create a root directory for the project.
2.  **Templating**:
    *   Create a base template (`baseof.html`, `index.html`, etc.) that will serve as the main layout for all pages.
    *   Create partials or components for the header, footer, and navigation using the HTML from `global_elements`.
3.  **Content Generation**:
    *   Iterate through the `pages` array in the JSON.
    *   For each page, create a corresponding file (e.g., `/content/about.md`, `/pages/about.js`).
    *   Populate the file with the page's title and content components.
4.  **Styling**: Add basic CSS to ensure the site is visually presentable.
5.  **Build**: Run the `hugo_build` command to generate the final website.

**Error Handling:**

*   If you encounter an error (e.g., a command fails, a file cannot be written), analyze the error message, backtrack if necessary, and try a different approach. Your goal is to be resilient and find a way to complete the task.
"""
    return create_react_agent(llm, tools, prompt=prompt)

