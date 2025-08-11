import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from langchain_core.tools import tool
from deepagents import create_deep_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from .prompt import AGENT_INSTRUCTIONS


@tool
def crawl_url(url: str):
    """
    Fetches the text content of a given URL and returns it along with all the hyperlinks found on the page.

    This tool is designed to crawl web pages, extract their textual content, and identify further links for crawling.
    It only processes links that belong to the same domain as the initial URL.

    Args:
        url: The URL of the web page to crawl.

    Returns:
        A dictionary containing the text content of the page and a list of unique links found on the page.
        If the URL is invalid or an error occurs during the request, an error message is returned.
    """
    if not url.startswith('http'):
        return "Error: Invalid URL. Please provide a valid URL starting with http or https."

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        return f"Error: Could not fetch the URL. Reason: {e}"

    soup = BeautifulSoup(response.content, 'html.parser')
    text_content = soup.get_text(separator='\\n', strip=True)
    base_url = url
    links = set()
    for a_tag in soup.find_all('a', href=True):
        link = a_tag['href']
        absolute_link = urljoin(base_url, link)
        parsed_link = urlparse(absolute_link)
        parsed_base = urlparse(base_url)
        if parsed_link.netloc == parsed_base.netloc:
            links.add(parsed_link._replace(fragment="").geturl())

    return {"text_content": text_content, "links": list(links)}

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

doc_reader_agent = create_deep_agent(tools=[crawl_url], instructions=AGENT_INSTRUCTIONS, model=model)
