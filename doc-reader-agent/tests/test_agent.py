import unittest
from unittest.mock import patch, MagicMock

from doc_reader_agent.agent import crawl_url


class TestCrawlUrl(unittest.TestCase):

    @patch('requests.get')
    def test_crawl_url_success(self, mock_get):
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'<html><head><title>Test Page</title></head><body><p>Hello World!</p><a href="/page2">Page 2</a><a href="https://external.com">External</a></body></html>'
        mock_get.return_value = mock_response

        # Act
        result = crawl_url('http://example.com')

        # Assert
        self.assertIn('text_content', result)
        self.assertIn('Hello World!', result['text_content'])
        self.assertIn('links', result)
        self.assertEqual(len(result['links']), 1)
        self.assertIn('http://example.com/page2', result['links'])
        self.assertNotIn('https://external.com', result['links'])

    @patch('requests.get')
    def test_crawl_url_request_exception(self, mock_get):
        # Arrange
        mock_get.side_effect = requests.exceptions.RequestException("Test error")

        # Act
        result = crawl_url('http://example.com')

        # Assert
        self.assertIn('Error: Could not fetch the URL.', result)

    def test_crawl_url_invalid_url(self):
        # Act
        result = crawl_url('invalid-url')

        # Assert
        self.assertIn('Error: Invalid URL.', result)

    @patch('requests.get')
    def test_crawl_url_no_links(self, mock_get):
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'<html><body><p>No links here.</p></body></html>'
        mock_get.return_value = mock_response

        # Act
