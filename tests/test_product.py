import json
import re
import unittest
from unittest.mock import patch

from requests.models import Response
from src.product import Product


def mocked_request_get(*args, **kwargs):
    response_content = None
    request_url = kwargs.get("url", None)
    response_file = None
    if "/api/stock/products/by-barcode/" in request_url:
        response_file = "product.json"
    elif re.search(r".*/stock/products/\d+/entries$", request_url):
        response_file = "product_stock_entries.json"

    if response_file:
        with open(f"responses/{response_file}", "r") as f:
            response_content = json.load(f)
    else:
        response_content = {}

    response = Response()
    response.status_code = 200
    response._content = json.dumps(response_content).encode()
    return response


class TestProduct(unittest.TestCase):
    @patch("src.api_client.requests.get", side_effect=mocked_request_get)
    def test_open_product(self, mock_get):
        product = Product(id=2, stock_id="62505f88ea718")
        product.open()
        # Check that get was called with correct parameters
        mock_get.assert_called()
        self.assertTrue(mock_get.call_args.kwargs["url"].endswith("/open"))


if __name__ == "__main__":
    unittest.main()
