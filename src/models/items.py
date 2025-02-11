from sqlmodel import Field, SQLModel

class Items(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    product_name: str = Field(index=True)
    description: str = Field(index=True)
    price: float = Field(index=True)
    quantity: int = Field(index=True)
    category: str = Field(index=True)
    item_color: str = Field(index=True)
    rating: int = Field(index=True)
