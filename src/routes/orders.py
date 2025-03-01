from datetime import datetime
from typing import List, Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select

from src.dependencies.orders import order_exists
from src.models.items import Items
from src.models.orders import Orders, OrderAddedResponse, OrderAdd, OrdersResponse
from src.database import get_session
from src.models.users import Users

SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter()


@router.get("/api/orders", tags=["orders"], response_model=List[Orders])
async def get_orders(session: SessionDep,
                     order_date: datetime = None,
                     discount: float = None,
                     total_amount: float = None,
                     status: str = None,
                     delivery_address: str = None,
                     item_id: int = None,
                     sort: str = "id",
                     order_by: str = "asc",
                     page: int = 1,
                     limit: int = 25
                     ):
    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be greater than or equl to 1")
    if limit < 1:
        raise HTTPException(status_code=400, detail="Limit must be greater than or equl to 1")

    orders = Orders
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
    if item_id:
        query = query.where(orders.items_ids.contains([item_id]))

    order = getattr(orders, sort)
    if order_by == "desc":
        order = order.desc()
    query = query.order_by(order)

    query = query.offset((page - 1) * limit).limit(limit)
    return session.exec(query).all()


@router.get("/api/orders/{order_id}", tags=["orders"], response_model=OrdersResponse)
async def get_order(session: SessionDep, order=Depends(order_exists)):
    items_data = []
    for item_id in order.items_ids:
        items = Items
        query = select(items).where(items.id == item_id)
        item = session.exec(query).first()
        if item:
            item = item.model_dump()
            items_data.append(item)

    del order.items_ids # delete old field
    order = order.model_dump()
    order["items"] = items_data # recreate new
    return order


@router.post("/api/orders", tags=["orders"], status_code=status.HTTP_201_CREATED,
             response_model=OrderAddedResponse)
async def create_order(order: OrderAdd, session: SessionDep):
    query = select(Users).where(Users.id == order.user_id)
    user = session.exec(query).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    order.order_date = datetime.now().replace(microsecond=0)

    if not order.items_ids:
        raise HTTPException(status_code=400, detail="Items array should have at least one element")

    total_price = 0
    for item_id in order.items_ids:
        query = select(Items.price).where(Items.id == item_id)
        item_price = session.exec(query).first()
        if not item_price:
            raise HTTPException(status_code=404, detail="Item not found")
        total_price += item_price
    order_discount = total_price * (order.discount / 100)
    total_price = total_price - order_discount

    order.total_amount = total_price
    db_order = Orders(**order.model_dump())

    try:
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
    except Exception as err:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'Failed create an order: {err}')
    return db_order


@router.delete("/api/orders/{order_id}", tags=["orders"], status_code=status.HTTP_200_OK)
async def delete_order(session: SessionDep, order=Depends(order_exists)):
    try:
        session.delete(order)
        session.commit()
        return {"message": "Order deleted successfully"}
    except Exception as err:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))