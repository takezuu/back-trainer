from datetime import datetime
from pydantic import BaseModel


class Orders(BaseModel):
    id: int
    customer_id: int
    items_ids: list[int]
    order_date: datetime
    discount: float
    total_amount: float
    status: str
    delivery_address: str

class OrderByid(BaseModel):
    id: int
    customer_id: int
    order_date: datetime
    discount: float
    total_amount: float
    status: str
    delivery_address: str
    items: list