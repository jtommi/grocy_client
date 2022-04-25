import json
import re
import unittest
from unittest.mock import patch

from requests.models import Response
from src.grocycode import GrocyCode
from src.product import Product


def mocked_request(*args, **kwargs):
    response_content = None
    request_url = kwargs.get("url", None)
    response_file = None
    if "/api/stock/products/by-barcode/" in request_url:
        response_file = "product.json"
    elif re.search(r".*/stock/products/235/entries$", request_url):
        response_file = "product_stock_entries_open.json"

    if response_file:
        with open(f"tests/responses/{response_file}", "r") as f:
            response_content = json.load(f)
    else:
        response_content = {}

    response = Response()
    response.status_code = 200
    response._content = json.dumps(response_content).encode()
    return response


class TestProduct(unittest.TestCase):
    @patch("src.api_client.requests.post", side_effect=mocked_request)
    def test_open_product(self, mock_post):
        product = Product(id=235, stock_id="62505f88ea718")
        product.open()
        # Check that get was called with correct parameters
        mock_post.assert_called()
        self.assertIn("/open", mock_post.call_args.kwargs["url"])
        self.assertIn("235", mock_post.call_args.kwargs["url"])

    @patch("src.api_client.requests.post", side_effect=mocked_request)
    def test_open_product_by_barcode(self, mock_post):
        CODE = "grcy:p:1:x624f2505ded59"
        grocycode = GrocyCode(CODE)
        product = grocycode.get_item()
        product.open()
        # Check that get was called with correct parameters
        mock_post.assert_called()
        self.assertIn("/open", mock_post.call_args.kwargs["url"])
        self.assertIn("by-barcode", mock_post.call_args.kwargs["url"])
        self.assertIn("x624f2505ded59", mock_post.call_args.kwargs["url"])

    @patch("src.api_client.requests.post", side_effect=mocked_request)
    def test_consume_product(self, mock_post):
        product = Product(id=235, stock_id="62505f88ea718")
        product.consume()
        # Check that get was called with correct parameters
        mock_post.assert_called()
        self.assertIn("/consume", mock_post.call_args.kwargs["url"])
        self.assertIn("235", mock_post.call_args.kwargs["url"])

    @patch("src.api_client.requests.post", side_effect=mocked_request)
    def test_consume_product_by_barcode(self, mock_post):
        CODE = "grcy:p:1:x624f2505ded59"
        grocycode = GrocyCode(CODE)
        product = grocycode.get_item()
        product.consume()
        # Check that get was called with correct parameters
        mock_post.assert_called()
        self.assertRegex(mock_post.call_args.kwargs["url"], r".*/consume$")
        self.assertIn("by-barcode", mock_post.call_args.kwargs["url"])
        self.assertIn("x624f2505ded59", mock_post.call_args.kwargs["url"])


if __name__ == "__main__":
    unittest.main()
