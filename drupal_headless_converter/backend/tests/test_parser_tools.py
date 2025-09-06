import unittest
from unittest.mock import patch, MagicMock
from drupal_headless_converter.backend.agents.parser_agent import scrape_url

class TestParserTools(unittest.TestCase):

    def setUp(self):
        self.patcher = patch('drupal_headless_converter.backend.agents.parser_agent.ChatGoogleGenerativeAI')
        self.mock_llm = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    @patch('requests.get')
    def test_scrape_url(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = "<html><body><h1>Test</h1><p>This is a test.</p></body></html>"
        mock_get.return_value = mock_response

        result = scrape_url.invoke({"url": "http://example.com"})
        self.assertIn("Test", result)
        self.assertIn("This is a test.", result)



