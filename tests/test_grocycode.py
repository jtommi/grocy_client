import unittest
from unittest.mock import patch

from src.grocycode import (
    CodeType,
    GrocyCode,
    InvalidGrocyCodeException,
    NotAProductException,
    UnknownCodeTypeException,
)
from src.product import Product


class TestGrocycode(unittest.TestCase):
    def test_code_prints_right(self):
        CODE = "grcy:p:1:x624f2505ded59"
        grocycode = GrocyCode(CODE)
        self.assertEqual(str(grocycode), CODE)

    def test_code_parsing_without_detail(self):
        CODE = "grcy:p:1"
        grocycode = GrocyCode(CODE)
        self.assertEqual(grocycode.type, CodeType.PRODUCT)
        self.assertEqual(grocycode.id, 1)
        self.assertIsNone(grocycode.detail)

    def test_code_parsing_with_detail(self):
        CODE = "grcy:p:1:x624f2505ded59"
        grocycode = GrocyCode(CODE)
        self.assertEqual(grocycode.type, CodeType.PRODUCT)
        self.assertEqual(grocycode.id, 1)
        self.assertEqual(grocycode.detail, "x624f2505ded59")

    def test_code_returns_product(self):
        CODE = "grcy:p:1:x624f2505ded59"
        grocycode = GrocyCode(CODE)
        product = grocycode.get_product()
        self.assertIsInstance(product, Product)
        self.assertEqual(product.id, 1)
        self.assertEqual(product.stock_id, "x624f2505ded59")

    def test_invalid_code_raises_exception(self):
        CODE = "123"
        with self.assertRaises(InvalidGrocyCodeException):
            GrocyCode(CODE)

    def test_unknown_code_type_raises_exception(self):
        CODE = "grcy:x:1:x624f2505ded59"
        with self.assertRaises(UnknownCodeTypeException) as error:
            GrocyCode(CODE)

        self.assertEqual(str(error.exception), "Unknown code type: 'x'")

    def test_not_a_product_raises_exception(self):
        CODE = "grcy:p:1"
        grocy_code = GrocyCode(CODE)

        with patch.object(grocy_code, "type", None):
            with self.assertRaises(NotAProductException) as error:
                grocy_code.get_product()

        self.assertIn(f"Not a product code: '{CODE}'", str(error.exception))


if __name__ == "__main__":
    unittest.main()
