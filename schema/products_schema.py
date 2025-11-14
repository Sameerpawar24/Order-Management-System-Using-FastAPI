from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    description: Optional[str]
    price: Decimal
    stock: int

class ProductRead(ProductCreate):
    id: int
    class Config:
        orm_mode = True

class StockUpdate(BaseModel):
    delta: int  # positive to add, negative to subtract
    note: Optional[str]
