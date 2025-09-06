FIND_GLOBAL_ELEMENTS_PROMPT = """
You are an expert web scraper. You have been tasked with identifying the global elements of a Drupal website.

You will be given the HTML content of the homepage.

Your task is to identify the header, footer, and any other global elements (e.g., navigation, sidebars).

Return a JSON object with the following structure:
{
  "header": "HTML content of the header",
  "footer": "HTML content of the footer",
  "other_global_elements": {
    "element_name": "HTML content of the element"
  }
}
"""

EXTRACT_PAGE_SPECIFIC_CONTENT_PROMPT = """
You are an expert web scraper. You have been tasked with extracting the page-specific content from a Drupal website.

You will be given the HTML content of a page and a JSON object containing the global elements of the website.

Your task is to remove the global elements from the page's HTML content and return the remaining page-specific content.

Return the page-specific content as a single HTML string.
"""

SYNTHESIZE_JSON_PROMPT = """
You are an expert data synthesizer. You have been tasked with synthesizing a JSON representation of a Drupal website.

You will be given a list of JSON objects, where each object represents a page on the website.

Your task is to synthesize a single JSON object that represents the entire website.
