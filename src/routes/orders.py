from datetime import datetime
from typing import List, Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session,select

from src.dependencies.orders import order_exists
from src.dependencies.users import user_exists
from src.models.items import ItemsModels
from src.models.orders import OrdersModels
from src.database import get_session

SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter()


@router.get("/api/orders", tags=["orders"], response_model=List[OrdersModels.Orders])
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


@router.get("/api/orders/{order_id}", tags=["orders"], response_model=OrdersModels.Orders)
async def get_order(session: SessionDep, order = Depends(order_exists)):
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

@router.post("/api/orders", tags=["items"], status_code=status.HTTP_201_CREATED,
             response_model=OrdersModels.OrderAddedResponse)
async def create_user(order: OrdersModels.OrderAdd, session: SessionDep):
    _ = user_exists(order.user_id)

    total_price = 0
    for item_id in order.items_ids:
        query = select(ItemsModels.Items.price).where(ItemsModels.Items.id == item_id)
        item_price = session.exec(query).first()
        total_price += item_price
    order_discount = total_price * (order.discount/100)
    total_price = total_price - order_discount

    order.total_amount = total_price
    db_order = OrdersModels.Orders(**order.model_dump())

    try:
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
    except Exception as err:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'Failed create an order: {err}')
    return db_order
