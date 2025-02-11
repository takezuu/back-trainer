from typing import List, Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from sqlmodel import select
from src import schemas, models
from src.database import get_session

SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter()


@router.get("/api/items", tags=["items"], response_model=List[schemas.Items])
async def get_items(session: SessionDep,
                    product_name: str = None,
                    price: float = None,
                    quantity: int = None,
                    category: str = None,
                    item_color: str = None,
                    rating: int = None,
                    sort: str = "id",
                    order_by: str = "asc",
                    page: int = 1,
                    limit: int = 25
                    ):
    items = models.Items
    query = select(items)

    if product_name:
        query = query.where(items.product_name == product_name)
    if price:
        query = query.where(items.price == price)
    if quantity:
        query = query.where(items.quantity == quantity)
    if category:
        query = query.where(items.category == category)
    if item_color:
        query = query.where(items.item_color == item_color)
    if rating:
        query = query.where(items.rating == rating)

    order = getattr(items, sort)
    if order_by == "desc":
        order = order.desc()
    query = query.order_by(order)

    query = query.offset((page - 1) * limit).limit(limit)
    return session.exec(query).all()


@router.get("/api/items/{item_id}", tags=["items"], response_model=schemas.Items)
async def get_item(item_id: int, session: SessionDep):
    statement = select(models.Items).where(models.Items.id == item_id)
    item = session.exec(statement).first()
    return item
