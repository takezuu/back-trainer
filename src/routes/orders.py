from datetime import datetime
from typing import List, Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from sqlmodel import select
from src import schemas, models
from src.database import get_session

SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter()


@router.get("/api/orders", tags=["orders"], response_model=List[schemas.Orders])
async def get_orders(session: SessionDep,
                     order_date: datetime = None,
                     discount: float = None,
                     total_amount: float = None,
                     status: str = None,
                     delivery_address: str = None,
                     sort: str = "id",
                     order_by: str = "asc",
                     page: int = 1,
                     limit: int = 25
                     ):
    orders = models.Orders
    query = select(orders)

    if order_date:
        query = query.where(orders.order_date == order_date)
    if discount:
        query = query.where(orders.discount == discount)
    if total_amount:
        query = query.where(orders.total_amount == total_amount)
    if status:
        query = query.where(orders.status == status)
    if delivery_address:
        query = query.where(orders.delivery_address == delivery_address)

    order = getattr(orders, sort)
    if order_by == "desc":
        order = order.desc()
    query = query.order_by(order)

    query = query.offset((page - 1) * limit).limit(limit)
    return session.exec(query).all()


@router.get("/api/orders/{order_id}", tags=["orders"], response_model=schemas.OrderByid)
async def get_order(order_id: int, session: SessionDep):
    query = select(models.Orders).where(models.Orders.id == order_id)
    order = session.exec(query).first()

    items_data = []
    for item_id in order.items_ids:
        items = models.Items
        query = select(items).where(items.id == item_id)
        item = session.exec(query).first()
        if item:
            item = item.model_dump()
            items_data.append(item)

    del order.items_ids
    order = order.model_dump()
    order["items"] = items_data
    return order
