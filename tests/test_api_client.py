import json
import os
import unittest
from unittest.mock import MagicMock, patch

from src.api_client import APIException, ApiClient


class TestApiClient(unittest.TestCase):
    @patch("src.api_client.requests.get")
    def test_get_raises_exception_on_http_error(self, mock_get):
        mock_get.return_value = MagicMock(status_code=500)
        with self.assertRaises(APIException) as exception:
            ApiClient().get("/api/stock/products/by-barcode/12345")
            self.assertIsNotNone(exception.status_code)

    @patch("src.api_client.requests.post")
    def test_post_raises_exception_on_http_error(self, mock_post):
        mock_post.return_value = MagicMock(status_code=500)
        with self.assertRaises(APIException) as exception:
            ApiClient().post("/api/stock/products/by-barcode/12345", data={})
            self.assertIsNotNone(exception.status_code)

    @patch("src.api_client.requests.get")
    def test_correct_base_url_through_env(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200, response=json.dumps({}))
        URL = "http://localhost:8080"
        os.environ["API_URL"] = URL
        ApiClient().get("/api/stock/products/by-barcode/12345")
        mock_get.assert_called()
        self.assertIn(URL, mock_get.call_args.kwargs["url"])

    @patch("src.api_client.requests.get")
    def test_correct_base_url_through_param(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200, response=json.dumps({}))
        URL = "http://localhost:8080"
        ApiClient(api_url=URL).get("/api/stock/products/by-barcode/12345")
        mock_get.assert_called()
        self.assertIn(URL, mock_get.call_args.kwargs["url"])


if __name__ == "__main__":
    unittest.main()
