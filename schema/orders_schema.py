
from pydantic import BaseModel, Field
from typing import List, Dict,Annotated
from decimal import Decimal
from enum import Enum

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: Annotated[int,Field(gt=0)]

class ShippingAddress(BaseModel):
    name: str
    line1: str
    line2: str = None
    city: str
    state: str
    postal_code: str
    country: str

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    shipping_address: ShippingAddress

class OrderItemRead(BaseModel):
    product_id: int
    quantity: int
    unit_price: Decimal

    class Config:
        orm_mode = True

class OrderRead(BaseModel):
    id: int
    user_id: int
    total_amount: Decimal
    shipping_address: Dict
    status: str
    items: List[OrderItemRead]

    class Config:
        orm_mode = True

class OrderStatusUpdate(BaseModel):
    new_status: str
    note: str = None


# class DeleteOrder(BaseModel):
#     roc:str