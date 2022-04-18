from pydantic import BaseModel


class Product(BaseModel):
    id: int
    stock_id: str = None
