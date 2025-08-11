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

def read_file(filename: str):
    """Reads the content of a file."""
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    return {"content": content}

crawler_agent = SubAgent(
    name="crawler-agent",
    description="Crawls a given URL, extracts its content and links, and saves the content to a file.",
    prompt="""You are a web crawler. Your job is to do the following:
1. Take a URL as input.
2. Fetch its content and discover any new links.
3. Save the content to a file, and output the new links.""",
    tools=["crawl_page", "save_content"],
)

summarizer_agent = SubAgent(
    name="summarizer-agent",
    description="Summarizes the content of all saved files into a single structured report.",
    prompt="You are a summarizer. Read all the .txt files in the current directory and create a detailed, structured summary in Markdown format.",
    tools=["read_file"],
)

agent_instructions = """
You are an autonomous documentation reader. Your goal is to recursively crawl a documentation website, save the content of each page, and then generate a comprehensive summary.

Here's how you'll do it:
1.  You will be given a starting URL. Create a file named `urls_to_visit.txt` and add the URL to it. Also, create an empty file named `visited_urls.txt`.
2.  As long as `urls_to_visit.txt` is not empty, you must repeat the following steps:
    a.  Read the first URL from `urls_to_visit.txt`.
    b.  Add this URL to `visited_urls.txt`.
    c.  Use the `crawler-agent` to process this URL. The agent will save the page content to a file.
    d.  The `crawler-agent` will return a list of new links. For each new link, check if it's already in `visited_urls.txt`.
    e.  If a link is not in `visited_urls.txt`, add it to `urls_to_visit.txt`.
    f.  Once you've processed all the new links, remove the URL you just crawled from `urls_to_visit.txt`.
3.  After the `urls_to_visit.txt` file is empty, the crawling process is complete.
"""

agent = create_deep_agent(
    tools=[crawl_page, save_content, read_file],
    instructions=agent_instructions,
    subagents=[crawler_agent, summarizer_agent],
    llm="gemini",
).with_config({"recursion_limit": 1000})

