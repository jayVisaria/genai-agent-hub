import json
from typing import List

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool
from urllib.parse import urljoin
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")

sitemap_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert at finding sitemaps for websites. "
            "Given a URL, find the sitemap and return a list of all the URLs in it. "
            "Only return URLs that are sub-pages of the initial URL. "
            "For example, if the initial URL is https://www.drupal.org, "
            "only return URLs that start with https://www.drupal.org.",
        ),
        ("user", "{url}"),
    ]
)

def find_sitemap_urls(url: str) -> List[str]:
    try:
        sitemap_url = urljoin(url, "/sitemap.xml")
        response = requests.get(sitemap_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "xml")
        urls = [loc.text for loc in soup.find_all("loc")]
        return [u for u in urls if u.startswith(url)]
    except requests.exceptions.RequestException:
        return []

find_sitemap = sitemap_prompt | llm | StrOutputParser()

global_elements_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert at identifying global elements in a website's HTML. "
            "Given the HTML content of a homepage, identify the header, footer, and navigation elements. "
            "Return these elements as a JSON object with keys 'header', 'footer', and 'nav'.",
        ),
        ("user", "{html}"),
    ]
)

find_global_elements = global_elements_prompt | llm | StrOutputParser()

class ParserState(TypedDict):
    initial_url: str
    urls_to_visit: List[str]
    visited_urls: List[str]
    scraped_data: List[dict]
    current_url: str
    global_elements: dict
    final_json: str

def find_global_elements_node(state: ParserState):
    html = scrape_url.invoke(state["initial_url"])
    global_elements = find_global_elements.invoke({"html": html})
    state["global_elements"] = json.loads(global_elements)

page_specific_content_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert at extracting page-specific content from a website's HTML. "
            "Given the HTML content of a page and the global elements (header, footer, nav), "
            "extract the content that is unique to the page. "
            "Return the content as a list of JSON objects, where each object has a 'type' and 'content' key. "
            "For example, a hero banner could be {'type': 'hero_banner', 'content': '<h1>Welcome</h1>'}. "
            "A text block could be {'type': 'text', 'content': '<p>Some text.</p>'}.",
        ),
        ("user", "HTML:\n{html}\n\nGlobal Elements:\n{global_elements}"),
    ]
)

extract_page_specific_content = page_specific_content_prompt | llm | StrOutputParser()

def synthesize_json_node(state: ParserState):
    final_json = {
        "global_elements": state["global_elements"],
        "pages": state["scraped_data"],
    }
    state["final_json"] = json.dumps(final_json, indent=2)

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

def crawl_node(state: ParserState):
    if not state["urls_to_visit"]:
        return
    url = state["urls_to_visit"].pop(0)
    state["current_url"] = url
    state["visited_urls"].append(url)
    html = scrape_url.invoke(url)
    content = extract_page_specific_content.invoke({"html": html, "global_elements": state["global_elements"]})
    state["scraped_data"].append({"url": url, "content": json.loads(content)})

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
    sitemap_urls = find_sitemap_urls(url)
    initial_state = {"initial_url": url, "urls_to_visit": sitemap_urls, "visited_urls": [], "scraped_data": [], "current_url": "", "global_elements": {}, "final_json": ""}
    final_state = graph.invoke(initial_state)
    return final_state["final_json"]

if __name__ == "__main__":
    print(run_parser("https://www.drupal.org"))
