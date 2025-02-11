from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from sqlmodel import Field, SQLModel, Column

class Orders(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    customer_id: int = Field(index=True)
    items_ids: list[int] = Field(sa_column=Column(JSON))
    order_date: datetime = Field(index=True)
    discount: int = Field(index=True)
    total_amount: float = Field(index=True)
    status: str = Field(index=True)
    delivery_address: str = Field(index=True)