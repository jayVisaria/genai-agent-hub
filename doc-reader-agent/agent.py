import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from deepagents import create_deep_agent, SubAgent

def crawl_page(url: str):
    """Fetches and parses a web page, returning its content and any newly discovered links."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extract text content
        text_content = soup.get_text(separator="\\n", strip=True)
        
        # Discover new links
        links = {urljoin(url, a["href"]) for a in soup.find_all("a", href=True)}
        
        return {"content": text_content, "links": list(links)}
    except requests.RequestException as e:
        return {"error": str(e)}

def save_content(filename: str, content: str):
    """Saves content to a file in the agent's file system."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return {"status": f"Content saved to {filename}"}

crawler_agent = SubAgent(
    name="crawler-agent",
    description="Crawls a given URL, extracts its content and links, and saves the content to a file.",
    prompt="You are a web crawler. Your job is to fetch content from a URL, save it, and report back any new links.",
    tools=["crawl_page", "save_content"],
)

summarizer_agent = SubAgent(
    name="summarizer-agent",
    description="Summarizes the content of all saved files into a single structured report.",
    prompt="You are a summarizer. Read all the .txt files in the current directory and create a detailed, structured summary in Markdown format.",
)

agent_instructions = """
You are an autonomous documentation reader. Your goal is to recursively crawl a documentation website,
save the content of each page, and then generate a comprehensive summary.

1.  Start with the initial URL provided by the user.
2.  Use the crawler-agent to fetch the content and discover new links.
3.  Save the content of each page to a unique .txt file.
4.  Keep track of visited URLs to avoid duplicate work.
5.  Maintain a queue of URLs to visit.
6.  Once all pages have been crawled, use the summarizer-agent to create a final report.
"""

agent = create_deep_agent(
    tools=[crawl_page, save_content],
    instructions=agent_instructions,
    subagents=[crawler_agent, summarizer_agent],
    llm="gemini",
).with_config({"recursion_limit": 1000})
