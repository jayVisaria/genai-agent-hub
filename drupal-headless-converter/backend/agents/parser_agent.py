import json
from typing import List

import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from typing import TypedDict


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


class ParserState(TypedDict):
    initial_url: str
    urls_to_visit: List[str]
    visited_urls: List[str]
    scraped_data: List[dict]
    current_url: str


def crawl_node(state: ParserState):
    if not state["urls_to_visit"]:
        return
    url = state["urls_to_visit"].pop(0)
    state["current_url"] = url
    state["visited_urls"].append(url)
    content = scrape_url.invoke({"url": url})
    state["scraped_data"].append({"url": url, "content": content})
    links = find_links.invoke({"url": url})
    for link in links:
        if link not in state["visited_urls"] and link not in state["urls_to_visit"]:
            state["urls_to_visit"].append(link)


def should_continue_node(state: ParserState):
    if not state["urls_to_visit"]:
        return "end"
    else:
        return "continue"


def create_parser_graph():
    workflow = StateGraph(ParserState)
    workflow.add_node("crawl", crawl_node)
    workflow.add_conditional_edges(
        "crawl",
        should_continue_node,
        {
            "continue": "crawl",
            "end": END,
        },
    )
    workflow.add_edge(START, "crawl")
    return workflow.compile()

def run_parser(url: str):
    graph = create_parser_graph()
    initial_state = {"initial_url": url, "urls_to_visit": [url], "visited_urls": [], "scraped_data": [], "current_url": ""}
    final_state = graph.invoke(initial_state)
    return json.dumps(final_state["scraped_data"], indent=2)

if __name__ == "__main__":
    print(run_parser("https://www.drupal.org"))


