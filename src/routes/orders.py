from datetime import datetime
from typing import List, Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session,select

from src.models.items import ItemsModels
from src.schemas.orders import OrdersSchema, OrderByidSchema
from src.models.orders import OrdersModels
from src.database import get_session

SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter()


@router.get("/api/orders", tags=["orders"], response_model=List[OrdersSchema])
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
    orders = OrdersModels.Orders
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


@router.get("/api/orders/{order_id}", tags=["orders"], response_model=OrderByidSchema)
async def get_order(order_id: int, session: SessionDep):
    query = select(OrdersModels.Orders).where(OrdersModels.Orders.id == order_id)
    order = session.exec(query).first()
    items_data = []
    for item_id in order.items_ids:
        items = ItemsModels.Items
        query = select(items).where(items.id == item_id)
        item = session.exec(query).first()
        if item:
            item = item.model_dump()
            items_data.append(item)

    del order.items_ids
    order = order.model_dump()
    order["items"] = items_data
    return order
