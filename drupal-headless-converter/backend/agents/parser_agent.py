import json
from typing import List

import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool
from urllib.parse import urljoin
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
    sitemap_urls = find_sitemap.invoke({"url": url})
    initial_state = {"initial_url": url, "urls_to_visit": sitemap_urls, "visited_urls": [], "scraped_data": [], "current_url": "", "global_elements": {}, "final_json": ""}
    final_state = graph.invoke(initial_state)
    return final_state["final_json"]

if __name__ == "__main__":
    print(run_parser("https://www.drupal.org"))













