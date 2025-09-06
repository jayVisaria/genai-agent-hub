import os
import subprocess

from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from . import prompts

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
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
    tools = [read_file, write_file, list_files, make_directory, run_bash]
    return create_react_agent(llm, tools, prompt=prompts.BUILDER_PROMPT)


