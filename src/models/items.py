from fastapi import HTTPException
from pydantic import field_validator
from sqlmodel import Field, SQLModel


class ItemsModels:
    class Items(SQLModel, table=True):
        id: int = Field(primary_key=True, index=True)
        product_name: str = Field(index=True)
        description: str = Field(index=True)
        price: float = Field(index=True)
        quantity: int = Field(index=True)
        category: str = Field(index=True)
        item_color: str = Field(index=True)
        rating: int = Field(index=True)

    class ItemAddedResponse(SQLModel):
        id: int

    class ItemAdd(SQLModel):
        product_name: str = Field(index=True)
        description: str | None = Field(index=True, default=None)
        price: float = Field(index=True)
        quantity: int = Field(index=True)
        category: str = Field(index=True)
        item_color: str | None = Field(index=True, default=None)
        rating: int | None = Field(index=True, default=None)

        @field_validator("product_name")
        def validate_product_name(cls, value: str):
            if len(value) < 5 or len(value) > 100:
                raise HTTPException(status_code=400, detail="Product name length should be from 5 to 100 characters")
            if not isinstance(value, str):
                print(type(value))
                raise HTTPException(status_code=400, detail="Product name should be Str type")
            return value

        @field_validator("description")
        def validate_description(cls, value: str):
            if len(value) > 500:
                raise HTTPException(status_code=400, detail="Description length should be less than 500 characters")
            if not isinstance(value, str):
                raise HTTPException(status_code=400, detail="Description name should be Str type")
            return value

        @field_validator("price")
        def validate_price(cls, value: float):
            if value < 1.0 or value > 1_000_000.0:
                raise HTTPException(status_code=400, detail="Price should be more than 1 and less than 1 000 000")
            if not isinstance(value, float):
                raise HTTPException(status_code=400, detail="Price should be Float type")
            return value

        @field_validator("quantity")
        def validate_quantity(cls, value: int):
            if value < 1 or value > 1000:
                raise HTTPException(status_code=400, detail="Quantity should be more than 1 and less than 1000")
            if not isinstance(value, int):
                raise HTTPException(status_code=400, detail="Quantity should be Int type")
            return value

        @field_validator("category")
        def validate_category(cls, value: str):
            if len(value) < 1 or len(value) > 100:
                raise HTTPException(status_code=400, detail="Category length should be from 1 to 100 characters")
            if not value.isalpha():
                raise HTTPException(status_code=400, detail="Category consists from letters only")
            if not isinstance(value, str):
                raise HTTPException(status_code=400, detail="Category should be Str type")
            return value

        @field_validator("item_color")
        def validate_item_color(cls, value: str):
            if len(value) < 1 or len(value) > 20:
                raise HTTPException(status_code=400, detail="Item color length should be from 1 to 20 characters")
            if not value.isalpha():
                raise HTTPException(status_code=400, detail="Item color consists from letters only")
            if not isinstance(value, str):
                raise HTTPException(status_code=400, detail="Item color should be Str type")
            return value

        @field_validator("rating")
        def validate_rating(cls, value: int):
            if value < 1 or value > 5:
                raise HTTPException(status_code=400, detail="Rating should be more than 1 and less than 6")
            if not isinstance(value, int):
                raise HTTPException(status_code=400, detail="Rating should be Int type")
            return value
