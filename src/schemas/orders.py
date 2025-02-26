from datetime import datetime
from pydantic import BaseModel


class OrdersSchema(BaseModel):
    id: int
    user_id: int
    items_ids: list[int]
    order_date: datetime
    discount: float
    total_amount: float
    status: str
    delivery_address: str

class OrderByidSchema(BaseModel):
    id: int
    user_id: int
    order_date: datetime
    discount: float
    total_amount: float
    status: str
    delivery_address: str
    items: list