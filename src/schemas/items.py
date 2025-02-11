from pydantic import BaseModel

class Items(BaseModel):
    id: int
    product_name: str
    description: str
    price: float
    quantity: int
    category: str
    item_color: str
    rating: int