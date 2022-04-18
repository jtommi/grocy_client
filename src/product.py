from pydantic import BaseModel
from src.api_client import ApiClient


class Product(BaseModel):
    id: int
    stock_id: str = None

    def open(self):
        api_client = ApiClient()
        api_client.get(path=f"/api/stock/products/{self.id}/open")
