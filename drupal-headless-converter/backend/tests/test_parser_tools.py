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
        mock_response.content = "<html><body><h1>Test</h1><p>This is a test.</p></body></html>"
        mock_get.return_value = mock_response

        result = scrape_url.invoke({"url": "http://example.com"})
        self.assertIn("Test", result)
        self.assertIn("This is a test.", result)

    @patch('requests.get')
    def test_find_links(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = '<html><body><a href="/page1">1</a><a href="http://test.com/page2">2</a></body></html>'
        mock_get.return_value = mock_response
        links = find_links.invoke({"url": "http://example.com"})
        self.assertEqual(links, ["/page1", "http://test.com/page2"])

