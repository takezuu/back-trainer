from datetime import datetime
from typing import Any

from fastapi import HTTPException
from pydantic import field_validator
from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import ARRAY
from sqlmodel import Field, SQLModel, Column


class Orders(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    user_id: int = Field(index=True)
    items_ids: list[int] = Field(sa_column=Column(ARRAY(Integer)))
    order_date: datetime = Field(index=True)
    discount: float = Field(index=True)
    total_amount: float = Field(index=True)
    status: str = Field(index=True)
    delivery_address: str = Field(index=True)

class OrdersResponse(SQLModel, table=True):
    id: int | None = Field(primary_key=True, index=True)
    user_id: int | None = Field(index=True)
    items_ids: list[int] | None = Field(sa_column=Column(ARRAY(Integer)))
    order_date: str | None = Field(index=True)
    discount: float | None = Field(index=True)
    total_amount: float | None = Field(index=True)
    status: str | None = Field(index=True)
    delivery_address: str | None = Field(index=True)


class OrderResponse(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    user_id: int = Field(index=True)
    items: list[dict] = Field(sa_column=Column(ARRAY(Integer)))
    order_date: str = Field(index=True)
    discount: float = Field(index=True)
    total_amount: float = Field(index=True)
    status: str = Field(index=True)
    delivery_address: str = Field(index=True)


class OrderAdd(SQLModel):
    user_id: int = Field(index=True)
    items_ids: list[int] = Field(sa_column=Column(ARRAY(Integer)))
    order_date: datetime | None = Field(index=True, default=None)
    discount: float = Field(index=True)
    total_amount: float | None = Field(index=True, default=None)
    status: str = Field(index=True)
    delivery_address: str = Field(index=True)

    @field_validator("user_id")
    def validate_user_id(cls, value: int):
        if not isinstance(value, int):
            raise HTTPException(status_code=400, detail="User_id should be Int type")
        if value < 1:
            raise HTTPException(status_code=400, detail="Id should be greater than 0")
        return value

    @field_validator("items_ids")
    def validate_items_ids(cls, value: list):
        if not isinstance(value, list):
            raise HTTPException(status_code=400, detail="Items_ids should be List type")
        if len(value) <= 0 or len(value) > 15:
            raise HTTPException(status_code=400, detail="Array length should be from 1 to 15")
        return value

    @field_validator("discount")
    def validate_discount(cls, value: float):
        if not isinstance(value, float):
            raise HTTPException(status_code=400, detail="Discount should be Float type")
        if value < 0 or value > 80.0:
            raise HTTPException(status_code=400, detail="Discount should be more than 0 and less than 80")
        return value

    @field_validator("status")
    def validate_status(cls, value: str):
        if not isinstance(value, str):
            raise HTTPException(status_code=400, detail="Status should be Str type")
        if value not in ["created", "paid", "preparing", "ready", "in delivery", "delivered"]:
            raise HTTPException(status_code=400,
                                detail="Status can be only: pending, created, paid, ready, delivered, preparing")
        return value


    @field_validator("delivery_address")
    def validate_delivery_address(cls, value: str):
        if not isinstance(value, str):
            raise HTTPException(status_code=400, detail="Delivery address should be Str type")
        if len(value) < 1 or len(value) > 200:

            raise HTTPException(status_code=400,
                                detail="Delivery address length should be from 1 to 200 characters")
        return value


class OrderAddedResponse(SQLModel):
    id: int


class OrderPut(SQLModel):
    items_ids: list[int] = Field(sa_column=Column(ARRAY(Integer)))
    discount: float = Field(index=True)
    total_amount: float | None = Field(index=True, default=None)
    status: str = Field(index=True)
    delivery_address: str = Field(index=True)

    @field_validator("items_ids")
    def validate_items_ids(cls, value: list):
        if not isinstance(value, list):
            raise HTTPException(status_code=400, detail="Items_ids should be List type")
        if len(value) <= 0 or len(value) > 15:
            raise HTTPException(status_code=400, detail="Array length should be from 1 to 15")
        return value

    @field_validator("discount")
    def validate_discount(cls, value: float):
        if not isinstance(value, float):
            raise HTTPException(status_code=400, detail="Discount should be Float type")
        if value < 0 or value > 80.0:
            raise HTTPException(status_code=400, detail="Discount should be more than 0 and less than 80")
        return value

    @field_validator("status")
    def validate_status(cls, value: str):
        if not isinstance(value, str):
            raise HTTPException(status_code=400, detail="Status should be Str type")
        if value not in ["pending", "created", "paid", "ready", "delivered", "preparing", "active"]:
            raise HTTPException(status_code=400,
                                detail="Status can be only: pending, created, paid, ready, delivered, preparing")
        return value

    @field_validator("delivery_address")
    def validate_delivery_address(cls, value: str):
        if not isinstance(value, str):
            raise HTTPException(status_code=400, detail="Delivery address should be Str type")
        if len(value) < 1 or len(value) > 200:
            raise HTTPException(status_code=400,
                                detail="Delivery address length should be from 1 to 200 characters")
        return value


class OrderUpdatedResponse(SQLModel):
    message: str
    updated_order: OrdersResponse


class OrderPatch(SQLModel):
    items_ids: list[int] | None = Field(sa_column=Column(ARRAY(Integer)), default=None)
    discount: float | None = Field(index=True, default=None)
    total_amount: float | None = Field(index=True, default=None)
    status: str | None = Field(index=True, default=None)
    delivery_address: str | None = Field(index=True, default=None)

    @field_validator("items_ids")
    def validate_items_ids(cls, value: list):
        if not isinstance(value, list):
            raise HTTPException(status_code=400, detail="Items_ids should be List type")
        if len(value) <= 0 or len(value) > 15:
            raise HTTPException(status_code=400, detail="Array length should be from 1 to 15")
        return value

    @field_validator("discount")
    def validate_discount(cls, value: float):
        if not isinstance(value, float):
            raise HTTPException(status_code=400, detail="Discount should be Float type")
        if value < 0 or value > 80.0:
            raise HTTPException(status_code=400, detail="Discount should be more than 0 and less than 80")
        return value

    @field_validator("status")
    def validate_status(cls, value: str):
        if not isinstance(value, str):
            raise HTTPException(status_code=400, detail="Status should be Str type")
        if value not in ["pending", "created", "paid", "ready", "delivered", "preparing", "active"]:
            raise HTTPException(status_code=400,
                                detail="Status can be only: pending, created, paid, ready, delivered, preparing")
        return value

    @field_validator("delivery_address")
    def validate_delivery_address(cls, value: str):
        if not isinstance(value, str):
            raise HTTPException(status_code=400, detail="Delivery address should be Str type")
        if len(value) < 1 or len(value) > 200:
            raise HTTPException(status_code=400,
                                detail="Delivery address length should be from 1 to 200 characters")
        return value
