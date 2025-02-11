from datetime import date, datetime
from sqlalchemy.dialects.postgresql import JSON
from sqlmodel import Field, SQLModel, Column


class Users(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    username: str = Field(index=True)
    email: str = Field(index=True)
    password_hash: str = Field(index=True)
    ip_address: str = Field(index=True)
    created_at: date = Field(index=True)
    last_login_time: str = Field(index=True)
    country_code: str = Field(index=True)
    phone: str = Field(index=True)


class Customers(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    user_id: int = Field(index=True)
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    address: str | None = Field(default=None, index=True)
    contact_phone: str | None = Field(default=None, index=True)
    date_of_birth: date | None = Field(default=None, index=True)


class Orders(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    customer_id: int = Field(index=True)
    items_ids: list[int] = Field(sa_column=Column(JSON))
    order_date: datetime = Field(index=True)
    discount: int = Field(index=True)
    total_amount: float = Field(index=True)
    status: str = Field(index=True)
    delivery_address: str = Field(index=True)


class Items(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    product_name: str = Field(index=True)
    description: str = Field(index=True)
    price: float = Field(index=True)
    quantity: int = Field(index=True)
    category: str = Field(index=True)
    item_color: str = Field(index=True)
    rating: int = Field(index=True)
