from datetime import date, datetime
from typing import List
from pydantic import BaseModel


class Users(BaseModel):
    id: int
    username: str
    email: str
    ip_address: str
    created_at: date
    last_login_time: str
    country_code: str
    phone: str


class Customers(BaseModel):
    id: int
    user_id: int
    first_name: str
    last_name: str
    address: str | None
    contact_phone: str | None
    date_of_birth: date | None


class Orders(BaseModel):
    id: int
    customer_id: int
    items_ids: List[int]
    order_date: datetime
    discount: float
    total_amount: float
    status: str
    delivery_address: str

class Items(BaseModel):
    id: int
    product_name: str
    description: str
    price: float
    quantity: int
    category: str
    item_color: str
    rating: int

