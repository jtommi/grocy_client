import unittest

from src.grocycode import GrocyCode, CodeType
from src.product import Product


class TestGrocycode(unittest.TestCase):
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
        product = grocycode.get_item()
        self.assertIsInstance(product, Product)
        self.assertEqual(product.id, 1)
        self.assertEqual(product.stock_id, "x624f2505ded59")


if __name__ == "__main__":
    unittest.main()
