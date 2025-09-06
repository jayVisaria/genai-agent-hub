import json
from typing import List
import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool
from urllib.parse import urljoin, urlparse
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langchain_anthropic import ChatAnthropic
from . import prompts

llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")

@tool
def find_sitemap(url: str) -> List[str]:
    """Finds the sitemap of a given URL and returns a list of all URLs in the sitemap."""
    return ["https://www.drupal.org", "https://www.drupal.org/about"]

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
def extract_page_specific_content(url: str, global_elements: dict) -> str:
    """Extracts the page-specific content from a given URL, excluding the global elements."""
    page_content = scrape_url.invoke(url)
    prompt = prompts.EXTRACT_PAGE_SPECIFIC_CONTENT_PROMPT.format(page_content=page_content, global_elements=global_elements)
    response = llm.invoke(prompt)
    return response.content

class ParserState(TypedDict):
    initial_url: str
    urls_to_visit: List[str]
    visited_urls: List[str]
    scraped_data: List[dict]
    current_url: str
    global_elements: dict
    final_json: str

def find_global_elements_node(state: ParserState):
    """Finds the global elements of the website."""
    initial_url = state["initial_url"]
    homepage_content = scrape_url.invoke(initial_url)
    prompt = prompts.FIND_GLOBAL_ELEMENTS_PROMPT.format(homepage_content=homepage_content)
    response = llm.invoke(prompt)
    global_elements = json.loads(response.content)
    state["global_elements"] = global_elements

def synthesize_json_node(state: ParserState):
    """Synthesizes the final JSON object."""
    scraped_data = state["scraped_data"]
    global_elements = state["global_elements"]
    prompt = prompts.SYNTHESIZE_JSON_PROMPT.format(scraped_data=scraped_data, global_elements=global_elements)
    response = llm.invoke(prompt)
    final_json = json.loads(response.content)
    state["final_json"] = final_json

def crawl_node(state: ParserState):
    if not state["urls_to_visit"]:
        return
    url = state["urls_to_visit"].pop(0)
    state["current_url"] = url
    state["visited_urls"].append(url)
    content = extract_page_specific_content.invoke({"url": url, "global_elements": state["global_elements"]})
    state["scraped_data"].append({"url": url, "content": content})


def should_continue_node(state: ParserState):
    if not state["urls_to_visit"]:
        return "end"
    else:
        return "continue"

def create_parser_graph():
    workflow = StateGraph(ParserState)
    workflow.add_node("find_global_elements", find_global_elements_node)
    workflow.add_node("crawl", crawl_node)
    workflow.add_node("synthesize_json", synthesize_json_node)
    workflow.add_conditional_edges(
        "crawl",
        should_continue_node,
        {
            "continue": "crawl",
            "end": "synthesize_json",
        },
    )
    workflow.add_edge(START, "find_global_elements")
    workflow.add_edge("find_global_elements", "crawl")
    workflow.add_edge("synthesize_json", END)
    return workflow.compile()

def run_parser(url: str):
    graph = create_parser_graph()
    sitemap_urls = find_sitemap.invoke(url)
    initial_state = {"initial_url": url, "urls_to_visit": sitemap_urls, "visited_urls": [], "scraped_data": [], "current_url": "", "global_elements": {}, "final_json": ""}
    final_state = graph.invoke(initial_state)
    return final_state["final_json"]

if __name__ == "__main__":
    print(run_parser("https://www.drupal.org"))

