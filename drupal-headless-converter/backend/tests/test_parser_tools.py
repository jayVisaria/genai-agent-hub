import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from unittest.mock import patch, MagicMock
from backend.agents.parser_agent import scrape_url, find_links

class TestParserTools(unittest.TestCase):

    @patch('requests.get')
    def test_scrape_url(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = "<html><body><h1>Test</h1><p>This is a test.</p></body></html>"
        mock_get.return_value = mock_response

        result = scrape_url("http://example.com")
        self.assertIn("Test", result)
        self.assertIn("This is a test.", result)

    def test_find_links(self):
        html_content = """
        <html><body>
            <a href="/page1">Page 1</a>
            <a href="http://example.com/page2">Page 2</a>
            <a href="/page1">Duplicate</a>
        </body></html>
        """
        links = find_links(html_content, "http://example.com")
        self.assertEqual(len(links), 2)
        self.assertIn("http://example.com/page1", links)
