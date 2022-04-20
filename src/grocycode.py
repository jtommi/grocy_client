import re
from enum import Enum

from src.product import Product


class CodeType(Enum):
    PRODUCT = "p"


PATTERN = re.compile(r"^grcy:([a-zA-Z]):(\d+)(?::(\w+))?$")


class GrocyCode:
    def __init__(self, code: str) -> None:
        self._parse_code(code)

    def _parse_code(self, code: str) -> None:
        matches = PATTERN.match(code)
        if not matches:
            raise ValueError(f"Invalid code: {code}")

        self.type = CodeType(matches[1])
        self.id = int(matches[2])
        self.detail = matches[3] if len(matches.groups()) == 3 else None

    def get_item(self) -> object:
        if self.type == CodeType.PRODUCT:
            return Product(id=self.id, stock_id=self.detail)
