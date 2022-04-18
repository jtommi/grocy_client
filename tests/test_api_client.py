import unittest
from unittest.mock import patch

from requests.models import Response
from src.api_client import ApiClient


def mocked_request_get_failed(*args, **kwargs):
    response = Response()
    response.status_code = 500
    return response


class TestApiClient(unittest.TestCase):
    @patch("src.api_client.requests.get", side_effect=mocked_request_get_failed)
    def test_client_raises_exception(self, mock_get):
        with self.assertRaises(Exception):
            ApiClient().get("/api/stock/products/by-barcode/12345")


if __name__ == "__main__":
    unittest.main()
