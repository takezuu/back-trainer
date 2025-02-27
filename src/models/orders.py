from datetime import datetime

from fastapi import HTTPException
from pydantic import field_validator
from pydantic_core.core_schema import is_instance_schema
from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from sqlmodel import Field, SQLModel, Column


class OrdersModels:
    class Orders(SQLModel, table=True):
        id: int = Field(primary_key=True, index=True)
        user_id: int = Field(index=True)
        items_ids: list[int] = Field(sa_column=Column(ARRAY(Integer)))
        order_date: datetime = Field(index=True)
        discount: float = Field(index=True)
        total_amount: float = Field(index=True)
        status: str = Field(index=True)
        delivery_address: str = Field(index=True)

    class OrderAdd(SQLModel):
        user_id: int = Field(index=True)
        items_ids: list[int]  = Field(sa_column=Column(ARRAY(Integer)))
        order_date: datetime = Field(index=True, default_factory=lambda: datetime.now().replace(microsecond=0))
        discount: float = Field(index=True)
        total_amount: float | None = None
        status: str = Field(index=True)
        delivery_address: str = Field(index=True)

        @field_validator("user_id")
        def validate_user_id(cls, value: int):
            if value < 1:
                raise HTTPException(status_code=400, detail="Id should be greater than 0")
            if not isinstance(value, int):
                raise HTTPException(status_code=400, detail="User_id should be Int type")
            return value

        @field_validator("items_ids")
        def validate_items_ids(cls, value: list):
            count = 0
            for i in value:
                if not isinstance(i, int):
                    raise HTTPException(status_code=400,
                                        detail=f"All elements in items_ids should be Int type. Problem in this {count}th element {i}")
                count += 1
            if not isinstance(value, list):
                raise HTTPException(status_code=400, detail="Items_ids should be List type")
            return value

        @field_validator("discount")
        def validate_discount(cls, value: float):
            if  value < 0 or value > 80.0:
                raise HTTPException(status_code=400, detail="Discount should be more than 1 and less than 80")
            if not isinstance(value, float):
                raise HTTPException(status_code=400, detail="Discount should be Float type")
            return value

        @field_validator("status")
        def validate_status(cls, value: str):
            if value not in ["pending", "created", "paid", "ready", "delivered", "preparing"]:
                raise HTTPException(status_code=400,
                                    detail="Status can be only: pending, created, paid, ready, delivered, preparing")
            if not isinstance(value, str):
                raise HTTPException(status_code=400, detail="Status should be Str type")
            return value

        @field_validator("delivery_address")
        def validate_delivery_address(cls, value: str):
            if len(value) < 1 or len(value) > 200:
                raise HTTPException(status_code=400,
                                    detail="Delivery address length should be from 1 to 200 characters")
            if not isinstance(value, str):
                raise HTTPException(status_code=400, detail="Delivery address should be Str type")
            return value

    class OrderAddedResponse(SQLModel):
        id: int
