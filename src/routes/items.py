from typing import List, Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from sqlmodel import select

from src.dependencies.items import item_exists
from src.models.items import ItemsModels
from src.database import get_session

SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter()


@router.get("/api/items", tags=["items"], response_model=List[ItemsModels.Items])
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
    items = ItemsModels.Items
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


@router.get("/api/items/{item_id}", tags=["items"], response_model=ItemsModels.Items)
async def get_item(item: dict[str, Any] = Depends(item_exists)):
    return item


@router.post("/api/items", tags=["items"], status_code=status.HTTP_201_CREATED,
             response_model=ItemsModels.ItemAddedResponse)
async def create_user(item: ItemsModels.ItemAdd, session: SessionDep):
    db_item = ItemsModels.Items(**item.model_dump())

    if db_item.product_name:
        query = select(ItemsModels.Items).where(ItemsModels.Items.product_name == db_item.product_name)
        product_name_exists = session.exec(query).first() is not None
        if product_name_exists:
            raise HTTPException(status_code=409, detail="Product name is already use")

    try:
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
    except Exception as err:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'Failed create an item: {err}')
    return db_item
