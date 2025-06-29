
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class ItemOrderBase(BaseModel):
    item_id: int
    customer_id: int
    order_quantity: int

class ItemOrderCreate(ItemOrderBase):
    pass

class ItemOrder(ItemOrderBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class ItemReorderLogBase(BaseModel):
    item_id: int

class ItemReorderLogCreate(ItemReorderLogBase):
    pass

class ItemReorderLog(ItemReorderLogBase):
    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    manufacturer_name: str
    manufacturer_email: str
    in_stock: int
    reorder_quantity: int

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    orders: List[ItemOrder] = []
    reorder_logs: List[ItemReorderLog] = []

    model_config = ConfigDict(from_attributes=True)

class CustomerBase(BaseModel):
    name: str
    address: str
    zip_code: str

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    orders: List[ItemOrder] = []

    model_config = ConfigDict(from_attributes=True)
