import json
import unittest
from unittest.mock import MagicMock, patch

from src.grocycode import GrocyCode
from src.product import NoStockEntriesException, Product, ProductNotExistsException


class TestProduct(unittest.TestCase):
    def setUp(self):
        response_files = {
            "stock_entries_open": "product_stock_entries_open.json",
            "stock_entries_not_open": "product_stock_entries_not_open.json",
        }
        self.response_data = {}
        for response, file in response_files.items():
            with open(f"tests/responses/{file}", "r") as f:
                self.response_data[response] = json.load(f)

    @patch("src.api_client.requests.post")
    def test_open_product(self, mock_post):
        mock_post.return_value = MagicMock(status_code=200)
        product = Product(id=235, stock_id="62505f88ea718")
        product.open()
        # Check that get was called with correct parameters
        mock_post.assert_called()
        self.assertIn("/open", mock_post.call_args.kwargs["url"])
        self.assertIn("235", mock_post.call_args.kwargs["url"])

    @patch("src.api_client.requests.post")
    def test_open_product_by_barcode(self, mock_post):
        mock_post.return_value = MagicMock(status_code=200)
        CODE = "grcy:p:1:x624f2505ded59"
        grocycode = GrocyCode(CODE)
        product = grocycode.get_item()
        product.open()
        # Check that get was called with correct parameters
        mock_post.assert_called()
        self.assertIn("/open", mock_post.call_args.kwargs["url"])
        self.assertIn("by-barcode", mock_post.call_args.kwargs["url"])
        self.assertIn("x624f2505ded59", mock_post.call_args.kwargs["url"])

    @patch("src.api_client.requests.post")
    def test_consume_product(self, mock_post):
        mock_post.return_value = MagicMock(status_code=200)
        product = Product(id=235, stock_id="62505f88ea718")
        product.consume()
        # Check that get was called with correct parameters
        mock_post.assert_called()
        self.assertIn("/consume", mock_post.call_args.kwargs["url"])
        self.assertIn("235", mock_post.call_args.kwargs["url"])

    @patch("src.api_client.requests.post")
    def test_consume_product_by_barcode(self, mock_post):
        mock_post.return_value = MagicMock(status_code=200)
        CODE = "grcy:p:1:x624f2505ded59"
        grocycode = GrocyCode(CODE)
        product = grocycode.get_item()
        product.consume()
        # Check that get was called with correct parameters
        mock_post.assert_called()
        self.assertRegex(mock_post.call_args.kwargs["url"], r".*/consume$")
        self.assertIn("by-barcode", mock_post.call_args.kwargs["url"])
        self.assertIn("x624f2505ded59", mock_post.call_args.kwargs["url"])

    @patch("src.api_client.requests.get")
    @patch("src.api_client.requests.post")
    def test_opens_when_not_open(self, mock_post, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: self.response_data["stock_entries_not_open"],
        )
        mock_post.return_value = MagicMock(status_code=200)
        product = Product(id=239, stock_id="62505f88ea718")
        product.open_or_consume()
        mock_post.assert_called()
        self.assertRegex(mock_post.call_args.kwargs["url"], r".*/open$")

    @patch("src.api_client.requests.get")
    @patch("src.api_client.requests.post")
    def test_consumes_when_open(self, mock_post, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: self.response_data["stock_entries_open"],
        )
        mock_post.return_value = MagicMock(status_code=200)
        product = Product(id=235, stock_id="62505f88ea718")
        product.open_or_consume()
        mock_post.assert_called()
        self.assertRegex(mock_post.call_args.kwargs["url"], r".*/consume$")

    @patch("src.api_client.requests.get")
    def test_open_or_consume_raises_on_no_entries(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: self.response_data["stock_entries_open"],
        )
        product = Product(id=235, stock_id="non_existing")
        with self.assertRaises(Exception) as exception:
            product.open_or_consume()
        self.assertIn("No stock entries found", str(exception.exception))

    @patch("src.api_client.requests.post")
    def test_open_and_consume_raise_on_inexisting_product(self, mock_post):
        mock_post.return_value = MagicMock(
            status_code=400,
            json=lambda: {"error_message": "Product does not exist or is inactive"},
        )
        product = Product(id=235)
        with self.assertRaises(ProductNotExistsException):
            product.open()
        with self.assertRaises(ProductNotExistsException):
            product.consume()

    @patch("src.api_client.requests.post")
    def test_open_and_consume_raise_on_inexisting_stock_entries(self, mock_post):
        mock_post.return_value = MagicMock(
            status_code=400,
            json=lambda: {
                "error_message": "No transaction was found by the given transaction id"
            },
        )
        product = Product(id=235)
        with self.assertRaises(NoStockEntriesException):
            product.open()
        mock_post.return_value = MagicMock(
            status_code=400,
            json=lambda: {
                "error_message": "Amount to be consumed cannot be > current stock amount (if supplied, at the desired location)"
            },
        )
        with self.assertRaises(NoStockEntriesException):
            product.consume()


if __name__ == "__main__":
    unittest.main()
