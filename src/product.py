from pydantic import BaseModel
from src.api_client import APIException, ApiClient


class NoStockEntriesException(Exception):
    pass


class Product(BaseModel):
    id: int
    stock_id: str = None
    grocycode: str = None

    def open(self, amount: int = 1):
        api_client = ApiClient()
        data = {"amount": amount}
        if self.grocycode:
            path = f"/api/stock/products/by-barcode/{self.grocycode}/open"
        else:
            path = f"/api/stock/products/{self.id}/open"
        try:
            api_client.post(path=path, data=data)
        except APIException as e:
            if e.message == "No transaction was found by the given transaction id":
                raise NoStockEntriesException(
                    f"No stock entries found for product {self.id}, stock_id {self.stock_id}"
                )

    def consume(self, amount: int = 1, spoiled: bool = False):
        api_client = ApiClient()
        data = {"amount": amount, "transaction_type": "consume", "spoiled": spoiled}
        if self.grocycode:
            path = f"/api/stock/products/by-barcode/{self.grocycode}/consume"
        else:
            path = f"/api/stock/products/{self.id}/consume"
        api_client.post(path=path, data=data)
        try:
            api_client.post(path=path, data=data)
        except APIException as e:
            if (
                e.message
                == "Amount to be consumed cannot be > current stock amount (if supplied, at the desired location)"
            ):
                raise NoStockEntriesException(
                    f"No stock entries found for product {self.id}, stock_id {self.stock_id}"
                )

    def open_or_consume(self):
        api_client = ApiClient()
        path = f"/api/stock/products/{self.id}/entries"
        entries = api_client.get(path=path)
        if self.stock_id and entries:
            entries = [entry for entry in entries if entry["stock_id"] == self.stock_id]
        if not entries:
            raise NoStockEntriesException(
                f"No stock entries found for product {self.id}, stock_id {self.stock_id}"
            )
        opened = any([int(entry["open"]) > 0 for entry in entries])
        if opened:
            self.consume()
        else:
            self.open()
