import os
import subprocess

from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic

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
def run_bash(command: str) -> str:
    """Runs a bash command."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout or result.stderr
    except Exception as e:
        return f"Error running command: {e}"


def create_builder_agent():
    """Creates the Full-Stack SWE-Agent."""
    llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")
    tools = [read_file, write_file, list_files, make_directory, run_bash]
    prompt = """You are a Full-Stack SWE-Agent.

Your task is to build a new website based on a JSON representation of a Drupal site.

Here's how you'll do it:
1. You will be given a JSON object representing the site structure and content.
2. Analyze the JSON to understand the site's hierarchy and content.
3. Create a new directory for the website.
4. Create a plan to build the website based on the JSON data.
5. Create the necessary files and directories.
6. Write the code for the website, using the global elements and page-specific components from the JSON data.
7. Verify that the website is working as expected.

Example Plan for Hugo:
1. Create root project folder.
2. Run hugo new site . to initialize.
3. Create base template in /layouts/_default/baseof.html.
4. Create partials for header (/layouts/partials/header.html) and footer (/layouts/partials/footer.html) using the global_elements HTML.
5. Iterate through the pages array in the JSON.
6. For each page, create a corresponding markdown file in /content/. For /about, create /content/about.md.
7. Populate the markdown front matter with the title.
8. For each component in the page, write its content into the markdown file. Potentially create Hugo shortcodes for complex component types like hero_banner.
9. Write basic CSS to style the site.
"""
    return create_react_agent(llm, tools, prompt)


