import json
import unittest
from unittest.mock import MagicMock, patch

from src.api_client import APIException, ApiClient


class TestApiClient(unittest.TestCase):
    @patch("src.api_client.os.getenv", return_value="something")
    @patch("src.api_client.requests.get")
    def test_get_raises_exception_on_http_error(self, mock_get, mock_getenv):
        mock_get.return_value = MagicMock(status_code=500)
        with self.assertRaises(APIException) as context:
            ApiClient().get("/api/stock/products/by-barcode/12345")
        self.assertIsNotNone(context.exception.status_code)

    @patch("src.api_client.os.getenv", return_value="something")
    @patch("src.api_client.requests.post")
    def test_post_raises_exception_on_http_error(self, mock_post, mock_getenv):
        mock_post.return_value = MagicMock(status_code=500)
        with self.assertRaises(APIException) as context:
            ApiClient().post("/api/stock/products/by-barcode/12345", data={})
        self.assertIsNotNone(context.exception.status_code)

    @patch("src.api_client.requests.get")
    @patch("src.api_client.os.getenv")
    def test_correct_base_url_through_env(self, mock_getenv, mock_get):
        mock_get.return_value = MagicMock(status_code=200, response=json.dumps({}))
        URL = "http://localhost:8080"
        mock_getenv.return_value = URL
        ApiClient().get("/api/stock/products/by-barcode/12345")
        mock_get.assert_called()
        self.assertIn(URL, mock_get.call_args.kwargs["url"])

    @patch("src.api_client.os.getenv", return_value="something")
    @patch("src.api_client.requests.get")
    def test_correct_base_url_through_param(self, mock_get, mock_getenv):
        mock_get.return_value = MagicMock(status_code=200, response=json.dumps({}))
        URL = "http://localhost:8080"
        ApiClient(api_url=URL).get("/api/stock/products/by-barcode/12345")
        mock_get.assert_called()
        self.assertIn(URL, mock_get.call_args.kwargs["url"])

    @patch("src.api_client.os.getenv", return_value=None)
    def test_init_raises_on_missing_values(self, mock_getenv):
        with self.assertRaises(ValueError):
            ApiClient()


if __name__ == "__main__":
    unittest.main()
