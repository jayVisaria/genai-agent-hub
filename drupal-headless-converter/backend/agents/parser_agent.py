import json
import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic

@tool
def scrape_url(url: str) -> str:
    """Scrapes the content of a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.get_text()
    except requests.exceptions.RequestException as e:
        return f"Error scraping URL: {e}"

@tool
def find_links(url: str) -> list[str]:
    """Finds all the links on a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        return [a["href"] for a in soup.find_all("a", href=True)]
    except requests.exceptions.RequestException as e:
        return f"Error finding links: {e}"

def create_parser_agent():
    """Creates the Drupal content intelligence agent."""
    llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")
    tools = [scrape_url, find_links]
    prompt = """You are a Drupal Content Intelligence Agent.

Your task is to crawl a Drupal website and generate a JSON representation of its content and structure.

Here's how you'll do it:
1. Start with a given URL.
2. Scrape the content of the URL.
3. Find all the links on the page.
4. For each link, repeat the process.
5. Keep track of visited URLs to avoid infinite loops.
6. Once you have crawled the entire site, generate a JSON object that represents the site structure and content.

The final JSON should be a list of objects, where each object has a "url" and a "content" key."""

    agent_executor = create_react_agent(llm, tools, prompt=prompt)
    return agent_executor
