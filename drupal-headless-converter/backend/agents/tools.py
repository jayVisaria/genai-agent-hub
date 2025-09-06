import os
from langchain_core.tools import tool

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




