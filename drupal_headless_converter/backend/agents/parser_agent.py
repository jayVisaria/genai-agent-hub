import json
from typing import List

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool
from urllib.parse import urljoin
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

sitemap_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a highly specialized web scraping expert with a deep understanding of XML sitemaps. 
            Your task is to analyze a given URL, locate its sitemap, and extract all the URLs contained within it.

**Instructions:**

1.  Given a base URL, find the sitemap. The most common location is `/sitemap.xml`.
2.  Parse the sitemap and extract every URL.
3.  **Crucially, you must only return URLs that are sub-pages of the initial base URL.** For example, if the base URL is `https://www.drupal.org`, you should only return URLs that begin with `https://www.drupal.org`.
4.  Return the URLs as a list of strings. If you cannot find a sitemap or if there are no relevant URLs, return an empty list.""",
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
            """You are an expert in HTML structure analysis. Your task is to identify the global elements of a website—specifically the header, footer, and navigation menu—from the HTML content of its homepage.

**Instructions:**

1.  Analyze the provided HTML content.
2.  Identify the HTML sections that correspond to the `<header>`, `<footer>`, and `<nav>` elements.
3.  Return these elements as a single, clean JSON object with the keys `header`, `footer`, and `nav`. The values should be the raw HTML content of these elements.
4.  If any of these elements are not found, the value for the corresponding key should be `null`.""",
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
            """You are a content extraction specialist. Your task is to analyze the HTML of a webpage and extract its page-specific content, distinguishing it from the global elements (header, footer, nav).

**Instructions:**

1.  You will be given the full HTML of a webpage and a JSON object containing the global elements.
2.  Your goal is to extract the content that is unique to this page.
3.  Structure the extracted content as a list of JSON objects, where each object has a `type` and a `content` key.
    *   The `type` key should describe the content's nature (e.g., `hero_banner`, `text_block`, `image_gallery`).
    *   The `content` key should contain the corresponding HTML.
4.  **Example**: A hero banner might be represented as `{'type': 'hero_banner', 'content': '<h1>Welcome to our Site</h1>'}`. A simple paragraph might be `{'type': 'text', 'content': '<p>This is a paragraph.</p>'}`.
5.  Return the final output as a single JSON array.""",
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
    content_str = extract_page_specific_content.invoke({"html": html, "global_elements": state["global_elements"]})
    try:
        content_json = json.loads(content_str)
        state["scraped_data"].append({"url": url, "content": content_json})
    except json.JSONDecodeError:
        state["scraped_data"].append({"url": url, "content": {"type": "error", "content": "Failed to parse content as JSON."}})


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



















