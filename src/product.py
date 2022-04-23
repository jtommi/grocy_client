from pydantic import BaseModel
from src.api_client import ApiClient


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
        api_client.post(path=path, data=data)

    def consume(self, amount: int = 1, spoiled: bool = False):
        api_client = ApiClient()
        data = {"amount": amount, "transaction_type": "consume", "spoiled": spoiled}
        if self.grocycode:
            path = f"/api/stock/products/by-barcode/{self.grocycode}/consume"
        else:
            path = f"/api/stock/products/{self.id}/consume"
        api_client.post(path=path, data=data)
